"""
Tenacious-Bench scoring evaluator aligned to Tenacious Style Guide v2.
Reads schema.json, scores each task automatically, and prints results.
"""

from __future__ import annotations

import copy
import json
import os
import re
import sys
from typing import Any


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

CONDESCENDING_PHRASES = [
    "behind the curve",
    "falling behind",
    "you need to",
    "you should",
    "catch up",
    "missing",
]

SUBJECT_BAD_PREFIXES = ("quick", "just", "hey")
SUBJECT_GOOD_PREFIXES = ("request:", "follow-up:", "context:", "question:", "resource:", "re:")
CTA_PATTERNS = [
    "would 15 minutes",
    "would 20 minutes",
    "want me to send",
    "reply with",
    "book a call",
    "set up a 30-minute",
    "set up a 15-minute",
    "calendar is at",
]

REQUIRED_OUTPUT_FIELDS = {"subject", "body", "signature", "attachments"}


class EvaluationError(ValueError):
    """Raised when a task or candidate output is missing required scoring fields."""


def normalize(text: str) -> str:
    return text.lower().strip()


def validate_task(task: dict[str, Any]) -> None:
    required_top_level = {"task_id", "outreach_type", "signal_confidence", "input"}
    missing = required_top_level - set(task.keys())
    if missing:
        raise EvaluationError(f"Task missing required keys: {sorted(missing)}")
    if "hiring_signal_brief" not in task["input"]:
        raise EvaluationError("Task input must include `hiring_signal_brief`.")
    if "bench_summary" not in task["input"]:
        raise EvaluationError("Task input must include `bench_summary`.")


def validate_agent_output(agent_output: dict[str, Any]) -> None:
    if not isinstance(agent_output, dict):
        raise EvaluationError("agent_output must be a dict.")
    missing = REQUIRED_OUTPUT_FIELDS - set(agent_output.keys())
    if missing:
        raise EvaluationError(f"agent_output missing required keys: {sorted(missing)}")
    if not isinstance(agent_output["signature"], list):
        raise EvaluationError("agent_output['signature'] must be a list.")
    if not isinstance(agent_output["attachments"], list):
        raise EvaluationError("agent_output['attachments'] must be a list.")


def get_output(task: dict[str, Any]) -> dict[str, Any]:
    return task["candidate_output"]


def full_text(task: dict[str, Any]) -> str:
    output = get_output(task)
    parts = [output["subject"], output["body"], "\n".join(output.get("signature", []))]
    return "\n".join(parts)


def word_limit_for(outreach_type: str) -> int:
    if outreach_type == "warm_reply":
        return 200
    if outreach_type == "re_engagement":
        return 100
    return 120


def check_banned_phrases(text: str) -> bool:
    lowered = normalize(text)
    return any(phrase in lowered for phrase in BANNED_PHRASES)


def check_non_condescending(text: str) -> bool:
    lowered = normalize(text)
    return not any(phrase in lowered for phrase in CONDESCENDING_PHRASES)


def check_subject_length(subject: str) -> bool:
    return len(subject.strip()) <= 60


def check_word_count(task: dict[str, Any]) -> bool:
    body = get_output(task)["body"]
    limit = word_limit_for(task["outreach_type"])
    return len(body.split()) <= limit


def count_asks(body: str) -> int:
    lowered = normalize(body)
    count = sum(1 for pattern in CTA_PATTERNS if pattern in lowered)
    if count == 0 and "?" in body:
        count = 1
    return count


def check_one_ask(task: dict[str, Any]) -> bool:
    return count_asks(get_output(task)["body"]) == 1


def check_signature(task: dict[str, Any]) -> bool:
    signature = get_output(task).get("signature", [])
    return signature == [
        "Yabi",
        "Research Partner",
        "Tenacious Intelligence Corporation",
        "gettenacious.com",
    ]


def check_attachment_policy(task: dict[str, Any]) -> bool:
    output = get_output(task)
    body = normalize(output["body"])
    if task["outreach_type"] == "cold_email" and output.get("attachments"):
        return False
    return "[attachment" not in body


def check_signal_grounding(task: dict[str, Any]) -> bool:
    brief = normalize(task["input"]["hiring_signal_brief"])
    output_text = normalize(full_text(task))
    brief_words = {word for word in re.findall(r"\b[a-z]{4,}\b", brief)}
    output_words = {word for word in re.findall(r"\b[a-z]{4,}\b", output_text)}
    overlap = len(brief_words & output_words)
    shared_digits = any(token in output_text for token in re.findall(r"\b\d+\b", brief))
    return overlap >= 3 and (shared_digits or "series" in output_text or "roles" in output_text)


def check_confidence_aware(task: dict[str, Any]) -> bool:
    confidence = task["signal_confidence"]
    body = normalize(get_output(task)["body"])
    if confidence == "high":
        return True
    hedges = [
        "if ",
        "whether",
        "cannot tell",
        "might",
        "would",
        "is ",
        "are ",
        "?",
    ]
    return any(hedge in body for hedge in hedges)


def extract_engineer_commitment(text: str) -> int | None:
    match = re.search(r"\b(\d+)\s+(?:senior\s+)?(?:python|go|data|ml|infra|infrastructure)?\s*engineers?\b", normalize(text))
    if match:
        return int(match.group(1))
    return None


