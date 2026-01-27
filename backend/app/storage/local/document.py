"""Local file-based document storage implementation."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from ..base import DocumentStorage
from ..models import Document, DocumentStatus


class LocalDocumentStorage(DocumentStorage):
    """Local JSON file-based document storage.

    This implementation stores document metadata in a JSON file,
    suitable for development and single-instance deployments.
    For production with multiple instances, use the database backend.
    """

    def __init__(self, storage_dir: str = "data/storage") -> None:
        """Initialize local document storage.

        Args:
            storage_dir: Directory path for storing the JSON data file.
        """
        self.storage_dir = Path(storage_dir)
        self.documents_file = self.storage_dir / "documents.json"
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Ensure storage directory and file exist."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if not self.documents_file.exists():
            self._save_documents({})

    def _load_documents(self) -> dict:
        """Load documents from JSON file.

        Returns:
            Dictionary of document data keyed by document ID.
        """
        try:
            with open(self.documents_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_documents(self, documents: dict) -> None:
        """Save documents to JSON file.

        Args:
            documents: Dictionary of document data to persist.
        """
        with open(self.documents_file, "w", encoding="utf-8") as f:
            json.dump(documents, f, indent=2, default=str)

    async def create(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str,
    ) -> Document:
        """Create a new document record.

        Args:
            filename: Original name of the uploaded file.
            file_path: Path where the file is stored.
            file_size: Size of the file in bytes.
            mime_type: MIME type of the file.

        Returns:
            The created Document with generated ID and timestamps.
        """
        documents = self._load_documents()

        doc_id = uuid.uuid4()
        now = datetime.now()

        doc_data = {
            "id": str(doc_id),
            "filename": filename,
            "file_path": file_path,
            "file_size": file_size,
            "mime_type": mime_type,
            "status": DocumentStatus.PENDING.value,
            "error_message": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }

        documents[str(doc_id)] = doc_data
        self._save_documents(documents)

        return Document(
            id=doc_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            status=DocumentStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

    async def get(self, doc_id: UUID) -> Optional[Document]:
        """Get document by ID.

        Args:
            doc_id: Unique identifier of the document.

        Returns:
            The Document if found, None otherwise.
        """
        documents = self._load_documents()
        doc_data = documents.get(str(doc_id))

        if not doc_data:
            return None

        return Document(
            id=UUID(doc_data["id"]),
            filename=doc_data["filename"],
            file_path=doc_data.get("file_path"),
            file_size=doc_data.get("file_size"),
            mime_type=doc_data.get("mime_type"),
            status=DocumentStatus(doc_data["status"]),
            error_message=doc_data.get("error_message"),
            created_at=datetime.fromisoformat(doc_data["created_at"]),
            updated_at=datetime.fromisoformat(doc_data["updated_at"]),
        )

    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Document]:
        """List documents with optional filtering and pagination.

        Args:
            status: Filter by document status (e.g., "pending", "completed").
            limit: Maximum number of documents to return.
            offset: Number of documents to skip for pagination.

        Returns:
            List of Document objects matching the criteria, sorted by
            created_at descending (newest first).
        """
        documents = self._load_documents()

        result = []
        for doc_data in documents.values():
            if status and doc_data["status"] != status:
                continue

            result.append(
                Document(
                    id=UUID(doc_data["id"]),
                    filename=doc_data["filename"],
                    file_path=doc_data.get("file_path"),
                    file_size=doc_data.get("file_size"),
                    mime_type=doc_data.get("mime_type"),
                    status=DocumentStatus(doc_data["status"]),
                    error_message=doc_data.get("error_message"),
                    created_at=datetime.fromisoformat(doc_data["created_at"]),
                    updated_at=datetime.fromisoformat(doc_data["updated_at"]),
                )
            )

        # Sort by created_at descending (newest first)
        result.sort(key=lambda x: x.created_at, reverse=True)

        return result[offset : offset + limit]

    async def update_status(
        self,
        doc_id: UUID,
        status: str,
        error_message: Optional[str] = None,
    ) -> bool:
        """Update the status of a document.

        Args:
            doc_id: Unique identifier of the document.
            status: New status value.
            error_message: Optional error message if status is "failed".

        Returns:
            True if the update was successful, False if document not found.
        """
        documents = self._load_documents()
        doc_key = str(doc_id)

        if doc_key not in documents:
            return False

        documents[doc_key]["status"] = status
        documents[doc_key]["updated_at"] = datetime.now().isoformat()

        if error_message is not None:
            documents[doc_key]["error_message"] = error_message

        self._save_documents(documents)
        return True

    async def delete(self, doc_id: UUID) -> bool:
        """Delete a document record.

        Args:
            doc_id: Unique identifier of the document.

        Returns:
            True if deletion was successful, False if document not found.
        """
        documents = self._load_documents()
        doc_key = str(doc_id)

        if doc_key not in documents:
            return False

        del documents[doc_key]
        self._save_documents(documents)
        return True
