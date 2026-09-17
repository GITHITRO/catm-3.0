# Rooms

Rooms are persistent business contexts, not folders. Each room defines relevant sources, glossary, default filters, skills, artifact types, pinned actions and permissions.

## Example

```json
{
  "id": "assortment",
  "title": "Ассортимент",
  "context": {
    "sources": ["sales", "assortment", "distribution", "product_attributes"],
    "default_period": "last_13_weeks",
    "glossary": ["SKU", "CDT", "substitution"]
  },
  "skills": ["assortment-review", "cdt-builder", "scenario-builder"],
  "pinned_actions": ["build_cdt", "find_delisting_risk", "simulate_assortment"],
  "artifact_types": ["cdt_map", "assortment_matrix", "scenario_comparison"]
}
```

## Initial rooms

- Overview;
- Assortment;
- Promo;
- Pricing;
- Planogram.

Users see rooms and business actions. The agent selects the underlying skills automatically.

## Governance

Rooms are scoped to workspace permissions. Room context is versioned. Archived rooms are read-only snapshots. Room-created artifacts retain room provenance.
