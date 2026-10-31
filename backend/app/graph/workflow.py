"""LangGraph workflow assembly and per-turn stateless execution pipeline."""
from __future__ import annotations

import logging
from typing import Any

from langgraph.graph import END, START, StateGraph

from app.adapters import RetrievalServiceError
from app.graph.nodes import (
    eligibility_seam_node,
    intent_classification_node,
    response_formatting_node,
    retrieval_seam_node,
)
from app.graph.state import YojanaWorkflowState
from app.llm.exceptions import LLMProviderError, LLMQuotaExceededError

logger = logging.getLogger(__name__)


def build_yojana_workflow() -> Any:
    """Build and compile the 4-phase functional LangGraph pipeline."""
    workflow = StateGraph(YojanaWorkflowState)

    # 1. Register the 4 functional phase nodes
    workflow.add_node("intent_classification", intent_classification_node)
    workflow.add_node("eligibility_seam", eligibility_seam_node)
    workflow.add_node("retrieval_seam", retrieval_seam_node)
    workflow.add_node("response_formatting", response_formatting_node)

    # 2. Add edges forming the functional turn pipeline
    workflow.add_edge(START, "intent_classification")
    workflow.add_edge("intent_classification", "eligibility_seam")
    workflow.add_edge("eligibility_seam", "retrieval_seam")
    workflow.add_edge("retrieval_seam", "response_formatting")
    workflow.add_edge("response_formatting", END)

    return workflow.compile()


# Singleton compiled graph instance for the application
compiled_workflow = build_yojana_workflow()


async def run_turn_workflow(
    initial_state: YojanaWorkflowState,
    history: list[Any] | None = None,
) -> YojanaWorkflowState:
    """Execute a single conversation turn through the stateless LangGraph workflow.

    History is passed as runtime configuration context, preserving the frozen 11-key state schema.
    """
    config = {
        "configurable": {
            "history": history or [],
        }
    }

    try:
        result_state = await compiled_workflow.ainvoke(initial_state, config=config)
        return result_state
    except (LLMProviderError, LLMQuotaExceededError) as exc:
        logger.warning("LLM provider error during turn workflow: %s", type(exc).__name__)
        err_state = dict(initial_state)
        err_state["error"] = {
            "code": "AI_SERVICE_UNAVAILABLE",
            "message": "The assistant is temporarily unavailable. Please try again or use text input later.",
            "retryable": True,
            "details": {},
        }
        return err_state  # type: ignore[return-value]
    except RetrievalServiceError as exc:
        logger.error("Retrieval infrastructure error during turn workflow: %s", type(exc).__name__)
        err_state = dict(initial_state)
        err_state["error"] = {
            "code": "AI_SERVICE_UNAVAILABLE",
            "message": "Knowledge retrieval is temporarily unavailable. Please try again.",
            "retryable": True,
            "details": {},
        }
        return err_state  # type: ignore[return-value]
    except Exception as exc:
        logger.exception("Unexpected exception inside LangGraph workflow: %s", type(exc).__name__)
        err_state = dict(initial_state)
        err_state["error"] = {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An internal workflow error occurred.",
            "retryable": False,
            "details": {},
        }
        return err_state  # type: ignore[return-value]

