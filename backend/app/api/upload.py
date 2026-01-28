"""文档上传 API（重构版 - 使用 Service DI，保持向后兼容）"""

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from app.config import Settings
from app.dependencies import (
    get_document_service,
    get_rag_instance,
    get_settings,
    get_task_service,
)
from app.models.response import UploadResponse
from app.services.document_service import DocumentService
from app.services.task_service import TaskService

router = APIRouter()


async def process_document_background(
    rag,
    doc_id,
    task_id,
    file_path: str,
    task_svc: TaskService,
):
    """后台处理文档任务"""
    try:
        # 启动任务
        await task_svc.start_task(task_id)
        await task_svc.update_progress(task_id, 5, "准备 AI 模型")

        # 解析文档
        await task_svc.update_progress(task_id, 15, "正在解析文档")

        # 处理文档
        await rag.process_document_complete(file_path, formula=False)

        # 完成
        await task_svc.update_progress(task_id, 90, "正在构建知识图谱")
        await task_svc.complete_task(task_id)

    except Exception as e:
        await task_svc.fail_task(task_id, str(e))


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    rag=Depends(get_rag_instance),
    settings: Settings = Depends(get_settings),
    doc_svc: DocumentService = Depends(get_document_service),
    task_svc: TaskService = Depends(get_task_service),
):
    """
    上传文档并开始处理

    - **file**: 要上传的文件
    """
    # 验证文件类型
    allowed_extensions = [
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

    file_ext = (
        "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    )
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。支持的格式: {', '.join(allowed_extensions)}",
        )

    try:
        # 保存文件
        file_path, file_size = await DocumentService.save_uploaded_file(
            file, settings.upload_dir
        )

        # 事务创建文档和任务
        document, task, _ = await doc_svc.create_document_with_task(
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type or "application/octet-stream",
        )

        # 后台处理文档
        background_tasks.add_task(
            process_document_background,
            rag,
            document.id,
            task.id,
            file_path,
            task_svc,
        )

        # 返回向后兼容的响应格式
        return UploadResponse(
            success=True,
            doc_id=str(document.id),
            filename=file.filename,
            size=file_size,
            status="processing",
            message="文件上传成功，正在处理中",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")
