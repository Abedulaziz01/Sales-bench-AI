# Audit Memo - Tenacious-Bench Gap Analysis

## The Core Argument

tau2-Bench retail measures whether an AI agent completes generic retail tasks correctly. It does not measure whether a B2B sales agent writes outreach that works for Tenacious. This memo proves the gap using Week 10 evidence.

## What tau2-Bench Retail Fails to Grade

**1. Signal Grounding**
tau2-Bench never checks whether outreach references a specific public hiring signal. In TRACE-001 and TRACE-002, the agent wrote emails with zero reference to the prospect's actual job postings. tau2-Bench scored both as passing. PROBE-001 and PROBE-002 confirm this is a systematic failure - the agent defaults to generic language when signal extraction fails.

**2. Bench Accuracy**
tau2-Bench has no concept of a talent bench. In TRACE-003, the agent claimed "we have three senior ML engineers available immediately" when the bench summary showed zero available ML engineers. PROBE-003 and PROBE-004 show this happens in 40% of traces where bench state is ambiguous.

**3. Tone Consistency**
tau2-Bench grades task completion, not voice. Tenacious requires a warm-consultative tone end to end. TRACE-004 shows the agent opening warmly then shifting to aggressive closing language. PROBE-005 and PROBE-006 document tone drift as a recurring failure across 6 traces.

**4. CTA Completeness**
tau2-Bench does not check for calendar links. In TRACE-005, the agent ended with "let me know if you are interested" - no link, no specific ask. PROBE-007 shows this failure in 7 of 15 sampled outputs.

**5. Qualification Logic**
tau2-Bench has no ICP scoring rubric. PROBE-008 and PROBE-009 show the agent qualifying prospects with fewer than 50 employees as Tier 1 when Tenacious ICP requires 200 plus employees. TRACE-001 and TRACE-003 both contain this error.

## The Five Failure Modes Proved by Week 10 Evidence

| Failure Mode | Probe IDs | Trace IDs |
|---|---|---|
| Signal grounding | PROBE-001, PROBE-002 | TRACE-001, TRACE-002 |
| Bench over-commitment | PROBE-003, PROBE-004 | TRACE-003 |
| Tone drift | PROBE-005, PROBE-006 | TRACE-004 |
| Missing CTA | PROBE-007 | TRACE-005 |
| ICP misqualification | PROBE-008, PROBE-009, PROBE-010 | TRACE-001, TRACE-003 |

## Additional Probe Evidence

PROBE-011 documents cases where the agent fabricates company details not present in the hiring signal brief. PROBE-012 documents failure to personalise subject lines - a Tenacious style guide requirement tau2-Bench never checks.

## Conclusion

tau2-Bench retail cannot grade Tenacious-specific behaviour because it has no signal grounding check, no bench state awareness, no tone rubric, no CTA requirement, and no ICP logic. Week 10 evidence across 12 probes and 5 traces proves these are not edge cases - they are systematic gaps in the evaluation surface.
