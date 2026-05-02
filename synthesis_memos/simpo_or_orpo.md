# Synthesis Memo — SimPO vs ORPO for Tenacious Path B

## Comparison Setup

This comparison focuses on what matters for this project:

- small preference dataset
- low training budget
- simple reproducibility and deployment
- stable integration with LoRA and existing tooling

## Head-to-Head Comparison

### SimPO

- Pros: strong empirical reports in low-cost preference settings; avoids some reference-model overhead patterns.
- Cons (for this project): additional implementation branching and validation overhead in our current pipeline timing window.

### ORPO

- Pros: straightforward integration in our existing stack; clear training objective for pairwise ranking; stable end-to-end wiring in the current repo.
- Cons: not automatically superior in all domains; still sensitive to pair quality and judge calibration.

## Pick and Why

I picked ORPO for this run.

- The decisive reason was end-to-end reliability under time and budget constraints, not theoretical preference for one paper.
- Our strongest measured gains came from dataset/judge quality and contamination discipline; ORPO was sufficient to convert that signal into held-out lift.

## Evidence

- Training log shows ORPO run with seed 42 and complete hyperparameter trace.
- Held-out outcomes were strong:
  - Delta A: `+0.3785` (p-value `0.0`)
  - Delta B: `+0.1033`
- Cost increase was measurable but controlled (`$0.0029` → `$0.0047`).

## Practical Note

If we had another iteration cycle, a controlled SimPO-vs-ORPO A/B run on the same pairs would be a good next experiment. For Week 11 delivery, ORPO was the higher-confidence choice.
