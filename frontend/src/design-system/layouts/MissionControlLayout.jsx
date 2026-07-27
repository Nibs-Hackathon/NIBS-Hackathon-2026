import { useState } from 'react';
import { Box } from '@mui/material';
import { LayoutPlaceholder, LayoutTabs, Pane, useCompactLayout } from './shared';

const TABS = [
  { id: 'queue', label: 'Queue' },
  { id: 'map', label: 'Risk map' },
  { id: 'sparklines', label: 'Telemetry' },
];

/**
 * MissionControlLayout
 * Slots: operationsStrip, riskMap, decisionQueue, sparklineRow, auditTicker
 * Sticky: strip top, audit bottom. Compact: Strip → Queue → Map → Sparklines
 */
export function MissionControlLayout({
  operationsStrip,
  riskMap,
  decisionQueue,
  sparklineRow,
  auditTicker,
  className = '',
  sx,
}) {
  const compact = useCompactLayout();
  const [tab, setTab] = useState('queue');

  return (
    <Box
      className={`rig-mission-layout ${compact ? 'is-tabbed' : ''} ${className}`}
      data-tab={compact ? tab : undefined}
      sx={sx}
    >
      <Box className="rig-mission-strip">
        {operationsStrip ?? <LayoutPlaceholder label="operationsStrip" />}
      </Box>

      {compact && <LayoutTabs tabs={TABS} value={tab} onChange={setTab} />}

      <Pane className="rig-mission-map">
        {riskMap ?? <LayoutPlaceholder label="riskMap" />}
      </Pane>
      <Pane className="rig-mission-queue">
        {decisionQueue ?? <LayoutPlaceholder label="decisionQueue" />}
      </Pane>
      <Box className="rig-mission-sparklines">
        {sparklineRow ?? <LayoutPlaceholder label="sparklineRow" />}
      </Box>
      <Box className="rig-mission-audit">
        {auditTicker ?? <LayoutPlaceholder label="auditTicker" />}
      </Box>
    </Box>
  );
}
