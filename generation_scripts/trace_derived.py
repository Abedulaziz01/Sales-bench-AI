"""Generate trace-derived Tenacious-Bench tasks."""

from __future__ import annotations

from pathlib import Path

from common import TRACE_SEEDS, append_log, body_for, ensure_dirs, make_task, write_jsonl


def main() -> int:
    ensure_dirs()
    tasks = []
    angles = [
        "I can bring one concrete delivery pattern from a similar team.",
        "I can keep this to one constraint and one next step.",
        "I can share the narrowest useful case study instead of a deck.",
        "I can route this to a delivery lead if the timing is real.",
        "I can keep the first conversation scoped to capacity only.",
        "I can send a one-page note if a call is not useful yet.",
    ]
    for seed_index, seed in enumerate(TRACE_SEEDS, start=1):
        for variant in range(12):
            use_good = variant % 2 == 0
            task_id = f"TD-{seed_index:02d}-{variant + 1:03d}"
            difficulty = "medium" if use_good else "hard"
            subject = seed["good_subject"] if use_good else f"Follow-up: {seed['company']} capacity note"
            body = seed["good_body"] if use_good else seed["bad_body"]
            if variant not in (0, 1):
                body = body.replace("15 minutes", f"{15 + (variant % 3) * 5} minutes")
                body = body.replace(
                    "\n\nBest,",
                    f"\n\n{angles[variant % len(angles)]} Variant lens {variant + 1:02d} keeps the trace distinct while preserving the same failure mode.\n\nBest,",
                )
            tasks.append(
                make_task(
                    task_id=task_id,
                    source_mode="trace-derived",
                    probe_id=seed["probe_id"],
                    trace_id=seed["trace_id"],
                    segment=seed["segment"],
                    signal_type=seed["signal_type"],
                    signal_confidence=seed["signal_confidence"],
                    company=seed["company"],
                    contact_name=seed["contact_name"],
                    title=seed["title"],
                    employee_count=seed["employee_count"],
                    signal_date=seed["signal_date"],
                    brief=seed["brief"],
                    subject=subject,
                    body=body,
                    stack=seed["stack"],
                    available_engineers=seed["available_engineers"],
                    earliest_start_days=seed["earliest_start_days"],
                    bench_state=seed["bench_state"],
                    difficulty=difficulty,
                    notes="Derived from Week 10 trace patterns and rewritten into scoreable task format.",
                )
            )
    out_path = Path("dataset/trace_derived_tasks.jsonl")
    count = write_jsonl(out_path, tasks)
    log_path = append_log(
        "trace_derived",
        [
            f"output_file={out_path}",
            f"task_count={count}",
            "source_mode=trace-derived",
            f"trace_seed_count={len(TRACE_SEEDS)}",
        ],
    )
    print(f"Generated {count} trace-derived tasks -> {out_path}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
