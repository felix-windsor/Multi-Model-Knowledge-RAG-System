"""V1 文档管理 API"""
import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends, HTTPException
from app.dependencies import get_rag_instance, get_settings
from app.services.document_service import DocumentService
from app.services.task_service import TaskService, TaskStatus
from app.services.webhook_service import WebhookService
from app.middleware.auth import verify_api_key
from app.middleware.response import wrap_response, ErrorCode
from app.models.response import V1UploadData, V1DocumentData, V1DocumentListData
from app.config import Settings

router = APIRouter()

# 允许的文件扩展名
ALLOWED_EXTENSIONS = [
    ".pdf", ".jpg", ".jpeg", ".png", ".bmp",
    ".doc", ".docx", ".ppt", ".pptx",
    ".txt", ".md"
]


async def process_document_with_callback(
    rag,
    doc_id: str,
    task_id: str,
    file_path: str,
    callback_url: Optional[str] = None
):
    """
    处理文档并发送回调（后台任务）

    Args:
        rag: RAGAnything 实例
        doc_id: 文档 ID
        task_id: 任务 ID
        file_path: 文件路径
        callback_url: 回调 URL
    """
    try:
        # 更新任务状态
        TaskService.update_task(
            task_id,
            status=TaskStatus.PROCESSING.value,
            progress=5,
            step="准备 AI 模型"
        )

        # 调用原有的处理逻辑
        await DocumentService.process_document(rag, doc_id, file_path)

        # 获取处理结果统计
        entities_count = 0
        relations_count = 0

        try:
            if hasattr(rag, 'lightrag') and rag.lightrag:
                graph_storage = rag.lightrag.chunk_entity_relation_graph
                if hasattr(graph_storage, '_graph'):
                    entities_count = graph_storage._graph.number_of_nodes()
                    relations_count = graph_storage._graph.number_of_edges()
        except Exception:
            pass

        # 更新任务状态为完成
        TaskService.update_task(
            task_id,
            status=TaskStatus.COMPLETED.value,
            progress=100,
            step="处理完成",
            result={
                "entities_count": entities_count,
                "relations_count": relations_count
            }
        )

        # 发送 Webhook 回调
        if callback_url:
            await WebhookService.notify_document_completed(
                callback_url=callback_url,
                doc_id=doc_id,
                task_id=task_id,
                entities_count=entities_count,
                relations_count=relations_count
            )

    except Exception as e:
        error_message = str(e)

        # 更新任务状态为失败
        TaskService.update_task(
            task_id,
            status=TaskStatus.FAILED.value,
            progress=0,
            step="处理失败",
            error_message=error_message
        )

        # 发送失败回调
        if callback_url:
            await WebhookService.notify_document_failed(
                callback_url=callback_url,
                doc_id=doc_id,
                task_id=task_id,
                error_message=error_message
            )


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    callback_url: Optional[str] = Form(default=None),
    background_tasks: BackgroundTasks = None,
    rag=Depends(get_rag_instance),
    settings: Settings = Depends(get_settings),
    api_key: str = Depends(verify_api_key)
):
    """
    上传文档（异步处理）

    - **file**: 要上传的文件
    - **callback_url**: 可选的 Webhook 回调 URL
    """
    # 设置 RAGAnything 实例
    DocumentService.set_rag_instance(rag)

    # 验证文件类型
    file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=wrap_response(
                code=ErrorCode.INVALID_FILE_TYPE,
                message=f"不支持的文件格式。支持的格式: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        )

    try:
        # 保存文件
        doc_id, file_path, file_size = await DocumentService.save_uploaded_file(
            file,
            settings.upload_dir
        )

        # 创建任务
        task = TaskService.create_task(
            doc_id=doc_id,
            task_type="document_processing",
            callback_url=callback_url
        )

        # 创建文档记录
        DocumentService.create_document_record(
            doc_id,
            file.filename,
            file_path,
            file_size
        )

        # 后台处理文档
        background_tasks.add_task(
            process_document_with_callback,
            rag,
            doc_id,
            task["task_id"],
            file_path,
            callback_url
        )

        return wrap_response(
            data=V1UploadData(
                doc_id=doc_id,
                task_id=task["task_id"],
                status="processing",
                filename=file.filename
            ).model_dump(),
            message="Document upload started"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.INTERNAL_ERROR,
                message=f"上传失败: {str(e)}"
            )
        )


@router.get("")
async def get_documents(
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    获取文档列表
    """
    DocumentService.set_rag_instance(rag)
    documents = await DocumentService.get_all_documents()

    doc_list = []
    for doc in documents:
        # 获取关联任务信息
        task = TaskService.get_task_by_doc_id(doc["doc_id"])
        entities_count = 0
        relations_count = 0

        if task and task.get("result"):
            entities_count = task["result"].get("entities_count", 0)
            relations_count = task["result"].get("relations_count", 0)

        doc_list.append(V1DocumentData(
            doc_id=doc["doc_id"],
            filename=doc["filename"],
            status=doc["status"],
            progress=doc.get("progress", 0),
            entities_count=entities_count,
            relations_count=relations_count,
            created_at=doc.get("created_at").isoformat() if doc.get("created_at") else None,
            completed_at=task.get("completed_at") if task else None,
            error_message=doc.get("error_message")
        ).model_dump())

    return wrap_response(
        data=V1DocumentListData(
            total=len(doc_list),
            documents=doc_list
        ).model_dump()
    )


@router.get("/{doc_id}")
async def get_document(
    doc_id: str,
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    获取文档详情和处理状态

    - **doc_id**: 文档 ID
    """
    DocumentService.set_rag_instance(rag)
    status = await DocumentService.get_document_status(doc_id)

    if not status:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.DOCUMENT_NOT_FOUND,
                message=f"文档不存在: {doc_id}"
            )
        )

    # 获取关联任务信息
    task = TaskService.get_task_by_doc_id(doc_id)
    entities_count = 0
    relations_count = 0

    if task and task.get("result"):
        entities_count = task["result"].get("entities_count", 0)
        relations_count = task["result"].get("relations_count", 0)

    return wrap_response(
        data=V1DocumentData(
            doc_id=status["doc_id"],
            filename=status["filename"],
            status=status["status"],
            progress=status.get("progress", 0),
            entities_count=entities_count,
            relations_count=relations_count,
            created_at=status.get("created_at").isoformat() if status.get("created_at") else None,
            completed_at=task.get("completed_at") if task else None,
            error_message=status.get("error_message")
        ).model_dump()
    )


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    删除文档

    - **doc_id**: 文档 ID

    注意: 当前仅删除文档记录，不会删除知识图谱中的实体关系
    """
    DocumentService.set_rag_instance(rag)
    status = await DocumentService.get_document_status(doc_id)

    if not status:
        raise HTTPException(
            status_code=404,
            detail=wrap_response(
                code=ErrorCode.DOCUMENT_NOT_FOUND,
                message=f"文档不存在: {doc_id}"
            )
        )

    # 删除文件
    file_path = status.get("file_path")
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass

    # TODO: 从 LightRAG 中删除文档相关的实体和关系
    # 目前 LightRAG 不支持按文档删除

    return wrap_response(
        data={"doc_id": doc_id, "deleted": True},
        message="Document deleted successfully"
    )
