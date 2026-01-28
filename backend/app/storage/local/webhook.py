"""Local file-based webhook storage implementation."""

import copy
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..base import WebhookStorage
from ..models import Webhook, WebhookStatus


class LocalWebhookStorage(WebhookStorage):
    """Local JSON file-based webhook storage.

    This implementation stores webhook metadata in a JSON file,
    suitable for development and single-instance deployments.
    For production with multiple instances, use the database backend.
    """

    def __init__(self, storage_dir: str = "data/storage") -> None:
        """Initialize local webhook storage.

        Args:
            storage_dir: Directory path for storing the JSON data file.
        """
        self.storage_dir = Path(storage_dir)
        self.webhooks_file = self.storage_dir / "webhooks.json"
        self._tx_snapshot: Optional[Dict[str, dict]] = None
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Ensure storage directory and file exist."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.webhooks_file.exists():
            self._save_webhooks({})

    def _load_webhooks(self) -> dict:
        """Load webhooks from JSON file.

        Returns:
            Dictionary of webhook data keyed by webhook ID.
        """
        try:
            with open(self.webhooks_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_webhooks(self, webhooks: dict) -> None:
        """Save webhooks to JSON file.

        Args:
            webhooks: Dictionary of webhook data to persist.
        """
        with open(self.webhooks_file, "w", encoding="utf-8") as f:
            json.dump(webhooks, f, indent=2, default=str)

    def _webhook_from_dict(self, data: dict) -> Webhook:
        """Convert dictionary data to Webhook model.

        Args:
            data: Dictionary containing webhook data.

        Returns:
            Webhook model instance.
        """
        return Webhook(
            id=UUID(data["id"]),
            document_id=UUID(data["document_id"]),
            callback_url=data["callback_url"],
            event_type=data.get("event_type"),
            status=WebhookStatus(data["status"]),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            last_error=data.get("last_error"),
            payload_data=data.get("payload_data"),
            next_retry_at=(
                datetime.fromisoformat(data["next_retry_at"])
                if data.get("next_retry_at")
                else None
            ),
            delivered_at=(
                datetime.fromisoformat(data["delivered_at"])
                if data.get("delivered_at")
                else None
            ),
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
        webhooks = self._load_webhooks()

        webhook_id = uuid.uuid4()

        webhook_data = {
            "id": str(webhook_id),
            "document_id": str(document_id),
            "callback_url": callback_url,
            "event_type": event_type,
            "status": WebhookStatus.PENDING.value,
            "retry_count": 0,
            "max_retries": 3,
            "last_error": None,
            "payload_data": None,
            "next_retry_at": None,
            "delivered_at": None,
        }

        webhooks[str(webhook_id)] = webhook_data
        self._save_webhooks(webhooks)

        return Webhook(
            id=webhook_id,
            document_id=document_id,
            callback_url=callback_url,
            event_type=event_type,
            status=WebhookStatus.PENDING,
            retry_count=0,
            max_retries=3,
        )

    async def get(self, webhook_id: UUID) -> Optional[Webhook]:
        """Get webhook by ID.

        Args:
            webhook_id: Unique identifier of the webhook.

        Returns:
            The Webhook if found, None otherwise.
        """
        webhooks = self._load_webhooks()
        webhook_data = webhooks.get(str(webhook_id))

        if not webhook_data:
            return None

        return self._webhook_from_dict(webhook_data)

    async def get_by_document(self, document_id: UUID) -> List[Webhook]:
        """Get all webhooks registered for a document.

        Args:
            document_id: ID of the document.

        Returns:
            List of Webhook objects for the document.
        """
        webhooks = self._load_webhooks()
        doc_id_str = str(document_id)

        return [
            self._webhook_from_dict(data)
            for data in webhooks.values()
            if data["document_id"] == doc_id_str
        ]

    async def list_pending(self, limit: int = 10) -> List[Webhook]:
        """Get pending webhooks ready for delivery.

        Includes webhooks that are pending and those with due retries
        (next_retry_at <= now).

        Args:
            limit: Maximum number of webhooks to return.

        Returns:
            List of pending Webhook objects.
        """
        webhooks = self._load_webhooks()
        now = datetime.now()

        result = []
        for data in webhooks.values():
            if data["status"] != WebhookStatus.PENDING.value:
                continue

            # Check if retry is due (skip if scheduled for future)
            if data.get("next_retry_at"):
                retry_at = datetime.fromisoformat(data["next_retry_at"])
                if retry_at > now:
                    continue

            result.append(self._webhook_from_dict(data))

        return result[:limit]

    async def mark_delivered(self, webhook_id: UUID) -> bool:
        """Mark a webhook as successfully delivered.

        Args:
            webhook_id: Unique identifier of the webhook.

        Returns:
            True if successful, False if webhook not found.
        """
        webhooks = self._load_webhooks()
        webhook_key = str(webhook_id)

        if webhook_key not in webhooks:
            return False

        webhooks[webhook_key]["status"] = WebhookStatus.DELIVERED.value
        webhooks[webhook_key]["delivered_at"] = datetime.now().isoformat()

        self._save_webhooks(webhooks)
        return True

    async def mark_failed(
        self,
        webhook_id: UUID,
        error: str,
        retry_after: Optional[datetime] = None,
    ) -> bool:
        """Mark a webhook as failed and optionally schedule retry.

        Args:
            webhook_id: Unique identifier of the webhook.
            error: Error message describing the failure.
            retry_after: Optional datetime for next retry attempt.

        Returns:
            True if successful, False if webhook not found.
        """
        webhooks = self._load_webhooks()
        webhook_key = str(webhook_id)

        if webhook_key not in webhooks:
            return False

        webhook = webhooks[webhook_key]
        webhook["retry_count"] = webhook.get("retry_count", 0) + 1
        webhook["last_error"] = error

        # Check if we should retry
        if webhook["retry_count"] < webhook.get("max_retries", 3):
            webhook["status"] = WebhookStatus.PENDING.value
            webhook["next_retry_at"] = (
                retry_after.isoformat() if retry_after else None
            )
        else:
            webhook["status"] = WebhookStatus.FAILED.value

        self._save_webhooks(webhooks)
        return True

    async def store_payload(
        self,
        webhook_id: UUID,
        data: Dict[str, Any],
    ) -> bool:
        """Store payload data with the webhook for retry purposes.

        Args:
            webhook_id: Unique identifier of the webhook.
            data: Payload data to store.

        Returns:
            True if successful, False if webhook not found.
        """
        webhooks = self._load_webhooks()
        webhook_key = str(webhook_id)

        if webhook_key not in webhooks:
            return False

        webhooks[webhook_key]["payload_data"] = data
        self._save_webhooks(webhooks)
        return True

    async def get_payload(self, webhook_id: UUID) -> Optional[Dict[str, Any]]:
        """Retrieve stored payload data for a webhook.

        Args:
            webhook_id: Unique identifier of the webhook.

        Returns:
            Stored payload data if found, None otherwise.
        """
        webhooks = self._load_webhooks()
        webhook_data = webhooks.get(str(webhook_id))

        if not webhook_data:
            return None

        return webhook_data.get("payload_data")

    async def delete_by_document(self, document_id: UUID) -> int:
        """Delete all webhooks for a document.

        Args:
            document_id: ID of the document.

        Returns:
            Number of webhooks deleted.
        """
        webhooks = self._load_webhooks()
        doc_id_str = str(document_id)

        to_delete = [
            webhook_id
            for webhook_id, data in webhooks.items()
            if data["document_id"] == doc_id_str
        ]

        for webhook_id in to_delete:
            del webhooks[webhook_id]

        self._save_webhooks(webhooks)
        return len(to_delete)

    async def begin_transaction(self) -> None:
        """Create a snapshot of current state for potential rollback."""
        self._tx_snapshot = copy.deepcopy(self._load_webhooks())

    async def commit_transaction(self) -> None:
        """Commit changes by clearing the snapshot.

        Changes are already persisted to disk during individual operations,
        so commit just clears the rollback snapshot.
        """
        self._tx_snapshot = None

    async def rollback_transaction(self) -> None:
        """Rollback to snapshot state by restoring from the saved snapshot."""
        if self._tx_snapshot is not None:
            self._save_webhooks(self._tx_snapshot)
            self._tx_snapshot = None
