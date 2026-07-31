# Folder: frontend/src/design-system/layouts Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/design-system/layouts`

Contains 10 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/design-system/layouts/ApplicationShell.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/ApplicationShell.jsx`

```javascript
import { useEffect, useState } from 'react';
import {
  Box, IconButton, Stack, Tooltip, Typography,
} from '@mui/material';
import {
  ArticleOutlined, BuildOutlined, ChevronLeftOutlined, ChevronRightOutlined,
  DashboardOutlined, DevicesOutlined, MemoryOutlined, ScienceOutlined, WarningAmberOutlined,
} from '@mui/icons-material';
import { AnimatePresence, LayoutGroup, motion, useReducedMotion } from 'motion/react';
import { CommandBar, Dock, WorkspaceHeader, WorkspacePanel } from '../catalog';
import { LayoutPlaceholder } from './shared';

const DEFAULT_NAV = [
  { id: 'command', label: 'Command Center', icon: DashboardOutlined, group: 'Overview' },
  { id: 'assets', label: 'Assets', icon: DevicesOutlined, group: 'Operations' },
  { id: 'incidents', label: 'Incidents', icon: WarningAmberOutlined, group: 'Operations' },
  { id: 'maintenance', label: 'Maintenance', icon: BuildOutlined, group: 'Operations' },
  { id: 'investigation', label: 'AI Investigation', icon: MemoryOutlined, group: 'Intelligence' },
  { id: 'forecasting', label: 'Forecasting', icon: ScienceOutlined, group: 'Intelligence' },
  { id: 'reports', label: 'Reports', icon: ArticleOutlined, group: 'Intelligence' },
];

/**
 * ApplicationShell — wraps all workspaces.
 * Presentational: AppShell wires live ops. Showcase chrome mirrors ProductShell density.
 */
