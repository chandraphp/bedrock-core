import pytest

from bedrock_core import App


def test_hello_world_smoke():
    """pip install -> App() -> agent.agent() -> agent.ask('Hello') — the frozen milestone."""
    app = App()
    agent = app.agent()  # defaults to provider="mock", no API key required

    result = agent.ask("Hello")

    assert isinstance(result.output, str) and result.output
    assert "elapsed_ms" in result.metrics()
    assert "tokens" in result.metrics()
    assert len(result.trace()) == 2
    assert result.trace()[0]["step"] == "chat.request"
    assert "usd" in result.cost()


def test_operational_data_is_on_the_result_not_the_agent():
    """Verifies the design decision: metrics/trace/cost belong to the execution."""
    app = App()
    agent = app.agent()

    result = agent.ask("Summarize today's incidents")

    assert hasattr(result, "metrics")
    assert hasattr(result, "trace")
    assert hasattr(result, "cost")
    assert not hasattr(agent, "metrics")


def test_unknown_provider_raises_value_error():
    app = App()
    with pytest.raises(ValueError):
        app.agent(provider="not-a-real-provider")


def test_anthropic_provider_without_api_key_raises_clear_error(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = App()
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        app.agent(provider="anthropic")
