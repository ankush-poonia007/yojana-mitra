"""Root API router combining all endpoint sub-routers."""
from __future__ import annotations

from fastapi import APIRouter
from app.api.routes import health, sessions, turns, voice

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(sessions.router)
api_router.include_router(turns.router)
api_router.include_router(voice.router)
api_router.include_router(health.router)

