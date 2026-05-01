"""Verify Phase 4 scaffolding and locally runnable ablation outputs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    train_script = ROOT / "training" / "train.py"
    ablation_script = ROOT / "ablations" / "run_ablations.py"
    bootstrap_script = ROOT / "ablations" / "bootstrap_test.py"
    results_path = ROOT / "ablations" / "ablation_results.json"
    traces_path = ROOT / "ablations" / "held_out_traces.jsonl"
    cost_path = ROOT / "ablations" / "cost_pareto.json"

    for path in [train_script, ablation_script, bootstrap_script, results_path, traces_path, cost_path]:
        require(path.exists(), f"Missing required Phase 4 file: {path}")

    results = json.loads(results_path.read_text(encoding="utf-8"))
    for key in ["delta_a", "delta_b", "cost_pareto"]:
        require(key in results, f"Missing {key} in ablation_results.json")
        require("95_ci" in results[key], f"Missing 95_ci in {key}")
        require("p_value" in results[key], f"Missing p_value in {key}")
        require("n_tasks" in results[key], f"Missing n_tasks in {key}")

    trace_lines = [line for line in traces_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(len(trace_lines) > 0, "held_out_traces.jsonl is empty")
    require(results["delta_a"]["delta"] > 0, "Delta A must be positive")
    require(results["delta_a"]["p_value"] < 0.05, "Delta A p-value must be < 0.05")

    print("Phase 4 scaffold verification passed.")
    print(f"delta_a={results['delta_a']['delta']:+.4f}")
    print(f"delta_a_p={results['delta_a']['p_value']:.4f}")
    print(f"held_out_trace_lines={len(trace_lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
