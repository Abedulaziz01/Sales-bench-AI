# Community Engagement Record

## Submission Type

GitHub issue on the `tau2-bench` repository describing the Tenacious-specific evaluation gap and linking the public dataset.

## Status

Draft prepared locally. Public submission still needs to be posted manually from a logged-in GitHub account.

## Target Repository

`tau2-bench` issue tracker

## Prepared Date

2026-05-01

## Public URL

`PENDING_PUBLIC_URL`

## Dataset Link

https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1

## Model Link

https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1

## Suggested Issue Title

Tenacious-style B2B outreach gap: signal grounding, capacity honesty, and tone-preserving evaluation

## Suggested Issue Body

Hi maintainers,

I built a small benchmark called Tenacious-Bench v0.1 to measure a gap I could not capture with generic retail-style agent evaluation. The core issue is that a fluent outreach agent can still fail in business-critical ways that broader task-completion suites do not grade:

- it can mention a generic growth pattern without grounding to the supplied public hiring signal
- it can over-commit staffing capacity when the structured capacity state does not support the claim
- it can drift into banned or vendor-cliche language while still looking syntactically correct
- it can frame a competitor-gap message in a condescending way that would be unacceptable in a real founder or CTO inbox

In my Week 10 traces, these were not rare edge cases. `PROBE-003` and `PROBE-005` expanded two recurring failures: unsupported capacity commitments and tone drift under realistic sales prompts. That motivated Tenacious-Bench v0.1, a 200-300 task benchmark built from trace-derived, programmatic, multi-LLM, and adversarial slices with contamination checks and machine-verifiable scoring.

Public dataset:
https://huggingface.co/datasets/abdulaziz0111/tenacious-bench-v0.1

Public adapter:
https://huggingface.co/abdulaziz0111/tenacious-judge-v0.1

Headline held-out result:
- baseline: `0.4848`
- trained judge: `0.8633`
- Delta A: `+0.3785`
- 95% CI: `[0.3487, 0.4084]`

I’m sharing it in case it is useful as a complementary sales-domain slice or as evidence for adding stronger grounded-communication and capacity-honesty checks to future benchmark revisions.

Thanks.

## Confirmation Evidence

After posting the issue, add one of the following here:

- a screenshot of the submitted issue page, or
- the visible response/confirmation text copied from the issue page
