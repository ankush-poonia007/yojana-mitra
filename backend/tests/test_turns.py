"""Unit tests for text turn submission: POST /api/v1/turns."""
from __future__ import annotations


def test_submit_text_turn_success(client):
    """Verify text turn returns awaiting_information fixture with audio and answer."""
    response = client.post(
        "/api/v1/turns",
        json={
            "session_id": "sess_demo_001",
            "text": "क्या मैं प्रधानमंत्री उज्ज्वला योजना के लिए पात्र हूं?",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "sess_demo_001"
    assert data["turn_id"] == "turn_003"
    assert data["status"] == "awaiting_information"
    assert "answer" in data
    assert "text" in data["answer"]
    assert "speech" in data
    assert data["speech"]["audio_base64"] == "DEMO_AUDIO_DATA"
    assert data["speech"]["content_type"] == "audio/mpeg"


def test_submit_text_turn_unknown_session_404(client):
    """Verify turn submission for unknown session returns HTTP 404."""
    response = client.post(
        "/api/v1/turns",
        json={
            "session_id": "sess_missing_999",
            "text": "नमस्ते",
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "SESSION_NOT_FOUND"


def test_submit_text_turn_empty_text_400(client):
    """Verify empty text string is rejected with HTTP 400 EMPTY_TEXT_INPUT."""
    response = client.post(
        "/api/v1/turns",
        json={
            "session_id": "sess_demo_001",
            "text": "",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "EMPTY_TEXT_INPUT"


def test_submit_text_turn_whitespace_text_400(client):
    """Verify whitespace-only text is rejected with HTTP 400 EMPTY_TEXT_INPUT."""
    response = client.post(
        "/api/v1/turns",
        json={
            "session_id": "sess_demo_001",
            "text": "   \n\t  ",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "EMPTY_TEXT_INPUT"


def test_submit_text_turn_missing_field_422(client):
    """Verify missing session_id produces standard 422 INVALID_REQUEST error."""
    response = client.post(
        "/api/v1/turns",
        json={"text": "कोई सत्र नहीं"},
    )
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_REQUEST"

