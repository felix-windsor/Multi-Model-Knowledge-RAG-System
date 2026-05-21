import json

import pytest

from app.rag_core.extractor import ExtractionConfig, GraphRAGExtractor
from app.rag_core.json_repair import repair_json_payload
from app.rag_core.normalizer import normalize_entity_name


def test_repair_json_payload_extracts_markdown_code_fence():
    raw = """模型输出如下：

```json
{
  "entities": [{"name": "统一身份认证平台", "type": "平台"}],
  "relations": []
}
```
"""

    result = repair_json_payload(raw)

    assert result.success is True
    assert result.payload["entities"][0]["name"] == "统一身份认证平台"


def test_normalize_entity_name_removes_common_wrappers_and_spaces():
    assert normalize_entity_name("《 信息系统平台 》") == "信息系统平台"
    assert normalize_entity_name("统一 身份 认证 平台") == "统一身份认证平台"


@pytest.mark.asyncio
async def test_extract_chunk_preserves_raw_types_and_maps_known_drift_to_canonical_schema():
    async def fake_llm(prompt, system_prompt=None, **kwargs):
        return {
            "entities": [
                {"name": "综合管理系统", "type": "业务系统", "description": "企业内部业务管理系统"},
                {"name": "统一身份认证平台", "type": "应用平台", "description": "提供用户登录认证能力"},
            ],
            "relations": [
                {
                    "source": "综合管理系统",
                    "target": "统一身份认证平台",
                    "type": "使用",
                    "description": "综合管理系统使用统一身份认证平台完成登录",
                    "evidence": "通过统一身份认证平台完成用户登录",
                }
            ],
        }

    extractor = GraphRAGExtractor(fake_llm)
    result = await extractor.extract_chunk("综合管理系统通过统一身份认证平台完成用户登录。")

    assert result.metrics.entity_type_drift_count == 2
    assert result.metrics.relation_type_drift_count == 1
    assert result.entities[0].raw_type == "业务系统"
    assert result.entities[0].type == "系统"
    assert result.entities[1].raw_type == "应用平台"
    assert result.entities[1].type == "平台"
    assert result.relations[0].raw_type == "使用"
    assert result.relations[0].type == "调用"
    assert result.relations[0].valid is True


@pytest.mark.asyncio
async def test_extract_chunk_maps_type_drift_and_scores_relations():
    async def fake_llm(prompt, system_prompt=None, **kwargs):
        assert "只输出一个 JSON 对象" in prompt
        return json.dumps(
            {
                "entities": [
                    {
                        "name": "综合管理系统",
                        "type": "未知业务类型",
                        "description": "企业内部业务管理系统",
                    },
                    {
                        "name": "统一身份认证平台",
                        "type": "平台",
                        "description": "提供用户登录认证能力",
                    },
                ],
                "relations": [
                    {
                        "source": "综合管理系统",
                        "target": "统一身份认证平台",
                        "type": "协同",
                        "description": "综合管理系统使用统一身份认证平台完成登录",
                        "evidence": "通过统一身份认证平台完成用户登录",
                    }
                ],
            },
            ensure_ascii=False,
        )

    extractor = GraphRAGExtractor(fake_llm)
    result = await extractor.extract_chunk(
        "综合管理系统通过统一身份认证平台完成用户登录。",
        chunk_id="chunk-1",
    )

    assert result.metrics.json_parse_success is True
    assert result.metrics.schema_validation_success is True
    assert result.metrics.entity_type_drift_count == 1
    assert result.metrics.relation_type_drift_count == 1
    assert result.entities[0].type == "其他"
    assert result.relations[0].type == "关联"
    assert result.relations[0].valid is True
    assert result.relations[0].confidence >= 0.8


@pytest.mark.asyncio
async def test_extract_chunk_merges_near_duplicate_entities():
    async def fake_llm(prompt, system_prompt=None, **kwargs):
        return {
            "entities": [
                {"name": "信息系统", "type": "系统", "description": "内部系统"},
                {
                    "name": "信息系统平台",
                    "type": "平台",
                    "description": "内部系统平台",
                    "aliases": ["信息系统"],
                },
            ],
            "relations": [],
        }

    extractor = GraphRAGExtractor(fake_llm)
    result = await extractor.extract_chunk("信息系统平台负责统一管理。")

    assert result.metrics.entities_before_normalization == 2
    assert result.metrics.entities_after_normalization == 1
    assert result.entities[0].name == "信息系统平台"
    assert "信息系统" in result.entities[0].aliases


@pytest.mark.asyncio
async def test_extract_chunk_marks_relation_with_missing_endpoint_invalid():
    async def fake_llm(prompt, system_prompt=None, **kwargs):
        return {
            "entities": [
                {"name": "审计服务", "type": "服务", "description": "记录日志"}
            ],
            "relations": [
                {
                    "source": "综合管理系统",
                    "target": "审计服务",
                    "type": "写入",
                    "description": "综合管理系统写入审计日志",
                }
            ],
        }

    extractor = GraphRAGExtractor(fake_llm, ExtractionConfig(drop_invalid_relations=False))
    result = await extractor.extract_chunk("审计服务记录操作日志。")

    assert result.metrics.invalid_relation_count == 1
    assert result.relations[0].valid is False
    assert result.relations[0].confidence < 0.5
    assert "missing endpoint" in result.relations[0].invalid_reason


@pytest.mark.asyncio
async def test_extract_chunk_marks_schema_incompatible_relation_invalid():
    async def fake_llm(prompt, system_prompt=None, **kwargs):
        return {
            "entities": [
                {"name": "运维部门", "type": "组织", "description": "负责运维管理"},
                {"name": "平均响应时间", "type": "指标", "description": "服务性能指标"},
            ],
            "relations": [
                {
                    "source": "运维部门",
                    "target": "平均响应时间",
                    "type": "读取",
                    "description": "运维部门读取平均响应时间",
                    "evidence": "运维部门读取平均响应时间",
                }
            ],
        }

    extractor = GraphRAGExtractor(fake_llm, ExtractionConfig(drop_invalid_relations=False))
    result = await extractor.extract_chunk("运维部门读取平均响应时间。")

    assert result.metrics.invalid_relation_count == 1
    assert result.relations[0].valid is False
    assert result.relations[0].confidence < 0.6
    assert "incompatible relation" in result.relations[0].invalid_reason
