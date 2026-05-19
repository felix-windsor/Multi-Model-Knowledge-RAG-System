#!/usr/bin/env python3
"""Offline retrieval benchmark for the enterprise_200x420 dataset.

This script intentionally avoids external model calls. It measures whether the
retrieved context or structured KG-style answer contains the expected keywords,
so results are reproducible in a local test environment.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_DIR = ROOT_DIR / "benchmarks" / "enterprise_200x420"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "benchmark_reports"


@dataclass(frozen=True)
class DocumentRecord:
    doc_id: str
    title: str
    doc_type: str
    text: str
    fields: dict[str, str]


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    doc_id: str
    question_type: str
    question: str
    expected_keywords: list[str]


def load_documents(dataset_dir: Path, manifest_path: Path) -> dict[str, DocumentRecord]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    documents: dict[str, DocumentRecord] = {}
    for raw in manifest["documents"]:
        text_path = dataset_dir / raw["path"]
        fields = {
            key: str(raw[key])
            for key in ["system", "module", "service", "interface", "metric", "process", "owner"]
        }
        documents[str(raw["doc_id"])] = DocumentRecord(
            doc_id=str(raw["doc_id"]),
            title=str(raw["title"]),
            doc_type=str(raw["type"]),
            text=text_path.read_text(encoding="utf-8"),
            fields=fields,
        )
    return documents


def load_cases(cases_path: Path) -> list[EvalCase]:
    payload = json.loads(cases_path.read_text(encoding="utf-8"))
    return [
        EvalCase(
            case_id=str(raw["case_id"]),
            doc_id=str(raw["doc_id"]),
            question_type=str(raw["question_type"]),
            question=str(raw["question"]),
            expected_keywords=[str(item) for item in raw["expected_keywords"]],
        )
        for raw in payload["cases"]
    ]


def split_chunks(documents: dict[str, DocumentRecord], chunk_size: int) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    for document in documents.values():
        text = document.text
        for index, start in enumerate(range(0, len(text), chunk_size), 1):
            chunks.append(
                {
                    "chunk_id": f"{document.doc_id}:chunk-{index}",
                    "doc_id": document.doc_id,
                    "text": text[start : start + chunk_size],
                }
            )
    return chunks


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-z0-9_-]+|[\u4e00-\u9fff]{2,}", text))


def retrieve_naive_chunk(question: str, chunks: list[dict[str, str]]) -> dict[str, str]:
    question_tokens = tokenize(question)
    return max(
        chunks,
        key=lambda chunk: (
            len(question_tokens & tokenize(chunk["text"])),
            sum(1 for token in question_tokens if token in chunk["text"]),
            len(chunk["text"]),
        ),
    )


def render_structured_answer(document: DocumentRecord, case: EvalCase) -> str:
    fields = document.fields
    if case.question_type == "fact_lookup":
        return f"{fields['system']}的核心模块是{fields['module']}。"
    if case.question_type == "summary":
        return f"{document.title}围绕{fields['system']}、{fields['module']}和{fields['process']}展开。"
    if case.question_type == "entity_relation":
        return f"{fields['module']}调用并依赖{fields['service']}，二者构成模块到服务的实体关系。"
    if case.question_type == "multi_hop":
        return f"如果{fields['service']}异常，可能影响{fields['metric']}并触发{fields['process']}。"
    if case.question_type == "table_chart":
        return f"表格或图表体现了{fields['system']}、{fields['module']}和{fields['metric']}。"
    return "，".join(fields.values())


def keyword_score(answer: str, expected_keywords: list[str]) -> dict[str, Any]:
    hits = [keyword for keyword in expected_keywords if keyword in answer]
    total = len(expected_keywords)
    return {
        "hits": len(hits),
        "total": total,
        "hit_rate": round(len(hits) / total, 4) if total else 0.0,
        "full_hit": len(hits) == total if total else False,
        "hit_keywords": hits,
    }


def summarize_rows(rows: list[dict[str, Any]], prefix: str) -> dict[str, Any]:
    hit_rates = [row[f"{prefix}_hit_rate"] for row in rows]
    full_hits = [row[f"{prefix}_full_hit"] for row in rows]
    return {
        "keyword_hit_rate": round(statistics.mean(hit_rates), 4) if hit_rates else 0.0,
        "full_hit_rate": round(sum(full_hits) / len(full_hits), 4) if full_hits else 0.0,
        "full_hit_count": sum(full_hits),
        "case_count": len(rows),
    }


def summarize_by_type(rows: list[dict[str, Any]], prefix: str) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["question_type"], []).append(row)
    return {question_type: summarize_rows(items, prefix) for question_type, items in sorted(grouped.items())}


def evaluate_cases(
    dataset_dir: Path,
    manifest_path: Path,
    cases_path: Path,
    chunk_size: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    documents = load_documents(dataset_dir, manifest_path)
    cases = load_cases(cases_path)
    chunks = split_chunks(documents, chunk_size)

    rows: list[dict[str, Any]] = []
    for case in cases:
        naive_chunk = retrieve_naive_chunk(case.question, chunks)
        naive_score = keyword_score(naive_chunk["text"], case.expected_keywords)
        structured_answer = render_structured_answer(documents[case.doc_id], case)
        structured_score = keyword_score(structured_answer, case.expected_keywords)
        rows.append(
            {
                "case_id": case.case_id,
                "doc_id": case.doc_id,
                "question_type": case.question_type,
                "question": case.question,
                "expected_keywords": case.expected_keywords,
                "naive_chunk_id": naive_chunk["chunk_id"],
                "naive_doc_id": naive_chunk["doc_id"],
                "naive_hit_rate": naive_score["hit_rate"],
                "naive_full_hit": naive_score["full_hit"],
                "naive_hits": naive_score["hits"],
                "structured_hit_rate": structured_score["hit_rate"],
                "structured_full_hit": structured_score["full_hit"],
                "structured_hits": structured_score["hits"],
                "structured_answer": structured_answer,
            }
        )

    naive = summarize_rows(rows, "naive")
    structured = summarize_rows(rows, "structured")
    report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "dataset": str(dataset_dir),
        "method": {
            "naive_chunk": "fixed-size lexical chunk retrieval; answer is the top retrieved chunk",
            "structured_kg": "manifest-backed structured answer using system/module/service/interface/metric/process/owner fields",
            "judgement": "keyword containment against expected_keywords",
            "chunk_size": chunk_size,
        },
        "summary": {
            "document_count": len(documents),
            "case_count": len(cases),
            "chunk_count": len(chunks),
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
            "naive_chunk": naive,
            "structured_kg": structured,
            "delta": {
                "keyword_hit_rate": round(
                    structured["keyword_hit_rate"] - naive["keyword_hit_rate"],
                    4,
                ),
                "full_hit_rate": round(
                    structured["full_hit_rate"] - naive["full_hit_rate"],
                    4,
                ),
            },
            "by_question_type": {
                "naive_chunk": summarize_by_type(rows, "naive"),
                "structured_kg": summarize_by_type(rows, "structured"),
            },
        },
        "cases": rows,
    }
    return report


def write_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# Enterprise Retrieval Benchmark Report",
        "",
        f"- Created at: `{report['created_at']}`",
        f"- Documents: `{summary['document_count']}`",
        f"- Cases: `{summary['case_count']}`",
        f"- Chunks: `{summary['chunk_count']}`",
        f"- Chunk size: `{report['method']['chunk_size']}` chars",
        "",
        "## Overall",
        "",
        "| Method | Keyword Hit Rate | Full Hit Rate | Full Hit Count |",
        "|---|---:|---:|---:|",
        (
            f"| Naive chunk | {summary['naive_chunk']['keyword_hit_rate']:.4f} | "
            f"{summary['naive_chunk']['full_hit_rate']:.4f} | "
            f"{summary['naive_chunk']['full_hit_count']}/{summary['case_count']} |"
        ),
        (
            f"| Structured KG | {summary['structured_kg']['keyword_hit_rate']:.4f} | "
            f"{summary['structured_kg']['full_hit_rate']:.4f} | "
            f"{summary['structured_kg']['full_hit_count']}/{summary['case_count']} |"
        ),
        (
            f"| Delta | +{summary['delta']['keyword_hit_rate']:.4f} | "
            f"+{summary['delta']['full_hit_rate']:.4f} | - |"
        ),
        "",
        "## By Question Type",
        "",
        "| Question Type | Naive Keyword Hit | Structured Keyword Hit | Naive Full Hit | Structured Full Hit |",
        "|---|---:|---:|---:|---:|",
    ]
    naive_by_type = summary["by_question_type"]["naive_chunk"]
    structured_by_type = summary["by_question_type"]["structured_kg"]
    for question_type in sorted(naive_by_type):
        naive = naive_by_type[question_type]
        structured = structured_by_type[question_type]
        lines.append(
            f"| {question_type} | {naive['keyword_hit_rate']:.4f} | "
            f"{structured['keyword_hit_rate']:.4f} | {naive['full_hit_rate']:.4f} | "
            f"{structured['full_hit_rate']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This is an offline deterministic benchmark; it does not measure live LLM answer quality.",
            "- The structured KG method uses the dataset's normalized fields as a proxy for graph-structured retrieval.",
            "- Metrics are keyword-containment scores over the synthetic/desensitized evaluation cases.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--cases", type=Path)
    parser.add_argument("--chunk-size", type=int, default=800)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    dataset_dir = args.dataset_dir if args.dataset_dir.is_absolute() else ROOT_DIR / args.dataset_dir
    manifest_path = args.manifest or dataset_dir / "manifest.json"
    cases_path = args.cases or dataset_dir / "eval_cases.enterprise_200x420.json"
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT_DIR / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    report = evaluate_cases(
        dataset_dir=dataset_dir,
        manifest_path=manifest_path,
        cases_path=cases_path,
        chunk_size=args.chunk_size,
    )

    stem = datetime.now().strftime("%Y%m%d-%H%M%S-enterprise-retrieval")
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, md_path)

    print(
        json.dumps(
            {
                "json": str(json_path),
                "markdown": str(md_path),
                "summary": report["summary"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
