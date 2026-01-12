"""文档管理 API"""
from fastapi import APIRouter, HTTPException, Depends
from app.services.document_service import DocumentService
from app.models.response import DocumentStatus, DocumentListResponse
from app.dependencies import get_rag_instance

router = APIRouter()


@router.get("/{doc_id}", response_model=DocumentStatus)
async def get_document_status(doc_id: str, rag=Depends(get_rag_instance)):
    """
    获取文档处理状态

    - **doc_id**: 文档 ID
    """
    # 设置 RAGAnything 实例
    DocumentService.set_rag_instance(rag)
    status = await DocumentService.get_document_status(doc_id)

    if not status:
        raise HTTPException(status_code=404, detail=f"文档不存在: {doc_id}")

    return DocumentStatus(**status)


@router.get("/", response_model=DocumentListResponse)
async def get_all_documents(rag=Depends(get_rag_instance)):
    """
    获取所有文档列表
    """
    # 设置 RAGAnything 实例
    DocumentService.set_rag_instance(rag)
    documents = await DocumentService.get_all_documents()

    # 简化文档信息
    doc_list = [
        {
            "doc_id": doc["doc_id"],
            "filename": doc["filename"],
            "status": doc["status"],
            "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
            "chunks_count": doc.get("chunks_count", 0)
        }
        for doc in documents
    ]

    return DocumentListResponse(
        total=len(doc_list),
        documents=doc_list
    )
