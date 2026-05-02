# Synthesis Memo — Gu et al. (2025) LLM-as-a-Judge Survey

## Core Takeaway

Gu et al. emphasize judge reliability, calibration, and bias controls. I followed that guidance by splitting high-volume filtering from high-cost evaluation and by enforcing model-family rotation between generation and judging.

## Applied Design Choice

I used a two-tier judge strategy:

- dev-tier judge for bulk filtering during authoring
- eval-tier judge reserved for sealed-slice evaluation passes

I also kept mechanical checks (banned phrases, one-ask rule, signal grounding constraints) alongside model-judged dimensions to reduce subjective drift.

## Disagreement / Adaptation

Gu et al. often favor richer semantic judge signals, but I intentionally used stricter rule-heavy gating in early pipeline stages.

- Disagreement: purely semantic judge-first scoring is too brittle for this domain at low budget.
- Adaptation: hard preflight constraints plus judge dimensions (coherence, verifiability, rubric clarity).
- Why: Tenacious has non-negotiable policy failures (`bench` phrasing externally, unsupported commitments) that should fail deterministically.

## Evidence From My Project

- Judge thresholds used:
  - coherence `>=3/5`
  - verifiability `>=4/5`
  - rubric clarity `>=3/5`
- Path B leakage policy separated rewrite-family and judge-family.
- Held-out Delta A improved significantly (`+0.3785`, p-value `0.0`), indicating the judge setup provided useful ranking signal.

## Practical Outcome

The adaptation produced a robust, low-cost judge pipeline that is easier to audit than a purely semantic black-box judge, while still preserving enough nuance for useful model ranking.
