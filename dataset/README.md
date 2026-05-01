---
license: cc-by-4.0
pretty_name: Tenacious-Bench v0.1
task_categories:
  - text-generation
  - text-classification
language:
  - en
tags:
  - sales
  - llm-evaluation
  - synthetic-data
  - b2b
configs:
  - config_name: default
    data_files:
      - split: train
        path: train.jsonl
      - split: dev
        path: dev.jsonl
      - split: held_out
        path: held_out.jsonl
---

# Tenacious-Bench v0.1

Tenacious-Bench v0.1 is a small, contamination-checked benchmark for Tenacious-style B2B sales outreach. It measures whether an agent can ground outreach in public hiring signals, stay within truthful capacity and pricing boundaries, preserve the Tenacious tone markers, and avoid brand-damaging failure modes that generic retail-style agent benchmarks do not measure.

## What is in the dataset

- `train` split: task authoring and training-pair construction
- `dev` split: rubric calibration and rapid iteration
- `held_out` split: sealed evaluation slice for final ablations

The benchmark combines four authoring modes:

- trace-derived tasks from Week 10 conversion-engine behavior
- programmatic parameter sweeps across company size, signal type, and capacity state
- multi-LLM synthesis with cross-family judge filtering
- hand-authored adversarial tasks targeting the hardest Tenacious-specific failures

## Why this benchmark exists

Public benchmarks such as retail task-completion suites can tell you whether an agent completes a generic flow, but they do not tell you whether a B2B outreach system:

- names the actual hiring signal rather than generic growth language
- refuses unsupported staffing commitments
- avoids banned prospect-facing language like `bench`, `world-class`, or `quick chat`
- uses conditional phrasing on weak signals
- preserves a professional, non-condescending founder/CTO tone

This benchmark was built to measure exactly those behaviors.

## Week 10 baseline

The Week 10 agent baseline on the Tenacious-Bench held-out slice scored:

- baseline score: `0.4848`
- trained judge score: `0.8633`
- Delta A improvement: `+0.3785`
- 95% CI: `[0.3487, 0.4084]`

These values match the ablation report used in Phase 4.

## Datasheet and documentation

The full dataset documentation ships with this repo:

- `datasheet.md`
- `data_card.md`
- `contamination_check.json`
- `inter_rater_agreement.md`

The datasheet covers motivation, composition, collection, preprocessing, uses, distribution, and maintenance, with telescopic, periscopic, and microscopic detail.

## Quickstart

The quickest way to load the dataset is:

```python
from datasets import load_dataset

ds = load_dataset("abdulaziz0111/tenacious-bench-v0.1")
print(ds)
print(ds["train"][0]["task_id"])
```

You can also score a committed example from this repo in under ten minutes:

```bash
python audit/scoring_evaluator.py
```

## License

This dataset is intended to be published under `CC-BY-4.0`.
