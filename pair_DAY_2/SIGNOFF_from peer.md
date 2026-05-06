# Signoff

## Gap Closure Judgment

Closed

## Explanation

The reproducibility gap is closed because the judge-generator coupling mechanism is now explicit in code and artifacts rather than implicit.

- `scoring_evaluator.py` now exposes explicit inference-time strategy selection (`rejection_sampling`, `best_of_n`, `reranker`) through a strategy wrapper and audit helper.
- `ablation_results.json` now includes strategy metadata per run row (`decoding_strategy`, `n_candidates`, `threshold`, `max_tries`) so Delta A conditions are reconstructible.
- `model_card.md` now documents the intended decoding strategy used in evaluation, preventing silent rewiring by downstream users.
