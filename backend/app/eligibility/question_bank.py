"""PMUY Question Bank and Four-Stage Interview Navigator.

Owned by Anamika.
Loads authoritative interview questions from data/schemes/pmuy/questions.json
and guides the conversational eligibility interview through Stages 1 to 4.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from app.eligibility.engine import evaluate_pmuy_eligibility
from app.eligibility.models import EligibilityResult, PMUYAnswers


class QuestionDefinition(BaseModel):
    """Pydantic model representing an authoritative PMUY interview question."""

    model_config = ConfigDict(extra="ignore")

    question_id: str
    stage: int
    stage_name: str
    order: int
    text_en: str
    text_hi: str
    help_text_en: str = ""
    help_text_hi: str = ""
    answer_type: str = "boolean"
    allowed_values: list[str] = Field(default_factory=list)
    engine_field: Optional[str] = None
    associated_rule: Optional[str] = None
    dimension: str = "eligibility"
    is_mandatory: bool = True
    is_exclusion_trigger_on: Optional[bool] = None

    def get_text(self, lang: str = "en") -> str:
        """Return localized question text (defaults to English if not Hindi)."""
        if lang and lang.lower().startswith("hi"):
            return self.text_hi
        return self.text_en

    def get_help_text(self, lang: str = "en") -> str:
        """Return localized help text (defaults to English if not Hindi)."""
        if lang and lang.lower().startswith("hi"):
            return self.help_text_hi
        return self.help_text_en


class QuestionBank:
    """Manages the PMUY question catalog and guides sequential interview progression."""

    def __init__(self, data_path: Optional[Union[str, Path]] = None) -> None:
        """Initialize QuestionBank, resolving questions.json path automatically if omitted."""
        if data_path is not None:
            resolved_path = Path(data_path)
        else:
            resolved_path = self._resolve_default_path()

        if not resolved_path.exists():
            raise FileNotFoundError(f"PMUY questions file not found at: {resolved_path}")

        with open(resolved_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._questions: list[QuestionDefinition] = [
            QuestionDefinition.model_validate(q) for q in data
        ]
        # Sort questions strictly by stage, then order
        self._questions.sort(key=lambda q: (q.stage, q.order))

        self._by_id: dict[str, QuestionDefinition] = {
            q.question_id: q for q in self._questions
        }
        self._by_stage: dict[int, list[QuestionDefinition]] = {}
        for q in self._questions:
            self._by_stage.setdefault(q.stage, []).append(q)

    @staticmethod
    def _resolve_default_path() -> Path:
        """Resolve path to data/schemes/pmuy/questions.json across execution contexts."""
        # Relative to this file: backend/app/eligibility/question_bank.py -> repo root is 3 parents up
        repo_root = Path(__file__).resolve().parents[3]
        candidate = repo_root / "data" / "schemes" / "pmuy" / "questions.json"
        if candidate.exists():
            return candidate

        # Fallbacks for current working directory or subdirectories
        cwd = Path.cwd()
        for candidate_path in [
            cwd / "data" / "schemes" / "pmuy" / "questions.json",
            cwd.parent / "data" / "schemes" / "pmuy" / "questions.json",
            cwd / ".." / "data" / "schemes" / "pmuy" / "questions.json",
        ]:
            if candidate_path.exists():
                return candidate_path.resolve()

        return candidate

    def get_all_questions(self) -> list[QuestionDefinition]:
        """Return all 21 questions in sequential order."""
        return list(self._questions)

    def get_question(self, question_id: str) -> Optional[QuestionDefinition]:
        """Look up a single question definition by ID (e.g. 'PMUY-Q01')."""
        return self._by_id.get(question_id)

    def get_stage_questions(self, stage: int) -> list[QuestionDefinition]:
        """Return all questions belonging to a specific interview stage (1, 2, 3, or 4)."""
        return list(self._by_stage.get(stage, []))

    def get_next_question(
        self,
        current_answers: Union[PMUYAnswers, dict[str, Any]],
        stop_on_exclusion: bool = True,
    ) -> Optional[QuestionDefinition]:
        """Determine the next unanswered question in the interview sequence.

        Args:
            current_answers: Current collected answers as PMUYAnswers model or dictionary.
            stop_on_exclusion: If True, evaluates eligibility first. If the applicant
                is likely_not_eligible (hit a hard exclusion), returns None to stop
                interrogating the applicant early.

        Returns:
            The next QuestionDefinition to present, or None if the interview is complete
            or early-terminated due to disqualification.
        """
        # Normalize inputs
        if isinstance(current_answers, dict):
            raw_answers: dict[str, Any] = dict(current_answers)
            try:
                pmuy_obj = PMUYAnswers(**current_answers)
            except Exception:
                pmuy_obj = None
        elif isinstance(current_answers, PMUYAnswers):
            pmuy_obj = current_answers
            raw_answers = current_answers.model_dump()
            # applies_in_own_name is a declared field on PMUYAnswers; model_dump() above
            # already captures it.  No extra lookup needed.
        else:
            raw_answers = {}
            pmuy_obj = None

        # Early exit check: if hard exclusion triggered and stop_on_exclusion is True
        if stop_on_exclusion and pmuy_obj is not None:
            eval_result = evaluate_pmuy_eligibility(pmuy_obj)
            if eval_result.result == EligibilityResult.LIKELY_NOT_ELIGIBLE:
                return None

        # Sequential scan through questions in order
        for q in self._questions:
            if not q.engine_field:
                continue

            val = raw_answers.get(q.engine_field)

            # Special case for age: synchronized model provides age_18_or_above if applicant_age set
            if q.engine_field == "age_18_or_above" and val is None and pmuy_obj is not None:
                val = pmuy_obj.age_18_or_above

            if val is None:
                return q

        return None

