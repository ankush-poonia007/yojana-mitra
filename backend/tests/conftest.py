"""Global pytest fixtures for Yojana Mitra backend tests."""

import pytest


@pytest.fixture
def mock_session_id():
    """Returns a canonical test session ID."""
    return "sess_demo_001"

