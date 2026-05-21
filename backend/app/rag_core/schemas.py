"""Closed schemas for the self-owned Graph RAG extraction layer."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


ENTITY_TYPES = {
    "系统",
    "平台",
    "模块",
    "服务",
    "接口",
    "数据表",
    "指标",
    "设备",
    "文档",
    "人员角色",
    "组织",
    "流程",
    "规范",
    "概念",
    "其他",
}

RELATION_TYPES = {
    "依赖",
    "调用",
    "包含",
    "产生",
    "写入",
    "读取",
    "管理",
    "约束",
    "属于",
    "关联",
    "输入",
    "输出",
    "触发",
    "影响",
}


ENTITY_TYPE_ALIASES = {
    "业务系统": "系统",
    "应用系统": "系统",
    "信息系统": "系统",
    "系统平台": "平台",
    "应用平台": "平台",
    "业务平台": "平台",
    "能力模块": "模块",
    "功能模块": "模块",
    "微服务": "服务",
    "接口服务": "服务",
    "API": "接口",
    "接口配置": "接口",
    "表": "数据表",
    "数据库表": "数据表",
    "数据指标": "指标",
    "性能指标": "指标",
    "终端设备": "设备",
    "硬件设备": "设备",
    "制度": "规范",
    "规程": "规范",
    "部门": "组织",
    "岗位": "人员角色",
    "角色": "人员角色",
}


RELATION_TYPE_ALIASES = {
    "使用": "调用",
    "访问": "调用",
    "请求": "调用",
    "接入": "调用",
    "依赖于": "依赖",
    "组成": "包含",
    "包括": "包含",
    "生成": "产生",
    "上报": "写入",
    "存储": "写入",
    "查询": "读取",
    "负责": "管理",
    "维护": "管理",
    "归属": "属于",
    "隶属": "属于",
    "受控于": "约束",
    "驱动": "触发",
    "输出到": "输出",
    "输入到": "输入",
}


RELATION_COMPATIBILITY = {
    "依赖": {
        "source": {"系统", "平台", "模块", "服务", "接口"},
        "target": {"系统", "平台", "模块", "服务", "接口", "数据表", "规范"},
    },
    "调用": {
        "source": {"系统", "平台", "模块", "服务", "接口"},
        "target": {"系统", "平台", "模块", "服务", "接口"},
    },
    "包含": {
        "source": {"系统", "平台", "模块", "服务", "文档", "组织", "流程"},
        "target": {"模块", "服务", "接口", "数据表", "指标", "设备", "文档", "流程", "规范", "概念"},
    },
    "产生": {
        "source": {"系统", "平台", "模块", "服务", "接口", "设备", "流程"},
        "target": {"数据表", "指标", "文档", "概念"},
    },
    "写入": {
        "source": {"系统", "平台", "模块", "服务", "接口", "流程"},
        "target": {"数据表", "服务", "平台", "系统", "文档"},
    },
    "读取": {
        "source": {"系统", "平台", "模块", "服务", "接口", "流程"},
        "target": {"数据表", "指标", "文档", "服务", "系统", "平台"},
    },
    "管理": {
        "source": {"组织", "人员角色", "系统", "平台", "模块", "服务"},
        "target": {"系统", "平台", "模块", "服务", "接口", "设备", "流程", "文档", "数据表", "指标"},
    },
    "约束": {
        "source": {"规范", "流程", "文档", "组织", "人员角色"},
        "target": {"系统", "平台", "模块", "服务", "接口", "流程", "人员角色", "组织"},
    },
    "属于": {
        "source": {"系统", "平台", "模块", "服务", "接口", "数据表", "设备", "人员角色", "文档"},
        "target": {"系统", "平台", "模块", "组织", "流程", "文档"},
    },
    "输入": {
        "source": {"系统", "平台", "模块", "服务", "接口", "流程"},
        "target": {"数据表", "指标", "文档", "概念", "设备"},
    },
    "输出": {
        "source": {"系统", "平台", "模块", "服务", "接口", "流程", "设备"},
        "target": {"数据表", "指标", "文档", "概念", "人员角色"},
    },
    "触发": {
        "source": {"系统", "平台", "模块", "服务", "接口", "指标", "设备", "流程"},
        "target": {"流程", "服务", "模块", "系统", "人员角色"},
    },
    "影响": {
        "source": {"系统", "平台", "模块", "服务", "接口", "指标", "设备", "流程", "规范"},
        "target": {"系统", "平台", "模块", "服务", "接口", "指标", "流程"},
    },
}


def canonicalize_entity_type(raw_type: str | None) -> tuple[str, str | None]:
    value = str(raw_type or "其他").strip() or "其他"
    if value in ENTITY_TYPES:
        return value, None
    if value in ENTITY_TYPE_ALIASES:
        return ENTITY_TYPE_ALIASES[value], "mapped_alias"
    return "其他", "unknown_entity_type"


def canonicalize_relation_type(raw_type: str | None) -> tuple[str, str | None]:
    value = str(raw_type or "关联").strip() or "关联"
    if value in RELATION_TYPES:
        return value, None
    if value in RELATION_TYPE_ALIASES:
        return RELATION_TYPE_ALIASES[value], "mapped_alias"
    return "关联", "unknown_relation_type"


class Entity(BaseModel):
    """Normalized enterprise-document entity."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    type: str = Field(default="其他")
    raw_type: str = Field(default="")
    canonical_type: str = Field(default="其他")
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
    type: str = Field(default="关联")
    raw_type: str = Field(default="")
    canonical_type: str = Field(default="关联")
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
