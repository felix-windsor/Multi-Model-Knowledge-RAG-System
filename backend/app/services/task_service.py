"""任务管理服务（重构版 - 使用 StorageManager）"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from app.storage.base import StorageManager
from app.storage.models import Task, TaskStatus


class TaskService:
    """任务管理服务

    This service provides task management operations using the storage
    abstraction layer. It supports task lifecycle management including
    creation, progress tracking, completion, and cancellation.
    """

    def __init__(self, storage: StorageManager) -> None:
        """Initialize task service with storage manager.

        Args:
            storage: StorageManager instance for data persistence.
        """
        self.storage = storage

    async def create_task(
        self,
        document_id: UUID,
        task_type: str = "document_processing",
    ) -> Task:
        """创建新任务

        Args:
            document_id: ID of the document this task processes.
            task_type: Type of task (e.g., "document_processing").

        Returns:
            The created Task.
        """
        return await self.storage.tasks.create(
            document_id=document_id,
            task_type=task_type,
        )

    async def get_task(self, task_id: UUID) -> Optional[Task]:
        """获取任务信息

        Args:
            task_id: Task ID.

        Returns:
            The Task if found, None otherwise.
        """
        return await self.storage.tasks.get(task_id)

    async def get_tasks_by_document(self, document_id: UUID) -> List[Task]:
        """获取文档的所有任务

        Args:
            document_id: Document ID.

        Returns:
            List of Task objects for the document.
        """
        return await self.storage.tasks.get_by_document(document_id)

    async def start_task(self, task_id: UUID) -> bool:
        """启动任务

        Args:
            task_id: Task ID.

        Returns:
            True if successful, False if task not found.
        """
        return await self.storage.tasks.start(task_id)

    async def update_progress(
        self,
        task_id: UUID,
        progress: int,
        step: Optional[str] = None,
    ) -> bool:
        """更新任务进度

        Args:
            task_id: Task ID.
            progress: Progress percentage (0-100).
            step: Optional description of current processing step.

        Returns:
            True if successful, False if task not found.
        """
        return await self.storage.tasks.update_progress(
            task_id,
            progress,
            step,
        )

    async def complete_task(
        self,
        task_id: UUID,
        result: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """完成任务

        Args:
            task_id: Task ID.
            result: Optional result data from the task.

        Returns:
            True if successful, False if task not found.
        """
        return await self.storage.tasks.complete(task_id, result)

    async def fail_task(
        self,
        task_id: UUID,
        error: str,
    ) -> bool:
        """标记任务失败

        Args:
            task_id: Task ID.
            error: Error message describing the failure.

        Returns:
            True if successful, False if task not found.
        """
        return await self.storage.tasks.fail(task_id, error)

    async def cancel_task(self, task_id: UUID) -> bool:
        """取消任务

        Args:
            task_id: Task ID.

        Returns:
            True if successful, False if task not found or cannot be cancelled.
        """
        return await self.storage.tasks.cancel(task_id)

    async def list_pending_tasks(self, limit: int = 10) -> List[Task]:
        """获取待处理任务列表

        Args:
            limit: Maximum number of tasks to return.

        Returns:
            List of pending Task objects.
        """
        return await self.storage.tasks.list_pending(limit)
