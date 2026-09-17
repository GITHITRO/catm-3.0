import { EventEnvelopeSchema } from '../../packages/protocol/src/index.js';

const event = {
  protocol: 'catman-agent-ui',
  protocol_version: '0.1',
  run_id: 'run_demo',
  event_id: 'evt_demo',
  timestamp: new Date().toISOString(),
  type: 'artifact.created',
  payload: {
    artifact: {
      id: 'artifact_demo',
      type: 'insight_brief',
      title: 'Promo uplift summary',
      status: 'ready'
    }
  },
  provenance: {
    sources: [{ source_id: 'sales_pos', label: 'POS sales' }],
    skills: ['promo-analysis'],
    generated_at: new Date().toISOString()
  },
  permissions: {
    display: true,
    drilldown: true,
    export: true,
    actions: [{ action_type: 'drilldown', label: 'Show drivers' }]
  }
};

console.log(EventEnvelopeSchema.parse(event));