export function ApplicationShell({
  children,
  navItems = DEFAULT_NAV,
  activeNavId,
  onNavigate,
  header,
  title = 'Workspace',
  breadcrumbs = [],
  scope,
  facilities,
  onScopeChange,
  syncAge,
  connected = true,
  headerActions,
  showAuditSpine = true,
  auditSpine,
  workspacePanelOpen = false,
  onWorkspacePanelChange,
  workspacePanelAudit,
  notifications = [],
  onNotificationClick,
  commandOpen = false,
  onCommandOpenChange,
  commands = [],
  onCopilot,
  onPin,
  onSync,
  clock,
  telemetryLabel,
  aiLabel = 'AI monitoring',
  agentsActive = 0,
  unreadCount = 0,
  copilotOpen = false,
  copilot,
  navCollapsed: navCollapsedProp,
  onNavCollapse,
  className = '',
  sx,
}) {
  const reduced = useReducedMotion();
  const [internalCollapsed, setInternalCollapsed] = useState(false);
  const collapsed = navCollapsedProp ?? internalCollapsed;
  const toggleCollapsed = () => {
    const next = !collapsed;
    if (onNavCollapse) onNavCollapse(next);
    else setInternalCollapsed(next);
  };

  const [internalCommand, setInternalCommand] = useState(false);
  const cmdOpen = onCommandOpenChange ? commandOpen : internalCommand;
  const setCmdOpen = (open) => {
    if (onCommandOpenChange) onCommandOpenChange(open);
    else setInternalCommand(open);
  };

  const [internalPanel, setInternalPanel] = useState(false);
  const panelOpen = onWorkspacePanelChange ? workspacePanelOpen : internalPanel;
  const setPanelOpen = (open) => {
    const next = typeof open === 'function' ? open(panelOpen) : open;
    if (onWorkspacePanelChange) onWorkspacePanelChange(next);
    else setInternalPanel(next);
  };

  useEffect(() => {
    const onKey = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setCmdOpen(true);
      }
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'j') {
        event.preventDefault();
        setPanelOpen((open) => !open);
      }
      if (event.key === 'Escape') {
        setCmdOpen(false);
        setPanelOpen(false);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  const groups = ['Overview', 'Operations', 'Intelligence'];
  const spring = reduced ? { duration: 0 } : { type: 'spring', stiffness: 420, damping: 36 };

  return (
    <Box
      className={`rig-app-shell ${collapsed ? 'is-nav-collapsed' : ''} ${className}`}
      sx={sx}
    >
      <LayoutGroup id="rig-app-nav">
        <aside className="rig-app-shell-nav" aria-label="Primary navigation">
          <Stack direction="row" alignItems="center" justifyContent="space-between" className="rig-app-brand">
            <Stack direction="row" spacing={1} alignItems="center">
              <Box className="rig-app-brand-mark">R</Box>
              {!collapsed && (
                <Box>
                  <Typography className="rig-app-brand-title">RIG OS</Typography>
                  <Typography className="rig-label" sx={{ fontSize: 9 }}>Operations</Typography>
                </Box>
              )}
            </Stack>
            <Tooltip title={collapsed ? 'Expand' : 'Collapse'}>
              <IconButton size="small" onClick={toggleCollapsed} aria-label="Toggle navigation">
                {collapsed ? <ChevronRightOutlined /> : <ChevronLeftOutlined />}
              </IconButton>
            </Tooltip>
          </Stack>

          <nav className="rig-app-nav">
            {groups.map((group) => {
              const items = navItems.filter((item) => item.group === group);
              if (!items.length) return null;
              return (
                <Box key={group} className="rig-app-nav-group">
                  {!collapsed && <Typography className="rig-label">{group}</Typography>}
                  {items.map((item) => {
                    const Icon = item.icon;
                    const active = activeNavId === item.id;
                    return (
                      <Tooltip key={item.id} title={collapsed ? item.label : ''} placement="right">
                        <Box
                          component="button"
                          type="button"
                          className={`rig-app-nav-item ${active ? 'is-active' : ''}`}
                          onClick={() => onNavigate?.(item)}
                          aria-current={active ? 'page' : undefined}
                        >
                          {active && (
                            <motion.span
                              className="rig-app-nav-pill"
                              layoutId="rig-app-nav-pill"
                              transition={spring}
                            />
                          )}
                          {Icon && <Icon fontSize="small" />}
                          {!collapsed && <span>{item.label}</span>}
                        </Box>
                      </Tooltip>
                    );
                  })}
                </Box>
              );
            })}
          </nav>

          <Box className="rig-app-nav-footer">
            <Box className={`rig-app-connection ${connected ? 'is-live' : 'is-offline'}`}>
              <motion.i
                animate={connected ? { opacity: [1, 0.45, 1] } : { opacity: [1, 0.25, 1] }}
                transition={{ repeat: Infinity, duration: connected ? 2.4 : 0.9 }}
              />
              {!collapsed && (
                <Typography variant="caption">
                  {connected ? 'Live connection' : 'Reconnecting'}
                </Typography>
              )}
            </Box>
          </Box>
        </aside>
      </LayoutGroup>

      <Box className="rig-app-shell-stage">
        <Box className="rig-app-shell-header">
          {header ?? (
            <WorkspaceHeader
              title={title}
              breadcrumbs={breadcrumbs}
              scope={scope}
              facilities={facilities}
              onScopeChange={onScopeChange}
              syncAge={syncAge}
              connected={connected}
              onSync={onSync}
              clock={clock}
              telemetryLabel={telemetryLabel}
              aiLabel={aiLabel}
              agentsActive={agentsActive}
              unreadCount={unreadCount}
              onAiClick={onCopilot}
              onInbox={onNotificationClick}
              actions={headerActions}
            />
          )}
        </Box>

        <main className="rig-app-shell-main">
          {children ?? <LayoutPlaceholder label="workspace layout" />}
        </main>

        {showAuditSpine && (
          <Box className="rig-app-shell-audit">
            {auditSpine ?? <LayoutPlaceholder label="auditSpine" />}
          </Box>
        )}
      </Box>

      <Dock
        onCommand={() => setCmdOpen(true)}
        onCopilot={onCopilot}
        onWorkspacePanel={() => setPanelOpen((open) => !open)}
        onPin={onPin}
      />

      <CommandBar
        open={cmdOpen}
        onClose={() => setCmdOpen(false)}
        commands={commands.length ? commands : navItems.map((item) => ({
          label: item.label,
          group: item.group,
          onSelect: () => onNavigate?.(item),
        }))}
      />

      <WorkspacePanel
        open={panelOpen}
        onClose={() => setPanelOpen(false)}
        auditContent={workspacePanelAudit}
        notifications={notifications}
        onNotificationClick={onNotificationClick}
      />

      <AnimatePresence>
        {copilotOpen && copilot && (
          <motion.aside
            className="rig-copilot-dock"
            initial={{ opacity: 0, x: 24 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 24 }}
            transition={spring}
          >
            {copilot}
          </motion.aside>
        )}
      </AnimatePresence>
    </Box>
  );
}

export { DEFAULT_NAV as APPLICATION_SHELL_NAV };
```

## frontend/src/design-system/layouts/ExecutiveLayout.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/ExecutiveLayout.jsx`

```javascript
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
```

## frontend/src/design-system/layouts/ExplorerLayout.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/ExplorerLayout.jsx`

```javascript
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
```

## frontend/src/design-system/layouts/IncidentLayout.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/IncidentLayout.jsx`

```javascript
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
```

## frontend/src/design-system/layouts/index.js

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/index.js`

```javascript
export { LayoutPlaceholder, LayoutTabs, Pane, useCompactLayout } from './shared';
export { MissionControlLayout } from './MissionControlLayout';
export { ExplorerLayout } from './ExplorerLayout';
export { IncidentLayout } from './IncidentLayout';
export { InvestigationLayout } from './InvestigationLayout';
export { KanbanLayout } from './KanbanLayout';
export { ExecutiveLayout } from './ExecutiveLayout';
export { ApplicationShell, APPLICATION_SHELL_NAV } from './ApplicationShell';
```

## frontend/src/design-system/layouts/InvestigationLayout.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/InvestigationLayout.jsx`

```javascript
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
```

## frontend/src/design-system/layouts/KanbanLayout.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/KanbanLayout.jsx`

```javascript
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
```

## frontend/src/design-system/layouts/layouts.css

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/layouts.css`

```css
/* Epic 2 — reusable layout grids. Slot containers only. */

.rig-layout {
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
  width: 100%;
  gap: 16px;
}

.rig-layout-scroll {
  overflow: auto;
  min-height: 0;
}

.rig-layout-pane {
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid rgba(164, 196, 228, 0.12);
  border-radius: 10px;
  background: #111722;
}

.rig-layout-pane-body {
  flex: 1;
  overflow: auto;
  min-height: 0;
  padding: 12px;
}

.rig-layout-placeholder {
  display: grid;
  place-items: center;
  min-height: 80px;
  padding: 16px;
  border: 1px dashed rgba(164, 196, 228, 0.22);
  border-radius: 8px;
  color: #93A2B8;
  font-size: 0.75rem;
  font-weight: 650;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  text-align: center;
}

.rig-layout-tabs {
  display: none;
  gap: 4px;
  flex-shrink: 0;
}

.rig-layout-tabs button {
  flex: 1;
  border: 0;
  padding: 10px 8px;
  border-radius: 8px;
  background: transparent;
  color: #93A2B8;
  font-size: 0.75rem;
  font-weight: 650;
  cursor: pointer;
}

.rig-layout-tabs button.is-active {
  background: #0d1219;
  color: #EEF4FC;
}

/* —— Mission Control —— */
.rig-mission-layout {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  grid-template-rows: auto minmax(200px, 1fr) auto auto;
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.rig-mission-strip {
  grid-column: 1 / -1;
  position: sticky;
  top: 0;
  z-index: 2;
}

.rig-mission-map { grid-column: 1 / 9; min-height: 0; }
.rig-mission-queue { grid-column: 9 / 13; min-height: 0; }
.rig-mission-sparklines { grid-column: 1 / -1; }
.rig-mission-audit {
  grid-column: 1 / -1;
  position: sticky;
  bottom: 0;
  z-index: 2;
  min-height: 32px;
}

/* —— Explorer (twin + forecast) —— */
.rig-explorer-layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr) 320px;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.rig-explorer-tree { grid-row: 1; grid-column: 1; }
.rig-explorer-canvas { grid-row: 1; grid-column: 2; }
.rig-explorer-inspector { grid-row: 1; grid-column: 3; }
.rig-explorer-signals {
  grid-column: 2;
  grid-row: 2;
  max-height: 120px;
}

.rig-explorer-layout[data-variant="forecast"] .rig-explorer-tree {
  /* watchlist same width as explorer */
}

/* —— Incident —— */
.rig-incident-layout {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr) 360px;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.rig-incident-queue { grid-column: 1; grid-row: 1; }
.rig-incident-timeline { grid-column: 2; grid-row: 1; }
.rig-incident-dossier { grid-column: 3; grid-row: 1; }
.rig-incident-decision {
  grid-column: 1 / -1;
  grid-row: 2;
  position: sticky;
  bottom: 0;
  z-index: 2;
}

/* —— Investigation —— */
.rig-investigation-layout {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  grid-template-rows: 120px minmax(0, 1fr) auto;
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.rig-investigation-pipeline {
  grid-column: 1 / -1;
  grid-row: 1;
  position: sticky;
  top: 0;
  z-index: 2;
  overflow-x: auto;
}

.rig-investigation-trace { grid-column: 1; grid-row: 2; }
.rig-investigation-evidence { grid-column: 2; grid-row: 2; }
.rig-investigation-decision {
  grid-column: 1 / -1;
  grid-row: 3;
  position: sticky;
  bottom: 0;
  z-index: 2;
}

/* —— Kanban —— */
.rig-kanban-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  grid-template-rows: auto minmax(0, 1fr);
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.rig-kanban-toolbar {
  grid-column: 1 / -1;
  position: sticky;
  top: 0;
  z-index: 2;
}

.rig-kanban-board {
  grid-column: 1;
  overflow-x: auto;
  overflow-y: hidden;
}

.rig-kanban-columns {
  display: flex;
  gap: 12px;
  min-width: max-content;
  height: 100%;
  padding-bottom: 4px;
}

.rig-kanban-column {
  width: 220px;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(164, 196, 228, 0.12);
  border-radius: 10px;
  background: #0d1219;
  overflow: hidden;
}

.rig-kanban-column-head {
  padding: 10px 12px;
  border-bottom: 1px solid rgba(164, 196, 228, 0.12);
  font-size: 0.6875rem;
  font-weight: 650;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #93A2B8;
}

.rig-kanban-column-body {
  flex: 1;
  overflow: auto;
  padding: 8px;
}

.rig-kanban-inspector { grid-column: 2; }

/* —— Executive —— */
.rig-executive-layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr) 300px;
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.rig-executive-index { overflow: auto; }
.rig-executive-brief { overflow: auto; }
.rig-executive-rail { overflow: auto; }

/* —— Application Shell —— */
.rig-app-shell {
  display: grid;
  grid-template-columns: var(--rig-nav-width, 246px) minmax(0, 1fr);
  height: 100vh;
  width: 100%;
  background:
    radial-gradient(1200px 600px at 20% -10%, rgba(38, 132, 255, 0.12), transparent 55%),
    radial-gradient(900px 500px at 90% 10%, rgba(94, 77, 178, 0.1), transparent 50%),
    #090b0f;
  color: #EEF4FC;
  --rig-nav-width: 246px;
}

.rig-app-shell.is-nav-collapsed {
  --rig-nav-width: 72px;
}

.rig-app-shell-nav {
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(148, 163, 184, 0.12);
  background: #0d1015;
  overflow: hidden;
  z-index: 20;
}

.rig-app-brand {
  height: 52px;
  padding: 12px 14px;
  flex-shrink: 0;
}

.rig-app-brand-mark {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border-radius: 9px;
  background: #edf3fb;
  color: #0d1015;
  font-weight: 900;
  font-size: 12px;
}

.rig-app-brand-title {
  font-size: 0.88rem;
  font-weight: 850;
  letter-spacing: -0.04em;
  line-height: 1;
}

.rig-app-nav {
  flex: 1;
  overflow: auto;
  padding: 8px 10px 16px;
}

.rig-app-nav-group {
  margin-bottom: 14px;
}

.rig-app-nav-group .rig-label {
  padding: 0 10px 6px;
  font-size: 0.58rem;
}

.rig-app-nav-item {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 40px;
  padding: 8px 12px;
  margin-bottom: 2px;
  border: 0;
  border-radius: 10px;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
  text-align: left;
  font-size: 0.84rem;
  font-weight: 650;
  z-index: 0;
}

.rig-app-nav-item:hover {
  color: #f8fafc;
  background: rgba(255, 255, 255, 0.04);
}

.rig-app-nav-item.is-active {
  color: #f8fafc;
}

.rig-app-nav-pill {
  position: absolute;
  inset: 0;
  border-radius: 10px;
  background: rgba(38, 132, 255, 0.16);
  z-index: -1;
}

.rig-app-nav-footer {
  padding: 12px;
  border-top: 1px solid rgba(148, 163, 184, 0.12);
}

.rig-app-connection {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #94a3b8;
}

.rig-app-connection i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22a06b;
  display: inline-block;
}

