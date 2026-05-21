"""Sidecar quality report generation for custom Graph RAG extraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from knowledge_graph_rag.utils import separate_content

from app.rag_core.evaluation import aggregate_metrics
from app.rag_core.extractor import GraphRAGExtractor
from app.rag_core.schemas import ExtractionResult


@dataclass(frozen=True)
class ExtractionSidecarService:
    """Generate document-level extraction quality reports without owning ingestion."""

    max_chars: int = 1200

    async def run_for_document(
        self,
        rag: Any,
        file_path: str,
        parse_kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        content_list, parsed_doc_id = await rag.parse_document(
            file_path,
            display_stats=False,
            **(parse_kwargs or {}),
        )
        text_content, multimodal_items = separate_content(content_list)
        chunks = split_text_chunks(text_content, self.max_chars)

        extractor = GraphRAGExtractor(rag.llm_model_func)
        results: list[ExtractionResult] = []
        for index, chunk in enumerate(chunks, 1):
            results.append(
                await extractor.extract_chunk(
                    chunk,
                    chunk_id=f"{parsed_doc_id}:sidecar-{index}",
                )
            )

        return {
            "enabled": True,
            "parsed_doc_id": parsed_doc_id,
            "chunk_count": len(chunks),
            "multimodal_item_count": len(multimodal_items),
            "aggregate": aggregate_metrics(results),
            "per_chunk": [
                {
                    "chunk_id": f"{parsed_doc_id}:sidecar-{index}",
                    "entities": len(result.entities),
                    "relations": len(result.relations),
                    "invalid_relations": result.metrics.invalid_relation_count,
                    "entity_type_drift_count": result.metrics.entity_type_drift_count,
                    "relation_type_drift_count": result.metrics.relation_type_drift_count,
                    "avg_relation_confidence": _chunk_relation_confidence(result),
                }
                for index, result in enumerate(results, 1)
            ],
        }


def split_text_chunks(text: str, max_chars: int) -> list[str]:
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    chunks: list[str] = []
    current = ""

    for block in blocks:
        if len(current) + len(block) + 2 <= max_chars:
            current = f"{current}\n\n{block}".strip()
            continue
        if current:
            chunks.append(current)
        current = block[:max_chars]

    if current:
        chunks.append(current)
    return chunks


def _chunk_relation_confidence(result: ExtractionResult) -> float:
    values = [relation.confidence for relation in result.relations]
    if not values:
        return 0.0
    return round(sum(values) / len(values), 4)
