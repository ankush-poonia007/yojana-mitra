"""Acceptance and integration tests for SessionService and TurnService persistence."""
from __future__ import annotations

import io
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import UploadFile

from app.core.config import settings
from app.core.errors import APIError
from app.database.repositories import ConcurrencyConflictError, SessionNotFoundError
from app.database.repositories.session_repository import SessionRecord, SessionRepository
from app.database.repositories.turn_repository import TurnRecord, TurnRepository
from app.schemas.session import SessionCreate, SessionCreateResponse, SessionGetResponse
from app.schemas.turn import TextTurn, TurnResponse
from app.services.session_service import SessionService
from app.services.turn_service import TurnService


# ==============================================================================
# 1. SESSION SERVICE TESTS
# ==============================================================================


@pytest.mark.asyncio
async def test_session_service_mock_create(monkeypatch):
    """Verify mock mode session creation uses fixtures and updates in-memory store."""
    monkeypatch.setattr(settings, "mock_mode", True)
    service = SessionService()

    payload = SessionCreate(language="hi", mode="voice")
    resp = await service.create_session(payload)

    assert resp["session_id"] == "sess_demo_001"
    assert resp["language"] == "hi"
    assert resp["mode"] == "voice"
    assert resp["status"] == "active"
    assert await service.session_exists("sess_demo_001") is True


@pytest.mark.asyncio
async def test_session_service_mock_get(monkeypatch):
    """Verify mock mode session retrieval returns seeded session with turn history."""
    monkeypatch.setattr(settings, "mock_mode", True)
    service = SessionService()

    resp = await service.get_session("sess_demo_001")
    assert resp["session_id"] == "sess_demo_001"
    assert resp["status"] == "active"
    assert "turns" in resp
    assert len(resp["turns"]) == 2


@pytest.mark.asyncio
async def test_session_service_mock_unknown_session(monkeypatch):
    """Verify mock mode raises 404 SESSION_NOT_FOUND for unknown session."""
    monkeypatch.setattr(settings, "mock_mode", True)
    service = SessionService()

    with pytest.raises(APIError) as exc_info:
        await service.get_session("sess_unknown_999")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail["code"] == "SESSION_NOT_FOUND"
    assert exc_info.value.detail["retryable"] is False


@pytest.mark.asyncio
async def test_session_service_mock_mode_zero_db_calls(monkeypatch):
    """Verify mock mode makes zero database or repository calls."""
    monkeypatch.setattr(settings, "mock_mode", True)

    mock_session_repo = MagicMock(spec=SessionRepository)
    mock_turn_repo = MagicMock(spec=TurnRepository)

    service = SessionService(
        session_repository=mock_session_repo,
        turn_repository=mock_turn_repo,
    )

    await service.create_session(SessionCreate(language="en", mode="text"))
    await service.get_session("sess_demo_001")
    await service.session_exists("sess_demo_001")
    await service.get_session_settings("sess_demo_001")

    mock_session_repo.create_session.assert_not_called()
    mock_session_repo.get_session.assert_not_called()
    mock_session_repo.session_exists.assert_not_called()
    mock_turn_repo.get_turns_for_session.assert_not_called()


@pytest.mark.asyncio
async def test_session_service_mock_mode_configured_url_cannot_bypass(monkeypatch):
    """Verify configured DATABASE_URL cannot bypass mock mode."""
    monkeypatch.setattr(settings, "mock_mode", True)
    monkeypatch.setattr(settings, "database_url", "postgresql://user:pass@localhost:5432/db")

    mock_session_repo = MagicMock(spec=SessionRepository)
    service = SessionService(session_repository=mock_session_repo)

    await service.create_session(SessionCreate(language="hi", mode="voice"))
    mock_session_repo.create_session.assert_not_called()


