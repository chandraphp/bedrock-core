"""Tests for OllamaProvider. No Ollama instance required — HTTP is mocked."""

import json
import urllib.error
from unittest.mock import patch, MagicMock

import pytest

from bedrock_core import App
from bedrock_core.providers.ollama import OllamaProvider


def _mock_response(body: dict) -> MagicMock:
    """Fake urllib response that returns JSON."""
    mock = MagicMock()
    mock.read.return_value = json.dumps(body).encode()
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def test_ollama_basic_completion():
    fake_response = {
        "response": "Kubernetes orchestrates containers.",
        "prompt_eval_count": 7,
        "eval_count": 4,
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(fake_response)):
        provider = OllamaProvider(model="llama3.2")
        text, usage = provider.complete("Explain Kubernetes.")

    assert text == "Kubernetes orchestrates containers."
    assert usage["prompt_tokens"] == 7
    assert usage["completion_tokens"] == 4


def test_ollama_cost_is_always_zero():
    provider = OllamaProvider(model="deepseek-r1")
    cost = provider.estimate_cost({"prompt_tokens": 1000, "completion_tokens": 500})
    assert cost["usd"] == 0.0
    assert "local" in cost["note"].lower()


def test_ollama_via_app_agent():
    fake_response = {
        "response": "A thread is lighter than a process.",
        "prompt_eval_count": 5,
        "eval_count": 8,
    }
    with patch("urllib.request.urlopen", return_value=_mock_response(fake_response)):
        app = App()
        agent = app.agent(provider="ollama", model="qwen2.5:9b")
        result = agent.ask("What is a thread?")

    assert "thread" in result.output.lower()
    assert result.cost()["usd"] == 0.0


def test_ollama_connection_error_gives_clear_message():
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("Connection refused"),
    ):
        provider = OllamaProvider(model="llama3.2")
        with pytest.raises(RuntimeError, match="ollama serve"):
            provider.complete("Hello")


def test_ollama_list_models():
    fake_tags = {"models": [{"name": "llama3.2"}, {"name": "qwen2.5:9b"}]}
    with patch("urllib.request.urlopen", return_value=_mock_response(fake_tags)):
        provider = OllamaProvider()
        models = provider.list_models()

    assert "llama3.2" in models
    assert "qwen2.5:9b" in models


def test_ollama_remote_host():
    """Verify a remote on-prem host can be configured."""
    provider = OllamaProvider(model="mistral", host="http://gpu-server-01:11434")
    assert provider.host == "http://gpu-server-01:11434"
    assert provider.model == "mistral"
