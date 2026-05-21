import pytest

from app.services.extraction_sidecar_service import ExtractionSidecarService


class FakeRAG:
    def __init__(self):
        self.llm_model_func = self.fake_llm
        self.parse_calls = []

    async def parse_document(self, file_path, display_stats=False, **kwargs):
        self.parse_calls.append({"file_path": file_path, "display_stats": display_stats, "kwargs": kwargs})
        return [
            {
                "type": "text",
                "text": "综合管理系统通过统一身份认证平台完成用户登录，并将操作日志写入审计服务。",
            }
        ], "parsed-doc-1"

    async def fake_llm(self, prompt, **kwargs):
        return {
            "entities": [
                {"name": "综合管理系统", "type": "业务系统"},
                {"name": "统一身份认证平台", "type": "平台"},
                {"name": "审计服务", "type": "服务"},
            ],
            "relations": [
                {"source": "综合管理系统", "target": "统一身份认证平台", "type": "使用"},
                {"source": "综合管理系统", "target": "审计服务", "type": "写入"},
            ],
        }


@pytest.mark.asyncio
async def test_extraction_sidecar_parses_document_and_returns_quality_report():
    rag = FakeRAG()
    service = ExtractionSidecarService(max_chars=1200)

    report = await service.run_for_document(rag, "/tmp/example.md", parse_kwargs={"formula": False})

    assert rag.parse_calls == [
        {"file_path": "/tmp/example.md", "display_stats": False, "kwargs": {"formula": False}}
    ]
    assert report["enabled"] is True
    assert report["parsed_doc_id"] == "parsed-doc-1"
    assert report["chunk_count"] == 1
    assert report["aggregate"]["entity_type_drift_count"] == 1
    assert report["aggregate"]["relation_type_drift_count"] == 1
    assert report["aggregate"]["top_entity_type_drifts"] == [
        {"raw_type": "业务系统", "canonical_type": "系统", "count": 1}
    ]
    assert report["aggregate"]["top_relation_type_drifts"] == [
        {"raw_type": "使用", "canonical_type": "调用", "count": 1}
    ]
