"""Eligibility engine seam adapter (H3 Contract Boundary)."""
from __future__ import annotations

import logging
from typing import Any

from app.eligibility.engine import evaluate_pmuy_eligibility

logger = logging.getLogger(__name__)


class EligibilityAdapter:
    """Boundary adapter connecting LangGraph workflow to deterministic PMUY rules."""

    def evaluate(
        self,
        scheme_id: str,
        answers: dict[str, Any],
        language: str = "hi",
    ) -> dict[str, Any]:
        """Evaluate eligibility answers adhering strictly to shared/api-contract.md §4.8.

        Connects LangGraph workflow to Anamika's deterministic PMUY rule engine.
        Returns strict 4-field contract: {scheme_id, result, reasons, missing_information}.
        Preserves missing, unclear, and contradictory answer semantics.
        """
        target_scheme = scheme_id or "pmuy"
        if target_scheme != "pmuy":
            is_hindi = language.lower().startswith("hi")
            return {
                "scheme_id": target_scheme,
                "result": "cannot_determine",
                "reasons": [
                    "वर्तमान में केवल प्रधानमंत्री उज्ज्वला योजना (PMUY 2.0) के लिए नियम मूल्यांकन समर्थित है।"
                    if is_hindi
                    else "Deterministic rule evaluation is currently supported only for PMUY 2.0."
                ],
                "missing_information": [],
            }

        assessment_result = evaluate_pmuy_eligibility(answers=answers or {}, language=language)
        return assessment_result.to_api_assessment()


eligibility_adapter = EligibilityAdapter()
