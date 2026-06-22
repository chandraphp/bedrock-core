"""
Quick Start.

Run with:
    python3 examples/hello_world.py

Uses the built-in mock provider — no API key, no network access required.
Swap provider="mock" for provider="anthropic" (with ANTHROPIC_API_KEY set and
`pip install "bedrock-core[anthropic]"`) to hit a real model.
"""

from bedrock_core import App

app = App()
agent = app.agent()  # provider="mock" by default

result = agent.ask("Explain Kubernetes in one sentence.")

print("Response:", result.output)
print("Metrics: ", result.metrics())
print("Trace:   ", result.trace())
print("Cost:    ", result.cost())
