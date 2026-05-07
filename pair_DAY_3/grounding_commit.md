# Day 3 Grounding Commit

## Purpose
Record what I changed (or will immediately change) in real project artifacts after closing the SimPO-vs-DPO gradient gap.

## Gap addressed
I previously justified SimPO mostly by intuition (“no reference model + better on small data”) without parameter-level gradient explanation.

## Grounded updates

1. `training/model_card.md`
- Add mechanism-level rationale:
  - DPO update magnitude is gated by policy-minus-reference margin.
  - SimPO update magnitude is gated by policy margin directly (reference-free).
- Replace vague wording (“works better on small data”) with defensible optimization-language.

2. `training/train.py` / training logs
- Add/track:
  - mean winner-loser log-prob gap (`delta_theta`)
  - fraction of pairs with positive margin
  - gradient norm trends for LoRA blocks
- Use these to detect whether preference signal is actually being learned.

3. `ablations/ablation_results.json` interpretation notes
- Add explicit note that held-out lift is interpreted together with training-dynamics diagnostics to reduce reward-overoptimization risk.

## Why this improves project quality
- Converts an intuition-only training choice into a mechanism-defensible choice.
- Makes my model card and training rationale auditable under senior technical review.
- Aligns evaluation claims with observable optimization behavior.

## Asker
- Name: Abdulaziz
- Date: 2026-05-07

