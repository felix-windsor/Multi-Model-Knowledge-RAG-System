"""Entity normalization and merge utilities."""

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
    """Merge duplicate/alias entities and rewrite relation endpoints."""
    merged: list[Entity] = []
    alias_to_canonical: dict[str, str] = {}

    for entity in entities:
        normalized_name = normalize_entity_name(entity.name)
        if not normalized_name:
            continue

        normalized_aliases = {
            normalize_entity_name(alias)
            for alias in entity.aliases + [entity.name]
            if normalize_entity_name(alias)
        }

        match_index = _find_merge_target(normalized_name, normalized_aliases, merged)
        normalized_entity = entity.model_copy(
            update={"name": normalized_name, "aliases": sorted(normalized_aliases - {normalized_name})}
        )

        if match_index is None:
            merged.append(normalized_entity)
            alias_to_canonical[normalized_name] = normalized_name
            for alias in normalized_entity.aliases:
                alias_to_canonical[alias] = normalized_name
            continue

        existing = merged[match_index]
        canonical = _choose_canonical_entity(existing, normalized_entity)
        aliases = set(existing.aliases) | set(normalized_entity.aliases) | {existing.name, normalized_entity.name}
        aliases.discard(canonical.name)

        merged[match_index] = canonical.model_copy(update={"aliases": sorted(aliases)})
        for alias in aliases | {existing.name, normalized_entity.name, canonical.name}:
            alias_to_canonical[alias] = canonical.name

    normalized_relations = [
        relation.model_copy(
            update={
                "source": alias_to_canonical.get(
                    normalize_entity_name(relation.source),
                    normalize_entity_name(relation.source),
                ),
                "target": alias_to_canonical.get(
                    normalize_entity_name(relation.target),
                    normalize_entity_name(relation.target),
                ),
            }
        )
        for relation in relations
    ]

    return merged, normalized_relations, alias_to_canonical


def _find_merge_target(name: str, aliases: set[str], entities: list[Entity]) -> int | None:
    for index, entity in enumerate(entities):
        existing_names = {entity.name, *entity.aliases}
        if name in existing_names or aliases & existing_names:
            return index
        if _is_near_duplicate(name, entity.name):
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
    if len(right.name) > len(left.name):
        winner, loser = right, left
    else:
        winner, loser = left, right

    entity_type = winner.type if winner.type != "其他" else loser.type
    description = winner.description if len(winner.description) >= len(loser.description) else loser.description
    source_chunk_id = winner.source_chunk_id or loser.source_chunk_id
    return winner.model_copy(
        update={
            "type": entity_type,
            "description": description,
            "source_chunk_id": source_chunk_id,
        }
    )
