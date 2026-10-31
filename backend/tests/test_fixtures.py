"""Unit tests verifying canonical JSON fixtures parse and remain immutable."""
from __future__ import annotations

import pytest
from app.services.fixture_service import fixture_service

CANONICAL_FIXTURES = [
    "error_envelope.json",
    "session_create_response.json",
    "session_get_response.json",
    "turn_awaiting_response.json",
    "turn_completed_response.json",
    "voice_turn_response.json",
]


def test_all_canonical_fixtures_load_cleanly():
    """Verify all 6 canonical shared fixtures parse into non-empty dictionaries."""
    for fixture_name in CANONICAL_FIXTURES:
        data = fixture_service.load_fixture(fixture_name)
        assert isinstance(data, dict), f"Fixture {fixture_name} did not load as dict"
        assert len(data) > 0, f"Fixture {fixture_name} is empty"


def test_fixture_immutability():
    """Verify mutating a returned fixture does not mutate subsequent loads."""
    first_load = fixture_service.load_fixture("session_create_response.json")
    first_load["mutated_key"] = "corrupted_value"

    second_load = fixture_service.load_fixture("session_create_response.json")
    assert "mutated_key" not in second_load


def test_missing_fixture_raises_filenotfound():
    """Verify attempting to load a non-existent fixture raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        fixture_service.load_fixture("non_existent_fixture.json")

