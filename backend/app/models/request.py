"""请求数据模型"""
from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================
# V1 API 请求模型
# ============================================

class V1QueryRequest(BaseModel):
    """V1 查询请求"""
    question: str = Field(..., description="问题内容", min_length=1)
    mode: str = Field(default="mix", description="查询模式: mix(默认), local, global, hybrid, naive")
    doc_ids: Optional[List[str]] = Field(default=None, description="限定查询的文档ID，空则查询全部")
    top_k: int = Field(default=5, description="返回结果数量", ge=1, le=20)

    class Config:
        json_schema_extra = {
            "example": {
                "question": "什么是知识图谱？",
                "mode": "mix",
                "doc_ids": ["doc_abc123"],
                "top_k": 5
            }
        }


class V1SubgraphRequest(BaseModel):
    """V1 子图查询请求参数"""
    entity: Optional[str] = Field(default=None, description="中心实体名称")
    depth: int = Field(default=2, description="查询深度", ge=1, le=5)
    doc_ids: Optional[List[str]] = Field(default=None, description="限定文档 ID")
    limit: int = Field(default=100, description="最大节点数", ge=1, le=1000)


# ============================================
# 旧版请求模型（保持向后兼容）
# ============================================

class QueryRequest(BaseModel):
    """查询请求"""
    question: str = Field(..., description="用户问题", min_length=1)
    mode: str = Field(default="mix", description="查询模式: local, global, hybrid, naive, mix")
    doc_ids: Optional[List[str]] = Field(default=None, description="指定文档 ID 列表")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "什么是机器学习？",
                "mode": "mix",
                "doc_ids": ["doc-abc123"]
            }
        }