@pytest.mark.asyncio
async def test_session_service_persistent_create(monkeypatch):
    """Verify persistent mode creates session via repository and returns Phase 3.3 contract."""
    monkeypatch.setattr(settings, "mock_mode", False)

    created_dt = datetime(2026, 10, 31, 8, 30, 0, tzinfo=timezone.utc)
    mock_record = SessionRecord(
        session_id="sess_persisted_001",
        status="active",
        language="hi",
        mode="voice",
        created_at=created_dt,
        updated_at=created_dt,
        version=1,
    )

    mock_session_repo = AsyncMock(spec=SessionRepository)
    mock_session_repo.create_session.return_value = mock_record

    service = SessionService(session_repository=mock_session_repo)
    resp = await service.create_session(SessionCreate(language="hi", mode="voice"))

    mock_session_repo.create_session.assert_awaited_once_with(
        language="hi",
        mode="voice",
    )
    assert resp["session_id"] == "sess_persisted_001"
    assert resp["status"] == "active"
    assert resp["language"] == "hi"
    assert resp["mode"] == "voice"
    assert resp["created_at"] == created_dt.isoformat()
    # Invariant: internal version and updated_at must NOT be exposed in create response
    assert "version" not in resp
    assert "updated_at" not in resp


@pytest.mark.asyncio
async def test_session_service_persistent_get_found(monkeypatch):
    """Verify persistent mode retrieves session and turn history from repositories."""
    monkeypatch.setattr(settings, "mock_mode", False)

    now = datetime(2026, 10, 31, 8, 30, 0, tzinfo=timezone.utc)
    mock_session_record = SessionRecord(
        session_id="sess_persisted_001",
        status="active",
        language="hi",
        mode="voice",
        created_at=now,
        updated_at=now,
        version=2,
    )
    mock_turns = [
        TurnRecord("turn_001", "sess_persisted_001", 0, "user", "नमस्ते", now),
        TurnRecord("turn_002", "sess_persisted_001", 1, "assistant", "नमस्ते, मैं मदद कर सकता हूँ", now),
    ]

    mock_session_repo = AsyncMock(spec=SessionRepository)
    mock_session_repo.get_session.return_value = mock_session_record

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    mock_turn_repo.get_turns_for_session.return_value = mock_turns

    service = SessionService(
        session_repository=mock_session_repo,
        turn_repository=mock_turn_repo,
    )
    resp = await service.get_session("sess_persisted_001")

    assert resp["session_id"] == "sess_persisted_001"
    assert resp["status"] == "active"
    assert resp["language"] == "hi"
    assert resp["mode"] == "voice"
    assert len(resp["turns"]) == 2
    assert resp["turns"][0] == {"turn_id": "turn_001", "role": "user", "text": "नमस्ते"}
    assert resp["turns"][1] == {"turn_id": "turn_002", "role": "assistant", "text": "नमस्ते, मैं मदद कर सकता हूँ"}


@pytest.mark.asyncio
async def test_session_service_persistent_get_not_found(monkeypatch):
    """Verify persistent mode raises 404 SESSION_NOT_FOUND when record is missing."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_repo = AsyncMock(spec=SessionRepository)
    mock_session_repo.get_session.return_value = None

    service = SessionService(session_repository=mock_session_repo)

    with pytest.raises(APIError) as exc_info:
        await service.get_session("sess_nonexistent")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail["code"] == "SESSION_NOT_FOUND"


@pytest.mark.asyncio
async def test_session_service_persistent_session_exists(monkeypatch):
    """Verify persistent mode queries session_exists on repository."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_repo = AsyncMock(spec=SessionRepository)
    mock_session_repo.session_exists.return_value = True

    service = SessionService(session_repository=mock_session_repo)
    exists = await service.session_exists("sess_test_123")

    assert exists is True
    mock_session_repo.session_exists.assert_awaited_once_with("sess_test_123")


# ==============================================================================
# 2. TURN SERVICE TESTS
# ==============================================================================


@pytest.mark.asyncio
async def test_turn_service_mock_text(monkeypatch):
    """Verify mock text processing returns fixture without database access."""
    monkeypatch.setattr(settings, "mock_mode", True)
    service = TurnService()

    payload = TextTurn(session_id="sess_demo_001", text="क्या मैं पात्र हूँ?")
    resp = await service.process_text_turn(payload)

    assert resp["session_id"] == "sess_demo_001"
    assert resp["status"] == "awaiting_information"
    assert "answer" in resp
    assert "speech" in resp