def extract_days(text: str) -> int | None:
    match = re.search(r"\b(\d+)\s+days?\b", normalize(text))
    if match:
        return int(match.group(1))
    if "two weeks" in normalize(text):
        return 14
    if "next friday" in normalize(text):
        return 7
    return None


def check_bench_term_absent(task: dict[str, Any]) -> bool:
    return "bench" not in normalize(full_text(task))


def check_bench_state_accuracy(task: dict[str, Any]) -> bool:
    output_text = full_text(task)
    bench = task["input"]["bench_summary"]
    committed_engineers = extract_engineer_commitment(output_text)
    committed_days = extract_days(output_text)
    if committed_engineers is not None and committed_engineers > bench["available_engineers"]:
        return False
    if committed_days is not None and committed_days < bench["earliest_start_days"]:
        return False
    return True


def check_pricing_scope(task: dict[str, Any]) -> bool:
    body = normalize(get_output(task)["body"])
    if "contract" in body or "payable" in body:
        return False
    if re.search(r"\$\d[\d,]{4,}", body):
        return False
    return True


def direct_score(task: dict[str, Any]) -> int:
    subject = normalize(get_output(task)["subject"])
    body = normalize(get_output(task)["body"])
    score = 5
    if not subject.startswith(SUBJECT_GOOD_PREFIXES):
        score -= 1
    if subject.startswith(SUBJECT_BAD_PREFIXES):
        score -= 2
    if not check_word_count(task):
        score -= 2
    if not check_one_ask(task):
        score -= 1
    if "i would love to" in body or "pain points" in body:
        score -= 1
    return max(1, min(5, score))


def grounded_score(task: dict[str, Any]) -> int:
    score = 5 if check_signal_grounding(task) else 1
    if not check_confidence_aware(task):
        score = min(score, 2)
    return score


def honest_score(task: dict[str, Any]) -> int:
    score = 5
    if not check_confidence_aware(task):
        score -= 2
    if not check_bench_state_accuracy(task):
        score -= 2
    if not check_pricing_scope(task):
        score -= 2
    if not check_signal_grounding(task):
        score -= 1
    return max(1, min(5, score))


def professional_score(task: dict[str, Any]) -> int:
    score = 5
    text = full_text(task)
    if check_banned_phrases(text):
        score -= 2
    if not check_bench_term_absent(task):
        score -= 2
    if not check_signature(task):
        score -= 1
    if not check_attachment_policy(task):
        score -= 1
    return max(1, min(5, score))


def non_condescending_score(task: dict[str, Any]) -> int:
    return 5 if check_non_condescending(full_text(task)) else 1


def score_task(task: dict[str, Any]) -> dict[str, Any]:
    validate_task(task)
    validate_agent_output(task["candidate_output"])
    checks = {
        "signal_grounded": check_signal_grounding(task),
        "confidence_aware": check_confidence_aware(task),
        "banned_phrases_present": check_banned_phrases(full_text(task)),
        "bench_term_absent": check_bench_term_absent(task),
        "bench_state_accurate": check_bench_state_accuracy(task),
        "pricing_scope_valid": check_pricing_scope(task),
        "word_count_ok": check_word_count(task),
        "subject_length_ok": check_subject_length(get_output(task)["subject"]),
        "one_ask": check_one_ask(task),
        "signature_valid": check_signature(task),
        "attachment_policy_valid": check_attachment_policy(task),
        "non_condescending_language": check_non_condescending(full_text(task)),
    }

    scores = {
        "direct_score": direct_score(task),
        "grounded_score": grounded_score(task),
        "honest_score": honest_score(task),
        "professional_score": professional_score(task),
        "non_condescending_score": non_condescending_score(task),
    }
    scores["total_score"] = sum(scores.values())

    return {
        "task_id": task["task_id"],
        "difficulty": task["difficulty"],
        "scores": scores,
        "ground_truth_checks": checks,
    }


def score_candidate(task: dict[str, Any], agent_output: dict[str, Any]) -> dict[str, Any]:
    """Score an arbitrary `(task, agent_output)` pair using the same evaluator contract."""
    validate_task(task)
    validate_agent_output(agent_output)
    task_copy = copy.deepcopy(task)
    task_copy["candidate_output"] = agent_output
    return score_task(task_copy)


def normalized_total_7(result: dict[str, Any]) -> float:
    """Map the 25-point rubric total onto the 7-point training-prep scale."""
    return round((result["scores"]["total_score"] / 25) * 7, 2)


def main() -> int:
    schema_path = os.path.join(os.path.dirname(__file__), "schema.json")
    with open(schema_path, encoding="utf-8") as file:
        schema = json.load(file)

    examples = schema["examples"]
    print(f"Loaded {len(examples)} tasks from schema.json\n")
    print("=" * 60)

    for task in examples:
        result = score_task(task)
        print(f"Task ID : {result['task_id']}")
        print(f"Difficulty : {result['difficulty']}")
        print(f"Direct : {result['scores']['direct_score']} / 5")
        print(f"Grounded : {result['scores']['grounded_score']} / 5")
        print(f"Honest : {result['scores']['honest_score']} / 5")
        print(f"Professional : {result['scores']['professional_score']} / 5")
        print(f"Non-condescending : {result['scores']['non_condescending_score']} / 5")
        print(f"TOTAL SCORE : {result['scores']['total_score']} / 25")
        print("-" * 60)

    print("\nScored all schema examples successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
