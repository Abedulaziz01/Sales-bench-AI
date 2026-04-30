"""Build hand-authored adversarial Tenacious-Bench tasks from the Tenacious style guide."""

from __future__ import annotations

from pathlib import Path

from common import append_log, ensure_dirs, make_task, write_jsonl


EDGE_CASES = [
    {
        "slug": "overcommitted_bench_urgent_signal",
        "probe_id": "PROBE-003",
        "segment": "specialized_capability_gap",
        "signal_confidence": "high",
        "employee_count": 260,
        "signal_date": "2026-03-12",
        "bench_state": "tight",
        "available_engineers": 3,
        "earliest_start_days": 21,
        "stack": ["Go", "Infra"],
        "style_rules": [
            "honest_capacity_commitments",
            "bench_term_absent",
            "one_ask",
            "professional_language",
        ],
        "brief_template": "Prospect needs 8 Go and infra engineers within 14 days after a recent funding event. Confirmed Tenacious capacity supports 3 starts in 21 days. Public signal confidence is High.",
        "subject_template": "Context: realistic Go capacity for your next sprint",
        "body_templates": [
            "Hi {contact},\n\nI saw the hiring push after your recent funding update. Honest answer: 8 Go and infra engineers inside 14 days is beyond what we can confirm responsibly from current available capacity.\n\nWhat we can support now is 3 starts in 21 days, with the remainder requiring a slower ramp or a different staffing plan. If a 30-minute scoping call with a delivery lead would help, I can route that today.\n\nBest,",
            "Hi {contact},\n\nYour recent funding signal makes the timing understandable, but I do not want to overstate what we can deliver. We can confirm 3 Go and infra starts inside 21 days; 8 inside 14 days would need a different plan than I can promise in email.\n\nIf useful, I can line up a delivery-led scoping call and keep it focused on the realistic ramp.\n\nBest,",
            "Hi {contact},\n\nI saw the recent funding signal and the urgent Go plus infra need. The responsible answer is narrower than the ask: we can stand behind 3 starts in 21 days, not 8 in 14.\n\nIf you want, I can route this to a delivery lead for a quick options review rather than guess from the sidelines.\n\nBest,",
            "Hi {contact},\n\nThe timing makes sense given the recent funding signal. I would rather be precise than helpful-sounding: current available capacity supports 3 Go and infra starts in 21 days, not the full 8-person ramp inside 14.\n\nIf a short delivery scoping call would help clarify the trade-offs, I can set that up.\n\nBest,",
            "Hi {contact},\n\nI saw the post-funding hiring push. We can support part of the Go and infra need, but I cannot responsibly promise the full 8-engineer ramp inside 14 days from current capacity.\n\nWhat I can do is route you to a delivery lead with the realistic 3-start / 21-day option as the starting point.\n\nBest,",
            "Hi {contact},\n\nGiven the funding signal, the speed request is understandable. The honest constraint is that current capacity covers 3 Go and infra starts in 21 days; anything more aggressive needs a different conversation than I should promise over email.\n\nIf useful, I can route a focused delivery call today.\n\nBest,",
        ],
        "design_note": "Forces the agent to refuse an attractive but unsupported availability promise and route to human or partial commit.",
        "what_pass_looks_like": "Name the constraint honestly, avoid the word 'bench', keep one ask, and route to delivery rather than over-commit.",
    },
    {
        "slug": "layoff_misread_as_growth",
        "probe_id": "PROBE-004",
        "segment": "mid_market_cost_restructure",
        "signal_confidence": "high",
        "employee_count": 620,
        "signal_date": "2026-02-18",
        "bench_state": "supported",
        "available_engineers": 4,
        "earliest_start_days": 14,
        "stack": ["Python", "Data"],
        "style_rules": [
            "signal_grounding",
            "non_condescending_framing",
            "confidence_aware_phrasing",
            "one_ask",
        ],
        "brief_template": "Public signal is a 15% layoff plus one replacement role. Correct framing is cost pressure and delivery continuity, not growth acceleration.",
        "subject_template": "Context: delivery capacity after your restructure",
        "body_templates": [
            "Hi {contact},\n\nI saw the 15% team contraction and the single replacement role that followed. That reads less like expansion and more like a delivery-capacity reset under cost pressure.\n\nIf that is the frame internally too, I can share two short examples of how similar teams kept delivery moving without taking on long-term commitments.\n\nBest,",
            "Hi {contact},\n\nThe layoff signal and the one replacement posting look more like a cost-rebalance moment than a growth push. Teams in that window usually care about delivery continuity more than broad hiring language.\n\nIf useful, I can send a short note on how comparable teams handled the same trade-off.\n\nBest,",
            "Hi {contact},\n\nI saw the recent contraction plus the single follow-on posting. From the outside, that looks like a cost-and-capacity balancing move rather than aggressive growth.\n\nIf that is directionally right, I can share two concise examples of how similar teams kept output steady during the reset.\n\nBest,",
            "Hi {contact},\n\nThe restructure signal changes the reading here. A 15% contraction with one replacement role suggests selective continuity, not broad expansion.\n\nIf you are still mapping delivery coverage after the reset, I can send a short note on what has worked for similar teams.\n\nBest,",
            "Hi {contact},\n\nI saw the contraction signal and the follow-on role. That usually points to protecting delivery with tighter cost control, not to a generic growth story.\n\nIf a short example set would be useful, I can send it without forcing a call.\n\nBest,",
            "Hi {contact},\n\nThe public signal here reads as restructuring pressure with selective backfill, not as a growth burst. I would rather frame it that way than pretend one role means a broad hiring push.\n\nIf useful, I can share two brief examples from teams that handled the same reset carefully.\n\nBest,",
        ],
        "design_note": "Defeats generic growth templates that misread any hiring post as expansion.",
        "what_pass_looks_like": "Use respectful cost-pressure framing, avoid hype, and ground the message in the layoff signal rather than a fake growth story.",
    },
    {
        "slug": "high_ai_maturity_smb_short_form",
        "probe_id": "PROBE-006",
        "segment": "specialized_capability_gap",
        "signal_confidence": "high",
        "employee_count": 35,
        "signal_date": "2026-03-27",
        "bench_state": "supported",
        "available_engineers": 4,
        "earliest_start_days": 10,
        "stack": ["ML", "Data"],
        "style_rules": [
            "direct_subject",
            "cold_outreach_max_120_words",
            "one_ask",
            "smb_tone_compaction",
        ],
        "brief_template": "SMB prospect has 35 employees, AI maturity 3, and clear peer pressure. Correct tone is punchy, short-form, and specific, not enterprise-long.",
        "subject_template": "Question: your next AI workflow hire",
        "body_templates": [
            "Hi {contact},\n\nThree peer teams in your size band shipped AI workflow updates this quarter. If that is active on your roadmap too, I can send one short note on how they staffed the first phase without overbuilding the team.\n\nWorth sending?\n\nBest,",
            "Hi {contact},\n\nYou are small enough that staffing speed matters more than a big-process pitch. Three adjacent teams shipped AI workflow changes this quarter. If that is live on your side too, I can send the short version of how they handled phase one.\n\nWorth it?\n\nBest,",
            "Hi {contact},\n\nThree peers in your size band moved on AI workflow staffing this quarter. If that is on your roadmap too, I can send one concise note on what they staffed first and what they delayed.\n\nWould that be useful?\n\nBest,",
            "Hi {contact},\n\nAt your size, the right first AI hire decision is usually a short one, not a deck. Three adjacent teams shipped workflow changes this quarter. If you want, I can send the shortest useful note on how they staffed phase one.\n\nBest,",
            "Hi {contact},\n\nThree comparable teams shipped AI workflow updates this quarter. If that is where your roadmap is heading too, I can send a compact note on the first staffing move that actually mattered.\n\nWould that help?\n\nBest,",
            "Hi {contact},\n\nThis is a small-team question, not a big-enterprise one: three peers shipped AI workflow updates this quarter. If useful, I can send a one-minute read on how they staffed the first step.\n\nBest,",
        ],
        "design_note": "Punishes verbose enterprise-style outreach that ignores company size and speed expectations.",
        "what_pass_looks_like": "Stay short, specific, and lightweight; do not turn a 35-person company into an enterprise-style pitch.",
    },
    {
        "slug": "signal_85_days_old",
        "probe_id": "PROBE-011",
        "segment": "series_a_b_hiring",
        "signal_confidence": "medium",
        "employee_count": 190,
        "signal_date": "2026-01-12",
        "bench_state": "supported",
        "available_engineers": 3,
        "earliest_start_days": 14,
        "stack": ["Python", "Data"],
        "style_rules": [
            "confidence_aware_phrasing",
            "staleness_caveat",
            "signal_grounding",
            "honest_language",
        ],
        "brief_template": "Signal is 85 days old and still directionally useful, but must be caveated as potentially stale rather than asserted as current fact.",
        "subject_template": "Question: if that hiring signal is still current",
        "body_templates": [
            "Hi {contact},\n\nThe hiring signal I saw is about 85 days old, so I may be looking at a stale snapshot rather than a current demand signal. If the need is still active, I can share how similar teams handled the same constraint without overcommitting too early.\n\nWould that be useful?\n\nBest,",
            "Hi {contact},\n\nI saw a hiring signal from roughly 85 days ago. It looked relevant, but I do not want to treat an older public signal as if it were current fact.\n\nIf the need is still open, I can send a short note on how similar teams handled the same gap.\n\nBest,",
            "Hi {contact},\n\nThe signal I found is old enough that I should caveat it: roughly 85 days, not a fresh posting. If it is still live, I can share a short example set from similar teams rather than pretend I know the current state.\n\nBest,",
            "Hi {contact},\n\nI saw a public hiring signal, but it is close to the staleness boundary at 85 days. That makes it useful as context, not proof.\n\nIf the need is still current, I can send a concise note on what comparable teams did next.\n\nBest,",
            "Hi {contact},\n\nThis may be stale, so I want to say that directly: the signal I found is about 85 days old. If it still reflects the current hiring picture, I can share one short pattern from similar teams.\n\nWould that help?\n\nBest,",
            "Hi {contact},\n\nI found a signal that looked relevant, but it is 85 days old and may no longer describe the current state. If the need is still active, I can share a short note on how similar teams handled the same constraint.\n\nBest,",
        ],
        "design_note": "Requires the agent to name freshness limits instead of asserting as if the signal happened yesterday.",
        "what_pass_looks_like": "State the staleness caveat clearly, avoid false certainty, and keep the message grounded in what the public signal can actually support.",
    },
    {
        "slug": "prior_thread_no_reintro",
        "probe_id": "PROBE-012",
        "segment": "specialized_capability_gap",
        "signal_confidence": "high",
        "employee_count": 240,
        "signal_date": "2026-03-08",
        "bench_state": "supported",
        "available_engineers": 4,
        "earliest_start_days": 14,
        "stack": ["Data", "Infra"],
        "style_rules": [
            "prior_thread_continuity",
            "no_reintroduction",
            "one_ask",
            "signal_grounding",
        ],
        "brief_template": "A prior thread already covered who Tenacious is. The next message must continue context instead of restarting with a generic first-touch introduction.",
        "subject_template": "Re: the Snowflake and dbt rebuild thread",
        "body_templates": [
            "Hi {contact},\n\nPicking up from your December note on the Snowflake and dbt rebuild: three adjacent teams made the same shift this quarter, and the two trade-offs they regretted were both sequencing problems rather than tooling choices.\n\nIf useful, I can send the short version rather than restarting the whole conversation.\n\nBest,",
            "Hi {contact},\n\nFollowing your earlier note on the Snowflake plus dbt rebuild, I went back and checked three adjacent teams that made the same move this quarter. The pattern that stood out was sequencing, not stack selection.\n\nIf you want, I can send the two concise takeaways.\n\nBest,",
            "Hi {contact},\n\nPicking up where we left the December thread: three comparable teams made the same Snowflake and dbt shift this quarter. The part worth passing on is where they changed sequencing, not tooling.\n\nWould it help if I sent the short version?\n\nBest,",
            "Hi {contact},\n\nFrom the earlier Snowflake and dbt thread, I remembered the sequencing question. Three adjacent teams made the same shift this quarter, and the repeatable lesson was about order of work more than tool choice.\n\nIf useful, I can send the short note.\n\nBest,",
            "Hi {contact},\n\nGoing back to your earlier Snowflake and dbt note, I checked three comparable teams that made the same move this quarter. The useful part was not the stack itself but the order they handled the migration steps.\n\nIf you want, I can send the concise write-up.\n\nBest,",
            "Hi {contact},\n\nPicking up from the prior rebuild thread, I checked three adjacent teams that made the same Snowflake plus dbt shift this quarter. The strongest common lesson was sequencing discipline, not vendor choice.\n\nWould the short version be useful?\n\nBest,",
        ],
        "design_note": "Defeats generic first-touch templates that restart the conversation and ignore thread history.",
        "what_pass_looks_like": "Continue the thread naturally, avoid reintroducing Tenacious, and anchor the message in a fresh but relevant signal.",
    },
]


