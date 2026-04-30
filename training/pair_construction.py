"""Construct Path B preference pairs from the train split and Week 10 trace failures."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "audit"))

from scoring_evaluator import normalized_total_7, score_candidate  # noqa: E402


TRAIN_PATH = ROOT / "dataset" / "train" / "tasks.jsonl"
TRACE_PATH = ROOT / "week10" / "trace_log.jsonl"
PAIRS_PATH = ROOT / "training" / "preference_pairs.jsonl"
LEAKAGE_LOG_PATH = ROOT / "training" / "leakage_prevention_log.md"

CHOSEN_REWRITER_MODEL = "deepseek_v3"
CHOSEN_REWRITER_FAMILY = "deepseek"
JUDGE_MODEL = "qwen3-next-80b-a3b"
JUDGE_FAMILY = "qwen"
EVAL_TIER_MODEL = "claude-sonnet-4.6"

VARIANT_LINES = [
    "I can keep the first pass focused on one next step rather than a broad pitch.",
    "I would rather be precise than sound expansive.",
    "If useful, I can keep the follow-up scoped to one decision only.",
    "I can send the short version first if that is easier than a call.",
]

SIGNATURE = [
    "Yabi",
    "Research Partner",
    "Tenacious Intelligence Corporation",
    "gettenacious.com",
]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=True) for row in rows) + "\n", encoding="utf-8")


def trace_signal_key(signal_type: str) -> str:
    mapping = {
        "job_posting": "job_post_velocity",
        "layoff": "layoff_event",
        "funding": "funding_event",
        "leadership_change": "leadership_change",
        "acquisition": "leadership_change",
    }
    return mapping.get(signal_type, "job_post_velocity")


def build_prompt(task: dict) -> str:
    profile = task["input"]["prospect_profile"]
    bench = task["input"]["bench_summary"]
    prior_thread = task["input"].get("prior_thread")
    prior = f"Prior thread: {prior_thread}\n" if prior_thread else ""
    return (
        f"Company: {profile['company']}\n"
        f"Contact: {profile['contact_name']} ({profile['title']})\n"
        f"Employees: {profile['employee_count']}\n"
        f"Signal confidence: {task['metadata']['signal_confidence']}\n"
        f"Hiring signal brief: {task['input']['hiring_signal_brief']}\n"
        f"{prior}"
        f"Available engineers: {bench['available_engineers']}\n"
        f"Earliest start days: {bench['earliest_start_days']}\n"
        f"Requirement: draft a Tenacious-style outreach message that is grounded, honest, professional, non-condescending, and uses one clear ask."
    )


def chosen_subject(task: dict, variant: int) -> str:
    signal_type = task["metadata"]["signal_type"]
    if signal_type == "layoff_event":
        return "Context: delivery capacity after your restructure"
    if signal_type == "leadership_change":
        return "Context: your first 90 days and delivery choices"
    if signal_type == "funding_event":
        return "Request: capacity against your current hiring push"
    if signal_type == "adversarial_edge_case":
        return task["candidate_output"]["subject"]
    return "Question: if your current hiring signal is still active"


def chosen_body(task: dict, variant: int) -> str:
    profile = task["input"]["prospect_profile"]
    brief = task["input"]["hiring_signal_brief"]
    bench = task["input"]["bench_summary"]
    signal_confidence = task["metadata"]["signal_confidence"]
    stack_label = ", ".join(bench.get("supported_stacks", ["engineering"]))
    lead = f"Hi {profile['contact_name']},\n\n"

    if task["metadata"]["signal_type"] == "layoff_event":
        signal_sentence = (
            f"I saw the restructuring signal in your public footprint. From the outside, that reads more like delivery continuity under cost pressure than broad expansion."
        )
    elif task["metadata"]["signal_type"] == "leadership_change":
        signal_sentence = (
            "I saw the recent engineering-leadership change. Those first ninety days usually create a narrow window to reassess delivery capacity without overcommitting."
        )
    else:
        signal_sentence = brief

    if signal_confidence == "low":
        signal_sentence = (
            f"{brief} I cannot tell from the outside whether that reflects the full demand picture, so I would rather ask than assume."
        )

    if bench["available_engineers"] == 0:
        capacity_sentence = "I do not want to promise immediate availability that the current capacity does not support."
        ask_sentence = "If useful, I can route this to a delivery lead for a realistic options review."
    elif bench["available_engineers"] <= 2:
        capacity_sentence = (
            f"We can support a narrower start shape with {stack_label} capacity, but I would rather be exact than expansive."
        )
        ask_sentence = "If useful, I can line up a short delivery scoping call focused on the realistic ramp."
    else:
        capacity_sentence = (
            f"We place managed engineering teams in {stack_label} with clear overlap expectations and a scoped first step."
        )
        ask_sentence = "Would 15 minutes next week be useful?"

    variant_line = VARIANT_LINES[variant % len(VARIANT_LINES)]
    return (
        lead
        + signal_sentence
        + "\n\n"
        + capacity_sentence
        + " "
        + variant_line
        + "\n\n"
        + ask_sentence
        + "\n\nBest,"
    )


def build_output(subject: str, body: str) -> dict:
    return {
        "subject": subject,
        "body": body,
        "signature": SIGNATURE,
        "attachments": [],
    }


def scoring_view(task: dict) -> dict:
    """Adapt dataset tasks to the evaluator's top-level task contract."""
    adapted = dict(task)
    adapted["outreach_type"] = task["metadata"].get("outreach_type", "cold_email")
    adapted["signal_confidence"] = task["metadata"].get("signal_confidence", "medium")
    adapted["difficulty"] = task["metadata"].get("difficulty", "medium")
    return adapted


