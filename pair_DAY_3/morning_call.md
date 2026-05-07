# Day 3 Morning Call

## Participants
- Abdulaziz
- Pair partner

## Date
- 2026-05-07

## Duration
- ~25 minutes

## Goal
Finalize Day 3 question on post-training mechanics (SimPO vs DPO gradient behavior on small preference datasets).

## What we discussed
- We synced on the chosen topic: LoRA, DPO/SimPO, and reward overoptimization risk.
- I shared my draft question and why it matters for my Week 11 artifacts.
- We sharpened the question from intuition-level wording to mechanism-level wording:
  - from “SimPO works better on small data”
  - to “what gradient term changes, and why that changes movement toward preference signal.”

## Question refinement outcomes
- Added explicit artifact grounding:
  - `training/model_card.md`
  - SimPO training script (`training/train.py` path context)
- Added explicit unresolved mechanism:
  - parameter-level penalty/gating difference between DPO and SimPO.
- Added explicit closure criteria:
  - derive both gradients,
  - explain why reference-free term changes effective update mass on 104 pairs.

## Morning call result
- Final Day 3 question agreed and locked.
- Ready for explainer exchange in evening session.

