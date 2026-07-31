import { useState } from 'react';
import { Box } from '@mui/material';
import { LayoutPlaceholder, LayoutTabs, Pane, useCompactLayout } from './shared';

const TABS = [
  { id: 'trace', label: 'Trace' },
  { id: 'evidence', label: 'Evidence' },
];

/**
 * InvestigationLayout
 * Slots: pipeline, tracePanel, evidenceDetail, decisionBar
 * Sticky: pipeline top, decisionBar bottom
 */
export function InvestigationLayout({
  pipeline,
  tracePanel,
  evidenceDetail,
  decisionBar,
  className = '',
  sx,
}) {
  const compact = useCompactLayout();
  const [tab, setTab] = useState('trace');

  return (
    <Box
      className={`rig-investigation-layout ${compact ? 'is-tabbed' : ''} ${className}`}
      data-tab={compact ? tab : undefined}
      sx={sx}
    >
      <Box className="rig-investigation-pipeline rig-layout-pane" sx={{ p: 1 }}>
        {pipeline ?? <LayoutPlaceholder label="pipeline" />}
      </Box>

      {compact && <LayoutTabs tabs={TABS} value={tab} onChange={setTab} />}

      <Pane className="rig-investigation-trace">
        {tracePanel ?? <LayoutPlaceholder label="tracePanel" />}
      </Pane>
      <Pane className="rig-investigation-evidence">
        {evidenceDetail ?? <LayoutPlaceholder label="evidenceDetail" />}
      </Pane>
      <Box className="rig-investigation-decision">
        {decisionBar ?? <LayoutPlaceholder label="decisionBar" />}
      </Box>
    </Box>
  );
}
