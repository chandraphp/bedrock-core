from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List


class PromptError(Exception):
    """Raised when a prompt operation fails."""


@dataclass
class PromptVersion:
    """One version of a prompt template.

    Templates use {variable} syntax. Variables are validated at render time.
    """
    version: str                          # e.g. "1.0", "1.1", "2.0"
    template: str                         # "Summarise {context}. Question: {question}"
    description: str = ""
    recommended_models: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    # Optional: a list of (input_dict, expected_output_substring) pairs
    # used by the built-in eval harness when it lands in v0.5
    eval_cases: List[Dict[str, Any]] = field(default_factory=list)

    def variables(self) -> List[str]:
        """Return the variable names expected by this template."""
        return re.findall(r"\{(\w+)\}", self.template)

    def render(self, **kwargs: Any) -> str:
        """Render the template with the provided variables.

        Raises PromptError if required variables are missing.
        """
        missing = set(self.variables()) - set(kwargs)
        if missing:
            raise PromptError(
                f"Prompt template '{self.version}' is missing variables: {missing}. "
                f"Expected: {self.variables()}"
            )
        return self.template.format(**kwargs)


@dataclass
class PromptEntry:
    """A named prompt with one or more versions."""
    name: str
    description: str = ""
    _versions: Dict[str, PromptVersion] = field(default_factory=dict, repr=False)

    def add_version(self, version: PromptVersion) -> "PromptEntry":
        self._versions[version.version] = version
        return self

    def get(self, version: str = "latest") -> PromptVersion:
        if not self._versions:
            raise PromptError(f"Prompt '{self.name}' has no versions registered.")
        if version == "latest":
            return sorted(self._versions.values(), key=lambda v: v.version)[-1]
        if version not in self._versions:
            available = list(self._versions)
            raise PromptError(
                f"Prompt '{self.name}' has no version '{version}'. "
                f"Available: {available}"
            )
        return self._versions[version]

    def versions(self) -> List[str]:
        return sorted(self._versions)


class PromptRegistry:
    """Registry for versioned, parameterised prompt templates.

    Resolves GAP-003: prompts are no longer inline strings. They are named,
    versioned assets with variable validation, metadata, and optional eval cases.

    Usage:

        registry = PromptRegistry()

        registry.register(
            "sre.rca",
            PromptVersion(
                version="1.0",
                template=(
                    "You are an SRE assistant.\\n"
                    "Recent errors:\\n{context}\\n\\n"
                    "Question: {question}"
                ),
                description="Root cause analysis over Splunk events",
                recommended_models=["claude-sonnet-4-6", "gpt-4o"],
                tags=["sre", "rca"],
            )
        )

        prompt = registry.render("sre.rca", context=events, question=user_q)
        result = agent.ask(prompt)
    """

    def __init__(self) -> None:
        self._entries: Dict[str, PromptEntry] = {}

    def register(
        self,
        name: str,
        version: PromptVersion,
        description: str = "",
    ) -> "PromptRegistry":
        """Register a versioned prompt. Multiple versions can be registered
        for the same name; the latest (by version string sort) is the default."""
        if name not in self._entries:
            self._entries[name] = PromptEntry(name=name, description=description)
        self._entries[name].add_version(version)
        return self

    def get(self, name: str, version: str = "latest") -> PromptVersion:
        if name not in self._entries:
            available = list(self._entries)
            raise PromptError(
                f"No prompt named '{name}' in registry. "
                f"Registered prompts: {available}"
            )
        return self._entries[name].get(version)

    def render(self, name: str, version: str = "latest", **kwargs: Any) -> str:
        """Get prompt by name (and optional version) and render it."""
        return self.get(name, version).render(**kwargs)

    def list_prompts(self) -> Dict[str, List[str]]:
        """Return {name: [versions]} for all registered prompts."""
        return {name: entry.versions() for name, entry in self._entries.items()}
