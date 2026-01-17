"""统一模型工厂 - 支持 LLM/Vision/Embedding/Rerank 独立配置"""
import os
import numpy as np
from typing import Callable, Tuple, Optional, List
from pathlib import Path
from dotenv import load_dotenv
import httpx

# 加载项目根目录的 .env 文件
ROOT_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env", override=True)

from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.llm.ollama import ollama_model_complete
from lightrag.utils import EmbeddingFunc


import asyncio
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Thread pool for synchronous HTTP requests to Ollama
_ollama_executor = ThreadPoolExecutor(max_workers=1)


def _sync_ollama_embed_single(text: str, embed_model: str, host: str, max_retries: int = 5) -> List[float]:
    """
    Synchronous function to get embedding for a single text.
    Uses requests library which is more stable with Ollama on Windows.
    """
    base_delay = 0.5

    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{host}/api/embeddings",
                json={"model": embed_model, "prompt": text},
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            return data["embedding"]
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 502 and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"INFO: Ollama 502 error, retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
            else:
                print(f"ERROR: Ollama embedding failed: {str(e)}")
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"INFO: Ollama error, retrying in {delay}s (attempt {attempt + 1}/{max_retries}): {str(e)}")
                time.sleep(delay)
            else:
                print(f"ERROR: Ollama embedding failed: {str(e)}")
                raise

    raise RuntimeError("Max retries exceeded for Ollama embedding")


def _sync_ollama_embed_batch(texts: List[str], embed_model: str, host: str) -> List[List[float]]:
    """
    Synchronous batch embedding function.
    """
    embeddings = []
    for text in texts:
        embedding = _sync_ollama_embed_single(text, embed_model, host)
        embeddings.append(embedding)
    return embeddings


async def custom_ollama_embed(texts: List[str], embed_model: str, host: str) -> np.ndarray:
    """
    Custom Ollama embedding function using synchronous requests in a thread pool.
    This avoids the async/Ollama compatibility issues on Windows.
    """
    loop = asyncio.get_event_loop()
    embeddings = await loop.run_in_executor(
        _ollama_executor,
        _sync_ollama_embed_batch,
        texts,
        embed_model,
        host
    )
    return np.array(embeddings)