@pytest.mark.asyncio
async def test_turn_service_mock_zero_db_calls(monkeypatch):
    """Verify mock mode never invokes turn repository operations."""
    monkeypatch.setattr(settings, "mock_mode", True)

    mock_turn_repo = MagicMock(spec=TurnRepository)
    service = TurnService(turn_repository_instance=mock_turn_repo)

    payload = TextTurn(session_id="sess_demo_001", text="Mock test")
    await service.process_text_turn(payload)

    mock_turn_repo.append_turn_pair.assert_not_called()
    mock_turn_repo.get_turns_for_session.assert_not_called()


@pytest.mark.asyncio
async def test_turn_service_persistent_text_success(monkeypatch):
    """Verify persistent text turn fetches history, appends turn pair atomically, and returns contract shape."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = {
        "session_id": "sess_123",
        "status": "active",
        "language": "hi",
        "mode": "text",
        "version": 1,
    }

    now = datetime(2026, 10, 31, 8, 30, 0, tzinfo=timezone.utc)
    user_rec = TurnRecord("turn_u1", "sess_123", 0, "user", "मैं पात्र हूँ?", now)
    asst_rec = TurnRecord("turn_a1", "sess_123", 1, "assistant", "मैं आपकी पात्रता...", now)

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    mock_turn_repo.get_turns_for_session.return_value = []
    mock_turn_repo.append_turn_pair.return_value = (user_rec, asst_rec)

    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    payload = TextTurn(session_id="sess_123", text="मैं पात्र हूँ?")
    resp = await service.process_text_turn(payload)

    mock_turn_repo.get_turns_for_session.assert_awaited_once_with("sess_123")
    mock_turn_repo.append_turn_pair.assert_awaited_once()
    assert resp["session_id"] == "sess_123"
    assert resp["turn_id"] == "turn_a1"
    assert resp["status"] == "awaiting_information"
    assert resp["language"] == "hi"
    assert "answer" in resp
    assert "speech" in resp


@pytest.mark.asyncio
async def test_turn_service_persistent_text_unknown_session(monkeypatch):
    """Verify persistent text turn raises 404 SESSION_NOT_FOUND if session does not exist."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = None

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    payload = TextTurn(session_id="sess_missing", text="Hello")
    with pytest.raises(APIError) as exc_info:
        await service.process_text_turn(payload)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail["code"] == "SESSION_NOT_FOUND"
    mock_turn_repo.append_turn_pair.assert_not_called()


@pytest.mark.asyncio
async def test_turn_service_text_empty_input_rejected(monkeypatch):
    """Verify empty or whitespace text raises 400 EMPTY_TEXT_INPUT before repository access."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = {
        "session_id": "sess_123",
        "language": "hi",
        "version": 1,
    }

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    with pytest.raises(APIError) as exc_info:
        await service.process_text_turn(TextTurn(session_id="sess_123", text="   "))

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["code"] == "EMPTY_TEXT_INPUT"
    mock_turn_repo.append_turn_pair.assert_not_called()


@pytest.mark.asyncio
async def test_turn_service_persistent_text_concurrency_conflict(monkeypatch):
    """Verify optimistic concurrency conflict raises retryable 500 without creating unapproved error codes."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = {
        "session_id": "sess_123",
        "language": "hi",
        "version": 1,
    }

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    mock_turn_repo.get_turns_for_session.return_value = []
    mock_turn_repo.append_turn_pair.side_effect = ConcurrencyConflictError("Version conflict: expected 1, found 2")

    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    with pytest.raises(APIError) as exc_info:
        await service.process_text_turn(TextTurn(session_id="sess_123", text="Conflict test"))

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail["code"] == "INTERNAL_SERVER_ERROR"
    assert exc_info.value.detail["retryable"] is True


