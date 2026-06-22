from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

from ..adapter import Adapter


class OpenAIProvider(Adapter):
    """Real provider adapter for OpenAI models.

    Exists primarily as evidence: if the Adapter interface designed against
    Anthropic's API also fits OpenAI's (different SDK, different response
    shape, different usage field names) without changes to Adapter itself,
    that's a real signal the interface generalizes — not an assumption.

    Requires: pip install "bedrock-core[openai]" and an OPENAI_API_KEY.
    """

    name = "openai"

    # USD per token, placeholder rates — replace with a real, maintained price table.
    _RATE_INPUT_PER_TOKEN = 2.5 / 1_000_000
    _RATE_OUTPUT_PER_TOKEN = 10.0 / 1_000_000

    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OpenAIProvider requires an OPENAI_API_KEY environment variable "
                "or an explicit api_key argument."
            )
        try:
            import openai  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "OpenAIProvider requires the 'openai' package. "
                "Install with: pip install \"bedrock-core[openai]\""
            ) from exc

    def complete(self, prompt: str, **kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        import openai

        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1000),
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content or ""
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
        }
        return text, usage

    def estimate_cost(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        usd = (
            usage.get("prompt_tokens", 0) * self._RATE_INPUT_PER_TOKEN
            + usage.get("completion_tokens", 0) * self._RATE_OUTPUT_PER_TOKEN
        )
        return {"usd": round(usd, 6), "note": "estimated from placeholder rates, not billed"}
