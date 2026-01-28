"""Test RAG instance creation with different backends"""
import pytest
import os
from unittest.mock import patch, AsyncMock, MagicMock
from app.dependencies import create_rag_instance
from app.config import Settings


@pytest.mark.asyncio
async def test_create_rag_instance_local():
    """Test RAG instance creation with local storage"""
    with patch.dict(os.environ, {"STORAGE_BACKEND": "local"}):
        # Mock ModelFactory to avoid actual LLM calls
        with patch("app.dependencies.ModelFactory") as mock_factory:
            mock_llm = MagicMock()
            mock_vision = MagicMock()
            mock_embed = MagicMock()

            mock_factory.create_llm_function.return_value = mock_llm
            mock_factory.create_vision_function.return_value = mock_vision
            mock_factory.create_embedding_function.return_value = mock_embed
            mock_factory.create_rerank_function.return_value = None

            # Mock RAGAnything to avoid initialization
            with patch("app.dependencies.RAGAnything") as mock_rag_class:
                mock_instance = MagicMock()
                mock_rag_class.return_value = mock_instance

                instance = await create_rag_instance("local")

                assert instance is not None
                assert instance == mock_instance

                # Verify RAGAnything was called with correct params
                mock_rag_class.assert_called_once()
                call_kwargs = mock_rag_class.call_args.kwargs

                # Verify model functions were passed
                assert call_kwargs["llm_model_func"] == mock_llm
                assert call_kwargs["embedding_func"] == mock_embed
                assert call_kwargs["vision_model_func"] == mock_vision


@pytest.mark.asyncio
async def test_create_rag_instance_qdrant_neo4j():
    """Test RAG instance creation with database storage"""
    # Mock ModelFactory to avoid actual LLM calls
    with patch("app.dependencies.ModelFactory") as mock_factory:
        mock_llm = MagicMock()
        mock_vision = MagicMock()
        mock_embed = MagicMock()

        mock_factory.create_llm_function.return_value = mock_llm
        mock_factory.create_vision_function.return_value = mock_vision
        mock_factory.create_embedding_function.return_value = mock_embed
        mock_factory.create_rerank_function.return_value = None

        # Mock settings to provide database configuration
        with patch("app.dependencies.settings") as mock_settings:
            mock_settings.storage_dir = "../data/storage"
            mock_settings.max_concurrent_files = 2
            mock_settings.embedding_dim = 1024
            mock_settings.embedding_batch_num = 20
            mock_settings.embedding_func_max_async = 16
            mock_settings.embedding_cache_enabled = True
            mock_settings.embedding_cache_threshold = 0.95
            mock_settings.chunk_token_size = 1200
            mock_settings.chunk_overlap_token_size = 100
            mock_settings.entity_extract_max_gleaning = 1
            mock_settings.query_top_k = 10
            mock_settings.qdrant_url = "http://localhost:6333"
            mock_settings.qdrant_collection_name = "test_collection"
            mock_settings.neo4j_uri = "bolt://localhost:7687"
            mock_settings.neo4j_user = "neo4j"
            mock_settings.neo4j_password = "test123"
            mock_settings.neo4j_database = "neo4j"

            def mock_get_model_config(model_type):
                return {
                    "provider": "openai",
                    "model": "gpt-4o",
                    "api_key": "test-key",
                    "base_url": "https://api.openai.com/v1"
                }

            mock_settings.get_model_config = mock_get_model_config

            # Mock RAGAnything to avoid initialization
            with patch("app.dependencies.RAGAnything") as mock_rag_class:
                mock_instance = MagicMock()
                mock_rag_class.return_value = mock_instance

                instance = await create_rag_instance("qdrant_neo4j")

                assert instance is not None
                assert instance == mock_instance

                # Verify Neo4j env vars were set
                assert os.environ["NEO4J_URI"] == "bolt://localhost:7687"
                assert os.environ["NEO4J_USERNAME"] == "neo4j"
                assert os.environ["NEO4J_PASSWORD"] == "test123"

                # Verify RAGAnything was called with storage backend config
                mock_rag_class.assert_called_once()
                call_kwargs = mock_rag_class.call_args.kwargs
                lightrag_kwargs = call_kwargs["lightrag_kwargs"]

                assert lightrag_kwargs["vector_storage"] == "QdrantVectorDBStorage"
                assert lightrag_kwargs["graph_storage"] == "Neo4JStorage"
                assert "vector_db_storage_cls_kwargs" in lightrag_kwargs
                assert lightrag_kwargs["vector_db_storage_cls_kwargs"]["url"] == "http://localhost:6333"
                assert lightrag_kwargs["vector_db_storage_cls_kwargs"]["collection_name"] == "test_collection"


