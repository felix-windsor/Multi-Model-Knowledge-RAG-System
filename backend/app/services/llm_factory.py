"""LLM 多模型适配工厂"""
import os
from typing import Callable, Tuple
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc


class LLMFactory:
    """LLM 工厂 - 支持多模型提供商"""

    @staticmethod
    async def create_llm_functions(
        provider: str = "openai"
    ) -> Tuple[Callable, EmbeddingFunc, Callable]:
        """
        创建 LLM 函数

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

    @staticmethod
    def _create_openai():
        """创建 OpenAI 函数"""
        api_key = os.getenv("LLM_API_KEY")
        base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("LLM_MODEL", "gpt-4o")

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
                    "gpt-4o",
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
                    "gpt-4o",
                    "",
                    messages=msg_list,
                    api_key=api_key,
                    base_url=base_url,
                    **kwargs
                )
            else:
                # 纯文本，回退到普通 LLM
                return await llm_func(prompt, system_prompt=system_prompt, **kwargs)

        # Embedding 函数 - 直接使用 openai_embed 的底层函数避免双重包装
        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "3072")),
            max_token_size=8192,
            func=lambda texts: openai_embed.func(
                texts,
                model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
                api_key=api_key,
                base_url=base_url
            )
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

        # Qwen Embedding - 直接使用 openai_embed 的底层函数避免双重包装
        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "1536")),
            max_token_size=8192,
            func=lambda texts: openai_embed.func(
                texts,
                model=os.getenv("EMBEDDING_MODEL", "text-embedding-v1"),
                api_key=api_key,
                base_url=base_url
            )
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

        # Ollama Embedding - 直接使用 ollama_embed 的底层函数避免双重包装
        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "1024")),
            max_token_size=8192,
            func=lambda texts: ollama_embed.func(
                texts,
                embed_model=embed_model,
                host=host
            )
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

        # LM Studio Embedding - 直接使用 openai_embed 的底层函数避免双重包装
        embed_model = os.getenv("EMBEDDING_MODEL", "local-embed-model")

        embedding_func = EmbeddingFunc(
            embedding_dim=int(os.getenv("EMBEDDING_DIM", "1536")),
            max_token_size=8192,
            func=lambda texts: openai_embed.func(
                texts,
                model=embed_model,
                api_key=api_key,
                base_url=base_url
            )
        )

        return llm_func, embedding_func, vision_func
