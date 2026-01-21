"""Webhook 回调服务"""
import asyncio
import httpx
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class WebhookService:
    """Webhook 回调服务"""

    # 默认超时时间（秒）
    DEFAULT_TIMEOUT = 30

    # 最大重试次数
    MAX_RETRIES = 3

    # 重试间隔（秒）
    RETRY_DELAY = 5

    @staticmethod
    async def send_webhook(
        callback_url: str,
        event: str,
        data: Dict[str, Any],
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = MAX_RETRIES
    ) -> bool:
        """
        发送 Webhook 回调

        Args:
            callback_url: 回调 URL
            event: 事件类型 (如 document.completed, document.failed)
            data: 事件数据
            timeout: 超时时间（秒）
            retries: 重试次数

        Returns:
            是否成功发送
        """
        if not callback_url:
            return False

        payload = {
            "event": event,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

        for attempt in range(retries + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(
                        callback_url,
                        json=payload,
                        headers={
                            "Content-Type": "application/json",
                            "User-Agent": "KnowledgeGraphRAG-Webhook/1.0"
                        }
                    )

                    if response.status_code in [200, 201, 202, 204]:
                        logger.info(f"Webhook sent successfully to {callback_url}: {event}")
                        return True
                    else:
                        logger.warning(
                            f"Webhook failed with status {response.status_code}: {callback_url}"
                        )

            except httpx.TimeoutException:
                logger.warning(f"Webhook timeout (attempt {attempt + 1}/{retries + 1}): {callback_url}")
            except httpx.RequestError as e:
                logger.warning(f"Webhook request error (attempt {attempt + 1}/{retries + 1}): {e}")
            except Exception as e:
                logger.error(f"Webhook unexpected error: {e}")
                return False

            # 如果不是最后一次尝试，等待后重试
            if attempt < retries:
                await asyncio.sleep(WebhookService.RETRY_DELAY)

        logger.error(f"Webhook failed after {retries + 1} attempts: {callback_url}")
        return False

    @staticmethod
    async def notify_document_completed(
        callback_url: str,
        doc_id: str,
        task_id: str,
        entities_count: int = 0,
        relations_count: int = 0
    ) -> bool:
        """
        通知文档处理完成

        Args:
            callback_url: 回调 URL
            doc_id: 文档 ID
            task_id: 任务 ID
            entities_count: 实体数量
            relations_count: 关系数量

        Returns:
            是否成功发送
        """
        return await WebhookService.send_webhook(
            callback_url=callback_url,
            event="document.completed",
            data={
                "doc_id": doc_id,
                "task_id": task_id,
                "status": "completed",
                "entities_count": entities_count,
                "relations_count": relations_count
            }
        )

    @staticmethod
    async def notify_document_failed(
        callback_url: str,
        doc_id: str,
        task_id: str,
        error_message: str
    ) -> bool:
        """
        通知文档处理失败

        Args:
            callback_url: 回调 URL
            doc_id: 文档 ID
            task_id: 任务 ID
            error_message: 错误信息

        Returns:
            是否成功发送
        """
        return await WebhookService.send_webhook(
            callback_url=callback_url,
            event="document.failed",
            data={
                "doc_id": doc_id,
                "task_id": task_id,
                "status": "failed",
                "error_message": error_message
            }
        )

    @staticmethod
    async def notify_document_progress(
        callback_url: str,
        doc_id: str,
        task_id: str,
        progress: int,
        step: str
    ) -> bool:
        """
        通知文档处理进度

        Args:
            callback_url: 回调 URL
            doc_id: 文档 ID
            task_id: 任务 ID
            progress: 进度 (0-100)
            step: 当前步骤

        Returns:
            是否成功发送
        """
        return await WebhookService.send_webhook(
            callback_url=callback_url,
            event="document.progress",
            data={
                "doc_id": doc_id,
                "task_id": task_id,
                "status": "processing",
                "progress": progress,
                "step": step
            }
        )