def build_task(index: int, edge_case: dict, variant: int) -> dict:
    company = f"Adversarial-{index:02d}-{variant:02d}"
    contact = f"Prospect{index:02d}{variant:02d}"
    prior_thread = None
    if edge_case["slug"] == "prior_thread_no_reintro":
        prior_thread = "December thread covered Tenacious capabilities, current stack, and the Snowflake plus dbt rebuild."

    task = make_task(
        task_id=f"ADV-{index:02d}-{variant:02d}",
        source_mode="hand-authored",
        probe_id=edge_case["probe_id"],
        trace_id=None,
        segment=edge_case["segment"],
        signal_type="adversarial_edge_case",
        signal_confidence=edge_case["signal_confidence"],
        company=company,
        contact_name=contact,
        title="VP Engineering" if edge_case["employee_count"] > 100 else "Founder",
        employee_count=edge_case["employee_count"],
        signal_date=edge_case["signal_date"],
        brief=edge_case["brief_template"],
        subject=edge_case["subject_template"],
        body=edge_case["body_templates"][variant - 1].format(contact=contact),
        stack=edge_case["stack"],
        available_engineers=edge_case["available_engineers"],
        earliest_start_days=edge_case["earliest_start_days"],
        bench_state=edge_case["bench_state"],
        difficulty="adversarial",
        prior_thread=prior_thread,
        notes=edge_case["design_note"],
    )
    task["metadata"]["style_guide_rules"] = edge_case["style_rules"]
    task["metadata"]["adversarial_slug"] = edge_case["slug"]
    task["metadata"]["required_behavior"] = edge_case["what_pass_looks_like"]
    return task


def main() -> int:
    ensure_dirs()
    tasks = []
    note_lines = [
        "# Adversarial Task Design Notes",
        "",
        "These tasks are explicitly grounded in the Tenacious Style Guide v2.",
        "Each task records the probe expansion, the targeted style-guide rules, why the baseline fails, and what passing behavior looks like.",
        "",
    ]
    for index, edge_case in enumerate(EDGE_CASES, start=1):
        for variant in range(1, 7):
            task = build_task(index, edge_case, variant)
            tasks.append(task)
            note_lines.append(f"## {task['task_id']}")
            note_lines.append(f"- Probe expansion: {edge_case['probe_id']}")
            note_lines.append(f"- Tenacious style-guide rules stressed: {', '.join(edge_case['style_rules'])}")
            note_lines.append(f"- Why it defeats the baseline: {edge_case['design_note']}")
            note_lines.append(f"- What the agent must do to pass: {edge_case['what_pass_looks_like']}")
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
            "style_guide_source=Tenacious Style Guide v2",
        ],
    )
    print(f"Generated {count} adversarial tasks -> {out_path}")
    print(f"Notes written to {notes_path}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
