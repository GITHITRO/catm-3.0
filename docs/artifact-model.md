# Artifact Model

## Common envelope

```json
{
  "id": "artifact_123",
  "type": "scenario_comparison",
  "version": 1,
  "title": "Baseline vs option B",
  "status": "ready",
  "data": {},
  "schema": {},
  "provenance": {},
  "quality": {
    "confidence": "medium",
    "assumptions": [],
    "limitations": []
  },
  "actions": []
}
```

## Rules

Artifacts are typed, validated, persistent, versioned, reproducible and actionable. The renderer is selected by `type` from a registry. The agent supplies data; the UI owns safe presentation.

## Initial types

`insight_brief`, `kpi_card`, `time_series`, `waterfall`, `assortment_matrix`, `cdt_map`, `diagnostic_tree`, `scenario_comparison`, `decision_matrix`, `retailer_story`, `watchlist`, `action_checklist`.

## Quality

Use human-readable confidence (`high`, `medium`, `low`) with assumptions and limitations. Never present a numeric result without its baseline, calculation context and data provenance.

## What-if

LLM parses the scenario and explains it. A validated calculation engine produces the numeric output. Each scenario stores baseline, changed parameters, formula/model reference, sensitivity and uncertainty.
