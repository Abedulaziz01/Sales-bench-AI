# Tenacious Probe Library v1.0

Generated from Week 10 Conversion Engine trace analysis.

---

## PROBE-001 — Generic opener on warm signal

**Failure Mode:** `tone_drift`  
**Severity:** high  
**Expansion Variants:** 5  

**Description:** Agent uses 'I hope this email finds you well' despite a fresh, specific hiring signal being available.

**Trigger Condition:** `Any trace where signal_type=job_posting AND banned_phrase_count > 0`

**Evidence Trace IDs:** TRACE-003, TRACE-011, TRACE-027

---

## PROBE-002 — Signal retrieved but not used in draft

**Failure Mode:** `weak_grounding`  
**Severity:** critical  
**Expansion Variants:** 6  

**Description:** Agent correctly retrieves the hiring signal in Step 1 but the outreach email makes no reference to it.

**Trigger Condition:** `signal_found=True AND signal_referenced=False in step 4`

**Evidence Trace IDs:** TRACE-007, TRACE-019, TRACE-033

---

## PROBE-003 — Bench over-committed but email promises immediate availability

**Failure Mode:** `over_commitment`  
**Severity:** critical  
**Expansion Variants:** 4  

**Description:** bench_state=over_committed but outreach email claims engineers are available immediately.

**Trigger Condition:** `bench_state=over_committed AND draft contains 'available immediately' or 'ready now'`

**Evidence Trace IDs:** TRACE-012, TRACE-024

---

## PROBE-004 — Low AI-maturity prospect qualified as high-fit

**Failure Mode:** `bad_qualification`  
**Severity:** medium  
**Expansion Variants:** 4  

**Description:** Prospect with ai_maturity ≤ 1 and no recent tech signal is qualified with score > 0.7.

**Trigger Condition:** `ai_maturity <= 1 AND qualification_score > 0.7`

**Evidence Trace IDs:** TRACE-016, TRACE-038

---

## PROBE-005 — Multiple banned phrases in single outreach

**Failure Mode:** `formulaic_phrasing`  
**Severity:** high  
**Expansion Variants:** 5  

**Description:** Draft contains 3+ banned phrases from the Tenacious style guide banned list.

**Trigger Condition:** `banned_phrase_count >= 3`

**Evidence Trace IDs:** TRACE-009, TRACE-022, TRACE-041

---

## PROBE-006 — No CTA or calendar link in outreach

**Failure Mode:** `missing_calendar_link`  
**Severity:** high  
**Expansion Variants:** 3  

**Description:** Email ends without a calendar link or concrete next-step ask.

**Trigger Condition:** `calendar_link_present=False`

**Evidence Trace IDs:** TRACE-005, TRACE-029, TRACE-044

---

## PROBE-007 — Enterprise tone used on SMB prospect

**Failure Mode:** `wrong_segment_tone`  
**Severity:** medium  
**Expansion Variants:** 4  

**Description:** Formal multi-paragraph structure used for SMB company where a shorter punchy email is appropriate.

**Trigger Condition:** `company_size=smb AND email word count > 200`

**Evidence Trace IDs:** TRACE-006, TRACE-018

---

## PROBE-008 — Each step locally correct but cumulative failure

**Failure Mode:** `trajectory_compound`  
**Severity:** high  
**Expansion Variants:** 6  

**Description:** Signal retrieval correct, qualification correct, bench check correct — but outreach tone mismatches segment and bench state is not reflected in commitment language.

**Trigger Condition:** `all step_correct=True AND overall_score < 0.45`

**Evidence Trace IDs:** TRACE-021, TRACE-035, TRACE-047

---

## PROBE-009 — Layoff signal present but email reads as growth pitch

**Failure Mode:** `weak_grounding`  
**Severity:** high  
**Expansion Variants:** 5  

**Description:** Signal type is layoff (rebuilding after reduction) but outreach email pitches bench capacity as if company is in growth mode.

**Trigger Condition:** `signal_type=layoff AND draft_tone=growth_pitch`

**Evidence Trace IDs:** TRACE-013, TRACE-031

---

## PROBE-010 — Warm open collapses into corporate close

**Failure Mode:** `tone_drift`  
**Severity:** medium  
**Expansion Variants:** 4  

**Description:** Email opens with a signal-grounded, warm opener but closes with corporate boilerplate ('Please let me know if you have any questions').

**Trigger Condition:** `opener_score >= 4 AND closer_score <= 2 on LLM judge`

**Evidence Trace IDs:** TRACE-002, TRACE-017, TRACE-039

---

## PROBE-011 — Partial bench stated as full availability

**Failure Mode:** `over_commitment`  
**Severity:** high  
**Expansion Variants:** 3  

**Description:** bench_state=partial but email claims 'a team ready to go' without qualifying the partial nature of availability.

**Trigger Condition:** `bench_state=partial AND draft contains 'team ready' without caveat`

**Evidence Trace IDs:** TRACE-025, TRACE-042

---

## PROBE-012 — Stale signal treated as fresh

**Failure Mode:** `bad_qualification`  
**Severity:** medium  
**Expansion Variants:** 4  

**Description:** Hiring signal is 90+ days old but agent qualifies with high signal_confidence as if it were recent.

**Trigger Condition:** `signal_age_days > 90 AND signal_confidence > 0.75`

**Evidence Trace IDs:** TRACE-008, TRACE-028, TRACE-046

---

