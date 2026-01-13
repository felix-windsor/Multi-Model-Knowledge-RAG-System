"""知识查询 API"""
import os
import time
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.dependencies import get_rag_instance
from app.models.request import QueryRequest
from app.models.response import QueryResponse
from app.services.semantic_cache import get_semantic_cache

router = APIRouter()

# V2.0: Check if streaming is enabled
ENABLE_QUERY_STREAMING = os.getenv("ENABLE_QUERY_STREAMING", "false").lower() == "true"

# V2.0: Get semantic cache instance
semantic_cache = get_semantic_cache()


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

        # V2.0: 尝试从语义缓存获取结果
        if semantic_cache:
            cached_result = await semantic_cache.get(request.question, request.mode)
            if cached_result:
                return QueryResponse(
                    answer=cached_result['answer'],
                    sources=cached_result.get('metadata', {}).get('sources', []),
                    query_time=cached_result['query_time'],
                    cache_hit=True,
                    cache_similarity=cached_result.get('cache_similarity')
                )

        # 执行查询
        answer = await rag.aquery(
            request.question,
            mode=request.mode
        )

        query_time = time.time() - start_time

        # TODO: 从 answer 中提取来源信息
        sources = []

        # V2.0: 将结果存入语义缓存
        if semantic_cache:
            await semantic_cache.set(
                query=request.question,
                mode=request.mode,
                answer=answer,
                query_time=query_time,
                metadata={'sources': sources}
            )

        return QueryResponse(
            answer=answer,
            sources=sources,
            query_time=query_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.post("/stream")
async def query_knowledge_stream(
    request: QueryRequest,
    rag=Depends(get_rag_instance)
):
    """
    执行知识查询（流式响应）- V2.0

    返回 Server-Sent Events (SSE) 格式的流式响应，
    用户可以实时看到生成的内容

    - **question**: 用户问题
    - **mode**: 查询模式 (local, global, hybrid, naive, mix)
    """

    async def generate_sse():
        """生成 SSE 事件流"""
        try:
            start_time = time.time()

            # 发送开始事件
            yield f"data: {json.dumps({'type': 'start', 'timestamp': start_time})}\n\n"

            # 检查 RAG 是否支持流式查询
            if hasattr(rag, 'aquery_stream'):
                # 使用 RAG 的流式 API
                accumulated_text = ""
                async for chunk in rag.aquery_stream(request.question, mode=request.mode):
                    accumulated_text += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

                answer = accumulated_text
            else:
                # 降级：执行普通查询并模拟流式输出
                answer = await rag.aquery(request.question, mode=request.mode)

                # 模拟流式输出（按句子分割）
                import re
                sentences = re.split(r'([。！？\n])', answer)
                accumulated = ""

                for i in range(0, len(sentences), 2):
                    if i < len(sentences):
                        sentence = sentences[i]
                        if i + 1 < len(sentences):
                            sentence += sentences[i + 1]

                        accumulated += sentence
                        yield f"data: {json.dumps({'type': 'chunk', 'content': sentence})}\n\n"

            query_time = time.time() - start_time

            # 发送完成事件
            yield f"data: {json.dumps({'type': 'done', 'query_time': query_time, 'answer': answer})}\n\n"

        except Exception as e:
            # 发送错误事件
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable Nginx buffering
        }
    )
