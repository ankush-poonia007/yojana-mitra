"""EV-D: Master P0 Scorecard — integrates all offline evaluation runners.

Owned by Anamika.

Detects which offline evaluation runners are present, executes each one,
and reports a unified P0 status.  Never treats a missing or unexecuted
runner as PASS.

Statuses used:
    PASS              - runner executed and exited 0
    FAIL              - runner executed and exited non-zero
    NOT IMPLEMENTED   - runner script does not exist yet
    BLOCKED           - depends on infrastructure not yet available (H4, live LLM, speech)
    PROVISIONAL       - runner executed and passed but fixtures are explicitly marked provisional

Usage (from repo root):
    python data/evaluation/run_scorecard.py

Exit code: 0 if all *executed* runners passed, 1 if any executed runner failed.
NOT IMPLEMENTED and BLOCKED entries do not affect the exit code.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_EVAL_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _EVAL_DIR.parent.parent

# Descriptions used in the report table
_BLOCKED_H4 = "BLOCKED (H4 chunk schema unresolved + source files not downloaded)"
_BLOCKED_LLM = "BLOCKED (live Gemini API required; not available in offline eval)"
_BLOCKED_STT = "BLOCKED (speech wrappers not yet built)"


# ---------------------------------------------------------------------------
# Runner registry
# ---------------------------------------------------------------------------

@dataclass
class RunnerEntry:
    label: str                        # e.g. "EV-A"
    description: str                  # one-line human description
    script: Optional[Path]            # None -> permanently blocked
    blocked_reason: Optional[str] = None  # set when script is None
    result: Optional[str] = field(default=None, init=False)
    detail: Optional[str] = field(default=None, init=False)
    exit_code: Optional[int] = field(default=None, init=False)


def _build_registry() -> list[RunnerEntry]:
    return [
        RunnerEntry(
            label="EV-A",
            description="Eligibility correctness",
            script=_EVAL_DIR / "run_eligibility_scorecard.py",
        ),
        RunnerEntry(
            label="EV-B",
            description="Normalizer safety",
            script=_EVAL_DIR / "run_normalizer_check.py",
        ),
        RunnerEntry(
            label="EV-C",
            description="Question-flow progression",
            script=_EVAL_DIR / "run_question_flow.py",
        ),
        RunnerEntry(
            label="EV-D",
            description="Grounding / refusal",
            script=None,
            blocked_reason=_BLOCKED_H4,
        ),
        RunnerEntry(
            label="EV-E",
            description="LLM explanation quality",
            script=None,
            blocked_reason=_BLOCKED_LLM,
        ),
        RunnerEntry(
            label="EV-F",
            description="STT benchmark",
            script=None,
            blocked_reason=_BLOCKED_STT,
        ),
    ]


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def execute_runner(entry: RunnerEntry) -> None:
    """Run a single runner script and populate entry.result / detail / exit_code."""
    # Permanently blocked — no script to run
    if entry.script is None:
        entry.result = "BLOCKED"
        entry.detail = entry.blocked_reason
        return

    # Runner script not yet implemented
    if not entry.script.exists():
        entry.result = "NOT IMPLEMENTED"
        entry.detail = f"{entry.script.name} does not exist"
        return

    # Execute with the same Python interpreter
    try:
        proc = subprocess.run(
            [sys.executable, str(entry.script)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(_REPO_ROOT),
        )
        entry.exit_code = proc.returncode
    except Exception as exc:
        entry.result = "FAIL"
        entry.detail = f"Failed to launch {entry.script.name}: {exc}"
        entry.exit_code = -1
        return

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    if proc.returncode == 0:
        # Extract summary line from runner output (last non-empty status line)
        summary = _extract_summary(stdout) or "exit 0"
        # Runner passed but fixtures are provisional — label PROVISIONAL
        if "provisional" in stdout.lower():
            entry.result = "PROVISIONAL"
        else:
            entry.result = "PASS"
        entry.detail = summary
    else:
        entry.result = "FAIL"
        # Include last few lines of stderr/stdout for context
        combined = "\n".join(filter(None, [stdout, stderr]))
        last_lines = "\n".join(combined.splitlines()[-5:]) if combined else "(no output)"
        entry.detail = f"exit {proc.returncode}: {last_lines}"


def _extract_summary(stdout: str) -> str:
    """Pull the most informative summary line from runner stdout."""
    lines = [l.strip() for l in stdout.splitlines() if l.strip()]
    # Prefer lines containing "Results:" or "status:"
    for line in reversed(lines):
        lower = line.lower()
        if "results:" in lower or "status:" in lower or "passed" in lower:
            return line
    return lines[-1] if lines else ""


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

_STATUS_ORDER = ["PASS", "PROVISIONAL", "FAIL", "NOT IMPLEMENTED", "BLOCKED"]


def _overall_status(entries: list[RunnerEntry]) -> tuple[str, int]:
    """Derive the master status and process exit code from all entries."""
    executed = [e for e in entries if e.result in ("PASS", "PROVISIONAL", "FAIL")]
    any_fail = any(e.result == "FAIL" for e in executed)
    any_not_impl = any(e.result == "NOT IMPLEMENTED" for e in entries)
    any_blocked = any(e.result == "BLOCKED" for e in entries)
    any_provisional = any(e.result == "PROVISIONAL" for e in entries)

    if any_fail:
        overall = "FAIL"
        exit_code = 1
    elif any_provisional or any_not_impl or any_blocked:
        overall = "PASS WITH DOCUMENTED LIMITATIONS"
        exit_code = 0
    else:
        overall = "PASS"
        exit_code = 0

    return overall, exit_code


def print_report(entries: list[RunnerEntry]) -> int:
    """Print the master scorecard report and return exit code."""
    overall, exit_code = _overall_status(entries)

    print()
    print("=" * 70)
    print("EV-D: Master P0 Scorecard - Yojana Mitra Offline Evaluation")
    print("=" * 70)
    print()

    label_w = max(len(e.label) for e in entries)
    desc_w = max(len(e.description) for e in entries)

    for e in entries:
        status = e.result or "UNKNOWN"
        detail = e.detail or ""
        # Truncate long detail lines for readability
        if len(detail) > 60:
            detail = detail[:57] + "..."
        row = (
            f"  [{e.label:<{label_w}}] "
            f"{e.description:<{desc_w}}  "
            f"{status}"
        )
        if detail:
            row += f"  |  {detail}"
        print(row)

    print()
    print("-" * 70)
    print(f"  Overall: {overall}")
    print("-" * 70)
    print()

    # Caveats section
    caveats: list[str] = []
    for e in entries:
        if e.result == "PROVISIONAL":
            caveats.append(
                f"  * {e.label}: Fixtures are marked PROVISIONAL - "
                "team approval required before treating as ground truth."
            )
        elif e.result == "NOT IMPLEMENTED":
            caveats.append(f"  * {e.label}: Runner not yet implemented ({e.script.name if e.script else '?'}).")
        elif e.result == "BLOCKED":
            caveats.append(f"  * {e.label}: {e.detail}")
    if caveats:
        print("Caveats:")
        for c in caveats:
            print(c)
        print()

    return exit_code


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    entries = _build_registry()

    print("Running offline evaluation suite...")
    for entry in entries:
        label = entry.label
        if entry.script is None:
            print(f"  {label}: skipping (permanently blocked)")
        elif not entry.script.exists():
            print(f"  {label}: script not found, marking NOT IMPLEMENTED")
        else:
            print(f"  {label}: executing {entry.script.name} ...")
        execute_runner(entry)

    return print_report(entries)


if __name__ == "__main__":
    sys.exit(main())

