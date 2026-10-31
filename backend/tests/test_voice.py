"""Unit tests for multipart voice turn submission: POST /api/v1/voice/turns."""
from __future__ import annotations

import io


def test_submit_voice_turn_success_default_language(client):
    """Verify voice turn returns transcription and speech sub-objects with default language."""
    audio_file = io.BytesIO(b"RIFF....WAVEfmt ....data....")
    response = client.post(
        "/api/v1/voice/turns",
        data={"session_id": "sess_demo_001"},
        files={"audio": ("sample.wav", audio_file, "audio/wav")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "sess_demo_001"
    assert data["turn_id"] == "turn_004"
    assert data["status"] == "awaiting_information"
    assert "transcription" in data
    assert data["transcription"]["text"] != ""
    assert "speech" in data
    assert data["speech"]["audio_base64"] == "DEMO_AUDIO_DATA"


def test_submit_voice_turn_success_explicit_language(client):
    """Verify voice turn honors explicitly passed language parameter."""
    audio_file = io.BytesIO(b"dummy_pcm_audio_bytes")
    response = client.post(
        "/api/v1/voice/turns",
        data={"session_id": "sess_demo_001", "language": "en"},
        files={"audio": ("sample.wav", audio_file, "audio/wav")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"


def test_submit_voice_turn_unknown_session_404(client):
    """Verify voice upload for unknown session returns HTTP 404."""
    audio_file = io.BytesIO(b"audio_bytes")
    response = client.post(
        "/api/v1/voice/turns",
        data={"session_id": "sess_missing_777"},
        files={"audio": ("sample.wav", audio_file, "audio/wav")},
    )
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "SESSION_NOT_FOUND"


def test_submit_voice_turn_empty_audio_400(client):
    """Verify 0-byte audio upload returns HTTP 400 INVALID_AUDIO."""
    empty_audio = io.BytesIO(b"")
    response = client.post(
        "/api/v1/voice/turns",
        data={"session_id": "sess_demo_001"},
        files={"audio": ("empty.wav", empty_audio, "audio/wav")},
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_AUDIO"


def test_submit_voice_turn_invalid_language_422(client):
    """Verify unsupported voice language returns HTTP 422 INVALID_REQUEST."""
    audio_file = io.BytesIO(b"valid_audio_bytes")
    response = client.post(
        "/api/v1/voice/turns",
        data={"session_id": "sess_demo_001", "language": "es"},
        files={"audio": ("sample.wav", audio_file, "audio/wav")},
    )
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_REQUEST"

