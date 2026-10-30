"""Voice turn endpoint: POST /api/v1/voice/turns."""
from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile
from app.services.turn_service import turn_service

router = APIRouter(prefix="/api/v1/voice/turns", tags=["voice"])


@router.post("")
async def submit_voice_turn(
    session_id: str = Form(...),
    audio: UploadFile = File(...),
    language: str | None = Form(None),
):
    """Submit a spoken voice query within an existing session."""
    return await turn_service.process_voice_turn(
        session_id=session_id,
        audio=audio,
        language=language,
    )

