# Leakage Prevention Log

## Rotation Policy

- Rejected samples: sourced from `week10/trace_log.jsonl` (historical real agent outputs, no rewrite model used during pair construction)
- Rejected pair text is trace-seeded: the core negative content comes from historical Week 10 failures and is wrapped in additional Tenacious-guide violations so the pair remains a clear rejected example.
- Chosen rewrites: generated under simulated Model Family A = `deepseek` (`deepseek_v3`)
- Judge filter on chosen rewrites: simulated Model Family B = `qwen` (`qwen3-next-80b-a3b`)
- Eval-tier spot-check reserved for Days 5-6 only: `claude-sonnet-4.6`

The chosen rewriter family and judge family are intentionally different to prevent preference leakage.

## Construction Summary

- Pair count: 672
- Mean chosen score (7-point scale): 6.18
- Mean rejected score (7-point scale): 2.25

## Rejected Sample Source

Rejected outputs come directly from Week 10 trace failures such as:

- missing calendar link
- formulaic phrasing
- weak grounding
- tone drift
- over commitment
- bad qualification

## Tenacious Style Guide Alignment

Chosen rewrites are constrained to:

- one clear ask
- confidence-aware phrasing on weak signals
- no banned Tenacious phrases
- no prospect-facing use of the word `bench`
- honest capacity and pricing scope
- professional, non-condescending language
