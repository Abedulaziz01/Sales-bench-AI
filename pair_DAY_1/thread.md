# Thread: Why `CI low = 0.00` and `p = 0.0316` can both be true (small-n bootstrap)

1/10  
I hit a reporting trap in a paired bootstrap result:  
`ci_low = 0.00` and `p = 0.0316` at the same time.  
Looked inconsistent. It isn’t.

2/10  
Setup: `n=12`, binary outcomes (0/1), paired resampling.  
This is exactly the regime where bootstrap distributions are coarse/discrete.

3/10  
Key mechanism: with 12 binary pairs, resampled means move in jumps of `1/12`.  
So bootstrap differences also live on a coarse grid, not a smooth continuum.

4/10  
Because of that grid, many resamples land exactly at `diff = 0.00`.  
That creates a visible probability mass at zero.

5/10  
Then the percentile CI lower edge (2.5th percentile) can land exactly on 0.00.  
So `ci_low = 0.00` can happen even if most resamples are positive.

6/10  
The one-sided p-value asks a different question:  
"How often is lift non-positive?"  
If that fraction is small (here ~3.16%), then `p < 0.05`.

7/10  
So both can be true:  
- CI lower edge touches zero  
- p-value still supports positive directional lift

8/10  
At small n, don’t reduce interpretation to "CI includes zero => no signal."  
That shortcut can fail in quantized bootstrap settings.

9/10  
Better FDE reporting:  
Lead with directional p-value + include CI + explicitly name small-n discreteness.  
That is honest and technically defensible.

10/10  
My update rule now: separate mechanism from slogan.  
If the distribution is quantized, say so.  
It improves memo quality and avoids false contradictions in executive readouts.

