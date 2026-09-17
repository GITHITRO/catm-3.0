# AGENTS.md

## Catman 3.0

Catman 3.0 is a provider-agnostic Agent UI Framework and Catman reference implementation. It turns agent runtime events into a simple but deeply competent workspace: Rooms, Chat, Progress Trace, typed Artifacts, Provenance and Actions.

## Principles

1. Simple surface, deep execution.
2. Runtime-independent contracts: do not couple UI to a model, provider or harness.
3. Typed artifacts: render registered components; do not render arbitrary business-critical HTML.
4. Trust by design: retain provenance, assumptions, data quality, skill version and receipts.
5. Progressive disclosure: headline first, evidence next, technical trace on demand.
6. Skills are implementation units; users see business outcomes and actions.

## Repository map

- `docs/` — architecture, protocol, artifacts, rooms, skills and roadmap.
- `schemas/` — JSON Schemas for events and artifacts.
- `packages/` — reusable protocol, schema, adapter, store and renderer packages.
- `apps/` — reference applications.
- `skills/` — common, domain and room skills.
- `examples/` — runtime integration examples.
- `evaluators/` — quality checks.

## Workflow

- Branches: `blueprint/*`, `feature/*`, `fix/*`, `docs/*`.
- Commits: Conventional Commits.
- Keep provider-specific code inside adapters.
- Never commit raw or sensitive business data.
- Every new artifact type requires a schema, renderer contract, fixture and evaluator.

## MVP

First end-to-end flow: promo analysis → insight brief + chart + waterfall + what-if comparison + decision matrix.
