"""Tests for LocalTaskStorage."""

import uuid

import pytest

from app.storage.local.task import LocalTaskStorage
from app.storage.models import TaskStatus


class TestLocalTaskStorage:
    """Test cases for LocalTaskStorage."""

    @pytest.mark.asyncio
    async def test_create_task(self, local_task_storage: LocalTaskStorage):
        """Test creating a new task."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        assert task.id is not None
        assert task.document_id == doc_id
        assert task.task_type == "document_processing"
        assert task.status == TaskStatus.PENDING
        assert task.progress == 0
        assert task.step is None

    @pytest.mark.asyncio
    async def test_get_task(self, local_task_storage: LocalTaskStorage):
        """Test getting a task by ID."""
        doc_id = uuid.uuid4()
        created = await local_task_storage.create(doc_id, "document_processing")

        task = await local_task_storage.get(created.id)

        assert task is not None
        assert task.id == created.id
        assert task.document_id == doc_id

    @pytest.mark.asyncio
    async def test_get_task_not_found(self, local_task_storage: LocalTaskStorage):
        """Test getting a non-existent task."""
        task = await local_task_storage.get(uuid.uuid4())
        assert task is None

    @pytest.mark.asyncio
    async def test_get_by_document(self, local_task_storage: LocalTaskStorage):
        """Test getting tasks by document ID."""
        doc_id = uuid.uuid4()
        await local_task_storage.create(doc_id, "task1")
        await local_task_storage.create(doc_id, "task2")
        await local_task_storage.create(uuid.uuid4(), "other_doc_task")

        tasks = await local_task_storage.get_by_document(doc_id)

        assert len(tasks) == 2
        assert all(t.document_id == doc_id for t in tasks)

    @pytest.mark.asyncio
    async def test_update_progress_with_step(
        self, local_task_storage: LocalTaskStorage
    ):
        """Test updating task progress with step."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        success = await local_task_storage.update_progress(
            task.id, 50, "Processing document"
        )

        assert success
        updated = await local_task_storage.get(task.id)
        assert updated.progress == 50
        assert updated.step == "Processing document"

    @pytest.mark.asyncio
    async def test_start_task(self, local_task_storage: LocalTaskStorage):
        """Test starting a task."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        success = await local_task_storage.start(task.id)

        assert success
        started = await local_task_storage.get(task.id)
        assert started.status == TaskStatus.PROCESSING
        assert started.started_at is not None

    @pytest.mark.asyncio
    async def test_complete_task(self, local_task_storage: LocalTaskStorage):
        """Test completing a task."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        success = await local_task_storage.complete(
            task.id, result={"entities_count": 10}
        )

        assert success
        completed = await local_task_storage.get(task.id)
        assert completed.status == TaskStatus.COMPLETED
        assert completed.progress == 100
        assert completed.result == {"entities_count": 10}
        assert completed.completed_at is not None

    @pytest.mark.asyncio
    async def test_fail_task_with_retry(self, local_task_storage: LocalTaskStorage):
        """Test failing a task with retry available."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        success = await local_task_storage.fail(task.id, "Test error")

        assert success
        failed = await local_task_storage.get(task.id)
        assert failed.status == TaskStatus.PENDING  # Reset for retry
        assert failed.retry_count == 1
        assert failed.last_error == "Test error"

    @pytest.mark.asyncio
    async def test_fail_task_max_retries(self, local_task_storage: LocalTaskStorage):
        """Test failing a task that has exhausted retries."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        # Fail multiple times to exhaust retries
        for i in range(3):
            await local_task_storage.fail(task.id, f"Error {i}")

        failed = await local_task_storage.get(task.id)
        assert failed.status == TaskStatus.FAILED
        assert failed.retry_count == 3

    @pytest.mark.asyncio
    async def test_cancel_task(self, local_task_storage: LocalTaskStorage):
        """Test cancelling a task."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        success = await local_task_storage.cancel(task.id)

        assert success
        cancelled = await local_task_storage.get(task.id)
        assert cancelled.status == TaskStatus.CANCELLED
        assert cancelled.completed_at is not None

    @pytest.mark.asyncio
    async def test_cancel_completed_task_fails(
        self, local_task_storage: LocalTaskStorage
    ):
        """Test that cancelling a completed task fails."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")
        await local_task_storage.complete(task.id)

        success = await local_task_storage.cancel(task.id)

        assert not success

    @pytest.mark.asyncio
    async def test_get_by_documents_batch(self, local_task_storage: LocalTaskStorage):
        """Test batch query for multiple documents."""
        doc_id1 = uuid.uuid4()
        doc_id2 = uuid.uuid4()
        doc_id3 = uuid.uuid4()

        await local_task_storage.create(doc_id1, "task1")
        await local_task_storage.create(doc_id1, "task2")
        await local_task_storage.create(doc_id2, "task3")
        await local_task_storage.create(doc_id3, "other")

        tasks = await local_task_storage.get_by_documents_batch([doc_id1, doc_id2])

        assert len(tasks) == 3
        doc_ids = {t.document_id for t in tasks}
        assert doc_ids == {doc_id1, doc_id2}

    @pytest.mark.asyncio
    async def test_get_by_documents_batch_empty(
        self, local_task_storage: LocalTaskStorage
    ):
        """Test batch query with empty list."""
        tasks = await local_task_storage.get_by_documents_batch([])
        assert tasks == []

    @pytest.mark.asyncio
    async def test_transaction_rollback(self, local_task_storage: LocalTaskStorage):
        """Test transaction rollback restores state."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        # Begin transaction and make changes
        await local_task_storage.begin_transaction()
        await local_task_storage.update_progress(task.id, 50, "Processing")

        # Verify change was made
        updated = await local_task_storage.get(task.id)
        assert updated.progress == 50

        # Rollback
        await local_task_storage.rollback_transaction()

        # Verify rollback restored original state
        restored = await local_task_storage.get(task.id)
        assert restored.progress == 0

    @pytest.mark.asyncio
    async def test_transaction_commit(self, local_task_storage: LocalTaskStorage):
        """Test transaction commit persists changes."""
        doc_id = uuid.uuid4()
        task = await local_task_storage.create(doc_id, "document_processing")

        # Begin transaction and make changes
        await local_task_storage.begin_transaction()
        await local_task_storage.update_progress(task.id, 75, "Building graph")
        await local_task_storage.commit_transaction()

        # Verify change persisted
        committed = await local_task_storage.get(task.id)
        assert committed.progress == 75
        assert committed.step == "Building graph"
