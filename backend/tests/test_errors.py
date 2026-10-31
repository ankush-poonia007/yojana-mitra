"""Unit tests verifying strict compliance with the shared error envelope."""
from __future__ import annotations

from app.services.turn_service import turn_service


def test_error_envelope_structure_404(client):
    """Verify 404 response contains code, message, retryable, and details keys."""
    response = client.get("/api/v1/sessions/non_existent_id")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    err = data["error"]
    assert err["code"] == "SESSION_NOT_FOUND"
    assert isinstance(err["message"], str)
    assert err["retryable"] is False
    assert isinstance(err["details"], dict)


def test_error_envelope_structure_422(client):
    """Verify 422 response contains standardized error envelope."""
    response = client.post("/api/v1/sessions", json={"language": "invalid", "mode": "voice"})
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    err = data["error"]
    assert err["code"] == "INVALID_SESSION_INPUT"
    assert err["retryable"] is False
    assert isinstance(err["details"], dict)


def test_error_envelope_structure_400(client):
    """Verify 400 response contains standardized error envelope."""
    response = client.post("/api/v1/turns", json={"session_id": "sess_demo_001", "text": " "})
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    err = data["error"]
    assert err["code"] == "EMPTY_TEXT_INPUT"
    assert err["retryable"] is False
    assert isinstance(err["details"], dict)


def test_general_exception_returns_500_envelope(monkeypatch):
    """Verify unhandled exceptions return HTTP 500 INTERNAL_SERVER_ERROR with retryable=True."""
    from starlette.testclient import TestClient
    from app.main import app

    async def broken_process(*args, **kwargs):
        raise RuntimeError("Simulated crash")

    monkeypatch.setattr(turn_service, "process_text_turn", broken_process)

    # Use raise_server_exceptions=False so TestClient returns the 500 response instead of re-raising
    test_client = TestClient(app, raise_server_exceptions=False)
    response = test_client.post(
        "/api/v1/turns",
        json={"session_id": "sess_demo_001", "text": "परीक्षण"},
    )
    assert response.status_code == 500
    data = response.json()
    assert "error" in data
    err = data["error"]
    assert err["code"] == "INTERNAL_SERVER_ERROR"
    assert err["retryable"] is True
    assert isinstance(err["details"], dict)
