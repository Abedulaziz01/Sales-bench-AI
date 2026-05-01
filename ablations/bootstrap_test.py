"""Print the ablation summary and deployment recommendation."""

from __future__ import annotations

import json
from pathlib import Path


RESULTS_PATH = Path("ablations/ablation_results.json")


def main() -> int:
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    delta_a = results["delta_a"]
    delta_b = results["delta_b"]
    cost_pareto = results["cost_pareto"]

    print("=" * 44)
    print("DELTA A - Trained vs Baseline")
    print(f"  Tasks scored : {delta_a['n_tasks']}")
    print(f"  Delta        : {delta_a['delta']:+.4f}")
    print(f"  95% CI       : [{delta_a['95_ci'][0]:.4f}, {delta_a['95_ci'][1]:.4f}]")
    print(f"  p-value      : {delta_a['p_value']:.4f}")
    if delta_a["p_value"] < 0.05 and delta_a["delta"] > 0:
        print("  RESULT       : PASS - p < 0.05, deploy recommended")
    else:
        print("  RESULT       : FAIL - p >= 0.05 or delta <= 0")

    print()
    print("DELTA B - Trained vs Prompt-only")
    print(f"  Tasks scored : {delta_b['n_tasks']}")
    print(f"  Delta        : {delta_b['delta']:+.4f}")
    print(f"  95% CI       : [{delta_b['95_ci'][0]:.4f}, {delta_b['95_ci'][1]:.4f}]")
    print(f"  p-value      : {delta_b['p_value']:.4f}")

    print()
    print("COST PARETO")
    print(f"  Cost baseline    : ${cost_pareto['cost_per_task_baseline']:.4f}/task")
    print(f"  Cost with judge  : ${cost_pareto['cost_per_task_with_judge']:.4f}/task")
    print(f"  Latency baseline : {cost_pareto['latency_p50_baseline']:.4f}s")
    print(f"  Latency w/judge  : {cost_pareto['latency_p50_with_judge']:.4f}s")
    print("=" * 44)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
