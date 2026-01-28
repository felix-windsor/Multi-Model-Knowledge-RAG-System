"""Pytest configuration and fixtures for storage tests."""

import os
import shutil
import tempfile
from typing import Generator

import pytest

from app.storage.local.document import LocalDocumentStorage
from app.storage.local.task import LocalTaskStorage
from app.storage.local.webhook import LocalWebhookStorage
from app.storage.base import StorageManager


@pytest.fixture
def temp_storage_dir() -> Generator[str, None, None]:
    """Create a temporary directory for storage tests.

    Yields:
        Path to temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def local_document_storage(temp_storage_dir: str) -> LocalDocumentStorage:
    """Create a LocalDocumentStorage instance for testing.

    Args:
        temp_storage_dir: Temporary directory for storage.

    Returns:
        LocalDocumentStorage instance.
    """
    return LocalDocumentStorage(storage_dir=temp_storage_dir)


@pytest.fixture
def local_task_storage(temp_storage_dir: str) -> LocalTaskStorage:
    """Create a LocalTaskStorage instance for testing.

    Args:
        temp_storage_dir: Temporary directory for storage.

    Returns:
        LocalTaskStorage instance.
    """
    return LocalTaskStorage(storage_dir=temp_storage_dir)


@pytest.fixture
def local_webhook_storage(temp_storage_dir: str) -> LocalWebhookStorage:
    """Create a LocalWebhookStorage instance for testing.

    Args:
        temp_storage_dir: Temporary directory for storage.

    Returns:
        LocalWebhookStorage instance.
    """
    return LocalWebhookStorage(storage_dir=temp_storage_dir)


@pytest.fixture
def local_storage_manager(
    local_document_storage: LocalDocumentStorage,
    local_task_storage: LocalTaskStorage,
    local_webhook_storage: LocalWebhookStorage,
) -> StorageManager:
    """Create a StorageManager with local storage backends.

    Args:
        local_document_storage: LocalDocumentStorage instance.
        local_task_storage: LocalTaskStorage instance.
        local_webhook_storage: LocalWebhookStorage instance.

    Returns:
        StorageManager instance.
    """
    return StorageManager(
        documents=local_document_storage,
        tasks=local_task_storage,
        webhooks=local_webhook_storage,
    )
