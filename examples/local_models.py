"""
Local / on-prem multi-model example.

Requirements:
    1. Ollama installed and running:  ollama serve
    2. At least one model pulled:
         ollama pull llama3.2
         ollama pull qwen2.5:9b      # already on Chandu's machine
         ollama pull deepseek-r1     # already on Chandu's machine
         ollama pull mistral

Run:
    python3 examples/local_models.py
"""

from bedrock_core import App
from bedrock_core.providers.ollama import OllamaProvider

app = App()

# ── Single model ────────────────────────────────────────────────────────────
agent = app.agent(provider=OllamaProvider(model="llama3.2"))
result = agent.ask("Explain Kubernetes in one sentence.")

print("=== llama3.2 ===")
print("Response:", result.output)
print("Metrics: ", result.metrics())
print("Cost:    ", result.cost())   # always 0.0 for local models
print()

# ── Multiple models, same App ────────────────────────────────────────────────
# Each agent is independent — swap models freely without changing anything else.
models = {
    "qwen2.5:9b":    app.agent(provider=OllamaProvider(model="qwen2.5:9b")),
    "deepseek-r1":   app.agent(provider=OllamaProvider(model="deepseek-r1")),
}

prompt = "What is the difference between a process and a thread?"

for model_name, model_agent in models.items():
    result = model_agent.ask(prompt)
    print(f"=== {model_name} ===")
    print("Response:", result.output[:200], "...")
    print("Tokens:  ", result.metrics()["tokens"])
    print()

# ── Remote on-prem host ──────────────────────────────────────────────────────
# Point at any Ollama instance on your network — an internal GPU server, etc.
# remote_agent = app.agent(
#     provider=OllamaProvider(model="llama3.2", host="http://gpu-server-01:11434")
# )

# ── List what's available on the local Ollama instance ──────────────────────
local = OllamaProvider()
try:
    print("Models available locally:", local.list_models())
except RuntimeError as e:
    print("Ollama not running:", e)
