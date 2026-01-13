"""HTTP 客户端连接池管理 - V2.0

使用 httpx 实现 HTTP/2 连接池，优化 LLM API 调用性能
"""
import os
from typing import Dict, Optional
import httpx
from contextlib import asynccontextmanager


class HTTPClientPool:
    """HTTP 客户端连接池管理器"""

    def __init__(self):
        """初始化连接池"""
        self._clients: Dict[str, httpx.AsyncClient] = {}
        self._default_timeout = float(os.getenv("HTTP_TIMEOUT", "30.0"))
        self._max_keepalive = int(os.getenv("HTTP_MAX_KEEPALIVE", "20"))
        self._max_connections = int(os.getenv("HTTP_MAX_CONNECTIONS", "100"))

        print(f"[HTTP Client Pool] Initialized")
        print(f"[HTTP Client Pool] Timeout: {self._default_timeout}s")
        print(f"[HTTP Client Pool] Max keepalive connections: {self._max_keepalive}")
        print(f"[HTTP Client Pool] Max total connections: {self._max_connections}")

    def get_client(
        self,
        base_url: str,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.AsyncClient:
        """
        获取或创建 HTTP 客户端

        Args:
            base_url: API 基础 URL
            timeout: 请求超时时间（秒）
            headers: 默认请求头

        Returns:
            httpx.AsyncClient 实例
        """
        # 使用 base_url 作为缓存键
        cache_key = base_url

        if cache_key not in self._clients:
            # 创建新的客户端
            timeout_config = timeout or self._default_timeout

            client = httpx.AsyncClient(
                base_url=base_url,
                timeout=httpx.Timeout(timeout_config),
                limits=httpx.Limits(
                    max_keepalive_connections=self._max_keepalive,
                    max_connections=self._max_connections,
                    keepalive_expiry=30.0  # Keep connections alive for 30s
                ),
                http2=True,  # 启用 HTTP/2
                headers=headers or {},
                follow_redirects=True
            )

            self._clients[cache_key] = client
            print(f"[HTTP Client Pool] Created new client for: {base_url}")

        return self._clients[cache_key]

    async def close_all(self):
        """关闭所有客户端连接"""
        for base_url, client in self._clients.items():
            await client.aclose()
            print(f"[HTTP Client Pool] Closed client for: {base_url}")

        self._clients.clear()

    async def close_client(self, base_url: str):
        """关闭指定的客户端连接"""
        if base_url in self._clients:
            await self._clients[base_url].aclose()
            del self._clients[base_url]
            print(f"[HTTP Client Pool] Closed client for: {base_url}")

    def get_stats(self) -> Dict[str, any]:
        """获取连接池统计信息"""
        return {
            'active_clients': len(self._clients),
            'base_urls': list(self._clients.keys()),
            'max_keepalive': self._max_keepalive,
            'max_connections': self._max_connections,
            'default_timeout': self._default_timeout
        }


# 全局连接池实例（单例模式）
_http_client_pool: Optional[HTTPClientPool] = None


def get_http_client_pool() -> HTTPClientPool:
    """
    获取 HTTP 客户端连接池实例

    Returns:
        HTTPClientPool 单例实例
    """
    global _http_client_pool

    if _http_client_pool is None:
        _http_client_pool = HTTPClientPool()

    return _http_client_pool


@asynccontextmanager
async def http_client(
    base_url: str,
    timeout: Optional[float] = None,
    headers: Optional[Dict[str, str]] = None
):
    """
    上下文管理器：获取 HTTP 客户端

    使用示例:
        async with http_client("https://api.openai.com/v1") as client:
            response = await client.post("/chat/completions", json=data)

    Args:
        base_url: API 基础 URL
        timeout: 请求超时时间（秒）
        headers: 默认请求头

    Yields:
        httpx.AsyncClient 实例
    """
    pool = get_http_client_pool()
    client = pool.get_client(base_url, timeout, headers)

    try:
        yield client
    finally:
        # 连接会保持在池中，不需要关闭
        pass


async def cleanup_http_clients():
    """清理所有 HTTP 客户端（应用关闭时调用）"""
    global _http_client_pool

    if _http_client_pool is not None:
        await _http_client_pool.close_all()
        _http_client_pool = None
        print("[HTTP Client Pool] All clients closed")
