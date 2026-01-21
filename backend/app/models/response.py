"""响应数据模型"""
from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Optional, List, Dict, Any
from datetime import datetime
import uuid

T = TypeVar("T")


# ============================================
# V1 API 统一响应格式
# ============================================

class APIResponse(BaseModel, Generic[T]):
    """
    V1 API 统一响应格式

    成功响应:
    {
        "code": 0,
        "message": "success",
        "data": { ... },
        "request_id": "uuid-xxx"
    }
    """
    code: int = Field(default=0, description="状态码，0 表示成功")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="请求唯一标识")


# ============================================
# V1 API 数据模型
# ============================================

class V1UploadData(BaseModel):
    """V1 文档上传响应数据"""
    doc_id: str = Field(..., description="文档 ID")
    task_id: str = Field(..., description="任务 ID")
    status: str = Field(default="processing", description="处理状态")
    filename: str = Field(..., description="文件名")


class V1DocumentData(BaseModel):
    """V1 文档详情数据"""
    doc_id: str = Field(..., description="文档 ID")
    filename: str = Field(..., description="文件名")
    status: str = Field(..., description="状态: processing, completed, failed")
    progress: int = Field(default=0, description="进度 (0-100)")
    entities_count: int = Field(default=0, description="实体数量")
    relations_count: int = Field(default=0, description="关系数量")
    created_at: Optional[str] = Field(default=None, description="创建时间 (ISO 8601)")
    completed_at: Optional[str] = Field(default=None, description="完成时间 (ISO 8601)")
    error_message: Optional[str] = Field(default=None, description="错误信息")


class V1DocumentListData(BaseModel):
    """V1 文档列表响应数据"""
    total: int = Field(..., description="文档总数")
    documents: List[V1DocumentData] = Field(..., description="文档列表")


class V1QuerySource(BaseModel):
    """V1 查询来源"""
    doc_id: str = Field(default="", description="文档 ID")
    chunk: str = Field(default="", description="相关文本片段")
    score: float = Field(default=0.0, description="相关度分数")


class V1QueryUsage(BaseModel):
    """V1 查询 Token 使用量"""
    prompt_tokens: int = Field(default=0, description="Prompt Token 数")
    completion_tokens: int = Field(default=0, description="Completion Token 数")


class V1QueryData(BaseModel):
    """V1 查询响应数据"""
    answer: str = Field(..., description="回答内容")
    sources: List[V1QuerySource] = Field(default_factory=list, description="来源列表")
    entities: List[str] = Field(default_factory=list, description="相关实体")
    usage: V1QueryUsage = Field(default_factory=V1QueryUsage, description="Token 使用量")


class V1GraphNode(BaseModel):
    """V1 图谱节点"""
    id: str = Field(..., description="节点 ID")
    label: str = Field(..., description="节点标签")
    type: str = Field(default="concept", description="节点类型")
    description: str = Field(default="", description="节点描述")


class V1GraphEdge(BaseModel):
    """V1 图谱边"""
    from_node: str = Field(..., alias="from", description="起始节点 ID")
    to_node: str = Field(..., alias="to", description="目标节点 ID")
    label: str = Field(default="", description="边标签")

    class Config:
        populate_by_name = True


class V1GraphData(BaseModel):
    """V1 图谱数据"""
    nodes: List[V1GraphNode] = Field(..., description="节点列表")
    edges: List[V1GraphEdge] = Field(..., description="边列表")


class V1GraphStatsData(BaseModel):
    """V1 图谱统计数据"""
    total_entities: int = Field(default=0, description="实体总数")
    total_relations: int = Field(default=0, description="关系总数")
    entity_types: Dict[str, int] = Field(default_factory=dict, description="实体类型分布")
    top_entities: List[Dict[str, Any]] = Field(default_factory=list, description="Top 实体")


class V1TaskData(BaseModel):
    """V1 任务状态数据"""
    task_id: str = Field(..., description="任务 ID")
    doc_id: str = Field(..., description="关联文档 ID")
    status: str = Field(..., description="状态: pending, processing, completed, failed, cancelled")
    progress: int = Field(default=0, description="进度 (0-100)")
    step: str = Field(default="", description="当前步骤描述")
    created_at: Optional[str] = Field(default=None, description="创建时间")
    updated_at: Optional[str] = Field(default=None, description="更新时间")
    error_message: Optional[str] = Field(default=None, description="错误信息")


class V1ConfigData(BaseModel):
    """V1 配置数据（脱敏）"""
    llm_provider: str = Field(..., description="LLM 提供商")
    llm_model: str = Field(..., description="LLM 模型")
    embedding_provider: str = Field(..., description="Embedding 提供商")
    embedding_model: str = Field(..., description="Embedding 模型")
    embedding_dim: int = Field(..., description="Embedding 维度")
    storage_dir: str = Field(..., description="存储目录")


class V1HealthData(BaseModel):
    """V1 健康检查数据"""
    status: str = Field(default="healthy", description="服务状态")
    version: str = Field(default="1.0.0", description="API 版本")
    rag_initialized: bool = Field(default=False, description="RAG 是否已初始化")


# ============================================
# 旧版响应模型（保持向后兼容）
# ============================================

class UploadResponse(BaseModel):
    """文档上传响应"""
    success: bool = Field(..., description="是否成功")
    doc_id: str = Field(..., description="文档 ID")
    filename: str = Field(..., description="文件名")
    size: int = Field(..., description="文件大小（字节）")
    status: str = Field(default="processing", description="处理状态")
    message: str = Field(default="文件上传成功，正在处理中", description="消息")


class DocumentStatus(BaseModel):
    """文档处理状态"""
    doc_id: str = Field(..., description="文档 ID")
    filename: str = Field(..., description="文件名")
    status: str = Field(..., description="状态: processing, completed, failed")
    progress: int = Field(default=0, description="进度 (0-100)")
    step: str = Field(default="", description="当前步骤描述")
    chunks_count: int = Field(default=0, description="已处理的块数量")
    error_message: Optional[str] = Field(default=None, description="错误信息")
    created_at: Optional[datetime] = Field(default=None, description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")


class DocumentListResponse(BaseModel):
    """文档列表响应"""
    total: int = Field(..., description="文档总数")
    documents: List[Dict[str, Any]] = Field(..., description="文档列表")


class QueryResponse(BaseModel):
    """查询响应"""
    answer: str = Field(..., description="回答内容")
    sources: List[str] = Field(default_factory=list, description="来源文件列表")
    query_time: float = Field(..., description="查询耗时（秒）")


class GraphNode(BaseModel):
    """图谱节点"""
    id: str = Field(..., description="节点 ID")
    label: str = Field(..., description="节点标签")
    type: str = Field(default="concept", description="节点类型")
    description: str = Field(default="", description="节点描述")
    color: str = Field(default="#9E9E9E", description="节点颜色")
    shape: str = Field(default="dot", description="节点形状")


class GraphEdge(BaseModel):
    """图谱边"""
    from_id: str = Field(..., description="起始节点 ID", alias="from")
    to_id: str = Field(..., description="目标节点 ID", alias="to")
    label: str = Field(default="", description="边标签")
    width: float = Field(default=1.0, description="边宽度")

    class Config:
        populate_by_name = True


class GraphResponse(BaseModel):
    """知识图谱响应"""
    nodes: List[GraphNode] = Field(..., description="节点列表")
    edges: List[GraphEdge] = Field(..., description="边列表")
    stats: Dict[str, int] = Field(..., description="统计信息")
