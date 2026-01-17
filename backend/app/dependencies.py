"""FastAPI 依赖注入"""
import sys
from pathlib import Path
from functools import lru_cache

# 添加 knowledge-graph-rag 到 Python 路径
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from knowledge_graph_rag import RAGAnything, RAGAnythingConfig
from app.services.llm_factory import ModelFactory, LLMFactory
from app.config import settings


_rag_instance = None


async def get_rag_instance() -> RAGAnything:
    """
    获取 RAGAnything 单例实例

    作为 FastAPI 依赖注入使用
    支持独立的模型提供商配置
    """
    global _rag_instance

    if _rag_instance is None:
        # 创建 RAG 配置
        rag_config = RAGAnythingConfig(
            working_dir=settings.storage_dir,
            parser="mineru",
            parse_method="auto",
            enable_image_processing=True,
            enable_table_processing=True,
            enable_equation_processing=True,
            max_concurrent_files=settings.max_concurrent_files
        )

        # 获取各模型类型的配置（支持配置继承）
        llm_config = settings.get_model_config("llm")
        vision_config = settings.get_model_config("vision")
        embedding_config = settings.get_model_config("embedding")
        rerank_config = settings.get_model_config("rerank")

        # 创建 LLM 函数
        llm_func = ModelFactory.create_llm_function(
            provider=llm_config["provider"],
            model=llm_config["model"],
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"]
        )

        # 创建 Vision 函数（使用 LLM 作为回退）
        vision_func = ModelFactory.create_vision_function(
            provider=vision_config["provider"],
            model=vision_config["model"],
            api_key=vision_config["api_key"],
            base_url=vision_config["base_url"],
            fallback_llm_func=llm_func
        )

        # 创建 Embedding 函数（独立配置）
        embed_func = ModelFactory.create_embedding_function(
            provider=embedding_config["provider"],
            model=embedding_config["model"],
            api_key=embedding_config["api_key"],
            base_url=embedding_config["base_url"],
            embedding_dim=settings.embedding_dim
        )

        # 创建 Rerank 函数（可选）
        rerank_func = None
        if rerank_config["provider"]:
            rerank_func = ModelFactory.create_rerank_function(
                provider=rerank_config["provider"],
                model=rerank_config["model"],
                api_key=rerank_config["api_key"],
                base_url=rerank_config["base_url"]
            )

        # 准备 LightRAG 的额外参数
        lightrag_kwargs = {}
        if rerank_func:
            lightrag_kwargs["rerank_model_func"] = rerank_func

        # 初始化 RAGAnything
        _rag_instance = RAGAnything(
            config=rag_config,
            llm_model_func=llm_func,
            embedding_func=embed_func,
            vision_model_func=vision_func,
            lightrag_kwargs=lightrag_kwargs
        )

    return _rag_instance


@lru_cache()
def get_settings():
    """获取配置实例"""
    return settings
