"""响应数据模型"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


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
