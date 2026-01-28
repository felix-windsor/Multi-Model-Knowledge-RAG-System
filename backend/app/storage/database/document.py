"""PostgreSQL document storage implementation."""

import uuid
from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

import asyncpg

from ..base import DocumentStorage
from ..models import Document, DocumentStatus
from .connection import DatabasePool


class DatabaseDocumentStorage(DocumentStorage):
    """PostgreSQL-based document storage.

    This class implements the DocumentStorage interface using PostgreSQL
    as the underlying storage backend. It provides CRUD operations for
    document records with proper connection pool management.
    """

    def __init__(self) -> None:
        """Initialize database document storage."""
        self._conn: Optional[asyncpg.Connection] = None
        self._tx: Optional[Any] = None

    async def _get_connection(self) -> asyncpg.Connection:
        """Get connection for query (transaction conn or new from pool).

        Returns:
            The transaction connection if active, otherwise acquires from pool.
        """
        if self._conn is not None:
            return self._conn
        return await DatabasePool.get_pool().acquire()

    async def _release_connection(self, conn: asyncpg.Connection) -> None:
        """Release connection back to pool if not in transaction mode."""
        if self._conn is None:
            await DatabasePool.get_pool().release(conn)

    async def begin_transaction(self) -> None:
        """Acquire connection and start transaction."""
        pool = DatabasePool.get_pool()
        self._conn = await pool.acquire()
        self._tx = self._conn.transaction()
        await self._tx.start()

    async def commit_transaction(self) -> None:
        """Commit transaction and release connection."""
        if self._tx is not None:
            await self._tx.commit()
            self._tx = None
        if self._conn is not None:
            await DatabasePool.get_pool().release(self._conn)
            self._conn = None

    async def rollback_transaction(self) -> None:
        """Rollback transaction and release connection."""
        if self._tx is not None:
            await self._tx.rollback()
            self._tx = None
        if self._conn is not None:
            await DatabasePool.get_pool().release(self._conn)
            self._conn = None

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
        doc_id = uuid.uuid4()
        now = datetime.now()

        conn = await self._get_connection()
        try:
            await conn.execute(
                """
                INSERT INTO documents (id, filename, file_path, file_size, mime_type, status, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                doc_id,
                filename,
                file_path,
                file_size,
                mime_type,
                DocumentStatus.PENDING.value,
                now,
                now,
            )
        finally:
            await self._release_connection(conn)

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
        async with DatabasePool.connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM documents WHERE id = $1",
                doc_id,
            )

        if not row:
            return None

        return Document(
            id=row["id"],
            filename=row["filename"],
            file_path=row["file_path"],
            file_size=row["file_size"],
            mime_type=row["mime_type"],
            status=DocumentStatus(row["status"]),
            error_message=row["error_message"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def list(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Document]:
        """List documents with optional filtering.

        Args:
            status: Filter by document status (e.g., "pending", "completed").
            limit: Maximum number of documents to return.
            offset: Number of documents to skip for pagination.

        Returns:
            List of Document objects matching the criteria.
        """
        async with DatabasePool.connection() as conn:
            if status:
                rows = await conn.fetch(
                    """
                    SELECT * FROM documents
                    WHERE status = $1
                    ORDER BY created_at DESC
                    LIMIT $2 OFFSET $3
                    """,
                    status,
                    limit,
                    offset,
                )
            else:
                rows = await conn.fetch(
                    """
                    SELECT * FROM documents
                    ORDER BY created_at DESC
                    LIMIT $1 OFFSET $2
                    """,
                    limit,
                    offset,
                )

        return [
            Document(
                id=row["id"],
                filename=row["filename"],
                file_path=row["file_path"],
                file_size=row["file_size"],
                mime_type=row["mime_type"],
                status=DocumentStatus(row["status"]),
                error_message=row["error_message"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    async def update_status(
        self,
        doc_id: UUID,
        status: str,
        error_message: Optional[str] = None,
    ) -> bool:
        """Update document status.

        Args:
            doc_id: Unique identifier of the document.
            status: New status value.
            error_message: Optional error message if status is "failed".

        Returns:
            True if the update was successful, False if document not found.
        """
        async with DatabasePool.connection() as conn:
            if error_message is not None:
                result = await conn.execute(
                    """
                    UPDATE documents
                    SET status = $1, error_message = $2, updated_at = $3
                    WHERE id = $4
                    """,
                    status,
                    error_message,
                    datetime.now(),
                    doc_id,
                )
            else:
                result = await conn.execute(
                    """
                    UPDATE documents
                    SET status = $1, updated_at = $2
                    WHERE id = $3
                    """,
                    status,
                    datetime.now(),
                    doc_id,
                )

        return result == "UPDATE 1"

    async def delete(self, doc_id: UUID) -> bool:
        """Delete document (cascade deletes tasks and webhooks).

        Args:
            doc_id: Unique identifier of the document.

        Returns:
            True if deletion was successful, False if document not found.
        """
        async with DatabasePool.connection() as conn:
            result = await conn.execute(
                "DELETE FROM documents WHERE id = $1",
                doc_id,
            )

        return result == "DELETE 1"
