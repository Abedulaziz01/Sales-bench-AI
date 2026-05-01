"""Verify Step 3.2 training contamination and methodology rationale artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "training" / "train_contamination_check.json"
RATIONALE_PATH = ROOT / "training" / "methodology_rationale.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    require(REPORT_PATH.exists(), "Missing training/train_contamination_check.json")
    require(RATIONALE_PATH.exists(), "Missing training/methodology_rationale.md")

    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    held_out = report["training_vs_held_out"]
    require(len(held_out["ngram_violations"]) == 0, "Held-out n-gram violations detected")
    require(len(held_out["embedding_violations"]) == 0, "Held-out embedding violations detected")

    rationale = RATIONALE_PATH.read_text(encoding="utf-8")
    trace_ids = set(re.findall(r"TRACE-\d{3}", rationale))
    require(len(trace_ids) >= 3, "Need at least 3 Week 10 trace IDs in methodology_rationale.md")

    paper_markers = [
        "Direct Preference Optimization",
        "SimPO",
        "ORPO",
        "Prometheus 2",
        "Preference Leakage",
    ]
    found_papers = [marker for marker in paper_markers if marker in rationale]
    require(len(found_papers) >= 2, "Need at least 2 path-specific paper citations in methodology_rationale.md")
    require("Path B" in rationale, "Path B justification missing from methodology_rationale.md")

    print("Training contamination and rationale verification passed.")
    print(f"held_out_ngram_violations={len(held_out['ngram_violations'])}")
    print(f"held_out_embedding_violations={len(held_out['embedding_violations'])}")
    print(f"trace_ids={sorted(trace_ids)}")
    print(f"papers={found_papers}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
