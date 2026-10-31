"""Unit tests for session creation, retrieval, and health endpoints."""
from __future__ import annotations


def test_create_session_success_hindi_voice(client):
    """Verify session creation in Hindi voice mode returns HTTP 201 with valid metadata."""
    response = client.post(
        "/api/v1/sessions",
        json={"language": "hi", "mode": "voice"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["session_id"] == "sess_demo_001"
    assert data["status"] == "active"
    assert data["language"] == "hi"
    assert data["mode"] == "voice"
    assert "created_at" in data


def test_create_session_success_english_text(client):
    """Verify session creation in English text mode returns HTTP 201 with updated settings."""
    response = client.post(
        "/api/v1/sessions",
        json={"language": "en", "mode": "text"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["language"] == "en"
    assert data["mode"] == "text"


def test_create_session_invalid_language_422(client):
    """Verify unsupported language produces standard 422 INVALID_SESSION_INPUT error."""
    response = client.post(
        "/api/v1/sessions",
        json={"language": "fr", "mode": "voice"},
    )
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_SESSION_INPUT"
    assert data["error"]["retryable"] is False


def test_create_session_invalid_mode_422(client):
    """Verify unsupported mode produces standard 422 INVALID_SESSION_INPUT error."""
    response = client.post(
        "/api/v1/sessions",
        json={"language": "hi", "mode": "telepathy"},
    )
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_SESSION_INPUT"


def test_create_session_empty_payload_422(client):
    """Verify empty payload produces standard 422 validation error."""
    response = client.post("/api/v1/sessions", json={})
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_SESSION_INPUT"


def test_get_session_success_seeded(client):
    """Verify retrieval of seeded session returns HTTP 200 with turn history."""
    response = client.get("/api/v1/sessions/sess_demo_001")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "sess_demo_001"
    assert data["status"] == "active"
    assert data["language"] == "hi"
    assert data["mode"] == "voice"
    assert "turns" in data
    assert len(data["turns"]) == 2
    assert data["turns"][0]["role"] == "user"
    assert data["turns"][1]["role"] == "assistant"


def test_get_session_unknown_404(client):
    """Verify requesting an unknown session returns HTTP 404 SESSION_NOT_FOUND."""
    response = client.get("/api/v1/sessions/sess_non_existent")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "SESSION_NOT_FOUND"
    assert data["error"]["retryable"] is False


def test_health_check_returns_200(client):
    """Verify health endpoint returns status ok and mode mock."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mode"] == "mock"

