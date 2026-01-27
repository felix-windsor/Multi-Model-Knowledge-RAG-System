"""Storage factory for creating storage instances based on configuration.

This module provides factory functions for creating storage backends based on
application configuration. It supports both local (file-based) storage and
database storage backends.

Usage:
    from app.storage.factory import get_storage_manager

    # Get the global storage manager instance
    storage = get_storage_manager()
    doc = await storage.documents.get(doc_id)
"""

from typing import Optional

from .base import StorageManager
from .local import LocalDocumentStorage, LocalTaskStorage, LocalWebhookStorage


def create_storage_manager(
    backend: str = "local",
    storage_dir: str = "data/storage",
    database_url: Optional[str] = None,
    **kwargs,
) -> StorageManager:
    """Create a StorageManager based on the specified backend.

    This factory function creates and configures a StorageManager with the
    appropriate storage implementations based on the backend parameter.

    Args:
        backend: Storage backend type ("local" or "database").
        storage_dir: Directory for local file storage (used by local backend).
        database_url: PostgreSQL connection URL (used by database backend).
        **kwargs: Additional backend-specific options.

    Returns:
        Configured StorageManager instance.

    Raises:
        ValueError: If an unknown backend is specified.
        NotImplementedError: If database backend is requested (not yet implemented).
    """
    if backend == "local":
        return StorageManager(
            documents=LocalDocumentStorage(storage_dir),
            tasks=LocalTaskStorage(storage_dir),
            webhooks=LocalWebhookStorage(storage_dir),
        )
    elif backend == "database":
        # Database implementation will be added in Phase 3
        raise NotImplementedError("Database backend not yet implemented")
    else:
        raise ValueError(f"Unknown storage backend: {backend}")


# Global storage manager instance
_storage_manager: Optional[StorageManager] = None


def get_storage_manager() -> StorageManager:
    """Get the global storage manager instance.

    This function implements a lazy singleton pattern for the storage manager.
    On first call, it creates a new StorageManager based on application settings.
    Subsequent calls return the same instance.

    Returns:
        The global StorageManager instance.

    Note:
        Configuration is loaded from app.config.settings on first access.
    """
    global _storage_manager

    if _storage_manager is None:
        # Import here to avoid circular imports
        from app.config import settings

        _storage_manager = create_storage_manager(
            backend=settings.storage_backend,
            storage_dir=settings.storage_dir,
            database_url=getattr(settings, "database_url", None),
        )

    return _storage_manager


def reset_storage_manager() -> None:
    """Reset the global storage manager instance.

    This function clears the global storage manager, forcing a new instance
    to be created on the next call to get_storage_manager(). This is primarily
    useful for testing scenarios where different configurations need to be tested.

    Note:
        After calling this function, the next call to get_storage_manager()
        will create a fresh instance based on current settings.
    """
    global _storage_manager
    _storage_manager = None
