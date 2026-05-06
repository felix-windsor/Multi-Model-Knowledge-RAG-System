#!/usr/bin/env python3
"""Run an end-to-end API benchmark against the local RAG service."""

from __future__ import annotations

import argparse
import json
import mimetypes
import statistics
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = REPO_ROOT / "benchmarks" / "eval_cases.enterprise_rag_demo.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "benchmark_reports"


@dataclass
class ApiResult:
    status_code: int
    elapsed_s: float
    body: dict[str, Any] | str


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = (len(ordered) - 1) * pct
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def unwrap_response(body: dict[str, Any] | str) -> dict[str, Any]:
    if not isinstance(body, dict):
        return {}
    if "data" in body and isinstance(body["data"], dict):
        return body["data"]
    return body


def keyword_hit_rate(answer: str, keywords: list[str]) -> tuple[int, int, float]:
    if not keywords:
        return 0, 0, 0.0
    lowered = answer.lower()
    hits = sum(1 for keyword in keywords if keyword.lower() in lowered)
    return hits, len(keywords), hits / len(keywords)


def parse_response(response: httpx.Response, elapsed: float) -> ApiResult:
    try:
        body: dict[str, Any] | str = response.json()
    except ValueError:
        body = response.text
    return ApiResult(response.status_code, elapsed, body)


def post_upload(client: httpx.Client, base_url: str, document: Path) -> ApiResult:
    mime_type = mimetypes.guess_type(document.name)[0] or "application/octet-stream"
    start = time.perf_counter()
    with document.open("rb") as handle:
        response = client.post(
            f"{base_url}/api/v1/documents/upload",
            files={"file": (document.name, handle, mime_type)},
        )
    elapsed = time.perf_counter() - start
    return parse_response(response, elapsed)


def wait_for_task(
    client: httpx.Client,
    base_url: str,
    task_id: str,
    max_wait_s: int,
    interval_s: float,
) -> tuple[dict[str, Any], float, list[dict[str, Any]]]:
    started = time.perf_counter()
    events: list[dict[str, Any]] = []
    while True:
        poll_started = time.perf_counter()
        response = client.get(f"{base_url}/api/v1/tasks/{task_id}")
        result = parse_response(response, time.perf_counter() - poll_started)
        data = unwrap_response(result.body)
        status = str(data.get("status", "")).lower()
        error_message = data.get("error_message")
        events.append(
            {
                "elapsed_s": round(time.perf_counter() - started, 3),
                "status": status,
                "progress": data.get("progress"),
                "step": data.get("step"),
                "http_status": result.status_code,
            }
        )
        if error_message and status != "completed":
            data["status"] = "failed"
            return data, time.perf_counter() - started, events
        if result.status_code >= 400 or status in {"completed", "failed", "cancelled"}:
            return data, time.perf_counter() - started, events
        if time.perf_counter() - started > max_wait_s:
            data["status"] = "timeout"
            data["error_message"] = f"Task did not finish within {max_wait_s}s"
            return data, time.perf_counter() - started, events
        time.sleep(interval_s)


def run_query(
    client: httpx.Client,
    base_url: str,
    question: str,
    mode: str,
    expected_keywords: list[str],
) -> dict[str, Any]:
    payload = {"question": question, "mode": mode, "top_k": 5}
    start = time.perf_counter()
    response = client.post(f"{base_url}/api/v1/query", json=payload)
    elapsed = time.perf_counter() - start
    result = parse_response(response, elapsed)
    data = unwrap_response(result.body)
    answer = str(data.get("answer", ""))
    hits, total, rate = keyword_hit_rate(answer, expected_keywords)
    success = result.status_code == 200 and bool(answer.strip())
    return {
        "question": question,
        "mode": mode,
        "status_code": result.status_code,
        "latency_s": round(elapsed, 3),
        "success": success,
        "answer_length": len(answer),
        "keyword_hits": hits,
        "keyword_total": total,
        "keyword_hit_rate": round(rate, 4),
        "expected_keywords": expected_keywords,
        "answer": answer,
        "raw_body": result.body if result.status_code != 200 else None,
    }


