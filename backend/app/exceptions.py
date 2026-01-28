"""Custom exceptions for the application."""


class StorageError(Exception):
    """Raised when storage operations fail.

    This exception indicates a failure in the storage layer, such as
    database connection errors, file system errors, or data integrity issues.
    """

    pass


class ServiceError(Exception):
    """Raised when business logic validation fails.

    This exception indicates a failure in the service layer, such as
    invalid input, constraint violations, or business rule failures.
    """

    pass
