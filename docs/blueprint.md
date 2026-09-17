# Catman Agent UI Framework — Blueprint

## Product decision

Build a provider-agnostic framework, not a provider-specific Catman frontend. Catman is the first domain package and reference implementation. Any agent runtime that can emit structured events and typed artifacts can integrate through an adapter.

## Ideal result

The user asks a simple question. The system discovers the right sources, validates grain and period, chooses the domain/common/room skills, executes calculations with tools, creates a typed artifact, explains limitations and offers the next action.

The WOW effect is twofold:

- **Visual WOW:** a calm, simple surface with one clear conclusion and one useful visual.
- **Competence WOW:** the agent visibly knows where data lives, how sources relate, which method to apply and what checks are required.

## Product loop

```text
Question → data discovery → validation → skill execution → artifact → decision → action → receipt
```

## Main concepts

| Concept | Meaning |
|---|---|
| Runtime | Backend agent/orchestrator that executes work |
| Adapter | Translates native runtime events into framework events |
| Room | Persistent business context and capabilities |
| Skill | Reusable procedure for a type of work |
| Tool | Data source or external operation |
| Artifact | Typed, persistent work result |
| Component | Safe UI renderer for an artifact type |
| Action | Next user/agent step |
| Receipt | Record of what the system did |

## UI composition

```text
Rooms / business contexts
        ↓
Pinned actions / suggested capabilities
        ↓
Chat / task control plane
        ↓
Progress trace / visible work receipt
        ↓
Artifact Canvas / durable result
        ↓
Decision, scenario or approved action
```

Rooms are visible to users. Skills remain an internal execution layer. The UI should expose outcomes such as “Разобрать промо” or “Собрать CDT”, not a technical list of skill names.

## First artifact family

- insight brief;
- time series;
- waterfall;
- assortment matrix;
- CDT map;
- diagnostic tree;
- what-if scenario comparison;
- decision matrix;
- retailer story;
- watchlist;
- action checklist.

## Trust contract

Every artifact carries sources, period, filters, data quality, skills and versions, assumptions, limitations, confidence, actions and run identifier. Every meaningful operation creates a receipt. Non-idempotent operations require approval.

## Storage decision

GitHub is the source of truth for framework code, contracts, skills, fixtures, evaluators and documentation. Runtime artifacts and raw business data belong in an Artifact Store and the source data platform; sensitive POS/master data must not be committed to GitHub.

## Implementation phases

1. Contract spike: events, schemas, mock adapter, mock store.
2. Reference UI: Rooms, chat, progress trace, artifact canvas and provenance drawer.
3. Runtime adapters: at least two distinct runtimes using the same UI.
4. Catman domain package: Promo and Assortment rooms with core skills.
5. Proactive workflows: watchlists and alerts with approval controls.

## Acceptance principle

A second runtime must be able to produce the same artifact in the same UI without changing the renderer or domain logic.
