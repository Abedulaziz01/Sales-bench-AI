# Grounding Commit

## Artifact Updated

Week 11 Tenacious-Bench evaluator / agent evaluation writeup

## Commit / Pull Request / File Link
https://github.com/bethel4/-Sales-Evaluation-Bench-and-Aligning-the-Conversion-Engine/pull/1
`scoring_evaluator.py`  
`ablation_results.json`  
`model_card.md`

## What Changed

I updated the evaluation and selection pathway to include an explicit decoding-strategy layer instead of treating scalar judge scores as self-executing decisions. The new version separates and names three inference-time coupling behaviors (`rejection_sampling`, `best_of_n`, `reranker`), logs their control parameters, and records strategy metadata in ablation outputs.

## Why It Changed

The Delta A claim was not fully reproducible because the coupling mechanism between judge score and generator action was implicit. This change makes the mechanism explicit, testable, and auditable, so collaborators can reproduce held-out results with the same strategy and cost/latency assumptions instead of inheriting silent library defaults.
