# Synthesis Memo — Prometheus 2 (Kim et al., 2024)

## Core Takeaway

Prometheus 2 shows that a compact evaluator can be useful when trained with clear preference structure and consistent rubric framing. I adopted that spirit for Tenacious by treating the judge as a focused specialist, not a general evaluator.

## Adaptation Section

What I adopted:

- rubric-centric judge behavior
- preference-pair training objective for ranking better vs worse outputs
- emphasis on evaluation reliability over broad generation capability

What I changed for sales-domain deployment:

- added deterministic preflight checks before judge scoring (banned phrases, one ask, no external `bench` usage, pricing scope constraints)
- explicitly encoded confidence-aware signal language expectations
- emphasized refusal and escalation behavior for unsupported commitments

Why I changed it:

- Tenacious failures are often policy violations that should fail deterministically.
- A pure semantic judge can still pass polished but unsafe messages in this workflow.

## Evidence From My Project

- Judge filter thresholds and rotation policy were documented and enforced.
- Week 10 failure traces (`TRACE-003`, `TRACE-005`) directly informed deterministic checks.
- Held-out gain (`+0.3785`) suggests the adapted specialist-judge approach was effective for this domain.

## Practical Outcome

The Prometheus-style specialist framing transferred well, but only after adding hard business-rule constraints specific to sales outreach risk.
