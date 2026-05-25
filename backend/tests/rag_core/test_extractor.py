"""Tests for the custom rag_core extraction pipeline.

After Step 2 (schema v2 + bilingual prompt + homonym fix), this suite locks
in 7 invariants we want to guard for the long term:

  A. v2 canonical types pass through canonicalize_* unchanged (no drift).
  B. v2 alias tables map Chinese/English synonyms to canonical names;
     unknown types fall back to 'Other' with the right drift_reason.
  C. The extraction prompt is bilingual (EN + ZH directives coexist; type
     listings use English canonical names, not the retired v1 Chinese).
  D. The prompt presents entity types grouped by Tier A-E with tier-first
     guidance, and every ENTITY_TYPES member belongs to some tier.
  E. Same name + different type → preserved as separate homonym nodes
     with a '[type]' disambiguation suffix; relations pointing at a
     homonym are flagged 'homonym_ambiguous'.
  F. Same-type near-duplicates / alias overlaps still merge into one node.
  G. When no homonym conflict exists, names stay un-suffixed (defensive
     guard against an over-eager homonym fix).

The pipeline-orchestration tests at the bottom of this file exercise
behaviors that only emerge from the full extractor (relation scoring,
missing-endpoint detection, alias merging through the orchestrator).
They use a fake_llm fixture as a *transport* — the assertions are about
real downstream behavior of the orchestration layer, not about the LLM.
"""

import json

import pytest

from app.rag_core.extractor import ExtractionConfig, GraphRAGExtractor
from app.rag_core.json_repair import repair_json_payload
from app.rag_core.normalizer import (
    normalize_entities_and_relations,
    normalize_entity_name,
)
from app.rag_core.prompts import _validate_tier_grouping, build_extraction_prompt
from app.rag_core.schemas import (
    Entity,
    Relation,
    canonicalize_entity_type,
    canonicalize_relation_type,
)


# ────────────────────────────────────────────────────────────────────────
# A. v2 canonical types pass through canonicalize_* unchanged
# ────────────────────────────────────────────────────────────────────────


def test_canonicalize_v2_entity_type_returns_canonical_directly():
    """Schema v2: a canonical entity-type name returns unchanged, no drift."""
    result, drift = canonicalize_entity_type("System")
    assert result == "System"
    assert drift is None


def test_canonicalize_v2_relation_type_returns_canonical_directly():
    """Schema v2: a canonical relation-type name returns unchanged, no drift."""
    result, drift = canonicalize_relation_type("DependsOn")
    assert result == "DependsOn"
    assert drift is None


# ────────────────────────────────────────────────────────────────────────
# B. v2 alias mapping (Chinese / English / unknown fallback)
# ────────────────────────────────────────────────────────────────────────


def test_canonicalize_chinese_entity_alias_maps_to_v2_canonical():
    """v2 alias table: Chinese '系统' → 'System' with drift='mapped_alias'."""
    result, drift = canonicalize_entity_type("系统")
    assert result == "System"
    assert drift == "mapped_alias"


def test_canonicalize_english_entity_alias_maps_to_v2_canonical():
    """v2 alias table: English 'Component' → 'Module' with drift='mapped_alias'."""
    result, drift = canonicalize_entity_type("Component")
    assert result == "Module"
    assert drift == "mapped_alias"


def test_canonicalize_chinese_relation_alias_maps_to_v2_canonical():
    """v2 alias table: Chinese '依赖' → 'DependsOn' with drift='mapped_alias'."""
    result, drift = canonicalize_relation_type("依赖")
    assert result == "DependsOn"
    assert drift == "mapped_alias"


def test_canonicalize_unknown_entity_type_falls_back_to_other_with_drift():
    """Unknown type → fallback to 'Other' with drift='unknown_entity_type'.

    This is the 兜底 contract: extraction never crashes on an unrecognized
    LLM-emitted type; we always have a safe canonical to land in.
    """
    result, drift = canonicalize_entity_type("Klingon")
    assert result == "Other"
    assert drift == "unknown_entity_type"


# ────────────────────────────────────────────────────────────────────────
# C. Bilingual prompt
# ────────────────────────────────────────────────────────────────────────


def test_build_extraction_prompt_emits_both_english_and_chinese_directives():
    """Bilingual contract: EN and ZH directives coexist; type listings use
    v2 English canonical names."""
    prompt = build_extraction_prompt("sample chunk")
    # English-side directives
    assert "Extract" in prompt
    assert "Graph RAG" in prompt
    # Chinese-side directives
    assert "抽取" in prompt
    # type lists must be in v2 English canonical
    assert "System" in prompt
    assert "FunctionalRequirement" in prompt


def test_build_extraction_prompt_does_not_resurrect_v1_chinese_canonical_type_names():
    """Schema v1 used '系统' as a canonical entity-type name; v2 retires it.

    The only legitimate occurrence of '系统' in the prompt is inside the
    Tier-B label '系统层'. Stripping that label, no '系统' should remain —
    this guards against an accidental revert to v1 canonicals.
    """
    prompt = build_extraction_prompt("sample chunk")
    stripped = prompt.replace("系统层", "")
    assert "系统" not in stripped


