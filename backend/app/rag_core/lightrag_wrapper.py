"""LightRAG subclass that replaces native extraction with GraphRAGExtractor.

History
-------
Phase B (Tasks 3.1 / 3.2):
    The wrapper let LightRAG run its native extraction and post-processed
    the raw ``(maybe_nodes, maybe_edges)`` tuples through rag_core
    (canonicalize → normalize → score). End-to-end testing showed this
    was insufficient: LightRAG's default prompt drives the LLM to emit
    its own ontology (``concept`` / ``method`` / ``artifact`` …) that
    isn't in v2 ENTITY_TYPES or the alias table, so the cleanup layer
    drowned in "Other" buckets.

Phase C (this file, Task 3.3):
    The wrapper REPLACES native extraction by routing each chunk
    through ``GraphRAGExtractor.extract_chunk()`` — the same component
    the sidecar already uses. The LLM is constrained at the prompt
    level (bilingual prompt + 7 hard rules + tier-grouped type list),
    so its output is already v2 canonical and no post-mapping is needed.
    ``normalize_entities_and_relations`` and ``score_relation`` are
    already invoked *inside* the extractor; we only translate the
    resulting ``ExtractionResult`` back to LightRAG's dict shape.

The phase-B helpers (``_apply_rag_core_v2`` and friends) are kept below
under the **DEPRECATED** banner. They are no longer on the hot path but
still exposed for: (a) defensive fall-back, (b) ingest of pre-existing
LightRAG-style chunk_results from other sources, (c) the existing unit
tests that pin their behavior. Do not call them from new code.

Parent contract (LightRAG 1.4.x) — verified via ``inspect.getsource``
-------------------------------------------------------------------
    async def _process_extract_entities(
        self,
        chunk: dict[str, Any],   # actually a *batch* of chunks keyed by chunk_id
        pipeline_status=None,
        pipeline_status_lock=None,
    ) -> list[tuple[dict, dict]]

Each chunk value is a ``TextChunkSchema`` TypedDict:
    {tokens: int, content: str, full_doc_id: str, chunk_order_index: int}
(LightRAG also reads ``file_path`` with a default fallback, so the field
is optional but commonly present.)

Output shape — one tuple per chunk in the batch, same order as input:
    maybe_nodes: dict[entity_name_str, list[entity_dict]]
    maybe_edges: dict[(src_id, tgt_id), list[relationship_dict]]
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from pydantic import ValidationError

from lightrag.lightrag import LightRAG

from app.rag_core.extractor import ExtractionConfig, GraphRAGExtractor
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


# ─────────────────────────────────────────────────────────────────────────
# Case-insensitive entity-type lookup (DEPRECATED, kept for phase-B path)
# ─────────────────────────────────────────────────────────────────────────
# LightRAG's native parser lowercases entity_type before our wrapper sees it.
# In phase C we don't call that parser, so the live extraction path no
# longer needs this. Left in place as a safety net for ``_apply_rag_core_v2``
# which can still be invoked manually on legacy chunk_results.


def _build_ci_entity_lookup() -> dict[str, tuple[str, str | None]]:
    lookup: dict[str, tuple[str, str | None]] = {}
    for canonical in ENTITY_TYPES:
        lookup[canonical.casefold()] = (canonical, None)
    for alias, canonical in ENTITY_TYPE_ALIASES.items():
        key = alias.casefold()
        if key not in lookup:
            lookup[key] = (canonical, "mapped_alias")
    return lookup


_CI_ENTITY_LOOKUP = _build_ci_entity_lookup()


def _canonicalize_entity_type_ci(raw_type: str | None) -> tuple[str, str | None]:
    """Case-insensitive canonicalization for entity types (phase-B helper)."""
    value = (raw_type or "").strip()
    if not value:
        return canonicalize_entity_type(None)
    hit = _CI_ENTITY_LOOKUP.get(value.casefold())
    if hit is not None:
        return hit
    return canonicalize_entity_type(value)


class LightRAGWrapper(LightRAG):
    """LightRAG subclass that runs extraction through ``GraphRAGExtractor``.

    Live path (phase C, default for ``_process_extract_entities``):
      1. For each chunk in the batch, call ``extractor.extract_chunk(text)``.
      2. ``GraphRAGExtractor`` already canonicalizes types, runs
         ``normalize_entities_and_relations`` (homonym fix + same-type merge)
         and ``score_relation`` (confidence + validity).
      3. Convert the ``ExtractionResult`` back to LightRAG's
         ``(maybe_nodes, maybe_edges)`` dict shape so downstream
         ``merge_nodes_and_edges`` is unchanged.

    Fall-back path (phase B, exposed but not on the hot path):
      ``_apply_rag_core_v2(chunk_results)`` still accepts LightRAG-native
      raw extraction tuples and applies post-process canonicalization.
      Use only when you have legacy chunk_results from outside the
      wrapper (e.g. archived extraction snapshots).
    """

    # ── Live extraction path ─────────────────────────────────────────────

    async def _process_extract_entities(
        self,
        chunk: dict[str, Any],
        pipeline_status: dict | None = None,
        pipeline_status_lock: Any = None,
    ) -> list[tuple[dict, dict]]:
        """Replace LightRAG's native extraction with ``GraphRAGExtractor``.

        Signature mirrors the parent's exactly so downstream callers that
        pass positional / keyword args keep working. ``pipeline_status`` /
        ``pipeline_status_lock`` are accepted but currently unused —
        per-chunk progress logs go through the module logger.
        """
        extractor = GraphRAGExtractor(
            llm_func=self.llm_model_func,
            config=ExtractionConfig(drop_invalid_relations=False),
        )

        chunk_results: list[tuple[dict, dict]] = []
        for chunk_id, chunk_data in chunk.items():
            text = ""
            file_path = "unknown_source"
            if isinstance(chunk_data, dict):
                text = str(chunk_data.get("content", "") or "")
                file_path = str(chunk_data.get("file_path", "unknown_source") or "unknown_source")

            if not text:
                logger.info(
                    "LightRAGWrapper: chunk %s has empty content; skipping extraction",
                    chunk_id,
                )
                chunk_results.append(({}, {}))
                continue

            try:
                result = await extractor.extract_chunk(text, chunk_id=chunk_id)
            except Exception as exc:  # noqa: BLE001 — per-chunk isolation
                logger.error(
                    "LightRAGWrapper: GraphRAGExtractor failed for chunk %s: "
                    "%s: %s; yielding empty result so the batch continues",
                    chunk_id, type(exc).__name__, exc, exc_info=True,
                )
                chunk_results.append(({}, {}))
                continue

            # Call the converters via the class (not ``self``) so the live
            # method stays usable with a minimal mock-self in unit tests —
            # the converters don't read any instance state anyway.
            maybe_nodes = LightRAGWrapper._entities_to_maybe_nodes(
                result.entities, chunk_id=chunk_id, file_path=file_path
            )
            maybe_edges = LightRAGWrapper._relations_to_maybe_edges(
                result.relations, chunk_id=chunk_id, file_path=file_path
            )
            chunk_results.append((maybe_nodes, maybe_edges))

            logger.info(
                "Chunk %s extracted %d Ent + %d Rel (via GraphRAGExtractor)",
                chunk_id, len(result.entities), len(result.relations),
            )

        return chunk_results

    # ── ExtractionResult → LightRAG dict converters ──────────────────────

    @staticmethod
    def _entities_to_maybe_nodes(
        entities: list[Entity],
        chunk_id: str,
        file_path: str,
    ) -> dict[str, list[dict]]:
        """Convert a rag_core ``Entity`` list to LightRAG's ``maybe_nodes`` shape.

        ``entity.type`` is the live, post-normalization type (same string as
        ``entity.canonical_type`` for results out of ``GraphRAGExtractor``),
        and ``entity.name`` already carries the ``[type]`` disambiguation
        suffix for homonyms — so the dict ``entity_name`` and the outer key
        match the canonical identity.
        """
        nodes: dict[str, list[dict]] = defaultdict(list)
        for ent in entities:
            nodes[ent.name].append(
                {
                    "entity_name": ent.name,
                    "entity_type": ent.type,  # v2 canonical, preserved case
                    "description": ent.description,
                    "source_id": chunk_id,
                    "file_path": file_path,
                    "timestamp": 0,
                    # Observability fields used by sidecar / monitoring layers.
                    "_rag_core_raw_type": ent.raw_type,
                    "_rag_core_canonical_type": ent.canonical_type,
                    "_rag_core_drift_reason": ent.drift_reason,
                }
            )
        return dict(nodes)

    @staticmethod
    def _relations_to_maybe_edges(
        relations: list[Relation],
        chunk_id: str,
        file_path: str,
    ) -> dict[tuple[str, str], list[dict]]:
        """Convert a rag_core ``Relation`` list to LightRAG's ``maybe_edges`` shape.

        We expose ``rel.canonical_type`` as both the ``keywords`` field
        (which LightRAG uses for keyword retrieval) and as
        ``_rag_core_canonical_type`` for explicit downstream consumption.
        ``rel.confidence`` becomes the edge weight when non-zero;
        otherwise we default to 1.0 to keep LightRAG's neutral weight.
        """
        edges: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for rel in relations:
            weight = float(rel.confidence) if rel.confidence else 1.0
            description = rel.description or rel.evidence or ""
            keywords = rel.canonical_type or rel.type
            edges[(rel.source, rel.target)].append(
                {
                    "src_id": rel.source,
                    "tgt_id": rel.target,
                    "weight": weight,
                    "description": description,
                    "keywords": keywords,
                    "source_id": chunk_id,
                    "file_path": file_path,
                    "timestamp": 0,
                    "_rag_core_canonical_type": rel.canonical_type,
                    "_rag_core_raw_type": rel.raw_type,
                    "_rag_core_confidence": rel.confidence,
                    "_rag_core_valid": rel.valid,
                    "_rag_core_drift_reason": rel.drift_reason,
                }
            )
        return dict(edges)

    # ─────────────────────────────────────────────────────────────────────
    # DEPRECATED (phase-B path): post-process LightRAG-native chunk_results.
    #
    # These helpers are NOT called by the live ``_process_extract_entities``
    # above. They remain so legacy callers (and the unit tests that lock
    # their behavior) keep working, and so we have a fall-back if we ever
    # need to re-ingest LightRAG-style ``(maybe_nodes, maybe_edges)``
    # tuples produced elsewhere (e.g. archived extraction snapshots).
    # ─────────────────────────────────────────────────────────────────────

    @staticmethod
    def _apply_rag_core_v2(chunk_results: list) -> list:
        """DEPRECATED — phase-B post-processor for LightRAG-native chunk_results.

        Kept for fall-back / legacy ingestion. The live extraction path
        no longer needs this because GraphRAGExtractor already applies
        canonicalize → normalize → score during extraction itself.
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
        """DEPRECATED — phase-B per-chunk post-processor."""
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

    @staticmethod
    def _to_rag_core_entities(
        maybe_nodes: dict[str, list[dict]],
    ) -> list[Entity]:
        """DEPRECATED — phase-B LightRAG-dict → rag_core Entity conversion."""
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
        """DEPRECATED — phase-B LightRAG-dict → rag_core Relation conversion."""
        relations: list[Relation] = []
        meta: list[dict] = []
        for (src, tgt), edges in maybe_edges.items():
            for rd in edges:
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

    @staticmethod
    def _to_lightrag_nodes(entities: list[Entity]) -> dict[str, list[dict]]:
        """DEPRECATED — phase-B rag_core Entity → LightRAG dict reassembly."""
        new_nodes: dict[str, list[dict]] = defaultdict(list)
        for ent in entities:
            attrs = ent.attributes or {}
            new_nodes[ent.name].append(
                {
                    "entity_name": ent.name,
                    "entity_type": ent.type,
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
        """DEPRECATED — phase-B rag_core Relation → LightRAG dict reassembly."""
        new_edges: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for rel, orig in zip(scored_relations, original_meta):
            key = (rel.source, rel.target)
            new_edges[key].append(
                {
                    "src_id": rel.source,
                    "tgt_id": rel.target,
                    "weight": orig.get("weight", 1.0),
                    "description": rel.description or orig.get("description", ""),
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
