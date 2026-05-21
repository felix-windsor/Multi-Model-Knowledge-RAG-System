"""Evaluation helpers for custom Graph RAG extraction results."""

from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any

from app.rag_core.schemas import ExtractionResult


def aggregate_metrics(results: list[ExtractionResult]) -> dict[str, Any]:
    if not results:
        return {}

    metrics = [result.metrics for result in results]
    total_entities_before = sum(item.entities_before_normalization for item in metrics)
    total_entities_after = sum(item.entities_after_normalization for item in metrics)
    total_relations_before = sum(item.relations_before_filtering for item in metrics)
    total_relations = sum(item.relations_after_filtering for item in metrics)
    entity_type_drift_count = sum(item.entity_type_drift_count for item in metrics)
    relation_type_drift_count = sum(item.relation_type_drift_count for item in metrics)
    invalid_relation_count = sum(item.invalid_relation_count for item in metrics)

    return {
        "json_parse_success_rate": _rate(sum(item.json_parse_success for item in metrics), len(metrics)),
        "schema_validation_success_rate": _rate(sum(item.schema_validation_success for item in metrics), len(metrics)),
        "entity_type_drift_count": entity_type_drift_count,
        "entity_type_drift_rate": _rate(entity_type_drift_count, total_entities_before),
        "relation_type_drift_count": relation_type_drift_count,
        "relation_type_drift_rate": _rate(relation_type_drift_count, total_relations_before),
        "entity_dedup_rate": _rate(total_entities_before - total_entities_after, total_entities_before),
        "invalid_relation_count": invalid_relation_count,
        "invalid_relation_rate": _rate(invalid_relation_count, total_relations),
        "top_entity_type_drifts": top_entity_type_drifts(results),
        "top_relation_type_drifts": top_relation_type_drifts(results),
        "avg_elapsed_ms": round(mean(item.elapsed_ms for item in metrics), 3),
        "avg_entities": round(mean(item.entities_after_normalization for item in metrics), 3),
        "avg_relations": round(mean(item.relations_after_filtering for item in metrics), 3),
        "avg_relation_confidence": avg_relation_confidence(results),
    }


def avg_relation_confidence(results: list[ExtractionResult]) -> float:
    values = [
        relation.confidence
        for result in results
        for relation in result.relations
    ]
    return round(mean(values), 4) if values else 0.0


def top_entity_type_drifts(results: list[ExtractionResult]) -> list[dict[str, Any]]:
    counter: Counter[tuple[str, str]] = Counter()
    for result in results:
        for entity in result.entities:
            if entity.raw_type and entity.raw_type != entity.type:
                counter[(entity.raw_type, entity.type)] += 1
    return [
        {"raw_type": raw_type, "canonical_type": canonical_type, "count": count}
        for (raw_type, canonical_type), count in counter.most_common(10)
    ]


def top_relation_type_drifts(results: list[ExtractionResult]) -> list[dict[str, Any]]:
    counter: Counter[tuple[str, str]] = Counter()
    for result in results:
        for relation in result.relations:
            if relation.raw_type and relation.raw_type != relation.type:
                counter[(relation.raw_type, relation.type)] += 1
    return [
        {"raw_type": raw_type, "canonical_type": canonical_type, "count": count}
        for (raw_type, canonical_type), count in counter.most_common(10)
    ]


def _rate(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)
