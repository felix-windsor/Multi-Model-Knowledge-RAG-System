"""Chinese enterprise-document prompts for custom entity/relation extraction."""

from app.rag_core.schemas import ENTITY_TYPES, RELATION_TYPES


def build_extraction_prompt(chunk_text: str, chunk_id: str | None = None) -> str:
    """Build a strict JSON extraction prompt for one document chunk."""
    entity_types = "、".join(sorted(ENTITY_TYPES))
    relation_types = "、".join(sorted(RELATION_TYPES))
    chunk_label = chunk_id or "unknown"

    return f"""你是企业内网知识图谱 RAG 系统的信息抽取模块。

任务：从一个中文企业文档片段中抽取实体和关系，用于后续 Graph RAG 检索。

约束：
1. 只输出一个 JSON 对象，不要输出 Markdown、解释、前后缀文本。
2. entities 中的 type 必须尽量从以下闭集选择：{entity_types}。
3. relations 中的 type 必须尽量从以下闭集选择：{relation_types}。
4. 不确定类型时，实体 type 使用“其他”，关系 type 使用“关联”。
5. relation.source 和 relation.target 必须引用 entities 中出现过的实体名称。
6. evidence 填写原文中支持该关系的短证据；没有证据时留空字符串。
7. 关系方向按语义主动方填写。例如“A 依赖 B”写 A -> 依赖 -> B；“A 受 B 约束”写 B -> 约束 -> A。
8. 如能判断更细粒度类别，可在 subtype 填写；如有单位、阈值、周期等结构化信息，可放入 attributes。

输出 JSON 结构：
{{
  "entities": [
    {{
      "name": "实体名称",
      "type": "系统",
      "subtype": "可选细分类别",
      "description": "基于原文的一句话说明",
      "aliases": ["可选别名"],
      "attributes": {{"key": "value"}}
    }}
  ],
  "relations": [
    {{
      "source": "源实体名称",
      "target": "目标实体名称",
      "type": "依赖",
      "description": "关系说明",
      "evidence": "原文证据"
    }}
  ]
}}

chunk_id: {chunk_label}

文档片段：
{chunk_text}
"""
