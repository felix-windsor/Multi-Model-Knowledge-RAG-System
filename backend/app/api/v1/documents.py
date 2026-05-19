"""V1 文档管理 API（重构版 - 使用 Service DI）"""

import asyncio
import os
from typing import Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.config import Settings
from app.dependencies import (
    get_document_service,
    get_rag_instance,
    get_settings,
    get_task_service,
    get_webhook_service,
)
from app.middleware.auth import verify_api_key
from app.middleware.response import ErrorCode, wrap_response
from app.models.response import V1DocumentData, V1DocumentListData, V1UploadData
from app.services.document_service import DocumentService
from app.services.extraction_sidecar_service import ExtractionSidecarService
from app.services.task_service import TaskService
from app.services.webhook_service import WebhookService
from app.storage.models import DocumentStatus, TaskStatus

router = APIRouter()

_processing_semaphores: dict[tuple[int, int], asyncio.Semaphore] = {}


def _get_document_processing_semaphore(max_concurrent_tasks: int) -> asyncio.Semaphore:
    limit = max(1, int(max_concurrent_tasks))
    loop_id = id(asyncio.get_running_loop())
    key = (loop_id, limit)
    if key not in _processing_semaphores:
        _processing_semaphores[key] = asyncio.Semaphore(limit)
    return _processing_semaphores[key]


# 允许的文件扩展名
ALLOWED_EXTENSIONS = [
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".txt",
    ".md",
]


async def process_document_with_callback(
    rag,
    doc_id: UUID,
    task_id: UUID,
    file_path: str,
    callback_url: Optional[str],
    task_svc: TaskService,
    webhook_svc: WebhookService,
    extraction_sidecar_enabled: bool = False,
    extraction_sidecar_max_chars: int = 1200,
    max_concurrent_tasks: int = 50,
):
    """
    处理文档并发送回调（后台任务）

    Args:
        rag: RAGAnything 实例
        doc_id: 文档 ID
        task_id: 任务 ID
        file_path: 文件路径
        callback_url: 回调 URL
        task_svc: TaskService 实例
        webhook_svc: WebhookService 实例
        max_concurrent_tasks: 最大后台解析任务并发数
    """
    try:
        semaphore = _get_document_processing_semaphore(max_concurrent_tasks)
        await task_svc.update_progress(task_id, 1, "等待文档处理并发槽位")

        async with semaphore:
            await _process_document_with_callback_locked(
                rag=rag,
                doc_id=doc_id,
                task_id=task_id,
                file_path=file_path,
                callback_url=callback_url,
                task_svc=task_svc,
                webhook_svc=webhook_svc,
                extraction_sidecar_enabled=extraction_sidecar_enabled,
                extraction_sidecar_max_chars=extraction_sidecar_max_chars,
            )

    except Exception as e:
        error_message = str(e)

        # 标记任务失败
        await task_svc.fail_task(task_id, error_message)

        # 发送失败回调
        if callback_url:
            await webhook_svc.deliver_document_event(
                doc_id,
                "document.failed",
                {
                    "status": "failed",
                    "error_message": error_message,
                },
            )


