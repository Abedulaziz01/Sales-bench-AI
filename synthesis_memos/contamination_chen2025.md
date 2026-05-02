# Synthesis Memo — Chen et al. (2025) Contamination-Resistant Evaluation

## Core Takeaway

Chen et al. argue that static splits are not enough and contamination checks must be explicit, repeatable, and tied to realistic leakage pathways. I used that framing as the default design for Tenacious-Bench partitioning.

## Applied Rule

I applied a three-check protocol before sealing held-out:

1. n-gram overlap screening
2. embedding similarity thresholding
3. time-shift verification for public-signal references

## Disagreement / Adaptation

I modified the contamination surface for Path B training: pair-level contamination should be evaluated using training-pair source fingerprints, not only raw generated text.

- Applied as-is: held-out must be separated and checked against train/dev.
- Modified: for preference pairs, raw text overlap over-counted harmless boilerplate, so we used task-fingerprint comparisons for the decisive check.
- Why: preference pairs contain shared format language by design; strict raw-text overlap produced false alarms without indicating true split leakage.

## Evidence From My Project

- Training contamination check final report:
  - held-out n-gram violations: `0`
  - held-out embedding violations: `0`
- Dataset contamination report final:
  - n-gram violations: `0`
  - embedding violations: `0`
  - timeshift verified: `true`

## Practical Outcome

The modified pair-aware contamination check preserved Chen et al.’s core objective (credible held-out integrity) while reducing noisy false positives for Path B preference data.
