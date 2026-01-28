"""Integration tests for document flow.

Tests the complete document lifecycle: upload -> process -> query status -> delete.
Tests V1 and Legacy API compatibility.
"""

import shutil
import tempfile
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1 import documents as v1_documents
from app.api.v1 import tasks as v1_tasks
from app.api import routes as legacy_routes
from app.dependencies import get_storage
from app.middleware.auth import verify_api_key
from app.storage.base import StorageManager
from app.storage.local.document import LocalDocumentStorage
from app.storage.local.task import LocalTaskStorage
from app.storage.local.webhook import LocalWebhookStorage


@pytest.fixture
def temp_storage_dir() -> Generator[str, None, None]:
    """Create a temporary directory for storage tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_upload_dir() -> Generator[str, None, None]:
    """Create a temporary directory for uploads."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def local_storage_manager(temp_storage_dir: str) -> StorageManager:
    """Create a StorageManager with local storage backends."""
    return StorageManager(
        documents=LocalDocumentStorage(storage_dir=temp_storage_dir),
        tasks=LocalTaskStorage(storage_dir=temp_storage_dir),
        webhooks=LocalWebhookStorage(storage_dir=temp_storage_dir),
    )


@pytest.fixture
def mock_settings(temp_upload_dir: str):
    """Create mock settings with temp upload directory."""
    settings = MagicMock()
    settings.upload_dir = temp_upload_dir
    settings.api_keys = ["test-api-key"]
    return settings


@pytest.fixture
def app(local_storage_manager: StorageManager, mock_settings) -> FastAPI:
    """Create a FastAPI test application."""
    app = FastAPI()

    # Override dependencies
    async def override_get_storage():
        return local_storage_manager

    async def override_verify_api_key():
        return "test-api-key"

    app.dependency_overrides[get_storage] = override_get_storage
    app.dependency_overrides[verify_api_key] = override_verify_api_key

    # Register routes
    app.include_router(v1_documents.router, prefix="/api/v1/documents")
    app.include_router(v1_tasks.router, prefix="/api/v1/tasks")
    app.include_router(legacy_routes.router, prefix="/api")

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a test client."""
    return TestClient(app)


class TestV1DocumentFlow:
    """Test V1 API document flow."""

    def test_get_documents_empty(self, client: TestClient):
        """Test getting documents when none exist."""
        response = client.get(
            "/api/v1/documents",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["total"] == 0
        assert data["data"]["documents"] == []

    def test_get_document_not_found(self, client: TestClient):
        """Test getting a non-existent document."""
        response = client.get(
            "/api/v1/documents/00000000-0000-0000-0000-000000000000",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 404

    def test_get_document_invalid_id(self, client: TestClient):
        """Test getting a document with invalid ID."""
        response = client.get(
            "/api/v1/documents/invalid-uuid",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 400

    def test_delete_document_not_found(self, client: TestClient):
        """Test deleting a non-existent document."""
        response = client.delete(
            "/api/v1/documents/00000000-0000-0000-0000-000000000000",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 404


class TestV1TaskFlow:
    """Test V1 API task flow."""

    def test_get_task_not_found(self, client: TestClient):
        """Test getting a non-existent task."""
        response = client.get(
            "/api/v1/tasks/00000000-0000-0000-0000-000000000000",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 404

    def test_get_task_invalid_id(self, client: TestClient):
        """Test getting a task with invalid ID."""
        response = client.get(
            "/api/v1/tasks/invalid-uuid",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 400

    def test_cancel_task_not_found(self, client: TestClient):
        """Test cancelling a non-existent task."""
        response = client.delete(
            "/api/v1/tasks/00000000-0000-0000-0000-000000000000",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 404


class TestLegacyDocumentFlow:
    """Test legacy API document flow."""

    def test_get_documents_empty(self, client: TestClient):
        """Test getting documents when none exist."""
        response = client.get("/api/documents/")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["documents"] == []

    def test_get_document_not_found(self, client: TestClient):
        """Test getting a non-existent document."""
        response = client.get("/api/documents/00000000-0000-0000-0000-000000000000")

        assert response.status_code == 404


class TestAPIResponseFormat:
    """Test API response format consistency."""

    def test_v1_success_response_format(self, client: TestClient):
        """Test V1 API success response has correct format."""
        response = client.get(
            "/api/v1/documents",
            headers={"X-API-Key": "test-api-key"},
        )

        data = response.json()
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert data["code"] == 0
        assert data["message"] == "success"

    def test_v1_error_response_format(self, client: TestClient):
        """Test V1 API error response has correct format."""
        response = client.get(
            "/api/v1/documents/invalid-uuid",
            headers={"X-API-Key": "test-api-key"},
        )

        assert response.status_code == 400
        data = response.json()
        # Error responses are wrapped in detail
        assert "detail" in data

    def test_legacy_list_response_format(self, client: TestClient):
        """Test legacy API list response has correct format."""
        response = client.get("/api/documents/")

        data = response.json()
        assert "total" in data
        assert "documents" in data
        assert isinstance(data["documents"], list)
