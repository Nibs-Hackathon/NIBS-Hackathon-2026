import { useState } from 'react';
import { Box } from '@mui/material';
import { LayoutPlaceholder, LayoutTabs, Pane, useCompactLayout } from './shared';

const TABS = [
  { id: 'queue', label: 'Queue' },
  { id: 'timeline', label: 'Timeline' },
  { id: 'dossier', label: 'Dossier' },
];

/**
 * IncidentLayout
 * Slots: queue, timeline, dossier, decisionBar
 * Sticky: decisionBar bottom. Compact: tabs
 */
export function IncidentLayout({
  queue,
  timeline,
  dossier,
  decisionBar,
  className = '',
  sx,
}) {
  const compact = useCompactLayout();
  const [tab, setTab] = useState('timeline');

  return (
    <Box
      className={`rig-incident-layout ${compact ? 'is-tabbed' : ''} ${className}`}
      data-tab={compact ? tab : undefined}
      sx={sx}
    >
      {compact && <LayoutTabs tabs={TABS} value={tab} onChange={setTab} />}

      <Pane className="rig-incident-queue">
        {queue ?? <LayoutPlaceholder label="queue" />}
      </Pane>
      <Pane className="rig-incident-timeline">
        {timeline ?? <LayoutPlaceholder label="timeline" />}
      </Pane>
      <Pane className="rig-incident-dossier">
        {dossier ?? <LayoutPlaceholder label="dossier" />}
      </Pane>
      <Box className="rig-incident-decision">
        {decisionBar ?? <LayoutPlaceholder label="decisionBar" />}
      </Box>
    </Box>
  );
}
