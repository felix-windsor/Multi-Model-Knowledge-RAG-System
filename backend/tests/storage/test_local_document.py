"""Tests for LocalDocumentStorage."""

import uuid

import pytest

from app.storage.local.document import LocalDocumentStorage
from app.storage.models import DocumentStatus


class TestLocalDocumentStorage:
    """Test cases for LocalDocumentStorage."""

    @pytest.mark.asyncio
    async def test_create_document(self, local_document_storage: LocalDocumentStorage):
        """Test creating a new document."""
        document = await local_document_storage.create(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        assert document.id is not None
        assert document.filename == "test.pdf"
        assert document.file_path == "/path/to/test.pdf"
        assert document.file_size == 1024
        assert document.mime_type == "application/pdf"
        assert document.status == DocumentStatus.PENDING

    @pytest.mark.asyncio
    async def test_get_document(self, local_document_storage: LocalDocumentStorage):
        """Test getting a document by ID."""
        created = await local_document_storage.create(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        document = await local_document_storage.get(created.id)

        assert document is not None
        assert document.id == created.id
        assert document.filename == "test.pdf"

    @pytest.mark.asyncio
    async def test_get_document_not_found(
        self, local_document_storage: LocalDocumentStorage
    ):
        """Test getting a non-existent document."""
        document = await local_document_storage.get(uuid.uuid4())
        assert document is None

    @pytest.mark.asyncio
    async def test_list_documents(self, local_document_storage: LocalDocumentStorage):
        """Test listing all documents."""
        await local_document_storage.create(
            filename="doc1.pdf",
            file_path="/path/to/doc1.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )
        await local_document_storage.create(
            filename="doc2.pdf",
            file_path="/path/to/doc2.pdf",
            file_size=2048,
            mime_type="application/pdf",
        )

        documents = await local_document_storage.list()

        assert len(documents) == 2

    @pytest.mark.asyncio
    async def test_list_documents_with_status_filter(
        self, local_document_storage: LocalDocumentStorage
    ):
        """Test listing documents with status filter."""
        doc1 = await local_document_storage.create(
            filename="doc1.pdf",
            file_path="/path/to/doc1.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )
        await local_document_storage.create(
            filename="doc2.pdf",
            file_path="/path/to/doc2.pdf",
            file_size=2048,
            mime_type="application/pdf",
        )

        # Update one document to completed
        await local_document_storage.update_status(
            doc1.id, DocumentStatus.COMPLETED.value
        )

        # Filter by pending
        pending = await local_document_storage.list(status=DocumentStatus.PENDING.value)
        assert len(pending) == 1

        # Filter by completed
        completed = await local_document_storage.list(
            status=DocumentStatus.COMPLETED.value
        )
        assert len(completed) == 1

    @pytest.mark.asyncio
    async def test_list_documents_pagination(
        self, local_document_storage: LocalDocumentStorage
    ):
        """Test listing documents with pagination."""
        for i in range(5):
            await local_document_storage.create(
                filename=f"doc{i}.pdf",
                file_path=f"/path/to/doc{i}.pdf",
                file_size=1024,
                mime_type="application/pdf",
            )

        # Get first page
        page1 = await local_document_storage.list(limit=2, offset=0)
        assert len(page1) == 2

        # Get second page
        page2 = await local_document_storage.list(limit=2, offset=2)
        assert len(page2) == 2

        # Get last page
        page3 = await local_document_storage.list(limit=2, offset=4)
        assert len(page3) == 1

    @pytest.mark.asyncio
    async def test_update_status(self, local_document_storage: LocalDocumentStorage):
        """Test updating document status."""
        document = await local_document_storage.create(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        success = await local_document_storage.update_status(
            document.id, DocumentStatus.PROCESSING.value
        )

        assert success
        updated = await local_document_storage.get(document.id)
        assert updated.status == DocumentStatus.PROCESSING

    @pytest.mark.asyncio
    async def test_update_status_with_error(
        self, local_document_storage: LocalDocumentStorage
    ):
        """Test updating document status with error message."""
        document = await local_document_storage.create(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        success = await local_document_storage.update_status(
            document.id, DocumentStatus.FAILED.value, error_message="Processing failed"
        )

        assert success
        updated = await local_document_storage.get(document.id)
        assert updated.status == DocumentStatus.FAILED
        assert updated.error_message == "Processing failed"

    @pytest.mark.asyncio
    async def test_delete_document(self, local_document_storage: LocalDocumentStorage):
        """Test deleting a document."""
        document = await local_document_storage.create(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        success = await local_document_storage.delete(document.id)

        assert success
        deleted = await local_document_storage.get(document.id)
        assert deleted is None

    @pytest.mark.asyncio
    async def test_delete_document_not_found(
        self, local_document_storage: LocalDocumentStorage
    ):
        """Test deleting a non-existent document."""
        success = await local_document_storage.delete(uuid.uuid4())
        assert not success

    @pytest.mark.asyncio
    async def test_transaction_rollback(
        self, local_document_storage: LocalDocumentStorage
    ):
        """Test transaction rollback restores state."""
        document = await local_document_storage.create(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        # Begin transaction
        await local_document_storage.begin_transaction()

        # Make changes
        await local_document_storage.update_status(
            document.id, DocumentStatus.COMPLETED.value
        )

        # Verify change
        updated = await local_document_storage.get(document.id)
        assert updated.status == DocumentStatus.COMPLETED

        # Rollback
        await local_document_storage.rollback_transaction()

        # Verify rollback
        restored = await local_document_storage.get(document.id)
        assert restored.status == DocumentStatus.PENDING

    @pytest.mark.asyncio
    async def test_transaction_commit(
        self, local_document_storage: LocalDocumentStorage
    ):
        """Test transaction commit persists changes."""
        document = await local_document_storage.create(
            filename="test.pdf",
            file_path="/path/to/test.pdf",
            file_size=1024,
            mime_type="application/pdf",
        )

        # Begin transaction
        await local_document_storage.begin_transaction()

        # Make changes
        await local_document_storage.update_status(
            document.id, DocumentStatus.PROCESSING.value
        )

        # Commit
        await local_document_storage.commit_transaction()

        # Verify persisted
        committed = await local_document_storage.get(document.id)
        assert committed.status == DocumentStatus.PROCESSING
