"""LightRAG subclass that funnels raw extraction through rag_core v2.

LightRAG exposes no entity_extract_func / on_extract callback, so the only
clean way to interpose schema-v2 normalization is to subclass LightRAG and
override the internal hook that already exists: ``_process_extract_entities``.
We let LightRAG run its native extraction (its prompt, its parser, its
caching), then post-process the raw ``(maybe_nodes, maybe_edges)`` tuples
before LightRAG's downstream ``merge_nodes_and_edges`` step ingests them.

Parent method (LightRAG 1.4.x) — discovered via inspect.getsource:

    async def _process_extract_entities(
        self,
        chunk: dict[str, Any],
        pipeline_status=None,
        pipeline_status_lock=None,
    ) -> list

Return value is a list with one entry per chunk processed concurrently
inside ``extract_entities``. Each entry is a ``(maybe_nodes, maybe_edges)``
tuple with this shape:

    maybe_nodes: dict[entity_name_str, list[entity_dict]]
        entity_dict keys (per `_handle_single_entity_extraction`):
            entity_name, entity_type, description,
            source_id, file_path, timestamp
        NOTE: LightRAG lowercases entity_type *before* we see it.
              (`entity_type = entity_type.replace(" ", "").lower()`)

    maybe_edges: dict[(src_id, tgt_id), list[relationship_dict]]
        relationship_dict keys (per `_handle_single_relationship_extraction`):
            src_id, tgt_id, weight, description,
            keywords, source_id, file_path, timestamp
        NOTE: keywords are NOT lowercased. We canonicalize the first
              comma-separated keyword as the relation type.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from pydantic import ValidationError

from lightrag.lightrag import LightRAG

from app.rag_core.normalizer import normalize_entities_and_relations
from app.rag_core.relation_scorer import score_relation
from app.rag_core.schemas import (
    ENTITY_TYPE_ALIASES,
    ENTITY_TYPES,
    Entity,
    Relation,
    canonicalize_entity_type,
    canonicalize_relation_type,
)


logger = logging.getLogger(__name__)


# ── Case-insensitive entity-type lookup ──────────────────────────────────
# LightRAG lowercases entity_type during its native parse, so a direct
# ENTITY_TYPES membership check on "system" would miss the canonical "System".
# This module-level lookup table fixes that without touching schemas.py.


def _build_ci_entity_lookup() -> dict[str, tuple[str, str | None]]:
    lookup: dict[str, tuple[str, str | None]] = {}
    for canonical in ENTITY_TYPES:
        lookup[canonical.casefold()] = (canonical, None)
    for alias, canonical in ENTITY_TYPE_ALIASES.items():
        key = alias.casefold()
        # Direct-canonical hit wins over alias mapping for the same key.
        if key not in lookup:
            lookup[key] = (canonical, "mapped_alias")
    return lookup


_CI_ENTITY_LOOKUP = _build_ci_entity_lookup()


def _canonicalize_entity_type_ci(raw_type: str | None) -> tuple[str, str | None]:
    """Case-insensitive canonicalization for entity types.

    Falls back to ``canonicalize_entity_type`` for unknown types so the
    'unknown_entity_type' drift reason matches the rest of rag_core.
    """
    value = (raw_type or "").strip()
    if not value:
        return canonicalize_entity_type(None)
    hit = _CI_ENTITY_LOOKUP.get(value.casefold())
    if hit is not None:
        return hit
    return canonicalize_entity_type(value)


class LightRAGWrapper(LightRAG):
    """LightRAG subclass that applies rag_core v2 normalization to
    raw extraction results before LightRAG merges them into the KG.

    Per-chunk pipeline (applied to each ``(maybe_nodes, maybe_edges)``):
      1. Convert LightRAG dicts → rag_core Entity / Relation models.
      2. Canonicalize types (v2 schema, case-insensitive for entities).
      3. ``normalize_entities_and_relations`` (homonym fix + same-type merge).
      4. ``score_relation`` (annotate confidence + validity; do NOT drop —
         keep LightRAG's existing pruning policy in charge).
      5. Convert back to LightRAG's dict shape; expose drift / confidence /
         validity via ``_rag_core_*`` keys for downstream observability.
    """

    async def _process_extract_entities(
        self,
        chunk: dict[str, Any],
        pipeline_status: dict | None = None,
        pipeline_status_lock: Any = None,
    ) -> list:
        chunk_results = await super()._process_extract_entities(
            chunk,
            pipeline_status=pipeline_status,
            pipeline_status_lock=pipeline_status_lock,
        )
        return self._apply_rag_core_v2(chunk_results)

    # ── Pure transform functions (no LightRAG state) ─────────────────────
    # Kept as staticmethods so they're trivially testable without a full
    # LightRAG instance (which requires real storage backends to construct).

    @staticmethod
    def _apply_rag_core_v2(chunk_results: list) -> list:
        """Normalize a list of ``(maybe_nodes, maybe_edges)`` tuples.

        Defensive contract:
          - Empty / falsy input → returned unchanged.
          - Non-list input → returned unchanged with a logger.warning.
          - Per-tuple normalization failure → that tuple is replaced by the
            raw input (logger.error); other tuples continue.
        Never raises.
        """
        if not chunk_results:
            return chunk_results
        if not isinstance(chunk_results, list):
            logger.warning(
                "LightRAGWrapper: unexpected chunk_results type %s; passing through",
                type(chunk_results).__name__,
            )
            return chunk_results

        cleaned: list = []
        for index, item in enumerate(chunk_results):
            try:
                cleaned.append(LightRAGWrapper._clean_chunk(item))
            except Exception as exc:  # noqa: BLE001 — defensive fall-through
                logger.error(
                    "LightRAGWrapper: rag_core normalization failed for "
                    "chunk_results[%d]: %s; falling back to raw chunk",
                    index, exc, exc_info=True,
                )
                cleaned.append(item)
        return cleaned

    @staticmethod
    def _clean_chunk(item: Any) -> tuple[dict, dict]:
        try:
            maybe_nodes, maybe_edges = item
        except (TypeError, ValueError):
            logger.warning(
                "LightRAGWrapper: chunk item is not a (nodes, edges) tuple; "
                "passing through unchanged"
            )
            return item

        if not isinstance(maybe_nodes, dict) or not isinstance(maybe_edges, dict):
            logger.warning(
                "LightRAGWrapper: nodes/edges are not dicts (got %s / %s); "
                "passing through chunk unchanged",
                type(maybe_nodes).__name__, type(maybe_edges).__name__,
            )
            return item

        entities = LightRAGWrapper._to_rag_core_entities(maybe_nodes)
        relations, relation_meta = LightRAGWrapper._to_rag_core_relations(maybe_edges)

        norm_entities, norm_relations, _alias_map = normalize_entities_and_relations(
            entities, relations
        )
        scored_relations = [
            score_relation(rel, norm_entities) for rel in norm_relations
        ]

        new_nodes = LightRAGWrapper._to_lightrag_nodes(norm_entities)
        new_edges = LightRAGWrapper._to_lightrag_edges(scored_relations, relation_meta)
        return new_nodes, new_edges

    # ── LightRAG dict → rag_core model ───────────────────────────────────

    @staticmethod
    def _to_rag_core_entities(
        maybe_nodes: dict[str, list[dict]],
    ) -> list[Entity]:
        """Flatten LightRAG ``maybe_nodes`` into rag_core Entity instances.

        LightRAG-specific metadata (file_path, timestamp) is stashed under
        ``Entity.attributes`` with a ``_lr_`` prefix so it survives the
        round-trip even when ``_choose_canonical_entity`` picks a winner
        and drops the loser's per-instance metadata.
        """
        entities: list[Entity] = []
        for entity_name, dups in maybe_nodes.items():
            for ed in dups:
                raw_type = str(ed.get("entity_type", "") or "")
                canonical_type, drift = _canonicalize_entity_type_ci(raw_type)
                try:
                    entities.append(
                        Entity(
                            name=str(ed.get("entity_name") or entity_name),
                            type=canonical_type,
                            raw_type=raw_type,
                            canonical_type=canonical_type,
                            description=str(ed.get("description", "") or ""),
                            drift_reason=drift,
                            source_chunk_id=ed.get("source_id"),
                            attributes={
                                "_lr_file_path": ed.get("file_path", "unknown_source"),
                                "_lr_timestamp": ed.get("timestamp", 0),
                            },
                        )
                    )
                except ValidationError as exc:
                    logger.warning(
                        "LightRAGWrapper: skipping malformed entity %r: %s",
                        ed, exc,
                    )
        return entities

    @staticmethod
    def _to_rag_core_relations(
        maybe_edges: dict[tuple[str, str], list[dict]],
    ) -> tuple[list[Relation], list[dict]]:
        """Flatten LightRAG ``maybe_edges`` into rag_core Relation instances.

        Returns ``(relations, original_dicts)`` in parallel order. The
        normalizer preserves relation order (it does not merge or drop
        relations), so the two lists stay aligned for the round trip.
        """
        relations: list[Relation] = []
        meta: list[dict] = []
        for (src, tgt), edges in maybe_edges.items():
            for rd in edges:
                # LightRAG packs keyword candidates as comma-separated text.
                # Treat the first one as the candidate relation type; the
                # full string is preserved on round-trip via _to_lightrag_edges.
                raw_keywords = str(rd.get("keywords", "") or "")
                raw_type = (
                    raw_keywords.split(",", 1)[0].strip() if raw_keywords else ""
                )
                canonical_type, drift = canonicalize_relation_type(raw_type or None)
                try:
                    relations.append(
                        Relation(
                            source=str(rd.get("src_id") or src),
                            target=str(rd.get("tgt_id") or tgt),
                            type=canonical_type,
                            raw_type=raw_type,
                            canonical_type=canonical_type,
                            description=str(rd.get("description", "") or ""),
                            drift_reason=drift,
                            source_chunk_id=rd.get("source_id"),
                        )
                    )
                    meta.append(rd)
                except ValidationError as exc:
                    logger.warning(
                        "LightRAGWrapper: skipping malformed relation %r: %s",
                        rd, exc,
                    )
        return relations, meta

    # ── rag_core model → LightRAG dict ───────────────────────────────────

    @staticmethod
    def _to_lightrag_nodes(entities: list[Entity]) -> dict[str, list[dict]]:
        """Reassemble normalized entities into LightRAG's ``maybe_nodes`` shape.

        Re-keys by the (possibly renamed) canonical entity name so any
        homonym ``[type]`` suffix becomes the live identity downstream.
        Observability fields ``_rag_core_raw_type`` and ``_rag_core_drift_reason``
        are added so the sidecar / monitoring layer can audit drift.
        """
        new_nodes: dict[str, list[dict]] = defaultdict(list)
        for ent in entities:
            attrs = ent.attributes or {}
            new_nodes[ent.name].append(
                {
                    "entity_name": ent.name,
                    "entity_type": ent.type,  # v2 canonical, preserved case
                    "description": ent.description,
                    "source_id": ent.source_chunk_id or "",
                    "file_path": attrs.get("_lr_file_path", "unknown_source"),
                    "timestamp": attrs.get("_lr_timestamp", 0),
                    "_rag_core_raw_type": ent.raw_type,
                    "_rag_core_drift_reason": ent.drift_reason,
                }
            )
        return dict(new_nodes)

    @staticmethod
    def _to_lightrag_edges(
        scored_relations: list[Relation],
        original_meta: list[dict],
    ) -> dict[tuple[str, str], list[dict]]:
        """Reassemble scored relations into LightRAG's ``maybe_edges`` shape.

        The new keys use the (possibly homonym-rewritten) (source, target)
        pair. The original LightRAG fields (weight, file_path, timestamp,
        full keyword list) are preserved from the parallel meta list.
        """
        new_edges: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for rel, orig in zip(scored_relations, original_meta):
            key = (rel.source, rel.target)
            new_edges[key].append(
                {
                    "src_id": rel.source,
                    "tgt_id": rel.target,
                    "weight": orig.get("weight", 1.0),
                    "description": rel.description or orig.get("description", ""),
                    # Preserve original keyword string so LightRAG's keyword
                    # retrieval still works; expose canonical type separately.
                    "keywords": orig.get("keywords", ""),
                    "source_id": rel.source_chunk_id or orig.get("source_id", ""),
                    "file_path": orig.get("file_path", "unknown_source"),
                    "timestamp": orig.get("timestamp", 0),
                    "_rag_core_canonical_type": rel.type,
                    "_rag_core_raw_type": rel.raw_type,
                    "_rag_core_drift_reason": rel.drift_reason,
                    "_rag_core_confidence": rel.confidence,
                    "_rag_core_valid": rel.valid,
                }
            )
        return dict(new_edges)
