"""V1 健康检查 API"""
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends
import httpx

from app.config import Settings
from app.dependencies import get_settings
from app.middleware.auth import get_api_key
from app.middleware.response import wrap_response

logger = logging.getLogger(__name__)

router = APIRouter()


async def get_storage_stats(settings: Settings) -> Dict[str, Any]:
    """
    Get storage statistics based on backend type

    Args:
        settings: Application settings

    Returns:
        Dictionary with storage statistics (empty for local backend)
    """
    backend = settings.storage_backend.lower()

    if backend == "local":
        return {}

    if backend == "qdrant_neo4j":
        stats = {}

        # Get Qdrant statistics
        try:
            async with httpx.AsyncClient(trust_env=False) as client:
                response = await client.get(
                    f"{settings.qdrant_url}/collections",
                    timeout=5.0
                )
                if response.status_code == 200:
                    collections_data = response.json()
                    collections = collections_data.get("result", {}).get("collections", [])

                    qdrant_stats = {}
                    for collection in collections:
                        if collection["name"] == settings.qdrant_collection_name:
                            qdrant_stats = {
                                "collection": collection["name"],
                                "vectors_count": collection.get("vectors_count", 0),
                                "points_count": collection.get("points_count", 0),
                            }
                            break

                    if qdrant_stats:
                        stats["qdrant"] = qdrant_stats
                    else:
                        stats["qdrant"] = {"status": "collection_not_found"}
                else:
                    stats["qdrant"] = {"status": "unavailable", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.warning(f"Failed to fetch Qdrant stats: {e}")
            stats["qdrant"] = {"status": "error", "error": str(e)}

        # Get Neo4j statistics
        driver = None
        try:
            from neo4j import GraphDatabase

            driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password)
            )

            with driver.session(database=settings.neo4j_database) as session:
                result = session.run(
                    "MATCH (n) RETURN count(n) as node_count"
                )
                record = result.single()
                node_count = record["node_count"] if record else 0

                result = session.run(
                    "MATCH ()-[r]->() RETURN count(r) as relationship_count"
                )
                record = result.single()
                relationship_count = record["relationship_count"] if record else 0

                stats["neo4j"] = {
                    "node_count": node_count,
                    "relationship_count": relationship_count,
                }

        except ImportError:
            logger.warning("Neo4j driver not installed")
            stats["neo4j"] = {"status": "driver_not_installed"}
        except Exception as e:
            logger.warning(f"Failed to fetch Neo4j stats: {e}")
            stats["neo4j"] = {"status": "error", "error": str(e)}
        finally:
            if driver is not None:
                driver.close()

        return stats

    return {}


@router.get("/health")
async def health_check(
    settings: Settings = Depends(get_settings),
    api_key: str = Depends(get_api_key)
):
    """
    Basic health check

    Returns service status and storage backend information
    """
    return wrap_response(
        data={
            "status": "healthy",
            "storage_backend": settings.storage_backend,
        }
    )


@router.get("/health/detailed")
async def health_check_detailed(
    settings: Settings = Depends(get_settings),
    api_key: str = Depends(get_api_key)
):
    """
    Detailed health check

    Returns service status, storage backend, storage statistics, and timestamp
    """
    storage_stats = await get_storage_stats(settings)

    return wrap_response(
        data={
            "status": "healthy",
            "storage_backend": settings.storage_backend,
            "storage_stats": storage_stats,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )
