# Thread: Closing a real FDE gap in my Week 11 eval claims

1/10  
I found a weak spot in my Week 11 writeup: I reported cost/task and latency, but could not defend *why* those numbers happened at inference time.

2/10  
My key question became:  
How do I decompose a judge-scoring call into prefill vs decode vs cache reuse so my `cost_pareto` claims are technically defensible?

3/10  
Important distinction: my setup is mixed.  
Training is self-hosted (Unsloth + LoRA), but held-out ablation scoring is API-served (Claude call path).

4/10  
That changes what I can claim.  
In API-served inference, I can measure usage/latency from provider outputs, but I cannot directly observe internal KV cache hits.

5/10  
Still, the mechanism model matters:  
- Prefill = processing input prompt tokens  
- Decode = generating output tokens  
Cost and latency behavior come from their balance.

6/10  
From my ablation file:  
- baseline cost/task = `$0.0029`  
- with judge cost/task = `$0.0047`  
- delta/task = `+$0.0018`  
So quality lift came with real extra token workload.

7/10  
With `67` held-out tasks, that is about `67 * 0.0018 = $0.1206` extra total.  
This is the exact kind of number I should tie to inference mechanics, not just report raw.

8/10  
Why can latency p50 stay near-flat while cost rises?  
Network overhead, short consistent decode lengths, and possible prefix-reuse effects can mask compute changes in end-to-end timing.

9/10  
What I changed: I now frame cost claims as API-contract accounting unless I run self-hosted profiling.  
If I want real cache-hit evidence, I need a vLLM/self-hosted measurement run.

10/10  
FDE takeaway: always separate *what you measured* from *what you inferred*.  
Mechanism-first reporting (prefill/decode/cache + observability limits) makes deployment recommendations credible.

