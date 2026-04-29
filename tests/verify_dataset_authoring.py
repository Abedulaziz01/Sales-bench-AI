"""Verification checks for Week 11 dataset authoring artifacts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
LOGS = ROOT / "generation_scripts" / "logs"


def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    trace_count = count_jsonl(DATASET / "trace_derived_tasks.jsonl")
    programmatic_count = count_jsonl(DATASET / "programmatic_tasks.jsonl")
    synthesis_count = count_jsonl(DATASET / "multi_llm_synthesis_tasks.jsonl")
    adversarial_count = count_jsonl(DATASET / "adversarial_tasks.jsonl")
    train_count = count_jsonl(DATASET / "train" / "tasks.jsonl")
    dev_count = count_jsonl(DATASET / "dev" / "tasks.jsonl")
    held_count = count_jsonl(DATASET / "held_out" / "tasks.jsonl")

    require(trace_count >= 60, f"trace-derived count too low: {trace_count}")
    require(programmatic_count >= 60, f"programmatic count too low: {programmatic_count}")
    require(synthesis_count >= 60, f"synthesis count too low: {synthesis_count}")
    require(adversarial_count >= 30, f"adversarial count too low: {adversarial_count}")

    total_partitioned = train_count + dev_count + held_count
    require(train_count == 168, f"unexpected train count: {train_count}")
    require(dev_count == 101, f"unexpected dev count: {dev_count}")
    require(held_count == 67, f"unexpected held-out count: {held_count}")
    require(total_partitioned == 336, f"unexpected partition total: {total_partitioned}")

    contamination = json.loads((DATASET / "contamination_check.json").read_text(encoding="utf-8"))
    require(len(contamination["ngram_violations"]) == 0, "ngram contamination violations present")
    require(len(contamination["embedding_violations"]) == 0, "embedding contamination violations present")
    require(contamination["timeshift_verified"] is True, "timeshift verification failed")

    for log_name in [
        "trace_derived.log",
        "programmatic_sweep.log",
        "multi_llm_synthesis.log",
        "judge_filter.log",
        "dedup.log",
        "build_adversarial_tasks.log",
        "partition_dataset.log",
        "contamination_check.log",
    ]:
        require((LOGS / log_name).exists(), f"missing log file: {log_name}")

    notes = (DATASET / "adversarial_notes.md").read_text(encoding="utf-8")
    require(notes.count("## ADV-") >= 30, "missing adversarial design notes")

    print("Week 11 dataset authoring verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
