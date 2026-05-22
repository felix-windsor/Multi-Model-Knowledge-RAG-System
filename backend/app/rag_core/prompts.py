"""Bilingual extraction prompts for software-project documents (schema v2).

Design:
- Bilingual (EN + ZH) instructions for an 81.5% EN / 18.5% ZH corpus.
- Entity / relation types are emitted in English canonical names only (v2).
- Entity types are presented grouped by tier (A-E) to help the LLM scope
  type selection (pick a tier first, then a concrete type) rather than
  defaulting to "Other" when overwhelmed by a flat 15-type list.
- 7 hard rules distilled from 5 schema review iterations are embedded inline.
- Schema-agnostic: only references ENTITY_TYPES / RELATION_TYPES interface;
  any ENTITY_TYPES not covered by ENTITY_TYPES_BY_TIER are surfaced under a
  fallback "Tier Z" group so they never silently disappear from the prompt.
"""

from app.rag_core.schemas import ENTITY_TYPES, RELATION_TYPES


# Tier grouping mirrors the 5-tier structure documented in schemas.py.
# Keep this in sync when adding new entity types to ENTITY_TYPES.
ENTITY_TYPES_BY_TIER: dict[str, list[str]] = {
    "A — Requirements 需求层": [
        "FunctionalRequirement",
        "NonFunctionalRequirement",
        "UserStory",
        "AcceptanceCriteria",
    ],
    "B — System 系统层": ["System", "Module", "Interface", "DataEntity"],
    "C — Actors 角色层": ["Stakeholder", "Team", "ExternalActor"],
    "D — Process 流程层": ["Process", "Decision", "Constraint"],
    "E — Fallback 兜底": ["Other"],
}


def _validate_tier_grouping() -> list[str]:
    """Return ENTITY_TYPES not covered by any tier (empty when complete)."""
    grouped: set[str] = set()
    for types in ENTITY_TYPES_BY_TIER.values():
        grouped.update(types)
    return sorted(ENTITY_TYPES - grouped)


def _format_entity_types_by_tier() -> str:
    """Render ENTITY_TYPES_BY_TIER as a multi-line tier listing.

    Schema-drift safe:
    - Drops any tier entries no longer present in ENTITY_TYPES (defensive).
    - Appends a "Tier Z — Unclassified" group for any ENTITY_TYPES not
      covered by any declared tier, so new types never disappear silently.
    """
    lines: list[str] = []
    for tier_name, types in ENTITY_TYPES_BY_TIER.items():
        present = [t for t in types if t in ENTITY_TYPES]
        if present:
            lines.append(f"Tier {tier_name}: {', '.join(present)}")
    unclassified = _validate_tier_grouping()
    if unclassified:
        lines.append(f"Tier Z — Unclassified 未分类: {', '.join(unclassified)}")
    return "\n".join(lines)


_RULES = """[RULES - 7 条抽取硬约束]

R1 Skip 跳过：markdown section headers; fenced ``` code blocks; mermaid / sequenceDiagram / flowchart diagrams; inline code (`xxx.ts`, `function()`); file paths and CLI commands.

R2 Do NOT extract as entities 不要抽：code symbols / function / class names (parseDocument(), class UserModel); file paths (src/cli.ts); CLI tools (gh, npm, yarn); abstract quality words (efficiency, scalability, usability); standalone status values (Draft, Ready, Done); attribute values — numbers, percentages, dates (62.8%, 25K tokens, Q1 2026).

R3 Name 字段：3-8 chars (EN) or 3-8 汉字 (ZH). Preserve doc language (EN doc → EN name; ZH doc → ZH name). NOT generic section labels ("Full user flow"). `type` is ALWAYS English canonical regardless of doc language.

R4 Context-aware type 上下文判断：software code → Module / Interface / System; user or operator → Stakeholder / ExternalActor; inside the system → Stakeholder / Module; outside party → ExternalActor. Same word may map to different types in different docs — judge by THIS doc.

R5 Homonym 同名异义：same name with different type → keep as separate entities (do NOT force-merge). Disambiguate by suffix in name, e.g. "agent[Module]" vs "agent[ExternalActor]".

R6 Granularity 抽取粒度：Priority + Version + Timeline triple → ONE Constraint (not three). State machine → ONE Process (not one per state). Section header itself → skip; extract the content below.

R7 Meta vs business 元数据与业务："This PRD describes ..." → PRD is meta, skip. "PRD lifecycle management" → PRD is a business object, extract as DataEntity. Verb test: describes / outlines = meta; manage / track / store = business."""


_JSON_FORMAT = """[OUTPUT JSON]
{"entities":[{"name":"...","type":"Module","subtype":"","description":"summary from source","aliases":[],"attributes":{}}],"relations":[{"source":"entity name","target":"entity name","type":"DependsOn","description":"...","evidence":"short quote"}]}

[OUTPUT CONSTRAINTS]
- Output exactly ONE JSON object — no markdown fence, no preamble, no postscript.
- `type` MUST be an English canonical name from the closed lists above.
- relation.source / relation.target MUST each appear in entities[].name.
- Relation direction follows active voice ("A depends on B" → A -> DependsOn -> B; "A is constrained by B" → B -> Constrains -> A).
- If nothing extractable, return {"entities":[],"relations":[]}."""


def build_extraction_prompt(chunk_text: str, chunk_id: str | None = None) -> str:
    """Build a strict JSON extraction prompt for one document chunk.

    Bilingual (EN + ZH) prompt for software project documents (PRD / SRS / TDD).
    Type names in the output JSON are always English canonical (v2 schema),
    regardless of the document language.
    """
    entity_types_block = _format_entity_types_by_tier()
    relation_types = ", ".join(sorted(RELATION_TYPES))
    chunk_label = chunk_id or "unknown"

    return f"""[ROLE] Entity-relation extractor for software project docs (PRD / SRS / TDD). 软件项目文档实体关系抽取器。

[TASK] Extract entities and relations from the chunk below for Graph RAG. 从下面文档片段抽取实体与关系，用于 Graph RAG 检索。

[ENTITY TYPES] (closed list — pick a tier first, then a type; choose Other only as a last resort)
{entity_types_block}

[RELATION TYPES] (closed list)
{relation_types}

{_RULES}

{_JSON_FORMAT}

[CHUNK ID] {chunk_label}

[DOCUMENT CHUNK]
{chunk_text}
"""
