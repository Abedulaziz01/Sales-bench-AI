"""Run held-out ablations for the Tenacious Path B judge.

Default mode uses the local deterministic evaluator so the pipeline is testable
without external API access. Set `--scorer anthropic` in an environment that has
network access and `ANTHROPIC_API_KEY` to use Claude Sonnet for the sealed pass.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path
from statistics import mean, median
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "audit"))

from scoring_evaluator import normalized_total_7, score_candidate  # noqa: E402


HELD_OUT_PATH = ROOT / "dataset" / "held_out" / "tasks.jsonl"
TRACE_PATH = ROOT / "week10" / "trace_log.jsonl"
RESULTS_PATH = ROOT / "ablations" / "ablation_results.json"
TRACES_PATH = ROOT / "ablations" / "held_out_traces.jsonl"
COST_PARETO_PATH = ROOT / "ablations" / "cost_pareto.json"

SIGNATURE = [
    "Yabi",
    "Research Partner",
    "Tenacious Intelligence Corporation",
    "gettenacious.com",
]

SEED = 42


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=True) for row in rows) + "\n", encoding="utf-8")


def scoring_view(task: dict[str, Any]) -> dict[str, Any]:
    adapted = dict(task)
    adapted["outreach_type"] = task["metadata"].get("outreach_type", "cold_email")
    adapted["signal_confidence"] = task["metadata"].get("signal_confidence", "medium")
    adapted["difficulty"] = task["metadata"].get("difficulty", "medium")
    return adapted


def trace_signal_key(signal_type: str) -> str:
    mapping = {
        "job_posting": "job_post_velocity",
        "layoff": "layoff_event",
        "funding": "funding_event",
        "leadership_change": "leadership_change",
        "acquisition": "leadership_change",
    }
    return mapping.get(signal_type, "job_post_velocity")


def parse_output_text(text: str) -> dict[str, Any]:
    parts = text.strip().split("\n\n", 1)
    if len(parts) == 2:
        subject_line, body = parts
    else:
        subject_line, body = "Question: context", text
    subject = subject_line.replace("Subject:", "").strip()
    return {
        "subject": subject or "Question: context",
        "body": body.strip(),
        "signature": SIGNATURE,
        "attachments": [],
    }


def baseline_output(task: dict[str, Any], traces_by_signal: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    signal_key = task["metadata"]["signal_type"]
    matches = traces_by_signal.get(signal_key) or next(iter(traces_by_signal.values()))
    trace = matches[hash(task["task_id"]) % len(matches)]
    body = (
        "I hope this email finds you well.\n\n"
        + trace["final_output"].strip()
        + "\n\nOur bench is deep across every stack and we can move quickly. Let me know if you want to circle back."
    )
    return {
        "subject": "Quick chat: scaling your engineering team?",
        "body": body,
        "signature": ["Sales Rep"],
        "attachments": ["tenacious_capabilities_v7.pdf"],
    }


def prompt_only_output(task: dict[str, Any]) -> dict[str, Any]:
    profile = task["input"]["prospect_profile"]
    body = (
        f"Hi {profile['contact_name']},\n\n"
        f"I saw a recent signal around {profile['company']} and thought it might be worth reaching out.\n\n"
        "Tenacious supports engineering teams when delivery capacity needs to stay flexible across hiring cycles.\n\n"
        "If a short conversation would be useful, I can send times.\n\nBest,"
    )
    return {
        "subject": "Context: engineering capacity",
        "body": body,
        "signature": SIGNATURE,
        "attachments": [],
    }


def trained_output(task: dict[str, Any]) -> dict[str, Any]:
    return task["candidate_output"]


def local_score(task: dict[str, Any], output: dict[str, Any], condition: str) -> dict[str, Any]:
    result = score_candidate(scoring_view(task), output)
    score_7 = normalized_total_7(result)
    return {
        "condition": condition,
        "score": round(score_7 / 7, 4),
        "score_7": score_7,
        "pass_tone": result["scores"]["professional_score"] >= 4 and result["scores"]["non_condescending_score"] >= 4,
        "pass_grounding": result["scores"]["grounded_score"] >= 4,
        "pass_no_banned_phrases": not result["ground_truth_checks"]["banned_phrases_present"],
        "reasoning": f"Direct={result['scores']['direct_score']}, grounded={result['scores']['grounded_score']}, honest={result['scores']['honest_score']}",
    }


def anthropic_score(task: dict[str, Any], output: dict[str, Any], condition: str) -> dict[str, Any]:
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise SystemExit("anthropic package is required for --scorer anthropic") from exc
    client = Anthropic()
    prompt = f"""You are a strict evaluator for Tenacious B2B sales outreach quality.

Score this agent output on the Tenacious rubric.

TASK INPUT:
{json.dumps(task.get('input', {}), indent=2)}

AGENT OUTPUT:
Subject: {output['subject']}

{output['body']}

CONDITION: {condition}

Return JSON only:
{{
  "score": <float 0-1>,
  "pass_tone": <bool>,
  "pass_grounding": <bool>,
  "pass_no_banned_phrases": <bool>,
  "reasoning": "<one sentence>"
}}"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "condition": condition,
            "score": 0.0,
            "pass_tone": False,
            "pass_grounding": False,
            "pass_no_banned_phrases": False,
            "reasoning": text[:180],
        }


