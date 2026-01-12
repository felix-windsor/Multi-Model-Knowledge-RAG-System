"""文档上传 API"""
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from app.dependencies import get_rag_instance, get_settings
from app.services.document_service import DocumentService
from app.models.response import UploadResponse
from app.config import Settings

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    rag=Depends(get_rag_instance),
    settings: Settings = Depends(get_settings)
):
    """
    上传文档并开始处理

    - **file**: 要上传的文件
    """
    # 设置 RAGAnything 实例（用于访问持久化存储）
    DocumentService.set_rag_instance(rag)
    # 验证文件类型
    allowed_extensions = [
        ".pdf", ".jpg", ".jpeg", ".png", ".bmp",
        ".doc", ".docx", ".ppt", ".pptx",
        ".txt", ".md"
    ]

    file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。支持的格式: {', '.join(allowed_extensions)}"
        )

    try:
        # 保存文件
        doc_id, file_path, file_size = await DocumentService.save_uploaded_file(
            file,
            settings.upload_dir
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
            DocumentService.process_document,
            rag,
            doc_id,
            file_path
        )

        return UploadResponse(
            success=True,
            doc_id=doc_id,
            filename=file.filename,
            size=file_size,
            status="processing",
            message="文件上传成功，正在处理中"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")
