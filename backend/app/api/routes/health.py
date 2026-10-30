"""Health check endpoint: GET /health."""
from __future__ import annotations

from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Liveness probe reporting current status and execution mode."""
    return {
        "status": "ok",
        "mode": "mock" if settings.mock_mode else "real",
    }

