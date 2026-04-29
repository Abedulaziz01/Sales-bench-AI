"""Shared utilities for deterministic Tenacious-Bench dataset generation."""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "dataset"
TRAIN_DIR = DATASET_DIR / "train"
DEV_DIR = DATASET_DIR / "dev"
HELD_OUT_DIR = DATASET_DIR / "held_out"
LOG_DIR = ROOT / "generation_scripts" / "logs"

SIGNATURE = [
    "Yabi",
    "Research Partner",
    "Tenacious Intelligence Corporation",
    "gettenacious.com",
]

BANNED_PHRASES = [
    "world-class",
    "top talent",
    "a-players",
    "rockstar",
    "ninja",
    "wizard",
    "skyrocket",
    "supercharge",
    "10x",
    "i hope this email finds you well",
    "just following up",
    "circling back",
    "quick question",
    "quick chat",
    "synergize",
    "synergy",
    "leverage",
    "ecosystem",
    "game-changer",
    "disruptor",
    "paradigm shift",
    "do not miss out",
    "per my last email",
]

TRACE_SEEDS = [
    {
        "trace_id": "TRACE-001",
        "probe_id": "PROBE-001",
        "segment": "series_a_b_hiring",
        "signal_type": "funding_event",
        "signal_confidence": "high",
        "company": "Acme Atlas",
        "contact_name": "Maya",
        "title": "VP Engineering",
        "employee_count": 420,
        "signal_date": "2026-02-14",
        "brief": "Closed a $14M Series A in February. Python roles increased from 2 to 7 in the last 60 days.",
        "good_subject": "Request: 15 minutes on your Python hiring",
        "good_body": "Hi Maya,\n\nYou closed your $14M Series A in February and your open Python roles went from 2 to 7 in the last 60 days. We place dedicated Python and data engineers, managed by Tenacious, with three hours of US overlap.\n\nWould 15 minutes next week be useful?\n\nBest,",
        "bad_body": "Hi Maya,\n\nTenacious is a world-class engineering outsourcing firm with top talent across every stack. We can help with all your hiring needs.\n\nWould you be open to a quick chat?\n\nBest,",
        "stack": ["Python", "Data"],
        "available_engineers": 2,
        "earliest_start_days": 2,
        "bench_state": "supported"
    },
    {
        "trace_id": "TRACE-002",
        "probe_id": "PROBE-002",
        "segment": "mid_market_cost_restructure",
        "signal_type": "layoff_event",
        "signal_confidence": "high",
        "company": "Northbridge Health",
        "contact_name": "Daniel",
        "title": "CTO",
        "employee_count": 780,
        "signal_date": "2026-03-03",
        "brief": "Team contracted by 12% in March. Delivery output still needs to hold while fully-loaded cost drops.",
        "good_subject": "Context: lower-cost engineering capacity post-restructure",
        "good_body": "Hi Daniel,\n\nI saw the announcement that your team contracted by about 12% in March. Companies in your stage often need to maintain delivery output while reducing fully-loaded cost.\n\nIf you are scoping the next twelve months of delivery capacity, I can share two short case studies from mid-market clients who rebalanced cost this way.\n\nBest,",
        "bad_body": "Hi Daniel,\n\nYou are clearly scaling aggressively after your layoffs and need to move fast. We can skyrocket throughput with top talent.\n\nLet's get on a call this week.\n\nBest,",
        "stack": ["Python", "Data", "ML"],
        "available_engineers": 5,
        "earliest_start_days": 14,
        "bench_state": "supported"
    },
    {
        "trace_id": "TRACE-003",
        "probe_id": "PROBE-003",
        "segment": "engineering_leadership_transition",
        "signal_type": "leadership_change",
        "signal_confidence": "high",
        "company": "Helix Systems",
        "contact_name": "Priya",
        "title": "CTO",
        "employee_count": 310,
        "signal_date": "2026-04-11",
        "brief": "New CTO announcement on April 11. Vendor reassessment window likely inside first 90 days.",
        "good_subject": "Context: a brief on offshore engineering models",
        "good_body": "Hi Priya,\n\nWelcome to your new role at Helix - I saw the announcement on April 11. New engineering leaders typically reassess vendor and offshore mix in their first 90 days.\n\nIf a 15-minute conversation in May would be useful, the calendar is at gettenacious.com/yabi. If not, no follow-up.\n\nBest,",
        "bad_body": "Hi Priya,\n\nCongratulations on your $40M Series C last month. We can plug a 15-engineer team into your stack within 30 days.\n\nWant to discuss?\n\nBest,",
        "stack": ["Go", "Infra"],
        "available_engineers": 4,
        "earliest_start_days": 21,
        "bench_state": "tight"
    },
    {
        "trace_id": "TRACE-004",
        "probe_id": "PROBE-005",
        "segment": "specialized_capability_gap",
        "signal_type": "peer_gap",
        "signal_confidence": "high",
        "company": "Loyalty Loop",
        "contact_name": "Felix",
        "title": "VP Engineering",
        "employee_count": 260,
        "signal_date": "2026-01-29",
        "brief": "Three named peers posted senior MLOps roles in the last 90 days. Prospect has not posted equivalent roles.",
        "good_subject": "Question: your MLOps function in 2026",
        "good_body": "Hi Felix,\n\nThree adjacent loyalty-platform companies posted senior MLOps roles in the last 90 days. Your team has not, at least not publicly. Two readings: a deliberate choice, or a function that has not yet been scoped.\n\nIf useful, 15 minutes is enough to walk through what those peers are doing.\n\nBest,",
        "bad_body": "Hi Felix,\n\nYour AI maturity is behind the curve and your leadership has not yet made the strategic moves the sector demands. We can help you catch up.\n\nBest,",
        "stack": ["ML", "Infra"],
        "available_engineers": 3,
        "earliest_start_days": 10,
        "bench_state": "supported"
    },
    {
        "trace_id": "TRACE-005",
        "probe_id": "PROBE-007",
        "segment": "series_a_b_hiring",
        "signal_type": "job_post_velocity",
        "signal_confidence": "low",
        "company": "Northstar Data",
        "contact_name": "Tom",
        "title": "VP Data",
        "employee_count": 180,
        "signal_date": "2026-04-05",
        "brief": "Two open data engineer roles on the careers page. Signal confidence low: ask, do not assert.",
        "good_subject": "Question: are your data engineering hires keeping up?",
        "good_body": "Hi Tom,\n\nTwo open data engineer roles on your careers page - I cannot tell from the outside whether hiring is keeping pace or whether the queue is longer than the postings suggest.\n\nIf the real number is higher, would 15 minutes be useful?\n\nBest,",
        "bad_body": "Hi Tom,\n\nI see you are scaling aggressively and must be feeling recruiting pain right now. We place top talent in 48 hours.\n\nQuick chat next week?\n\nBest,",
        "stack": ["Data", "Python"],
        "available_engineers": 3,
        "earliest_start_days": 14,
        "bench_state": "supported"
    },
    {
        "trace_id": "TRACE-006",
        "probe_id": "PROBE-009",
        "segment": "specialized_capability_gap",
        "signal_type": "ai_maturity_gap",
        "signal_confidence": "medium",
        "company": "Orbit Foundry",
        "contact_name": "Sophia",
        "title": "Founder",
        "employee_count": 10,
        "signal_date": "2026-03-19",
        "brief": "Series A company with 10 engineers, AI maturity score 0-1, no public AI roles. Early-stage AI function not yet staffed.",
        "good_subject": "Question: standing up your first AI function",
        "good_body": "Hi Sophia,\n\nYou closed your Series A in March, your team is ten engineers, and your public roles are backend and product only. No AI roles yet - which is normal at your stage, not a gap.\n\nIf an AI feature is on your roadmap in the next twelve months, would 15 minutes be useful?\n\nBest,",
        "bad_body": "Hi Sophia,\n\nMost peer companies in your stage are now scoping agentic systems and dedicated MLOps functions. We should discuss your agentic roadmap.\n\nBest,",
        "stack": ["ML", "Data"],
        "available_engineers": 1,
        "earliest_start_days": 30,
        "bench_state": "partial"
    }
]


