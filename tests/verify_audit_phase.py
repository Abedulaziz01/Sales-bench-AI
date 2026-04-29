"""
Verification checks for the Week 11 audit bundle.
Run with: python tests/verify_audit_phase.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "audit"

sys.path.insert(0, str(AUDIT_DIR))
import scoring_evaluator  # noqa: E402


def verify_audit_memo() -> None:
    memo_path = AUDIT_DIR / "audit_memo.md"
    text = memo_path.read_text(encoding="utf-8")
    words = len(text.split())
    probes = set(re.findall(r"PROBE-\d+", text))
    traces = set(re.findall(r"TRACE-\d+", text))

    assert words <= 600, f"audit_memo.md is {words} words; expected <= 600"
    assert len(probes) >= 8, f"Found {len(probes)} unique probes; expected >= 8"
    assert len(traces) >= 5, f"Found {len(traces)} unique traces; expected >= 5"


def verify_required_files() -> None:
    required = [
        AUDIT_DIR / "gap_analysis.md",
        AUDIT_DIR / "schema.json",
        AUDIT_DIR / "scoring_evaluator.py",
        AUDIT_DIR / "methodology.md",
    ]
    for path in required:
        assert path.exists(), f"Missing required file: {path}"


def verify_schema_examples() -> None:
    schema = json.loads((AUDIT_DIR / "schema.json").read_text(encoding="utf-8"))
    examples = schema["examples"]
    assert len(examples) == 3, f"Expected 3 schema examples; found {len(examples)}"

    for task in examples:
        result = scoring_evaluator.score_task(task)
        assert result["scores"] == task["rubric"], (
            f"Rubric mismatch for {task['task_id']}: "
            f"expected {task['rubric']}, got {result['scores']}"
        )
        assert result["ground_truth_checks"] == task["ground_truth"], (
            f"Ground-truth mismatch for {task['task_id']}: "
            f"expected {task['ground_truth']}, got {result['ground_truth_checks']}"
        )


def main() -> int:
    verify_audit_memo()
    verify_required_files()
    verify_schema_examples()
    print("All audit-phase verification checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
