"""Storage layer package.

This package provides abstract storage interfaces and data models for
the document management system. It supports multiple storage backends
through the abstract interface pattern.

Usage:
    from app.storage import StorageManager, Document, DocumentStatus

    # Get storage manager via dependency injection
    storage = get_storage_manager()
    doc = await storage.documents.get(doc_id)
"""

from .base import DocumentStorage, StorageManager, TaskStorage, WebhookStorage
from .models import Document, DocumentStatus, Task, TaskStatus, Webhook, WebhookStatus

__all__ = [
    # Data models
    "Document",
    "Task",
    "Webhook",
    # Status enums
    "DocumentStatus",
    "TaskStatus",
    "WebhookStatus",
    # Abstract interfaces
    "DocumentStorage",
    "TaskStorage",
    "WebhookStorage",
    "StorageManager",
]
