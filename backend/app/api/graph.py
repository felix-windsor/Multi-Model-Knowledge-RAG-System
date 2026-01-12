"""知识图谱导出 API"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.dependencies import get_rag_instance
from app.services.graph_service import GraphService
from app.models.response import GraphResponse

router = APIRouter()


@router.get("/", response_model=GraphResponse)
async def get_knowledge_graph(
    doc_id: Optional[str] = Query(None, description="可选的文档 ID 过滤"),
    limit: int = Query(1000, description="返回的最大节点数", ge=1, le=5000),
    rag=Depends(get_rag_instance)
):
    """
    导出知识图谱

    - **doc_id**: 可选的文档 ID,用于过滤特定文档的图谱
    - **limit**: 返回的最大节点数量 (1-5000)
    """
    graph_service = GraphService(rag)
    graph_data = await graph_service.export_graph(doc_id, limit)

    return GraphResponse(**graph_data)
