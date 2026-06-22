from __future__ import annotations

from typing import Any, Union

from .adapter import Adapter
from .capability import ChatCapability
from .providers.mock import MockProvider
from .runtime import ExecutionResult, Runtime

_BUILTIN_PROVIDERS = {
    "mock": MockProvider,
}


def _resolve_provider(provider: Union[str, Adapter], **kwargs: Any) -> Adapter:
    if isinstance(provider, Adapter):
        return provider

    if provider == "anthropic":
        from .providers.anthropic import AnthropicProvider

        return AnthropicProvider(**kwargs)

    if provider == "openai":
        from .providers.openai import OpenAIProvider

        return OpenAIProvider(**kwargs)

    if provider in _BUILTIN_PROVIDERS:
        return _BUILTIN_PROVIDERS[provider](**kwargs)

    known = list(_BUILTIN_PROVIDERS) + ["anthropic", "openai"]
    raise ValueError(f"Unknown provider '{provider}'. Known providers: {known}")


class Agent:
    """Public-facing sugar API: a Runtime pre-configured with one ChatCapability.

    Internally this is just `Runtime(capabilities=[ChatCapability(adapter)])` —
    the simplification exists so `app.agent()` / `agent.ask(...)` reads naturally,
    while extension authors work against Runtime/Capability/Adapter directly.
    """

    def __init__(self, provider: Union[str, Adapter] = "mock", **provider_kwargs: Any):
        adapter = _resolve_provider(provider, **provider_kwargs)
        self._runtime = Runtime(capabilities=[ChatCapability(adapter)])

    def ask(self, prompt: str, **kwargs: Any) -> ExecutionResult:
        return self._runtime.execute("chat", prompt=prompt, **kwargs)


class App:
    """Entry point. `app = App(); agent = app.agent(); agent.ask("Hello")`."""

    def __init__(self) -> None:
        self._agents: list[Agent] = []

    def agent(self, provider: Union[str, Adapter] = "mock", **provider_kwargs: Any) -> Agent:
        agent = Agent(provider=provider, **provider_kwargs)
        self._agents.append(agent)
        return agent
