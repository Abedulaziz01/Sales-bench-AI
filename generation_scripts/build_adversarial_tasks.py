"""Build hand-authored adversarial Tenacious-Bench tasks and notes."""

from __future__ import annotations

from pathlib import Path

from common import SIGNATURE, append_log, ensure_dirs, make_task, write_jsonl


EDGE_CASES = [
    {
        "slug": "overcommitted_bench_urgent_signal",
        "probe_id": "PROBE-003",
        "brief": "Prospect needs 8 Go/infra engineers in 14 days after a funding event. Current confirmed capacity supports 3 starts in 21 days.",
        "design_note": "Forces the agent to refuse an attractive but unsupported availability promise and route to human or partial commit.",
    },
    {
        "slug": "layoff_misread_as_growth",
        "probe_id": "PROBE-004",
        "brief": "Public signal is a 15% layoff and a single replacement posting. Correct framing is cost pressure, not growth acceleration.",
        "design_note": "Defeats generic growth templates that misread any hiring post as expansion.",
    },
    {
        "slug": "high_ai_maturity_smb_short_form",
        "probe_id": "PROBE-006",
        "brief": "SMB prospect has 35 employees, AI maturity 3, and public peer pressure. The correct tone is punchy and short, not enterprise-long.",
        "design_note": "Punishes verbose enterprise-style outreach that ignores company size and speed expectations.",
    },
    {
        "slug": "signal_85_days_old",
        "probe_id": "PROBE-011",
        "brief": "Signal is 85 days old and still directionally useful, but must be caveated as potentially stale.",
        "design_note": "Requires the agent to name freshness limits instead of asserting as if the signal happened yesterday.",
    },
    {
        "slug": "prior_thread_no_reintro",
        "probe_id": "PROBE-012",
        "brief": "A prior thread already covered who Tenacious is. The next email must continue context instead of reintroducing the company from scratch.",
        "design_note": "Defeats generic first-touch templates that restart the conversation and ignore thread history.",
    },
]


def build_task(index: int, edge_case: dict, variant: int) -> dict:
    company = f"Adversarial-{index:02d}-{variant:02d}"
    contact = f"Prospect{index:02d}{variant:02d}"
    body = (
        f"Hi {contact},\n\n"
        f"{edge_case['brief']}\n\n"
        "What matters here is whether the agent preserves Tenacious tone under pressure and grounds every claim to what the brief actually supports.\n\n"
        "Would 15 minutes be useful?\n\nBest,"
    )
    if edge_case["slug"] == "high_ai_maturity_smb_short_form":
        body = (
            f"Hi {contact},\n\n"
            "Three peer teams shipped AI workflow updates this quarter. If this is live on your roadmap too, I can send one short note on how they staffed the first phase.\n\n"
            "Worth sending?\n\nBest,"
        )
    if edge_case["slug"] == "signal_85_days_old":
        body = (
            f"Hi {contact},\n\n"
            "The hiring signal I saw is 85 days old, so I may be looking at a stale snapshot. If the need is still active, I can share how similar teams handled the same constraint without overcommitting early.\n\n"
            "Would that be useful?\n\nBest,"
        )
    prior_thread = None
    if edge_case["slug"] == "prior_thread_no_reintro":
        prior_thread = "December thread covered Tenacious capabilities and current stack."
        body = (
            f"Hi {contact},\n\n"
            "Picking up from your December note on the Snowflake and dbt rebuild: three adjacent teams made the same shift this quarter. If the workstream is still open, I can send the two implementation trade-offs that mattered most.\n\n"
            "Would that be useful?\n\nBest,"
        )
    return make_task(
        task_id=f"ADV-{index:02d}-{variant:02d}",
        source_mode="hand-authored",
        probe_id=edge_case["probe_id"],
        trace_id=None,
        segment="specialized_capability_gap" if index % 2 else "mid_market_cost_restructure",
        signal_type="adversarial_edge_case",
        signal_confidence="medium",
        company=company,
        contact_name=contact,
        title="VP Engineering",
        employee_count=35 if edge_case["slug"] == "high_ai_maturity_smb_short_form" else 240,
        signal_date=f"2026-03-{10 + variant:02d}",
        brief=edge_case["brief"],
        subject=f"Question: adversarial check {index:02d}-{variant:02d}",
        body=body,
        stack=["Go", "Infra"] if edge_case["slug"] == "overcommitted_bench_urgent_signal" else ["Python", "Data"],
        available_engineers=3 if edge_case["slug"] == "overcommitted_bench_urgent_signal" else 4,
        earliest_start_days=21 if edge_case["slug"] == "overcommitted_bench_urgent_signal" else 14,
        bench_state="tight" if edge_case["slug"] == "overcommitted_bench_urgent_signal" else "supported",
        difficulty="adversarial",
        prior_thread=prior_thread,
        notes=edge_case["design_note"],
    )


def main() -> int:
    ensure_dirs()
    tasks = []
    note_lines = ["# Adversarial Task Design Notes", ""]
    for index, edge_case in enumerate(EDGE_CASES, start=1):
        for variant in range(1, 7):
            task = build_task(index, edge_case, variant)
            tasks.append(task)
            note_lines.append(f"## {task['task_id']}")
            note_lines.append(f"- Probe expansion: {edge_case['probe_id']}")
            note_lines.append(f"- Why it defeats the baseline: {edge_case['design_note']}")
            note_lines.append("- What the agent must do to pass: stay grounded, preserve tone, and choose the correct routing or framing.")
            note_lines.append("")
    out_path = Path("dataset/adversarial_tasks.jsonl")
    notes_path = Path("dataset/adversarial_notes.md")
    count = write_jsonl(out_path, tasks)
    notes_path.write_text("\n".join(note_lines) + "\n", encoding="utf-8")
    log_path = append_log(
        "build_adversarial_tasks",
        [
            f"output_file={out_path}",
            f"notes_file={notes_path}",
            f"task_count={count}",
            f"edge_case_count={len(EDGE_CASES)}",
        ],
    )
    print(f"Generated {count} adversarial tasks -> {out_path}")
    print(f"Notes written to {notes_path}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
