"""Deterministic relation confidence scoring."""

from __future__ import annotations

from app.rag_core.schemas import (
    RELATION_COMPATIBILITY,
    Entity,
    Relation,
    canonicalize_relation_type,
)


def score_relation(
    relation: Relation,
    entities: list[Entity] | dict[str, str] | set[str],
    chunk_text: str | None = None,
) -> Relation:
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
            entity_types.get(relation.source, "Other"),
            entity_types.get(relation.target, "Other"),
        )

    schema_score = 1.0 if not missing and not self_relation and compatible else 0.0
    evidence_score = _evidence_score(relation.evidence, chunk_text)
    endpoint_score = 0.0 if missing or self_relation else 1.0
    type_score = _relation_type_score(relation)
    description_score = _description_score(relation.description)

    confidence = (
        0.40 * schema_score
        + 0.30 * evidence_score
        + 0.10 * endpoint_score
        + 0.10 * type_score
        + 0.10 * description_score
    )

    invalid_reason = None
    if self_relation:
        invalid_reason = "self relation"
    elif missing:
        invalid_reason = f"missing endpoint: {', '.join(missing)}"
    elif not compatible:
        invalid_reason = (
            "incompatible relation: "
            f"{entity_types.get(relation.source, 'Other')} -{relation.type}-> "
            f"{entity_types.get(relation.target, 'Other')}"
        )

    hard_invalid = invalid_reason is not None
    confidence = max(0.0, min(1.0, round(confidence, 4)))
    valid = confidence >= 0.5 and not hard_invalid

    return relation.model_copy(
        update={
            "confidence": confidence,
            "valid": valid,
            "invalid_reason": invalid_reason,
        }
    )


def _entity_type_lookup(entities: list[Entity] | dict[str, str] | set[str]) -> dict[str, str]:
    if isinstance(entities, dict):
        return dict(entities)
    if isinstance(entities, set):
        return {entity_name: "Other" for entity_name in entities}
    return {entity.name: entity.type for entity in entities}


def _is_compatible_relation(relation_type: str, source_type: str, target_type: str) -> bool:
    if relation_type == "RelatedTo":
        return True
    rule = RELATION_COMPATIBILITY.get(relation_type)
    if not rule:
        return False
    return source_type in rule["source"] and target_type in rule["target"]


def _relation_type_score(relation: Relation) -> float:
    raw_type = relation.raw_type or relation.type
    _canonical, drift_reason = canonicalize_relation_type(raw_type)
    return 0.0 if drift_reason == "unknown_relation_type" else 1.0


def _evidence_score(evidence: str, chunk_text: str | None) -> float:
    normalized_evidence = _normalize_text(evidence)
    if not normalized_evidence:
        return 0.0
    if chunk_text is None:
        return 1.0
    return 1.0 if normalized_evidence in _normalize_text(chunk_text) else 0.0


def _description_score(description: str) -> float:
    normalized = _normalize_text(description)
    if len(normalized) < 12:
        return 0.0
    generic = {
        "related to",
        "associated with",
        "has relationship",
        "has relation",
        "is related to",
        "关联",
        "相关",
        "有关系",
    }
    return 0.0 if normalized in generic else 1.0


def _normalize_text(value: str) -> str:
    return " ".join(str(value or "").casefold().split())