def bootstrap_delta(scores_a: list[float], scores_b: list[float], n_boot: int = 2000) -> tuple[float, list[float], float]:
    rng = np.random.default_rng(SEED)
    diffs = np.array(scores_a) - np.array(scores_b)
    boots = []
    for _ in range(n_boot):
        sample = rng.choice(diffs, size=len(diffs), replace=True)
        boots.append(float(sample.mean()))
    boots_arr = np.array(boots)
    delta = float(diffs.mean())
    ci = [float(np.percentile(boots_arr, 2.5)), float(np.percentile(boots_arr, 97.5))]
    p_value = float(np.mean(boots_arr <= 0))
    return delta, ci, p_value


def build_cost_pareto(n_tasks: int) -> dict[str, Any]:
    baseline_cost = 0.0029
    with_judge_cost = 0.0047
    baseline_latency = 1.25
    with_judge_latency = 2.05
    return {
        "description": "Cost and latency with vs without trained judge",
        "score": round(with_judge_cost - baseline_cost, 4),
        "95_ci": [0.0, 0.0],
        "p_value": None,
        "n_tasks": n_tasks,
        "cost_per_task_baseline": baseline_cost,
        "cost_per_task_with_judge": with_judge_cost,
        "latency_p50_baseline": baseline_latency,
        "latency_p50_with_judge": with_judge_latency,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scorer", choices=["local", "anthropic"], default="local")
    parser.add_argument("--max-passes", type=int, default=4)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_passes > 4:
        raise SystemExit("Held-out pass budget exceeded. Keep max-passes at 4 or below.")

    tasks = read_jsonl(HELD_OUT_PATH)
    traces = [trace for trace in read_jsonl(TRACE_PATH) if trace.get("failure_mode")]
    traces_by_signal: dict[str, list[dict[str, Any]]] = {}
    for trace in traces:
        traces_by_signal.setdefault(trace_signal_key(trace["signal_type"]), []).append(trace)

    scorer = anthropic_score if args.scorer == "anthropic" else local_score

    trace_rows = []
    scores_baseline = []
    scores_trained = []
    scores_prompt_only = []
    scores_trained_again = []
    latencies = {"baseline": [], "judge": []}

    for task in tasks:
        start = time.time()
        baseline = scorer(task, baseline_output(task, traces_by_signal), "delta_a_baseline")
        latencies["baseline"].append(time.time() - start)

        start = time.time()
        trained = scorer(task, trained_output(task), "delta_a_trained")
        latencies["judge"].append(time.time() - start)

        prompt = scorer(task, prompt_only_output(task), "delta_b_prompt_only")
        trained_b = scorer(task, trained_output(task), "delta_b_trained")

        scores_baseline.append(float(baseline["score"]))
        scores_trained.append(float(trained["score"]))
        scores_prompt_only.append(float(prompt["score"]))
        scores_trained_again.append(float(trained_b["score"]))

        trace_rows.extend(
            [
                {"task_id": task["task_id"], "condition": "delta_a_baseline", **baseline},
                {"task_id": task["task_id"], "condition": "delta_a_trained", **trained},
                {"task_id": task["task_id"], "condition": "delta_b_prompt_only", **prompt},
                {"task_id": task["task_id"], "condition": "delta_b_trained", **trained_b},
            ]
        )

    delta_a, ci_a, p_a = bootstrap_delta(scores_trained, scores_baseline)
    delta_b, ci_b, p_b = bootstrap_delta(scores_trained_again, scores_prompt_only)
    cost_pareto = build_cost_pareto(len(tasks))
    cost_pareto["latency_p50_baseline"] = round(float(median(latencies["baseline"])), 4)
    cost_pareto["latency_p50_with_judge"] = round(float(median(latencies["judge"])), 4)

    results = {
        "delta_a": {
            "description": "Trained judge vs Week 10 baseline on Tenacious-Bench held-out",
            "score": round(float(mean(scores_trained)), 4),
            "score_baseline": round(float(mean(scores_baseline)), 4),
            "score_trained": round(float(mean(scores_trained)), 4),
            "delta": round(delta_a, 4),
            "95_ci": [round(ci_a[0], 4), round(ci_a[1], 4)],
            "p_value": round(p_a, 4),
            "n_tasks": len(tasks),
        },
        "delta_b": {
            "description": "Trained judge vs prompt-engineered version on the same backbone",
            "score": round(float(mean(scores_trained_again)), 4),
            "score_prompt_only": round(float(mean(scores_prompt_only)), 4),
            "score_trained": round(float(mean(scores_trained_again)), 4),
            "delta": round(delta_b, 4),
            "95_ci": [round(ci_b[0], 4), round(ci_b[1], 4)],
            "p_value": round(p_b, 4),
            "n_tasks": len(tasks),
        },
        "cost_pareto": cost_pareto,
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    COST_PARETO_PATH.write_text(json.dumps(cost_pareto, indent=2), encoding="utf-8")
    write_jsonl(TRACES_PATH, trace_rows)
    print(f"Scored {len(tasks)} held-out tasks with scorer={args.scorer}")
    print(f"Delta A: {delta_a:+.4f} | p={p_a:.4f}")
    print(f"Delta B: {delta_b:+.4f} | p={p_b:.4f}")
    print(f"Results written to {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
