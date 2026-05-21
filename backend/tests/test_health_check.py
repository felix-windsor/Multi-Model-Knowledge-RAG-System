"""Test storage health checks"""
import pytest
from unittest.mock import AsyncMock, patch
from app.dependencies import check_storage_health
from app.config import Settings


pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_local_storage_health_empty():
    """Test local storage returns empty health dict"""
    settings = Settings(storage_backend="local")
    health = await check_storage_health("local", settings)
    assert health == {}


@pytest.mark.asyncio
async def test_qdrant_health_check_success():
    """Test Qdrant health check when service is healthy"""
    settings = Settings(
        storage_backend="qdrant_neo4j",
        qdrant_url="http://localhost:6333"
    )

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

        health = await check_storage_health("qdrant_neo4j", settings)
        assert health["qdrant"] is True


@pytest.mark.asyncio
async def test_qdrant_health_check_failure():
    """Test Qdrant health check when service is down"""
    settings = Settings(
        storage_backend="qdrant_neo4j",
        qdrant_url="http://localhost:6333"
    )

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Connection refused")

        health = await check_storage_health("qdrant_neo4j", settings)
        assert health["qdrant"] is False


@pytest.mark.asyncio
async def test_neo4j_health_check_success():
    """Test Neo4j health check when service is healthy"""
    settings = Settings(
        storage_backend="qdrant_neo4j",
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

        health = await check_storage_health("qdrant_neo4j", settings)
        assert health["neo4j"] is True


@pytest.mark.asyncio
async def test_neo4j_health_check_failure():
    """Test Neo4j health check when service is down"""
    settings = Settings(
        storage_backend="qdrant_neo4j",
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Connection refused")

        health = await check_storage_health("qdrant_neo4j", settings)
        assert health["neo4j"] is False