.rig-app-connection.is-offline i {
  background: #e2483d;
}

.rig-app-shell-stage {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.rig-app-shell-header {
  padding: 0 20px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
  background: rgba(13, 16, 21, 0.72);
  backdrop-filter: blur(12px);
  z-index: 3;
  flex-shrink: 0;
}

.rig-app-shell-main {
  flex: 1;
  padding: 16px 20px;
  overflow: hidden;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.rig-app-shell-audit {
  flex-shrink: 0;
  z-index: 3;
}

.rig-copilot-dock {
  position: fixed;
  top: 72px;
  right: 16px;
  bottom: 72px;
  width: min(420px, calc(100vw - 32px));
  z-index: 50;
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: #111418;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
}

.rig-layout-pane {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.02), transparent 40%),
    repeating-linear-gradient(0deg, transparent, transparent 23px, rgba(148, 163, 184, 0.04) 24px),
    #111722;
}

@media (max-width: 1023px) {
  .rig-layout-tabs { display: flex; }

  .rig-mission-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }
  .rig-mission-strip,
  .rig-mission-map,
  .rig-mission-queue,
  .rig-mission-sparklines,
  .rig-mission-audit { grid-column: 1; }
  .rig-mission-layout.is-tabbed .rig-mission-map,
  .rig-mission-layout.is-tabbed .rig-mission-queue,
  .rig-mission-layout.is-tabbed .rig-mission-sparklines { display: none; }
  .rig-mission-layout.is-tabbed[data-tab="queue"] .rig-mission-queue { display: flex; }
  .rig-mission-layout.is-tabbed[data-tab="map"] .rig-mission-map { display: flex; }
  .rig-mission-layout.is-tabbed[data-tab="sparklines"] .rig-mission-sparklines { display: block; }

  .rig-explorer-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto minmax(0, 1fr) auto;
  }
  .rig-explorer-tree,
  .rig-explorer-canvas,
  .rig-explorer-inspector,
  .rig-explorer-signals { grid-column: 1; grid-row: auto; }
  .rig-explorer-layout.is-tabbed .rig-explorer-tree,
  .rig-explorer-layout.is-tabbed .rig-explorer-canvas,
  .rig-explorer-layout.is-tabbed .rig-explorer-inspector { display: none; }
  .rig-explorer-layout.is-tabbed[data-tab="explorer"] .rig-explorer-tree { display: flex; }
  .rig-explorer-layout.is-tabbed[data-tab="canvas"] .rig-explorer-canvas { display: flex; }
  .rig-explorer-layout.is-tabbed[data-tab="inspector"] .rig-explorer-inspector { display: flex; }

  .rig-incident-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto minmax(0, 1fr) auto;
  }
  .rig-incident-queue,
  .rig-incident-timeline,
  .rig-incident-dossier,
  .rig-incident-decision { grid-column: 1; grid-row: auto; }
  .rig-incident-layout.is-tabbed .rig-incident-queue,
  .rig-incident-layout.is-tabbed .rig-incident-timeline,
  .rig-incident-layout.is-tabbed .rig-incident-dossier { display: none; }
  .rig-incident-layout.is-tabbed[data-tab="queue"] .rig-incident-queue { display: flex; }
  .rig-incident-layout.is-tabbed[data-tab="timeline"] .rig-incident-timeline { display: flex; }
  .rig-incident-layout.is-tabbed[data-tab="dossier"] .rig-incident-dossier { display: flex; }

  .rig-investigation-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto minmax(0, 1fr) auto;
  }
  .rig-investigation-pipeline,
  .rig-investigation-trace,
  .rig-investigation-evidence,
  .rig-investigation-decision { grid-column: 1; }
  .rig-investigation-layout.is-tabbed .rig-investigation-trace,
  .rig-investigation-layout.is-tabbed .rig-investigation-evidence { display: none; }
  .rig-investigation-layout.is-tabbed[data-tab="trace"] .rig-investigation-trace { display: flex; }
  .rig-investigation-layout.is-tabbed[data-tab="evidence"] .rig-investigation-evidence { display: flex; }

  .rig-kanban-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto minmax(0, 1fr);
  }
  .rig-kanban-inspector { grid-column: 1; }
  .rig-kanban-layout.is-tabbed .rig-kanban-board,
  .rig-kanban-layout.is-tabbed .rig-kanban-inspector { display: none; }
  .rig-kanban-layout.is-tabbed[data-tab="board"] .rig-kanban-board { display: block; }
  .rig-kanban-layout.is-tabbed[data-tab="inspector"] .rig-kanban-inspector { display: flex; }

  .rig-executive-layout {
    grid-template-columns: 1fr;
  }
  .rig-executive-layout.is-tabbed .rig-executive-index,
  .rig-executive-layout.is-tabbed .rig-executive-brief,
  .rig-executive-layout.is-tabbed .rig-executive-rail { display: none; }
  .rig-executive-layout.is-tabbed[data-tab="index"] .rig-executive-index { display: flex; }
  .rig-executive-layout.is-tabbed[data-tab="brief"] .rig-executive-brief { display: flex; }
  .rig-executive-layout.is-tabbed[data-tab="rail"] .rig-executive-rail { display: flex; }

  .rig-app-shell {
    grid-template-columns: 72px minmax(0, 1fr);
  }
  .rig-app-shell-nav .rig-app-brand > div:not(.rig-app-brand-mark),
  .rig-app-nav-group .rig-label,
  .rig-app-nav-item span,
  .rig-app-connection .MuiTypography-root {
    display: none;
  }
}

