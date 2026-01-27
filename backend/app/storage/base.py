"""Abstract storage interfaces.

This module defines the abstract base classes that establish the storage
interface contract. Both local (in-memory/file-based) and database
implementations will implement these interfaces, enabling seamless
switching between storage backends.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from .models import Document, Task, Webhook


class DocumentStorage(ABC):
    """Abstract interface for document metadata storage.

    Implementations handle persistent storage of document records,
    including creation, retrieval, status updates, and deletion.
    """

    @abstractmethod
    async def create(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str,
    ) -> Document:
        """Create a new document record.

        Args:
            filename: Original name of the uploaded file.
            file_path: Path where the file is stored.
            file_size: Size of the file in bytes.
            mime_type: MIME type of the file.

        Returns:
            The created Document with generated ID and timestamps.
        """
        pass

    @abstractmethod
    async def get(self, doc_id: UUID) -> Optional[Document]:
        """Get a document by its ID.

        Args:
            doc_id: Unique identifier of the document.

        Returns:
            The Document if found, None otherwise.
        """
        pass

    @abstractmethod
    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Document]:
        """List documents with optional filtering and pagination.

        Args:
            status: Filter by document status (e.g., "pending", "completed").
            limit: Maximum number of documents to return.
            offset: Number of documents to skip for pagination.

        Returns:
            List of Document objects matching the criteria.
        """
        pass

    @abstractmethod
    async def update_status(
        self,
        doc_id: UUID,
        status: str,
        error_message: Optional[str] = None,
    ) -> bool:
        """Update the status of a document.

        Args:
            doc_id: Unique identifier of the document.
            status: New status value.
            error_message: Optional error message if status is "failed".

        Returns:
            True if the update was successful, False if document not found.
        """
        pass

    @abstractmethod
    async def delete(self, doc_id: UUID) -> bool:
        """Delete a document and cascade to related records.

        This should also delete associated tasks and webhooks.

        Args:
            doc_id: Unique identifier of the document.

        Returns:
            True if deletion was successful, False if document not found.
        """
        pass


class TaskStorage(ABC):
    """Abstract interface for background task storage.

    Implementations handle persistent storage of task records,
    including lifecycle management, progress tracking, and retry logic.
    """

    @abstractmethod
    async def create(self, document_id: UUID, task_type: str) -> Task:
        """Create a new task for document processing.

        Args:
            document_id: ID of the document this task processes.
            task_type: Type of task (e.g., "document_processing").

        Returns:
            The created Task with generated ID and timestamps.
        """
        pass

    @abstractmethod
    async def get(self, task_id: UUID) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            The Task if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_by_document(self, document_id: UUID) -> List[Task]:
        """Get all tasks associated with a document.

        Args:
            document_id: ID of the document.

        Returns:
            List of Task objects for the document.
        """
        pass

    @abstractmethod
    async def list_pending(self, limit: int = 10) -> List[Task]:
        """Get pending tasks ready for processing.

        Args:
            limit: Maximum number of tasks to return.

        Returns:
            List of pending Task objects.
        """
        pass

    @abstractmethod
    async def start(self, task_id: UUID) -> bool:
        """Mark a task as started/processing.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            True if successful, False if task not found.
        """
        pass

    @abstractmethod
    async def update_progress(self, task_id: UUID, progress: int) -> bool:
        """Update the progress of a task.

        Args:
            task_id: Unique identifier of the task.
            progress: Progress percentage (0-100).

        Returns:
            True if successful, False if task not found.
        """
        pass

    @abstractmethod
    async def complete(self, task_id: UUID, result: Optional[Any] = None) -> bool:
        """Mark a task as completed.

        Args:
            task_id: Unique identifier of the task.
            result: Optional result data from the task.

        Returns:
            True if successful, False if task not found.
        """
        pass

    @abstractmethod
    async def fail(self, task_id: UUID, error: str) -> bool:
        """Mark a task as failed and handle retry logic.

        If the task has remaining retries, it should be reset to pending
        with incremented retry count. Otherwise, it stays failed.

        Args:
            task_id: Unique identifier of the task.
            error: Error message describing the failure.

        Returns:
            True if successful, False if task not found.
        """
        pass

    @abstractmethod
    async def cancel(self, task_id: UUID) -> bool:
        """Cancel a pending or processing task.

        Args:
            task_id: Unique identifier of the task.

        Returns:
            True if successful, False if task not found or cannot be cancelled.
        """
        pass


class WebhookStorage(ABC):
    """Abstract interface for webhook storage.

    Implementations handle persistent storage of webhook configurations
    and delivery tracking, including retry scheduling.
    """

    @abstractmethod
    async def create(
        self,
        document_id: UUID,
        callback_url: str,
        event_type: str,
    ) -> Webhook:
        """Create a new webhook for document event notification.

        Args:
            document_id: ID of the document to monitor.
            callback_url: URL to call when the event occurs.
            event_type: Type of event to trigger the webhook.

        Returns:
            The created Webhook with generated ID.
        """
        pass

    @abstractmethod
    async def get(self, webhook_id: UUID) -> Optional[Webhook]:
        """Get a webhook by its ID.

        Args:
            webhook_id: Unique identifier of the webhook.

        Returns:
            The Webhook if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_by_document(self, document_id: UUID) -> List[Webhook]:
        """Get all webhooks registered for a document.

        Args:
            document_id: ID of the document.

        Returns:
            List of Webhook objects for the document.
        """
        pass

    @abstractmethod
    async def list_pending(self, limit: int = 10) -> List[Webhook]:
        """Get pending webhooks ready for delivery.

        Includes webhooks that are pending and those with due retries
        (next_retry_at <= now).

        Args:
            limit: Maximum number of webhooks to return.

        Returns:
            List of pending Webhook objects.
        """
        pass

    @abstractmethod
    async def mark_delivered(self, webhook_id: UUID) -> bool:
        """Mark a webhook as successfully delivered.

        Args:
            webhook_id: Unique identifier of the webhook.

        Returns:
            True if successful, False if webhook not found.
        """
        pass

    @abstractmethod
    async def mark_failed(
        self,
        webhook_id: UUID,
        error: str,
        retry_after: Optional[datetime] = None,
    ) -> bool:
        """Mark a webhook as failed and optionally schedule retry.

        Args:
            webhook_id: Unique identifier of the webhook.
            error: Error message describing the failure.
            retry_after: Optional datetime for next retry attempt.

        Returns:
            True if successful, False if webhook not found.
        """
        pass


class StorageManager:
    """Unified storage manager providing access to all storage interfaces.

    This class aggregates the individual storage interfaces and provides
    a single point of access for storage operations. Use this as the
    main entry point for storage in services.

    Attributes:
        documents: Document metadata storage interface.
        tasks: Background task storage interface.
        webhooks: Webhook configuration storage interface.
    """

    def __init__(
        self,
        documents: DocumentStorage,
        tasks: TaskStorage,
        webhooks: WebhookStorage,
    ) -> None:
        """Initialize the storage manager with storage implementations.

        Args:
            documents: Implementation of DocumentStorage interface.
            tasks: Implementation of TaskStorage interface.
            webhooks: Implementation of WebhookStorage interface.
        """
        self.documents = documents
        self.tasks = tasks
        self.webhooks = webhooks
