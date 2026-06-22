from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import Any, Dict, Tuple

from ..adapter import Adapter


class OllamaProvider(Adapter):
    """Local/on-prem provider for any model served by Ollama.

    No API key. No cloud. Requires Ollama running locally (or on a remote host).

    Install Ollama:  https://ollama.com
    Pull a model:    ollama pull llama3.2
                     ollama pull mistral
                     ollama pull deepseek-r1
                     ollama pull qwen2.5:9b    # Chandu's existing local model

    Usage:
        from bedrock_core import App
        from bedrock_core.providers.ollama import OllamaProvider

        app = App()
        agent = app.agent(provider=OllamaProvider(model="llama3.2"))
        result = agent.ask("Explain Kubernetes in one sentence.")

    Multi-model:
        agent_llama  = app.agent(provider=OllamaProvider(model="llama3.2"))
        agent_qwen   = app.agent(provider=OllamaProvider(model="qwen2.5:9b"))
        agent_ds     = app.agent(provider=OllamaProvider(model="deepseek-r1"))
    """

    name = "ollama"

    def __init__(
        self,
        model: str = "llama3.2",
        host: str = "http://localhost:11434",
        timeout: int = 120,
    ):
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def complete(self, prompt: str, **kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                k: v for k, v in kwargs.items()
                if k in {"temperature", "top_p", "top_k", "num_predict", "stop"}
            },
        }).encode()

        req = urllib.request.Request(
            url=f"{self.host}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read())
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"OllamaProvider: could not reach Ollama at {self.host}. "
                f"Is Ollama running? Start it with: ollama serve\n"
                f"Original error: {exc}"
            ) from exc

        text = body.get("response", "")
        usage = {
            "prompt_tokens":     body.get("prompt_eval_count", 0),
            "completion_tokens": body.get("eval_count", 0),
        }
        return text, usage

    def estimate_cost(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "usd":  0.0,
            "note": f"local model ({self.model} via Ollama at {self.host}) — no cost incurred",
        }

    def list_models(self) -> list[str]:
        """Return names of models currently available in this Ollama instance."""
        req = urllib.request.Request(url=f"{self.host}/api/tags", method="GET")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = json.loads(resp.read())
            return [m["name"] for m in body.get("models", [])]
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"OllamaProvider: could not reach Ollama at {self.host}.\n"
                f"Original error: {exc}"
            ) from exc