class ModelFactory:
    """统一模型工厂 - 支持多种模型类型的独立配置"""

    @staticmethod
    def create_llm_function(
        provider: str,
        model: str,
        api_key: str,
        base_url: str
    ) -> Callable:
        """
        创建 LLM 函数
        
        Args:
            provider: 提供商 (openai, qwen, ollama, lmstudio)
            model: 模型名称
            api_key: API Key
            base_url: Base URL
            
        Returns:
            LLM 函数
        """
        if provider == "openai" or provider == "qwen" or provider == "lmstudio":
            async def llm_func(prompt, system_prompt=None, history_messages=[], **kwargs):
                return await openai_complete_if_cache(
                    model,
                    prompt,
                    system_prompt=system_prompt,
                    history_messages=history_messages,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            return llm_func
        elif provider == "ollama":
            # Ollama 使用 host 而不是 base_url
            host = base_url.replace("/v1", "") if base_url.endswith("/v1") else base_url
            async def llm_func(prompt, system_prompt=None, history_messages=[], **kwargs):
                return await ollama_model_complete(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    history_messages=history_messages,
                    model=model,
                    host=host,
                    **kwargs
                )
            return llm_func
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def create_vision_function(
        provider: str,
        model: str,
        api_key: str,
        base_url: str,
        fallback_llm_func: Optional[Callable] = None
    ) -> Callable:
        """
        创建 Vision 函数
        
        Args:
            provider: 提供商 (openai, qwen, ollama, lmstudio)
            model: 模型名称
            api_key: API Key
            base_url: Base URL
            fallback_llm_func: 回退的 LLM 函数（用于纯文本）
            
        Returns:
            Vision 函数
        """
        if provider == "openai" or provider == "qwen" or provider == "lmstudio":
            async def vision_func(prompt, image_data=None, messages=None, **kwargs):
                system_prompt = kwargs.pop("system_prompt", None)
                
                if messages:
                    return await openai_complete_if_cache(
                        model,
                        "",
                        messages=messages,
                        api_key=api_key,
                        base_url=base_url,
                        **kwargs
                    )
                elif image_data:
                    msg_list = []
                    if system_prompt:
                        msg_list.append({"role": "system", "content": system_prompt})
                    
                    msg_list.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    })
                    
                    return await openai_complete_if_cache(
                        model,
                        "",
                        messages=msg_list,
                        api_key=api_key,
                        base_url=base_url,
                        **kwargs
                    )
                else:
                    # 纯文本，回退到 LLM
                    if fallback_llm_func:
                        return await fallback_llm_func(prompt, system_prompt=system_prompt, **kwargs)
                    else:
                        return await openai_complete_if_cache(
                            model,
                            prompt,
                            system_prompt=system_prompt,
                            api_key=api_key,
                            base_url=base_url,
                            **kwargs
                        )
            return vision_func
        elif provider == "ollama":
            host = base_url.replace("/v1", "") if base_url.endswith("/v1") else base_url
            async def vision_func(prompt, image_data=None, messages=None, **kwargs):
                system_prompt = kwargs.pop("system_prompt", None)
                
                if image_data:
                    # Ollama 的图片处理方式
                    combined_prompt = f"{prompt}\n[Image: data:image/jpeg;base64,{image_data}]"
                    return await ollama_model_complete(
                        prompt=combined_prompt,
                        system_prompt=system_prompt,
                        model=model,
                        host=host,
                        **kwargs
                    )
                else:
                    # 纯文本，回退到 LLM
                    if fallback_llm_func:
                        return await fallback_llm_func(prompt, system_prompt=system_prompt, **kwargs)
                    else:
                        return await ollama_model_complete(
                            prompt=prompt,
                            system_prompt=system_prompt,
                            model=model,
                            host=host,
                            **kwargs
                        )
            return vision_func
        else:
            raise ValueError(f"Unsupported Vision provider: {provider}")

    @staticmethod
    def create_embedding_function(
        provider: str,
        model: str,
        api_key: str,
        base_url: str,
        embedding_dim: int = 1536
    ) -> EmbeddingFunc:
        """
        创建 Embedding 函数
        
        Args:
            provider: 提供商 (openai, qwen, ollama, lmstudio)
            model: 模型名称
            api_key: API Key
            base_url: Base URL
            embedding_dim: 向量维度
            
        Returns:
            EmbeddingFunc
        """
        if provider == "openai" or provider == "qwen" or provider == "lmstudio":
            async def openai_embed_func(texts):
                return await openai_embed(
                    texts,
                    model=model,
                    api_key=api_key,
                    base_url=base_url
                )
            embedding_func = EmbeddingFunc(
                embedding_dim=embedding_dim,
                max_token_size=8192,
                func=openai_embed_func
            )
            return embedding_func
        elif provider == "ollama":
            host = base_url.replace("/v1", "") if base_url.endswith("/v1") else base_url
            async def ollama_embed_func(texts):
                return await custom_ollama_embed(
                    texts,
                    embed_model=model,
                    host=host
                )
            embedding_func = EmbeddingFunc(
                embedding_dim=embedding_dim,
                max_token_size=8192,
                func=ollama_embed_func
            )
            return embedding_func
        else:
            raise ValueError(f"Unsupported Embedding provider: {provider}")

    @staticmethod
    def create_rerank_function(
        provider: str,
        model: str,
        api_key: str,
        base_url: str
    ) -> Optional[Callable]:
        """
        创建 Rerank 函数（可选）
        
        Args:
            provider: 提供商 (openai, ollama)
            model: 模型名称
            api_key: API Key
            base_url: Base URL
            
        Returns:
            Rerank 函数或 None
        """
        if not provider:
            return None
            
        # 目前 LightRAG 的 rerank 支持有限，这里先返回 None
        # 未来可以扩展支持
        return None


