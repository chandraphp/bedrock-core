# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.0.1-alpha | ✅ Current |

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report security issues via
[GitHub private security advisories](https://github.com/chandraphp/bedrock-core/security/advisories/new).

Include:

- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fix (optional)

You will receive a response within 72 hours. We will coordinate disclosure
timing with you before publishing any fix.

## Scope

- Vulnerabilities in `bedrock-core` itself
- Vulnerabilities in the provider adapters that could expose API keys or
  leak sensitive data
- Dependency vulnerabilities (please also check if Dependabot already
  filed an alert)

## Out of scope

- Vulnerabilities in Ollama, Anthropic, or OpenAI's own infrastructure
- Issues requiring physical access to the user's machine
