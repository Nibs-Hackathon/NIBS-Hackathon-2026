import { useMemo, useState } from 'react';
import {
  Badge, Box, Button, Dialog, DialogContent, IconButton, MenuItem, Stack, TextField, Tooltip, Typography,
} from '@mui/material';
import {
  NotificationsOutlined, PushPinOutlined, SearchOutlined, SmartToyOutlined, SyncOutlined, ViewSidebarOutlined,
} from '@mui/icons-material';
import { motion } from 'motion/react';
import { MetricCard } from './data';
import { StatusBadge, normalizeStatus } from './status';
import { AuditEvent } from './time';
import { ObjectRow, IncidentQueueItem } from './objects';
import WorkspaceDock from '../../components/react-bits/Dock/Dock';
import '../../components/react-bits/Dock/Dock.css';

/** WorkspaceHeader — title + breadcrumbs + ambient ops chrome */
export function WorkspaceHeader({
  title, breadcrumbs = [], scope, onScopeChange, facilities = [], syncAge, connected = true,
  onSync, clock, telemetryLabel, aiLabel, agentsActive = 0, unreadCount = 0, onAiClick, onInbox,
  actions, className = '', sx,
}) {
  return (
    <Box className={`rig-workspace-header ${className}`} sx={sx}>
      <Box sx={{ minWidth: 0 }}>
        {breadcrumbs.length > 0 && (
          <nav className="rig-breadcrumbs" aria-label="Breadcrumb">
            {breadcrumbs.map((crumb, index) => (
              <Box key={`${crumb.label}-${index}`} component="span" sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.75 }}>
                {index > 0 && <span aria-hidden>›</span>}
                <button type="button" onClick={() => crumb.onNavigate?.(crumb)} disabled={!crumb.onNavigate}>
                  {crumb.label}
                </button>
              </Box>
            ))}
          </nav>
        )}
        <Typography component="h1">{title}</Typography>
      </Box>
      <Stack direction="row" spacing={1} alignItems="center" flexShrink={0} className="rig-workspace-chrome">
        {(clock || telemetryLabel) && (
          <Box className="rig-ambient">
            {clock && <Typography className="rig-mono">{clock}</Typography>}
            {telemetryLabel && <Typography variant="caption" color="text.secondary">{telemetryLabel}</Typography>}
          </Box>
        )}
        {scope !== undefined && (
          <ScopeSwitcher value={scope} onChange={onScopeChange} options={facilities} />
        )}
        <SyncIndicator connected={connected} syncAge={syncAge} onRefresh={onSync} />
        {aiLabel && (
          <Tooltip title={aiLabel}>
            <Button
              className="rig-ai-status"
              size="small"
              onClick={onAiClick}
              startIcon={<SmartToyOutlined fontSize="small" />}
            >
              <motion.i
                className="rig-ai-pulse-dot"
                animate={agentsActive ? { opacity: [1, 0.4, 1] } : false}
                transition={{ repeat: Infinity, duration: 1.6 }}
              />
              {aiLabel}
            </Button>
          </Tooltip>
        )}
        {onInbox && (
          <Tooltip title="Notifications">
            <IconButton onClick={onInbox} aria-label="Open notifications" size="small">
              <Badge badgeContent={unreadCount} color="error">
                <NotificationsOutlined fontSize="small" />
              </Badge>
            </IconButton>
          </Tooltip>
        )}
        {actions}
      </Stack>
    </Box>
  );
}

/** ScopeSwitcher */
export function ScopeSwitcher({
  value,
  onChange,
  options = ['Alpha Refinery', 'North Sea Portfolio', 'Enterprise view'],
  className = '',
  sx,
}) {
  const normalized = options.map((opt) => (
    typeof opt === 'string' ? { value: opt, label: opt, detail: null } : opt
  ));
  const safeValue = normalized.some((opt) => opt.value === value)
    ? value
    : (normalized[0]?.value || 'Enterprise view');

  return (
    <TextField
      select
      size="small"
      value={safeValue}
      onChange={(e) => onChange?.(e.target.value)}
      className={className}
      sx={{ minWidth: 200, ...sx }}
      aria-label="Facility scope"
    >
      {normalized.map((opt) => (
        <MenuItem key={opt.value} value={opt.value}>
          <Box>
            <Typography variant="body2" sx={{ lineHeight: 1.3 }}>{opt.label}</Typography>
            {opt.detail ? (
              <Typography variant="caption" color="text.secondary" display="block">
                {opt.detail}
              </Typography>
            ) : null}
          </Box>
        </MenuItem>
      ))}
    </TextField>
  );
}