@pytest.mark.asyncio
async def test_create_rag_instance_validates_config():
    """Test RAG instance creation validates config"""
    with patch.dict(os.environ, {
        "STORAGE_BACKEND": "qdrant_neo4j",
        # Missing Neo4j config
    }, clear=True):
        # Need to reload settings to pick up the cleared environment
        with patch("app.dependencies.settings") as mock_settings:
            mock_settings.qdrant_url = ""
            mock_settings.neo4j_uri = ""
            mock_settings.neo4j_user = ""
            mock_settings.neo4j_password = ""

            with pytest.raises(ValueError, match="requires"):
                await create_rag_instance("qdrant_neo4j")


@pytest.mark.asyncio
async def test_create_rag_instance_with_rerank():
    """Test RAG instance creation with rerank function"""
    with patch.dict(os.environ, {"STORAGE_BACKEND": "local"}):
        # Mock ModelFactory to return a rerank function
        with patch("app.dependencies.ModelFactory") as mock_factory:
            mock_llm = MagicMock()
            mock_vision = MagicMock()
            mock_embed = MagicMock()
            mock_rerank = MagicMock()

            mock_factory.create_llm_function.return_value = mock_llm
            mock_factory.create_vision_function.return_value = mock_vision
            mock_factory.create_embedding_function.return_value = mock_embed
            mock_factory.create_rerank_function.return_value = mock_rerank

            # Mock settings to return rerank provider
            with patch("app.dependencies.settings") as mock_settings:
                mock_settings.storage_dir = "../data/storage"
                mock_settings.max_concurrent_files = 2
                mock_settings.embedding_dim = 1024
                mock_settings.embedding_batch_num = 20
                mock_settings.embedding_func_max_async = 16
                mock_settings.embedding_cache_enabled = True
                mock_settings.embedding_cache_threshold = 0.95
                mock_settings.chunk_token_size = 1200
                mock_settings.chunk_overlap_token_size = 100
                mock_settings.entity_extract_max_gleaning = 1
                mock_settings.query_top_k = 10

                def mock_get_model_config(model_type):
                    if model_type == "rerank":
                        return {
                            "provider": "jina",
                            "model": "jina-reranker-v1",
                            "api_key": "test-key",
                            "base_url": "https://api.jina.ai/v1"
                        }
                    return {
                        "provider": "openai",
                        "model": "gpt-4o",
                        "api_key": "test-key",
                        "base_url": "https://api.openai.com/v1"
                    }

                mock_settings.get_model_config = mock_get_model_config

                # Mock RAGAnything
                with patch("app.dependencies.RAGAnything") as mock_rag_class:
                    mock_instance = MagicMock()
                    mock_rag_class.return_value = mock_instance

                    instance = await create_rag_instance("local")

                    assert instance is not None

                    # Verify rerank function was passed to lightrag_kwargs
                    call_kwargs = mock_rag_class.call_args.kwargs
                    lightrag_kwargs = call_kwargs["lightrag_kwargs"]
                    assert "rerank_model_func" in lightrag_kwargs
                    assert lightrag_kwargs["rerank_model_func"] == mock_rerank
