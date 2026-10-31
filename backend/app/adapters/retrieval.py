"""Retrieval seam adapter (H4 Contract Boundary)."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class RetrievalServiceError(Exception):
    """Raised when the retrieval infrastructure encounters an unrecoverable failure."""


class RetrievalAdapter:
    """Boundary adapter connecting LangGraph workflow to official-source retrieval."""

    def search(
        self,
        query: str,
        scheme_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve relevant grounded passages matching shared/api-contract.md §4.9.

        Round 1 Pre-Integration Seam:
        Official-source retrieval corpus and ingestion (H4) are pending handoff.
        Always returns empty evidence list [] until validated retrieval is integrated.
        Never manufactures source references, URLs, page numbers, or retrieved evidence.
        """
        # Until validated retrieval ingestion is integrated, return empty evidence.
        # This ensures zero fabricated citations and triggers explicit refusal.
        return []


retrieval_adapter = RetrievalAdapter()
