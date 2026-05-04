# Asker Signoff

## Question
How do I defensibly explain my reported cost and latency numbers using prefill/decode/KV-cache mechanics?

## Did the explainer close the gap?
Yes - fully closed.

## What became clear
- I can now separate per-call inference into prefill and decode phases.
- I understand what prefix caching can reuse and what still must be recomputed.
- I can explain why cost increased while p50 latency remained near-flat.
- I have specific edits to make in `ablations/cost_pareto.json`, `training/model_card.md`, and `docs/blog_post.md`.

## Remaining confusion
- None blocking. Next depth area is speculative decoding, but that is intentionally out-of-scope for this question.

## Asker name/date
- Abdulaziz
- 2026-05-04

