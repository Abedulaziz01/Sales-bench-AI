# Synthesis Memo — Liu et al. (2024) Synthetic Data Best Practices

## Core Takeaway

Liu et al. argue that synthetic-data quality and coverage are more important than raw volume. I agree with that direction and applied it directly in Tenacious-Bench: we prioritized difficult, diagnosis-rich tasks over generic volume expansion.

## Applied Design Choice

I followed Liu et al. on mixed authoring modes, but weighted trace-derived and adversarial slices higher than a generic synthesis-heavy mix. In our build, real Week 10 traces plus hand-authored adversarial cases were the strongest drivers of useful failures, especially for bench over-commitment and tone drift.

## Disagreement / Adaptation

Liu et al. emphasize broad synthetic diversification. I adapted this for Tenacious by deliberately narrowing some synthetic diversity in favor of policy-critical failure density.

- Disagreement: “more diverse synthetic variety” was not always better for our domain.
- Adaptation: I constrained synthetic variants to Tenacious-specific guardrails (signal grounding, no `bench` phrasing externally, one ask, confidence-aware wording).
- Why: unconstrained diversity generated many fluent but low-diagnostic tasks that passed generic checks while missing business-critical failure surfaces.

## Evidence From My Project

- `TRACE-003`: fluent draft with unsupported capacity implication.
- `TRACE-005`: signal mention present but tone drift into non-Tenacious language.
- `PROBE-003`: repeated over-commitment pressure scenarios.
- `PROBE-005`: repeated tone-drift and style-regression scenarios.
- Judge-filter logs showed better downstream signal when we filtered hard on verifiability (`>=4/5`) and rubric clarity (`>=3/5`) rather than maximizing synthetic novelty.

## Practical Outcome

This adaptation improved Phase 4 outcomes on held-out:

- Delta A: `+0.3785` (95% CI `[0.3487, 0.4084]`)
- Delta B: `+0.1033`

The result supports Liu et al.’s quality-first principle, but with a domain adaptation: in Tenacious-style sales evaluation, targeted failure density beats generic diversity once minimum coverage is reached.
