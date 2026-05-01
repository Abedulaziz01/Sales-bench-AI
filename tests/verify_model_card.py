"""Verify the Phase 4 model card sections and result consistency."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_CARD = ROOT / "training" / "model_card.md"
ABLATIONS = ROOT / "ablations" / "ablation_results.json"

REQUIRED_SECTIONS = [
    "## Backbone",
    "## Training Data",
    "## Hyperparameters",
    "## Intended Use",
    "## Limitations",
    "## Evaluation Results",
    "## Environmental Cost",
    "## License",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    require(MODEL_CARD.exists(), "Missing training/model_card.md")
    text = MODEL_CARD.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        require(section in text, f"Missing section: {section}")

    results = json.loads(ABLATIONS.read_text(encoding="utf-8"))
    expected_snippets = [
        str(results["delta_a"]["score_baseline"]),
        str(results["delta_a"]["score_trained"]),
        str(results["delta_a"]["delta"]),
        str(results["delta_a"]["95_ci"][0]),
        str(results["delta_a"]["95_ci"][1]),
        str(results["delta_b"]["score_prompt_only"]),
        str(results["delta_b"]["score_trained"]),
        str(results["delta_b"]["delta"]),
        str(results["cost_pareto"]["cost_per_task_baseline"]),
        str(results["cost_pareto"]["cost_per_task_with_judge"]),
    ]
    for snippet in expected_snippets:
        require(snippet in text, f"Model card missing expected evaluation value: {snippet}")

    print("Model card verification passed.")
    print(f"sections={len(REQUIRED_SECTIONS)}")
    print("evaluation_values_match=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
