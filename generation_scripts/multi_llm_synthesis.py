"""Generate multi-LLM synthesis tasks and judge-filter them."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from common import MODEL_FAMILIES, TRACE_SEEDS, append_log, judge_pass, judge_scores, make_task, write_jsonl


MODEL_ROUTES = [
    ("claude_sonnet", "gpt_4o_mini"),
    ("gpt_4o_mini", "qwen3_next"),
    ("claude_sonnet", "deepseek_v3"),
    ("gpt_4o_mini", "deepseek_v3"),
]


def synthesis_body(seed: dict, family: str, variant: int) -> str:
    if variant % 4 == 0:
        return seed["good_body"]
    if variant % 4 == 1:
        return seed["bad_body"]
    if family in {"qwen", "deepseek"}:
        return (
            f"Hi {seed['contact_name']},\n\n"
            f"{seed['brief']} If that timing is still current, I can share a short brief on how similar teams handled the same constraint.\n\n"
            f"This draft came through the {family} synthesis branch.\n\nWould 15 minutes next week be useful?\n\nBest,"
        )
    return (
        f"Hi {seed['contact_name']},\n\n"
        f"{seed['brief']} I do not want to overstate what the public signal proves, but it looked worth asking.\n\n"
        f"If useful, I can send a one-page note instead of asking for time. This draft came through the {family} synthesis branch.\n\nBest,"
    )


def main() -> int:
    accepted = []
    raw = []
    route_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"seen": 0, "accepted": 0})
    judge_family = "openai"
    task_number = 0
    for route_index, (author_model, rewriter_model) in enumerate(MODEL_ROUTES, start=1):
        author_family = MODEL_FAMILIES[author_model]
        rewriter_family = MODEL_FAMILIES[rewriter_model]
        for seed in TRACE_SEEDS:
            for variant in range(4):
                task_number += 1
                model_family = author_family if variant < 2 else rewriter_family
                task = make_task(
                    task_id=f"ML-{route_index:02d}-{task_number:03d}",
                    source_mode="multi-llm-synthesis",
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
                    subject=seed["good_subject"],
                    body=synthesis_body(seed, model_family, variant),
                    stack=seed["stack"],
                    available_engineers=seed["available_engineers"],
                    earliest_start_days=seed["earliest_start_days"],
                    bench_state=seed["bench_state"],
                    difficulty="adversarial" if variant == 1 else "hard",
                    model_name=author_model if variant < 2 else rewriter_model,
                    model_family=model_family,
                    notes=f"Routed through {author_model} then {rewriter_model}.",
                )
                raw.append(task)
                route_stats[model_family]["seen"] += 1
                scores = judge_scores(task, judge_family=judge_family)
                task["judge_filter"] = {
                    "judge_family": judge_family,
                    "scores": scores,
                    "accepted": judge_pass(scores),
                }
                if task["judge_filter"]["accepted"]:
                    accepted.append(task)
                    route_stats[model_family]["accepted"] += 1

    raw_path = Path("dataset/multi_llm_synthesis_raw.jsonl")
    filtered_path = Path("dataset/multi_llm_synthesis_tasks.jsonl")
    write_jsonl(raw_path, raw)
    count = write_jsonl(filtered_path, accepted)

    log_lines = [
        f"raw_output={raw_path}",
        f"filtered_output={filtered_path}",
        "model_routes=claude_sonnet->gpt_4o_mini,gpt_4o_mini->qwen3_next,claude_sonnet->deepseek_v3,gpt_4o_mini->deepseek_v3",
    ]
    for family, stats in sorted(route_stats.items()):
        acceptance_rate = stats["accepted"] / stats["seen"] if stats["seen"] else 0.0
        log_lines.append(
            f"family={family} seen={stats['seen']} accepted={stats['accepted']} acceptance_rate={acceptance_rate:.2f}"
        )
    log_path = append_log("multi_llm_synthesis", log_lines)
    print("Model routes used:")
    for route in MODEL_ROUTES:
        print(f"- {route[0]} -> {route[1]}")
    for family, stats in sorted(route_stats.items()):
        acceptance_rate = stats["accepted"] / stats["seen"] if stats["seen"] else 0.0
        print(f"{family}: {stats['accepted']}/{stats['seen']} accepted ({acceptance_rate:.0%})")
    print(f"Tasks passing judge filter: {count} -> {filtered_path}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