@pytest.mark.asyncio
async def test_turn_service_persistent_text_session_not_found_on_append(monkeypatch):
    """Verify SessionNotFoundError raised during turn pair append surfaces as 404 SESSION_NOT_FOUND."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = {
        "session_id": "sess_deleted",
        "language": "hi",
        "version": 1,
    }

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    mock_turn_repo.get_turns_for_session.return_value = []
    mock_turn_repo.append_turn_pair.side_effect = SessionNotFoundError("Session missing in DB")

    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    with pytest.raises(APIError) as exc_info:
        await service.process_text_turn(TextTurn(session_id="sess_deleted", text="Check"))

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail["code"] == "SESSION_NOT_FOUND"


# ==============================================================================
# 3. VOICE SERVICE TESTS
# ==============================================================================


@pytest.mark.asyncio
async def test_turn_service_mock_voice(monkeypatch):
    """Verify mock voice processing returns fixture with updated session metadata."""
    monkeypatch.setattr(settings, "mock_mode", True)
    service = TurnService()

    audio_file = UploadFile(filename="voice.wav", file=io.BytesIO(b"RIFF_FAKE_AUDIO_DATA"))
    resp = await service.process_voice_turn(session_id="sess_demo_001", audio=audio_file, language="hi")

    assert resp["session_id"] == "sess_demo_001"
    assert resp["language"] == "hi"
    assert "transcription" in resp
    assert "speech" in resp


@pytest.mark.asyncio
async def test_turn_service_voice_empty_audio_rejected(monkeypatch):
    """Verify empty audio upload is rejected with 400 INVALID_AUDIO."""
    monkeypatch.setattr(settings, "mock_mode", True)
    service = TurnService()

    empty_audio = UploadFile(filename="empty.wav", file=io.BytesIO(b""))
    with pytest.raises(APIError) as exc_info:
        await service.process_voice_turn(session_id="sess_demo_001", audio=empty_audio)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["code"] == "INVALID_AUDIO"


@pytest.mark.asyncio
async def test_turn_service_voice_invalid_language_rejected(monkeypatch):
    """Verify unsupported language in voice turn raises 422 INVALID_REQUEST."""
    monkeypatch.setattr(settings, "mock_mode", True)
    service = TurnService()

    audio_file = UploadFile(filename="voice.wav", file=io.BytesIO(b"RIFF_FAKE_AUDIO"))
    with pytest.raises(APIError) as exc_info:
        await service.process_voice_turn(session_id="sess_demo_001", audio=audio_file, language="invalid_lang")

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail["code"] == "INVALID_REQUEST"


@pytest.mark.asyncio
async def test_turn_service_persistent_voice_stt_unavailable(monkeypatch):
    """Verify persistent voice turn raises 503 STT_UNAVAILABLE when speech processing is unavailable."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = {
        "session_id": "sess_123",
        "language": "hi",
        "version": 1,
    }

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    audio_file = UploadFile(filename="voice.wav", file=io.BytesIO(b"RIFF_SAMPLE_AUDIO_BYTES"))

    # When no transcription is provided (STT not available in Phase 2)
    with pytest.raises(APIError) as exc_info:
        await service.process_voice_turn(session_id="sess_123", audio=audio_file)

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail["code"] == "STT_UNAVAILABLE"
    assert exc_info.value.detail["retryable"] is True
    # Ensure no database turns were saved
    mock_turn_repo.append_turn_pair.assert_not_called()