PROGRAMMATIC_DIMENSIONS = {
    "company_size": [
        ("smb", 45),
        ("mid_market", 220),
        ("enterprise", 850),
    ],
    "bench_state": [
        ("supported", 4, 7),
        ("partial", 2, 14),
        ("unsupported", 0, 30),
    ],
    "signal_type": [
        "funding_event",
        "job_post_velocity",
        "layoff_event",
        "leadership_change",
    ],
}

MODEL_FAMILIES = {
    "claude_sonnet": "anthropic",
    "gpt_4o_mini": "openai",
    "qwen3_next": "qwen",
    "deepseek_v3": "deepseek",
}


def stable_rng(seed: str) -> random.Random:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def ensure_dirs() -> None:
    for path in [DATASET_DIR, TRAIN_DIR, DEV_DIR, HELD_OUT_DIR, LOG_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    ensure_dirs()
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")
            count += 1
    return count


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def append_log(script_name: str, lines: list[str]) -> Path:
    ensure_dirs()
    path = LOG_DIR / f"{script_name}.log"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def subject_for(signal_type: str, variant: int, confidence: str) -> str:
    if signal_type == "funding_event":
        return "Request: hiring capacity after your funding round"
    if signal_type == "layoff_event":
        return "Context: engineering capacity after your restructure"
    if signal_type == "leadership_change":
        return "Context: a brief for your first 90 days"
    if confidence == "low":
        return "Question: is your hiring queue keeping up?"
    return f"Question: signal review {variant}"


def body_for(company: str, contact_name: str, signal_line: str, bench_state: str, confidence: str, stack_label: str, stale_note: str | None = None, prior_thread: str | None = None) -> str:
    opener = f"Hi {contact_name},\n\n"
    if prior_thread:
        opener += f"Picking up from your earlier note about {prior_thread}.\n\n"
    if confidence == "low":
        signal_sentence = f"{signal_line} I cannot tell from the outside whether that reflects real demand or just a narrow public snapshot."
    else:
        signal_sentence = signal_line
    if bench_state == "unsupported":
        capacity_sentence = f"We have some {stack_label} capacity, but I would rather confirm the right deployment shape than over-commit in email."
    elif bench_state == "partial":
        capacity_sentence = f"We can likely support part of that need with {stack_label} engineers, but exact start shape depends on timing and scope."
    else:
        capacity_sentence = f"We place managed {stack_label} engineers with at least three hours of US overlap and can move quickly when the fit is real."
    note = f" {stale_note}" if stale_note else ""
    return (
        opener
        + signal_sentence
        + note
        + "\n\n"
        + capacity_sentence
        + "\n\nWould 15 minutes next week be useful?\n\nBest,"
    )


def make_task(
    task_id: str,
    source_mode: str,
    probe_id: str,
    trace_id: str | None,
    segment: str,
    signal_type: str,
    signal_confidence: str,
    company: str,
    contact_name: str,
    title: str,
    employee_count: int,
    signal_date: str,
    brief: str,
    subject: str,
    body: str,
    stack: list[str],
    available_engineers: int,
    earliest_start_days: int,
    bench_state: str,
    difficulty: str,
    outreach_type: str = "cold_email",
    channel: str = "email",
    model_name: str | None = None,
    model_family: str | None = None,
    prior_thread: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "metadata": {
            "source_mode": source_mode,
            "probe_id": probe_id,
            "trace_id": trace_id,
            "difficulty": difficulty,
            "outreach_type": outreach_type,
            "channel": channel,
            "primary_segment": segment,
            "signal_type": signal_type,
            "signal_confidence": signal_confidence,
            "company_size": employee_count,
            "bench_state": bench_state,
            "model_name": model_name,
            "model_family": model_family,
            "time_shift_verified": True,
        },
        "input": {
            "prospect_profile": {
                "company": company,
                "contact_name": contact_name,
                "title": title,
                "employee_count": employee_count,
            },
            "hiring_signal_brief": brief,
            "signal_date": signal_date,
            "prior_thread": prior_thread,
            "bench_summary": {
                "available_engineers": available_engineers,
                "supported_stacks": stack,
                "earliest_start_days": earliest_start_days,
                "prospect_facing_capacity_phrase": "engineering team",
            },
        },
        "candidate_output": {
            "subject": subject,
            "body": body,
            "signature": SIGNATURE,
            "attachments": [],
        },
        "notes": notes,
    }


def task_text(task: dict[str, Any]) -> str:
    output = task["candidate_output"]
    return " ".join(
        [
            task["input"]["prospect_profile"]["company"],
            task["input"]["hiring_signal_brief"],
            output["subject"],
            output["body"],
            task["metadata"]["probe_id"],
            task["metadata"]["signal_type"],
        ]
    ).lower()


def contamination_text(task: dict[str, Any]) -> str:
    profile = task["input"]["prospect_profile"]
    bench = task["input"]["bench_summary"]
    company = normalize_whitespace(profile["company"]).replace(" ", "_")
    title = normalize_whitespace(profile["title"]).replace(" ", "_")
    stacks = "_".join(normalize_whitespace(stack).replace(" ", "_") for stack in bench["supported_stacks"])
    return " ".join(
        [
            f"company={company}",
            f"title={title}",
            f"profile={profile['employee_count']}_{task['metadata']['signal_type']}_{task['metadata']['signal_confidence']}",
            f"timing={task['input']['signal_date']}",
            f"capacity={task['metadata']['bench_state']}_{bench['available_engineers']}_{bench['earliest_start_days']}",
            f"stacks={stacks}",
            f"probe={task['metadata']['probe_id']}",
        ]
    ).lower()


def judge_scores(task: dict[str, Any], judge_family: str) -> dict[str, int]:
    text = task_text(task)
    coherence = 5
    verifiability = 5
    clarity = 4
    if any(phrase in text for phrase in BANNED_PHRASES):
        coherence -= 1
        clarity -= 1
    if "bench" in text:
        verifiability -= 1
    if "quick chat" in text or "world-class" in text:
        coherence -= 1
    if task["metadata"]["signal_confidence"] == "low" and "cannot tell" not in text and "if " not in text:
        verifiability -= 1
    if judge_family == task["metadata"].get("model_family"):
        verifiability -= 2
    return {
        "coherence": max(1, coherence),
        "verifiability": max(1, verifiability),
        "rubric_clarity": max(1, clarity),
    }


def judge_pass(scores: dict[str, int]) -> bool:
    return (
        scores["coherence"] >= 3
        and scores["verifiability"] >= 4
        and scores["rubric_clarity"] >= 3
    )


def dedup_key(task: dict[str, Any]) -> str:
    body = normalize_whitespace(task["candidate_output"]["body"])
    subject = normalize_whitespace(task["candidate_output"]["subject"])
    probe = task["metadata"]["probe_id"]
    company = normalize_whitespace(task["input"]["prospect_profile"]["company"])
    return hashlib.sha1(f"{probe}|{company}|{subject}|{body}".encode("utf-8")).hexdigest()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def token_ngrams(text: str, n: int = 8) -> set[tuple[str, ...]]:
    tokens = re.findall(r"[a-z0-9_=:-]+", text.lower())
    return {tuple(tokens[i:i + n]) for i in range(max(0, len(tokens) - n + 1))}


def cosine_similarity(task_a: dict[str, Any], task_b: dict[str, Any]) -> float:
    tokens_a = Counter(re.findall(r"[a-z0-9_=:-]+", contamination_text(task_a)))
    tokens_b = Counter(re.findall(r"[a-z0-9_=:-]+", contamination_text(task_b)))
    shared = set(tokens_a) & set(tokens_b)
    numerator = sum(tokens_a[token] * tokens_b[token] for token in shared)
    denom_a = math.sqrt(sum(value * value for value in tokens_a.values()))
    denom_b = math.sqrt(sum(value * value for value in tokens_b.values()))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / (denom_a * denom_b)


def split_counts(total: int) -> tuple[int, int, int]:
    train = total // 2
    dev = round(total * 0.3)
    held_out = total - train - dev
    return train, dev, held_out
