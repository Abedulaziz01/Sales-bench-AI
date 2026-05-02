# Synthesis Memo — Rafailov et al. (2023) DPO

## Core Takeaway

DPO provides a clean preference-optimization objective without full RL complexity. The central insight I used is that relative preference supervision can directly align outputs toward domain policy.

## Algorithm Choice Section

For Tenacious Path B, I chose ORPO rather than vanilla DPO.

- Chosen method in run log: `ORPO`
- Reason 1: simpler operational footprint for our constrained environment.
- Reason 2: no separate heavy reference-model management in our practical setup.
- Reason 3: better fit for small, high-quality preference pairs with tight compute budget.

## Disagreement / Adaptation

DPO is a strong baseline, but I did not treat it as default-best under Week 11 constraints.

- Disagreement: in this setting, “start with vanilla DPO” was less attractive than ORPO due to tooling simplicity and run-time constraints.
- Adaptation: ORPO with LoRA on a small backbone and strict data quality filtering.
- Why: our bottleneck was data quality and benchmark fidelity, not algorithmic exploration budget.

## Evidence From My Project

- Training method: `ORPO` (`training/training_run.log`)
- Training pairs used: `605`
- Final held-out gains:
  - Delta A: `+0.3785`
  - Delta B: `+0.1033`

## Practical Outcome

The ORPO choice produced a strong result while keeping implementation and compute overhead low, which is consistent with the Week 11 cost and reproducibility constraints.
