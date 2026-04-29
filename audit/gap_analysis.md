# Gap Analysis - tau2-Bench Retail vs Tenacious-Bench

## Section 1 - What tau2-Bench Measures

tau2-Bench retail evaluates AI agents on generic task completion in retail scenarios. It measures:

- Whether the agent retrieves the correct product information
- Whether the agent completes a multi-step purchase flow
- Whether the agent handles returns and refunds correctly

**Example 1:** tau2-Bench checks if an agent finds a product by SKU. It does not check if the agent references why that product is relevant to this specific customer.

**Example 2:** tau2-Bench checks if a refund is processed. It does not check if the agent's tone matches a brand voice guideline.

## Section 2 - What tau2-Bench Misses

tau2-Bench has no grading surface for any of the following Tenacious-specific behaviours:

**Example 1 - Signal Grounding (PROBE-001, TRACE-001):**
The agent in TRACE-001 wrote an outreach email that contained zero reference to the prospect's actual hiring signal (3 open ML engineer roles posted on LinkedIn). tau2-Bench scored this as a pass because the email was grammatically correct and contained a greeting and a sign-off.

**Example 2 - Bench State Accuracy (PROBE-003, TRACE-003):**
In TRACE-003 the agent claimed bench availability that did not exist. tau2-Bench has no bench concept and cannot detect this. The output passed tau2-Bench scoring while containing a factual lie about Tenacious's actual supply.

## Section 3 - Evidence from Week 10

Week 10 traces and probes prove the gap is systematic, not anecdotal.

**Example 1 - Tone Drift (PROBE-005, PROBE-006, TRACE-004):**
TRACE-004 shows the agent opening with warm-consultative language then closing with "We should connect ASAP to discuss next steps" - aggressive language that violates the Tenacious style guide. tau2-Bench has no tone rubric and scored this output as passing.

**Example 2 - ICP Misqualification (PROBE-008, PROBE-009, TRACE-001, TRACE-003):**
In both TRACE-001 and TRACE-003 the agent scored a 38-employee startup as Tier 1 ICP. Tenacious ICP requires a minimum of 200 employees for Tier 1. tau2-Bench has no ICP logic and graded both outputs as correct.
