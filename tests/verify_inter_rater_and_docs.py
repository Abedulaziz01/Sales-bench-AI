"""Verification checks for inter-rater agreement and dataset docs."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "dataset"
METHODOLOGY_PATH = ROOT / "audit" / "methodology.md"

DIMENSIONS = [
    "direct_score",
    "grounded_score",
    "honest_score",
    "professional_score",
    "non_condescending_score",
]


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def exact_agreement(round1: list[dict], round2: list[dict]) -> dict[str, float]:
    by_task = {row["task_id"]: row for row in round2}
    result = {}
    for dim in DIMENSIONS:
        matches = sum(1 for row in round1 if row["rubric"][dim] == by_task[row["task_id"]]["rubric"][dim])
        result[dim] = matches / len(round1)
    return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    round1 = load_jsonl(DATASET_DIR / "rater_labels_round1.jsonl")
    round2 = load_jsonl(DATASET_DIR / "rater_labels_round2.jsonl")
    require(len(round1) == 30, f"round1 label count expected 30, found {len(round1)}")
    require(len(round2) == 30, f"round2 label count expected 30, found {len(round2)}")

    for row in round1 + round2:
        require(set(row["rubric"].keys()) == set(DIMENSIONS), f"rubric keys mismatch for {row['task_id']}")

    round1_times = [datetime.fromisoformat(row["labeled_at"]) for row in round1]
    round2_times = [datetime.fromisoformat(row["labeled_at"]) for row in round2]
    require(min(round2_times) - max(round1_times) >= (datetime.fromisoformat("2026-04-29T10:00:00") - datetime.fromisoformat("2026-04-28T10:00:00")), "round2 was not created at least 24 hours after round1")

    agreement = exact_agreement(round1, round2)
    for dim, score in agreement.items():
        require(score >= 0.8, f"{dim} agreement below threshold: {score:.2%}")

    agreement_md = (DATASET_DIR / "inter_rater_agreement.md").read_text(encoding="utf-8")
    require("Agreement Matrix" in agreement_md, "inter_rater_agreement.md missing agreement matrix")

    methodology = METHODOLOGY_PATH.read_text(encoding="utf-8")
    require("## Inter-Rater Agreement" in methodology, "methodology missing inter-rater section")

    datasheet = (DATASET_DIR / "datasheet.md").read_text(encoding="utf-8")
    headers = [
        "## 1. Motivation",
        "## 2. Composition",
        "## 3. Collection Process",
        "## 4. Preprocessing / Cleaning / Labeling",
        "## 5. Uses",
        "## 6. Distribution",
        "## 7. Maintenance",
    ]
    for header in headers:
        require(header in datasheet, f"dataset/datasheet.md missing section {header}")
    word_count = len(datasheet.split())
    require(900 <= word_count <= 2600, f"dataset/datasheet.md word count out of range: {word_count}")

    data_card = (DATASET_DIR / "data_card.md").read_text(encoding="utf-8")
    for marker in ["## Telescopic", "## Periscopic", "## Microscopic"]:
        require(marker in data_card, f"dataset/data_card.md missing layer {marker}")

    print("Inter-rater agreement and dataset documentation verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
