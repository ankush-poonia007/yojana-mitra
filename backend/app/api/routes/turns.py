"""Text turn endpoint: POST /api/v1/turns."""
from __future__ import annotations

from fastapi import APIRouter
from app.schemas.turn import TextTurn
from app.services.turn_service import turn_service

router = APIRouter(prefix="/api/v1/turns", tags=["turns"])


@router.post("")
async def submit_text_turn(payload: TextTurn):
    """Submit a text query or answer within an existing session."""
    return await turn_service.process_text_turn(payload)

