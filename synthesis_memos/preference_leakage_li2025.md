# Synthesis Memo — Preference Leakage (Li et al., 2025)

## Core Takeaway

Li et al. show that preference pipelines can leak style and hidden bias when generation and judgment share model-family artifacts. I treated leakage control as a first-class design requirement for Path B.

## Leakage-Prevention Section

### Mapping Li et al. Leakage Patterns to My Pipeline

1. Same-family generate-and-judge contamination
- Risk in paper: judge rewards familiar generation signatures.
- My policy: separate family tags for chosen rewrites vs judge filtering.

2. Evaluation contamination by iterative tuning on sealed slice
- Risk in paper: silent overfitting to held-out feedback loops.
- My policy: held-out separated and contamination-checked; dev iteration done before sealed evaluation.

3. Preference-pair style shortcut learning
- Risk in paper: model learns superficial lexical cues.
- My policy: rejected pairs were trace-seeded but checked against rubric constraints and contamination checks.

## Confirmed Rotation Policy

- Rejected samples: from `week10/trace_log.jsonl` failures (no rewrite model needed).
- Chosen rewrites: model family A (`deepseek` in our logs/policy docs).
- Judge filter: model family B (`qwen`).
- Eval-tier spot-checking reserved for final passes.
- No same-model generate-and-judge pairs were allowed.

## Evidence

- `training/leakage_prevention_log.md`
- contamination check reports with held-out violations at zero
- final held-out evaluation separation preserved

## Practical Outcome

Leakage controls were not just theoretical hygiene: they supported credible held-out estimates and reduced the risk that gains were model-family artifacts rather than real Tenacious-policy alignment.
