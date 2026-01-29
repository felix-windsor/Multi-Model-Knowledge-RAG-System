"""FastAPI 依赖注入"""
import os
import sys
from pathlib import Path
from functools import lru_cache
import httpx
import logging
from typing import Dict, Optional

from fastapi import Depends

# 设置 NO_PROXY 环境变量，避免本地服务走代理
# 这对 qdrant_client, neo4j 等库内部使用的 httpx 也生效
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
os.environ.setdefault("no_proxy", "localhost,127.0.0.1")

# 添加 knowledge-graph-rag 到 Python 路径
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from knowledge_graph_rag import RAGAnything, RAGAnythingConfig
from app.services.llm_factory import ModelFactory, LLMFactory
from app.services.document_service import DocumentService
from app.services.task_service import TaskService
from app.services.webhook_service import WebhookService
from app.config import settings, Settings, validate_storage_config
from app.storage import StorageManager, get_storage_manager

logger = logging.getLogger(__name__)


_rag_instance: Optional[RAGAnything] = None
_storage_healthy: Optional[bool] = None  # None means not yet checked


async def create_rag_instance(backend: str) -> RAGAnything:
    """
    Create RAG instance with specified storage backend

    Args:
        backend: Storage backend type ("local" or "qdrant_neo4j")

    Returns:
        Configured RAGAnything instance

    Raises:
        ValueError: If configuration is invalid
    """
    # Validate configuration
    validate_storage_config(backend, settings)

    # Create RAG config
    rag_config = RAGAnythingConfig(
        working_dir=settings.storage_dir,
        parser="mineru",
        parse_method="auto",
        enable_image_processing=True,
        enable_table_processing=True,
        enable_equation_processing=True,
        max_concurrent_files=settings.max_concurrent_files
    )

    # Get model configurations
    llm_config = settings.get_model_config("llm")
    vision_config = settings.get_model_config("vision")
    embedding_config = settings.get_model_config("embedding")
    rerank_config = settings.get_model_config("rerank")

    # Create model functions
    llm_func = ModelFactory.create_llm_function(
        provider=llm_config["provider"],
        model=llm_config["model"],
        api_key=llm_config["api_key"],
        base_url=llm_config["base_url"]
    )

    vision_func = ModelFactory.create_vision_function(
        provider=vision_config["provider"],
        model=vision_config["model"],
        api_key=vision_config["api_key"],
        base_url=vision_config["base_url"],
        fallback_llm_func=llm_func
    )

    embed_func = ModelFactory.create_embedding_function(
        provider=embedding_config["provider"],
        model=embedding_config["model"],
        api_key=embedding_config["api_key"],
        base_url=embedding_config["base_url"],
        embedding_dim=settings.embedding_dim
    )

    rerank_func = None
    if rerank_config["provider"]:
        rerank_func = ModelFactory.create_rerank_function(
            provider=rerank_config["provider"],
            model=rerank_config["model"],
            api_key=rerank_config["api_key"],
            base_url=rerank_config["base_url"]
        )

    # LightRAG performance parameters
    lightrag_kwargs = {
        "embedding_batch_num": settings.embedding_batch_num,
        "embedding_func_max_async": settings.embedding_func_max_async,
        "chunk_token_size": settings.chunk_token_size,
        "chunk_overlap_token_size": settings.chunk_overlap_token_size,
        "entity_extract_max_gleaning": settings.entity_extract_max_gleaning,
        "top_k": settings.query_top_k,
    }

    # Add embedding cache configuration
    if settings.embedding_cache_enabled:
        lightrag_kwargs["embedding_cache_config"] = {
            "enabled": True,
            "similarity_threshold": settings.embedding_cache_threshold,
        }

    if rerank_func:
        lightrag_kwargs["rerank_model_func"] = rerank_func

    # Configure storage backend
    if backend == "qdrant_neo4j":
        lightrag_kwargs.update({
            "vector_storage": "QdrantVectorDBStorage",
            "graph_storage": "Neo4JStorage",
            "vector_db_storage_cls_kwargs": {
                "url": settings.qdrant_url,
                "collection_name": settings.qdrant_collection_name,
                "timeout": 30,
                "prefer_grpc": True,
            }
        })

        # Neo4j config via environment variables (LightRAG reads these)
        os.environ["NEO4J_URI"] = settings.neo4j_uri
        os.environ["NEO4J_USERNAME"] = settings.neo4j_user
        os.environ["NEO4J_PASSWORD"] = settings.neo4j_password
        os.environ["NEO4J_DATABASE"] = settings.neo4j_database

    # Create RAG instance
    instance = RAGAnything(
        config=rag_config,
        llm_model_func=llm_func,
        embedding_func=embed_func,
        vision_model_func=vision_func,
        lightrag_kwargs=lightrag_kwargs
    )

    logger.info(f"RAG instance created with backend: {backend}")
    return instance


