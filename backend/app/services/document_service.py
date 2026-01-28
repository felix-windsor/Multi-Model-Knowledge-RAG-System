"""文档处理服务（重构版 - 使用 StorageManager）"""

import asyncio
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import UploadFile

from app.exceptions import ServiceError
from app.storage.base import StorageManager
from app.storage.models import Document, DocumentStatus, Task


class DocumentService:
    """文档处理服务

    This service provides document management operations using the storage
    abstraction layer. It supports transactional creation of documents with
    associated tasks and webhooks.
    """

    def __init__(self, storage: StorageManager) -> None:
        """Initialize document service with storage manager.

        Args:
            storage: StorageManager instance for data persistence.
        """
        self.storage = storage

    @staticmethod
    async def save_uploaded_file(
        file: UploadFile,
        upload_dir: str,
    ) -> tuple[str, int]:
        """保存上传的文件到磁盘

        Args:
            file: The uploaded file.
            upload_dir: Directory to save the file.

        Returns:
            Tuple of (file_path, file_size).
        """
        # 确保上传目录存在
        Path(upload_dir).mkdir(parents=True, exist_ok=True)

        # 生成唯一文件名
        file_id = uuid.uuid4().hex[:12]
        file_path = os.path.join(upload_dir, f"doc-{file_id}_{file.filename}")

        # 保存文件
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return file_path, len(content)

    async def create_document(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str,
    ) -> Document:
        """创建文档记录

        Args:
            filename: Original filename.
            file_path: Path where file is stored.
            file_size: Size of the file in bytes.
            mime_type: MIME type of the file.

        Returns:
            The created Document.
        """
        return await self.storage.documents.create(
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
        )

    async def create_document_with_task(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str,
        callback_url: Optional[str] = None,
    ) -> tuple[Document, Task, Optional[Any]]:
        """事务创建文档、任务、Webhook

        Creates a document, associated processing task, and optional webhook
        in a single transaction. If any step fails, all changes are rolled back.

        Args:
            filename: Original filename.
            file_path: Path where file is stored.
            file_size: Size of the file in bytes.
            mime_type: MIME type of the file.
            callback_url: Optional webhook callback URL.

        Returns:
            Tuple of (Document, Task, Webhook or None).

        Raises:
            ServiceError: If transaction fails.
        """
        try:
            await self.storage.begin_transaction()

            # 创建文档
            document = await self.storage.documents.create(
                filename=filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=mime_type,
            )

            # 创建任务
            task = await self.storage.tasks.create(
                document_id=document.id,
                task_type="document_processing",
            )

            # 创建 webhook（如果需要）
            webhook = None
            if callback_url:
                webhook = await self.storage.webhooks.create(
                    document_id=document.id,
                    callback_url=callback_url,
                    event_type="document.processed",
                )

            await self.storage.commit()
            return document, task, webhook

        except Exception as e:
            await self.storage.rollback()
            raise ServiceError(f"Failed to create document: {e}") from e

    async def get_document(self, doc_id: UUID) -> Optional[Document]:
        """获取文档记录

        Args:
            doc_id: Document ID.

        Returns:
            The Document if found, None otherwise.
        """
        return await self.storage.documents.get(doc_id)

    async def get_document_with_status(
        self,
        doc_id: UUID,
    ) -> Optional[Dict[str, Any]]:
        """获取文档及其处理状态（聚合 Document + Task + Webhook）

        Retrieves document information along with its latest task status
        and webhook configuration.

        Args:
            doc_id: Document ID.

        Returns:
            Dictionary with aggregated document status, or None if not found.
        """
        # 并发获取数据
        document, tasks, webhooks = await asyncio.gather(
            self.storage.documents.get(doc_id),
            self.storage.tasks.get_by_document(doc_id),
            self.storage.webhooks.get_by_document(doc_id),
        )

        if not document:
            return None

        # 获取最新任务
        latest_task = tasks[0] if tasks else None

        # 获取 webhook
        webhook = webhooks[0] if webhooks else None

        # 组合数据
        return {
            "doc_id": str(document.id),
            "filename": document.filename,
            "file_path": document.file_path,
            "file_size": document.file_size,
            "mime_type": document.mime_type,
            "status": (
                latest_task.status.value if latest_task else document.status.value
            ),
            "progress": latest_task.progress if latest_task else 0,
            "step": latest_task.step if latest_task else "等待处理",
            "chunks_count": (
                latest_task.result.get("chunks_count", 0)
                if latest_task and latest_task.result
                else 0
            ),
            "callback_url": webhook.callback_url if webhook else None,
            "error_message": document.error_message
            or (latest_task.last_error if latest_task else None),
            "created_at": document.created_at,
            "updated_at": document.updated_at,
        }

    async def list_documents_with_status(
        self,
        status: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """批量获取文档状态

        Retrieves multiple documents with their task status using batch
        queries to avoid N+1 performance issues.

        Args:
            status: Optional status filter.
            limit: Maximum number of documents to return.

        Returns:
            List of document status dictionaries.
        """
        # 获取所有文档
        documents = await self.storage.documents.list(
            status=status,
            limit=limit,
        )

        if not documents:
            return []

        # 批量获取所有文档的任务（一次查询）
        doc_ids = [doc.id for doc in documents]
        all_tasks = await self.storage.tasks.get_by_documents_batch(doc_ids)

        # 按 document_id 分组
        tasks_by_doc: Dict[UUID, List[Task]] = {}
        for task in all_tasks:
            if task.document_id not in tasks_by_doc:
                tasks_by_doc[task.document_id] = []
            tasks_by_doc[task.document_id].append(task)

        # 组合数据
        results = []
        for doc in documents:
            tasks = tasks_by_doc.get(doc.id, [])
            latest_task = (
                max(tasks, key=lambda t: t.created_at) if tasks else None
            )

            results.append({
                "doc_id": str(doc.id),
                "filename": doc.filename,
                "file_path": doc.file_path,
                "file_size": doc.file_size,
                "status": (
                    latest_task.status.value if latest_task else doc.status.value
                ),
                "progress": latest_task.progress if latest_task else 0,
                "step": latest_task.step if latest_task else "等待处理",
                "created_at": doc.created_at,
                "updated_at": doc.updated_at,
            })

        return results

    async def update_status(
        self,
        doc_id: UUID,
        status: DocumentStatus,
        error_message: Optional[str] = None,
    ) -> bool:
        """更新文档状态

        Args:
            doc_id: Document ID.
            status: New status.
            error_message: Optional error message.

        Returns:
            True if update was successful.
        """
        return await self.storage.documents.update_status(
            doc_id,
            status.value,
            error_message,
        )

    async def delete_document(self, doc_id: UUID) -> bool:
        """删除文档（级联删除任务和 webhook）

        Deletes the document and all associated tasks and webhooks
        in a transactional manner.

        Args:
            doc_id: Document ID.

        Returns:
            True if deletion was successful.
        """
        try:
            await self.storage.begin_transaction()

            # Delete associated tasks first
            await self.storage.tasks.delete_by_document(doc_id)

            # Delete associated webhooks
            await self.storage.webhooks.delete_by_document(doc_id)

            # Delete the document
            result = await self.storage.documents.delete(doc_id)

            await self.storage.commit()
            return result

        except Exception as e:
            await self.storage.rollback()
            raise ServiceError(f"Failed to delete document: {e}") from e
