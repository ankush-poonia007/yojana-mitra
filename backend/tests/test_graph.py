"""Unit and integration tests for LangGraph orchestration and adapter seams."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.adapters import eligibility_adapter, retrieval_adapter, speech_adapter
from app.adapters.retrieval import RetrievalServiceError
from app.adapters.speech import STTUnavailableError
from app.graph.nodes.eligibility_seam import eligibility_seam_node
from app.graph.nodes.intent_classification import intent_classification_node
from app.graph.nodes.response_formatting import response_formatting_node
from app.graph.nodes.retrieval_seam import retrieval_seam_node
from app.graph.state import YojanaWorkflowState
from app.graph.workflow import compiled_workflow, run_turn_workflow
from app.llm.exceptions import LLMProviderError


# =====================================================================
# 1. State Contract Adherence (Strictly 11 Frozen Keys)
# =====================================================================

def test_workflow_state_contract_strictly_11_keys():
    """Verify YojanaWorkflowState contains strictly the 11 frozen keys from API contract §4.7."""
    frozen_keys = {
        "session_id",
        "language",
        "input_type",
        "user_text",
        "intent",
        "scheme_id",
        "eligibility_answers",
        "retrieved_evidence",
        "assessment",
        "response",
        "error",
    }
    actual_keys = set(YojanaWorkflowState.__annotations__.keys())
    assert actual_keys == frozen_keys, (
        f"State schema deviation! Difference: {actual_keys.symmetric_difference(frozen_keys)}"
    )


# =====================================================================
# 2. Eligibility Adapter Boundary Tests (Round 1 Remediation)
# =====================================================================

def test_eligibility_adapter_always_returns_cannot_determine_empty_answers():
    """Verify eligibility adapter returns cannot_determine with pending handoff message for empty answers."""
    result = eligibility_adapter.evaluate(scheme_id="pmuy", answers={})
    assert result["result"] == "cannot_determine"
    assert "नियम इंजन एकीकरण लंबित है" in result["reasons"][0]
    assert "preliminary_answers" in result["missing_information"]


def test_eligibility_adapter_never_evaluates_rules_or_returns_likely_eligible():
    """Verify eligibility adapter never returns likely_eligible even with complete passing answers."""
    answers = {
        "household_has_lpg": False,
        "applicant_is_woman": True,
        "age_18_or_above": True,
    }
    result = eligibility_adapter.evaluate(scheme_id="pmuy", answers=answers)
    assert result["result"] == "cannot_determine"
    assert result["result"] != "likely_eligible"
    assert "नियम इंजन एकीकरण लंबित है" in result["reasons"][0]


def test_eligibility_adapter_never_evaluates_rules_or_returns_likely_not_eligible():
    """Verify eligibility adapter never evaluates R01/R03 disqualifications in Round 1 stub."""
    disqualifying_answers = {
        "household_has_lpg": True,
        "applicant_is_woman": False,
        "age_18_or_above": False,
    }
    result = eligibility_adapter.evaluate(scheme_id="pmuy", answers=disqualifying_answers)
    assert result["result"] == "cannot_determine"
    assert result["result"] != "likely_not_eligible"
    assert "नियम इंजन एकीकरण लंबित है" in result["reasons"][0]


@pytest.mark.asyncio
async def test_eligibility_seam_node_returns_cannot_determine():
    """Verify Phase B node always returns cannot_determine through the adapter seam."""
    state: YojanaWorkflowState = {
        "session_id": "ses_test_elig",
        "language": "hi",
        "input_type": "text",
        "user_text": "क्या मैं पात्र हूँ?",
        "intent": "eligibility_interview",
        "scheme_id": "pmuy",
        "eligibility_answers": {"household_has_lpg": True},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    result = await eligibility_seam_node(state)
    assert result["assessment"] is not None
    assert result["assessment"]["result"] == "cannot_determine"
    assert "नियम इंजन एकीकरण लंबित है" in result["assessment"]["reasons"][0]


# =====================================================================
# 3. Retrieval Adapter Boundary Tests (Round 1 Remediation)
# =====================================================================

def test_retrieval_adapter_returns_empty_evidence_without_fabrication():
    """Verify retrieval adapter returns empty evidence [] with zero fabricated citations or URLs."""
    result = retrieval_adapter.search(query="उज्ज्वला योजना के नियम क्या हैं?", scheme_id="pmuy")
    assert result == []


@pytest.mark.asyncio
async def test_retrieval_seam_node_returns_empty_evidence():
    """Verify Phase C node passes empty evidence list [] into state."""
    state: YojanaWorkflowState = {
        "session_id": "ses_test_ret",
        "language": "hi",
        "input_type": "text",
        "user_text": "योजना के दिशानिर्देश बताएं",
        "intent": "scheme_query",
        "scheme_id": "pmuy",
        "eligibility_answers": {},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    result = await retrieval_seam_node(state)
    assert result["retrieved_evidence"] == []


# =====================================================================
# 4. Speech Adapter Boundary Tests (Round 1 Remediation)
# =====================================================================

def test_speech_adapter_availability_flags_report_pending():
    """Verify speech adapter flags report STT and TTS as not live in Round 1."""
    assert speech_adapter.is_stt_available is False
    assert speech_adapter.is_tts_available is False


@pytest.mark.asyncio
async def test_speech_adapter_transcribe_raises_stt_unavailable():
    """Verify speech adapter raises STTUnavailableError ensuring zero fake speech claims."""
    with pytest.raises(STTUnavailableError, match="Speech-to-text provider integration is pending"):
        await speech_adapter.transcribe(b"fake_audio_bytes", language="hi")


@pytest.mark.asyncio
async def test_speech_adapter_synthesizes_placeholder_audio():
    """Verify speech adapter produces contract placeholder string without claiming genuine synthesis."""
    audio_b64 = await speech_adapter.synthesize("नमस्ते", language="hi")
    assert audio_b64 == "DEMO_AUDIO_DATA"


# =====================================================================
# 5. Intent and History Recovery Tests
# =====================================================================

@pytest.mark.asyncio
async def test_intent_classification_node_extracts_facts_and_scheme():
    """Verify Phase A extracts scheme and dialogue facts from user text."""
    state: YojanaWorkflowState = {
        "session_id": "ses_test01",
        "language": "hi",
        "input_type": "text",
        "user_text": "मैं 25 वर्ष की महिला हूँ और मुझे उज्ज्वला गैस चाहिए, घर में गैस नहीं है",
        "intent": "scheme_query",
        "scheme_id": None,
        "eligibility_answers": {},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    result = await intent_classification_node(state)
    assert result["scheme_id"] == "pmuy"
    answers = result["eligibility_answers"]
    assert answers.get("applicant_is_woman") is True
    assert answers.get("age_18_or_above") is True
    assert answers.get("household_has_lpg") is False


@pytest.mark.asyncio
async def test_intent_classification_recovers_facts_from_runtime_history():
    """Verify Phase A accumulates prior dialogue facts passed via RunnableConfig history."""
    class FakeTurn:
        def __init__(self, role: str, text: str):
            self.role = role
            self.text = text

    history = [
        FakeTurn("user", "नमस्ते, मैं 22 वर्ष की महिला हूँ"),
        FakeTurn("assistant", "क्या आपके घर में पहले से कोई गैस कनेक्शन है?"),
    ]

    state: YojanaWorkflowState = {
        "session_id": "ses_test02",
        "language": "hi",
        "input_type": "text",
        "user_text": "नहीं, हमारे घर में गैस नहीं है",
        "intent": "scheme_query",
        "scheme_id": "pmuy",
        "eligibility_answers": {},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    config = {"configurable": {"history": history}}
    result = await intent_classification_node(state, config=config)

    answers = result["eligibility_answers"]
    assert answers.get("applicant_is_woman") is True
    assert answers.get("age_18_or_above") is True
    assert answers.get("household_has_lpg") is False


# =====================================================================
# 6. Response Formatting Node Tests
# =====================================================================

@pytest.mark.asyncio
async def test_response_formatting_node_empty_evidence_produces_refusal():
    """Verify Phase D formats an unsupported-answer refusal when evidence is empty."""
    state: YojanaWorkflowState = {
        "session_id": "ses_test06",
        "language": "hi",
        "input_type": "text",
        "user_text": "मुझे योजना के बारे में बताएं",
        "intent": "scheme_query",
        "scheme_id": "pmuy",
        "eligibility_answers": {},
        "assessment": {
            "result": "cannot_determine",
            "reasons": ["पात्रता निर्धारण के लिए नियम इंजन एकीकरण लंबित है।"],
            "missing_information": [],
            "scheme_id": "pmuy",
        },
        "retrieved_evidence": [],
        "response": {},
        "error": None,
    }

    with patch("app.graph.nodes.response_formatting.settings.gemini_api_key", None):
        result = await response_formatting_node(state)

    resp = result["response"]
    assert resp["status"] == "awaiting_information"
    assert "सत्यापित आधिकारिक योजना दिशानिर्देश अभी उपलब्ध नहीं हैं" in resp["answer"]["text"]
    assert resp["sources"] == []
    assert resp["card"] is None
    assert resp["speech"]["audio_base64"] == "DEMO_AUDIO_DATA"


@pytest.mark.asyncio
async def test_response_formatting_node_english_refusal():
    """Verify Phase D produces English unsupported-answer refusal when language is 'en'."""
    state: YojanaWorkflowState = {
        "session_id": "ses_test_en",
        "language": "en",
        "input_type": "text",
        "user_text": "Tell me about PMUY guidelines",
        "intent": "scheme_query",
        "scheme_id": "pmuy",
        "eligibility_answers": {},
        "assessment": {
            "result": "cannot_determine",
            "reasons": ["Rule engine pending."],
            "missing_information": [],
            "scheme_id": "pmuy",
        },
        "retrieved_evidence": [],
        "response": {},
        "error": None,
    }

    with patch("app.graph.nodes.response_formatting.settings.gemini_api_key", None):
        result = await response_formatting_node(state)

    resp = result["response"]
    assert resp["status"] == "awaiting_information"
    assert "Verified official scheme guidelines are not currently available" in resp["answer"]["text"]
    assert resp["sources"] == []
    assert resp["card"] is None


@pytest.mark.asyncio
async def test_response_formatting_node_with_gemini_polishing():
    """Verify Phase D invokes Gemini polishing when API key is configured."""
    state: YojanaWorkflowState = {
        "session_id": "ses_test_gemini",
        "language": "hi",
        "input_type": "text",
        "user_text": "योजना की जानकारी",
        "intent": "scheme_query",
        "scheme_id": "pmuy",
        "eligibility_answers": {},
        "assessment": {
            "result": "cannot_determine",
            "reasons": ["Rule engine pending."],
            "missing_information": [],
            "scheme_id": "pmuy",
        },
        "retrieved_evidence": [],
        "response": {},
        "error": None,
    }

    with patch("app.graph.nodes.response_formatting.settings.gemini_api_key", "test_key"), \
         patch("app.graph.nodes.response_formatting.gemini_client.generate", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = "आधिकारिक दिशानिर्देश उपलब्ध नहीं हैं। कृपया ग्राम पंचायत से संपर्क करें।"
        result = await response_formatting_node(state)

    resp = result["response"]
    assert "आधिकारिक दिशानिर्देश उपलब्ध नहीं हैं" in resp["answer"]["text"]
    assert resp["sources"] == []
    assert resp["card"] is None


# =====================================================================
# 7. End-to-End Workflow Execution & Outage Distinction Tests
# =====================================================================

@pytest.mark.asyncio
async def test_run_turn_workflow_full_pipeline_success():
    """Verify complete 4-phase graph execution succeeds with refusal on empty evidence."""
    initial_state: YojanaWorkflowState = {
        "session_id": "ses_e2e01",
        "language": "hi",
        "input_type": "text",
        "user_text": "नमस्ते, मुझे उज्ज्वला गैस कनेक्शन के बारे में जानना है",
        "intent": "scheme_query",
        "scheme_id": None,
        "eligibility_answers": {},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    with patch("app.graph.nodes.response_formatting.gemini_client.generate", new_callable=AsyncMock) as mock_gen:
        mock_gen.return_value = "इस विषय पर आधिकारिक योजना दिशानिर्देश उपलब्ध नहीं हैं। कृपया ग्राम पंचायत से संपर्क करें।"
        final_state = await run_turn_workflow(initial_state)

    assert final_state["scheme_id"] == "pmuy"
    assert final_state["assessment"]["result"] == "cannot_determine"
    assert final_state["response"]["status"] == "awaiting_information"
    assert final_state["response"]["sources"] == []
    assert final_state["response"]["card"] is None
    assert final_state["error"] is None


@pytest.mark.asyncio
async def test_run_turn_workflow_deterministic_fallback_when_gemini_unavailable():
    """Verify response formatting falls back cleanly to deterministic refusal if Gemini fails."""
    initial_state: YojanaWorkflowState = {
        "session_id": "ses_e2e_fallback",
        "language": "hi",
        "input_type": "text",
        "user_text": "हमारे पास पहले से गैस कनेक्शन है",
        "intent": "eligibility_interview",
        "scheme_id": "pmuy",
        "eligibility_answers": {},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    with patch("app.graph.nodes.response_formatting.gemini_client.generate", side_effect=RuntimeError("LLM unavailable")):
        final_state = await run_turn_workflow(initial_state)

    assert final_state["assessment"]["result"] == "cannot_determine"
    assert final_state["response"]["status"] == "awaiting_information"
    assert "सत्यापित आधिकारिक योजना दिशानिर्देश अभी उपलब्ध नहीं हैं" in final_state["response"]["answer"]["text"]
    assert final_state["response"]["sources"] == []
    assert final_state["response"]["card"] is None


@pytest.mark.asyncio
async def test_run_turn_workflow_retrieval_outage_distinct_from_empty_evidence():
    """Verify retrieval infrastructure failure raises distinct AI_SERVICE_UNAVAILABLE error envelope."""
    initial_state: YojanaWorkflowState = {
        "session_id": "ses_e2e_ret_fail",
        "language": "hi",
        "input_type": "text",
        "user_text": "योजना के बारे में जानकारी दें",
        "intent": "scheme_query",
        "scheme_id": "pmuy",
        "eligibility_answers": {},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    with patch("app.graph.nodes.retrieval_seam.retrieval_adapter.search", side_effect=RetrievalServiceError("Vector DB down")):
        result_state = await run_turn_workflow(initial_state)

    assert result_state["error"] is not None
    assert result_state["error"]["code"] == "AI_SERVICE_UNAVAILABLE"
    assert result_state["error"]["retryable"] is True
    assert "Knowledge retrieval is temporarily unavailable" in result_state["error"]["message"]


@pytest.mark.asyncio
async def test_run_turn_workflow_llm_provider_error_maps_to_ai_service_unavailable():
    """Verify LLM provider failure during graph execution sets AI_SERVICE_UNAVAILABLE in state."""
    initial_state: YojanaWorkflowState = {
        "session_id": "ses_e2e_llm_err",
        "language": "hi",
        "input_type": "text",
        "user_text": "Test error",
        "intent": "scheme_query",
        "scheme_id": None,
        "eligibility_answers": {},
        "retrieved_evidence": [],
        "assessment": None,
        "response": {},
        "error": None,
    }

    with patch.object(compiled_workflow, "ainvoke", side_effect=LLMProviderError("Google API down")):
        result_state = await run_turn_workflow(initial_state)

    assert result_state["error"] is not None
    assert result_state["error"]["code"] == "AI_SERVICE_UNAVAILABLE"
    assert result_state["error"]["retryable"] is True
