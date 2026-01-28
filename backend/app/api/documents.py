"""文档管理 API（重构版 - 使用 Service DI，保持向后兼容）"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_document_service
from app.models.response import DocumentListResponse, DocumentStatus
from app.services.document_service import DocumentService

router = APIRouter()


@router.get("/{doc_id}", response_model=DocumentStatus)
async def get_document_status(
    doc_id: str,
    doc_svc: DocumentService = Depends(get_document_service),
):
    """
    获取文档处理状态

    - **doc_id**: 文档 ID
    """
    try:
        uuid_doc_id = UUID(doc_id)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的文档 ID 格式: {doc_id}")

    status = await doc_svc.get_document_with_status(uuid_doc_id)

    if not status:
        raise HTTPException(status_code=404, detail=f"文档不存在: {doc_id}")

    # 返回向后兼容的响应格式
    return DocumentStatus(
        doc_id=status["doc_id"],
        filename=status["filename"],
        status=status["status"],
        progress=status.get("progress", 0),
        step=status.get("step", "等待处理"),
        chunks_count=status.get("chunks_count", 0),
        error_message=status.get("error_message"),
        created_at=status["created_at"] if status.get("created_at") else None,
        updated_at=status["updated_at"] if status.get("updated_at") else None,
    )


@router.get("/", response_model=DocumentListResponse)
async def get_all_documents(
    doc_svc: DocumentService = Depends(get_document_service),
):
    """
    获取所有文档列表
    """
    documents = await doc_svc.list_documents_with_status()

    # 转换为向后兼容的响应格式
    doc_list = [
        {
            "doc_id": doc["doc_id"],
            "filename": doc["filename"],
            "status": doc["status"],
            "created_at": (
                doc["created_at"].isoformat() if doc.get("created_at") else None
            ),
            "chunks_count": 0,
        }
        for doc in documents
    ]

    return DocumentListResponse(total=len(doc_list), documents=doc_list)
