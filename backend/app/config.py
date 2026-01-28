"""应用配置管理"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional

# 获取项目根目录（config.py 在 backend/app/，向上两级到根目录）
ROOT_DIR = Path(__file__).parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    """应用配置 - 支持独立的模型提供商配置"""

    # ============================================
    # LLM 配置 (主配置，必填)
    # ============================================
    llm_provider: str = "openai"  # openai, qwen, ollama, lmstudio
    llm_model: str = "gpt-4o"
    llm_api_key: str = ""  # Ollama 不需要 API Key
    llm_base_url: str = "https://api.openai.com/v1"

    # ============================================
    # Vision 配置 (可选，默认继承 LLM 配置)
    # ============================================
    vision_provider: Optional[str] = None  # 留空则使用 llm_provider
    vision_model: Optional[str] = None  # 留空则使用 llm_model
    vision_api_key: Optional[str] = None  # 留空则使用 llm_api_key
    vision_base_url: Optional[str] = None  # 留空则使用 llm_base_url

    # ============================================
    # Embedding 配置 (可选，默认继承 LLM 配置)
    # ============================================
    embedding_provider: Optional[str] = None  # 留空则使用 llm_provider
    embedding_model: Optional[str] = None  # 留空则使用 llm_model
    embedding_dim: int = 3072  # 默认维度，实际值取决于模型
    embedding_api_key: Optional[str] = None  # 留空则使用 llm_api_key
    embedding_base_url: Optional[str] = None  # 留空则使用 llm_base_url

    # ============================================
    # Rerank 配置 (可选，默认不使用)
    # ============================================
    rerank_provider: Optional[str] = None  # 留空则不使用 rerank
    rerank_model: Optional[str] = None
    rerank_api_key: Optional[str] = None  # 留空则使用 llm_api_key
    rerank_base_url: Optional[str] = None  # 留空则使用 llm_base_url

    # ============================================
    # 存储配置
    # ============================================
    storage_dir: str = "../data/storage"
    upload_dir: str = "../data/uploads"
    output_dir: str = "../data/output"

    # ============================================
    # 文档处理配置
    # ============================================
    max_concurrent_files: int = 2

    # ============================================
    # Performance Tuning Configuration
    # ============================================
    embedding_batch_num: int = 20  # LightRAG batch processing size
    embedding_func_max_async: int = 16  # LightRAG max async concurrency
    embedding_max_workers: int = 4  # Thread pool workers (for Ollama)
    embedding_cache_enabled: bool = True  # Enable embedding cache
    embedding_cache_threshold: float = 0.95  # Cache similarity threshold
    chunk_token_size: int = 1200  # Token size per chunk
    chunk_overlap_token_size: int = 100  # Overlap between chunks
    entity_extract_max_gleaning: int = 1  # Max entity extraction iterations
    query_top_k: int = 10  # Number of top results to return

    # ============================================
    # Storage Backend Configuration
    # ============================================
    storage_backend: str = "local"  # local | qdrant_neo4j

    # PostgreSQL (legacy, for future use)
    postgres_user: str = "rag"
    postgres_password: str = "rag123"
    postgres_db: str = "ragdb"
    database_url: Optional[str] = None

    # Qdrant Configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "rag_collection"
    qdrant_host: str = "localhost"  # legacy, kept for compatibility
    qdrant_port: int = 6333  # legacy, kept for compatibility

    # Neo4j Configuration
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""
    neo4j_database: str = "neo4j"

    # ============================================
    # 服务器配置
    # ============================================
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # 忽略 .env 中未定义的字段
    )

    def get_model_config(self, model_type: str) -> dict:
        """
        获取指定模型类型的配置，支持配置继承
        
        Args:
            model_type: 'llm', 'vision', 'embedding', 'rerank'
            
        Returns:
            包含 provider, model, api_key, base_url 的字典
        """
        # LLM 配置作为基础配置
        base_config = {
            "provider": self.llm_provider,
            "model": self.llm_model,
            "api_key": self.llm_api_key,
            "base_url": self.llm_base_url
        }
        
        if model_type == "llm":
            return base_config
        
        # 其他模型类型支持独立配置
        provider_attr = f"{model_type}_provider"
        model_attr = f"{model_type}_model"
        api_key_attr = f"{model_type}_api_key"
        base_url_attr = f"{model_type}_base_url"
        
        # 获取属性值，如果是 None 或空字符串，则使用基础配置
        def get_value_or_default(attr_name: str, default_key: str):
            value = getattr(self, attr_name)
            # 对于 Optional[str]，None 或空字符串都视为未设置
            if value is None or (isinstance(value, str) and value.strip() == ""):
                return base_config[default_key]
            return value
        
        config = {
            "provider": get_value_or_default(provider_attr, "provider"),
            "model": get_value_or_default(model_attr, "model"),
            "api_key": get_value_or_default(api_key_attr, "api_key"),
            "base_url": get_value_or_default(base_url_attr, "base_url")
        }
        
        return config


def validate_storage_config(backend: str, config: Settings) -> None:
    """
    Validate storage configuration completeness

    Args:
        backend: Storage backend type ("local" or "qdrant_neo4j")
        config: Settings instance

    Raises:
        ValueError: If required configuration is missing
    """
    if backend == "qdrant_neo4j":
        required = {
            "QDRANT_URL": config.qdrant_url,
            "NEO4J_URI": config.neo4j_uri,
            "NEO4J_USER": config.neo4j_user,
            "NEO4J_PASSWORD": config.neo4j_password,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(
                f"STORAGE_BACKEND=qdrant_neo4j requires: {', '.join(missing)}"
            )


# 全局配置实例
settings = Settings()
