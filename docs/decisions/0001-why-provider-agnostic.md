# ADR 0001: Provider-agnostic framework

## Context

Catman needs an AI-first interface but must not be locked to one LLM provider or harness.

## Decision

Core packages expose normalized events, typed artifacts, renderer contracts, adapter APIs and trust/action metadata. Provider-specific code belongs in adapters and examples.

## Consequences

- Initial adapter work costs more.
- UI and domain logic remain portable.
- Multiple runtimes can be evaluated against the same artifact contract.
