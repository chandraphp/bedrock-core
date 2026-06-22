from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

from ..adapter import Adapter


class AnthropicProvider(Adapter):
    """Real provider adapter for Claude models.

    Requires: pip install "bedrock-core[anthropic]"  and an ANTHROPIC_API_KEY.
    Pricing below is a placeholder for cost *estimation* only — it is not billing
    data and should be replaced with a maintained price table before release.
    """

    name = "anthropic"

    # USD per token, placeholder rates — replace with a real, maintained price table.
    _RATE_INPUT_PER_TOKEN = 3.0 / 1_000_000
    _RATE_OUTPUT_PER_TOKEN = 15.0 / 1_000_000

    def __init__(self, model: str = "claude-sonnet-4-6", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "AnthropicProvider requires an ANTHROPIC_API_KEY environment variable "
                "or an explicit api_key argument."
            )
        try:
            import anthropic  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "AnthropicProvider requires the 'anthropic' package. "
                "Install with: pip install \"bedrock-core[anthropic]\""
            ) from exc

    def complete(self, prompt: str, **kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        import anthropic

        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1000),
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )
        usage = {
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
        }
        return text, usage

    def estimate_cost(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        usd = (
            usage.get("prompt_tokens", 0) * self._RATE_INPUT_PER_TOKEN
            + usage.get("completion_tokens", 0) * self._RATE_OUTPUT_PER_TOKEN
        )
        return {"usd": round(usd, 6), "note": "estimated from placeholder rates, not billed"}
