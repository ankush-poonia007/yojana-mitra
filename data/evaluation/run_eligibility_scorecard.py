#!/usr/bin/env python3
"""EV-A: PMUY Deterministic Eligibility Scorecard.

Owned by Anamika.

Loads PMUY eligibility test cases from data/evaluation/eligibility_cases.jsonl
and runs each through the deterministic eligibility engine.

Usage (from repository root):
    python data/evaluation/run_eligibility_scorecard.py

Or from backend/:
    python -m app.eligibility.engine   # (for import path)
    cd ..  # back to repo root, then run the script

Requirements:
    - Python 3.11+
    - No network, no database, no LLM, no new dependencies.
    - Runs entirely offline.

Exit codes:
    0 — all cases pass
    1 — one or more cases fail or the fixture file is missing/malformed

IMPORTANT:
    - Cases marked "provisional": true are constructed from the local test
      suite and have NOT been independently verified against the official
      PMUY-T01 through PMUY-T12 artifact. They must be replaced or confirmed
      once the authoritative case definitions are available.
    - Passing this scorecard does NOT prove official-source currency or
      that the rules match the current PMUY guidelines.
    - All proposed thresholds are PROPOSED — TEAM APPROVAL REQUIRED.
    - This script does not make or override eligibility decisions; it only
      calls the deterministic engine and compares results.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path setup: allow running from repo root OR from backend/
# ---------------------------------------------------------------------------

_SCRIPT_DIR = Path(__file__).resolve().parent          # data/evaluation/
_REPO_ROOT = _SCRIPT_DIR.parent.parent                 # yojana-mitra/
_BACKEND_DIR = _REPO_ROOT / "backend"

if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

try:
    from app.eligibility.engine import evaluate_pmuy_eligibility
    from app.eligibility.models import EligibilityResult, PMUYAnswers
except ImportError as exc:
    print(
        f"ERROR: Cannot import eligibility engine.\n"
        f"  {exc}\n"
        f"  Ensure you have installed backend/requirements.txt dependencies.\n"
        f"  Tried path: {_BACKEND_DIR}",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FIXTURE_PATH = _SCRIPT_DIR / "eligibility_cases.jsonl"

# PROPOSED thresholds — not approved by the team; do not present as official.
_PROPOSED_PASS_THRESHOLD = 1.0   # 100% — all cases must pass for the deterministic engine
_THRESHOLD_LABEL = "PROPOSED — TEAM APPROVAL REQUIRED"


# ---------------------------------------------------------------------------
# Case loading
# ---------------------------------------------------------------------------

def load_cases(path: Path) -> list[dict[str, Any]]:
    """Load and parse all cases from the JSONL fixture file."""
    if not path.exists():
        print(f"ERROR: Fixture file not found: {path}", file=sys.stderr)
        sys.exit(1)

    cases: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                print(
                    f"ERROR: Malformed JSON on line {lineno} of {path}:\n  {exc}",
                    file=sys.stderr,
                )
                sys.exit(1)

            for required_field in ("case_id", "inputs", "expected_result"):
                if required_field not in obj:
                    print(
                        f"ERROR: Line {lineno} missing required field '{required_field}'.",
                        file=sys.stderr,
                    )
                    sys.exit(1)

            cases.append(obj)

    if not cases:
        print(f"ERROR: No cases found in {path}.", file=sys.stderr)
        sys.exit(1)

    return cases


# ---------------------------------------------------------------------------
# Case runner
# ---------------------------------------------------------------------------

def run_case(case: dict[str, Any]) -> dict[str, Any]:
    """Run a single case through the engine and return a result record.

    Never raises — all errors are caught and recorded as failures.
    Does NOT modify eligibility decisions; only records the engine output.
    """
    case_id = case["case_id"]
    inputs = case["inputs"]
    expected_result_str = case["expected_result"]
    expected_triggered = set(case.get("expected_triggered_rules", []))
    expected_missing = set(case.get("expected_missing", []))

    # Validate expected result is a known enum value
    try:
        expected_result = EligibilityResult(expected_result_str)
    except ValueError:
        return {
            "case_id": case_id,
            "passed": False,
            "error": f"Fixture error: unknown expected_result value '{expected_result_str}'.",
            "actual_result": None,
            "expected_result": expected_result_str,
            "actual_triggered": [],
            "actual_missing": [],
        }

    # Validate inputs against PMUYAnswers schema
    try:
        # null values in JSON become None in Python — engine must handle them
        validated = PMUYAnswers.model_validate(inputs)
    except Exception as exc:  # noqa: BLE001
        return {
            "case_id": case_id,
            "passed": False,
            "error": f"Input validation error: {exc}",
            "actual_result": None,
            "expected_result": expected_result_str,
            "actual_triggered": [],
            "actual_missing": [],
        }

    # Call the engine — deterministic, no side effects
    try:
        assessment = evaluate_pmuy_eligibility(validated, language="en")
    except Exception as exc:  # noqa: BLE001
        return {
            "case_id": case_id,
            "passed": False,
            "error": f"Engine raised an exception: {exc}",
            "actual_result": None,
            "expected_result": expected_result_str,
            "actual_triggered": [],
            "actual_missing": [],
        }

    actual_result = assessment.result
    actual_triggered = set(assessment.triggered_rules)
    actual_missing = set(assessment.missing_information)

    # --- Safety invariant check ---
    # Unknown/None inputs must NEVER silently produce likely_eligible
    # when the expected result is cannot_determine or likely_not_eligible.
    # This check is purely observational; the engine is the authority.

    failures: list[str] = []

    if actual_result != expected_result:
        failures.append(
            f"result mismatch: expected '{expected_result.value}', "
            f"got '{actual_result.value}'"
        )

    if expected_triggered and not expected_triggered.issubset(actual_triggered):
        missing_triggers = expected_triggered - actual_triggered
        failures.append(
            f"expected triggered rules not found: {sorted(missing_triggers)}"
        )

    if expected_missing and not expected_missing.issubset(actual_missing):
        missing_from_missing = expected_missing - actual_missing
        failures.append(
            f"expected missing_information keys not found: {sorted(missing_from_missing)}"
        )

    return {
        "case_id": case_id,
        "passed": len(failures) == 0,
        "error": "; ".join(failures) if failures else None,
        "actual_result": actual_result.value,
        "expected_result": expected_result_str,
        "actual_triggered": sorted(actual_triggered),
        "actual_missing": sorted(actual_missing),
    }


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------

def print_report(results: list[dict[str, Any]], provisional_count: int) -> int:
    """Print the scorecard report and return 0 (all pass) or 1 (any fail)."""

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    pass_rate = passed / total if total > 0 else 0.0

    # Count by expected result
    dist: dict[str, int] = {}
    for r in results:
        key = r["expected_result"]
        dist[key] = dist.get(key, 0) + 1

    print()
    print("=" * 66)
    print("  PMUY Eligibility Scorecard (EV-A)")
    print("=" * 66)
    print(f"  Fixture:     {FIXTURE_PATH.name}")
    print(f"  Total cases: {total}  "
          f"(provisional: {provisional_count} — pending official T01-T12 confirmation)")
    print()
    print("  Case distribution:")
    for outcome, count in sorted(dist.items()):
        print(f"    {outcome:<30} {count}")
    print()

    # Per-case results
    print("  Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        marker = "  " if r["passed"] else "! "
        print(f"  {marker}{status}  {r['case_id']:<12} -> {r['actual_result'] or 'ERROR'}")
        if not r["passed"] and r["error"]:
            print(f"           {r['error']}")

    print()
    print("-" * 66)
    print(f"  Passed:    {passed}/{total}")
    print(f"  Failed:    {failed}/{total}")
    print(f"  Pass rate: {pass_rate:.1%}")
    print()
    print(f"  Proposed threshold: {_PROPOSED_PASS_THRESHOLD:.0%}")
    print(f"  Threshold status:   {_THRESHOLD_LABEL}")
    print()

    if failed == 0:
        print("  STATUS: ALL CASES PASS")
    else:
        print(f"  STATUS: {failed} CASE(S) FAILED — review failures above")

    print("=" * 66)
    print()

    return 0 if failed == 0 else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Run the scorecard and return an exit code."""

    cases = load_cases(FIXTURE_PATH)

    # Count provisional cases for the report header
    provisional_count = sum(1 for c in cases if c.get("provisional", False))

    results = [run_case(case) for case in cases]

    exit_code = print_report(results, provisional_count)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
