import { z } from 'zod';

export const EventTypeSchema = z.enum([
  'run.started', 'run.completed', 'run.failed', 'message.delta',
  'task.interpreted', 'plan.updated', 'source.discovered', 'source.validated',
  'skill.started', 'skill.completed', 'artifact.created', 'artifact.updated',
  'artifact.versioned', 'action.proposed', 'approval.requested',
  'action.completed', 'receipt.created', 'warning.created'
]);

export const EventEnvelopeSchema = z.object({
  protocol: z.literal('catman-agent-ui'),
  protocol_version: z.string(),
  run_id: z.string().min(1),
  event_id: z.string().min(1),
  timestamp: z.string().datetime(),
  type: EventTypeSchema,
  payload: z.record(z.unknown()),
  provenance: z.object({
    sources: z.array(z.record(z.unknown())),
    skills: z.array(z.string()),
    generated_at: z.string().datetime()
  }),
  permissions: z.object({
    display: z.boolean(),
    drilldown: z.boolean(),
    export: z.boolean(),
    actions: z.array(z.record(z.unknown()))
  })
});

export type EventType = z.infer<typeof EventTypeSchema>;
export type EventEnvelope = z.infer<typeof EventEnvelopeSchema>;
