"""Storage factory for creating storage instances based on configuration"""
from typing import Optional

from .base import StorageManager
from .local import LocalDocumentStorage, LocalTaskStorage, LocalWebhookStorage


_storage_manager: Optional[StorageManager] = None
_database_initialized: bool = False


async def _initialize_database(database_url: str):
    """Initialize database connection pool"""
    global _database_initialized

    if not _database_initialized:
        from .database import DatabasePool
        await DatabasePool.initialize(database_url)
        _database_initialized = True


async def create_storage_manager(
    backend: str = "local",
    storage_dir: str = "data/storage",
    database_url: Optional[str] = None,
    **kwargs
) -> StorageManager:
    """
    Create a StorageManager based on the specified backend.

    Args:
        backend: "local" or "database"
        storage_dir: Directory for local storage
        database_url: PostgreSQL connection URL (for database backend)
        **kwargs: Additional backend-specific options

    Returns:
        Configured StorageManager instance
    """
    if backend == "local":
        return StorageManager(
            documents=LocalDocumentStorage(storage_dir),
            tasks=LocalTaskStorage(storage_dir),
            webhooks=LocalWebhookStorage(storage_dir)
        )
    elif backend == "database":
        if not database_url:
            raise ValueError("database_url is required for database backend")

        # Initialize database connection
        await _initialize_database(database_url)

        from .database import (
            DatabaseDocumentStorage,
            DatabaseTaskStorage,
            DatabaseWebhookStorage
        )

        return StorageManager(
            documents=DatabaseDocumentStorage(),
            tasks=DatabaseTaskStorage(),
            webhooks=DatabaseWebhookStorage()
        )
    else:
        raise ValueError(f"Unknown storage backend: {backend}")


async def get_storage_manager() -> StorageManager:
    """Get the global storage manager instance"""
    global _storage_manager

    if _storage_manager is None:
        from app.config import settings

        _storage_manager = await create_storage_manager(
            backend=settings.storage_backend,
            storage_dir=settings.storage_dir,
            database_url=getattr(settings, 'database_url', None)
        )

    return _storage_manager


async def close_storage():
    """Close storage connections (call on shutdown)"""
    global _storage_manager, _database_initialized

    if _database_initialized:
        from .database import DatabasePool
        await DatabasePool.close()
        _database_initialized = False

    _storage_manager = None


def reset_storage_manager():
    """Reset the global storage manager (useful for testing)"""
    global _storage_manager
    _storage_manager = None