@pytest.mark.asyncio
async def test_turn_service_persistent_voice_with_transcription_persists_pair(monkeypatch):
    """Verify persistent voice turn with available transcription persists pair and returns contract response."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = {
        "session_id": "sess_123",
        "language": "hi",
        "version": 1,
    }

    now = datetime(2026, 10, 31, 8, 30, 0, tzinfo=timezone.utc)
    user_rec = TurnRecord("turn_v_u1", "sess_123", 0, "user", "मेरे घर में गैस कनेक्शन नहीं है", now)
    asst_rec = TurnRecord("turn_v_a1", "sess_123", 1, "assistant", "समझ गया। क्या आवेदन करने वाली महिला की उम्र 18 वर्ष या उससे अधिक है?", now)

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    mock_turn_repo.get_turns_for_session.return_value = []
    mock_turn_repo.append_turn_pair.return_value = (user_rec, asst_rec)

    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    audio_file = UploadFile(filename="voice.wav", file=io.BytesIO(b"RIFF_AUDIO_CONTENT"))
    resp = await service.process_voice_turn(
        session_id="sess_123",
        audio=audio_file,
        language="hi",
        transcription_text="मेरे घर में गैस कनेक्शन नहीं है",
    )

    # Invariant: Turn pair is persisted with the transcribed text; raw audio bytes are NOT passed to repository
    mock_turn_repo.append_turn_pair.assert_awaited_once_with(
        session_id="sess_123",
        expected_version=1,
        user_text="मेरे घर में गैस कनेक्शन नहीं है",
        assistant_text=resp["answer"]["text"],
    )

    assert resp["session_id"] == "sess_123"
    assert resp["turn_id"] == "turn_v_a1"
    assert resp["transcription"]["text"] == "मेरे घर में गैस कनेक्शन नहीं है"
    assert resp["speech"]["audio_base64"] == "DEMO_AUDIO_DATA"


# ==============================================================================
# 4. API SCHEMA COMPATIBILITY VERIFICATION
# ==============================================================================


@pytest.mark.asyncio
async def test_session_create_response_schema_compatibility(monkeypatch):
    """Verify persistent session creation response strictly validates against SessionCreateResponse."""
    monkeypatch.setattr(settings, "mock_mode", False)

    now = datetime(2026, 10, 31, 8, 30, 0, tzinfo=timezone.utc)
    mock_record = SessionRecord(
        session_id="sess_schema_test",
        status="active",
        language="en",
        mode="text",
        created_at=now,
        updated_at=now,
        version=1,
    )

    mock_session_repo = AsyncMock(spec=SessionRepository)
    mock_session_repo.create_session.return_value = mock_record

    service = SessionService(session_repository=mock_session_repo)
    raw_resp = await service.create_session(SessionCreate(language="en", mode="text"))

    # Validates with Pydantic model
    validated = SessionCreateResponse(**raw_resp)
    assert validated.session_id == "sess_schema_test"
    assert validated.language == "en"
    assert validated.mode == "text"
    assert validated.status == "active"


@pytest.mark.asyncio
async def test_session_get_response_schema_compatibility(monkeypatch):
    """Verify persistent session retrieval response strictly validates against SessionGetResponse."""
    monkeypatch.setattr(settings, "mock_mode", False)

    now = datetime(2026, 10, 31, 8, 30, 0, tzinfo=timezone.utc)
    mock_session_record = SessionRecord(
        session_id="sess_schema_test",
        status="active",
        language="hi",
        mode="voice",
        created_at=now,
        updated_at=now,
        version=2,
    )
    mock_turns = [
        TurnRecord("turn_001", "sess_schema_test", 0, "user", "प्रणाम", now),
        TurnRecord("turn_002", "sess_schema_test", 1, "assistant", "नमस्ते", now),
    ]

    mock_session_repo = AsyncMock(spec=SessionRepository)
    mock_session_repo.get_session.return_value = mock_session_record

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    mock_turn_repo.get_turns_for_session.return_value = mock_turns

    service = SessionService(
        session_repository=mock_session_repo,
        turn_repository=mock_turn_repo,
    )
    raw_resp = await service.get_session("sess_schema_test")

    validated = SessionGetResponse(**raw_resp)
    assert validated.session_id == "sess_schema_test"
    assert len(validated.turns) == 2
    assert validated.turns[0].turn_id == "turn_001"
    assert validated.turns[0].role == "user"


@pytest.mark.asyncio
async def test_turn_response_schema_compatibility(monkeypatch):
    """Verify persistent turn response strictly validates against TurnResponse."""
    monkeypatch.setattr(settings, "mock_mode", False)

    mock_session_service = AsyncMock(spec=SessionService)
    mock_session_service.get_session_settings.return_value = {
        "session_id": "sess_schema_turn",
        "language": "hi",
        "version": 1,
    }

    now = datetime(2026, 10, 31, 8, 30, 0, tzinfo=timezone.utc)
    user_rec = TurnRecord("turn_u1", "sess_schema_turn", 0, "user", "सवाल", now)
    asst_rec = TurnRecord("turn_a1", "sess_schema_turn", 1, "assistant", "जवाब", now)

    mock_turn_repo = AsyncMock(spec=TurnRepository)
    mock_turn_repo.get_turns_for_session.return_value = []
    mock_turn_repo.append_turn_pair.return_value = (user_rec, asst_rec)

    service = TurnService(
        session_service_instance=mock_session_service,
        turn_repository_instance=mock_turn_repo,
    )

    raw_resp = await service.process_text_turn(
        TextTurn(session_id="sess_schema_turn", text="सवाल")
    )

    validated = TurnResponse(**raw_resp)
    assert validated.session_id == "sess_schema_turn"
    assert validated.turn_id == "turn_a1"
    assert validated.status == "awaiting_information"
    assert validated.speech.audio_base64 == "DEMO_AUDIO_DATA"
