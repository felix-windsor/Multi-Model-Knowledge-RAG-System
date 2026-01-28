"""Webhook 管理服务（重构版 - 使用 StorageManager）"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

import httpx

from app.storage.base import StorageManager
from app.storage.models import Webhook, WebhookStatus

logger = logging.getLogger(__name__)


class WebhookService:
    """Webhook 管理服务

    This service provides webhook management operations using the storage
    abstraction layer. It supports webhook registration, delivery with
    automatic retries, and failure handling.
    """

    # 默认超时时间（秒）
    DEFAULT_TIMEOUT = 10

    # 重试间隔基数（分钟）
    RETRY_INTERVAL_MINUTES = 5

    def __init__(self, storage: StorageManager) -> None:
        """Initialize webhook service with storage manager.

        Args:
            storage: StorageManager instance for data persistence.
        """
        self.storage = storage

    async def create_webhook(
        self,
        document_id: UUID,
        callback_url: str,
        event_type: str = "document.processed",
    ) -> Webhook:
        """注册 Webhook 回调

        Args:
            document_id: ID of the document to monitor.
            callback_url: URL to call when the event occurs.
            event_type: Type of event to trigger the webhook.

        Returns:
            The created Webhook.
        """
        return await self.storage.webhooks.create(
            document_id=document_id,
            callback_url=callback_url,
            event_type=event_type,
        )

    async def get_webhook(self, webhook_id: UUID) -> Optional[Webhook]:
        """获取 Webhook 信息

        Args:
            webhook_id: Webhook ID.

        Returns:
            The Webhook if found, None otherwise.
        """
        return await self.storage.webhooks.get(webhook_id)

    async def get_webhooks_by_document(
        self,
        document_id: UUID,
    ) -> List[Webhook]:
        """获取文档的所有 Webhook

        Args:
            document_id: Document ID.

        Returns:
            List of Webhook objects for the document.
        """
        return await self.storage.webhooks.get_by_document(document_id)

    async def deliver_webhook(
        self,
        webhook: Webhook,
        payload: Dict[str, Any],
    ) -> bool:
        """发送 Webhook 回调（实际 HTTP 请求）

        Attempts to deliver the webhook payload to the registered URL.
        On success, marks the webhook as delivered. On failure, schedules
        a retry with exponential backoff.

        Args:
            webhook: The Webhook to deliver.
            payload: The payload to send.

        Returns:
            True if delivery was successful, False otherwise.
        """
        try:
            async with httpx.AsyncClient(
                timeout=self.DEFAULT_TIMEOUT
            ) as client:
                response = await client.post(
                    webhook.callback_url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "KnowledgeGraphRAG-Webhook/1.0",
                    },
                )
                response.raise_for_status()

            # 标记为已发送
            await self.storage.webhooks.mark_delivered(webhook.id)
            logger.info(
                f"Webhook delivered successfully to {webhook.callback_url}"
            )
            return True

        except httpx.TimeoutException as e:
            error_msg = f"Timeout: {e}"
            logger.warning(
                f"Webhook timeout for {webhook.callback_url}: {error_msg}"
            )
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
            logger.warning(
                f"Webhook HTTP error for {webhook.callback_url}: {error_msg}"
            )
        except httpx.RequestError as e:
            error_msg = f"Request error: {e}"
            logger.warning(
                f"Webhook request error for {webhook.callback_url}: {error_msg}"
            )
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(
                f"Webhook unexpected error for {webhook.callback_url}: {error_msg}"
            )

        # 标记为失败，计划重试
        retry_after = datetime.now() + timedelta(
            minutes=self.RETRY_INTERVAL_MINUTES * (webhook.retry_count + 1)
        )
        await self.storage.webhooks.mark_failed(
            webhook.id,
            error_msg,
            retry_after,
        )
        return False

    async def deliver_document_event(
        self,
        document_id: UUID,
        event_type: str,
        data: Dict[str, Any],
    ) -> int:
        """发送文档事件到所有注册的 Webhook

        Args:
            document_id: Document ID.
            event_type: Event type (e.g., "document.processed", "document.failed").
            data: Event data payload.

        Returns:
            Number of successfully delivered webhooks.

        Note:
            Webhooks registered for "document.processed" will also receive
            "document.failed" events, since both represent completion of the
            document processing flow.
        """
        webhooks = await self.storage.webhooks.get_by_document(document_id)
        success_count = 0

        for webhook in webhooks:
            # 只发送待发送的 webhook
            if webhook.status != WebhookStatus.PENDING:
                continue

            # Allow failure events to be delivered to webhooks registered for
            # processed events (both are document completion events)
            if webhook.event_type != event_type:
                if not (
                    webhook.event_type == "document.processed"
                    and event_type == "document.failed"
                ):
                    continue

            payload = {
                "event": event_type,
                "document_id": str(document_id),
                "data": data,
                "timestamp": datetime.now().isoformat(),
            }

            # Store payload data with webhook for retry purposes
            await self.storage.webhooks.store_payload(webhook.id, data)

            if await self.deliver_webhook(webhook, payload):
                success_count += 1

        return success_count

    async def retry_failed_webhooks(self) -> int:
        """重试失败的 Webhook

        Retrieves all pending webhooks that are due for retry and
        attempts to deliver them.

        Returns:
            Number of webhooks retried.
        """
        pending = await self.storage.webhooks.list_pending(limit=100)
        retry_count = 0
        now = datetime.now()

        for webhook in pending:
            # 检查是否到了重试时间
            if webhook.next_retry_at and webhook.next_retry_at > now:
                continue

            # 检查是否超过最大重试次数
            if webhook.retry_count >= webhook.max_retries:
                continue

            # Retrieve stored payload data for retry
            stored_payload = await self.storage.webhooks.get_payload(webhook.id)

            # 构造 payload with original data
            payload = {
                "event": webhook.event_type,
                "document_id": str(webhook.document_id),
                "data": stored_payload if stored_payload else {},
                "timestamp": now.isoformat(),
                "retry_attempt": webhook.retry_count + 1,
            }

            await self.deliver_webhook(webhook, payload)
            retry_count += 1

        return retry_count

    async def list_pending_webhooks(self, limit: int = 10) -> List[Webhook]:
        """获取待发送的 Webhook 列表

        Args:
            limit: Maximum number of webhooks to return.

        Returns:
            List of pending Webhook objects.
        """
        return await self.storage.webhooks.list_pending(limit)
