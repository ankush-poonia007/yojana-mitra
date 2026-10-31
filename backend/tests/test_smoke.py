"""Smoke tests to verify backend test harness and package configuration."""

import importlib


def test_environment_smoke():
    """Verify standard assertion behavior in the test harness."""
    assert True


def test_conftest_fixture(mock_session_id):
    """Verify that global test fixtures in conftest.py are loaded properly."""
    assert mock_session_id == "sess_demo_001"


def test_package_import_smoke():
    """Verify that app and app.eligibility packages import without error."""
    app_module = importlib.import_module("app")
    eligibility_module = importlib.import_module("app.eligibility")

    assert app_module is not None
    assert eligibility_module is not None

