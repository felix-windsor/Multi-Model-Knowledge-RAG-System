"""V1 配置和健康检查 API"""
from fastapi import APIRouter, Depends
from app.dependencies import get_rag_instance, get_settings
from app.middleware.auth import verify_api_key, get_api_key
from app.middleware.response import wrap_response
from app.models.response import V1ConfigData, V1HealthData
from app.config import Settings

router = APIRouter()


@router.get("/health")
async def health_check(
    api_key: str = Depends(get_api_key)  # 健康检查不强制要求 API Key
):
    """
    健康检查

    返回服务状态和基本信息
    """
    # 检查 RAG 是否初始化
    rag_initialized = False
    try:
        rag = await get_rag_instance()
        rag_initialized = rag is not None
    except Exception:
        pass

    return wrap_response(
        data=V1HealthData(
            status="healthy",
            version="1.0.0",
            rag_initialized=rag_initialized
        ).model_dump()
    )


@router.get("/config")
async def get_config(
    settings: Settings = Depends(get_settings),
    api_key: str = Depends(verify_api_key)
):
    """
    获取当前配置（脱敏）

    不返回敏感信息如 API Key
    """
    # 获取模型配置（脱敏）
    llm_config = settings.get_model_config("llm")
    embedding_config = settings.get_model_config("embedding")

    return wrap_response(
        data=V1ConfigData(
            llm_provider=llm_config["provider"],
            llm_model=llm_config["model"],
            embedding_provider=embedding_config["provider"],
            embedding_model=embedding_config["model"],
            embedding_dim=settings.embedding_dim,
            storage_dir=settings.storage_dir
        ).model_dump()
    )
