"""Pytest configuration, path resolution, and shared fixtures."""
from __future__ import annotations

import sys
from pathlib import Path
import pytest
from starlette.testclient import TestClient

# Ensure the backend directory is in the Python module search path
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app
from app.services.session_service import session_service


@pytest.fixture(autouse=True)
def reset_mock_state():
    """Reset session service in-memory store before each test for state isolation."""
    session_service.reset_store()
    yield
    session_service.reset_store()


@pytest.fixture
def client() -> TestClient:
    """Provide a TestClient instance for exercising API endpoints."""
    return TestClient(app)

