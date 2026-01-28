"""统一响应格式中间件"""
import uuid
from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    统一 API 响应格式

    成功响应:
    {
        "code": 0,
        "message": "success",
        "data": { ... },
        "request_id": "uuid-xxx"
    }

    错误响应:
    {
        "code": 40001,
        "message": "Invalid API Key",
        "data": null,
        "request_id": "uuid-xxx"
    }
    """
    code: int = Field(default=0, description="状态码，0 表示成功")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="请求唯一标识")


def wrap_response(
    data: Any = None,
    code: int = 0,
    message: str = "success",
    request_id: Optional[str] = None
) -> dict:
    """
    包装响应数据为统一格式

    Args:
        data: 响应数据
        code: 状态码，0 表示成功
        message: 响应消息
        request_id: 请求 ID，如果不提供则自动生成

    Returns:
        统一格式的响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data,
        "request_id": request_id or str(uuid.uuid4())
    }


def error_response(
    code: int,
    message: str,
    request_id: Optional[str] = None
) -> dict:
    """
    创建错误响应

    Args:
        code: 错误码
        message: 错误消息
        request_id: 请求 ID

    Returns:
        错误响应字典
    """
    return wrap_response(data=None, code=code, message=message, request_id=request_id)


# 错误码常量
class ErrorCode:
    """错误码定义"""
    # 成功
    SUCCESS = 0

    # 认证/授权错误 (40001-40099)
    MISSING_API_KEY = 40001
    INVALID_API_KEY = 40002
    PERMISSION_DENIED = 40003

    # 参数校验错误 (40100-40199)
    INVALID_PARAMETER = 40100
    MISSING_PARAMETER = 40101
    INVALID_FILE_TYPE = 40102
    FILE_TOO_LARGE = 40103
    INVALID_QUERY_MODE = 40104

    # 资源不存在 (40200-40299)
    DOCUMENT_NOT_FOUND = 40200
    TASK_NOT_FOUND = 40201
    ENTITY_NOT_FOUND = 40202

    # 服务端错误 (50001-50099)
    INTERNAL_ERROR = 50001
    RAG_ERROR = 50002
    STORAGE_ERROR = 50003
    WEBHOOK_ERROR = 50004
    PROCESSING_ERROR = 50005
    SERVICE_UNAVAILABLE = 50301


# 错误消息映射
ERROR_MESSAGES = {
    ErrorCode.SUCCESS: "success",
    ErrorCode.MISSING_API_KEY: "Missing API Key",
    ErrorCode.INVALID_API_KEY: "Invalid API Key",
    ErrorCode.PERMISSION_DENIED: "Permission denied",
    ErrorCode.INVALID_PARAMETER: "Invalid parameter",
    ErrorCode.MISSING_PARAMETER: "Missing required parameter",
    ErrorCode.INVALID_FILE_TYPE: "Invalid file type",
    ErrorCode.FILE_TOO_LARGE: "File too large",
    ErrorCode.INVALID_QUERY_MODE: "Invalid query mode",
    ErrorCode.DOCUMENT_NOT_FOUND: "Document not found",
    ErrorCode.TASK_NOT_FOUND: "Task not found",
    ErrorCode.ENTITY_NOT_FOUND: "Entity not found",
    ErrorCode.INTERNAL_ERROR: "Internal server error",
    ErrorCode.RAG_ERROR: "RAG processing error",
    ErrorCode.STORAGE_ERROR: "Storage error",
    ErrorCode.WEBHOOK_ERROR: "Webhook callback error",
    ErrorCode.PROCESSING_ERROR: "Document processing error",
    ErrorCode.SERVICE_UNAVAILABLE: "Service unavailable",
}
