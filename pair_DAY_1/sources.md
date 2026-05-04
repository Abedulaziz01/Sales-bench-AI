# Sources

## 1) Canonical mechanism source: KV cache / prefix caching in practical LLM serving
- vLLM Documentation - Automatic Prefix Caching  
  https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html

Why this source is load-bearing:
- It explains what prefix caching is, when shared prompt prefixes can be reused, and why reuse depends on exact token-prefix matching. This is directly required to explain what gets recomputed vs reused in repeated judge calls.

## 2) Canonical mechanism source: prefill vs decode performance split
- Hugging Face Text Generation Inference (TGI) conceptual/performance docs  
  https://huggingface.co/docs/text-generation-inference

Why this source is load-bearing:
- It describes inference serving behavior and the practical difference between prompt processing and token generation phases, which maps to prefill/decode decomposition used in the cost explanation.

## Optional supporting context (not load-bearing)
- OpenAI API docs for token usage fields and accounting patterns  
  https://platform.openai.com/docs

