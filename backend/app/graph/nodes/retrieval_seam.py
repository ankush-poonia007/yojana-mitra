"""Phase C: Official-Source Retrieval and Grounding Seam Node (H4 Seam)."""
from __future__ import annotations

import logging
from typing import Any, Optional
from langchain_core.runnables import RunnableConfig

from app.adapters import retrieval_adapter
from app.graph.state import YojanaWorkflowState

logger = logging.getLogger(__name__)


async def retrieval_seam_node(
    state: YojanaWorkflowState,
    config: Optional[RunnableConfig] = None,
) -> dict[str, Any]:
    """Execute Phase C: Retrieve grounded evidence using H4 adapter seam."""
    user_text = state.get("user_text", "")
    scheme_id = state.get("scheme_id")

    # Search official documents through the retrieval adapter seam
    evidence = retrieval_adapter.search(query=user_text, scheme_id=scheme_id)
    return {
        "retrieved_evidence": evidence,
    }