async def _process_document_with_callback_locked(
    rag,
    doc_id: UUID,
    task_id: UUID,
    file_path: str,
    callback_url: Optional[str],
    task_svc: TaskService,
    webhook_svc: WebhookService,
    extraction_sidecar_enabled: bool,
    extraction_sidecar_max_chars: int,
):
    """Run document processing after the concurrency slot has been acquired."""
    try:
        # 启动任务
        await task_svc.start_task(task_id)

        # 更新任务状态
        await task_svc.update_progress(task_id, 5, "准备 AI 模型")

        # 解析文档
        await task_svc.update_progress(task_id, 15, "正在解析文档")

        # 处理文档（主要耗时操作）
        await rag.process_document_complete(file_path, formula=False)

        # 处理多模态内容
        await task_svc.update_progress(task_id, 70, "正在处理多模态内容")

        # 构建知识图谱
        await task_svc.update_progress(task_id, 90, "正在构建知识图谱")

        # 获取处理结果统计
        entities_count = 0
        relations_count = 0

        try:
            if hasattr(rag, "lightrag") and rag.lightrag:
                graph_storage = rag.lightrag.chunk_entity_relation_graph
                if hasattr(graph_storage, "_graph"):
                    entities_count = graph_storage._graph.number_of_nodes()
                    relations_count = graph_storage._graph.number_of_edges()
        except Exception:
            pass

        extraction_sidecar = None
        if extraction_sidecar_enabled:
            await task_svc.update_progress(task_id, 92, "正在生成抽取质量报告")
            try:
                extraction_sidecar = await ExtractionSidecarService(
                    max_chars=extraction_sidecar_max_chars
                ).run_for_document(
                    rag,
                    file_path,
                    parse_kwargs={"formula": False},
                )
            except Exception as sidecar_error:
                extraction_sidecar = {
                    "enabled": True,
                    "status": "failed",
                    "error_message": str(sidecar_error),
                }

        # 完成任务
        result = {
            "entities_count": entities_count,
            "relations_count": relations_count,
        }
        if extraction_sidecar is not None:
            result["extraction_sidecar"] = extraction_sidecar

        await task_svc.complete_task(task_id, result=result)

        # 发送 Webhook 回调
        if callback_url:
            await webhook_svc.deliver_document_event(
                doc_id,
                "document.processed",
                {
                    "status": "completed",
                    "entities_count": entities_count,
                    "relations_count": relations_count,
                },
            )

    except Exception as e:
        error_message = str(e)

        # 标记任务失败
        await task_svc.fail_task(task_id, error_message)

        # 发送失败回调
        if callback_url:
            await webhook_svc.deliver_document_event(
                doc_id,
                "document.failed",
                {
                    "status": "failed",
                    "error_message": error_message,
                },
            )


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    callback_url: Optional[str] = Form(default=None),
    background_tasks: BackgroundTasks = None,
    rag=Depends(get_rag_instance),
    settings: Settings = Depends(get_settings),
    doc_svc: DocumentService = Depends(get_document_service),
    task_svc: TaskService = Depends(get_task_service),
    webhook_svc: WebhookService = Depends(get_webhook_service),
    api_key: str = Depends(verify_api_key),
):
    """
    上传文档（异步处理）

    - **file**: 要上传的文件
    - **callback_url**: 可选的 Webhook 回调 URL
    """
    # Check if RAG instance is available
    if rag is None:
        raise HTTPException(
            status_code=503,
            detail=wrap_response(
                code=ErrorCode.SERVICE_UNAVAILABLE,
                message="RAG service is unavailable. Storage backend is not ready. "
                        "Please ensure Docker services (Qdrant/Neo4j) are running if using database storage. "
                        "Run 'docker compose up -d' to start the services."
            )
        )

    # 验证文件类型
    file_ext = (
        "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    )
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_FILE_TYPE,
                message=f"不支持的文件格式。支持的格式: {', '.join(ALLOWED_EXTENSIONS)}",
            ),
        )

    try:
        # 保存文件
        file_path, file_size = await DocumentService.save_uploaded_file(
            file, settings.upload_dir
        )

        # 事务创建文档、任务、Webhook
        document, task, webhook = await doc_svc.create_document_with_task(
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type or "application/octet-stream",
            callback_url=callback_url,
        )

        # 后台处理文档
        background_tasks.add_task(
            process_document_with_callback,
            rag,
            document.id,
            task.id,
            file_path,
            callback_url,
            task_svc,
            webhook_svc,
            settings.custom_graph_extraction_enabled,
            settings.custom_graph_extraction_max_chars,
            settings.document_processing_max_concurrent_tasks,
        )

        return wrap_response(
            data=V1UploadData(
                doc_id=str(document.id),
                task_id=str(task.id),
                status="processing",
                filename=file.filename,
            ).model_dump(),
            message="Document upload started",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"上传失败: {str(e)}",
            ),
        )


