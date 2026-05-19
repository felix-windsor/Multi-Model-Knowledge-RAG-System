import json
from pathlib import Path

from scripts.evaluate_enterprise_retrieval import (
    DocumentRecord,
    EvalCase,
    evaluate_cases,
    render_structured_answer,
)


def test_structured_answer_covers_multihop_expected_keywords():
    document = DocumentRecord(
        doc_id="ent-001",
        title="技术手册-综合管理系统-001",
        doc_type="technical_manual",
        text="",
        fields={
            "system": "综合管理系统",
            "module": "指标采集模块",
            "service": "指标计算服务",
            "interface": "报表导出接口",
            "metric": "日志留存天数",
            "process": "配置发布流程",
            "owner": "业务审核角色",
        },
    )
    case = EvalCase(
        case_id="case-1",
        doc_id="ent-001",
        question_type="multi_hop",
        question="如果指标计算服务异常，可能影响哪个指标并触发哪个流程？",
        expected_keywords=["指标计算服务", "日志留存天数", "配置发布流程"],
    )

    answer = render_structured_answer(document, case)

    assert "指标计算服务" in answer
    assert "日志留存天数" in answer
    assert "配置发布流程" in answer


def test_evaluate_cases_reports_naive_and_structured_delta(tmp_path):
    docs_dir = tmp_path / "documents"
    docs_dir.mkdir()
    doc_path = docs_dir / "ent-001.md"
    doc_path.write_text(
        "\n".join(
            [
                "# 技术手册-综合管理系统-001",
                "综合管理系统面向内网业务提供统一操作入口，核心组件为指标采集模块。",
                "指标采集模块调用指标计算服务。",
            ]
        ),
        encoding="utf-8",
    )
    manifest = {
        "documents": [
            {
                "doc_id": "ent-001",
                "type": "technical_manual",
                "title": "技术手册-综合管理系统-001",
                "path": "documents/ent-001.md",
                "system": "综合管理系统",
                "module": "指标采集模块",
                "service": "指标计算服务",
                "interface": "报表导出接口",
                "metric": "日志留存天数",
                "process": "配置发布流程",
                "owner": "业务审核角色",
            }
        ]
    }
    cases = {
        "cases": [
            {
                "case_id": "case-1",
                "doc_id": "ent-001",
                "question_type": "multi_hop",
                "question": "如果指标计算服务异常，可能影响哪个指标并触发哪个流程？",
                "expected_keywords": ["指标计算服务", "日志留存天数", "配置发布流程"],
            }
        ]
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (tmp_path / "eval_cases.json").write_text(json.dumps(cases), encoding="utf-8")

    report = evaluate_cases(
        dataset_dir=tmp_path,
        manifest_path=tmp_path / "manifest.json",
        cases_path=tmp_path / "eval_cases.json",
        chunk_size=80,
    )

    assert report["summary"]["case_count"] == 1
    assert report["summary"]["naive_chunk"]["keyword_hit_rate"] < 1.0
    assert report["summary"]["structured_kg"]["keyword_hit_rate"] == 1.0
    assert report["summary"]["delta"]["keyword_hit_rate"] > 0
