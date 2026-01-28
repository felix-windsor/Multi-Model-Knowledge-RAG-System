"""Test error handling for unavailable storage backends"""
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_rag_instance, get_settings
from app.middleware.auth import verify_api_key


def test_upload_document_returns_503_when_rag_unavailable():
    """Test that document upload returns 503 when RAG instance is None"""

    # Mock dependency to return None for RAG instance
    async def mock_get_rag_instance():
        return None

    # Mock API key verification to pass
    async def mock_verify_api_key():
        return "test-key"

    # Mock settings
    def mock_get_settings():
        settings = MagicMock()
        settings.upload_dir = "/tmp/test"
        return settings

    # Override dependencies
    app.dependency_overrides[get_rag_instance] = mock_get_rag_instance
    app.dependency_overrides[verify_api_key] = mock_verify_api_key
    app.dependency_overrides[get_settings] = mock_get_settings

    try:
        client = TestClient(app)

        # Prepare test file
        test_file_content = b"test content"
        files = {"file": ("test.pdf", test_file_content, "application/pdf")}

        # Make request
        response = client.post("/api/v1/documents/upload", files=files)

        # Should return 503 Service Unavailable
        assert response.status_code == 503

        # Check response format
        data = response.json()
        # HTTPException wraps our response in 'detail'
        assert "detail" in data
        detail = data["detail"]
        assert detail["code"] != 0  # Error code
        assert "RAG" in detail["message"] or "storage" in detail["message"].lower()
        assert "unavailable" in detail["message"].lower() or "not ready" in detail["message"].lower()
        assert "request_id" in detail
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


def test_query_returns_503_when_rag_unavailable():
    """Test that query returns 503 when RAG instance is None"""

    # Mock dependency to return None for RAG instance
    async def mock_get_rag_instance():
        return None

    # Mock API key verification to pass
    async def mock_verify_api_key():
        return "test-key"

    # Override dependencies
    app.dependency_overrides[get_rag_instance] = mock_get_rag_instance
    app.dependency_overrides[verify_api_key] = mock_verify_api_key

    try:
        client = TestClient(app)

        # Make request
        response = client.post(
            "/api/v1/query",
            json={"question": "What is this?", "mode": "mix"}
        )

        # Should return 503 Service Unavailable
        assert response.status_code == 503

        # Check response format
        data = response.json()
        # HTTPException wraps our response in 'detail'
        assert "detail" in data
        detail = data["detail"]
        assert detail["code"] != 0  # Error code
        assert "RAG" in detail["message"] or "storage" in detail["message"].lower()
        assert "unavailable" in detail["message"].lower() or "not ready" in detail["message"].lower()
        assert "request_id" in detail
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


def test_query_stream_returns_503_when_rag_unavailable():
    """Test that stream query returns 503 when RAG instance is None"""

    # Mock dependency to return None for RAG instance
    async def mock_get_rag_instance():
        return None

    # Mock API key verification to pass
    async def mock_verify_api_key():
        return "test-key"

    # Override dependencies
    app.dependency_overrides[get_rag_instance] = mock_get_rag_instance
    app.dependency_overrides[verify_api_key] = mock_verify_api_key

    try:
        client = TestClient(app)

        # Make request
        response = client.post(
            "/api/v1/query/stream",
            json={"question": "What is this?", "mode": "mix"}
        )

        # Should return 503 Service Unavailable
        assert response.status_code == 503

        # Check response format
        data = response.json()
        # HTTPException wraps our response in 'detail'
        assert "detail" in data
        detail = data["detail"]
        assert detail["code"] != 0  # Error code
        assert "RAG" in detail["message"] or "storage" in detail["message"].lower()
        assert "unavailable" in detail["message"].lower() or "not ready" in detail["message"].lower()
        assert "request_id" in detail
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


def test_get_documents_returns_503_when_rag_unavailable():
    """Test that get documents returns 503 when RAG instance is None"""

    # Mock dependency to return None for RAG instance
    async def mock_get_rag_instance():
        return None

    # Mock API key verification to pass
    async def mock_verify_api_key():
        return "test-key"

    # Override dependencies
    app.dependency_overrides[get_rag_instance] = mock_get_rag_instance
    app.dependency_overrides[verify_api_key] = mock_verify_api_key

    try:
        client = TestClient(app)

        # Make request
        response = client.get("/api/v1/documents")

        # Should return 503 Service Unavailable
        assert response.status_code == 503

        # Check response format
        data = response.json()
        # HTTPException wraps our response in 'detail'
        assert "detail" in data
        detail = data["detail"]
        assert detail["code"] != 0  # Error code
        assert "request_id" in detail
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


def test_get_document_by_id_returns_503_when_rag_unavailable():
    """Test that get document by ID returns 503 when RAG instance is None"""

    # Mock dependency to return None for RAG instance
    async def mock_get_rag_instance():
        return None

    # Mock API key verification to pass
    async def mock_verify_api_key():
        return "test-key"

    # Override dependencies
    app.dependency_overrides[get_rag_instance] = mock_get_rag_instance
    app.dependency_overrides[verify_api_key] = mock_verify_api_key

    try:
        client = TestClient(app)

        # Make request
        response = client.get("/api/v1/documents/test-doc-id")

        # Should return 503 Service Unavailable
        assert response.status_code == 503

        # Check response format
        data = response.json()
        # HTTPException wraps our response in 'detail'
        assert "detail" in data
        detail = data["detail"]
        assert detail["code"] != 0  # Error code
        assert "request_id" in detail
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


def test_delete_document_returns_503_when_rag_unavailable():
    """Test that delete document returns 503 when RAG instance is None"""

    # Mock dependency to return None for RAG instance
    async def mock_get_rag_instance():
        return None

    # Mock API key verification to pass
    async def mock_verify_api_key():
        return "test-key"

    # Override dependencies
    app.dependency_overrides[get_rag_instance] = mock_get_rag_instance
    app.dependency_overrides[verify_api_key] = mock_verify_api_key

    try:
        client = TestClient(app)

        # Make request
        response = client.delete("/api/v1/documents/test-doc-id")

        # Should return 503 Service Unavailable
        assert response.status_code == 503

        # Check response format
        data = response.json()
        # HTTPException wraps our response in 'detail'
        assert "detail" in data
        detail = data["detail"]
        assert detail["code"] != 0  # Error code
        assert "request_id" in detail
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()
