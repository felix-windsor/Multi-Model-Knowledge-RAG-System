"""语义缓存服务 - V2.0

使用 Redis + Sentence Transformers 实现语义相似度缓存
减少重复查询的 LLM API 调用，提升响应速度和降低成本
"""
import os
import json
import hashlib
from typing import Optional, Dict, Any
import redis
from sentence_transformers import SentenceTransformer
import numpy as np


class SemanticCache:
    """语义缓存服务"""

    def __init__(
        self,
        redis_url: str = None,
        model_name: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.92,
        cache_ttl: int = 3600
    ):
        """
        初始化语义缓存

        Args:
            redis_url: Redis 连接 URL
            model_name: Sentence Transformer 模型名称
            similarity_threshold: 相似度阈值（0-1）
            cache_ttl: 缓存过期时间（秒）
        """
        # Redis 连接
        redis_url = redis_url or os.getenv("REDIS_URI", "redis://localhost:6379")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)

        # Sentence Transformer 模型
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        # 配置
        self.similarity_threshold = float(os.getenv("SEMANTIC_CACHE_THRESHOLD", similarity_threshold))
        self.cache_ttl = cache_ttl

        # 缓存键前缀
        self.query_prefix = "semantic_cache:query:"
        self.embedding_prefix = "semantic_cache:embedding:"
        self.index_key = "semantic_cache:index"

        print(f"[Semantic Cache] Initialized with model: {model_name}")
        print(f"[Semantic Cache] Similarity threshold: {self.similarity_threshold}")
        print(f"[Semantic Cache] Embedding dimension: {self.embedding_dim}")

    def _generate_query_hash(self, query: str, mode: str = "hybrid") -> str:
        """生成查询的唯一哈希"""
        content = f"{query}:{mode}"
        return hashlib.md5(content.encode()).hexdigest()

    def _encode_query(self, query: str) -> np.ndarray:
        """将查询编码为向量"""
        return self.model.encode(query, normalize_embeddings=True)

    def _compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """计算两个向量的余弦相似度"""
        return float(np.dot(embedding1, embedding2))

    async def get(self, query: str, mode: str = "hybrid") -> Optional[Dict[str, Any]]:
        """
        从缓存中获取查询结果

        Args:
            query: 查询文本
            mode: 查询模式

        Returns:
            缓存的查询结果，如果没有找到相似查询则返回 None
        """
        try:
            # 编码查询
            query_embedding = self._encode_query(query)

            # 从索引中获取所有缓存的查询哈希
            cached_hashes = self.redis_client.smembers(self.index_key)

            best_similarity = 0.0
            best_match_hash = None

            # 遍历所有缓存的查询，计算相似度
            for cached_hash in cached_hashes:
                # 获取缓存的 embedding
                embedding_key = f"{self.embedding_prefix}{cached_hash}"
                cached_embedding_str = self.redis_client.get(embedding_key)

                if not cached_embedding_str:
                    continue

                # 解析 embedding
                cached_embedding = np.array(json.loads(cached_embedding_str))

                # 计算相似度
                similarity = self._compute_similarity(query_embedding, cached_embedding)

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match_hash = cached_hash

            # 如果找到相似度超过阈值的查询，返回缓存结果
            if best_similarity >= self.similarity_threshold and best_match_hash:
                query_key = f"{self.query_prefix}{best_match_hash}"
                cached_result = self.redis_client.get(query_key)

                if cached_result:
                    result = json.loads(cached_result)
                    result['cache_hit'] = True
                    result['cache_similarity'] = best_similarity

                    print(f"[Semantic Cache] Cache HIT - Similarity: {best_similarity:.4f}")
                    return result

            print(f"[Semantic Cache] Cache MISS - Best similarity: {best_similarity:.4f}")
            return None

        except Exception as e:
            print(f"[Semantic Cache] Error getting from cache: {e}")
            return None

    async def set(
        self,
        query: str,
        mode: str,
        answer: str,
        query_time: float,
        metadata: Dict[str, Any] = None
    ):
        """
        将查询结果存入缓存

        Args:
            query: 查询文本
            mode: 查询模式
            answer: 查询结果
            query_time: 查询耗时
            metadata: 额外的元数据
        """
        try:
            # 生成查询哈希
            query_hash = self._generate_query_hash(query, mode)

            # 编码查询
            query_embedding = self._encode_query(query)

            # 存储查询结果
            result = {
                'query': query,
                'mode': mode,
                'answer': answer,
                'query_time': query_time,
                'metadata': metadata or {},
                'cache_hit': False
            }

            query_key = f"{self.query_prefix}{query_hash}"
            self.redis_client.setex(
                query_key,
                self.cache_ttl,
                json.dumps(result, ensure_ascii=False)
            )

            # 存储 embedding
            embedding_key = f"{self.embedding_prefix}{query_hash}"
            self.redis_client.setex(
                embedding_key,
                self.cache_ttl,
                json.dumps(query_embedding.tolist())
            )

            # 添加到索引
            self.redis_client.sadd(self.index_key, query_hash)

            print(f"[Semantic Cache] Cached query: {query[:50]}...")

        except Exception as e:
            print(f"[Semantic Cache] Error setting cache: {e}")

    async def clear(self):
        """清空所有缓存"""
        try:
            # 获取所有缓存的查询哈希
            cached_hashes = self.redis_client.smembers(self.index_key)

            # 删除所有缓存条目
            for cached_hash in cached_hashes:
                query_key = f"{self.query_prefix}{cached_hash}"
                embedding_key = f"{self.embedding_prefix}{cached_hash}"
                self.redis_client.delete(query_key, embedding_key)

            # 清空索引
            self.redis_client.delete(self.index_key)

            print(f"[Semantic Cache] Cleared {len(cached_hashes)} cache entries")

        except Exception as e:
            print(f"[Semantic Cache] Error clearing cache: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        try:
            cached_count = self.redis_client.scard(self.index_key)

            return {
                'cached_queries': cached_count,
                'similarity_threshold': self.similarity_threshold,
                'cache_ttl': self.cache_ttl,
                'embedding_dim': self.embedding_dim
            }

        except Exception as e:
            print(f"[Semantic Cache] Error getting stats: {e}")
            return {}


# 全局缓存实例（单例模式）
_semantic_cache_instance: Optional[SemanticCache] = None


def get_semantic_cache() -> Optional[SemanticCache]:
    """
    获取语义缓存实例

    Returns:
        SemanticCache 实例，如果未启用则返回 None
    """
    global _semantic_cache_instance

    # 检查是否启用
    enabled = os.getenv("ENABLE_SEMANTIC_CACHE", "false").lower() == "true"
    if not enabled:
        return None

    # 创建单例实例
    if _semantic_cache_instance is None:
        try:
            _semantic_cache_instance = SemanticCache()
        except Exception as e:
            print(f"[Semantic Cache] Failed to initialize: {e}")
            return None

    return _semantic_cache_instance
