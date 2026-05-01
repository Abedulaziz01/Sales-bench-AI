"""Verify Phase 5 publication artifacts before live upload."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_README = ROOT / "dataset" / "README.md"
DATASET_UPLOAD = ROOT / "dataset" / "hf_upload.py"
MODEL_PUSH = ROOT / "training" / "hf_push_adapter.py"
BLOG_POST = ROOT / "docs" / "blog_post.md"
ABLATIONS = ROOT / "ablations" / "ablation_results.json"

BLOG_SECTIONS = [
    "## The Gap",
    "## The Audit Method",
    "## The Dataset",
    "## The Training Experiment",
    "## The Honest Result",
    "## What's Next",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    for path in [DATASET_README, DATASET_UPLOAD, MODEL_PUSH, BLOG_POST]:
        require(path.exists(), f"Missing Phase 5 artifact: {path}")

    dataset_text = DATASET_README.read_text(encoding="utf-8").lower()
    require("license: cc-by-4.0" in dataset_text, "Dataset README must set cc-by-4.0")
    require("train.jsonl" in dataset_text and "dev.jsonl" in dataset_text and "held_out.jsonl" in dataset_text, "Dataset README must expose 3 partitions")
    require("0.4848" in dataset_text, "Dataset README must show Week 10 baseline score")
    require("load_dataset(\"abdulaziz0111/tenacious-bench-v0.1\")" in DATASET_README.read_text(encoding="utf-8"), "Dataset README quickstart missing")

    blog_text = BLOG_POST.read_text(encoding="utf-8")
    for section in BLOG_SECTIONS:
        require(section in blog_text, f"Missing blog section: {section}")
    word_count = len(blog_text.split())
    require(1200 <= word_count <= 2000, f"Blog post word count out of range: {word_count}")
    require(len(set(re.findall(r"PROBE-\d{3}", blog_text))) >= 2, "Blog post needs at least 2 probe IDs")
    require("DeepSeek" in blog_text and "Qwen" in blog_text, "Blog post must explain multi-LLM routing")
    require("3/5" in blog_text and "4/5" in blog_text, "Blog post must describe judge-filter thresholds")

    ablations = json.loads(ABLATIONS.read_text(encoding="utf-8"))
    expected_values = [
        str(ablations["delta_a"]["delta"]),
        str(ablations["delta_a"]["95_ci"][0]),
        str(ablations["delta_a"]["95_ci"][1]),
        str(ablations["delta_b"]["delta"]),
    ]
    for value in expected_values:
        require(value in blog_text, f"Blog post missing exact numeric claim: {value}")

    print("Phase 5 publication artifact verification passed.")
    print(f"blog_word_count={word_count}")
    print("dataset_card_ready=1")
    print("model_push_ready=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
