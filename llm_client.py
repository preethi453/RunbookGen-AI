"""LLM client for RunbookGen AI.

Default provider: Ollama running locally.
Fallback: deterministic rule-based generator if Ollama is unavailable.
"""

import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
REQUEST_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))


class LLMError(RuntimeError):
    pass


def generate_with_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
            "num_ctx": 4096,
        },
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise LLMError(f"Ollama request failed: {exc}") from exc

    data = response.json()
    answer = data.get("response", "").strip()
    if not answer:
        raise LLMError("Ollama returned an empty response.")
    return answer