# ────────────────────────────────────────────────────────────────────────
# D. Tier grouping in prompt
# ────────────────────────────────────────────────────────────────────────


def test_build_extraction_prompt_includes_all_five_tier_groups():
    """The prompt must present entity types grouped by Tier A-E and tell the
    LLM to pick a tier first. Flat 15-type listings push the LLM toward 'Other'."""
    prompt = build_extraction_prompt("sample chunk")
    for tier in ("Tier A", "Tier B", "Tier C", "Tier D", "Tier E"):
        assert tier in prompt, f"prompt missing {tier}"
    assert "tier first" in prompt.lower()


def test_every_entity_type_is_covered_by_some_tier():
    """Schema-drift safety: every member of ENTITY_TYPES must belong to some
    declared tier. If somebody adds a new type to schemas.py without updating
    ENTITY_TYPES_BY_TIER, this test fires so we don't silently lose it."""
    assert _validate_tier_grouping() == []


# ────────────────────────────────────────────────────────────────────────
# E. Homonym preservation (core Step 2 bug fix)
# ────────────────────────────────────────────────────────────────────────


def test_normalizer_preserves_homonym_entities_with_disambiguation_suffix():
    """Same name + different types → kept as separate nodes with '[type]' suffix.

    Mirrors the production-KG identity model: a node's identity is
    (name, type), not name alone. Old behavior force-merged them and lost
    two of the three semantic identities depending on input order.
    """
    entities = [
        Entity(name="agent", type="Module", description="software agent module"),
        Entity(name="agent", type="Stakeholder", description="human reviewer"),
        Entity(name="agent", type="ExternalActor", description="third-party agent"),
    ]
    result_entities, _, _ = normalize_entities_and_relations(entities, [])
    assert len(result_entities) == 3
    names = {e.name for e in result_entities}
    assert names == {"agent[Module]", "agent[Stakeholder]", "agent[ExternalActor]"}


def test_normalizer_flags_homonym_relation_endpoint_as_ambiguous():
    """A relation whose source/target name matches a homonym is rewritten to
    one of the disambiguated entities and tagged drift_reason='homonym_ambiguous'
    so downstream evaluation can flag the edge for manual review."""
    entities = [
        Entity(name="agent", type="Module"),
        Entity(name="agent", type="Stakeholder"),
    ]
    relations = [Relation(source="agent", target="LoginSystem", type="DependsOn")]

    _, result_relations, _ = normalize_entities_and_relations(entities, relations)

    assert len(result_relations) == 1
    assert result_relations[0].drift_reason == "homonym_ambiguous"
    # The source is rewritten to one of the disambiguated names (deterministic
    # fallback: the first matching entity).
    assert result_relations[0].source.startswith("agent[")


# ────────────────────────────────────────────────────────────────────────
# F. Same-type merge still works (regression for the homonym fix)
# ────────────────────────────────────────────────────────────────────────


def test_normalizer_merges_same_type_near_duplicate_names():
    """'LoginSystem' and 'LoginSystems' under the same type → one merged node.

    The homonym fix must NOT break same-type near-duplicate merging; that
    would re-introduce node fragmentation.
    """
    entities = [
        Entity(name="LoginSystem", type="Module"),
        Entity(name="LoginSystems", type="Module"),
    ]
    result_entities, _, _ = normalize_entities_and_relations(entities, [])
    assert len(result_entities) == 1


# ────────────────────────────────────────────────────────────────────────
# G. No suffix when there is no homonym conflict (defensive)
# ────────────────────────────────────────────────────────────────────────


def test_normalizer_does_not_add_suffix_when_no_homonym_conflict_exists():
    """Distinct names with distinct types must NOT get a '[type]' suffix.

    Guards against a regression where the homonym fix indiscriminately
    renames every entity. Only true homonym conflicts trigger the suffix.
    """
    entities = [
        Entity(name="LoginSystem", type="Module"),
        Entity(name="LoginUser", type="Stakeholder"),
    ]
    result_entities, _, _ = normalize_entities_and_relations(entities, [])
    assert len(result_entities) == 2
    names = {e.name for e in result_entities}
    assert names == {"LoginSystem", "LoginUser"}
    assert not any("[" in name for name in names), (
        "No '[type]' suffix should appear when names are already unambiguous"
    )


# ────────────────────────────────────────────────────────────────────────
# Utility-level tests (kept — they pin pure-function behavior)
# ────────────────────────────────────────────────────────────────────────


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


# ────────────────────────────────────────────────────────────────────────
# Pipeline-orchestration tests (kept from the prior suite).
#
# These use a fake_llm fixture as a transport. The assertions verify
# real downstream behavior of the orchestrator (alias merging through the
# extractor, missing-endpoint flagging, schema-incompatible-relation
# flagging) — NOT the fake_llm content itself.
# ────────────────────────────────────────────────────────────────────────


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
    assert result.relations[0].confidence == 0.6
    assert "incompatible relation" in result.relations[0].invalid_reason
