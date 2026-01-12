"""文档处理服务"""
import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import UploadFile


# 简单的内存存储（用于临时存储上传中的文档）
_document_store: Dict[str, Dict[str, Any]] = {}

# RAGAnything 实例引用（用于访问持久化存储）
_rag_instance = None


class DocumentService:
    """文档处理服务"""

    @staticmethod
    def set_rag_instance(rag):
        """设置 RAGAnything 实例"""
        global _rag_instance
        _rag_instance = rag

    @staticmethod
    def generate_doc_id() -> str:
        """生成文档 ID"""
        return f"doc-{uuid.uuid4().hex[:12]}"

    @staticmethod
    async def save_uploaded_file(file: UploadFile, upload_dir: str) -> tuple[str, str, int]:
        """
        保存上传的文件

        Returns:
            (doc_id, file_path, file_size)
        """
        # 生成 doc_id
        doc_id = DocumentService.generate_doc_id()

        # 确保上传目录存在
        Path(upload_dir).mkdir(parents=True, exist_ok=True)

        # 保存文件
        file_path = os.path.join(upload_dir, f"{doc_id}_{file.filename}")
        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        return doc_id, file_path, len(content)

    @staticmethod
    def create_document_record(
        doc_id: str,
        filename: str,
        file_path: str,
        file_size: int
    ):
        """创建文档记录"""
        _document_store[doc_id] = {
            "doc_id": doc_id,
            "filename": filename,
            "file_path": file_path,
            "file_size": file_size,
            "status": "processing",
            "progress": 0,
            "step": "开始处理文档",
            "chunks_count": 0,
            "error_message": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

    @staticmethod
    def update_status(
        doc_id: str,
        status: str,
        progress: int = None,
        step: str = None,
        chunks_count: int = None,
        error: str = None
    ):
        """更新文档状态"""
        if doc_id not in _document_store:
            return

        doc = _document_store[doc_id]
        doc["status"] = status
        doc["updated_at"] = datetime.now()

        if progress is not None:
            doc["progress"] = progress
        if step is not None:
            doc["step"] = step
        if chunks_count is not None:
            doc["chunks_count"] = chunks_count
        if error is not None:
            doc["error_message"] = error

    @staticmethod
    async def get_document_status(doc_id: str) -> Optional[Dict[str, Any]]:
        """获取文档状态（优先从 LightRAG 存储读取）"""
        # 先检查内存存储（用于正在处理的文档）
        if doc_id in _document_store:
            return _document_store[doc_id]

        # 从 LightRAG 持久化存储读取
        if _rag_instance and hasattr(_rag_instance, 'lightrag'):
            try:
                doc_status = await _rag_instance.lightrag.doc_status.get_by_id(doc_id)
                if doc_status:
                    # 转换为前端需要的格式
                    return {
                        "doc_id": doc_id,
                        "filename": doc_status.get("file_path", "").split("_", 1)[-1] if doc_status.get("file_path") else "unknown",
                        "file_path": doc_status.get("file_path", ""),
                        "status": "completed" if doc_status.get("status") == "PROCESSED" else "processing",
                        "progress": 100 if doc_status.get("status") == "PROCESSED" else 50,
                        "step": "文档已处理完成",
                        "chunks_count": doc_status.get("chunks_count", 0),
                        "created_at": datetime.fromtimestamp(doc_status.get("create_time", 0)) if doc_status.get("create_time") else datetime.now(),
                        "updated_at": datetime.now()
                    }
            except Exception as e:
                print(f"Error reading from LightRAG storage: {e}")

        return None

    @staticmethod
    async def get_all_documents() -> List[Dict[str, Any]]:
        """获取所有文档（从 LightRAG 存储和内存存储）"""
        all_docs = []

        # 1. 从 LightRAG 持久化存储读取
        if _rag_instance and hasattr(_rag_instance, 'lightrag'):
            try:
                # 确保 LightRAG 已初始化
                if _rag_instance.lightrag is None:
                    await _rag_instance._ensure_lightrag_initialized()

                doc_status_storage = _rag_instance.lightrag.doc_status

                # 使用 get_docs_paginated 方法获取所有文档
                # 返回值是 tuple[list[tuple[str, dict]], int]
                docs_list, total_count = await doc_status_storage.get_docs_paginated(
                    status_filter=None,  # 获取所有状态的文档
                    page=1,
                    page_size=10000,  # 足够大以获取所有文档
                    sort_field="created_at",
                    sort_direction="desc"
                )

                print(f"Found {total_count} documents in storage")

                # doc_data 是 DocProcessingStatus 对象，需要使用属性访问
                from lightrag.base import DocStatus
                from dateutil import parser as date_parser

                for doc_id, doc_data in docs_list:
                    # 提取文件名（从 file_path）
                    file_path = doc_data.file_path
                    filename = Path(file_path).name if file_path else "unknown"
                    # 如果文件名包含 doc_id 前缀，移除它
                    if "_" in filename:
                        filename = filename.split("_", 1)[-1]

                    # 状态处理：doc_data.status 是 DocStatus 枚举
                    is_completed = doc_data.status == DocStatus.PROCESSED

                    # 解析创建时间
                    created_at = doc_data.created_at
                    if created_at:
                        # 如果是字符串格式的 ISO 时间
                        if isinstance(created_at, str):
                            try:
                                created_at = date_parser.parse(created_at)
                            except:
                                created_at = datetime.now()
                        else:
                            created_at = datetime.now()
                    else:
                        created_at = datetime.now()

                    all_docs.append({
                        "doc_id": doc_id,
                        "filename": filename,
                        "file_path": file_path,
                        "status": "completed" if is_completed else "processing",
                        "progress": 100 if is_completed else 50,
                        "chunks_count": doc_data.chunks_count or 0,
                        "created_at": created_at
                    })

            except Exception as e:
                print(f"Error reading documents from LightRAG storage: {e}")
                import traceback
                traceback.print_exc()

        # 2. 添加内存中正在处理的文档
        for doc_id, doc_data in _document_store.items():
            # 避免重复
            if not any(d["doc_id"] == doc_id for d in all_docs):
                all_docs.append(doc_data)

        # 按创建时间倒序排序
        all_docs.sort(key=lambda x: x.get("created_at", datetime.min), reverse=True)

        return all_docs

    @staticmethod
    async def process_document(rag, doc_id: str, file_path: str):
        """
        处理文档（后台任务）

        Args:
            rag: RAGAnything 实例
            doc_id: 文档 ID
            file_path: 文件路径
        """
        try:
            # 步骤 1: 下载模型（首次使用）
            DocumentService.update_status(
                doc_id,
                "processing",
                5,
                "准备 AI 模型（首次使用需下载）..."
            )

            # 步骤 2: 解析文档
            DocumentService.update_status(
                doc_id,
                "processing",
                15,
                "正在解析 PDF 文档（提取文本、图片、表格、公式）..."
            )

            # 步骤 3: 处理文本内容
            DocumentService.update_status(
                doc_id,
                "processing",
                40,
                "正在处理文本内容..."
            )

            # 处理文档（这是主要耗时操作）
            await rag.process_document_complete(file_path)

            # 步骤 4: 处理多模态内容
            DocumentService.update_status(
                doc_id,
                "processing",
                70,
                "正在处理多模态内容（图片、表格、公式）..."
            )

            # 步骤 5: 构建知识图谱
            DocumentService.update_status(
                doc_id,
                "processing",
                90,
                "正在构建知识图谱和实体关系..."
            )

            # 获取处理后的 chunks 数量
            try:
                # 从 RAGAnything 获取文档状态
                doc_status = await rag.lightrag.doc_status.get_by_id(doc_id)
                chunks_count = doc_status.get("chunks_count", 0) if doc_status else 0
            except:
                # 如果获取失败，使用默认值
                chunks_count = 0

            # 完成
            DocumentService.update_status(
                doc_id,
                "completed",
                100,
                "文档处理完成",
                chunks_count=chunks_count
            )

        except Exception as e:
            # 更新状态：failed
            DocumentService.update_status(
                doc_id,
                "failed",
                0,
                "处理失败",
                error=str(e)
            )
            raise
