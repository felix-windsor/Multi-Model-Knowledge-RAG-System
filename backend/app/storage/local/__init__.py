"""Local storage implementations.

This package provides file-based storage implementations suitable for
development and single-instance deployments. For production environments
with multiple instances, use the database storage backend instead.
"""

from .document import LocalDocumentStorage

__all__ = ["LocalDocumentStorage"]
