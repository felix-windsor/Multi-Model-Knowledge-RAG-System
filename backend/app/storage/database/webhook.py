"""PostgreSQL webhook storage implementation."""

import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..base import WebhookStorage
from ..models import Webhook, WebhookStatus
from .connection import DatabasePool


class DatabaseWebhookStorage(WebhookStorage):
    """PostgreSQL-based webhook storage.

    This class implements the WebhookStorage interface using PostgreSQL
    as the underlying storage backend. It provides CRUD operations for
    webhook records including delivery tracking and retry scheduling.
    """

    def _row_to_webhook(self, row) -> Webhook:
        """Convert a database row to a Webhook model.

        Args:
            row: An asyncpg Record containing webhook data.

        Returns:
            A Webhook model instance populated from the row data.
        """
        return Webhook(
            id=row["id"],
            document_id=row["document_id"],
            callback_url=row["callback_url"],
            event_type=row["event_type"],
            status=WebhookStatus(row["status"]),
            retry_count=row["retry_count"],
            max_retries=row["max_retries"],
            last_error=row["last_error"],
            next_retry_at=row["next_retry_at"],
            delivered_at=row["delivered_at"],
        )

    async def create(
        self,
        document_id: UUID,
        callback_url: str,
        event_type: str,
    ) -> Webhook:
        """Create a new webhook for document event notification.

        Args:
            document_id: ID of the document to monitor.
            callback_url: URL to call when the event occurs.
            event_type: Type of event to trigger the webhook.

        Returns:
            The created Webhook with generated ID.
        """
        webhook_id = uuid.uuid4()

        async with DatabasePool.connection() as conn:
            await conn.execute(
                """
                INSERT INTO webhooks (id, document_id, callback_url, event_type, status)
                VALUES ($1, $2, $3, $4, $5)
                """,
                webhook_id,
                document_id,
                callback_url,
                event_type,
                WebhookStatus.PENDING.value,
            )

        return Webhook(
            id=webhook_id,
            document_id=document_id,
            callback_url=callback_url,
            event_type=event_type,
            status=WebhookStatus.PENDING,
        )

    async def get(self, webhook_id: UUID) -> Optional[Webhook]:
        """Get a webhook by its ID.

        Args:
            webhook_id: Unique identifier of the webhook.

        Returns:
            The Webhook if found, None otherwise.
        """
        async with DatabasePool.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM webhooks WHERE id = $1",
                webhook_id,
            )

        if not row:
            return None

        return self._row_to_webhook(row)

    async def get_by_document(self, document_id: UUID) -> List[Webhook]:
        """Get all webhooks registered for a document.

        Args:
            document_id: ID of the document.

        Returns:
            List of Webhook objects for the document.
        """
        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM webhooks WHERE document_id = $1",
                document_id,
            )

        return [self._row_to_webhook(row) for row in rows]

    async def list_pending(self, limit: int = 10) -> List[Webhook]:
        """Get pending webhooks ready for delivery.

        Includes webhooks that are pending and those with due retries
        (next_retry_at <= now).

        Args:
            limit: Maximum number of webhooks to return.

        Returns:
            List of pending Webhook objects, ordered by next retry time.
        """
        now = datetime.now()

        async with DatabasePool.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM webhooks
                WHERE status = $1
                  AND (next_retry_at IS NULL OR next_retry_at <= $2)
                ORDER BY next_retry_at ASC NULLS FIRST
                LIMIT $3
                """,
                WebhookStatus.PENDING.value,
                now,
                limit,
            )

        return [self._row_to_webhook(row) for row in rows]

    async def mark_delivered(self, webhook_id: UUID) -> bool:
        """Mark a webhook as successfully delivered.

        Args:
            webhook_id: Unique identifier of the webhook.

        Returns:
            True if successful, False if webhook not found.
        """
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                """
                UPDATE webhooks
                SET status = $1, delivered_at = $2
                WHERE id = $3
                """,
                WebhookStatus.DELIVERED.value,
                datetime.now(),
                webhook_id,
            )

        return result == "UPDATE 1"

    async def mark_failed(
        self,
        webhook_id: UUID,
        error: str,
        retry_after: Optional[datetime] = None,
    ) -> bool:
        """Mark a webhook as failed and optionally schedule retry.

        If the webhook has remaining retries, it will stay pending with
        an incremented retry count and scheduled next retry time.
        Otherwise, it will be marked as permanently failed.

        Args:
            webhook_id: Unique identifier of the webhook.
            error: Error message describing the failure.
            retry_after: Optional datetime for next retry attempt.

        Returns:
            True if successful, False if webhook not found.
        """
        async with DatabasePool.transaction() as conn:
            # Get current retry count and max retries
            row = await conn.fetchrow(
                "SELECT retry_count, max_retries FROM webhooks WHERE id = $1",
                webhook_id,
            )

            if not row:
                return False

            new_retry_count = row["retry_count"] + 1

            if new_retry_count < row["max_retries"]:
                # Retry available: keep pending with next retry time
                await conn.execute(
                    """
                    UPDATE webhooks
                    SET retry_count = $1, last_error = $2, next_retry_at = $3
                    WHERE id = $4
                    """,
                    new_retry_count,
                    error,
                    retry_after,
                    webhook_id,
                )
            else:
                # Max retries reached: mark as permanently failed
                await conn.execute(
                    """
                    UPDATE webhooks
                    SET status = $1, retry_count = $2, last_error = $3
                    WHERE id = $4
                    """,
                    WebhookStatus.FAILED.value,
                    new_retry_count,
                    error,
                    webhook_id,
                )

        return True
