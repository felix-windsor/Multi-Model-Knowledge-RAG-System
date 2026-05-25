"""Tests for deterministic relation confidence scoring."""

from app.rag_core.relation_scorer import score_relation
from app.rag_core.schemas import Entity, Relation


def _entities() -> list[Entity]:
    return [
        Entity(name="CheckoutRequirement", type="FunctionalRequirement"),
        Entity(name="CheckoutModule", type="Module"),
        Entity(name="CheckoutApi", type="Interface"),
        Entity(name="OrderRecord", type="DataEntity"),
        Entity(name="SupportAgent", type="Stakeholder"),
    ]


def test_score_relation_full_evidence_reaches_perfect_confidence():
    relation = Relation(
        source="CheckoutRequirement",
        target="CheckoutModule",
        type="ImplementedBy",
        raw_type="ImplementedBy",
        canonical_type="ImplementedBy",
        description="CheckoutRequirement is implemented by CheckoutModule.",
        evidence="CheckoutRequirement is implemented by CheckoutModule",
    )

    scored = score_relation(
        relation,
        _entities(),
        chunk_text="The CheckoutRequirement is implemented by CheckoutModule.",
    )

    assert scored.confidence == 1.0
    assert scored.valid is True
    assert scored.invalid_reason is None


def test_score_relation_requires_evidence_to_appear_in_chunk_when_available():
    relation = Relation(
        source="CheckoutRequirement",
        target="CheckoutModule",
        type="ImplementedBy",
        raw_type="ImplementedBy",
        canonical_type="ImplementedBy",
        description="CheckoutRequirement is implemented by CheckoutModule.",
        evidence="not present in the source document",
    )

    scored = score_relation(
        relation,
        _entities(),
        chunk_text="The CheckoutRequirement is implemented by CheckoutModule.",
    )

    assert scored.confidence == 0.7
    assert scored.valid is True


def test_score_relation_marks_missing_endpoint_invalid_even_if_other_scores_pass():
    relation = Relation(
        source="MissingRequirement",
        target="CheckoutModule",
        type="ImplementedBy",
        raw_type="ImplementedBy",
        canonical_type="ImplementedBy",
        description="MissingRequirement is implemented by CheckoutModule.",
        evidence="MissingRequirement is implemented by CheckoutModule",
    )

    scored = score_relation(
        relation,
        _entities(),
        chunk_text="MissingRequirement is implemented by CheckoutModule.",
    )

    assert scored.confidence == 0.5
    assert scored.valid is False
    assert scored.invalid_reason == "missing endpoint: MissingRequirement"


def test_score_relation_marks_schema_incompatible_relation_invalid():
    relation = Relation(
        source="SupportAgent",
        target="OrderRecord",
        type="Manipulates",
        raw_type="Manipulates",
        canonical_type="Manipulates",
        description="SupportAgent manipulates OrderRecord during checkout support.",
        evidence="SupportAgent manipulates OrderRecord",
    )

    scored = score_relation(
        relation,
        _entities(),
        chunk_text="SupportAgent manipulates OrderRecord during checkout support.",
    )

    assert scored.confidence == 0.6
    assert scored.valid is False
    assert (
        scored.invalid_reason
        == "incompatible relation: Stakeholder -Manipulates-> DataEntity"
    )


def test_score_relation_penalizes_unknown_relation_type_after_canonicalization():
    relation = Relation(
        source="CheckoutRequirement",
        target="CheckoutModule",
        type="RelatedTo",
        raw_type="teleports_to",
        canonical_type="RelatedTo",
        description="CheckoutRequirement is connected with CheckoutModule.",
        evidence="CheckoutRequirement is connected with CheckoutModule",
        drift_reason="unknown_relation_type",
    )

    scored = score_relation(
        relation,
        _entities(),
        chunk_text="CheckoutRequirement is connected with CheckoutModule.",
    )

    assert scored.confidence == 0.9
    assert scored.valid is True


def test_score_relation_rejects_generic_description_for_description_score():
    relation = Relation(
        source="CheckoutRequirement",
        target="CheckoutModule",
        type="ImplementedBy",
        raw_type="ImplementedBy",
        canonical_type="ImplementedBy",
        description="related to",
        evidence="CheckoutRequirement is implemented by CheckoutModule",
    )

    scored = score_relation(
        relation,
        _entities(),
        chunk_text="CheckoutRequirement is implemented by CheckoutModule.",
    )

    assert scored.confidence == 0.9
    assert scored.valid is True
