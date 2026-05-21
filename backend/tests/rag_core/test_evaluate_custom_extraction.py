from app.rag_core.schemas import Entity, ExtractionMetrics, ExtractionResult, Relation
from app.rag_core.evaluation import aggregate_metrics


def test_aggregate_metrics_reports_drift_and_invalid_relation_rates():
    results = [
        ExtractionResult(
            entities=[
                Entity(name="综合管理系统", type="系统", raw_type="业务系统", canonical_type="系统"),
                Entity(name="统一身份认证平台", type="平台"),
            ],
            relations=[
                Relation(
                    source="综合管理系统",
                    target="统一身份认证平台",
                    type="调用",
                    raw_type="使用",
                    canonical_type="调用",
                    confidence=0.9,
                ),
                Relation(source="综合管理系统", target="统一身份认证平台", type="关联", confidence=0.6),
            ],
            metrics=ExtractionMetrics(
                json_parse_success=True,
                schema_validation_success=True,
                entity_type_drift_count=1,
                relation_type_drift_count=1,
                entities_before_normalization=3,
                entities_after_normalization=2,
                relations_before_filtering=2,
                relations_after_filtering=2,
                invalid_relation_count=1,
                elapsed_ms=10,
            ),
        ),
        ExtractionResult(
            entities=[Entity(name="审计服务", type="服务")],
            relations=[Relation(source="审计服务", target="审计服务", type="关联", confidence=0.2)],
            metrics=ExtractionMetrics(
                json_parse_success=True,
                schema_validation_success=True,
                entity_type_drift_count=0,
                relation_type_drift_count=0,
                entities_before_normalization=1,
                entities_after_normalization=1,
                relations_before_filtering=1,
                relations_after_filtering=1,
                invalid_relation_count=1,
                elapsed_ms=20,
            ),
        ),
    ]

    aggregate = aggregate_metrics(results)

    assert aggregate["entity_type_drift_rate"] == 0.25
    assert aggregate["relation_type_drift_rate"] == 0.3333
    assert aggregate["entity_dedup_rate"] == 0.25
    assert aggregate["invalid_relation_rate"] == 0.6667
    assert aggregate["top_entity_type_drifts"] == [{"raw_type": "业务系统", "canonical_type": "系统", "count": 1}]
    assert aggregate["top_relation_type_drifts"] == [{"raw_type": "使用", "canonical_type": "调用", "count": 1}]
