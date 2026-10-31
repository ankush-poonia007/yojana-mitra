"""Fixture service for loading canonical JSON examples safely."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from app.core.config import REPO_ROOT

FIXTURE_DIR = REPO_ROOT / "shared" / "examples"


class FixtureService:
    """Safe, immutable loader for canonical shared JSON fixtures."""

    def __init__(self, fixture_dir: Path = FIXTURE_DIR) -> None:
        self.fixture_dir = fixture_dir
        self._cache: dict[str, dict] = {}

    def load_fixture(self, name: str) -> dict:
        """Load a JSON fixture file by name and return a deep copy to prevent mutation."""
        if name not in self._cache:
            fixture_path = self.fixture_dir / name
            if not fixture_path.is_file():
                raise FileNotFoundError(f"Fixture '{name}' not found in {self.fixture_dir}")
            with fixture_path.open("r", encoding="utf-8") as f:
                self._cache[name] = json.load(f)

        return copy.deepcopy(self._cache[name])


fixture_service = FixtureService()

