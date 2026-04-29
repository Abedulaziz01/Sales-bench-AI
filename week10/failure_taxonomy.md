# Tenacious Failure Taxonomy v1.0

Derived from 50 Week 10 Conversion Engine traces. Each failure class maps directly to a Tenacious-Bench schema dimension.

---

## FC-01 — Tone & Voice Failures

**Description:** The agent produces output that deviates from Tenacious's warm, consultative, signal-grounded voice.

**Schema Dimension:** `tone_score`  
**Scoring Method:** LLM-judge 1–5 on five Tenacious tone markers + banned_phrase_count == 0

**Sub-types:**

- `FC-01a` **Generic opener** — Probe IDs: PROBE-001 | Frequency: 12% | Example: `TRACE-003`
- `FC-01b` **Corporate close** — Probe IDs: PROBE-010 | Frequency: 8% | Example: `TRACE-002`
- `FC-01c` **Banned phrase usage** — Probe IDs: PROBE-005 | Frequency: 10% | Example: `TRACE-009`
- `FC-01d` **Segment tone mismatch** — Probe IDs: PROBE-007 | Frequency: 6% | Example: `TRACE-006`

---

## FC-02 — Signal Grounding Failures

**Description:** The agent retrieves a public signal but fails to anchor the outreach in that specific signal.

**Schema Dimension:** `grounding_score`  
**Scoring Method:** signal_referenced == True AND signal_text_overlap_with_draft > 0.3

**Sub-types:**

- `FC-02a` **Signal retrieved, not used** — Probe IDs: PROBE-002 | Frequency: 14% | Example: `TRACE-007`
- `FC-02b` **Wrong signal interpretation** — Probe IDs: PROBE-009 | Frequency: 8% | Example: `TRACE-013`
- `FC-02c` **Stale signal treated as fresh** — Probe IDs: PROBE-012 | Frequency: 6% | Example: `TRACE-008`

---

## FC-03 — Bench Commitment Failures

**Description:** The agent misrepresents bench availability in outreach — over-promising or under-communicating capacity.

**Schema Dimension:** `bench_accuracy_score`  
**Scoring Method:** bench_state_in_draft matches bench_state in bench_check step

**Sub-types:**

- `FC-03a` **Over-committed bench promised as available** — Probe IDs: PROBE-003 | Frequency: 8% | Example: `TRACE-012`
- `FC-03b` **Partial bench stated as full** — Probe IDs: PROBE-011 | Frequency: 6% | Example: `TRACE-025`

---

## FC-04 — Qualification Logic Failures

**Description:** The agent qualifies or disqualifies a prospect incorrectly based on ICP criteria.

**Schema Dimension:** `qualification_accuracy`  
**Scoring Method:** qualification_score vs ground_truth_icp_fit derived from company metadata

**Sub-types:**

- `FC-04a` **Low-maturity prospect over-qualified** — Probe IDs: PROBE-004 | Frequency: 8% | Example: `TRACE-016`
- `FC-04b` **Stale signal inflates confidence** — Probe IDs: PROBE-012 | Frequency: 6% | Example: `TRACE-028`

---

## FC-05 — CTA / Structural Failures

**Description:** The agent produces an email that lacks a clear call-to-action or closes without a calendar link.

**Schema Dimension:** `cta_present`  
**Scoring Method:** calendar_link_present == True (regex check for calendly or cal.com link)

**Sub-types:**

- `FC-05a` **Missing calendar link** — Probe IDs: PROBE-006 | Frequency: 10% | Example: `TRACE-005`

---

## FC-06 — Trajectory Compounding Failures

**Description:** Each individual step scores above threshold but cumulative decisions produce a low-quality final output.

**Schema Dimension:** `trajectory_coherence`  
**Scoring Method:** mean(step_scores) - overall_output_score > 0.25 signals compounding failure

**Sub-types:**

- `FC-06a` **Locally correct, globally incoherent** — Probe IDs: PROBE-008 | Frequency: 6% | Example: `TRACE-021`

---

## Summary Statistics

- **Total Traces Analysed:** 50
- **Failure Rate:** 0.56
- **Top Failure Class:** FC-02 (Signal Grounding)
- **Critical Severity Probes:** 3
- **High Severity Probes:** 6
- **Medium Severity Probes:** 3
