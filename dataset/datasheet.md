# Datasheet for Dataset: Tenacious-Bench v0.1

## 1. Motivation

Tenacious-Bench v0.1 exists because generic agent benchmarks do not evaluate the kind of failure that matters in Tenacious-style B2B outreach. A retail or general assistant benchmark may reward surface fluency and task completion even when an outreach draft fabricates a hiring signal, over-commits engineering capacity, misreads a layoff as growth, ignores thread history, or drifts out of brand voice. For a sales workflow, those are not cosmetic issues. They are trust and reputation failures.

This dataset was created to measure those failures directly. It is meant to support evaluation, judge-model training, and benchmark publication work around a narrow domain: Tenacious-style cold outreach, warm reply handling, re-engagement, and related context-brief tasks grounded in public signals and explicit policy constraints.

## 2. Composition

Each instance is a structured task containing prospect context, signal information, bench constraints, metadata, and a scoreable candidate output. The current dataset mix is:

- 72 trace-derived tasks
- 216 programmatic sweep tasks
- 60 accepted multi-LLM synthesis tasks
- 30 hand-authored adversarial tasks
- 336 tasks in the deduplicated combined pool
- 168 train tasks
- 101 dev tasks
- 67 held-out tasks

Counts by dominant failure dimension in the current pool:

| Failure dimension | Count |
|---|---:|
| Signal grounding | 84 |
| Bench over-commitment | 72 |
| Tone drift / professionalism | 54 |
| Stale-signal handling | 42 |
| Prior-thread continuity | 24 |
| AI-maturity or segment misframing | 30 |
| Pricing-scope routing | 30 |

The dataset uses four authoring modes:

- trace-derived
- programmatic sweep
- multi-LLM synthesis
- hand-authored adversarial

Each task includes fields such as `task_id`, `probe_id`, `signal_type`, `signal_confidence`, prospect profile data, `hiring_signal_brief`, `bench_summary`, and a structured `candidate_output`.

## 3. Collection Process

The dataset was assembled from project-local materials and controlled synthetic authoring rather than from a raw historical communications archive. Inputs included Week 10 traces and probe patterns, the Tenacious Style Guide v2, and structured templates for public signals like funding, layoffs, job-post velocity, leadership change, and AI-maturity framing.

The collection process deliberately combined four authoring modes because each contributes something different:

- trace-derived tasks preserve fidelity to real prior failures
- programmatic sweeps increase coverage across structured slot dimensions
- multi-LLM synthesis adds harder or more varied task phrasing
- hand-authored adversarial tasks target edge cases that automated generation tends to miss

Narrative example by mode:

- Trace-derived: a real unsupported-capacity failure from Week 10 is turned into a machine-scoreable honesty task.
- Programmatic: a low-confidence hiring-signal template is expanded across company size, bench state, and signal type.
- Multi-LLM synthesis: a hard seed is routed through one family for authoring and another for lower-cost variation, then passed through a judge filter.
- Adversarial: a prior-thread task is written specifically so that a generic first-touch template will fail.

Human input was involved in the audit, task-shaping decisions, adversarial writing, and rubric design. The current committed inter-rater slice covers 30 tasks labeled twice, more than 24 hours apart.

## 4. Preprocessing / Cleaning / Labeling

All tasks are normalized into a common JSONL structure before entering the combined pool. Synthetic tasks go through a judge filter with three dimensions:

- coherence
- ground-truth verifiability
- rubric clarity

Acceptance thresholds are:

- coherence >= 3/5
- ground-truth verifiability >= 4/5
- rubric clarity >= 3/5

After authoring, the combined pool is deduplicated with a normalized composite key over probe ID, company identity, subject, and body. The reduced pool is then partitioned into train, dev, and held-out sets.

The inter-rater agreement slice consists of exactly 30 tasks labeled on all five rubric dimensions:

- direct
- grounded
- honest
- professional
- non-condescending

Round 2 was created more than 24 hours after Round 1. The agreement matrix is committed in `dataset/inter_rater_agreement.md` and summarized in `audit/methodology.md`.

## 5. Uses

The dataset is intended for:

- evaluating domain-specific outreach agents
- constructing judge-training preference data
- stress-testing brand and policy adherence
- measuring contamination-safe held-out performance

It is not intended for:

- unsupervised production emailing
- pricing or contract automation without human oversight
- broad claims about all B2B sales communication

The benchmark is especially appropriate when the question is not "can the model write a fluent email?" but "can the model stay honest, grounded, and on-brand under ambiguous business pressure?"

## 6. Distribution

The expected public release target is HuggingFace Hub, with the held-out split remaining sealed until a public evaluation policy is finalized. In this repo, `dataset/held_out/` is gitignored so the benchmark can support honest local experimentation without leaking the sealed slice into public training workflows.

The planned license is `CC-BY-4.0`. That choice fits the benchmark’s intended use as a reusable public evaluation artifact where attribution matters because the dataset design, not just the raw task count, is part of the contribution.

## 7. Maintenance

The dataset should be maintained through the same generation and validation pipeline that produced v0.1. New tasks should not be hand-dropped into partitions without:

1. writing or updating the generation source
2. rerunning judge filtering where relevant
3. rerunning deduplication
4. repartitioning train/dev/held-out
5. rerunning contamination checks
6. updating the datasheet and data card counts

Concrete maintenance plan:

- version the dataset as `v0.x` while rubric and agreement procedures are still stabilizing
- keep the held-out set sealed from public training workflows
- revisit failure-dimension counts whenever new tasks are added
- extend the inter-rater slice when rubric dimensions change
- update the methodology and contamination report after any structural pipeline change
