# Day 2 - My Questions
## Topic: Agent and Tool-Use Internals

1. In an agent loop, what is the minimal internal state machine (plan -> tool-select -> execute -> observe -> revise) I should implement so tool calls are reliable and debuggable under production failures?

2. How should I enforce argument correctness before execution (schema validation, enum checks, ID existence checks) so hallucinated tool inputs fail fast and do not corrupt downstream steps?

3. What is the right retry policy per failure type (timeout, rate-limit, malformed response, partial success), and how do I keep retries idempotent when tools mutate external systems?

4. How do I separate planner quality from executor quality in logs so I can attribute errors correctly to reasoning mistakes vs tool-interface mistakes vs external API/runtime failures?

5. For multi-tool workflows, how should I design fallback and escalation logic (alternate tool, degraded mode, human handoff) so the agent stays useful without hiding uncertainty or fabricating completion?

