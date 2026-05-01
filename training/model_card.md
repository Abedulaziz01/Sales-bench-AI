# Tenacious Judge Adapter Model Card

## Backbone

This adapter was trained on top of `unsloth/Qwen2.5-0.5B-Instruct` using LoRA. The release artifact is the adapter only, not a merged full model. Consumers must load it against the matching base checkpoint and respect the upstream base-model license and usage terms.

## Training Data

The adapter was trained on Tenacious-specific Path B preference pairs stored in `training/preference_pairs.jsonl`. The training set contains 605 preference pairs and the validation split contains 67 pairs. Each pair uses the same prompt with a `chosen` response that passes the Tenacious style-guide evaluator and a `rejected` response derived from Week 10 trace failures or equivalent failure patterns. The supervision signal is centered on grounded claims, honest capacity language, professional tone, non-condescending framing, and one-clear-ask outreach behavior.

## Hyperparameters

- Backbone: `unsloth/Qwen2.5-0.5B-Instruct`
- Training method: `ORPO`
- LoRA rank: `16`
- LoRA alpha: `32`
- Learning rate: `5e-05`
- Batch size: `2`
- Gradient accumulation steps: `4`
- Num epochs: `2`
- Max sequence length: `2048`
- Seed: `42`
- Total wall time: `4.45` minutes
- Training pairs used: `605`
- Validation pairs used: `67`
- Final train loss: `2.2945`
- Final validation loss: `0.9481`

## Intended Use

This adapter is intended to act as a small Tenacious-specific judge or critic for B2B outreach drafts. The target use case is reranking, rejection-sampling, rollback, or human-escalation decisions inside a sales-outreach workflow where Tenacious tone rules and signal-grounding constraints matter. It is suitable for offline evaluation experiments and lightweight production gating on outreach drafts that follow the Tenacious task schema.

## Limitations

This model is not a general-purpose reward model for arbitrary writing tasks. It is tuned to Tenacious-style sales outreach and inherits the limits of the synthetic-plus-trace-derived benchmark used to train it. It may underperform on channels or scenarios not represented well in the current dataset, including richer multi-turn negotiation, phone-call behavior, or unseen market segments. It should not be used to invent pricing, promise unsupported staffing capacity, or replace human review for high-value commitments.

## Evaluation Results

Evaluation results below match `ablations/ablation_results.json` exactly.

- Delta A: trained judge vs Week 10 baseline on Tenacious-Bench held-out
  - Score baseline: `0.4848`
  - Score trained: `0.8633`
  - Delta: `+0.3785`
  - 95% CI: `[0.3487, 0.4084]`
  - p-value: `0.0`
  - n_tasks: `67`
- Delta B: trained judge vs prompt-engineered version on the same backbone
  - Score prompt-only: `0.76`
  - Score trained: `0.8633`
  - Delta: `+0.1033`
  - 95% CI: `[0.0746, 0.1325]`
  - p-value: `0.0`
  - n_tasks: `67`
- Cost Pareto
  - Cost per task baseline: `$0.0029`
  - Cost per task with judge: `$0.0047`
  - Latency p50 baseline: `0.0008s`
  - Latency p50 with judge: `0.0008s`
  - n_tasks: `67`

## Environmental Cost

The logged training run completed in `4.45` minutes on a GPU-backed Colab workflow. This was a single LoRA adapter run rather than a full-model fine-tune, which materially reduced compute and storage cost. The released artifact is adapter-only to avoid duplicating the backbone and to keep storage, transfer, and inference setup lighter than a merged checkpoint release.

## License

This adapter release is published as an adapter artifact for research and evaluation use in the Tenacious-Bench workflow. The adapter distribution should be accompanied by `CC-BY-4.0` documentation for the benchmark artifacts, while actual model use must also comply with the upstream license and acceptable-use terms of `unsloth/Qwen2.5-0.5B-Instruct`.
