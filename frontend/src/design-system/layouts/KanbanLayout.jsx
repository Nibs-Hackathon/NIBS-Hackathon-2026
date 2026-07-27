import { useState } from 'react';
import { Box } from '@mui/material';
import { LayoutPlaceholder, LayoutTabs, Pane, useCompactLayout } from './shared';

const DEFAULT_COLUMNS = ['Backlog', 'Ready', 'Scheduled', 'In progress', 'Complete'];

const TABS = [
  { id: 'board', label: 'Board' },
  { id: 'inspector', label: 'Inspector' },
];

/**
 * KanbanLayout — read-only board shell (DnD deferred)
 * Slots: toolbar, board (or columns map), inspector
 */
export function KanbanLayout({
  toolbar,
  board,
  columns = DEFAULT_COLUMNS,
  columnContent,
  inspector,
  className = '',
  sx,
}) {
  const compact = useCompactLayout();
  const [tab, setTab] = useState('board');

  const boardNode = board ?? (
    <Box className="rig-kanban-columns">
      {columns.map((name) => (
        <Box key={name} className="rig-kanban-column">
          <Box className="rig-kanban-column-head">{name}</Box>
          <Box className="rig-kanban-column-body">
            {columnContent?.[name] ?? <LayoutPlaceholder label={name} />}
          </Box>
        </Box>
      ))}
    </Box>
  );

  return (
    <Box
      className={`rig-kanban-layout ${compact ? 'is-tabbed' : ''} ${className}`}
      data-tab={compact ? tab : undefined}
      sx={sx}
    >
      <Box className="rig-kanban-toolbar">
        {toolbar ?? <LayoutPlaceholder label="toolbar" />}
      </Box>

      {compact && <LayoutTabs tabs={TABS} value={tab} onChange={setTab} />}

      <Box className="rig-kanban-board">
        {boardNode}
      </Box>
      <Pane className="rig-kanban-inspector">
        {inspector ?? <LayoutPlaceholder label="objectInspector" />}
      </Pane>
    </Box>
  );
}
