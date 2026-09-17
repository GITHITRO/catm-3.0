# Skills

A skill is a reusable, versioned procedure between tools and runtime. It is not the entire product feature.

## Families

### Common

- `data-profiler`;
- `data-visualizer`;
- `evidence-checker`;
- `scenario-builder`;
- `report-composer`.

### Domain

- `promo-analysis`;
- `assortment-review`;
- `cdt-builder`;
- `pricing-and-elasticity`;
- `planogram-analysis`;
- `retailer-story`.

### Room

Room skills provide context, KPI defaults, vocabulary, preferred artifacts and orchestration constraints. They should not duplicate domain logic.

## Skill contract

A skill documents purpose, inputs, allowed tools, data checks, steps, outputs, quality gates and human-approval requirements. It should include examples, schemas, evaluators and fixtures.

## Anti-patterns

- Do not let the model invent a skill that is absent from the registry.
- Do not let the LLM make ungrounded numeric calculations.
- Do not hide material limitations.
- Do not expose internal chain-of-thought as UI.
