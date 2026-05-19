#!/usr/bin/env python3
"""Generate a synthetic desensitized enterprise RAG evaluation dataset."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT_DIR / "benchmarks" / "enterprise_200x420"


@dataclass(frozen=True)
class DocSpec:
    doc_id: str
    doc_type: str
    title: str
    path: str
    system: str
    module: str
    service: str
    interface: str
    metric: str
    process: str
    owner: str


DOC_DISTRIBUTION = [
    ("technical_manual", "技术手册", 70),
    ("policy_process", "制度流程", 50),
    ("api_config", "接口配置", 30),
    ("table_ledger", "表格台账", 30),
    ("scan_diagram", "扫描图表", 20),
]

QUERY_DISTRIBUTION = [
    ("fact_lookup", 130),
    ("summary", 70),
    ("entity_relation", 90),
    ("multi_hop", 80),
    ("table_chart", 50),
]

SYSTEMS = [
    "综合管理系统",
    "设备监控系统",
    "数据交换平台",
    "统一身份认证平台",
    "审计分析平台",
    "物资管理系统",
    "任务调度平台",
    "安全态势平台",
]

MODULES = [
    "用户权限模块",
    "设备监控模块",
    "指标采集模块",
    "告警联动模块",
    "报表生成模块",
    "数据同步模块",
    "配置管理模块",
    "日志归档模块",
]

SERVICES = [
    "统一身份认证服务",
    "消息队列服务",
    "审计日志服务",
    "指标计算服务",
    "文件转换服务",
    "图谱检索服务",
    "接口网关服务",
    "任务编排服务",
]

INTERFACES = [
    "用户登录接口",
    "设备状态接口",
    "指标上报接口",
    "告警推送接口",
    "报表导出接口",
    "日志查询接口",
    "配置下发接口",
    "图谱导出接口",
]

METRICS = [
    "接口成功率",
    "平均响应时间",
    "告警闭环率",
    "任务完成率",
    "数据同步延迟",
    "日志留存天数",
    "设备在线率",
    "异常处置时长",
]

PROCESSES = [
    "用户准入流程",
    "设备巡检流程",
    "告警处置流程",
    "数据归档流程",
    "接口变更流程",
    "权限审批流程",
    "配置发布流程",
    "应急响应流程",
]

OWNERS = [
    "运维人员角色",
    "安全管理员角色",
    "业务审核角色",
    "系统管理员角色",
    "数据治理角色",
]


def main() -> None:
    if DATASET_DIR.exists():
        shutil.rmtree(DATASET_DIR)
    (DATASET_DIR / "documents").mkdir(parents=True)

    documents = build_documents()
    cases = build_cases(documents)

    for document in documents:
        doc_path = DATASET_DIR / document.path
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(render_document(document), encoding="utf-8")

    manifest = {
        "name": "enterprise_200x420",
        "description": "Synthetic desensitized enterprise document evaluation dataset for RAG demos.",
        "document_count": len(documents),
        "query_count": len(cases),
        "document_distribution": {
            doc_type: count for doc_type, _, count in DOC_DISTRIBUTION
        },
        "query_distribution": {query_type: count for query_type, count in QUERY_DISTRIBUTION},
        "documents": [serialize_document(document) for document in documents],
    }

    (DATASET_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (DATASET_DIR / "eval_cases.enterprise_200x420.json").write_text(
        json.dumps({"dataset": "enterprise_200x420", "cases": cases}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (DATASET_DIR / "combined_corpus.md").write_text(
        render_combined_corpus(documents),
        encoding="utf-8",
    )
    (DATASET_DIR / "api_benchmark_cases.enterprise_200x420.json").write_text(
        json.dumps(
            {
                "document": "benchmarks/enterprise_200x420/combined_corpus.md",
                "queries": [
                    {
                        "question": case["question"],
                        "mode": "mix",
                        "expected_keywords": case["expected_keywords"],
                        "case_id": case["case_id"],
                        "doc_id": case["doc_id"],
                        "question_type": case["question_type"],
                    }
                    for case in cases
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (DATASET_DIR / "README.md").write_text(render_readme(), encoding="utf-8")

    print(f"Generated {len(documents)} documents and {len(cases)} eval cases at {DATASET_DIR}")


def build_documents() -> list[DocSpec]:
    documents: list[DocSpec] = []
    index = 1
    for doc_type, label, count in DOC_DISTRIBUTION:
        for local_index in range(1, count + 1):
            system = SYSTEMS[(index - 1) % len(SYSTEMS)]
            module = MODULES[(index + 1) % len(MODULES)]
            service = SERVICES[(index + 2) % len(SERVICES)]
            interface = INTERFACES[(index + 3) % len(INTERFACES)]
            metric = METRICS[(index + 4) % len(METRICS)]
            process = PROCESSES[(index + 5) % len(PROCESSES)]
            owner = OWNERS[(index + 6) % len(OWNERS)]
            doc_id = f"ent-{index:03d}"
            slug = f"{doc_id}-{doc_type}.md"
            documents.append(
                DocSpec(
                    doc_id=doc_id,
                    doc_type=doc_type,
                    title=f"{label}-{system}-{local_index:03d}",
                    path=f"documents/{doc_type}/{slug}",
                    system=system,
                    module=module,
                    service=service,
                    interface=interface,
                    metric=metric,
                    process=process,
                    owner=owner,
                )
            )
            index += 1
    return documents


def serialize_document(document: DocSpec) -> dict:
    return {
        "doc_id": document.doc_id,
        "type": document.doc_type,
        "title": document.title,
        "path": document.path,
        "system": document.system,
        "module": document.module,
        "service": document.service,
        "interface": document.interface,
        "metric": document.metric,
        "process": document.process,
        "owner": document.owner,
    }


def render_document(doc: DocSpec) -> str:
    if doc.doc_type == "technical_manual":
        body = [
            f"{doc.system}面向内网业务提供统一操作入口，核心组件为{doc.module}。",
            f"{doc.module}调用{doc.service}，并通过{doc.interface}对外提供状态查询能力。",
            f"运行指标以{doc.metric}为主，异常时触发{doc.process}，由{doc.owner}跟进。",
            f"系统依赖关系：{doc.system} -> {doc.module} -> {doc.service} -> {doc.interface}。",
        ]
    elif doc.doc_type == "policy_process":
        body = [
            f"本规范适用于{doc.system}的{doc.process}。",
            f"{doc.owner}负责审核{doc.module}的变更申请，并检查{doc.metric}是否满足阈值。",
            f"当{doc.service}异常时，必须记录审计日志并通知相关角色。",
            f"流程约束：{doc.process}约束{doc.module}，{doc.module}依赖{doc.service}。",
        ]
    elif doc.doc_type == "api_config":
        body = [
            f"{doc.interface}属于{doc.system}，用于支撑{doc.module}的数据访问。",
            f"接口调用前需要通过{doc.service}完成鉴权，返回字段包含{doc.metric}。",
            f"配置项包括超时时间、重试次数、调用方标识和审计开关。",
            f"接口关系：{doc.interface}调用{doc.service}，影响{doc.metric}。",
        ]
    elif doc.doc_type == "table_ledger":
        body = [
            f"| 系统 | 模块 | 指标 | 责任角色 |",
            f"|---|---|---:|---|",
            f"| {doc.system} | {doc.module} | {doc.metric} | {doc.owner} |",
            f"| {doc.service} | {doc.interface} | 数据同步延迟 | 数据治理角色 |",
            f"表格说明：{doc.module}读取{doc.metric}，并由{doc.owner}进行周期性复核。",
        ]
    else:
        body = [
            f"扫描图说明：图中展示{doc.system}、{doc.module}、{doc.service}和{doc.interface}之间的链路。",
            f"流程从{doc.owner}发起，经{doc.process}进入{doc.module}。",
            f"图表节点显示{doc.service}影响{doc.metric}，异常路径会触发告警。",
            f"图中箭头关系：{doc.module}调用{doc.service}，{doc.service}输出{doc.metric}。",
        ]

    return "\n".join(
        [
            f"# {doc.title}",
            "",
            f"- 文档编号：{doc.doc_id}",
            f"- 文档类型：{doc.doc_type}",
            f"- 脱敏说明：本文件为合成企业文档样例，不包含真实公司数据。",
            "",
            "## 内容",
            "",
            *body,
            "",
            "## 关键实体",
            "",
            f"- 系统：{doc.system}",
            f"- 模块：{doc.module}",
            f"- 服务：{doc.service}",
            f"- 接口：{doc.interface}",
            f"- 指标：{doc.metric}",
            f"- 流程：{doc.process}",
            f"- 角色：{doc.owner}",
            "",
        ]
    )


def build_cases(documents: list[DocSpec]) -> list[dict]:
    cases: list[dict] = []
    cursor = 0
    case_index = 1

    for question_type, count in QUERY_DISTRIBUTION:
        for _ in range(count):
            doc = documents[cursor % len(documents)]
            cursor += 1
            cases.append(build_case(case_index, question_type, doc))
            case_index += 1
    return cases


def build_case(case_index: int, question_type: str, doc: DocSpec) -> dict:
    if question_type == "fact_lookup":
        question = f"{doc.title}中，{doc.system}的核心模块是什么？"
        expected = [doc.system, doc.module]
    elif question_type == "summary":
        question = f"请概括{doc.title}的主要内容和适用场景？"
        expected = [doc.system, doc.module, doc.process]
    elif question_type == "entity_relation":
        question = f"{doc.title}中，{doc.module}和{doc.service}是什么关系？"
        expected = [doc.module, doc.service, "调用", "依赖"]
    elif question_type == "multi_hop":
        question = f"如果{doc.service}异常，可能影响哪个指标并触发哪个流程？"
        expected = [doc.service, doc.metric, doc.process]
    else:
        question = f"{doc.title}中的表格或图表体现了哪些系统、模块和指标？"
        expected = [doc.system, doc.module, doc.metric]

    return {
        "case_id": f"case-{case_index:04d}",
        "doc_id": doc.doc_id,
        "question_type": question_type,
        "question": question,
        "expected_keywords": expected,
        "answer_judgement": "keyword_hit",
        "notes": "Synthetic desensitized case for RAG evaluation.",
    }


def render_combined_corpus(documents: list[DocSpec]) -> str:
    sections = [
        "# Enterprise 200x420 Combined Corpus",
        "",
        "本文件由 200 份合成脱敏企业文档拼接生成，用于现有 API benchmark 脚本一次性上传测试。",
        "",
    ]
    for document in documents:
        sections.append(render_document(document))
        sections.append("\n---\n")
    return "\n".join(sections)


def render_readme() -> str:
    return """# Enterprise 200x420 RAG Evaluation Dataset

This dataset is synthetic and desensitized. It is designed to simulate enterprise
intranet documents for RAG pipeline evaluation without containing confidential data.

## Scale

- Documents: 200
- Query cases: 420
- Document types: technical manuals, policy/process docs, API/config docs, table ledgers, scan/diagram-style docs
- Query types: fact lookup, summary, entity relation, multi-hop, table/chart understanding

## Files

- `manifest.json`: document inventory and distribution
- `eval_cases.enterprise_200x420.json`: query cases and expected keywords
- `api_benchmark_cases.enterprise_200x420.json`: compatible input for `scripts/run_api_benchmark.py`
- `combined_corpus.md`: all 200 documents concatenated for one-shot API benchmark runs
- `documents/`: markdown documents grouped by type

## Intended Metrics

- document processing time
- average query latency and P95 latency
- answer keyword hit rate
- entity/relation counts
- schema drift and invalid relation rates for the custom extraction core
"""


if __name__ == "__main__":
    main()
