# Explainer: Why `ci_low = 0.00` and `p = 0.0316` can both be correct at `n=12`

## 1) The exact gap being closed
In a paired bootstrap with 12 binary outcomes, Eyoel observed:
- 95% CI lower bound: `0.00`
- one-sided p-value: `0.0316`

This looked contradictory during reporting. The gap is: *how to explain this without hand-waving* in an FDE memo.

---

## 2) Short answer
They are not contradictory.

- The percentile CI asks: "Where do the middle 95% of bootstrap differences fall?"
- The one-sided p-value asks: "How often is the bootstrap difference non-positive?"

At very small `n` with binary outcomes, bootstrap differences are discrete (quantized). That can place noticeable probability mass exactly at `0.00`, so CI can touch zero while the non-positive mass is still small enough to yield `p < 0.05`.

---

## 3) Mechanism in plain language (load-bearing concept)

With `n=12` and binary outcomes, each bootstrap sample mean is restricted to increments of `1/12`.  
So the paired difference distribution also takes values on a coarse grid.

That coarse grid creates two effects:

1. **Mass at exactly zero**  
Many resamples produce equal trained and baseline success counts, so `diff = 0.00` appears often.

2. **Percentile edge behavior**  
If enough mass sits at zero, the 2.5th percentile can land exactly at `0.00` even when most resamples are positive.

So `ci_low = 0.00` here is often a *discreteness artifact*, not proof of no effect.

---

## 4) Hands-on demonstration (runnable and verifiable)

Run this from repo root:

```python
import numpy as np

def paired_bootstrap(a, b, n_resamples=10000, seed=42):
    rng = np.random.default_rng(seed)
    a, b = np.array(a), np.array(b)
    diffs = []
    for _ in range(n_resamples):
        idx = rng.integers(0, len(a), size=len(a))
        diffs.append(a[idx].mean() - b[idx].mean())
    diffs = np.array(diffs)
    return {
        "ci_low": float(np.percentile(diffs, 2.5)),
        "ci_high": float(np.percentile(diffs, 97.5)),
        "p_value": float((diffs <= 0).mean()),
        "mass_at_zero": float((diffs == 0).mean()),
    }

# Example close to observed regime (n=12 binary pairs)
a12 = np.array([1,1,1,1,1,0,0,0,0,0,0,0])  # 5/12
b12 = np.array([1,1,0,0,0,0,0,0,0,0,0,0])  # 2/12

out = paired_bootstrap(a12, b12, n_resamples=10000, seed=42)
print(out)
```

Expected style of output:

```text
{
  'ci_low': 0.0,
  'ci_high': 0.5,
  'p_value': 0.0316,
  'mass_at_zero': <non-trivial positive value>
}
```

Why this demo is enough:
- It directly shows zero-mass in the bootstrap distribution.
- It reproduces the "CI touches 0 but p<0.05" pattern.
- It is minimal and can be re-run by anyone reviewing the artifact.

---

## 5) What to write in an executive memo

Recommended wording:

> The trained system showed positive directional lift in 96.84% of paired bootstrap resamples (`p = 0.0316`, one-sided).  
> The 95% percentile CI is `[0.00, ...]`; at `n=12` with binary outcomes, this lower bound touching zero is expected from bootstrap discreteness and should not be interpreted alone as "no effect."

What *not* to write:

> "The result is not significant because CI includes zero."

At this sample size and outcome type, that sentence is often misleading.

---

## 6) Scope discipline (what is intentionally out-of-scope)

This explainer focuses only on:
- paired bootstrap discreteness at small `n`
- percentile CI interpretation
- one-sided p-value interpretation

Out-of-scope (not needed to close this gap):
- BCa interval derivation details
- Bayesian alternatives
- sequential testing corrections

---

## 7) Why this closes the original question

Eyoel can now:
- defend both reported numbers without contradiction,
- explain the mechanism in plain language,
- report direction + uncertainty honestly in FDE-facing artifacts.

