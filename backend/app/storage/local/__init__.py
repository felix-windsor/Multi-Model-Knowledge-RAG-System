"""Local storage implementations.

This package provides file-based storage implementations suitable for
development and single-instance deployments. For production environments
with multiple instances, use the database storage backend instead.
"""

from .document import LocalDocumentStorage
from .task import LocalTaskStorage

__all__ = ["LocalDocumentStorage", "LocalTaskStorage"]