def get_graph(client: httpx.Client, base_url: str) -> dict[str, Any]:
    start = time.perf_counter()
    response = client.get(f"{base_url}/api/v1/graph", params={"limit": 5000})
    elapsed = time.perf_counter() - start
    result = parse_response(response, elapsed)
    data = unwrap_response(result.body)
    nodes = data.get("nodes") if isinstance(data, dict) else []
    edges = data.get("edges") if isinstance(data, dict) else []
    return {
        "status_code": result.status_code,
        "latency_s": round(elapsed, 3),
        "entity_count": len(nodes or []),
        "relation_count": len(edges or []),
        "sample_entities": (nodes or [])[:10],
        "raw_body": result.body if result.status_code != 200 else None,
    }


def summarize(report: dict[str, Any]) -> dict[str, Any]:
    queries = report["queries"]
    query_latencies = [q["latency_s"] for q in queries if q["success"]]
    success_count = sum(1 for q in queries if q["success"])
    keyword_rates = [q["keyword_hit_rate"] for q in queries if q["keyword_total"]]
    doc = report["document_processing"]
    graph = report["graph"]
    summary = {
        "document_status": doc.get("task_status"),
        "file_size_kb": doc.get("file_size_kb"),
        "upload_time_s": doc.get("upload_time_s"),
        "processing_time_s": doc.get("processing_time_s"),
        "total_ingest_time_s": doc.get("total_ingest_time_s"),
        "processing_speed_kb_s": doc.get("processing_speed_kb_s"),
        "query_count": len(queries),
        "query_success_count": success_count,
        "query_success_rate": round(success_count / len(queries), 4) if queries else 0.0,
        "avg_query_latency_s": round(statistics.mean(query_latencies), 3)
        if query_latencies
        else None,
        "p50_query_latency_s": round(percentile(query_latencies, 0.5), 3)
        if query_latencies
        else None,
        "p95_query_latency_s": round(percentile(query_latencies, 0.95), 3)
        if query_latencies
        else None,
        "answer_keyword_hit_rate": round(statistics.mean(keyword_rates), 4)
        if keyword_rates
        else None,
        "entity_count": graph.get("entity_count"),
        "relation_count": graph.get("relation_count"),
        "top_k_hit_rate_note": (
            "The current /api/v1/query response does not expose retrieved chunks "
            "or sources, so this run reports answer keyword hit rate instead."
        ),
    }
    report["summary"] = summary
    return summary


