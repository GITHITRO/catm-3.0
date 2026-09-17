# Architecture

## Layers

```text
Application / Catman Product
  Rooms, domain context, skills, permissions

Agent UI Framework
  Protocol, artifact schemas, registry, trust, actions

Runtime Adapter Layer
  LangGraph, OpenAI Agents, Claude, DeepSeek Harness, custom

Data / Tool Layer
  MCP, SQL, REST, files, warehouse and APIs
```

The UI depends only on normalized framework events and typed artifact contracts. Provider-specific logic stays in adapters.

## Reference flow

```text
User input
→ runtime receives task
→ adapter emits task.interpreted
→ runtime discovers and validates sources
→ runtime executes skills/tools
→ adapter emits artifact.created
→ renderer validates and displays artifact
→ user drills down, compares, exports or approves an action
```

## UI

- Left: Rooms and contextual pinned actions.
- Center: Chat and user-visible progress trace.
- Right: Artifact Canvas with versions, provenance and actions.

Progress trace shows useful milestones, not hidden chain-of-thought.

## Boundaries

- No raw sensitive data in the framework repository.
- No arbitrary generated HTML for business-critical views.
- No automatic external state changes without approval.
- No provider-specific assumptions in core packages.

## MVP choices

- TypeScript contracts.
- JSON Schema for interoperability.
- HTTP POST + SSE initially.
- React reference renderer.
- Local filesystem/mock store initially, then object storage + metadata database.
