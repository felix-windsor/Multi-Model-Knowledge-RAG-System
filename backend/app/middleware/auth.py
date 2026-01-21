"""API Key 认证中间件"""
import os
from typing import Optional
from fastapi import Request, HTTPException, Security
from fastapi.security import APIKeyHeader
from app.config import settings

# API Key Header 定义
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_valid_api_keys() -> list[str]:
    """
    获取有效的 API Key 列表
    从环境变量或配置文件读取
    支持多个 API Key（用逗号分隔）
    """
    api_keys_str = os.getenv("API_KEYS", "")
    if not api_keys_str:
        # 如果没有配置 API Keys，返回空列表（允许无认证访问）
        return []

    # 分割并过滤空字符串
    return [key.strip() for key in api_keys_str.split(",") if key.strip()]


def is_valid_api_key(api_key: str) -> bool:
    """验证 API Key 是否有效"""
    valid_keys = get_valid_api_keys()

    # 如果没有配置任何 API Key，则允许所有访问（开发模式）
    if not valid_keys:
        return True

    return api_key in valid_keys


async def verify_api_key(
    request: Request,
    api_key: Optional[str] = Security(api_key_header)
) -> Optional[str]:
    """
    验证 API Key 依赖

    用于 FastAPI 的依赖注入：
    @router.get("/endpoint")
    async def endpoint(api_key: str = Depends(verify_api_key)):
        ...
    """
    valid_keys = get_valid_api_keys()

    # 如果没有配置任何 API Key，跳过验证（开发模式）
    if not valid_keys:
        return None

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "code": 40001,
                "message": "Missing API Key. Please provide X-API-Key header."
            }
        )

    if not is_valid_api_key(api_key):
        raise HTTPException(
            status_code=401,
            detail={
                "code": 40002,
                "message": "Invalid API Key"
            }
        )

    return api_key


async def get_api_key(
    api_key: Optional[str] = Security(api_key_header)
) -> Optional[str]:
    """
    获取 API Key（不验证，用于可选认证场景）
    """
    return api_key
