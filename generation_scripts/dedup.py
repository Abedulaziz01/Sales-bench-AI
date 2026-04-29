"""Deduplicate the combined Tenacious-Bench authoring pool."""

from __future__ import annotations

from pathlib import Path

from common import append_log, dedup_key, read_jsonl, write_jsonl


def main() -> int:
    source_files = [
        Path("dataset/trace_derived_tasks.jsonl"),
        Path("dataset/programmatic_tasks.jsonl"),
        Path("dataset/multi_llm_synthesis_tasks.jsonl"),
        Path("dataset/adversarial_tasks.jsonl"),
    ]
    combined = []
    for path in source_files:
        combined.extend(read_jsonl(path))
    before = len(combined)
    seen = set()
    deduped = []
    for task in combined:
        key = dedup_key(task)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(task)
    out_path = Path("dataset/combined_pool_deduped.jsonl")
    after = write_jsonl(out_path, deduped)
    reduction = ((before - after) / before) if before else 0.0
    log_path = append_log(
        "dedup",
        [
            f"before={before}",
            f"after={after}",
            f"reduction={reduction:.2%}",
            f"output_file={out_path}",
        ],
    )
    print(f"Before dedup: {before}")
    print(f"After dedup: {after}")
    print(f"Reduction: {reduction:.0%}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
