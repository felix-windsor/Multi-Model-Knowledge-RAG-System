"""Deterministic relation confidence scoring."""

from __future__ import annotations

from app.rag_core.schemas import RELATION_COMPATIBILITY, RELATION_TYPES, Entity, Relation


def score_relation(relation: Relation, entities: list[Entity] | dict[str, str] | set[str]) -> Relation:
    """Score relation quality from deterministic evidence instead of trusting the LLM."""
    entity_types = _entity_type_lookup(entities)
    entity_names = set(entity_types)
    missing = [
        endpoint
        for endpoint in (relation.source, relation.target)
        if endpoint not in entity_names
    ]
    self_relation = relation.source == relation.target
    compatible = True
    if not missing and not self_relation:
        compatible = _is_compatible_relation(
            relation.type,
            entity_types.get(relation.source, "其他"),
            entity_types.get(relation.target, "其他"),
        )
    valid = not missing and not self_relation and compatible

    confidence = 0.35
    if relation.type in RELATION_TYPES:
        confidence += 0.05
    if relation.description.strip():
        confidence += 0.15
    if relation.evidence.strip():
        confidence += 0.10
    if relation.drift_reason:
        confidence -= 0.05
    if valid:
        confidence += 0.25
    else:
        confidence -= 0.25

    invalid_reason = None
    if self_relation:
        invalid_reason = "self relation"
    elif missing:
        invalid_reason = f"missing endpoint: {', '.join(missing)}"
    elif not compatible:
        invalid_reason = (
            "incompatible relation: "
            f"{entity_types.get(relation.source, '其他')} -{relation.type}-> "
            f"{entity_types.get(relation.target, '其他')}"
        )

    return relation.model_copy(
        update={
            "confidence": max(0.0, min(1.0, round(confidence, 4))),
            "valid": valid,
            "invalid_reason": invalid_reason,
        }
    )


def _entity_type_lookup(entities: list[Entity] | dict[str, str] | set[str]) -> dict[str, str]:
    if isinstance(entities, dict):
        return dict(entities)
    if isinstance(entities, set):
        return {entity_name: "其他" for entity_name in entities}
    return {entity.name: entity.type for entity in entities}


def _is_compatible_relation(relation_type: str, source_type: str, target_type: str) -> bool:
    if relation_type == "关联":
        return True
    rule = RELATION_COMPATIBILITY.get(relation_type)
    if not rule:
        return True
    return source_type in rule["source"] and target_type in rule["target"]
