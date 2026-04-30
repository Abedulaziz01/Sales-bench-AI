"""Verification checks for Path B training data preparation."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PAIRS_PATH = ROOT / "training" / "preference_pairs.jsonl"
LEAKAGE_LOG_PATH = ROOT / "training" / "leakage_prevention_log.md"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    pairs = load_jsonl(PAIRS_PATH)
    require(len(pairs) >= 500, f"expected at least 500 pairs, found {len(pairs)}")

    for row in pairs[:3]:
        require("prompt" in row and "chosen" in row and "rejected" in row, f"missing required fields in {row.get('pair_id')}")

    chosen_mean = mean(row["chosen_score_7"] for row in pairs)
    rejected_mean = mean(row["rejected_score_7"] for row in pairs)

    require(chosen_mean >= 5.5, f"chosen mean too low: {chosen_mean:.2f}")
    require(rejected_mean <= 2.5, f"rejected mean too high: {rejected_mean:.2f}")

    leakage_text = LEAKAGE_LOG_PATH.read_text(encoding="utf-8")
    require("Rejected samples" in leakage_text, "leakage log missing rejected sample section")
    require("Chosen rewrites" in leakage_text, "leakage log missing chosen rewrite section")
    require("Judge filter" in leakage_text, "leakage log missing judge section")
    require("different" in leakage_text.lower(), "leakage log should explicitly mention family separation")

    print("Training preference-pair verification passed.")
    print(f"pair_count={len(pairs)}")
    print(f"chosen_mean_7={chosen_mean:.2f}")
    print(f"rejected_mean_7={rejected_mean:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