/** SyncIndicator */
export function SyncIndicator({ connected = true, syncAge, onRefresh, className = '', sx }) {
  const label = connected
    ? (syncAge != null ? `Synced ${syncAge}s ago` : 'Live')
    : 'Reconnecting';
  return (
    <Stack direction="row" spacing={0.75} alignItems="center" className={className} sx={sx}>
      <StatusBadge label={connected ? 'Live' : 'Offline'} status={connected ? 'nominal' : 'offline'} live={connected} />
      <Typography variant="caption" color="text.secondary">{label}</Typography>
      {onRefresh && (
        <IconButton size="small" onClick={onRefresh} aria-label="Refresh telemetry"><SyncOutlined fontSize="small" /></IconButton>
      )}
    </Stack>
  );
}

/** OperationsStrip — 4 KPIs + CTA */
export function OperationsStrip({ metrics = [], cta, className = '', sx }) {
  const items = metrics.slice(0, 4);
  while (items.length < 4) items.push({ label: '—', value: '—' });
  return (
    <Box className={`rig-operations-strip ${className}`} sx={sx} role="region" aria-label="Operations strip">
      {items.map((metric, index) => (
        <Box key={metric.label || index} className="rig-strip-metric">
          <Typography className="rig-label">{metric.label}</Typography>
          <Typography className="rig-kpi">{metric.value}</Typography>
          {metric.detail && <Typography variant="caption" color="text.secondary">{metric.detail}</Typography>}
        </Box>
      ))}
      <Box className="rig-strip-cta">{cta}</Box>
    </Box>
  );
}

/** CommandBar — global modal search/actions */
export function CommandBar({ open, onClose, commands = [], placeholder = 'Search or run a command…' }) {
  const [query, setQuery] = useState('');
  const filtered = useMemo(
    () => commands.filter((c) => `${c.label} ${c.description || ''} ${c.group || ''}`.toLowerCase().includes(query.toLowerCase())),
    [commands, query],
  );
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" PaperProps={{ sx: { bgcolor: '#111722', backgroundImage: 'none' } }}>
      <DialogContent sx={{ p: 2 }}>
        <Typography className="rig-label" sx={{ mb: 1 }}>Command</Typography>
        <TextField
          autoFocus fullWidth size="small" value={query} onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          InputProps={{ startAdornment: <SearchOutlined fontSize="small" sx={{ mr: 1, color: 'text.secondary' }} /> }}
        />
        <Stack spacing={0.5} sx={{ mt: 1.5, maxHeight: 320, overflow: 'auto' }}>
          {filtered.map((command, index) => (
            <Button
              key={command.id || index}
              onClick={() => { command.onSelect?.(); onClose?.(); }}
              sx={{ justifyContent: 'space-between', textTransform: 'none', color: 'text.primary' }}
            >
              <Box textAlign="left">
                <Typography fontWeight={700}>{command.label}</Typography>
                {command.description && <Typography variant="caption" color="text.secondary">{command.description}</Typography>}
              </Box>
              {command.shortcut && <kbd className="rig-mono">{command.shortcut}</kbd>}
            </Button>
          ))}
          {!filtered.length && <Typography color="text.secondary" sx={{ p: 2, textAlign: 'center' }}>No matches</Typography>}
        </Stack>
      </DialogContent>
    </Dialog>
  );
}

/** Toolbar */
export function Toolbar({ children, className = '', sx }) {
  return <Box className={`rig-toolbar ${className}`} role="toolbar" sx={sx}>{children}</Box>;
}

/** AuditSpine — last N decisions */
export function AuditSpine({ events = [], className = '', sx, tabIndex }) {
  return (
    <Box className={`rig-audit-spine ${className}`} sx={sx} role="status" aria-label="Audit spine" tabIndex={tabIndex}>
      <Typography className="rig-label" sx={{ flexShrink: 0 }}>Audit</Typography>
      <Box className="rig-audit-spine-track">
        {events.length
          ? events.map((event, index) => <AuditEvent key={event.id || index} {...event} />)
          : <Typography variant="caption" color="text.secondary">No recent decisions</Typography>}
      </Box>
    </Box>
  );
}

