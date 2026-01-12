"""知识查询 API"""
import time
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_rag_instance
from app.models.request import QueryRequest
from app.models.response import QueryResponse

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_knowledge(
    request: QueryRequest,
    rag=Depends(get_rag_instance)
):
    """
    执行知识查询

    - **question**: 用户问题
    - **mode**: 查询模式 (local, global, hybrid, naive, mix)
    - **doc_ids**: 可选的文档 ID 列表（暂未实现过滤）
    """
    try:
        start_time = time.time()

        # 执行查询
        answer = await rag.aquery(
            request.question,
            mode=request.mode
        )

        query_time = time.time() - start_time

        # TODO: 从 answer 中提取来源信息
        sources = []

        return QueryResponse(
            answer=answer,
            sources=sources,
            query_time=query_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
