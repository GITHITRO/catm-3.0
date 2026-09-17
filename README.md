# Catman 3.0 — Agent UI Framework

Provider-agnostic framework for turning any agent runtime into a visually simple, deeply competent workspace with Rooms, Chat, typed Artifacts, provenance and controlled Actions.

## Core idea

```text
Any Agent Runtime → normalized events → Catman UI Framework → Rooms + Chat + Artifacts
```

The runtime may be LangGraph, OpenAI Agents, Claude, DeepSeek Harness or a custom orchestrator. The UI depends on contracts, not on the provider.

## Repository

- `docs/blueprint.md` — product and architecture blueprint.
- `docs/architecture.md` — framework layers and boundaries.
- `docs/protocol.md` — normalized event protocol.
- `docs/artifact-model.md` — typed artifact model.
- `docs/rooms.md` — contextual workspaces.
- `docs/skills.md` — common, domain and room skills.
- `docs/roadmap.md` — implementation milestones.
- `schemas/` — machine-readable contracts.

## Experience

A user asks a business question. The agent finds the right data, validates it, selects the appropriate skill, executes calculations through tools and returns a concise insight plus a beautiful, inspectable artifact.

## Status

Blueprint branch. Contract spike and reference UI are next.
