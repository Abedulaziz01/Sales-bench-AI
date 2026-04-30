# Data Card: Tenacious-Bench v0.1

## Telescopic

Tenacious-Bench v0.1 is a domain-specific benchmark for B2B sales outreach. It measures whether an agent can produce outreach that is signal-grounded, confidence-aware, honest about capacity and pricing, and consistent with Tenacious tone rules. The benchmark is intentionally narrow: it does not aim to represent all sales communication, only the kinds of prospecting and follow-up behaviors that matter for the Tenacious workflow.

## Periscopic

### Breakdown by authoring mode

- Trace-derived: 72
- Programmatic sweep: 216
- Multi-LLM synthesis accepted: 60
- Hand-authored adversarial: 30

### Breakdown by partition

- Train: 168
- Dev: 101
- Held-out: 67

### Breakdown by dominant failure dimension

- Signal grounding: 84
- Bench over-commitment: 72
- Tone drift / professionalism: 54
- Stale-signal handling: 42
- Prior-thread continuity: 24
- AI-maturity misframing: 30
- Pricing-scope routing: 30

### Quality-control layers

- Judge filter with 3 scored dimensions
- Deduplication on normalized composite keys
- N-gram contamination check
- Embedding-style similarity check
- Time-shift verification
- Inter-rater agreement on a 30-task subset

## Microscopic

### Trace-derived tasks

These tasks preserve the structure of real project failures from Week 10 and convert them into machine-scoreable instances. They are strongest for realism and probe fidelity.

### Programmatic sweep tasks

These tasks vary structured dimensions such as company size, bench state, and signal type while holding the target failure mode fixed. They are strongest for controlled coverage.

### Multi-LLM synthesis tasks

These tasks are authored or rewritten through distinct model families, then filtered by a separate judge family. They are strongest for richer phrasing and harder synthetic edges.

### Hand-authored adversarial tasks

These tasks are written manually to defeat baseline shortcuts. They target cases like over-commitment pressure, stale signals, prior-thread continuity, and wrong-segment framing.
