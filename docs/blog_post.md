## The Gap

Week 11 started with a simple but uncomfortable question: how do we know the Week 10 conversion engine actually works for Tenacious, rather than merely looking competent on a generic benchmark? Public agent benchmarks can be useful for broad capability checks, but they miss the exact behaviors that create risk in a B2B sales workflow. Tenacious outreach has to do more than complete a task. It has to ground a message in a public hiring signal, stay within truthful staffing and pricing constraints, preserve a warm-consultative but direct tone, and avoid the kind of brand-damaging language that gets screenshotted on LinkedIn for the wrong reasons.

That gap showed up clearly in our Week 10 evidence. `PROBE-003` expanded cases where the agent over-committed capacity when the underlying bench state was tight or unsupported. `PROBE-005` expanded the tone-drift failure where a message starts warm and ends in canned staffing language. In `TRACE-003`, the system was fluent but still implied capacity it could not support responsibly. In `TRACE-005`, it referenced a real leadership-change signal but slid into formulaic, non-Tenacious phrasing. A generic retail-style benchmark would score these as plausible completions. A real sales team would treat them as operational and brand failures.

That was the core motivation for Tenacious-Bench v0.1: create an evaluation set that measures the exact things a production outreach system must get right for this business, not just whether it produces polished text.

## The Audit Method

The audit started with two sources: the Week 10 trace log and the probe library. The trace log gave us real agent behavior under a realistic workflow. The probe library gave us a way to convert failure observations into explicit benchmark dimensions. Rather than inventing an evaluation schema from scratch, we let the failures define the measurement surface.

The most important design choice was mechanical scoring. A good benchmark for this setting cannot stop at “sounds on brand.” We needed checks that could be run reproducibly against held-out outputs: does the message reference at least one specific signal from the brief, does it avoid banned phrases, does it keep to one clear ask, does it avoid prospect-facing use of the word `bench`, does it stay within the capacity described in the structured input, and does it preserve a non-condescending framing when using a competitor-gap argument. Those checks became the backbone of the scorer.

The judge design was informed by the LLM-as-a-judge literature, but we stayed conservative. Every generated task passed three filters before entering the benchmark: input coherence at least `3/5`, ground-truth verifiability at least `4/5`, and rubric-application clarity at least `3/5`. Those numbers were chosen because they strike the balance between throughput and confidence for a small-data benchmark: coherence and clarity can tolerate slightly more variation, but verifiability cannot, because the whole point of this benchmark is that claims can be checked against real or structured evidence.

## The Dataset

Tenacious-Bench v0.1 was built from four authoring modes. About a third of the tasks are trace-derived, because real workflow failures are the highest-fidelity evidence we have. Another third come from programmatic sweeps over structured variables like company size, signal type, and capacity state. Roughly a quarter come from multi-LLM synthesis, and the remainder are hand-authored adversarial tasks aimed at the most Tenacious-specific edge cases.

The multi-LLM routing decision mattered more than it first appeared. We used cross-family routing because we wanted diversity in phrasing and failure structure without letting one model family dominate both generation and judging. Frontier-class models were reserved for authoring harder seed cases anchored to the Week 10 failure taxonomy, while cheaper families such as Qwen and DeepSeek were used for bulk variations and filtering. That rotation was not just a cost decision. It was also a leakage-prevention decision. If the same model family both writes and judges the task, the benchmark starts drifting toward model-specific style preferences instead of business-specific quality criteria.

The hand-authored adversarial slice was where the Tenacious guide mattered most. We wrote tasks specifically around the failure patterns a generic benchmark would miss: an urgent signal paired with unsupported capacity, a layoff signal misread as a growth pitch, a near-stale signal at the 85-day boundary that should trigger caution rather than certainty, and prior-thread cases where the system must continue a relationship instead of reintroducing Tenacious from scratch. These are exactly the kinds of things that matter in real B2B outreach and are invisible to broader benchmarks.

