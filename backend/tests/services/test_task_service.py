"""Tests for TaskService."""

import uuid

import pytest

from app.services.task_service import TaskService
from app.storage.base import StorageManager
from app.storage.models import TaskStatus


class TestTaskService:
    """Test cases for TaskService."""

    @pytest.mark.asyncio
    async def test_create_task(self, local_storage_manager: StorageManager):
        """Test creating a task."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        task = await service.create_task(doc_id, "document_processing")

        assert task.id is not None
        assert task.document_id == doc_id
        assert task.task_type == "document_processing"
        assert task.status == TaskStatus.PENDING

    @pytest.mark.asyncio
    async def test_get_task(self, local_storage_manager: StorageManager):
        """Test getting a task."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        created = await service.create_task(doc_id, "document_processing")
        task = await service.get_task(created.id)

        assert task is not None
        assert task.id == created.id

    @pytest.mark.asyncio
    async def test_get_task_not_found(self, local_storage_manager: StorageManager):
        """Test getting a non-existent task."""
        service = TaskService(local_storage_manager)

        task = await service.get_task(uuid.uuid4())

        assert task is None

    @pytest.mark.asyncio
    async def test_get_tasks_by_document(self, local_storage_manager: StorageManager):
        """Test getting tasks by document ID."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        await service.create_task(doc_id, "task1")
        await service.create_task(doc_id, "task2")

        tasks = await service.get_tasks_by_document(doc_id)

        assert len(tasks) == 2
        assert all(t.document_id == doc_id for t in tasks)

    @pytest.mark.asyncio
    async def test_start_task(self, local_storage_manager: StorageManager):
        """Test starting a task."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        task = await service.create_task(doc_id, "document_processing")
        success = await service.start_task(task.id)

        assert success
        started = await service.get_task(task.id)
        assert started.status == TaskStatus.PROCESSING

    @pytest.mark.asyncio
    async def test_update_progress(self, local_storage_manager: StorageManager):
        """Test updating task progress."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        task = await service.create_task(doc_id, "document_processing")
        success = await service.update_progress(task.id, 50, "Processing document")

        assert success
        updated = await service.get_task(task.id)
        assert updated.progress == 50
        assert updated.step == "Processing document"

    @pytest.mark.asyncio
    async def test_complete_task(self, local_storage_manager: StorageManager):
        """Test completing a task."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        task = await service.create_task(doc_id, "document_processing")
        success = await service.complete_task(
            task.id, result={"entities_count": 10}
        )

        assert success
        completed = await service.get_task(task.id)
        assert completed.status == TaskStatus.COMPLETED
        assert completed.progress == 100
        assert completed.result == {"entities_count": 10}

    @pytest.mark.asyncio
    async def test_fail_task(self, local_storage_manager: StorageManager):
        """Test failing a task."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        task = await service.create_task(doc_id, "document_processing")
        success = await service.fail_task(task.id, "Test error")

        assert success
        failed = await service.get_task(task.id)
        assert failed.last_error == "Test error"

    @pytest.mark.asyncio
    async def test_cancel_task(self, local_storage_manager: StorageManager):
        """Test cancelling a task."""
        service = TaskService(local_storage_manager)
        doc_id = uuid.uuid4()

        task = await service.create_task(doc_id, "document_processing")
        success = await service.cancel_task(task.id)

        assert success
        cancelled = await service.get_task(task.id)
        assert cancelled.status == TaskStatus.CANCELLED

    @pytest.mark.asyncio
    async def test_list_pending_tasks(self, local_storage_manager: StorageManager):
        """Test listing pending tasks."""
        service = TaskService(local_storage_manager)

        # Create multiple tasks
        for i in range(3):
            await service.create_task(uuid.uuid4(), f"task{i}")

        pending = await service.list_pending_tasks()

        assert len(pending) == 3
        assert all(t.status == TaskStatus.PENDING for t in pending)
