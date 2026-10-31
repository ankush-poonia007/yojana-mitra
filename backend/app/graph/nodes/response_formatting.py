"""Phase D: Response Formatting Node."""
from __future__ import annotations

import json
import logging
from typing import Any, Optional
from langchain_core.runnables import RunnableConfig

from app.adapters import speech_adapter
from app.core.config import settings
from app.graph.state import YojanaWorkflowState
from app.llm import ModelTier, gemini_client
from app.llm.prompts import (
    RESPONSE_FORMATTING_SYSTEM_INSTRUCTION,
    RESPONSE_FORMATTING_USER_PROMPT_TEMPLATE,
)

logger = logging.getLogger(__name__)


async def response_formatting_node(
    state: YojanaWorkflowState,
    config: Optional[RunnableConfig] = None,
) -> dict[str, Any]:
    """Execute Phase D: Format user-facing conversational answer, card, and sources."""
    language = state.get("language", "hi")
    scheme_id = state.get("scheme_id")
    assessment = state.get("assessment")
    evidence = state.get("retrieved_evidence") or []
    user_text = state.get("user_text", "")

    status = "awaiting_information"
    card = None
    sources: list[dict[str, Any]] = []

    # Map evidence chunks to SourceReference format without inventing fake defaults
    for chk in evidence:
        sources.append({
            "document_id": chk.get("document_id", ""),
            "title": chk.get("title", ""),
            "url": chk.get("source_url", ""),
            "page": chk.get("page", 1),
            "section": chk.get("section", ""),
        })

    # Default conversational answers based on state
    if not evidence:
        # Absence of verified evidence -> Explicit unsupported-answer refusal
        if language == "en":
            answer_text = (
                "Verified official scheme guidelines are not currently available for this topic. "
                "Please contact your local Gram Panchayat, Common Service Centre (CSC), or relevant government office."
            )
        else:
            answer_text = (
                "इस विषय पर सत्यापित आधिकारिक योजना दिशानिर्देश अभी उपलब्ध नहीं हैं। "
                "कृपया अपने नजदीकी ग्राम पंचायत, कॉमन सर्विस सेंटर (CSC) या संबंधित सरकारी कार्यालय से संपर्क करें।"
            )
        status = "awaiting_information"
    elif assessment and assessment.get("result") in {"likely_eligible", "likely_not_eligible"}:
        status = "completed"
        if language == "en":
            res_str = "likely eligible" if assessment["result"] == "likely_eligible" else "likely not eligible"
            reasons_str = " ".join(assessment.get("reasons", []))
            answer_text = f"Based on your answers, you are {res_str}. {reasons_str} Final verification will be conducted by the official distributor."
        else:
            res_str = "संभवतः पात्र हैं" if assessment["result"] == "likely_eligible" else "संभवतः पात्र नहीं हैं"
            reasons_str = " ".join(assessment.get("reasons", []))
            answer_text = f"आपके दिए गए उत्तरों के आधार पर आप {res_str}। {reasons_str} अंतिम पुष्टि अधिकृत वितरक द्वारा की जाएगी।"

        card = {
            "scheme_name": "प्रधानमंत्री उज्ज्वला योजना" if language == "hi" else "Pradhan Mantri Ujjwala Yojana",
            "documents": [
                "आधार कार्ड (Aadhaar Card)",
                "राशन कार्ड या परिवार संरचना प्रमाण (Ration Card or Family Composition Proof)",
                "बैंक पासबुक (Bank Passbook)",
            ],
            "where_to_apply": [
                "निकटतम LPG वितरक (Nearest LPG Distributor)",
                "Common Service Centre (CSC)",
            ],
            "disclaimer": "यह केवल प्रारंभिक पात्रता जानकारी है, आधिकारिक स्वीकृति नहीं।" if language == "hi" else "This is indicative eligibility information only, not an official government approval.",
        }
    elif assessment and assessment.get("missing_information"):
        missing = assessment["missing_information"]
        if "applicant_is_woman" in missing:
            answer_text = "क्या आवेदन करने वाली महिला हैं?" if language == "hi" else "Is the applicant a woman?"
        elif "household_has_lpg" in missing:
            answer_text = "क्या आपके घर में पहले से कोई LPG गैस कनेक्शन है?" if language == "hi" else "Does your household already have an LPG connection?"
        elif "age_18_or_above" in missing:
            answer_text = "क्या आवेदक की उम्र 18 वर्ष या उससे अधिक है?" if language == "hi" else "Is the applicant aged 18 years or older?"
        else:
            answer_text = "मैं आपकी पात्रता समझने में मदद करूंगा। क्या आपके घर में पहले से LPG कनेक्शन है?" if language == "hi" else "I will help you determine your eligibility. Does your household already have an LPG connection?"
    else:
        if language == "en":
            answer_text = "I will help you understand your eligibility for PMUY. Does your household already have an LPG connection?"
        else:
            answer_text = "मैं उज्ज्वला योजना के लिए आपकी पात्रता समझने में मदद करूंगा। क्या आपके घर में पहले से LPG कनेक्शन है?"

    # Polish response text with Gemini Lite if configured
    if settings.gemini_api_key and settings.gemini_model_lite:
        try:
            prompt = RESPONSE_FORMATTING_USER_PROMPT_TEMPLATE.format(
                language=language,
                scheme_id=scheme_id or "pmuy",
                assessment_json=json.dumps(assessment or {}),
                evidence_json=json.dumps(evidence),
                user_text=user_text,
            )
            polished = await gemini_client.generate(
                tier=ModelTier.LITE,
                prompt=prompt,
                system_instruction=RESPONSE_FORMATTING_SYSTEM_INSTRUCTION.format(language=language),
                temperature=0.3,
            )
            if polished and len(polished.strip()) > 10:
                answer_text = polished.strip()
        except Exception as exc:
            logger.debug("Gemini response polishing skipped: %s; using deterministic baseline", type(exc).__name__)

    audio_placeholder = await speech_adapter.synthesize(answer_text, language=language)

    response_payload = {
        "session_id": state.get("session_id", ""),
        "turn_id": "",  # Populated with assistant TurnRecord ID by TurnService
        "status": status,
        "language": language,
        "answer": {
            "text": answer_text,
        },
        "assessment": assessment,
        "card": card,
        "sources": sources,
        "speech": {
            "status": "generated",
            "content_type": "audio/mpeg",
            "audio_base64": audio_placeholder,
        },
    }

    return {
        "response": response_payload,
    }
