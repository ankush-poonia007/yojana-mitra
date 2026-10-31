"""Shared error envelope, custom exceptions, and FastAPI exception handlers."""
from __future__ import annotations

from typing import Any
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class APIError(HTTPException):
    """Custom API exception that maps directly to the shared error envelope."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        *,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        detail = {
            "code": code,
            "message": message,
            "retryable": retryable,
            "details": details or {},
        }
        super().__init__(status_code=status_code, detail=detail)


def error_response(
    status_code: int,
    code: str,
    message: str,
    *,
    retryable: bool = False,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    """Generate a standard error envelope JSONResponse matching Phase 3.3."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "retryable": retryable,
                "details": details or {},
            }
        },
    )


def raise_api_error(
    status_code: int,
    code: str,
    message: str,
    *,
    retryable: bool = False,
    details: dict[str, Any] | None = None,
) -> None:
    """Helper to raise an HTTPException with the standard error dictionary."""
    raise APIError(
        status_code=status_code,
        code=code,
        message=message,
        retryable=retryable,
        details=details,
    )


async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle 422 validation errors with contract-compliant codes."""
    if request.url.path == "/api/v1/sessions":
        return error_response(
            422,
            "INVALID_SESSION_INPUT",
            "The selected language or mode is not supported.",
        )
    return error_response(
        422,
        "INVALID_REQUEST",
        "The request does not match the supported input format.",
    )


async def http_error_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTPExceptions preserving code, message, and retryable flag."""
    detail = exc.detail
    if isinstance(detail, dict) and {"code", "message"} <= detail.keys():
        return error_response(
            exc.status_code,
            detail["code"],
            detail["message"],
            retryable=detail.get("retryable", False),
            details=detail.get("details", {}),
        )
    return error_response(exc.status_code, "REQUEST_ERROR", str(detail))


async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Catch-all 500 handler returning standard error envelope."""
    return error_response(
        500,
        "INTERNAL_SERVER_ERROR",
        "An unexpected error occurred.",
        retryable=True,
    )

