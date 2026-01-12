"""FastAPI 依赖注入"""
import sys
from pathlib import Path
from functools import lru_cache

# 添加 knowledge-graph-rag 到 Python 路径
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from knowledge_graph_rag import RAGAnything, RAGAnythingConfig
from app.services.llm_factory import LLMFactory
from app.config import settings


_rag_instance = None


async def get_rag_instance() -> RAGAnything:
    """
    获取 RAGAnything 单例实例

    作为 FastAPI 依赖注入使用
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

        # 创建 LLM 函数
        llm_func, embed_func, vision_func = await LLMFactory.create_llm_functions(
            provider=settings.llm_provider
        )

        # 初始化 RAGAnything
        _rag_instance = RAGAnything(
            config=rag_config,
            llm_model_func=llm_func,
            embedding_func=embed_func,
            vision_model_func=vision_func
        )

    return _rag_instance


@lru_cache()
def get_settings():
    """获取配置实例"""
    return settings
