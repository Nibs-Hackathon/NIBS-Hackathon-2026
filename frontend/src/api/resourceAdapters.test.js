import assert from 'node:assert/strict';
import test from 'node:test';
import { notificationPresentation } from './resourceAdapters.js';

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
