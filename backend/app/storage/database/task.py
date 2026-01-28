"""PostgreSQL task storage implementation."""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..base import TaskStorage
from ..models import Task, TaskStatus
from .connection import DatabasePool


class DatabaseTaskStorage(TaskStorage):
    """PostgreSQL-based task storage.

    This class implements the TaskStorage interface using PostgreSQL
    as the underlying storage backend. It provides CRUD operations for
    task records including lifecycle management, progress tracking,
    and automatic retry logic.
    """

    def _row_to_task(self, row) -> Task:
        """Convert a database row to a Task model.

        Args:
            row: An asyncpg Record containing task data.

        Returns:
            A Task model instance populated from the row data.
        """
        result_data: Optional[Dict[str, Any]] = None
        if row["result"] is not None:
            if isinstance(row["result"], str):
                result_data = json.loads(row["result"])
            else:
                result_data = row["result"]

        return Task(
            id=row["id"],
            document_id=row["document_id"],
            task_type=row["task_type"],
            status=TaskStatus(row["status"]),
            progress=row["progress"],
            step=row.get("step"),
            retry_count=row["retry_count"],
            max_retries=row["max_retries"],
            last_error=row["last_error"],
            result=result_data,
            created_at=row["created_at"],
            started_at=row["started_at"],
            completed_at=row["completed_at"],
        )

    async def create(self, document_id: UUID, task_type: str) -> Task:
        """Create a new task for document processing.

        Args:
            document_id: ID of the document this task processes.
            task_type: Type of task (e.g., "document_processing").

        Returns:
            The created Task with generated ID and timestamps.
        """
        task_id = uuid.uuid4()
        now = datetime.now()

        async with DatabasePool.connection() as conn:
            await conn.execute(
                """
                INSERT INTO tasks (id, document_id, task_type, status, progress, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                task_id,
                document_id,
                task_type,
                TaskStatus.PENDING.value,
                0,
                now,
            )

        return Task(
            id=task_id,
            document_id=document_id,
            task_type=task_type,
            status=TaskStatus.PENDING,
            progress=0,
            created_at=now,
        )

    async def get(self, task_id: UUID) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            The Task if found, None otherwise.
        """
        async with DatabasePool.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM tasks WHERE id = $1",
                task_id,
            )

        if not row:
            return None

        return self._row_to_task(row)

    async def get_by_document(self, document_id: UUID) -> List[Task]:
        """Get all tasks associated with a document.

        Args:
            document_id: ID of the document.

        Returns:
            List of Task objects for the document, ordered by creation time descending.
        """
        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM tasks
                WHERE document_id = $1
                ORDER BY created_at DESC
                """,
                document_id,
            )

        return [self._row_to_task(row) for row in rows]

    async def list_pending(self, limit: int = 10) -> List[Task]:
        """Get pending tasks ready for processing.

        Args:
            limit: Maximum number of tasks to return.

        Returns:
            List of pending Task objects, ordered by creation time ascending (FIFO).
        """
        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM tasks
                WHERE status = $1
                ORDER BY created_at ASC
                LIMIT $2
                """,
                TaskStatus.PENDING.value,
                limit,
            )

        return [self._row_to_task(row) for row in rows]

    async def start(self, task_id: UUID) -> bool:
        """Mark a task as started/processing.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            True if successful, False if task not found.
        """
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                """
                UPDATE tasks
                SET status = $1, started_at = $2
                WHERE id = $3
                """,
                TaskStatus.PROCESSING.value,
                datetime.now(),
                task_id,
            )

        return result == "UPDATE 1"

    async def update_progress(
        self, task_id: UUID, progress: int, step: Optional[str] = None
    ) -> bool:
        """Update the progress of a task.

        Args:
            task_id: Unique identifier of the task.
            progress: Progress percentage (0-100). Values outside this range
                will be clamped.
            step: Optional description of the current processing step.

        Returns:
            True if successful, False if task not found.
        """
        progress = max(0, min(100, progress))

        async with DatabasePool.connection() as conn:
            if step is not None:
                result = await conn.execute(
                    "UPDATE tasks SET progress = $1, step = $2 WHERE id = $3",
                    progress,
                    step,
                    task_id,
                )
            else:
                result = await conn.execute(
                    "UPDATE tasks SET progress = $1 WHERE id = $2",
                    progress,
                    task_id,
                )

        return result == "UPDATE 1"

    async def complete(self, task_id: UUID, result: Optional[Any] = None) -> bool:
        """Mark a task as completed.

        Args:
            task_id: Unique identifier of the task.
            result: Optional result data from the task.

        Returns:
            True if successful, False if task not found.
        """
        now = datetime.now()
        result_json = json.dumps(result) if result is not None else None

        async with DatabasePool.connection() as conn:
            db_result = await conn.execute(
                """
                UPDATE tasks
                SET status = $1, progress = 100, result = $2, completed_at = $3
                WHERE id = $4
                """,
                TaskStatus.COMPLETED.value,
                result_json,
                now,
                task_id,
            )

        return db_result == "UPDATE 1"

    async def fail(self, task_id: UUID, error: str) -> bool:
        """Mark a task as failed and handle retry logic.

        If the task has remaining retries, it will be reset to pending status
        with an incremented retry count. Otherwise, it will be marked as failed.

        Args:
            task_id: Unique identifier of the task.
            error: Error message describing the failure.

        Returns:
            True if successful, False if task not found.
        """
        async with DatabasePool.transaction() as conn:
            # Get current retry count and max retries
            row = await conn.fetchrow(
                "SELECT retry_count, max_retries FROM tasks WHERE id = $1",
                task_id,
            )

            if not row:
                return False

            new_retry_count = row["retry_count"] + 1

            if new_retry_count < row["max_retries"]:
                # Retry available: reset to pending status
                await conn.execute(
                    """
                    UPDATE tasks
                    SET status = $1, retry_count = $2, last_error = $3
                    WHERE id = $4
                    """,
                    TaskStatus.PENDING.value,
                    new_retry_count,
                    error,
                    task_id,
                )
            else:
                # Max retries reached: mark as permanently failed
                await conn.execute(
                    """
                    UPDATE tasks
                    SET status = $1, retry_count = $2, last_error = $3, completed_at = $4
                    WHERE id = $5
                    """,
                    TaskStatus.FAILED.value,
                    new_retry_count,
                    error,
                    datetime.now(),
                    task_id,
                )

        return True

    async def cancel(self, task_id: UUID) -> bool:
        """Cancel a pending or processing task.

        Only tasks in pending or processing status can be cancelled.
        Completed or failed tasks cannot be cancelled.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            True if successful, False if task not found or cannot be cancelled.
        """
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                """
                UPDATE tasks
                SET status = $1, completed_at = $2
                WHERE id = $3 AND status IN ($4, $5)
                """,
                TaskStatus.CANCELLED.value,
                datetime.now(),
                task_id,
                TaskStatus.PENDING.value,
                TaskStatus.PROCESSING.value,
            )

        return result == "UPDATE 1"

    async def get_by_documents_batch(self, doc_ids: List[UUID]) -> List[Task]:
        """Retrieve all tasks for multiple documents in a single query.

        Args:
            doc_ids: List of document IDs to query tasks for.

        Returns:
            List of all tasks associated with the given document IDs.
        """
        if not doc_ids:
            return []

        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM tasks
                WHERE document_id = ANY($1)
                ORDER BY created_at DESC
                """,
                doc_ids,
            )

        return [self._row_to_task(row) for row in rows]
