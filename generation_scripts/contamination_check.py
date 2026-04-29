"""Run contamination checks across dataset partitions."""

from __future__ import annotations

import json
from pathlib import Path

from common import HELD_OUT_DIR, TRAIN_DIR, append_log, contamination_text, cosine_similarity, read_jsonl, token_ngrams


def main() -> int:
    train_tasks = read_jsonl(TRAIN_DIR / "tasks.jsonl")
    held_out_tasks = read_jsonl(HELD_OUT_DIR / "tasks.jsonl")
    if not train_tasks or not held_out_tasks:
        raise SystemExit("Missing partition files. Build dataset partitions first.")

    ngram_violations = []
    embedding_violations = []
    for held in held_out_tasks:
        held_ngrams = token_ngrams(contamination_text(held), n=8)
        for train in train_tasks:
            shared = held_ngrams & token_ngrams(contamination_text(train), n=8)
            if shared:
                ngram_violations.append(
                    {
                        "held_out_task_id": held["task_id"],
                        "train_task_id": train["task_id"],
                    }
                )
            similarity = cosine_similarity(held, train)
            if similarity > 0.85:
                embedding_violations.append(
                    {
                        "held_out_task_id": held["task_id"],
                        "train_task_id": train["task_id"],
                        "cosine_similarity": round(similarity, 4),
                    }
                )
    all_tasks = train_tasks + held_out_tasks
    timeshift_verified = all(task["metadata"].get("time_shift_verified") for task in all_tasks)
    report = {
        "ngram_violations": ngram_violations,
        "embedding_violations": embedding_violations,
        "timeshift_verified": timeshift_verified,
    }
    out_path = Path("dataset/contamination_check.json")
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    log_path = append_log(
        "contamination_check",
        [
            f"ngram_violations={len(ngram_violations)}",
            f"embedding_violations={len(embedding_violations)}",
            f"timeshift_verified={timeshift_verified}",
            f"output_file={out_path}",
        ],
    )
    print(f"N-gram check: {len(ngram_violations)} pairs with >= 8-gram overlap")
    print(f"Embedding check: {len(embedding_violations)} pairs with cosine sim > 0.85")
    print(f"Time-shift: all signals documented = {timeshift_verified}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
