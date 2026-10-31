"""Phase B: Eligibility Integration Seam Node (H3 Seam)."""
from __future__ import annotations

import logging
from typing import Any, Optional
from langchain_core.runnables import RunnableConfig

from app.adapters import eligibility_adapter
from app.graph.state import YojanaWorkflowState

logger = logging.getLogger(__name__)


async def eligibility_seam_node(
    state: YojanaWorkflowState,
    config: Optional[RunnableConfig] = None,
) -> dict[str, Any]:
    """Execute Phase B: Evaluate eligibility answers using H3 adapter seam."""
    scheme_id = state.get("scheme_id")
    answers = state.get("eligibility_answers") or {}

    if not scheme_id or scheme_id != "pmuy":
        return {
            "assessment": None,
        }

    # Delegate exclusively to deterministic eligibility adapter
    assessment = eligibility_adapter.evaluate(scheme_id=scheme_id, answers=answers)
    return {
        "assessment": assessment,
    }
