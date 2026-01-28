"""
Integration tests for RAG system with database backends

These tests require Docker services to be running:
- docker-compose up -d qdrant neo4j

Tests are automatically skipped if:
- STORAGE_BACKEND != qdrant_neo4j
- Required services are not available
"""
import os
import pytest
import asyncio
import httpx
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.config import Settings
from app.dependencies import create_rag_instance, check_storage_health


pytestmark = pytest.mark.integration


@pytest.fixture
def storage_backend():
    """Get current storage backend from environment"""
    return os.getenv("STORAGE_BACKEND", "local")


@pytest.fixture
def skip_if_not_database(storage_backend):
    """Skip test if storage backend is not qdrant_neo4j"""
    if storage_backend != "qdrant_neo4j":
        pytest.skip(f"Test requires STORAGE_BACKEND=qdrant_neo4j, got {storage_backend}")


@pytest.fixture
async def wait_for_services():
    """
    Wait for Qdrant and Neo4j to be ready

    Skips test if services are not available after timeout
    """
    settings = Settings(storage_backend="qdrant_neo4j")
    max_retries = 10
    retry_delay = 2

    for attempt in range(max_retries):
        health = await check_storage_health("qdrant_neo4j", settings)

        if health.get("qdrant") and health.get("neo4j"):
            return True

        if attempt < max_retries - 1:
            await asyncio.sleep(retry_delay)

    pytest.skip("Required services (Qdrant/Neo4j) are not available")


@pytest.mark.asyncio
async def test_health_check_with_database_backend(skip_if_not_database, wait_for_services):
    """
    Test health check endpoint when database services are running

    Verifies:
    - Health endpoint returns 200
    - Response includes storage_backend
    - Backend is set to qdrant_neo4j
    """
    from app.main import app

    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["status"] == "healthy"
    assert data["data"]["storage_backend"] == "qdrant_neo4j"


@pytest.mark.asyncio
async def test_detailed_health_check_with_statistics(skip_if_not_database, wait_for_services):
    """
    Test detailed health check endpoint returns storage statistics

    Verifies:
    - Detailed health endpoint returns 200
    - Response includes storage_stats
    - Statistics include qdrant and neo4j data
    """
    from app.main import app

    client = TestClient(app)

    response = client.get("/api/v1/health/detailed")

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "storage_stats" in data["data"]

    storage_stats = data["data"]["storage_stats"]
    assert "qdrant" in storage_stats or "neo4j" in storage_stats


@pytest.mark.asyncio
async def test_qdrant_connection(skip_if_not_database, wait_for_services):
    """
    Test direct connection to Qdrant service

    Verifies:
    - Qdrant health endpoint is accessible
    - Collections endpoint returns valid response
    """
    settings = Settings(storage_backend="qdrant_neo4j")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.qdrant_url}/healthz", timeout=5.0)
        assert response.status_code == 200

        response = await client.get(f"{settings.qdrant_url}/collections", timeout=5.0)
        assert response.status_code == 200
        data = response.json()
        assert "result" in data


@pytest.mark.asyncio
async def test_neo4j_connection(skip_if_not_database, wait_for_services):
    """
    Test direct connection to Neo4j service

    Verifies:
    - Neo4j driver can connect
    - Simple query executes successfully
    """
    settings = Settings(storage_backend="qdrant_neo4j")

    try:
        from neo4j import GraphDatabase
    except ImportError:
        pytest.skip("neo4j driver not installed")

    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password)
    )

    with driver.session(database=settings.neo4j_database) as session:
        result = session.run("RETURN 1 as value")
        record = result.single()
        assert record["value"] == 1

    driver.close()


@pytest.mark.asyncio
async def test_create_rag_instance_with_database_backend(skip_if_not_database, wait_for_services):
    """
    Test RAG instance creation with database backend

    Verifies:
    - RAG instance can be created with qdrant_neo4j backend
    - Instance has correct storage configuration
    - No exceptions are raised during creation
    """
    settings = Settings(storage_backend="qdrant_neo4j")

    with patch("app.config.settings", settings):
        instance = await create_rag_instance("qdrant_neo4j")

        assert instance is not None
        assert instance.lightrag_kwargs.get("vector_storage") == "QdrantVectorDBStorage"
        assert instance.lightrag_kwargs.get("graph_storage") == "Neo4JStorage"


@pytest.mark.asyncio
async def test_document_upload_with_database_backend(skip_if_not_database, wait_for_services):
    """
    Test document upload with database backend

    Verifies:
    - Document can be uploaded via API
    - Upload request returns 202 (accepted for processing)
    - Response includes task_id for tracking
    """
    from app.main import app
    from io import BytesIO

    client = TestClient(app)

    test_content = b"This is a test document for integration testing."
    test_file = BytesIO(test_content)
    test_file.name = "test_integration.txt"

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test_integration.txt", test_file, "text/plain")}
    )

    assert response.status_code == 202
    data = response.json()
    assert data["code"] == 0
    assert "task_id" in data["data"]
    assert "doc_id" in data["data"]


@pytest.mark.asyncio
async def test_check_storage_health_function(skip_if_not_database, wait_for_services):
    """
    Test check_storage_health utility function

    Verifies:
    - Function returns health status for both services
    - Both qdrant and neo4j are marked as healthy
    """
    settings = Settings(storage_backend="qdrant_neo4j")

    health = await check_storage_health("qdrant_neo4j", settings)

    assert "qdrant" in health
    assert "neo4j" in health
    assert health["qdrant"] is True
    assert health["neo4j"] is True


@pytest.mark.asyncio
async def test_qdrant_collection_operations(skip_if_not_database, wait_for_services):
    """
    Test Qdrant collection operations

    Verifies:
    - Can list collections
    - Target collection exists or can be created
    - Collection info can be retrieved
    """
    settings = Settings(storage_backend="qdrant_neo4j")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.qdrant_url}/collections",
            timeout=5.0
        )
        assert response.status_code == 200

        data = response.json()
        collections = data.get("result", {}).get("collections", [])

        collection_names = [c["name"] for c in collections]

        if settings.qdrant_collection_name not in collection_names:
            pytest.skip(f"Collection {settings.qdrant_collection_name} not yet created")
        else:
            response = await client.get(
                f"{settings.qdrant_url}/collections/{settings.qdrant_collection_name}",
                timeout=5.0
            )
            assert response.status_code == 200


@pytest.mark.asyncio
async def test_neo4j_database_operations(skip_if_not_database, wait_for_services):
    """
    Test Neo4j database operations

    Verifies:
    - Can execute queries
    - Can count nodes and relationships
    - Database is accessible and responsive
    """
    settings = Settings(storage_backend="qdrant_neo4j")

    try:
        from neo4j import GraphDatabase
    except ImportError:
        pytest.skip("neo4j driver not installed")

    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password)
    )

    with driver.session(database=settings.neo4j_database) as session:
        result = session.run("MATCH (n) RETURN count(n) as node_count")
        record = result.single()
        node_count = record["node_count"]
        assert node_count >= 0

        result = session.run("MATCH ()-[r]->() RETURN count(r) as rel_count")
        record = result.single()
        rel_count = record["rel_count"]
        assert rel_count >= 0

    driver.close()
