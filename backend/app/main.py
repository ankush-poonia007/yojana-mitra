"""FastAPI application entry point for Yojana Mitra."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import api_router
from app.core.config import settings
from app.core.errors import (
    general_exception_handler,
    http_error_handler,
    request_validation_error_handler,
)
from app.database.connection import close_db, init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycles."""
    # Startup
    if settings.mock_mode:
        logger.info("Yojana Mitra backend starting in MOCK_MODE (in-memory fixtures).")
    else:
        logger.info("Yojana Mitra backend starting in PERSISTENT mode.")
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL must be configured when MOCK_MODE=false.")
        # Initialize connection pool and verify database readiness
        await init_db(settings.database_url)

    try:
        yield
    finally:
        # Shutdown
        logger.info("Yojana Mitra backend shutting down.")
        await close_db()


def create_app() -> FastAPI:
    """Create, configure, and return the FastAPI application instance."""
    app = FastAPI(
        title="Yojana Mitra API",
        version="1.0.0",
        description="Voice- and text-enabled government scheme navigation assistant API.",
        lifespan=lifespan,
    )

    # CORS configuration
    if settings.cors_origins_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins_list,
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
        )

    # Exception handlers matching Phase 3.3 error envelope
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Include root API router (containing /api/v1/sessions, /api/v1/turns, /api/v1/voice/turns, /health)
    app.include_router(api_router)

    return app


app = create_app()
