# Methodology - Tenacious-Bench v0.1

## Path Declaration

**Selected Path: B - Preference-Tuned Judge**

## Justification

Week 10 evidence points to inconsistency failures, not generation-quality failures. In TRACE-003, the agent produced a well-written email that contained a false bench claim. In TRACE-004, the agent opened correctly then drifted in tone by the third paragraph. These are not cases where the agent cannot write - they are cases where the agent cannot tell when it is wrong.

A Path B judge trained on (chosen, rejected) preference pairs directly addresses this. The judge learns to detect the difference between a grounded outreach and a hallucinated one, between a tone-consistent email and a drifted one. Deployed as a rejection-sampling layer in front of the Week 10 generator, it catches failures before they reach the prospect.

Path A (SFT) would improve average output quality but would not solve the inconsistency problem - the agent would still occasionally produce bad outputs and have no mechanism to detect them. Path C (PRM) is appropriate for trajectory failures, but Week 10 evidence shows the failures are at the output level, not the step level.

## Partitioning Protocol

| Partition | Share | Purpose |
|---|---|---|
| Training | 50% | Preference pairs for judge training |
| Dev | 30% | Iteration and rubric calibration |
| Held-out | 20% | Sealed. Used only for final evaluation |

Contamination checks applied before sealing held-out:
1. N-gram overlap check - less than 8-gram overlap between held-out and training
2. Embedding similarity check - cosine similarity below 0.85
3. Time-shift check - all public signals from documented date windows

## Contamination Prevention

The held-out partition will be kept separate from training workflows and excluded from public training runs. Before public release, the full held-out content should be gitignored or otherwise sealed so only task IDs and contamination metadata are published until the leaderboard is live.

## Judge Filter Rules

Every generated task is scored on three dimensions before entering the dataset:

1. Input coherence must be at least 3/5
2. Ground-truth verifiability must be at least 4/5
3. Rubric-application clarity must be at least 3/5

Tasks that fail any threshold are rejected from the accepted pool.

### Rotation Policy

The same model family is never used to generate and judge the same task. In the local scaffold, synthesis tasks carry a `model_family` tag and the judge filter is run under a different `judge_family`. This mirrors the preference-leakage prevention rule from the Week 11 brief and keeps the methodology aligned with the published process.

## Inter-Rater Agreement

A 30-task subset was labeled twice more than 24 hours apart. Exact agreement by rubric dimension is:

| Dimension | Agreement |
|---|---:|
| direct_score | 86.7% |
| grounded_score | 83.3% |
| honest_score | 90.0% |
| professional_score | 86.7% |
| non_condescending_score | 93.3% |

All five dimensions are above the 80% threshold, so no rubric revision was required before proceeding to the next stage.
