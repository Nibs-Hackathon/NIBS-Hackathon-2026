import { useState } from 'react';
import { Box } from '@mui/material';
import { LayoutPlaceholder, LayoutTabs, Pane, useCompactLayout } from './shared';

const TABS = [
  { id: 'explorer', label: 'Explorer' },
  { id: 'canvas', label: 'Canvas' },
  { id: 'inspector', label: 'Inspector' },
];

/**
 * ExplorerLayout — Assets twin + Forecasting
 * Slots: explorer, canvas, inspector, signalStrip (optional)
 * canvasVariant: "twin" | "forecast"
 * Compact: tabs Explorer | Canvas | ObjectInspector
 */
export function ExplorerLayout({
  explorer,
  canvas,
  inspector,
  signalStrip,
  canvasVariant = 'twin',
  className = '',
  sx,
}) {
  const compact = useCompactLayout();
  const [tab, setTab] = useState('canvas');

  return (
    <Box
      className={`rig-explorer-layout ${compact ? 'is-tabbed' : ''} ${className}`}
      data-variant={canvasVariant}
      data-tab={compact ? tab : undefined}
      sx={sx}
    >
      {compact && <LayoutTabs tabs={TABS} value={tab} onChange={setTab} />}

      <Pane className="rig-explorer-tree">
        {explorer ?? <LayoutPlaceholder label={canvasVariant === 'forecast' ? 'watchlist' : 'explorer'} />}
      </Pane>
      <Pane className="rig-explorer-canvas">
        {canvas ?? <LayoutPlaceholder label={`canvas:${canvasVariant}`} />}
      </Pane>
      <Pane className="rig-explorer-inspector">
        {inspector ?? <LayoutPlaceholder label="objectInspector" />}
      </Pane>
      {signalStrip != null && (
        <Box className="rig-explorer-signals">
          {signalStrip || <LayoutPlaceholder label="signalStrip" />}
        </Box>
      )}
    </Box>
  );
}
