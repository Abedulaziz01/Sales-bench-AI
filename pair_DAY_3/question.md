# Day 3 — Question

## Topic: Training and Post-Training Mechanics (LoRA, DPO/SimPO, Reward Overoptimization)

In my Sales-bench-AI Week 11 pipeline, I trained a small judge adapter with preference optimization and reported held-out lift, but I cannot defend whether that lift reflects true alignment or early reward overoptimization on a narrow preference surface.

**Specifically: how can I diagnose, at parameter-and-metric level, whether my LoRA preference training setup (DPO vs SimPO style) is learning stable winner-vs-loser behavior versus exploiting shortcuts in the judge/rubric, and what concrete controls should I add to my current artifacts (`training/train.py`, `ablations/ablation_results.json`, `training/model_card.md`) to prove I am not overoptimizing the reward signal?**

### Why this is diagnostic for this project

- My benchmark is small and domain-specific, so overoptimization risk is real.
- I report Delta A/Delta B, but these alone do not prove robustness.
- If I cannot separate real alignment from reward hacking, deployment guidance is weak and I cannot defend against a potential attacker.

### What I have tried

1. I have run the same point-biserial correlation on my preference pairs and compared it to the base model's preference correlation. If my judge's preference correlates with response length (|r| > 0.3, p < 0.05), length is a confound in my training signal.
2. I have run my held-out pairs through both my trained adapter AND the base model (before adaptation). Count disagreements.
3. I have run my held-out pairs through both my trained adapter AND the base model (before adaptation).

### What closing this would change

1. Add overoptimization diagnostics (margin trends, calibration drift, disagreement checks) into training logs.
2. Add robustness slices to ablations, not just aggregate held-out score.
3. Add an explicit “reward overoptimization risk” section in `model_card.md` with mitigations and failure triggers.
