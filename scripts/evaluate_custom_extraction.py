#!/usr/bin/env python3
"""Evaluate the custom Graph RAG extraction core on local chunks.

Default mode uses a deterministic mock LLM so it can run without API keys.
Use --use-llm to call the configured project LLM from the root .env file.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.config import settings
from app.rag_core.evaluation import aggregate_metrics
from app.rag_core.extractor import GraphRAGExtractor
from app.rag_core.schemas import ExtractionResult
from app.services.llm_factory import ModelFactory


SAMPLE_CHUNKS = [
    {
        "chunk_id": "sample-1",
        "text": "综合管理系统通过统一身份认证平台完成用户登录，并将操作日志写入审计服务。",
    },
    {
        "chunk_id": "sample-2",
        "text": "设备监控模块读取传感器指标，触发告警流程，并向运维人员角色输出处置建议。",
    },
    {
        "chunk_id": "sample-3",
        "text": "数据交换接口依赖消息队列服务，消息队列服务受接口调用规范约束。",
    },
]


async def main() -> None:
    args = parse_args()
    chunks = load_chunks(args.input, args.max_chars)
    llm_func = build_real_llm_func() if args.use_llm else mock_llm
    extractor = GraphRAGExtractor(llm_func)

    results: list[dict[str, Any]] = []
    for item in chunks:
        result = await extractor.extract_chunk(item["text"], chunk_id=item["chunk_id"])
        results.append(
            {
                "chunk_id": item["chunk_id"],
                "text": item["text"],
                "result": result.model_dump(),
            }
        )

    report = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "mode": "real_llm" if args.use_llm else "mock",
        "chunk_count": len(results),
        "aggregate": aggregate_metrics(
            [ExtractionResult.model_validate(item["result"]) for item in results]
        ),
        "results": results,
    }

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = datetime.now().strftime("%Y%m%d-%H%M%S-custom-extraction")
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")

    print(f"Wrote JSON report: {json_path}")
    print(f"Wrote Markdown report: {md_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate custom Graph RAG extraction.")
    parser.add_argument("--input", help="Optional text/markdown file to split into chunks.")
    parser.add_argument("--output-dir", default="benchmark_reports")
    parser.add_argument("--max-chars", type=int, default=1200)
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use the configured LLM from .env instead of the deterministic mock.",
    )
    return parser.parse_args()


def load_chunks(input_path: str | None, max_chars: int) -> list[dict[str, str]]:
    if not input_path:
        return SAMPLE_CHUNKS

    text = Path(input_path).read_text(encoding="utf-8")
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    chunks: list[dict[str, str]] = []
    current = ""
    index = 1

    for block in blocks:
        if len(current) + len(block) + 2 <= max_chars:
            current = f"{current}\n\n{block}".strip()
            continue
        if current:
            chunks.append({"chunk_id": f"input-{index}", "text": current})
            index += 1
        current = block[:max_chars]

    if current:
        chunks.append({"chunk_id": f"input-{index}", "text": current})
    return chunks


def build_real_llm_func():
    llm_config = settings.get_model_config("llm")
    return ModelFactory.create_llm_function(
        provider=llm_config["provider"],
        model=llm_config["model"],
        api_key=llm_config["api_key"],
        base_url=llm_config["base_url"],
    )


async def mock_llm(prompt: str, **kwargs):
    if "综合管理系统" in prompt:
        return {
            "entities": [
                {"name": "综合管理系统", "type": "业务系统", "description": "企业内部业务管理系统"},
                {"name": "统一身份认证平台", "type": "平台", "description": "提供用户登录认证能力"},
                {"name": "审计服务", "type": "服务", "description": "记录操作日志"},
            ],
            "relations": [
                {
                    "source": "综合管理系统",
                    "target": "统一身份认证平台",
                    "type": "使用",
                    "description": "综合管理系统使用统一身份认证平台完成登录",
                    "evidence": "通过统一身份认证平台完成用户登录",
                },
                {
                    "source": "综合管理系统",
                    "target": "审计服务",
                    "type": "写入",
                    "description": "综合管理系统将操作日志写入审计服务",
                    "evidence": "将操作日志写入审计服务",
                },
            ],
        }

    if "设备监控模块" in prompt:
        return {
            "entities": [
                {"name": "设备监控模块", "type": "模块", "description": "负责设备指标监控"},
                {"name": "传感器指标", "type": "指标", "description": "设备采集指标"},
                {"name": "告警流程", "type": "流程", "description": "异常告警处理流程"},
                {"name": "运维人员角色", "type": "人员角色", "description": "负责运维处置的角色"},
            ],
            "relations": [
                {"source": "设备监控模块", "target": "传感器指标", "type": "读取", "description": "模块读取传感器指标"},
                {"source": "设备监控模块", "target": "告警流程", "type": "触发", "description": "模块触发告警流程"},
                {"source": "设备监控模块", "target": "运维人员角色", "type": "输出", "description": "模块输出处置建议"},
            ],
        }

    return {
        "entities": [
            {"name": "数据交换接口", "type": "接口", "description": "用于数据交换"},
            {"name": "消息队列服务", "type": "服务", "description": "提供异步消息能力"},
            {"name": "接口调用规范", "type": "规范", "description": "约束接口调用方式"},
        ],
        "relations": [
            {"source": "数据交换接口", "target": "消息队列服务", "type": "依赖", "description": "接口依赖消息队列服务"},
            {"source": "消息队列服务", "target": "接口调用规范", "type": "约束", "description": "消息队列服务受规范约束"},
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    aggregate = report["aggregate"]
    lines = [
        "# Custom Graph RAG Extraction Report",
        "",
        f"- Created at: `{report['created_at']}`",
        f"- Mode: `{report['mode']}`",
        f"- Chunks: `{report['chunk_count']}`",
        "",
        "## Aggregate Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in aggregate.items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Per Chunk", ""])
    for item in report["results"]:
        result = item["result"]
        lines.append(f"### {item['chunk_id']}")
        lines.append("")
        lines.append(f"- Entities: `{len(result['entities'])}`")
        lines.append(f"- Relations: `{len(result['relations'])}`")
        lines.append(f"- Invalid relations: `{result['metrics']['invalid_relation_count']}`")
        lines.append("")

    return "\n".join(lines) + "\n"


def _rate(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


if __name__ == "__main__":
    asyncio.run(main())
