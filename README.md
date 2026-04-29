# Sales-bench-AI

Tenacious-Bench v0.1 is a domain-specific evaluation scaffold for B2B sales outreach. The project focuses on failure modes that generic agent benchmarks miss: signal grounding, confidence-aware phrasing, honest capacity commitments, tone preservation, channel discipline, and contamination-resistant dataset construction.

This repository currently contains the Act I and Act II foundation for Week 11:

- an audit memo and schema for Tenacious-specific evaluation
- deterministic generation scripts for trace-derived, programmatic, synthesis, adversarial, and partitioned dataset authoring
- a contamination check pipeline and sealed held-out split
- verification scripts that make the dataset scaffold reproducible

## What This Bench Measures

Tenacious-Bench is designed to grade outreach that a real B2B services team would defend publicly. It evaluates whether a draft:

- references a real public signal instead of generic personalization
- respects Tenacious tone markers: direct, grounded, honest, professional, non-condescending
- avoids unsupported bench or pricing commitments
- adapts to signal confidence, AI maturity, prior-thread context, and outreach channel
- survives contamination checks before entering the held-out partition

The style and rubric logic are grounded in the Tenacious Style Guide v2 and encoded in the evaluation schema and authoring pipeline.

## Current Repo Status

Implemented now:

- [audit/audit_memo.md](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/audit_memo.md:1)
- [audit/schema.json](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/schema.json:1)
- [audit/scoring_evaluator.py](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/scoring_evaluator.py:1)
- [audit/methodology.md](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/audit/methodology.md:1)
- [generation_scripts](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/generation_scripts)
- [dataset](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/dataset)
- [tests/verify_audit_phase.py](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/tests/verify_audit_phase.py:1)
- [tests/verify_dataset_authoring.py](C:/Users/user/Desktop/mll/week11/Sales-bench-AI/tests/verify_dataset_authoring.py:1)

Generated dataset counts at the current checkpoint:

| Artifact | Count |
|---|---:|
| Trace-derived tasks | 72 |
| Programmatic sweep tasks | 216 |
| Multi-LLM synthesis tasks accepted | 60 |
| Hand-authored adversarial tasks | 30 |
| Deduplicated combined pool | 336 |
| Train split | 168 |
| Dev split | 101 |
| Held-out split | 67 |

Contamination status:

- n-gram violations: `0`
- embedding violations: `0`
- time-shift verified: `true`

## Repository Layout

```text
audit/
  audit_memo.md
  gap_analysis.md
  methodology.md
  schema.json
  scoring_evaluator.py

dataset/
  trace_derived_tasks.jsonl
  programmatic_tasks.jsonl
  multi_llm_synthesis_raw.jsonl
  multi_llm_synthesis_tasks.jsonl
  adversarial_tasks.jsonl
  adversarial_notes.md
  combined_pool_deduped.jsonl
  contamination_check.json
  train/tasks.jsonl
  dev/tasks.jsonl
  held_out/tasks.jsonl

generation_scripts/
  common.py
  trace_derived.py
  programmatic_sweep.py
  multi_llm_synthesis.py
  judge_filter.py
  dedup.py
  build_adversarial_tasks.py
  partition_dataset.py
  contamination_check.py
  logs/

tests/
  test_openrouter.py
  verify_audit_phase.py
  verify_dataset_authoring.py
```

## Quick Start

Use the project virtual environment and run the verification scripts from the repo root.

```powershell
python tests\verify_audit_phase.py
python tests\verify_dataset_authoring.py
```

If you want to regenerate the dataset-authoring artifacts from source:

```powershell
python generation_scripts\trace_derived.py
python generation_scripts\programmatic_sweep.py
python generation_scripts\multi_llm_synthesis.py
python generation_scripts\judge_filter.py
python generation_scripts\build_adversarial_tasks.py
python generation_scripts\dedup.py
python generation_scripts\partition_dataset.py
python generation_scripts\contamination_check.py
```

For a single yes/no health check:

```powershell
python tests\verify_dataset_authoring.py
```

## Evaluation and Authoring Rules

The current dataset scaffold enforces these rules:

- input coherence must score at least `3/5`
- ground-truth verifiability must score at least `4/5`
- rubric clarity must score at least `3/5`
- the same model family cannot both generate and judge the same task
- held-out data stays sealed under `dataset/held_out/` and is gitignored

## Notes on Publication Safety

- `.env` files are ignored by git
- `dataset/held_out/` is ignored by git to keep the sealed split out of public release flows
- logs are stored under `generation_scripts/logs/` for reproducibility

## Next Milestones

- expand the datasheet into publication-ready form
- convert the train split into Path B preference pairs
- run the first judge-training experiment
- publish the public dataset package and public-facing documentation

This repository is set up to make those next steps reproducible rather than ad hoc.
