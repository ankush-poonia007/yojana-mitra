"""Eligibility engine seam adapter (H3 Contract Boundary)."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class EligibilityAdapter:
    """Boundary adapter connecting LangGraph workflow to deterministic PMUY rules."""

    def evaluate(self, scheme_id: str, answers: dict[str, Any]) -> dict[str, Any]:
        """Evaluate eligibility answers adhering strictly to shared/api-contract.md §4.8.

        Round 1 Pre-Integration Seam:
        The deterministic eligibility rule engine handoff (H3) is pending from Anamika.
        Always returns cannot_determine. Never returns likely_eligible or likely_not_eligible.
        Communicates clearly that the deterministic eligibility engine handoff is pending.
        Preserves missing, unclear, and contradictory answer semantics.
        """
        reasons = [
            "पात्रता निर्धारण के लिए नियम इंजन एकीकरण लंबित है (Deterministic eligibility engine handoff is pending)."
        ]

        # Preserve missing answer semantics without inventing unapproved engine contracts
        missing: list[str] = []
        if not answers:
            missing.append("preliminary_answers")

        return {
            "scheme_id": scheme_id or "pmuy",
            "result": "cannot_determine",
            "reasons": reasons,
            "missing_information": missing,
        }


eligibility_adapter = EligibilityAdapter()
