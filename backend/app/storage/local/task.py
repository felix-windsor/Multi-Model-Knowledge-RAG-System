"""Local file-based task storage implementation."""

import copy
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..base import TaskStorage
from ..models import Task, TaskStatus


class LocalTaskStorage(TaskStorage):
    """Local JSON file-based task storage.

    This implementation stores task metadata in a JSON file,
    suitable for development and single-instance deployments.
    For production with multiple instances, use the database backend.
    """

    def __init__(self, storage_dir: str = "data/storage") -> None:
        """Initialize local task storage.

        Args:
            storage_dir: Directory path for storing the JSON data file.
        """
        self.storage_dir = Path(storage_dir)
        self.tasks_file = self.storage_dir / "tasks.json"
        self._tx_snapshot: Optional[Dict[str, dict]] = None
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Ensure storage directory and file exist."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.tasks_file.exists():
            self._save_tasks({})

    def _load_tasks(self) -> dict:
        """Load tasks from JSON file.

        Returns:
            Dictionary of task data keyed by task ID.
        """
        try:
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_tasks(self, tasks: dict) -> None:
        """Save tasks to JSON file.

        Args:
            tasks: Dictionary of task data to persist.
        """
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, default=str)

    def _task_from_dict(self, data: dict) -> Task:
        """Convert dictionary data to Task model.

        Args:
            data: Dictionary containing task data.

        Returns:
            Task model instance.
        """
        return Task(
            id=UUID(data["id"]),
            document_id=UUID(data["document_id"]),
            task_type=data["task_type"],
            status=TaskStatus(data["status"]),
            progress=data.get("progress", 0),
            step=data.get("step"),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            last_error=data.get("last_error"),
            result=data.get("result"),
            created_at=datetime.fromisoformat(data["created_at"]),
            started_at=(
                datetime.fromisoformat(data["started_at"])
                if data.get("started_at")
                else None
            ),
            completed_at=(
                datetime.fromisoformat(data["completed_at"])
                if data.get("completed_at")
                else None
            ),
        )

    async def create(self, document_id: UUID, task_type: str) -> Task:
        """Create a new task for document processing.

        Args:
            document_id: ID of the document this task processes.
            task_type: Type of task (e.g., "document_processing").

        Returns:
            The created Task with generated ID and timestamps.
        """
        tasks = self._load_tasks()

        task_id = uuid.uuid4()
        now = datetime.now()

        task_data = {
            "id": str(task_id),
            "document_id": str(document_id),
            "task_type": task_type,
            "status": TaskStatus.PENDING.value,
            "progress": 0,
            "step": None,
            "retry_count": 0,
            "max_retries": 3,
            "last_error": None,
            "result": None,
            "created_at": now.isoformat(),
            "started_at": None,
            "completed_at": None,
        }

        tasks[str(task_id)] = task_data
        self._save_tasks(tasks)

        return Task(
            id=task_id,
            document_id=document_id,
            task_type=task_type,
            status=TaskStatus.PENDING,
            progress=0,
            retry_count=0,
            max_retries=3,
            created_at=now,
        )

    async def get(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            The Task if found, None otherwise.
        """
        tasks = self._load_tasks()
        task_data = tasks.get(str(task_id))

        if not task_data:
            return None

        return self._task_from_dict(task_data)

    async def get_by_document(self, document_id: UUID) -> List[Task]:
        """Get all tasks associated with a document.

        Args:
            document_id: ID of the document.

        Returns:
            List of Task objects for the document, sorted by
            created_at descending (newest first).
        """
        tasks = self._load_tasks()
        doc_id_str = str(document_id)

        result = [
            self._task_from_dict(data)
            for data in tasks.values()
            if data["document_id"] == doc_id_str
        ]

        result.sort(key=lambda x: x.created_at, reverse=True)
        return result

    async def list_pending(self, limit: int = 10) -> List[Task]:
        """Get pending tasks ready for processing.

        Args:
            limit: Maximum number of tasks to return.

        Returns:
            List of pending Task objects, sorted by created_at ascending
            (oldest first for FIFO processing).
        """
        tasks = self._load_tasks()

        result = [
            self._task_from_dict(data)
            for data in tasks.values()
            if data["status"] == TaskStatus.PENDING.value
        ]

        result.sort(key=lambda x: x.created_at)
        return result[:limit]

    async def start(self, task_id: UUID) -> bool:
        """Mark a task as started/processing.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            True if successful, False if task not found.
        """
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        tasks[task_key]["status"] = TaskStatus.PROCESSING.value
        tasks[task_key]["started_at"] = datetime.now().isoformat()

        self._save_tasks(tasks)
        return True

    async def update_progress(
        self, task_id: UUID, progress: int, step: Optional[str] = None
    ) -> bool:
        """Update the progress of a task.

        Args:
            task_id: Unique identifier of the task.
            progress: Progress percentage (0-100).
            step: Optional description of the current processing step.

        Returns:
            True if successful, False if task not found.
        """
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        tasks[task_key]["progress"] = max(0, min(100, progress))
        if step is not None:
            tasks[task_key]["step"] = step

        self._save_tasks(tasks)
        return True

    async def complete(
        self, task_id: UUID, result: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Mark a task as completed.

        Args:
            task_id: Unique identifier of the task.
            result: Optional result data from the task.

        Returns:
            True if successful, False if task not found.
        """
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        now = datetime.now()
        tasks[task_key]["status"] = TaskStatus.COMPLETED.value
        tasks[task_key]["progress"] = 100
        tasks[task_key]["completed_at"] = now.isoformat()

        if result is not None:
            tasks[task_key]["result"] = result

        self._save_tasks(tasks)
        return True

    async def fail(self, task_id: UUID, error: str) -> bool:
        """Mark a task as failed and handle retry logic.

        If the task has remaining retries, it will be reset to pending
        with incremented retry count. Otherwise, it stays failed.

        Args:
            task_id: Unique identifier of the task.
            error: Error message describing the failure.

        Returns:
            True if successful, False if task not found.
        """
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        task = tasks[task_key]
        task["retry_count"] = task.get("retry_count", 0) + 1
        task["last_error"] = error

        # Check if we should retry
        if task["retry_count"] < task.get("max_retries", 3):
            task["status"] = TaskStatus.PENDING.value
        else:
            task["status"] = TaskStatus.FAILED.value
            task["completed_at"] = datetime.now().isoformat()

        self._save_tasks(tasks)
        return True

    async def cancel(self, task_id: UUID) -> bool:
        """Cancel a pending or processing task.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            True if successful, False if task not found or cannot be cancelled.
        """
        tasks = self._load_tasks()
        task_key = str(task_id)

        if task_key not in tasks:
            return False

        task = tasks[task_key]

        # Can only cancel pending or processing tasks
        if task["status"] not in [
            TaskStatus.PENDING.value,
            TaskStatus.PROCESSING.value,
        ]:
            return False

        task["status"] = TaskStatus.CANCELLED.value
        task["completed_at"] = datetime.now().isoformat()

        self._save_tasks(tasks)
        return True

    async def get_by_documents_batch(self, doc_ids: List[UUID]) -> List[Task]:
        """Retrieve all tasks for multiple documents in a single query.

        Args:
            doc_ids: List of document IDs to query tasks for.

        Returns:
            List of all tasks associated with the given document IDs.
        """
        if not doc_ids:
            return []

        tasks = self._load_tasks()
        doc_ids_set = {str(doc_id) for doc_id in doc_ids}

        result = [
            self._task_from_dict(data)
            for data in tasks.values()
            if data["document_id"] in doc_ids_set
        ]

        result.sort(key=lambda x: x.created_at, reverse=True)
        return result

    async def delete_by_document(self, document_id: UUID) -> int:
        """Delete all tasks for a document.

        Args:
            document_id: ID of the document.

        Returns:
            Number of tasks deleted.
        """
        tasks = self._load_tasks()
        doc_id_str = str(document_id)

        to_delete = [
            task_id
            for task_id, data in tasks.items()
            if data["document_id"] == doc_id_str
        ]

        for task_id in to_delete:
            del tasks[task_id]

        self._save_tasks(tasks)
        return len(to_delete)

    async def begin_transaction(self) -> None:
        """Create a snapshot of current state for potential rollback."""
        self._tx_snapshot = copy.deepcopy(self._load_tasks())

    async def commit_transaction(self) -> None:
        """Commit changes by clearing the snapshot.

        Changes are already persisted to disk during individual operations,
        so commit just clears the rollback snapshot.
        """
        self._tx_snapshot = None

    async def rollback_transaction(self) -> None:
        """Rollback to snapshot state by restoring from the saved snapshot."""
        if self._tx_snapshot is not None:
            self._save_tasks(self._tx_snapshot)
            self._tx_snapshot = None
