"""Phase A: Input, Intent, and Scheme Classification Node."""
from __future__ import annotations

import logging
import re
from typing import Any, Optional
from langchain_core.runnables import RunnableConfig

from app.core.config import settings
from app.graph.state import YojanaWorkflowState
from app.llm import ModelTier, gemini_client
from app.llm.prompts import (
    INTENT_SCHEME_SYSTEM_INSTRUCTION,
    INTENT_SCHEME_USER_PROMPT_TEMPLATE,
)

logger = logging.getLogger(__name__)


def _extract_answers_heuristically(user_text: str, current_answers: dict[str, Any]) -> dict[str, Any]:
    """Deterministic factual extractor for core PMUY dialogue facts."""
    updated = dict(current_answers)
    text_lower = user_text.lower()

    # Gender checks
    if any(w in text_lower for w in ["महिला", "woman", "female", "औरत", "पत्नी"]):
        updated["applicant_is_woman"] = True
    elif any(w in text_lower for w in ["पुरुष", "man", "male", "लड़का", "पति"]):
        updated["applicant_is_woman"] = False

    # Age checks
    age_match = re.search(r"(\d+)\s*(?:साल|वर्ष|years?|yr)", text_lower)
    if age_match:
        age_val = int(age_match.group(1))
        updated["age_18_or_above"] = age_val >= 18
    elif any(w in text_lower for w in ["18 से अधिक", "18+", "वयस्क", "adult", "18 वर्ष"]):
        updated["age_18_or_above"] = True
    elif any(w in text_lower for w in ["नाबालिग", "under 18", "minor", "बच्ची"]):
        updated["age_18_or_above"] = False

    # LPG connection checks
    if any(w in text_lower for w in ["गैस नहीं", "lpg नहीं", "no gas", "no lpg", "कनेक्शन नहीं"]):
        updated["household_has_lpg"] = False
    elif any(w in text_lower for w in ["पहले से गैस", "गैस है", "lpg है", "already have gas", "have lpg"]):
        updated["household_has_lpg"] = True

    return updated


async def intent_classification_node(
    state: YojanaWorkflowState,
    config: Optional[RunnableConfig] = None,
) -> dict[str, Any]:
    """Execute Phase A: Extract language context, intent, scheme ID, and facts."""
    cfg = config.get("configurable", {}) if config else {}
    history = cfg.get("history", [])

    user_text = state.get("user_text", "")
    language = state.get("language", "hi")
    current_answers = dict(state.get("eligibility_answers") or {})

    # Reconstruct previous facts from history if available
    for turn in history:
        t_text = getattr(turn, "text", "") if hasattr(turn, "text") else turn.get("text", "")
        role = getattr(turn, "role", "") if hasattr(turn, "role") else turn.get("role", "")
        if role == "user":
            current_answers = _extract_answers_heuristically(t_text, current_answers)

    # Accumulate facts from current turn
    current_answers = _extract_answers_heuristically(user_text, current_answers)

    # Determine scheme context
    scheme_id = state.get("scheme_id")
    cleaned_text = user_text.lower()
    if any(w in cleaned_text for w in ["उज्ज्वला", "pmuy", "ujjwala", "lpg", "गैस"]):
        scheme_id = "pmuy"
    elif not scheme_id and history:
        # Preserve active PMUY context if ongoing interview
        scheme_id = "pmuy"

    intent = "scheme_query"
    if scheme_id == "pmuy" and current_answers:
        intent = "eligibility_interview"

    # Attempt Gemini Lite extraction if credentials are configured
    if settings.gemini_api_key and settings.gemini_model_lite:
        try:
            history_summary = "\n".join(
                f"{getattr(t, 'role', 'turn')}: {getattr(t, 'text', '')}"
                for t in history[-4:]
            )
            prompt = INTENT_SCHEME_USER_PROMPT_TEMPLATE.format(
                language=language,
                history_summary=history_summary or "None",
                user_text=user_text,
            )
            extracted_json = await gemini_client.generate_json(
                tier=ModelTier.LITE,
                prompt=prompt,
                system_instruction=INTENT_SCHEME_SYSTEM_INSTRUCTION,
            )
            if isinstance(extracted_json, dict):
                intent = extracted_json.get("intent", intent)
                scheme_id = extracted_json.get("scheme_id") or scheme_id
                ai_answers = extracted_json.get("extracted_answers", {})
                if isinstance(ai_answers, dict):
                    for k, v in ai_answers.items():
                        if v is not None:
                            current_answers[k] = v
        except Exception as exc:
            logger.debug("Gemini extraction skipped or failed: %s; using deterministic baseline", type(exc).__name__)

    return {
        "intent": intent,
        "scheme_id": scheme_id,
        "eligibility_answers": current_answers,
    }
