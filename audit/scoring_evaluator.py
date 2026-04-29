"""
Tenacious-Bench Scoring Evaluator
Reads schema.json, scores each task automatically, no human input required.
"""

import json
import os
import re
import sys


BANNED_PHRASES = [
    "hope you are well",
    "hope this finds you",
    "touching base",
    "circling back",
    "just following up",
    "as per my last email",
    "going forward",
    "synergy",
    "leverage",
    "lots of companies like yours",
]

CALENDAR_LINK_PATTERN = r"https?://cal\.[a-zA-Z0-9./\-]+"


def check_banned_phrases(text: str) -> bool:
    """Return True if any banned phrase is found."""
    text_lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase.lower() in text_lower:
            return True
    return False


def check_signal_referenced(output: str, brief: str) -> bool:
    """
    Check whether the output references at least one key term from the brief.
    """
    brief_words = {word.lower() for word in re.findall(r"\b[A-Za-z]{4,}\b", brief)}
    output_words = {word.lower() for word in re.findall(r"\b[A-Za-z]{4,}\b", output)}
    overlap = brief_words & output_words
    return len(overlap) >= 3


def check_calendar_link(text: str) -> bool:
    """Return True if a calendar link is present."""
    return bool(re.search(CALENDAR_LINK_PATTERN, text))


def check_bench_accuracy(output: str, bench_summary: str) -> bool:
    """
    Check whether bench claims in the output match the bench summary.
    """
    bench_lower = bench_summary.lower()
    output_lower = output.lower()

    if "available: 0" in bench_lower:
        false_claims = [
            "available immediately",
            "available now",
            "ready to start",
            "on our bench right now",
            "need any engineers",
        ]
        for claim in false_claims:
            if claim in output_lower:
                return False
    return True


def simple_tone_score(output: str) -> int:
    """
    Simple rule-based tone scorer (1-5).
    In production this would call an LLM judge.
    """
    score = 3
    output_lower = output.lower()

    if any(word in output_lower for word in ["noticed", "saw", "spotted"]):
        score += 1

    if any(phrase in output_lower for phrase in ["would you have 20 minutes", "explore fit"]):
        score += 1

    if check_banned_phrases(output):
        score -= 1

    if output_lower.startswith("hi there") or "asap" in output_lower:
        score -= 1

    if any(phrase in output_lower for phrase in ["book a call", "next hire"]):
        score -= 1

    return max(1, min(5, score))


def score_task(task: dict) -> dict:
    """Score one task and return the rubric results."""
    output = task["candidate_output"]
    brief = task["input"]["hiring_signal_brief"]
    bench = task["input"]["bench_summary"]

    banned = check_banned_phrases(output)
    signal = check_signal_referenced(output, brief)
    cal_link = check_calendar_link(output)
    bench_ok = check_bench_accuracy(output, bench)

    tone = simple_tone_score(output)
    grounding = 1 if signal else 0
    bench_score = 1 if bench_ok else 0
    cta = 1 if cal_link else 0

    tone_contribution = tone - 1
    total = tone_contribution + grounding + bench_score + cta

    return {
        "task_id": task["task_id"],
        "difficulty": task["difficulty"],
        "scores": {
            "tone_score": tone,
            "grounding_score": grounding,
            "bench_accuracy": bench_score,
            "cta_present": cta,
            "total_score": total,
        },
        "ground_truth_checks": {
            "banned_phrases_present": banned,
            "signal_referenced": signal,
            "calendar_link_present": cal_link,
            "bench_state_accurate": bench_ok,
        },
    }


def main() -> int:
    schema_path = os.path.join(os.path.dirname(__file__), "schema.json")
    with open(schema_path, encoding="utf-8") as file:
        schema = json.load(file)

    examples = schema["examples"]
    print(f"Loaded {len(examples)} tasks from schema.json\n")
    print("=" * 50)

    results = []
    for task in examples:
        result = score_task(task)
        results.append(result)

        print(f"Task ID : {result['task_id']}")
        print(f"Difficulty : {result['difficulty']}")
        print(f"Tone Score : {result['scores']['tone_score']} / 5")
        print(f"Grounding : {result['scores']['grounding_score']} / 1")
        print(f"Bench Accuracy : {result['scores']['bench_accuracy']} / 1")
        print(f"CTA Present : {result['scores']['cta_present']} / 1")
        print(f"TOTAL SCORE : {result['scores']['total_score']} / 7")
        print("-" * 50)

    print(f"\nScored {len(results)} tasks successfully. No human input required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
