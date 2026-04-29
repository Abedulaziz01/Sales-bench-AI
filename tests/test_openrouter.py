"""Test OpenRouter API connection with a cheap model."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

session = requests.Session()
session.trust_env = False

try:
    response = session.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openrouter/free",
            "messages": [{"role": "user", "content": "Say hello in one word."}],
            "max_tokens": 10,
        },
        timeout=30,
    )
except requests.RequestException as exc:
    raise SystemExit(f"OpenRouter request failed: {exc}") from exc

if response.status_code == 200:
    result = response.json()
    model_used = result["model"]
    reply = result["choices"][0]["message"]["content"]
    print(f"OpenRouter works! Model: {model_used} | Reply: {reply}")
else:
    print(f"OpenRouter error {response.status_code}: {response.text}")
