# Protocol

## Envelope

```json
{
  "protocol": "catman-agent-ui",
  "protocol_version": "0.1",
  "run_id": "run_123",
  "event_id": "evt_456",
  "timestamp": "2026-09-17T07:00:00Z",
  "type": "artifact.created",
  "payload": {},
  "provenance": {},
  "permissions": {}
}
```

## Event types

- `run.started`, `run.completed`, `run.failed`;
- `message.delta`;
- `task.interpreted`, `plan.updated`;
- `source.discovered`, `source.validated`;
- `skill.started`, `skill.completed`;
- `artifact.created`, `artifact.updated`, `artifact.versioned`;
- `action.proposed`, `approval.requested`, `action.completed`;
- `receipt.created`, `warning.created`.

## Provenance

Artifact events must include source references, skill identifiers/versions and generation time. Source metadata should include period, grain, row count, filters and quality warnings when available.

## Permissions

Permissions control display, drilldown, export and available actions. An action that changes external state must be gated by approval.

## Transport

MVP: HTTP POST to start a run and SSE for events. WebSocket and webhook transports may be added without changing event payloads.

## Versioning

Events are additive. Artifact schemas use explicit versions. Adapters declare supported protocol versions.
