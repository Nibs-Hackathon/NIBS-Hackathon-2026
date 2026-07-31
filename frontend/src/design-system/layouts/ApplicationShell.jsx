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
