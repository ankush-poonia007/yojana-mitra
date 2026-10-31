"""EV-C: Offline question-flow scenario evaluation for the PMUY QuestionBank.

Owned by Anamika.

Runs deterministic, offline scenarios against the actual QuestionBank and
PMUYAnswers interfaces.  No LLM, database, network, or new dependencies required.

Usage (from repo root):
    python data/evaluation/run_question_flow.py

Exit code: 0 if all scenarios pass, 1 if any scenario fails or an error occurs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Path setup — mirror run_eligibility_scorecard.py exactly
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # data/evaluation/ -> repo root
_BACKEND_DIR = _REPO_ROOT / "backend"
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.eligibility.models import PMUYAnswers  # noqa: E402
from app.eligibility.question_bank import QuestionBank  # noqa: E402

_SCENARIOS_FILE = Path(__file__).resolve().parent / "question_flow_scenarios.jsonl"

# ---------------------------------------------------------------------------
# Required fields for each test_type
# ---------------------------------------------------------------------------
_REQUIRED_COMMON = {"scenario_id", "description", "test_type", "provisional"}
_REQUIRED_BY_TYPE: dict[str, set[str]] = {
    "progression": {"setup_answers", "stop_on_exclusion", "expected_is_none"},
    "early_exit": {"setup_answers", "stop_on_exclusion", "expected_is_none"},
    "no_early_exit": {"setup_answers", "stop_on_exclusion", "expected_is_none"},
    "missing_safety": {"setup_answers", "stop_on_exclusion", "expected_is_none"},
    "readiness_separation": {"setup_answers", "stop_on_exclusion", "expected_is_none"},
    "lookup": {"lookup_id", "expected_question_id", "expected_stage", "expected_engine_field"},
    "localization": {"lookup_id"},
    "stage_listing": {"lookup_stage", "expected_count", "expected_first_engine_field", "expected_last_engine_field"},
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_scenarios(path: Path) -> list[dict[str, Any]]:
    """Parse JSONL scenarios; exit 1 on any parse error."""
    scenarios: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(f"FATAL: JSON parse error on line {lineno}: {exc}")
                sys.exit(1)
            missing_common = _REQUIRED_COMMON - set(obj.keys())
            if missing_common:
                print(
                    f"FATAL: Scenario on line {lineno} missing required fields: "
                    f"{sorted(missing_common)}"
                )
                sys.exit(1)
            test_type = obj.get("test_type", "")
            required_extra = _REQUIRED_BY_TYPE.get(test_type, set())
            missing_extra = required_extra - set(obj.keys())
            if missing_extra:
                print(
                    f"FATAL: Scenario '{obj.get('scenario_id')}' (type={test_type}) "
                    f"missing fields: {sorted(missing_extra)}"
                )
                sys.exit(1)
            scenarios.append(obj)
    return scenarios


# ---------------------------------------------------------------------------
# Individual scenario runners
# ---------------------------------------------------------------------------

def _build_answers(setup_answers: dict[str, Any]) -> PMUYAnswers:
    """Construct a PMUYAnswers from a raw dict; unknown keys are silently ignored."""
    return PMUYAnswers(**setup_answers)


def _run_progression_variant(
    scenario: dict[str, Any],
    bank: QuestionBank,
) -> tuple[bool, str]:
    """Handle progression, early_exit, no_early_exit, missing_safety, readiness_separation."""
    setup = scenario["setup_answers"]
    stop_on_exclusion: bool = scenario["stop_on_exclusion"]
    expected_is_none: bool = scenario["expected_is_none"]
    expected_qid: Optional[str] = scenario.get("expected_next_question_id")

    try:
        pmuy = _build_answers(setup)
    except Exception as exc:
        return False, f"PMUYAnswers construction failed: {exc}"

    try:
        result = bank.get_next_question(pmuy, stop_on_exclusion=stop_on_exclusion)
    except Exception as exc:
        return False, f"get_next_question raised unexpected exception: {exc}"

    if expected_is_none:
        if result is None:
            return True, "get_next_question returned None as expected"
        return False, (
            f"Expected None (interview complete or early exit) "
            f"but got question_id='{result.question_id}'"
        )
    else:
        if result is None:
            return False, (
                f"Expected question_id='{expected_qid}' "
                f"but got None (unexpected early termination)"
            )
        if result.question_id != expected_qid:
            return False, (
                f"Expected question_id='{expected_qid}' "
                f"but got '{result.question_id}'"
            )
        return True, f"get_next_question returned '{result.question_id}' as expected"


def _run_lookup(
    scenario: dict[str, Any],
    bank: QuestionBank,
) -> tuple[bool, str]:
    """Verify get_question() by ID."""
    lookup_id: str = scenario["lookup_id"]
    expected_qid: str = scenario["expected_question_id"]
    expected_stage: int = scenario["expected_stage"]
    expected_field: str = scenario["expected_engine_field"]

    q = bank.get_question(lookup_id)
    if q is None:
        return False, f"get_question('{lookup_id}') returned None (not found)"
    errors: list[str] = []
    if q.question_id != expected_qid:
        errors.append(f"question_id: expected '{expected_qid}', got '{q.question_id}'")
    if q.stage != expected_stage:
        errors.append(f"stage: expected {expected_stage}, got {q.stage}")
    if q.engine_field != expected_field:
        errors.append(f"engine_field: expected '{expected_field}', got '{q.engine_field}'")
    if errors:
        return False, "; ".join(errors)
    return True, f"get_question('{lookup_id}') returned correct definition"


def _run_stage_listing(
    scenario: dict[str, Any],
    bank: QuestionBank,
) -> tuple[bool, str]:
    """Verify get_stage_questions() count and order."""
    stage: int = scenario["lookup_stage"]
    expected_count: int = scenario["expected_count"]
    expected_first: str = scenario["expected_first_engine_field"]
    expected_last: str = scenario["expected_last_engine_field"]

    questions = bank.get_stage_questions(stage)
    errors: list[str] = []
    if len(questions) != expected_count:
        errors.append(
            f"count: expected {expected_count}, got {len(questions)}"
        )
    if questions and questions[0].engine_field != expected_first:
        errors.append(
            f"first engine_field: expected '{expected_first}', "
            f"got '{questions[0].engine_field}'"
        )
    if questions and questions[-1].engine_field != expected_last:
        errors.append(
            f"last engine_field: expected '{expected_last}', "
            f"got '{questions[-1].engine_field}'"
        )
    if errors:
        return False, "; ".join(errors)
    return True, (
        f"get_stage_questions({stage}) returned {len(questions)} questions "
        f"in correct order"
    )


def _run_localization(
    scenario: dict[str, Any],
    bank: QuestionBank,
) -> tuple[bool, str]:
    """Verify get_text() returns distinct non-empty English and Hindi strings."""
    lookup_id: str = scenario["lookup_id"]
    q = bank.get_question(lookup_id)
    if q is None:
        return False, f"get_question('{lookup_id}') returned None"

    text_en = q.get_text("en")
    text_hi = q.get_text("hi")
    errors: list[str] = []
    if not text_en:
        errors.append("English text is empty")
    if not text_hi:
        errors.append("Hindi text is empty")
    if text_en and text_hi and text_en == text_hi:
        errors.append(
            "English and Hindi texts are identical "
            "(localization not implemented or texts were not translated)"
        )
    if errors:
        return False, "; ".join(errors)
    return True, (
        f"get_text('en') and get_text('hi') both non-empty and distinct "
        f"for '{lookup_id}'"
    )


def run_scenario(
    scenario: dict[str, Any],
    bank: QuestionBank,
) -> tuple[bool, str]:
    """Dispatch to the correct sub-runner based on test_type."""
    test_type: str = scenario.get("test_type", "")
    dispatch = {
        "progression": _run_progression_variant,
        "early_exit": _run_progression_variant,
        "no_early_exit": _run_progression_variant,
        "missing_safety": _run_progression_variant,
        "readiness_separation": _run_progression_variant,
        "lookup": _run_lookup,
        "stage_listing": _run_stage_listing,
        "localization": _run_localization,
    }
    runner = dispatch.get(test_type)
    if runner is None:
        return False, f"Unknown test_type '{test_type}'; cannot run scenario"
    try:
        return runner(scenario, bank)
    except Exception as exc:
        return False, f"Unexpected runner error: {exc}"


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(results: list[tuple[dict[str, Any], bool, str]]) -> int:
    """Print per-scenario results and summary; return exit code."""
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = total - passed

    print()
    print("=" * 70)
    print("EV-C: Question-Flow Evaluation")
    print("=" * 70)
    for scenario, ok, detail in results:
        sid = scenario["scenario_id"]
        desc = scenario["description"]
        prov = "[PROVISIONAL] " if scenario.get("provisional") else ""
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {sid}: {desc}")
        if not ok:
            print(f"         Reason: {detail}")
        elif scenario.get("provisional"):
            print(f"         Note: {prov}result accepted pending team approval of fixtures")
    print()
    print(f"Results: {passed}/{total} passed")
    if failed:
        print(f"FAILED:  {failed} scenario(s)")
        print()
        print("EV-C status: FAIL")
        return 1
    print()
    print("EV-C status: PASS (all results provisional pending team approval)")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    """Load scenarios, run each against the live QuestionBank, report results."""
    if not _SCENARIOS_FILE.exists():
        print(f"FATAL: scenarios file not found: {_SCENARIOS_FILE}")
        return 1

    print(f"Loading scenarios from: {_SCENARIOS_FILE.name}")
    scenarios = load_scenarios(_SCENARIOS_FILE)
    print(f"Loaded {len(scenarios)} scenario(s).")

    try:
        bank = QuestionBank()
    except Exception as exc:
        print(f"FATAL: Failed to initialise QuestionBank: {exc}")
        return 1

    results: list[tuple[dict[str, Any], bool, str]] = []
    for scenario in scenarios:
        ok, detail = run_scenario(scenario, bank)
        results.append((scenario, ok, detail))

    return print_report(results)


if __name__ == "__main__":
    sys.exit(main())

