#!/usr/bin/env python3
"""
exceptions.py - Custom exception classes

Autor: Homero Thompson del Lago del Terror
"""

from typing import Any


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            message=f"{resource} with id '{identifier}' not found",
            status_code=404,
            details={"resource": resource, "identifier": str(identifier)},
        )


class ValidationError(AppException):
    """Validation error."""

    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"Validation failed for field '{field}': {message}",
            status_code=422,
            details={"field": field, "validation_message": message},
        )


class AuthenticationError(AppException):
    """Authentication error."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message=message, status_code=401)


class AuthorizationError(AppException):
    """Authorization error."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, status_code=403)


class ConflictError(AppException):
    """Resource conflict error."""

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            message=f"{resource} with {field}='{value}' already exists",
            status_code=409,
            details={"resource": resource, "field": field, "value": value},
        )


class ExternalServiceError(AppException):
    """External service error."""

    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"External service '{service}' error: {message}",
            status_code=502,
            details={"service": service},
        )


class RateLimitError(AppException):
    """Rate limit exceeded."""

    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Rate limit exceeded. Please try again later.",
            status_code=429,
            details={"retry_after": retry_after},
        )
