"""Closed schemas for the self-owned Graph RAG extraction layer.

Schema v2: software project documents (PRD/SRS/TDD).
- 15 entity types organized in 5 tiers
- 14 relation types organized in 5 tiers
- Canonical type names in English (multilingual prompt support)
- Alias mapping supports Chinese / English / common synonyms
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


SCHEMA_VERSION = "2.0.0"
SCHEMA_APPLICABLE_DOMAIN = "software_project_docs"


ENTITY_TYPES = {
    # Tier A: 需求层 (4)
    "FunctionalRequirement",
    "NonFunctionalRequirement",
    "UserStory",
    "AcceptanceCriteria",
    # Tier B: 系统层 (4)
    "System",
    "Module",
    "Interface",
    "DataEntity",
    # Tier C: 角色层 (3)
    "Stakeholder",
    "Team",
    "ExternalActor",
    # Tier D: 流程层 (3)
    "Process",
    "Decision",
    "Constraint",
    # Tier E: 兜底 (1)
    "Other",
}


RELATION_TYPES = {
    # Tier A: 需求拆解 (4)
    "Refines",
    "Satisfies",
    "Constrains",
    "DependsOn",
    # Tier B: 实现链 (3)
    "ImplementedBy",
    "PartOf",
    "Exposes",
    # Tier C: 责任链 (3)
    "OwnedBy",
    "ParticipatesIn",
    "Approves",
    # Tier D: 流程决策 (3)
    "Triggers",
    "Affects",
    "Manipulates",
    # Tier E: 兜底 (1)
    "RelatedTo",
}


ENTITY_TYPE_ALIASES = {
    # FunctionalRequirement
    "FR": "FunctionalRequirement",
    "Functional Requirement": "FunctionalRequirement",
    "功能需求": "FunctionalRequirement",
    "需求": "FunctionalRequirement",
    "Feature": "FunctionalRequirement",
    "Requirement": "FunctionalRequirement",
    # NonFunctionalRequirement
    "NFR": "NonFunctionalRequirement",
    "Non-Functional Requirement": "NonFunctionalRequirement",
    "非功能需求": "NonFunctionalRequirement",
    "Quality Attribute": "NonFunctionalRequirement",
    "Performance Requirement": "NonFunctionalRequirement",
    # UserStory
    "User Story": "UserStory",
    "用户故事": "UserStory",
    "Story": "UserStory",
    "Use Case": "UserStory",
    # AcceptanceCriteria
    "AC": "AcceptanceCriteria",
    "Acceptance Criterion": "AcceptanceCriteria",
    "验收标准": "AcceptanceCriteria",
    "DOD": "AcceptanceCriteria",
    "Definition of Done": "AcceptanceCriteria",
    # System
    "Application": "System",
    "Product": "System",
    "Platform": "System",
    "应用": "System",
    "系统": "System",
    "平台": "System",
    # Module
    "Component": "Module",
    "Subsystem": "Module",
    "模块": "Module",
    "组件": "Module",
    "Service": "Module",
    "服务": "Module",
    # Interface
    "API": "Interface",
    "Endpoint": "Interface",
    "接口": "Interface",
    "Integration Point": "Interface",
    "CLI": "Interface",
    # DataEntity
    "Entity": "DataEntity",
    "Data Object": "DataEntity",
    "Table": "DataEntity",
    "数据表": "DataEntity",
    "数据实体": "DataEntity",
    "Model": "DataEntity",
    # Stakeholder
    "Person": "Stakeholder",
    "User": "Stakeholder",
    "Role": "Stakeholder",
    "角色": "Stakeholder",
    "干系人": "Stakeholder",
    "Actor": "Stakeholder",
    # Team
    "Department": "Team",
    "Group": "Team",
    "团队": "Team",
    "部门": "Team",
    # ExternalActor
    "External User": "ExternalActor",
    "Customer": "ExternalActor",
    "Third Party": "ExternalActor",
    "外部用户": "ExternalActor",
    "客户": "ExternalActor",
    "External Service": "ExternalActor",
    "Competitor": "ExternalActor",
    "Court": "ExternalActor",
    "Agency": "ExternalActor",
    "Organization": "ExternalActor",
    # Process
    "Workflow": "Process",
    "Procedure": "Process",
    "流程": "Process",
    "工作流": "Process",
    "Flow": "Process",
    # Decision
    "Design Decision": "Decision",
    "Architectural Decision": "Decision",
    "ADR": "Decision",
    "决策": "Decision",
    "Approval": "Decision",
    "Key Decision": "Decision",
    # Constraint
    "Restriction": "Constraint",
    "Limitation": "Constraint",
    "约束": "Constraint",
    "限制": "Constraint",
    "Regulation": "Constraint",
    "Priority": "Constraint",
    "Complexity Score": "Constraint",
    # LightRAG default entity types (lowercased by LightRAG internally)
    # Both lowercase and capitalized variants for safety
    "concept": "Other",
    "Concept": "Other",
    "method": "Module",
    "Method": "Module",
    "artifact": "Module",
    "Artifact": "Module",
    "content": "DataEntity",
    "Content": "DataEntity",
    "data": "DataEntity",
    "Data": "DataEntity",
    "organization": "ExternalActor",
    "Organization": "ExternalActor",
    "event": "Process",
    "Event": "Process",
    "location": "Other",
    "Location": "Other",
    "geo": "Other",
    "Geo": "Other",
    "person": "Stakeholder",
    "Person": "Stakeholder",
    "category": "Other",
    "Category": "Other",
}


RELATION_TYPE_ALIASES = {
    # Refines
    "refines": "Refines",
    "细化": "Refines",
    "拆解": "Refines",
    "breaks_down": "Refines",
    # Satisfies
    "verifies": "Satisfies",
    "tests": "Satisfies",
    "covers": "Satisfies",
    "验证": "Satisfies",
    "覆盖": "Satisfies",
    # Constrains
    "limits": "Constrains",
    "restricts": "Constrains",
    "约束": "Constrains",
    "限制": "Constrains",
    # DependsOn
    "depends_on": "DependsOn",
    "requires": "DependsOn",
    "依赖": "DependsOn",
    "需要": "DependsOn",
    "blocked_by": "DependsOn",
    # ImplementedBy
    "implements": "ImplementedBy",
    "realizes": "ImplementedBy",
    "实现": "ImplementedBy",
    # PartOf
    "belongs_to": "PartOf",
    "属于": "PartOf",
    # Exposes
    "provides": "Exposes",
    "publishes": "Exposes",
    "暴露": "Exposes",
    "提供": "Exposes",
    # OwnedBy
    "owned_by": "OwnedBy",
    "responsible_for": "OwnedBy",
    "assigned_to": "OwnedBy",
    "负责": "OwnedBy",
    "归属": "OwnedBy",
    # ParticipatesIn
    "participates": "ParticipatesIn",
    "involved_in": "ParticipatesIn",
    "参与": "ParticipatesIn",
    # Approves
    "approved_by": "Approves",
    "signed_off": "Approves",
    "批准": "Approves",
    "审批": "Approves",
    # Triggers
    "starts": "Triggers",
    "initiates": "Triggers",
    "触发": "Triggers",
    "启动": "Triggers",
    # Affects
    "impacts": "Affects",
    "influences": "Affects",
    "影响": "Affects",
    # Manipulates
    "reads": "Manipulates",
    "writes": "Manipulates",
    "updates": "Manipulates",
    "queries": "Manipulates",
    "读取": "Manipulates",
    "写入": "Manipulates",
    "操作": "Manipulates",
    # RelatedTo (兜底)
    "associated_with": "RelatedTo",
    "related": "RelatedTo",
    "关联": "RelatedTo",
}


RELATION_COMPATIBILITY = {
    "Refines": {
        "source": {"UserStory", "FunctionalRequirement"},
        "target": {"FunctionalRequirement", "AcceptanceCriteria"},
    },
    "Satisfies": {
        "source": {"AcceptanceCriteria", "UserStory"},
        "target": {"FunctionalRequirement", "NonFunctionalRequirement"},
    },
    "Constrains": {
        "source": {"NonFunctionalRequirement", "Constraint"},
        "target": {"System", "Module", "Interface", "FunctionalRequirement", "Process"},
    },
    "DependsOn": {
        "source": {"FunctionalRequirement", "NonFunctionalRequirement", "Module", "System", "Interface"},
        "target": {"FunctionalRequirement", "NonFunctionalRequirement", "Module", "System", "Interface", "DataEntity"},
    },
    "ImplementedBy": {
        "source": {"FunctionalRequirement", "UserStory"},
        "target": {"Module", "Interface", "System"},
    },
    "PartOf": {
        "source": {"Module", "Interface", "Process", "Stakeholder"},
        "target": {"System", "Module", "Team"},
    },
    "Exposes": {
        "source": {"Module", "System"},
        "target": {"Interface"},
    },
    "OwnedBy": {
        "source": {"FunctionalRequirement", "NonFunctionalRequirement", "Module", "System", "Process", "Decision"},
        "target": {"Stakeholder", "Team"},
    },
    "ParticipatesIn": {
        "source": {"Stakeholder", "Team", "ExternalActor"},
        "target": {"Process", "Decision"},
    },
    "Approves": {
        "source": {"Stakeholder", "Team"},
        "target": {"Decision", "FunctionalRequirement", "NonFunctionalRequirement"},
    },
    "Triggers": {
        "source": {"Process", "Decision", "FunctionalRequirement"},
        "target": {"Process", "Decision"},
    },
    "Affects": {
        "source": {"Decision", "Constraint", "NonFunctionalRequirement"},
        "target": {"System", "Module", "FunctionalRequirement", "Process"},
    },
    "Manipulates": {
        "source": {"Process", "Module", "Interface"},
        "target": {"DataEntity"},
    },
}


def canonicalize_entity_type(raw_type: str | None) -> tuple[str, str | None]:
    """Canonicalize entity type to v2 canonical names. Default fallback: Other."""
    value = str(raw_type or "Other").strip() or "Other"
    if value in ENTITY_TYPES:
        return value, None
    if value in ENTITY_TYPE_ALIASES:
        return ENTITY_TYPE_ALIASES[value], "mapped_alias"
    return "Other", "unknown_entity_type"


def canonicalize_relation_type(raw_type: str | None) -> tuple[str, str | None]:
    """Canonicalize relation type to v2 canonical names. Default fallback: RelatedTo."""
    value = str(raw_type or "RelatedTo").strip() or "RelatedTo"
    if value in RELATION_TYPES:
        return value, None
    if value in RELATION_TYPE_ALIASES:
        return RELATION_TYPE_ALIASES[value], "mapped_alias"
    return "RelatedTo", "unknown_relation_type"


class Entity(BaseModel):
    """Normalized enterprise-document entity."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    type: str = Field(default="Other")
    raw_type: str = Field(default="")
    canonical_type: str = Field(default="Other")
    subtype: str = Field(default="")
    description: str = Field(default="")
    aliases: list[str] = Field(default_factory=list)
    attributes: dict[str, Any] = Field(default_factory=dict)
    drift_reason: str | None = None
    source_chunk_id: str | None = None


class Relation(BaseModel):
    """Normalized relation between two extracted entities."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    type: str = Field(default="RelatedTo")
    raw_type: str = Field(default="")
    canonical_type: str = Field(default="RelatedTo")
    description: str = Field(default="")
    evidence: str = Field(default="")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    valid: bool = True
    invalid_reason: str | None = None
    drift_reason: str | None = None
    source_chunk_id: str | None = None


class ExtractionMetrics(BaseModel):
    """Operational metrics for extraction quality and drift diagnosis."""

    model_config = ConfigDict(extra="forbid")

    json_parse_success: bool = False
    schema_validation_success: bool = False
    entity_type_drift_count: int = 0
    relation_type_drift_count: int = 0
    entities_before_normalization: int = 0
    entities_after_normalization: int = 0
    relations_before_filtering: int = 0
    relations_after_filtering: int = 0
    invalid_relation_count: int = 0
    elapsed_ms: float = 0.0


class ExtractionResult(BaseModel):
    """Final extraction result returned by the custom core."""

    model_config = ConfigDict(extra="forbid")

    entities: list[Entity] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)
    metrics: ExtractionMetrics = Field(default_factory=ExtractionMetrics)