/** Dock — magnified quick actions (React Bits style) */
export function Dock({
  onCommand, onCopilot, onWorkspacePanel, onPin, className = '', sx,
}) {
  const items = [
    { icon: <SearchOutlined fontSize="small" />, label: 'Command', onClick: onCommand },
    { icon: <SmartToyOutlined fontSize="small" />, label: 'Copilot', onClick: onCopilot },
    { icon: <ViewSidebarOutlined fontSize="small" />, label: 'Panel', onClick: onWorkspacePanel },
    { icon: <PushPinOutlined fontSize="small" />, label: 'Pin', onClick: onPin },
  ].filter((item) => typeof item.onClick === 'function');

  return (
    <Box className={className} sx={sx}>
      <WorkspaceDock items={items} />
    </Box>
  );
}

/** UnitRiskMap — facility schematic with risk-tinted nodes */
export function UnitRiskMap({ units = [], onSelect, selectedId, className = '', sx }) {
  const positions = [
    { x: 18, y: 28 }, { x: 52, y: 22 }, { x: 78, y: 38 },
    { x: 28, y: 62 }, { x: 58, y: 68 }, { x: 82, y: 70 },
  ];
  return (
    <Box className={`rig-unit-risk-map ${className}`} sx={sx} role="list" aria-label="Unit risk map">
      <Typography className="rig-label rig-unit-risk-kicker">Facility risk map</Typography>
      <svg className="rig-unit-risk-svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden>
        <defs>
          <radialGradient id="rig-unit-glow" cx="50%" cy="40%" r="60%">
            <stop offset="0%" stopColor="rgba(38,132,255,0.18)" />
            <stop offset="100%" stopColor="rgba(10,13,18,0)" />
          </radialGradient>
        </defs>
        <rect width="100" height="100" fill="url(#rig-unit-glow)" />
        <path d="M12 48 H88 M35 20 V78 M65 18 V82" stroke="rgba(148,163,184,0.22)" strokeWidth="0.6" fill="none" />
        <path d="M20 35 Q50 28 80 42" stroke="rgba(88,216,255,0.2)" strokeWidth="0.5" fill="none" />
      </svg>
      {units.map((unit, index) => {
        const risk = Number(unit.risk ?? (100 - (unit.health ?? 100)));
        const status = normalizeStatus(unit.status) || (risk >= 70 ? 'critical' : risk >= 40 ? 'attention' : 'nominal');
        const t = resolveTone(status);
        const id = unit.id || unit.name || index;
        const pos = positions[index % positions.length];
        return (
          <Box
            component="button"
            type="button"
            key={id}
            role="listitem"
            className={`rig-unit-node ${selectedId === id ? 'is-selected' : ''} ${risk >= 40 ? 'is-risk' : ''}`}
            onClick={() => onSelect?.(unit)}
            style={{
              left: `${pos.x}%`,
              top: `${pos.y}%`,
              borderColor: `${t.main}88`,
              boxShadow: risk >= 40 ? `0 0 18px ${t.main}44` : undefined,
            }}
            aria-pressed={selectedId === id}
          >
            <Typography fontWeight={750} fontSize={12}>{unit.name || unit.label}</Typography>
            <Typography className="rig-mono" sx={{ fontSize: 10, color: t.main }}>
              {unit.health != null ? `${Math.round(unit.health)}%` : `${Math.round(risk)} risk`}
            </Typography>
          </Box>
        );
      })}
      {!units.length && <Typography color="text.secondary" sx={{ p: 2 }}>No units in scope</Typography>}
    </Box>
  );
}

/** DecisionQueue — prioritized list for Mission Control */
export function DecisionQueue({ items = [], onSelect, selectedId, className = '', sx }) {
  return (
    <Box className={`rig-decision-queue ${className}`} sx={sx} role="list" aria-label="Decision queue">
      {items.map((item, index) => {
        if (item.kind === 'incident' || item.severity) {
          return (
            <IncidentQueueItem
              key={item.id || index}
              {...item}
              selected={selectedId === item.id}
              onClick={() => onSelect?.(item)}
            />
          );
        }
        return (
          <ObjectRow
            key={item.id || index}
            name={item.title || item.name}
            status={item.status}
            secondaryId={item.id}
            selected={selectedId === item.id}
            onClick={() => onSelect?.(item)}
          />
        );
      })}
      {!items.length && <Typography color="text.secondary" sx={{ p: 1 }}>No pending decisions</Typography>}
    </Box>
  );
}

export { MetricCard };
