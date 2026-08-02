import assert from 'node:assert/strict';
import test from 'node:test';
import { fleetHealthForScope, notificationPresentation } from './resourceAdapters.js';

test('notification presentation prioritizes asset and refinery identity', () => {
  assert.deepEqual(
    notificationPresentation({
      title: 'Legacy incident title',
      message: 'Pressure spike detected',
      asset_name: 'Pipeline P-002',
      refinery_name: 'Mumbai Coastal Refinery',
      incident_type: 'Pressure spike',
    }),
    {
      title: 'Pipeline P-002 · Mumbai Coastal Refinery',
      detail: 'Pressure spike detected',
    },
  );
});

test('notification presentation supports legacy incident payloads', () => {
  assert.deepEqual(
    notificationPresentation({
      title: 'Pressure spike',
      message: 'Pipeline P-002',
      asset_name: 'Pipeline P-002',
      incident_type: 'Pressure spike',
    }),
    {
      title: 'Pipeline P-002',
      detail: 'Pressure spike',
    },
  );
});

test('fleet health averages only published numeric readings', () => {
  assert.equal(
    fleetHealthForScope({
      assets: [{ health: 90 }, { health: null }, { health: 70 }],
      dashboard: { fleet_health: 10 },
    }, 'Enterprise view'),
    80,
  );
});

test('fleet health falls back to dashboard when assets lack readings', () => {
  assert.equal(
    fleetHealthForScope({
      assets: [{ health: null }],
      dashboard: { fleet_health: 92.5 },
    }, 'Enterprise view'),
    92.5,
  );
});
