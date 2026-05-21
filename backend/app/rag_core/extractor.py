"""Main orchestration for custom entity/relation extraction."""

from __future__ import annotations

import inspect
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from pydantic import ValidationError

from app.rag_core.json_repair import repair_json_payload
from app.rag_core.normalizer import normalize_entities_and_relations, normalize_entity_name
from app.rag_core.prompts import build_extraction_prompt
from app.rag_core.relation_scorer import score_relation
from app.rag_core.schemas import (
    Entity,
    ExtractionMetrics,
    ExtractionResult,
    Relation,
    canonicalize_entity_type,
    canonicalize_relation_type,
)


LLMFunc = Callable[..., Awaitable[Any] | Any]


@dataclass(frozen=True)
class ExtractionConfig:
    """Runtime knobs for the custom extraction layer."""

    drop_invalid_relations: bool = False


class GraphRAGExtractor:
    """Custom extraction pipeline for Chinese enterprise document chunks."""

    def __init__(self, llm_func: LLMFunc, config: ExtractionConfig | None = None):
        self.llm_func = llm_func
        self.config = config or ExtractionConfig()

    async def extract_chunk(self, chunk_text: str, chunk_id: str | None = None) -> ExtractionResult:
        started = time.perf_counter()
        prompt = build_extraction_prompt(chunk_text, chunk_id=chunk_id)
        raw_response = await self._call_llm(prompt)
        repair_result = repair_json_payload(raw_response)

        metrics = ExtractionMetrics(json_parse_success=repair_result.success)
        if not repair_result.success:
            metrics.elapsed_ms = _elapsed_ms(started)
            return ExtractionResult(metrics=metrics)

        try:
            entities, relations, drift = self._coerce_payload(repair_result.payload, chunk_id)
        except ValidationError:
            metrics.elapsed_ms = _elapsed_ms(started)
            return ExtractionResult(metrics=metrics)

        metrics.schema_validation_success = True
        metrics.entity_type_drift_count = drift["entity_type"]
        metrics.relation_type_drift_count = drift["relation_type"]
        metrics.entities_before_normalization = len(entities)
        metrics.relations_before_filtering = len(relations)

        entities, relations, _ = normalize_entities_and_relations(entities, relations)
        scored_relations = [score_relation(relation, entities) for relation in relations]
        if self.config.drop_invalid_relations:
            scored_relations = [relation for relation in scored_relations if relation.valid]

        metrics.entities_after_normalization = len(entities)
        metrics.invalid_relation_count = sum(1 for relation in scored_relations if not relation.valid)
        metrics.relations_after_filtering = len(scored_relations)
        metrics.elapsed_ms = _elapsed_ms(started)

        return ExtractionResult(entities=entities, relations=scored_relations, metrics=metrics)

    async def _call_llm(self, prompt: str) -> Any:
        result = self.llm_func(prompt)
        if inspect.isawaitable(result):
            return await result
        return result

    def _coerce_payload(
        self,
        payload: dict[str, Any],
        chunk_id: str | None,
    ) -> tuple[list[Entity], list[Relation], dict[str, int]]:
        entity_drift = 0
        relation_drift = 0
        entities: list[Entity] = []
        relations: list[Relation] = []

        for raw_entity in payload.get("entities", []) or []:
            if not isinstance(raw_entity, dict):
                continue
            raw_type = str(raw_entity.get("type") or raw_entity.get("entity_type") or "其他").strip()
            entity_type, drift_reason = canonicalize_entity_type(raw_type)
            if drift_reason:
                entity_drift += 1
            entity = Entity.model_validate(
                {
                    "name": normalize_entity_name(raw_entity.get("name") or raw_entity.get("entity_name")),
                    "type": entity_type,
                    "raw_type": raw_type,
                    "canonical_type": entity_type,
                    "subtype": str(raw_entity.get("subtype") or raw_entity.get("entity_subtype") or ""),
                    "description": str(raw_entity.get("description") or raw_entity.get("entity_description") or ""),
                    "aliases": _coerce_aliases(raw_entity.get("aliases", [])),
                    "attributes": _coerce_attributes(raw_entity.get("attributes", {})),
                    "drift_reason": drift_reason,
                    "source_chunk_id": chunk_id,
                }
            )
            entities.append(entity)

        for raw_relation in payload.get("relations", []) or []:
            if not isinstance(raw_relation, dict):
                continue
            raw_type = str(raw_relation.get("type") or raw_relation.get("relation_type") or "关联").strip()
            relation_type, drift_reason = canonicalize_relation_type(raw_type)
            if drift_reason:
                relation_drift += 1
            relation = Relation.model_validate(
                {
                    "source": normalize_entity_name(raw_relation.get("source") or raw_relation.get("src") or raw_relation.get("source_entity")),
                    "target": normalize_entity_name(raw_relation.get("target") or raw_relation.get("tgt") or raw_relation.get("target_entity")),
                    "type": relation_type,
                    "raw_type": raw_type,
                    "canonical_type": relation_type,
                    "description": str(raw_relation.get("description") or raw_relation.get("relationship_description") or ""),
                    "evidence": str(raw_relation.get("evidence") or ""),
                    "drift_reason": drift_reason,
                    "source_chunk_id": chunk_id,
                }
            )
            relations.append(relation)

        return entities, relations, {"entity_type": entity_drift, "relation_type": relation_drift}


def _coerce_aliases(raw_aliases: Any) -> list[str]:
    if raw_aliases is None:
        return []
    if isinstance(raw_aliases, str):
        return [raw_aliases] if raw_aliases.strip() else []
    if isinstance(raw_aliases, list):
        return [str(alias) for alias in raw_aliases if str(alias).strip()]
    return []


def _coerce_attributes(raw_attributes: Any) -> dict[str, Any]:
    if isinstance(raw_attributes, dict):
        return {str(key): value for key, value in raw_attributes.items()}
    return {}


def _elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 3)