@router.get("")
async def get_documents(
    rag=Depends(get_rag_instance),
    doc_svc: DocumentService = Depends(get_document_service),
    api_key: str = Depends(verify_api_key),
):
    """
    获取文档列表
    """
    # Check if RAG instance is available
    if rag is None:
        raise HTTPException(
            status_code=503,
            detail=wrap_response(
                code=ErrorCode.SERVICE_UNAVAILABLE,
                message="RAG service is unavailable. Storage backend is not ready. "
                        "Please ensure Docker services (Qdrant/Neo4j) are running if using database storage. "
                        "Run 'docker compose up -d' to start the services."
            )
        )

    documents = await doc_svc.list_documents_with_status()

    doc_list = []
    for doc in documents:
        doc_list.append(
            V1DocumentData(
                doc_id=doc["doc_id"],
                filename=doc["filename"],
                status=doc["status"],
                progress=doc.get("progress", 0),
                entities_count=0,
                relations_count=0,
                created_at=(
                    doc["created_at"].isoformat() if doc.get("created_at") else None
                ),
                completed_at=None,
                error_message=None,
            ).model_dump()
        )

    return wrap_response(
        data=V1DocumentListData(total=len(doc_list), documents=doc_list).model_dump()
    )


@router.get("/{doc_id}")
async def get_document(
    doc_id: str,
    rag=Depends(get_rag_instance),
    doc_svc: DocumentService = Depends(get_document_service),
    api_key: str = Depends(verify_api_key),
):
    """
    获取文档详情和处理状态

    - **doc_id**: 文档 ID
    """
    # Check if RAG instance is available
    if rag is None:
        raise HTTPException(
            status_code=503,
            detail=wrap_response(
                code=ErrorCode.SERVICE_UNAVAILABLE,
                message="RAG service is unavailable. Storage backend is not ready. "
                        "Please ensure Docker services (Qdrant/Neo4j) are running if using database storage. "
                        "Run 'docker compose up -d' to start the services."
            )
        )

    try:
        uuid_doc_id = UUID(doc_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_PARAMETER,
                message=f"无效的文档 ID 格式: {doc_id}",
            ),
        )

    status = await doc_svc.get_document_with_status(uuid_doc_id)

    if not status:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.DOCUMENT_NOT_FOUND,
                message=f"文档不存在: {doc_id}",
            ),
        )

    return wrap_response(
        data=V1DocumentData(
            doc_id=status["doc_id"],
            filename=status["filename"],
            status=status["status"],
            progress=status.get("progress", 0),
            entities_count=status.get("chunks_count", 0),
            relations_count=0,
            created_at=(
                status["created_at"].isoformat() if status.get("created_at") else None
            ),
            completed_at=None,
            error_message=status.get("error_message"),
        ).model_dump()
    )


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    rag=Depends(get_rag_instance),
    doc_svc: DocumentService = Depends(get_document_service),
    api_key: str = Depends(verify_api_key),
):
    """
    删除文档

    - **doc_id**: 文档 ID

    注意: 当前仅删除文档记录和文件，知识图谱中的实体关系需要单独清理
    """
    # Check if RAG instance is available
    if rag is None:
        raise HTTPException(
            status_code=503,
            detail=wrap_response(
                code=ErrorCode.SERVICE_UNAVAILABLE,
                message="RAG service is unavailable. Storage backend is not ready. "
                        "Please ensure Docker services (Qdrant/Neo4j) are running if using database storage. "
                        "Run 'docker compose up -d' to start the services."
            )
        )

    try:
        uuid_doc_id = UUID(doc_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_PARAMETER,
                message=f"无效的文档 ID 格式: {doc_id}",
            ),
        )

    # 获取文档信息
    document = await doc_svc.get_document(uuid_doc_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.DOCUMENT_NOT_FOUND,
                message=f"文档不存在: {doc_id}",
            ),
        )

    # 删除文件
    if document.file_path and os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception:
            pass

    # 删除文档记录（级联删除任务和 webhook）
    await doc_svc.delete_document(uuid_doc_id)

    return wrap_response(
        data={"doc_id": doc_id, "deleted": True},
        message="Document deleted successfully",
    )
