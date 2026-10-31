"""Session endpoints: POST /api/v1/sessions and GET /api/v1/sessions/{session_id}."""
from __future__ import annotations

from fastapi import APIRouter
from app.schemas.session import SessionCreate
from app.services.session_service import session_service

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.post("", status_code=201)
async def create_session(payload: SessionCreate):
    """Create a new consultation session."""
    return session_service.create_session(payload)


@router.get("/{session_id}")
async def get_session(session_id: str):
    """Retrieve session details and prior conversation turn history."""
    return session_service.get_session(session_id)