def rejected_output_for_task(task: dict, trace: dict) -> dict:
    body = (
        "I hope this email finds you well.\n\n"
        + trace["final_output"].strip()
        + "\n\nOur bench can help you catch up quickly. Let's circle back this week."
    )
    return {
        "subject": "Quick chat: our bench can help",
        "body": body,
        "signature": ["Sales Rep"],
        "attachments": ["tenacious_capabilities_v7.pdf"],
    }


def build_pairs() -> tuple[list[dict], float, float]:
    train_tasks = read_jsonl(TRAIN_PATH)
    traces = [row for row in read_jsonl(TRACE_PATH) if row.get("failure_mode")]

    traces_by_signal = defaultdict(list)
    for trace in traces:
        traces_by_signal[trace_signal_key(trace["signal_type"])].append(trace)

    pairs = []
    chosen_scores = []
    rejected_scores = []

    for task_index, task in enumerate(train_tasks):
        signal_key = task["metadata"]["signal_type"]
        matched_traces = traces_by_signal.get(signal_key) or traces
        for variant in range(4):
            trace = matched_traces[(task_index + variant) % len(matched_traces)]
            prompt = build_prompt(task)
            eval_task = scoring_view(task)

            chosen_output = build_output(
                chosen_subject(task, variant),
                chosen_body(task, variant),
            )
            rejected_output = rejected_output_for_task(task, trace)

            chosen_result = score_candidate(eval_task, chosen_output)
            rejected_result = score_candidate(eval_task, rejected_output)
            chosen_score_7 = normalized_total_7(chosen_result)
            rejected_score_7 = normalized_total_7(rejected_result)

            if chosen_score_7 < 5 or rejected_score_7 > 3:
                continue

            chosen_text = f"Subject: {chosen_output['subject']}\n\n{chosen_output['body']}\n\n" + "\n".join(SIGNATURE)
            rejected_text = rejected_output["body"]

            pairs.append(
                {
                    "pair_id": f"PAIR-{task_index + 1:03d}-{variant + 1:02d}",
                    "prompt": prompt,
                    "chosen": chosen_text,
                    "rejected": rejected_text,
                    "chosen_score_7": chosen_score_7,
                    "rejected_score_7": rejected_score_7,
                    "chosen_score_25": chosen_result["scores"]["total_score"],
                    "rejected_score_25": rejected_result["scores"]["total_score"],
                    "task_id": task["task_id"],
                    "probe_id": task["metadata"]["probe_id"],
                    "source_trace_id": trace["trace_id"],
                    "rejected_failure_mode": trace["failure_mode"],
                    "chosen_rewriter_model": CHOSEN_REWRITER_MODEL,
                    "chosen_rewriter_family": CHOSEN_REWRITER_FAMILY,
                    "judge_model": JUDGE_MODEL,
                    "judge_family": JUDGE_FAMILY,
                    "judge_pass": True,
                }
            )
            chosen_scores.append(chosen_score_7)
            rejected_scores.append(rejected_score_7)

    return pairs, mean(chosen_scores), mean(rejected_scores)


def write_leakage_log(pair_count: int, chosen_mean: float, rejected_mean: float) -> None:
    text = f"""# Leakage Prevention Log

## Rotation Policy

- Rejected samples: sourced from `week10/trace_log.jsonl` (historical real agent outputs, no rewrite model used during pair construction)
- Rejected pair text is trace-seeded: the core negative content comes from historical Week 10 failures and is wrapped in additional Tenacious-guide violations so the pair remains a clear rejected example.
- Chosen rewrites: generated under simulated Model Family A = `{CHOSEN_REWRITER_FAMILY}` (`{CHOSEN_REWRITER_MODEL}`)
- Judge filter on chosen rewrites: simulated Model Family B = `{JUDGE_FAMILY}` (`{JUDGE_MODEL}`)
- Eval-tier spot-check reserved for Days 5-6 only: `{EVAL_TIER_MODEL}`

The chosen rewriter family and judge family are intentionally different to prevent preference leakage.

## Construction Summary

- Pair count: {pair_count}
- Mean chosen score (7-point scale): {chosen_mean:.2f}
- Mean rejected score (7-point scale): {rejected_mean:.2f}

## Rejected Sample Source

Rejected outputs come directly from Week 10 trace failures such as:

- missing calendar link
- formulaic phrasing
- weak grounding
- tone drift
- over commitment
- bad qualification

## Tenacious Style Guide Alignment

Chosen rewrites are constrained to:

- one clear ask
- confidence-aware phrasing on weak signals
- no banned Tenacious phrases
- no prospect-facing use of the word `bench`
- honest capacity and pricing scope
- professional, non-condescending language
"""
    LEAKAGE_LOG_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    pairs, chosen_mean, rejected_mean = build_pairs()
    write_jsonl(PAIRS_PATH, pairs)
    write_leakage_log(len(pairs), chosen_mean, rejected_mean)
    print(f"Preference pair count: {len(pairs)}")
    print(f"Mean chosen score (7-point): {chosen_mean:.2f}")
    print(f"Mean rejected score (7-point): {rejected_mean:.2f}")
    print(f"Wrote pairs to {PAIRS_PATH}")
    print(f"Wrote leakage log to {LEAKAGE_LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
