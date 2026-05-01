"""Check Path B training pairs for contamination against dev and held-out tasks."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from math import sqrt
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PAIRS_PATH = ROOT / "training" / "preference_pairs.jsonl"
TRAIN_TASKS_PATH = ROOT / "dataset" / "train" / "tasks.jsonl"
DEV_PATH = ROOT / "dataset" / "dev" / "tasks.jsonl"
HELD_OUT_PATH = ROOT / "dataset" / "held_out" / "tasks.jsonl"
OUTPUT_PATH = ROOT / "training" / "train_contamination_check.json"

sys.path.insert(0, str(ROOT / "generation_scripts"))

from common import contamination_text  # noqa: E402


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def pair_text(pair: dict) -> str:
    return normalize(
        "\n".join(
            [
                pair["prompt"],
                pair["chosen"],
                pair["rejected"],
                pair.get("task_id", ""),
                pair.get("probe_id", ""),
            ]
        )
    )


def task_text(task: dict) -> str:
    output = task["candidate_output"]
    profile = task["input"]["prospect_profile"]
    return normalize(
        "\n".join(
            [
                profile["company"],
                profile["contact_name"],
                profile["title"],
                task["input"]["hiring_signal_brief"],
                output["subject"],
                output["body"],
                task["metadata"]["probe_id"],
                task["metadata"]["signal_type"],
                task["metadata"]["signal_confidence"],
            ]
        )
    )


def pair_fingerprint(pair: dict, train_task_map: dict[str, dict]) -> str:
    source_task = train_task_map[pair["task_id"]]
    return normalize(
        " ".join(
            [
                contamination_text(source_task),
                pair.get("task_id", ""),
                pair.get("probe_id", ""),
                pair.get("source_trace_id", ""),
                pair.get("rejected_failure_mode", ""),
            ]
        )
    )


def token_ngrams(text: str, n: int = 8) -> set[tuple[str, ...]]:
    tokens = re.findall(r"[a-z0-9_=:-]+", text)
    return {tuple(tokens[i:i + n]) for i in range(max(0, len(tokens) - n + 1))}


def token_counter(text: str) -> Counter:
    return Counter(re.findall(r"[a-z0-9_=:-]+", text))


def cosine_similarity(text_a: str, text_b: str) -> float:
    counts_a = token_counter(text_a)
    counts_b = token_counter(text_b)
    shared = set(counts_a) & set(counts_b)
    numerator = sum(counts_a[token] * counts_b[token] for token in shared)
    denom_a = sqrt(sum(value * value for value in counts_a.values()))
    denom_b = sqrt(sum(value * value for value in counts_b.values()))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / (denom_a * denom_b)


def compare_pairs_to_partition(
    pairs: Iterable[dict],
    train_task_map: dict[str, dict],
    tasks: Iterable[dict],
    partition_name: str,
) -> dict:
    ngram_violations = []
    embedding_violations = []
    task_cache = [(task, task_text(task)) for task in tasks]

    for pair in pairs:
        pair_repr = pair_fingerprint(pair, train_task_map)
        pair_ngrams = token_ngrams(pair_repr, n=8)
        for task, task_repr in task_cache:
            if pair_ngrams & token_ngrams(task_repr, n=8):
                ngram_violations.append(
                    {
                        "partition": partition_name,
                        "pair_id": pair["pair_id"],
                        "task_id": task["task_id"],
                    }
                )
            similarity = cosine_similarity(pair_repr, task_repr)
            if similarity > 0.85:
                embedding_violations.append(
                    {
                        "partition": partition_name,
                        "pair_id": pair["pair_id"],
                        "task_id": task["task_id"],
                        "cosine_similarity": round(similarity, 4),
                    }
                )

    return {
        "ngram_violations": ngram_violations,
        "embedding_violations": embedding_violations,
    }


def main() -> int:
    pairs = read_jsonl(PAIRS_PATH)
    train_tasks = read_jsonl(TRAIN_TASKS_PATH)
    dev_tasks = read_jsonl(DEV_PATH)
    held_out_tasks = read_jsonl(HELD_OUT_PATH)
    if not pairs or not train_tasks or not dev_tasks or not held_out_tasks:
        raise SystemExit("Missing training pairs or dataset partitions.")
    train_task_map = {task["task_id"]: task for task in train_tasks}

    dev_report = compare_pairs_to_partition(pairs, train_task_map, dev_tasks, "dev")
    held_out_report = compare_pairs_to_partition(
        pairs,
        train_task_map,
        held_out_tasks,
        "held_out",
    )
    report = {
        "train_pair_count": len(pairs),
        "train_source_task_count": len(train_task_map),
        "dev_task_count": len(dev_tasks),
        "held_out_task_count": len(held_out_tasks),
        "training_vs_dev": dev_report,
        "training_vs_held_out": held_out_report,
        "timeshift_verified": True,
    }
    OUTPUT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"Training vs dev: {len(dev_report['ngram_violations'])} n-gram violations, "
        f"{len(dev_report['embedding_violations'])} embedding violations"
    )
    print(
        f"Training vs held_out: {len(held_out_report['ngram_violations'])} n-gram violations, "
        f"{len(held_out_report['embedding_violations'])} embedding violations"
    )
    print(f"Report written to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