def write_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    env = report["environment"]
    lines = [
        "# RAG Demo Benchmark Report",
        "",
        f"Run ID: `{report['run_id']}`",
        f"Generated At: `{report['generated_at']}`",
        "",
        "## Model Configuration",
        "",
        f"- LLM: `{env.get('LLM_MODEL', '')}`",
        f"- Vision: `{env.get('VISION_MODEL', '')}`",
        f"- Embedding: `{env.get('EMBEDDING_MODEL', '')}`",
        f"- Embedding Dim: `{env.get('EMBEDDING_DIM', '')}`",
        f"- Storage Backend: `{env.get('STORAGE_BACKEND', 'local')}`",
        "",
        "## Resume-Friendly Metrics",
        "",
        f"- Document status: `{summary['document_status']}`",
        f"- File size: `{summary['file_size_kb']}` KB",
        f"- Upload latency: `{summary['upload_time_s']}` s",
        f"- Processing latency: `{summary['processing_time_s']}` s",
        f"- Total ingest latency: `{summary['total_ingest_time_s']}` s",
        f"- Processing speed: `{summary['processing_speed_kb_s']}` KB/s",
        f"- Query success rate: `{summary['query_success_count']}/{summary['query_count']}` "
        f"({summary['query_success_rate'] * 100:.1f}%)",
        f"- Average query latency: `{summary['avg_query_latency_s']}` s",
        f"- P50 query latency: `{summary['p50_query_latency_s']}` s",
        f"- P95 query latency: `{summary['p95_query_latency_s']}` s",
        f"- Answer keyword hit rate: `{summary['answer_keyword_hit_rate']}`",
        f"- Exported entities: `{summary['entity_count']}`",
        f"- Exported relations: `{summary['relation_count']}`",
        "",
        "## Query Details",
        "",
        "| # | Mode | Latency(s) | Success | Keyword Hits | Answer Length |",
        "|---|------|------------|---------|--------------|---------------|",
    ]
    for index, query in enumerate(report["queries"], 1):
        lines.append(
            f"| {index} | {query['mode']} | {query['latency_s']} | "
            f"{query['success']} | {query['keyword_hits']}/{query['keyword_total']} | "
            f"{query['answer_length']} |"
        )
    lines.extend(["", "## Notes", "", f"- {summary['top_k_hit_rate_note']}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-wait-s", type=int, default=900)
    parser.add_argument("--poll-interval-s", type=float, default=2.0)
    args = parser.parse_args()

    cases_path = args.cases if args.cases.is_absolute() else REPO_ROOT / args.cases
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    document = Path(cases["document"])
    if not document.is_absolute():
        document = REPO_ROOT / document
    if not document.exists():
        print(f"Document not found: {document}", file=sys.stderr)
        return 2

    env = load_dotenv(REPO_ROOT / ".env")
    output_dir = args.output_dir if args.output_dir.is_absolute() else REPO_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
    raw_path = output_dir / f"{run_id}.json"
    md_path = output_dir / f"{run_id}.md"

    timeout = httpx.Timeout(connect=10.0, read=600.0, write=600.0, pool=10.0)
    report: dict[str, Any] = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": args.base_url,
        "environment": {
            key: env.get(key)
            for key in [
                "LLM_MODEL",
                "VISION_MODEL",
                "EMBEDDING_MODEL",
                "EMBEDDING_DIM",
                "STORAGE_BACKEND",
            ]
        },
        "document": str(document),
        "document_processing": {},
        "queries": [],
        "graph": {},
    }

    with httpx.Client(timeout=timeout, trust_env=False) as client:
        health_start = time.perf_counter()
        health = client.get(f"{args.base_url}/api/v1/health")
        report["health"] = parse_response(health, time.perf_counter() - health_start).__dict__

        upload = post_upload(client, args.base_url, document)
        upload_data = unwrap_response(upload.body)
        task_id = str(upload_data.get("task_id", ""))
        doc_id = str(upload_data.get("doc_id", ""))
        file_size_kb = round(document.stat().st_size / 1024, 3)
        task_data, processing_time, task_events = wait_for_task(
            client,
            args.base_url,
            task_id,
            args.max_wait_s,
            args.poll_interval_s,
        )
        total_time = upload.elapsed_s + processing_time
        report["document_processing"] = {
            "doc_id": doc_id,
            "task_id": task_id,
            "task_status": task_data.get("status"),
            "task_progress": task_data.get("progress"),
            "task_step": task_data.get("step"),
            "error_message": task_data.get("error_message"),
            "file_size_kb": file_size_kb,
            "upload_time_s": round(upload.elapsed_s, 3),
            "processing_time_s": round(processing_time, 3),
            "total_ingest_time_s": round(total_time, 3),
            "processing_speed_kb_s": round(file_size_kb / processing_time, 3)
            if processing_time > 0
            else None,
            "task_events": task_events,
            "upload_status_code": upload.status_code,
            "upload_body": upload.body if upload.status_code != 200 else None,
        }

        if str(task_data.get("status", "")).lower() == "completed":
            for case in cases.get("queries", []):
                report["queries"].append(
                    run_query(
                        client,
                        args.base_url,
                        str(case["question"]),
                        str(case.get("mode", "mix")),
                        list(case.get("expected_keywords", [])),
                    )
                )
            report["graph"] = get_graph(client, args.base_url)
        else:
            report["graph"] = {"status_code": None, "entity_count": 0, "relation_count": 0}

    summarize(report)
    raw_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, md_path)
    print(
        json.dumps(
            {"json": str(raw_path), "markdown": str(md_path), "summary": report["summary"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["summary"]["document_status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
