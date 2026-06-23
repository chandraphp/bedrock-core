from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar("T", bound="BaseConfig")


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""


class BaseConfig:
    """Base for all bedrock-core configuration objects.

    Subclass this in application code to define typed, validated config
    that reads from environment variables with safe defaults.

    Resolution order (highest priority last, i.e. overrides win):
        1. Class-level defaults (dataclass field defaults)
        2. Environment variables
        3. Explicit keyword arguments passed to __init__

    Secret fields (names ending in _key, _secret, _password, _token) are
    never included in __repr__ or logged — they show as '***'.
    """

    _SECRET_SUFFIXES = ("_key", "_secret", "_password", "_token", "_credential")

    def to_dict(self, redact_secrets: bool = True) -> Dict[str, Any]:
        result = {}
        for f in fields(self):  # type: ignore[arg-type]
            value = getattr(self, f.name)
            if redact_secrets and any(f.name.endswith(s) for s in self._SECRET_SUFFIXES):
                result[f.name] = "***"
            else:
                result[f.name] = value
        return result

    def __repr__(self) -> str:
        parts = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({parts})"

    @classmethod
    def validate(cls: Type[T], instance: T) -> T:
        """Override in subclasses to add validation logic.

        Should raise ConfigurationError with a clear message on failure.
        """
        return instance


@dataclass
class LLMConfig(BaseConfig):
    """Standard LLM configuration consumed by App.agent()."""

    provider: str = field(
        default_factory=lambda: os.environ.get("BEDROCK_PROVIDER", "mock")
    )
    model: str = field(
        default_factory=lambda: os.environ.get("BEDROCK_MODEL", "")
    )
    api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("BEDROCK_API_KEY")
    )
    timeout: int = field(
        default_factory=lambda: int(os.environ.get("BEDROCK_TIMEOUT", "30"))
    )

    def __post_init__(self) -> None:
        LLMConfig.validate(self)

    @classmethod
    def validate(cls, instance: "LLMConfig") -> "LLMConfig":
        if instance.timeout <= 0:
            raise ConfigurationError(
                f"BEDROCK_TIMEOUT must be a positive integer, got {instance.timeout}"
            )
        return instance


@dataclass
class ConnectorConfig(BaseConfig):
    """Base configuration for any connector.

    Application connectors (SplunkConfig, JiraConfig, etc.) should subclass
    this and add their own fields — they'll inherit secret-redaction and
    validation hooks automatically.
    """

    mock: bool = field(
        default_factory=lambda: os.environ.get("BEDROCK_MOCK_MODE", "true").lower() == "true"
    )
    timeout: int = field(
        default_factory=lambda: int(os.environ.get("BEDROCK_CONNECTOR_TIMEOUT", "30"))
    )
