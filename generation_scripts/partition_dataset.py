"""Partition the deduplicated Tenacious-Bench pool into train/dev/held_out."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from common import DEV_DIR, HELD_OUT_DIR, TRAIN_DIR, append_log, read_jsonl, split_counts, stable_rng, write_jsonl


def main() -> int:
    source = Path("dataset/combined_pool_deduped.jsonl")
    tasks = read_jsonl(source)
    if not tasks:
        raise SystemExit("Missing deduplicated pool. Run dedup.py first.")
    rng = stable_rng("tenacious-bench-partition-v1")
    buckets = defaultdict(list)
    for task in tasks:
        company = task["input"]["prospect_profile"]["company"]
        buckets[company].append(task)
    bucket_items = list(buckets.items())
    rng.shuffle(bucket_items)
    train_target, dev_target, held_target = split_counts(len(tasks))
    train, dev, held = [], [], []
    for _, bucket in bucket_items:
        if len(train) + len(bucket) <= train_target:
            train.extend(bucket)
        elif len(dev) + len(bucket) <= dev_target:
            dev.extend(bucket)
        else:
            held.extend(bucket)
    write_jsonl(TRAIN_DIR / "tasks.jsonl", train)
    write_jsonl(DEV_DIR / "tasks.jsonl", dev)
    write_jsonl(HELD_OUT_DIR / "tasks.jsonl", held)
    log_path = append_log(
        "partition_dataset",
        [
            f"source_file={source}",
            f"total_tasks={len(tasks)}",
            f"train_count={len(train)}",
            f"dev_count={len(dev)}",
            f"held_out_count={len(held)}",
        ],
    )
    print(f"Train: {len(train)}")
    print(f"Dev: {len(dev)}")
    print(f"Held-out: {len(held)}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
