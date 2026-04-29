"""Generate programmatic sweep Tenacious-Bench tasks."""

from __future__ import annotations

from pathlib import Path

from common import PROGRAMMATIC_DIMENSIONS, append_log, body_for, ensure_dirs, make_task, subject_for, write_jsonl


SIGNAL_LINES = {
    "funding_event": "You closed a fresh funding round and your hiring pattern suggests a delivery-capacity question is coming into focus.",
    "job_post_velocity": "Your open engineering roles increased recently, which can indicate demand outrunning the existing hiring funnel.",
    "layoff_event": "Your recent restructuring changes the cost profile without removing the need to keep shipping.",
    "leadership_change": "A new engineering leader typically reassesses delivery model choices within the first 90 days.",
}


def main() -> int:
    ensure_dirs()
    tasks = []
    company_sizes = PROGRAMMATIC_DIMENSIONS["company_size"]
    bench_states = PROGRAMMATIC_DIMENSIONS["bench_state"]
    signal_types = PROGRAMMATIC_DIMENSIONS["signal_type"]
    variant_counter = 0
    for company_size_label, employee_count in company_sizes:
        for bench_state_label, available_engineers, earliest_start_days in bench_states:
            for signal_type in signal_types:
                for variant in range(6):
                    variant_counter += 1
                    confidence = "low" if signal_type == "job_post_velocity" and variant % 2 else "high"
                    company = f"{company_size_label.title()}-{signal_type[:4].upper()}-{variant:02d}"
                    contact = f"Contact{variant:02d}"
                    stack = ["Python", "Data"] if signal_type != "leadership_change" else ["Go", "Infra"]
                    stale_note = None
                    if variant == 5:
                        stale_note = "The public signal is close to ninety days old, so the timing may already have shifted."
                    body = body_for(
                        company=company,
                        contact_name=contact,
                        signal_line=SIGNAL_LINES[signal_type],
                        bench_state=bench_state_label,
                        confidence=confidence,
                        stack_label=" and ".join(stack),
                        stale_note=stale_note,
                    )
                    tasks.append(
                        make_task(
                            task_id=f"PS-{variant_counter:03d}",
                            source_mode="programmatic",
                            probe_id=f"PROBE-{20 + (variant_counter % 10):03d}",
                            trace_id=None,
                            segment="mid_market_cost_restructure" if signal_type == "layoff_event" else "series_a_b_hiring",
                            signal_type=signal_type,
                            signal_confidence=confidence,
                            company=company,
                            contact_name=contact,
                            title="VP Engineering",
                            employee_count=employee_count,
                            signal_date=f"2026-0{(variant % 4) + 1}-{10 + variant:02d}",
                            brief=SIGNAL_LINES[signal_type],
                            subject=subject_for(signal_type, variant, confidence),
                            body=body,
                            stack=stack,
                            available_engineers=available_engineers,
                            earliest_start_days=earliest_start_days,
                            bench_state=bench_state_label,
                            difficulty="easy" if bench_state_label == "supported" else "medium",
                            notes="Programmatic sweep over company_size, bench_state, and signal_type slots.",
                        )
                    )
    out_path = Path("dataset/programmatic_tasks.jsonl")
    count = write_jsonl(out_path, tasks)
    grid_size = len(company_sizes) * len(bench_states) * len(signal_types)
    log_path = append_log(
        "programmatic_sweep",
        [
            f"output_file={out_path}",
            f"parameter_grid_size={grid_size}",
            "varied_dimensions=company_size,bench_state,signal_type",
            f"task_count={count}",
        ],
    )
    print(f"Parameter grid size: {grid_size}")
    print(f"Generated {count} programmatic sweep tasks -> {out_path}")
    print(f"Log written to {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