To make the dataset publishable rather than just internally useful, we also added contamination checks. We ran n-gram overlap constraints, embedding-similarity checks, and a time-shift rule for public signals. The final training-to-held-out contamination check passed with `0` n-gram violations and `0` embedding violations. That matters because a benchmark only helps if the held-out slice is meaningfully distinct from the training and development artifacts.

## The Training Experiment

Given the Week 10 evidence, Path B was the right intervention. The failure mode was not that the system could never write a decent draft. It was that it could not reliably distinguish a Tenacious-compliant outreach from a superficially plausible failure. That is a preference-learning problem more than a pure supervised-generation problem.

So we converted the training partition into preference pairs. Rejected examples were sourced from Week 10 trace failures and wrapped in the kinds of rule-breaking patterns our evaluator is designed to catch. Chosen examples were corrected rewrites that passed the Tenacious scorer: grounded, honest, professional, non-condescending, and constrained to one clear ask. The final training set contained `605` training pairs and `67` validation pairs.

For the actual run, we trained an ORPO LoRA adapter on top of `unsloth/Qwen2.5-0.5B-Instruct` with rank `16`, alpha `32`, learning rate `5e-05`, batch size `2`, gradient accumulation `4`, and seed `42`. The run completed in `4.45` minutes on a Colab GPU. Training loss fell from the high `4.x` range early in the run to a final logged train loss of `2.2945`, while validation loss ended at `0.9481`. This was exactly the kind of cheap, bounded training run the Week 11 brief intended: the hard part was building the right benchmark and pair data, not burning compute.

## The Honest Result

The trained judge improved held-out performance substantially over the Week 10 baseline. On Delta A, the baseline score was `0.4848` and the trained score was `0.8633`, for an absolute lift of `+0.3785` with a `95%` confidence interval of `[0.3487, 0.4084]`. The paired bootstrap p-value was `0.0`, so the result is statistically significant by the project threshold.

Delta B was also positive. The prompt-only version on the same backbone reached `0.76`, while the trained judge scored `0.8633`, for an additional lift of `+0.1033` with a `95%` confidence interval of `[0.0746, 0.1325]`. This matters because it suggests the improvement is not just prompt polish. The training signal added measurable value beyond careful prompt engineering alone.

The cost-quality tradeoff is real, though not disqualifying. The baseline path was measured at `$0.0029` per task, while the path with the judge was `$0.0047` per task. That increase is not free, so it belongs in the deployment decision. In this case the accuracy lift is large enough that the tradeoff is still favorable, but it is exactly the sort of operational number that needs to stay visible rather than hidden behind benchmark enthusiasm.

One unresolved failure remains. The current benchmark and judge are strong on single-message outbound quality, but they are still relatively weak on longer multi-turn negotiation behavior, especially around pricing scope and partial-capacity routing. The model can now do a much better job deciding whether a draft is Tenacious-compliant, but the benchmark still under-represents back-and-forth sequences where a prospect presses on contract value, timeline, or staffing shape. That is the first thing I would expand in a v0.2.

## What's Next

The next step is not to declare the problem solved. It is to operationalize the judge conservatively. The strongest production role for this model is as a gate: rerank candidate drafts, reject the ones that violate Tenacious constraints, and escalate uncertain cases where the business risk is high. That is especially important for capacity commitments, pricing language, and competitor-gap messaging.

There is also a straightforward path to improving the benchmark itself. v0.2 should add more multi-turn tasks, more prospect-history continuity cases, and more explicit measurement around when the right action is to refuse or defer rather than draft a stronger message. Those are the behaviors that make a system not just persuasive, but safe and trustworthy in a real sales motion.

The broader lesson from this week is that small, domain-specific evaluation work can move the needle more than a bigger training run. We did not need a massive corpus or a costly post-training pipeline to get a meaningful result. We needed a benchmark that measured the right failures, a judge that could recognize them, and enough discipline to keep the held-out slice clean. For Tenacious-style B2B outreach, that turned out to be enough to turn a plausible agent into a measurably more reliable one.
