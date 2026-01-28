"""Test health check API endpoints"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_check_basic():
    """Test basic health check endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert data["code"] == 0

        # Check health data
        health_data = data["data"]
        assert "status" in health_data
        assert health_data["status"] == "healthy"
        assert "storage_backend" in health_data


@pytest.mark.asyncio
async def test_health_check_detailed():
    """Test detailed health check endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health/detailed")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert data["code"] == 0

        # Check detailed health data
        health_data = data["data"]
        assert "status" in health_data
        assert health_data["status"] == "healthy"
        assert "storage_backend" in health_data
        assert "storage_stats" in health_data
        assert "timestamp" in health_data

        # Verify timestamp is ISO format
        from datetime import datetime
        timestamp = health_data["timestamp"]
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


@pytest.mark.asyncio
async def test_health_check_no_auth_required():
    """Test that health checks don't require authentication"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Call without X-API-Key header
        response = await client.get("/api/v1/health")
        assert response.status_code == 200

        response = await client.get("/api/v1/health/detailed")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check_storage_stats_local():
    """Test storage stats for local backend"""
    import os
    original_backend = os.environ.get("STORAGE_BACKEND")

    try:
        os.environ["STORAGE_BACKEND"] = "local"

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/health/detailed")

            assert response.status_code == 200
            data = response.json()
            health_data = data["data"]

            assert health_data["storage_backend"] == "local"
            # Local backend should return empty storage_stats
            assert health_data["storage_stats"] == {}

    finally:
        if original_backend:
            os.environ["STORAGE_BACKEND"] = original_backend
        else:
            os.environ.pop("STORAGE_BACKEND", None)


@pytest.mark.asyncio
async def test_health_check_storage_stats_qdrant_neo4j():
    """Test storage stats structure for qdrant_neo4j backend"""
    from app.config import Settings
    from app.dependencies import get_settings

    # Create a mock settings with qdrant_neo4j backend
    mock_settings = Settings()
    mock_settings.storage_backend = "qdrant_neo4j"
    mock_settings.qdrant_url = "http://localhost:6333"
    mock_settings.qdrant_collection_name = "rag_collection"
    mock_settings.neo4j_uri = "bolt://localhost:7687"
    mock_settings.neo4j_user = "neo4j"
    mock_settings.neo4j_password = "password"
    mock_settings.neo4j_database = "neo4j"

    # Override the dependency
    def override_get_settings():
        return mock_settings

    app.dependency_overrides[get_settings] = override_get_settings

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/health/detailed")

            assert response.status_code == 200
            data = response.json()
            health_data = data["data"]

            # Verify the mocked backend is returned
            assert health_data["storage_backend"] == "qdrant_neo4j"
            assert "storage_stats" in health_data

            # Storage stats should be present (may contain errors if services unavailable)
            stats = health_data["storage_stats"]
            assert isinstance(stats, dict)
    finally:
        # Clean up dependency override
        app.dependency_overrides.clear()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
