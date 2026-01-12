"""应用配置管理"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # LLM 配置
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    llm_api_key: str
    llm_base_url: str = "https://api.openai.com/v1"

    # Embedding 配置
    embedding_model: str = "text-embedding-3-large"
    embedding_dim: int = 3072

    # 存储配置
    storage_dir: str = "../data/storage"
    upload_dir: str = "../data/uploads"
    output_dir: str = "../data/output"

    # 文档处理配置
    max_concurrent_files: int = 2

    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # 忽略 .env 中未定义的字段
    )


# 全局配置实例
settings = Settings()
