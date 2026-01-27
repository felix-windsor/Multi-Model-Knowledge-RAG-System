"""V1 智能问答 API"""
import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.dependencies import get_rag_instance
from app.middleware.auth import verify_api_key
from app.middleware.response import wrap_response, ErrorCode
from app.models.request import V1QueryRequest
from app.models.response import V1QueryData, V1QueryUsage

router = APIRouter()

# 有效的查询模式
VALID_MODES = ["mix", "local", "global", "hybrid", "naive"]


@router.post("")
async def query_knowledge(
    request: V1QueryRequest,
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    知识库问答

    - **question**: 问题内容
    - **mode**: 查询模式 (mix, local, global, hybrid, naive)
    - **doc_ids**: 限定查询的文档 ID（暂未实现）
    - **top_k**: 返回结果数量

    注意: 当前版本不支持来源追踪 (sources)、实体提取 (entities) 和 Token 统计 (usage)，
    这些字段返回空值作为预留接口。
    """
    if request.mode not in VALID_MODES:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_QUERY_MODE,
                message=f"无效的查询模式。有效模式: {', '.join(VALID_MODES)}"
            )
        )

    try:
        answer = await rag.aquery(
            request.question,
            mode=request.mode
        )

        return wrap_response(
            data=V1QueryData(
                answer=answer,
                sources=[],
                entities=[],
                usage=V1QueryUsage()
            ).model_dump()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.RAG_ERROR,
                message=f"查询失败: {str(e)}"
            )
        )


@router.post("/stream")
async def query_knowledge_stream(
    request: V1QueryRequest,
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    流式问答（SSE）

    使用 Server-Sent Events 返回流式响应

    - **question**: 问题内容
    - **mode**: 查询模式 (mix, local, global, hybrid, naive)
    - **doc_ids**: 限定查询的文档 ID（暂未实现）
    - **top_k**: 返回结果数量
    """
    # 验证查询模式
    if request.mode not in VALID_MODES:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_QUERY_MODE,
                message=f"无效的查询模式。有效模式: {', '.join(VALID_MODES)}"
            )
        )

    async def generate_stream() -> AsyncGenerator[str, None]:
        """生成 SSE 流"""
        try:
            # 检查 RAG 是否支持流式查询
            if hasattr(rag, 'aquery_stream'):
                # 使用流式查询
                async for chunk in rag.aquery_stream(
                    request.question,
                    mode=request.mode
                ):
                    yield f"data: {chunk}\n\n"
            else:
                # 如果不支持流式，使用普通查询并分块返回
                answer = await rag.aquery(
                    request.question,
                    mode=request.mode
                )

                # 将答案分块发送
                chunk_size = 50
                for i in range(0, len(answer), chunk_size):
                    chunk = answer[i:i + chunk_size]
                    yield f"data: {chunk}\n\n"
                    await asyncio.sleep(0.01)  # 小延迟以模拟流式效果

            # 发送结束标记
            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