async def check_storage_health(backend: str, config: Settings) -> Dict[str, bool]:
    """
    Check storage backend health status

    Args:
        backend: Storage backend type
        config: Settings instance

    Returns:
        Dictionary with health status for each backend
        {"qdrant": True/False, "neo4j": True/False}
    """
    global _storage_healthy
    health = {}

    if backend == "qdrant_neo4j":
        # Check Qdrant
        try:
            async with httpx.AsyncClient(trust_env=False) as client:
                response = await client.get(
                    f"{config.qdrant_url}/healthz",
                    timeout=5.0
                )
                health["qdrant"] = response.status_code == 200
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            health["qdrant"] = False

        # Check Neo4j via HTTP API (avoids pyarrow dependency issues)
        try:
            # Neo4j Browser HTTP endpoint
            neo4j_http_url = config.neo4j_uri.replace("bolt://", "http://").replace(":7687", ":7474")
            async with httpx.AsyncClient(trust_env=False) as client:
                response = await client.get(
                    neo4j_http_url,
                    timeout=5.0
                )
                # Neo4j returns JSON with bolt_routing info when healthy
                health["neo4j"] = response.status_code == 200
        except Exception as e:
            logger.error(f"Neo4j health check failed: {e}")
            health["neo4j"] = False

        # Update global health status
        _storage_healthy = all(health.values())
    else:
        # Local storage is always considered healthy
        _storage_healthy = True

    return health


async def get_rag_instance() -> Optional[RAGAnything]:
    """
    Get RAGAnything singleton instance

    Uses STORAGE_BACKEND environment variable to determine backend.
    Returns None if storage health check failed (graceful degradation).
    """
    global _rag_instance, _storage_healthy

    # If health check failed, don't initialize RAG instance
    if _storage_healthy is False:
        logger.warning("RAG instance not available: storage health check failed")
        return None

    if _rag_instance is None:
        backend = os.getenv("STORAGE_BACKEND", settings.storage_backend)
        try:
            _rag_instance = await create_rag_instance(backend)
        except Exception as e:
            logger.error(f"Failed to create RAG instance: {e}")
            _storage_healthy = False
            return None

    return _rag_instance


@lru_cache()
def get_settings():
    """获取配置实例"""
    return settings


async def get_storage() -> StorageManager:
    """
    FastAPI dependency for storage manager.

    Use with Depends() to inject storage into route handlers:
        @router.get("/documents")
        async def list_documents(storage: StorageManager = Depends(get_storage)):
            return await storage.documents.list()
    """
    return await get_storage_manager()


async def get_document_service(
    storage: StorageManager = Depends(get_storage),
) -> DocumentService:
    """
    FastAPI dependency for document service.

    Use with Depends() to inject into route handlers:
        @router.post("/documents/upload")
        async def upload_document(
            doc_svc: DocumentService = Depends(get_document_service),
        ):
            ...
    """
    return DocumentService(storage)


async def get_task_service(
    storage: StorageManager = Depends(get_storage),
) -> TaskService:
    """
    FastAPI dependency for task service.

    Use with Depends() to inject into route handlers:
        @router.get("/tasks/{task_id}")
        async def get_task(
            task_id: str,
            task_svc: TaskService = Depends(get_task_service),
        ):
            ...
    """
    return TaskService(storage)


async def get_webhook_service(
    storage: StorageManager = Depends(get_storage),
) -> WebhookService:
    """
    FastAPI dependency for webhook service.

    Use with Depends() to inject into route handlers:
        @router.post("/webhooks")
        async def create_webhook(
            webhook_svc: WebhookService = Depends(get_webhook_service),
        ):
            ...
    """
    return WebhookService(storage)