class LLMFactory:
    """LLM 工厂 - 向后兼容的包装类"""

    @staticmethod
    async def create_llm_functions(
        provider: str = "openai"
    ) -> Tuple[Callable, EmbeddingFunc, Callable]:
        """
        创建 LLM 函数（向后兼容方法）

        Args:
            provider: LLM 提供商 (openai, qwen, ollama, lmstudio)

        Returns:
            (llm_func, embedding_func, vision_func)
        """
        if provider == "openai":
            return LLMFactory._create_openai()
        elif provider == "qwen":
            return LLMFactory._create_qwen()
        elif provider == "ollama":
            return LLMFactory._create_ollama()
        elif provider == "lmstudio":
            return LLMFactory._create_lmstudio()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    # ============================================
    # 向后兼容的旧方法（保留）
    # ============================================
    
    @staticmethod
    def _create_openai():
        """创建 OpenAI 函数"""
        api_key = os.getenv("LLM_API_KEY")
        base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("LLM_MODEL", "gpt-4o")
        vision_model = os.getenv("VISION_MODEL", model)  # 默认使用主模型

        async def llm_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return await openai_complete_if_cache(
                model,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=api_key,
                base_url=base_url,
                **kwargs
            )

        async def vision_func(prompt, image_data=None, messages=None, **kwargs):
            """Vision 模型函数"""
            system_prompt = kwargs.pop("system_prompt", None)

            if messages:
                # 直接使用提供的 messages
                return await openai_complete_if_cache(
                    vision_model,
                    "",
                    messages=messages,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            elif image_data:
                # 构建包含图片的 messages
                msg_list = []
                if system_prompt:
                    msg_list.append({"role": "system", "content": system_prompt})

                msg_list.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                })

                return await openai_complete_if_cache(
                    vision_model,
                    "",
                    messages=msg_list,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            else:
                # 纯文本，回退到普通 LLM
                return await llm_func(prompt, system_prompt=system_prompt, **kwargs)

        # Embedding 函数
        embed_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
        async def openai_embed_func(texts):
            return await openai_embed(
                texts,
                model=embed_model,
                api_key=api_key,
                base_url=base_url
            )
        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "3072")),
            max_token_size=8192,
            func=openai_embed_func
        )

        return llm_func, embedding_func, vision_func

    @staticmethod
    def _create_qwen():
        """创建 Qwen 函数（OpenAI 兼容 API）"""
        api_key = os.getenv("LLM_API_KEY")
        base_url = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        model = os.getenv("LLM_MODEL", "qwen-turbo")

        async def llm_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return await openai_complete_if_cache(
                model,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=api_key,
                base_url=base_url,
                **kwargs
            )

        async def vision_func(prompt, image_data=None, messages=None, **kwargs):
            """Qwen Vision 模型"""
            system_prompt = kwargs.pop("system_prompt", None)
            vision_model = os.getenv("VISION_MODEL", "qwen-vl-plus")

            if messages:
                return await openai_complete_if_cache(
                    vision_model,
                    "",
                    messages=messages,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            elif image_data:
                msg_list = []
                if system_prompt:
                    msg_list.append({"role": "system", "content": system_prompt})

                msg_list.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                })

                return await openai_complete_if_cache(
                    vision_model,
                    "",
                    messages=msg_list,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            else:
                return await llm_func(prompt, system_prompt=system_prompt, **kwargs)

        # Qwen Embedding
        embed_model = os.getenv("EMBEDDING_MODEL", "text-embedding-v1")
        async def qwen_embed_func(texts):
            return await openai_embed(
                texts,
                model=embed_model,
                api_key=api_key,
                base_url=base_url
            )
        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "1536")),
            max_token_size=8192,
            func=qwen_embed_func
        )

        return llm_func, embedding_func, vision_func

    @staticmethod
    def _create_ollama():
        """创建 Ollama 函数（本地部署）"""
        host = os.getenv("LLM_BASE_URL", "http://localhost:11434")
        model = os.getenv("LLM_MODEL", "qwen2.5:14b")
        embed_model = os.getenv("EMBEDDING_MODEL", "bge-m3:latest")

        async def llm_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return await ollama_model_complete(
                prompt=prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                model=model,
                host=host,
                **kwargs
            )

        async def vision_func(prompt, image_data=None, messages=None, **kwargs):
            """Ollama Vision 模型 (如 llava)"""
            vision_model = os.getenv("VISION_MODEL", "llava:latest")
            system_prompt = kwargs.pop("system_prompt", None)

            # Ollama 的 vision 模型处理方式
            # 注意：Ollama 的图片处理可能需要不同的格式
            if image_data:
                # 对于 Ollama，可能需要直接传递 base64 图片
                combined_prompt = f"{prompt}\n[Image: data:image/jpeg;base64,{image_data}]"
                return await ollama_model_complete(
                    prompt=combined_prompt,
                    system_prompt=system_prompt,
                    model=vision_model,
                    host=host,
                    **kwargs
                )
            else:
                return await llm_func(prompt, system_prompt=system_prompt, **kwargs)

        # Ollama Embedding
        async def ollama_embed_func(texts):
            return await custom_ollama_embed(
                texts,
                embed_model=embed_model,
                host=host
            )
        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "1024")),
            max_token_size=8192,
            func=ollama_embed_func
        )

        return llm_func, embedding_func, vision_func

    @staticmethod
    def _create_lmstudio():
        """创建 LM Studio 函数（OpenAI 兼容 API）"""
        api_key = os.getenv("LLM_API_KEY", "lm-studio")
        base_url = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
        model = os.getenv("LLM_MODEL", "local-model")

        async def llm_func(prompt, system_prompt=None, history_messages=[], **kwargs):
            return await openai_complete_if_cache(
                model,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=api_key,
                base_url=base_url,
                **kwargs
            )

        async def vision_func(prompt, image_data=None, messages=None, **kwargs):
            """LM Studio Vision (如果支持)"""
            # LM Studio 使用 OpenAI 兼容格式
            system_prompt = kwargs.pop("system_prompt", None)

            if messages:
                return await openai_complete_if_cache(
                    model,
                    "",
                    messages=messages,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            elif image_data:
                msg_list = []
                if system_prompt:
                    msg_list.append({"role": "system", "content": system_prompt})

                msg_list.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                })

                return await openai_complete_if_cache(
                    model,
                    "",
                    messages=msg_list,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            else:
                return await llm_func(prompt, system_prompt=system_prompt, **kwargs)

        # LM Studio Embedding
        embed_model = os.getenv("EMBEDDING_MODEL", "local-embed-model")

        async def lmstudio_embed_func(texts):
            return await openai_embed(
                texts,
                model=embed_model,
                api_key=api_key,
                base_url=base_url
            )
        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "1536")),
            max_token_size=8192,
            func=lmstudio_embed_func
        )

        return llm_func, embedding_func, vision_func
