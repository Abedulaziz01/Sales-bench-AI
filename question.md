# My Day 1 Question

## The gap
I cannot defensibly explain how my reported per-task cost and latency are produced at inference time (prefill vs decode, KV cache reuse, and token-level billing effects).

## The question
How should I decompose one held-out judge-scoring call into prefill tokens, decode tokens, and cache reuse so that I can explain why `cost_per_task` is `$0.0029` vs `$0.0047` and why latency appears flat in my ablations? I specifically do not understand what is recomputed each call versus what KV/prefix cache can reuse across repeated rubric prompts on similar tasks.

## Connection to my work
This directly affects:
- `training/model_card.md` (Evaluation Results -> Cost Pareto section),
- `ablations/ablation_results.json` (`cost_pareto` block),
- `docs/blog_post.md` (The Honest Result -> cost-quality tradeoff paragraph).
In those sections I report cost and latency outcomes without a mechanism-level inference explanation.

## What closing it would change
I would revise `ablations/cost_pareto.json` and related model card/blog text to include a token-mechanics breakdown (prefill, decode, cache-hit assumptions) so the cost and latency claims are technically defensible.

## Why this generalizes beyond my project
This same gap appears in many FDE workflows that repeatedly score model outputs against a fixed rubric (sales QA, support QA, compliance QA). If we cannot separate prefill, decode, and cache effects, we cannot make trustworthy cost-latency recommendations in production.
