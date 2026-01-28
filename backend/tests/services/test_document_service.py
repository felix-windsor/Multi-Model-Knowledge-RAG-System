"""Tests for DocumentService."""

import uuid

import pytest

from app.exceptions import ServiceError
from app.services.document_service import DocumentService
from app.storage.base import StorageManager
from app.storage.models import DocumentStatus


class TestDocumentService:
    """Test cases for DocumentService."""

    @pytest.mark.asyncio
    async def test_create_document(self, local_storage_manager: StorageManager):
        """Test creating a document."""
        service = DocumentService(local_storage_manager)

        document = await service.create_document(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        assert document.id is not None
        assert document.filename == "test.pdf"
        assert document.status == DocumentStatus.PENDING

    @pytest.mark.asyncio
    async def test_create_document_with_task(
        self, local_storage_manager: StorageManager
    ):
        """Test transactional creation of document with task."""
        service = DocumentService(local_storage_manager)

        document, task, webhook = await service.create_document_with_task(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        assert document.id is not None
        assert task.id is not None
        assert task.document_id == document.id
        assert webhook is None  # No callback_url provided

    @pytest.mark.asyncio
    async def test_create_document_with_task_and_webhook(
        self, local_storage_manager: StorageManager
    ):
        """Test transactional creation with webhook."""
        service = DocumentService(local_storage_manager)

        document, task, webhook = await service.create_document_with_task(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
            callback_url="https://example.com/callback",
        )

        assert document.id is not None
        assert task.id is not None
        assert webhook is not None
        assert webhook.callback_url == "https://example.com/callback"
        assert webhook.document_id == document.id

    @pytest.mark.asyncio
    async def test_get_document(self, local_storage_manager: StorageManager):
        """Test getting a document."""
        service = DocumentService(local_storage_manager)

        created = await service.create_document(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        document = await service.get_document(created.id)

        assert document is not None
        assert document.id == created.id

    @pytest.mark.asyncio
    async def test_get_document_not_found(self, local_storage_manager: StorageManager):
        """Test getting a non-existent document."""
        service = DocumentService(local_storage_manager)

        document = await service.get_document(uuid.uuid4())

        assert document is None

    @pytest.mark.asyncio
    async def test_get_document_with_status(
        self, local_storage_manager: StorageManager
    ):
        """Test getting document with aggregated status."""
        service = DocumentService(local_storage_manager)

        document, task, _ = await service.create_document_with_task(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        # Update task progress
        await local_storage_manager.tasks.update_progress(
            task.id, 50, "Processing"
        )

        status = await service.get_document_with_status(document.id)

        assert status is not None
        assert status["doc_id"] == str(document.id)
        assert status["filename"] == "test.pdf"
        assert status["progress"] == 50
        assert status["step"] == "Processing"

    @pytest.mark.asyncio
    async def test_list_documents_with_status(
        self, local_storage_manager: StorageManager
    ):
        """Test listing documents with status using batch query."""
        service = DocumentService(local_storage_manager)

        # Create multiple documents
        for i in range(3):
            await service.create_document_with_task(
                filename=f"doc{i}.pdf",
                file_path=f"/path/to/doc{i}.pdf",
                file_size=1024 * (i + 1),
                mime_type="application/pdf",
            )

        documents = await service.list_documents_with_status()

        assert len(documents) == 3
        assert all("doc_id" in doc for doc in documents)
        assert all("progress" in doc for doc in documents)

    @pytest.mark.asyncio
    async def test_update_status(self, local_storage_manager: StorageManager):
        """Test updating document status."""
        service = DocumentService(local_storage_manager)

        document = await service.create_document(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        success = await service.update_status(
            document.id, DocumentStatus.COMPLETED
        )

        assert success
        updated = await service.get_document(document.id)
        assert updated.status == DocumentStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_delete_document(self, local_storage_manager: StorageManager):
        """Test deleting a document."""
        service = DocumentService(local_storage_manager)

        document = await service.create_document(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        success = await service.delete_document(document.id)

        assert success
        deleted = await service.get_document(document.id)
        assert deleted is None
