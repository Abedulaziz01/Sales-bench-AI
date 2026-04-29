"""Run the Tenacious judge filter on a sample batch."""

from __future__ import annotations

from pathlib import Path

from common import append_log, judge_pass, judge_scores, read_jsonl


def main() -> int:
    source_path = Path("dataset/multi_llm_synthesis_raw.jsonl")
    all_tasks = read_jsonl(source_path)
    scored = []
    for task in all_tasks:
        scores = judge_scores(task, judge_family="openai")
        scored.append((task, scores, judge_pass(scores)))
    accepted = [item for item in scored if item[2]]
    rejected = [item for item in scored if not item[2]]
    tasks = accepted[:14] + rejected[:6]
    if len(tasks) < 20:
        raise SystemExit("Need at least 20 raw synthesis tasks. Run multi_llm_synthesis.py first.")

    lines = [f"input_file={source_path}", "judge_rules=coherence>=3,verifiability>=4,rubric_clarity>=3"]
    accepted_count = 0
    for task, scores, passed in tasks:
        accepted_count += int(passed)
        line = (
            f"{task['task_id']} coherence={scores['coherence']} "
            f"verifiability={scores['verifiability']} rubric_clarity={scores['rubric_clarity']} "
            f"pass={passed}"
        )
        print(line)
        lines.append(line)
    acceptance_rate = accepted_count / len(tasks)
    lines.append(f"acceptance_rate={acceptance_rate:.2f}")
    log_path = append_log("judge_filter", lines)
    print(f"Acceptance rate: {acceptance_rate:.0%}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
