"""Entity normalization and merge utilities.

Identity model:
    An entity's identity is the composite (name, type) — NOT name alone.
    Two entities are the same node only when both name and type match.
    Same name + different type = a homonym and must be preserved as
    separate nodes (each renamed to ``"{name}[{type}]"`` for unique
    addressing). This mirrors production knowledge-graph practice of
    using hash(name + type) as a stable node identifier.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher

from app.rag_core.schemas import Entity, Relation


WRAPPER_CHARS = "\"'`“”‘’《》〈〉（）()[]【】{}"


def normalize_entity_name(name: str) -> str:
    """Normalize entity names for deterministic matching."""
    value = str(name or "").strip()
    value = value.strip(WRAPPER_CHARS)
    value = re.sub(r"\s+", "", value)
    value = re.sub(r"[，,。；;：:]+$", "", value)
    return value.strip()


def normalize_entities_and_relations(
    entities: list[Entity],
    relations: list[Relation],
) -> tuple[list[Entity], list[Relation], dict[str, str]]:
    """Merge duplicate/alias entities (type-aware) and rewrite relation endpoints.

    Behavior:
    - Same (name, type) or name overlap via aliases with same type → merge.
    - Near-duplicate names with same type → merge.
    - Same name but different type → kept as separate entities; each is
      renamed to ``"{name}[{type}]"`` so the canonical name is unique.
    - Relation endpoints pointing to a name with homonym conflicts resolve
      to the first matching disambiguated entity; relation.drift_reason
      is set to ``"homonym_ambiguous"`` so downstream evaluation can flag it.
    """
    merged: list[Entity] = []
    # Maps any lookup name (canonical or alias) → list of indices into ``merged``.
    # Multiple indices indicate a homonym conflict; relation rewriting uses this
    # to detect ambiguity and pick a fallback.
    name_to_indices: dict[str, list[int]] = {}

    for entity in entities:
        normalized_name = normalize_entity_name(entity.name)
        if not normalized_name:
            continue

        normalized_aliases = {
            normalize_entity_name(alias)
            for alias in entity.aliases + [entity.name]
            if normalize_entity_name(alias)
        }

        match_index = _find_merge_target(
            normalized_name, entity.type, normalized_aliases, merged
        )
        normalized_entity = entity.model_copy(
            update={
                "name": normalized_name,
                "aliases": sorted(normalized_aliases - {normalized_name}),
            }
        )

        if match_index is None:
            merged.append(normalized_entity)
            new_index = len(merged) - 1
            for key in {normalized_name} | normalized_aliases:
                _register_index(name_to_indices, key, new_index)
            continue

        existing = merged[match_index]
        canonical = _choose_canonical_entity(existing, normalized_entity)
        aliases = (
            set(existing.aliases)
            | set(normalized_entity.aliases)
            | {existing.name, normalized_entity.name}
        )
        aliases.discard(canonical.name)

        merged[match_index] = canonical.model_copy(update={"aliases": sorted(aliases)})
        for key in {normalized_name, canonical.name} | normalized_aliases:
            _register_index(name_to_indices, key, match_index)

    # ── Homonym disambiguation ────────────────────────────────────────────
    # Any primary name shared by 2+ merged entities is a homonym. Each gets
    # a "{name}[{type}]" suffix so it remains uniquely addressable.
    name_owners: dict[str, list[int]] = {}
    for idx, entity in enumerate(merged):
        name_owners.setdefault(entity.name, []).append(idx)

    for shared_name, indices in name_owners.items():
        if len(indices) < 2:
            continue
        for idx in indices:
            ent = merged[idx]
            merged[idx] = ent.model_copy(
                update={"name": f"{ent.name}[{ent.type}]"}
            )

    # ── Legacy alias_to_canonical map (for backward-compat return value) ──
    # Maps each lookup name to ONE canonical name. For ambiguous (homonym)
    # names this is the first occurrence — relation rewriting uses
    # ``name_to_indices`` directly so it can detect and flag ambiguity.
    alias_to_canonical: dict[str, str] = {}
    for entity in merged:
        alias_to_canonical.setdefault(entity.name, entity.name)
        for alias in entity.aliases:
            alias_to_canonical.setdefault(alias, entity.name)

    # ── Relation endpoint rewriting ───────────────────────────────────────
    normalized_relations: list[Relation] = []
    for relation in relations:
        src_resolved, src_ambig = _resolve_endpoint(
            normalize_entity_name(relation.source), name_to_indices, merged
        )
        tgt_resolved, tgt_ambig = _resolve_endpoint(
            normalize_entity_name(relation.target), name_to_indices, merged
        )
        drift_reason = relation.drift_reason
        if src_ambig or tgt_ambig:
            drift_reason = "homonym_ambiguous"
        normalized_relations.append(
            relation.model_copy(
                update={
                    "source": src_resolved,
                    "target": tgt_resolved,
                    "drift_reason": drift_reason,
                }
            )
        )

    return merged, normalized_relations, alias_to_canonical


def _register_index(
    name_to_indices: dict[str, list[int]],
    key: str,
    index: int,
) -> None:
    """Add ``index`` to ``name_to_indices[key]`` without duplicates."""
    bucket = name_to_indices.setdefault(key, [])
    if index not in bucket:
        bucket.append(index)


def _resolve_endpoint(
    name: str,
    name_to_indices: dict[str, list[int]],
    merged: list[Entity],
) -> tuple[str, bool]:
    """Resolve a raw relation endpoint name to a canonical merged-entity name.

    Returns (resolved_name, is_ambiguous):
      - 0 candidates  → return name as-is, not ambiguous (endpoint may be missing,
                        handled later by relation_scorer).
      - 1 candidate   → return its current canonical name, not ambiguous.
      - 2+ candidates → homonym; return the first match's name + flag ambiguous.
    """
    indices = name_to_indices.get(name)
    if not indices:
        return name, False
    if len(indices) == 1:
        return merged[indices[0]].name, False
    return merged[indices[0]].name, True


def _find_merge_target(
    name: str,
    entity_type: str,
    aliases: set[str],
    entities: list[Entity],
) -> int | None:
    """Find a merge target with type-aware matching.

    Returns the index of an existing entity whose ``type`` matches and whose
    name/aliases overlap with the incoming entity's name/aliases (either
    exactly or via near-duplicate string similarity). Returns ``None`` when
    no merge candidate exists — including the homonym case where name
    overlaps but type differs.
    """
    for index, existing in enumerate(entities):
        if existing.type != entity_type:
            continue
        existing_names = {existing.name, *existing.aliases}
        if name in existing_names or aliases & existing_names:
            return index
        if _is_near_duplicate(name, existing.name):
            return index
    return None


def _is_near_duplicate(left: str, right: str) -> bool:
    if not left or not right:
        return False
    if left in right or right in left:
        shorter, longer = sorted((left, right), key=len)
        return len(longer) - len(shorter) <= 3
    return SequenceMatcher(None, left, right).ratio() >= 0.86


def _choose_canonical_entity(left: Entity, right: Entity) -> Entity:
    """Pick the canonical entity when merging two same-type entities.

    Preference order: longer name → richer description → either source_chunk_id.
    Both inputs are guaranteed to share the same ``type`` (caller enforces
    type-aware matching), so no type-reconciliation is needed.
    """
    if len(right.name) > len(left.name):
        winner, loser = right, left
    else:
        winner, loser = left, right

    description = (
        winner.description
        if len(winner.description) >= len(loser.description)
        else loser.description
    )
    source_chunk_id = winner.source_chunk_id or loser.source_chunk_id
    return winner.model_copy(
        update={
            "description": description,
            "source_chunk_id": source_chunk_id,
        }
    )
