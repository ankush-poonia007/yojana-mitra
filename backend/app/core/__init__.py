"""Core configuration and shared error handling package."""
from app.core.config import settings
from app.core.errors import (
    APIError,
    error_response,
    general_exception_handler,
    http_error_handler,
    raise_api_error,
    request_validation_error_handler,
)

__all__ = [
    "settings",
    "APIError",
    "error_response",
    "raise_api_error",
    "request_validation_error_handler",
    "http_error_handler",
    "general_exception_handler",
]