html[data-rigos-theme='light'] .rig-layout-pane,
html[data-rigos-theme='light'] .rig-app-shell-nav,
html[data-rigos-theme='light'] .rig-kanban-column {
  background: #fff;
  border-color: rgba(15, 23, 42, 0.1);
  color: #111827;
}
html[data-rigos-theme='light'] .rig-app-shell,
html[data-rigos-theme='light'] .rig-app-shell-header {
  background: #f6f7f9;
  color: #111827;
}
html[data-rigos-theme='light'] .rig-layout-placeholder {
  color: #64748b;
  border-color: rgba(15, 23, 42, 0.15);
}
```

## frontend/src/design-system/layouts/MissionControlLayout.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/MissionControlLayout.jsx`

```javascript
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
```

## frontend/src/design-system/layouts/shared.jsx

**Folder path:** `frontend/src/design-system/layouts`

**File path:** `frontend/src/design-system/layouts/shared.jsx`

```javascript
import { useEffect, useState } from 'react';
import { Box } from '@mui/material';

const COMPACT_MQ = '(max-width: 1023px)';

/** True when layout should use tab collapse (<1024px). */
export function useCompactLayout() {
  const [compact, setCompact] = useState(() => (
    typeof window !== 'undefined' ? window.matchMedia(COMPACT_MQ).matches : false
  ));

  useEffect(() => {
    const media = window.matchMedia(COMPACT_MQ);
    const onChange = () => setCompact(media.matches);
    onChange();
    media.addEventListener('change', onChange);
    return () => media.removeEventListener('change', onChange);
  }, []);

  return compact;
}

/** Slot placeholder for layout previews / empty slots */
export function LayoutPlaceholder({ label = 'Slot', className = '', sx }) {
  return (
    <Box className={`rig-layout-placeholder ${className}`} sx={sx}>
      {label}
    </Box>
  );
}

/** Mobile tab strip for compact layouts */
export function LayoutTabs({ tabs = [], value, onChange, className = '' }) {
  return (
    <Box className={`rig-layout-tabs ${className}`} role="tablist">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          type="button"
          role="tab"
          aria-selected={value === tab.id}
          className={value === tab.id ? 'is-active' : ''}
          onClick={() => onChange?.(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </Box>
  );
}

export function Pane({ children, className = '', bodyClassName = '', sx }) {
  return (
    <Box className={`rig-layout-pane ${className}`} sx={sx}>
      <Box className={`rig-layout-pane-body ${bodyClassName}`}>{children}</Box>
    </Box>
  );
}
```
