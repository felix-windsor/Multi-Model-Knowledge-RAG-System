"""Database connection management.

This module provides PostgreSQL connection pool management for async database access.
It uses asyncpg for high-performance async PostgreSQL operations.
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

import asyncpg


class DatabasePool:
    """PostgreSQL connection pool manager.

    This class manages a singleton connection pool for PostgreSQL database access.
    It provides methods for initializing, closing, and acquiring connections from
    the pool, as well as transaction management.

    Usage:
        # Initialize the pool at application startup
        await DatabasePool.initialize(database_url)

        # Use a connection
        async with DatabasePool.connection() as conn:
            result = await conn.fetch("SELECT * FROM documents")

        # Use a transaction
        async with DatabasePool.transaction() as conn:
            await conn.execute("INSERT INTO documents ...")
            await conn.execute("UPDATE tasks ...")

        # Close the pool at application shutdown
        await DatabasePool.close()
    """

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def initialize(
        cls,
        database_url: str,
        min_size: int = 5,
        max_size: int = 20,
    ) -> None:
        """Initialize the connection pool.

        Args:
            database_url: PostgreSQL connection string.
            min_size: Minimum number of connections in the pool.
            max_size: Maximum number of connections in the pool.

        Raises:
            asyncpg.PostgresError: If connection to database fails.
        """
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                database_url,
                min_size=min_size,
                max_size=max_size,
            )

    @classmethod
    async def close(cls) -> None:
        """Close the connection pool.

        This method should be called during application shutdown to properly
        release all database connections.
        """
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        """Get the connection pool.

        Returns:
            The asyncpg connection pool.

        Raises:
            RuntimeError: If the pool has not been initialized.
        """
        if cls._pool is None:
            raise RuntimeError(
                "Database pool not initialized. Call initialize() first."
            )
        return cls._pool

    @classmethod
    @asynccontextmanager
    async def connection(cls) -> AsyncIterator[asyncpg.Connection]:
        """Get a connection from the pool.

        This context manager acquires a connection from the pool and
        automatically releases it when the context exits.

        Yields:
            An asyncpg connection.

        Raises:
            RuntimeError: If the pool has not been initialized.
        """
        pool = cls.get_pool()
        async with pool.acquire() as conn:
            yield conn

    @classmethod
    @asynccontextmanager
    async def transaction(cls) -> AsyncIterator[asyncpg.Connection]:
        """Get a connection with an active transaction.

        This context manager acquires a connection from the pool, starts a
        transaction, and automatically commits or rolls back when the context
        exits.

        Yields:
            An asyncpg connection with an active transaction.

        Raises:
            RuntimeError: If the pool has not been initialized.
        """
        pool = cls.get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                yield conn


async def check_database_health(database_url: str) -> bool:
    """Check if database is accessible.

    This function attempts to connect to the database and execute a simple
    query to verify connectivity.

    Args:
        database_url: PostgreSQL connection string.

    Returns:
        True if the database is accessible, False otherwise.
    """
    try:
        conn = await asyncpg.connect(database_url)
        await conn.execute("SELECT 1")
        await conn.close()
        return True
    except Exception:
        return False
