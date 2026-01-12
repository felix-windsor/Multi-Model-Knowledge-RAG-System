"""请求数据模型"""
from pydantic import BaseModel, Field
from typing import Optional, List


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
