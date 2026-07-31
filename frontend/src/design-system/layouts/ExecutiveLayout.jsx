import { useState } from 'react';
import { Box } from '@mui/material';
import { LayoutPlaceholder, LayoutTabs, Pane, useCompactLayout } from './shared';

const TABS = [
  { id: 'index', label: 'Index' },
  { id: 'brief', label: 'Brief' },
  { id: 'rail', label: 'Decision' },
];

/**
 * ExecutiveLayout — non-operational (no AuditSpine in shell)
 * Slots: reportIndex, briefDocument, decisionRail
 */
export function ExecutiveLayout({
  reportIndex,
  briefDocument,
  decisionRail,
  className = '',
  sx,
}) {
  const compact = useCompactLayout();
  const [tab, setTab] = useState('brief');

  return (
    <Box
      className={`rig-executive-layout ${compact ? 'is-tabbed' : ''} ${className}`}
      data-tab={compact ? tab : undefined}
      sx={sx}
    >
      {compact && <LayoutTabs tabs={TABS} value={tab} onChange={setTab} />}

      <Pane className="rig-executive-index">
        {reportIndex ?? <LayoutPlaceholder label="reportIndex" />}
      </Pane>
      <Pane className="rig-executive-brief">
        {briefDocument ?? <LayoutPlaceholder label="briefDocument" />}
      </Pane>
      <Pane className="rig-executive-rail">
        {decisionRail ?? <LayoutPlaceholder label="decisionRail" />}
      </Pane>
    </Box>
  );
}
