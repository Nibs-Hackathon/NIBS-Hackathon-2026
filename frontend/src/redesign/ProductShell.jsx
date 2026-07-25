import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Avatar, Badge, Box, Button, Dialog, Divider, IconButton, InputAdornment, Stack, TextField, Tooltip, Typography } from '@mui/material';
import { ArticleOutlined, BuildOutlined, CloseOutlined, DashboardOutlined, DarkModeOutlined, DevicesOutlined, KeyboardCommandKeyOutlined, LightModeOutlined, MemoryOutlined, NotificationsOutlined, ScienceOutlined, SearchOutlined, SettingsOutlined, SmartToyOutlined, WarningAmberOutlined } from '@mui/icons-material';
import { useColorMode } from '../context/ColorModeContext';
import { useOperations } from '../context/OperationsContext';
import { markNotificationsRead } from '../api/client';
import { AssistantPanel } from './AssistantPanel';

const nav = [
  ['Command Center', '/', DashboardOutlined, 'Navigate'], ['Assets', '/assets', DevicesOutlined, 'Navigate'],
  ['Incidents', '/incident-simulator', WarningAmberOutlined, 'Navigate'], ['Maintenance', '/maintenance', BuildOutlined, 'Navigate'],
  ['AI Investigation', '/agent-monitor', MemoryOutlined, 'Navigate'], ['Forecasting', '/health-prediction', ScienceOutlined, 'Navigate'],
  ['Reports', '/reports', ArticleOutlined, 'Navigate'],
];

export function ProductShell({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { mode, toggle } = useColorMode();
  const { operations, connected, refresh } = useOperations();
  const [expanded, setExpanded] = useState(false);
  const [commandOpen, setCommandOpen] = useState(false);
  const [inboxOpen, setInboxOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [assistantOpen, setAssistantOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [facility, setFacility] = useState(() => localStorage.getItem('rigos-facility') || 'Portfolio view');

  const current = nav.find((item) => item[1] === location.pathname) || nav[0];
  const notifications = operations.notifications || [];
  const unread = notifications.filter((item) => !item.read);
  const activeIncidents = Number(operations.dashboard?.active_incidents || 0);
  const fleetHealth = Number(operations.dashboard?.fleet_health || 0);
  const systemLabel = !connected ? 'Synchronizing' : activeIncidents > 0 ? 'Investigating' : fleetHealth && fleetHealth < 80 ? 'Needs review' : 'System healthy';
  const systemTone = !connected || activeIncidents > 0 || (fleetHealth && fleetHealth < 80) ? 'warn' : 'ok';

  const commands = useMemo(() => [
    ...nav.map(([label, path, Icon, group]) => ({ label, group, icon: <Icon />, run: () => navigate(path) })),
    { label: mode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode', group: 'Workspace', icon: mode === 'dark' ? <LightModeOutlined /> : <DarkModeOutlined />, run: toggle },
    { label: 'Open notifications', group: 'Workspace', icon: <NotificationsOutlined />, run: () => setInboxOpen(true) },
    { label: 'Open settings', group: 'Workspace', icon: <SettingsOutlined />, run: () => setSettingsOpen(true) },
    { label: 'Ask RigOS AI', group: 'AI', icon: <SmartToyOutlined />, run: () => setAssistantOpen(true) },
  ], [mode, navigate, toggle]);
  const matches = commands.filter((item) => `${item.label} ${item.group}`.toLowerCase().includes(query.toLowerCase()));

  useEffect(() => {
    const onKey = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); setCommandOpen(true); }
      if (event.key === 'Escape') setCommandOpen(false);
    };
    addEventListener('keydown', onKey);
    return () => removeEventListener('keydown', onKey);
  }, []);

  const execute = (command) => { command.run(); setCommandOpen(false); setQuery(''); };
  const markInboxRead = async () => { try { await markNotificationsRead({ mark_all: true }); await refresh(); } catch { /* REST polling retries safely. */ } };
  const openInbox = async () => { setInboxOpen(true); if (unread.length) await markInboxRead(); };

  return <Box className={`product-app ${expanded ? 'nav-open' : ''}`}>
    <aside className="product-nav" onMouseEnter={() => setExpanded(true)} onMouseLeave={() => setExpanded(false)}>
      <Box className="product-logo"><Box>R</Box><Typography>RigOS</Typography></Box>
      <Stack className="product-nav-stack">{nav.map(([name, path, Icon]) => <Tooltip key={path} title={expanded ? '' : name} placement="right"><Link to={path} className={path === current[1] ? 'active' : ''}><Icon /><span>{name}</span></Link></Tooltip>)}</Stack>
      <Button className="product-settings" onClick={() => setSettingsOpen(true)} startIcon={<SettingsOutlined />}><span>Settings</span></Button>
    </aside>
    <Box className="product-stage">
      <header className="product-top">
        <Button className="product-search" onClick={() => setCommandOpen(true)} startIcon={<SearchOutlined />} endIcon={<KeyboardCommandKeyOutlined />}>Search assets, incidents, knowledge…</Button>
        <Stack direction="row" alignItems="center" spacing={1.4}>
          <Box className={`product-live ${systemTone}`}><i />{systemLabel}</Box>
          <IconButton onClick={() => setAssistantOpen(true)} aria-label="Open AI assistant"><SmartToyOutlined /></IconButton>
          <IconButton onClick={toggle} aria-label="Change theme">{mode === 'dark' ? <LightModeOutlined /> : <DarkModeOutlined />}</IconButton>
          <IconButton onClick={openInbox} aria-label="Open notifications"><Badge badgeContent={unread.length} color="error"><NotificationsOutlined /></Badge></IconButton>
          <Avatar>CO</Avatar>
        </Stack>
      </header>
      <main><Box className="product-crumb"><Typography>{current[0]}</Typography><Typography>{facility}</Typography></Box>{children}</main>
    </Box>
    <Dialog open={commandOpen} onClose={() => setCommandOpen(false)} fullWidth maxWidth="sm" PaperProps={{ className: 'product-dialog' }}><Box className="product-command"><TextField autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Type a command or search…" fullWidth InputProps={{ startAdornment: <InputAdornment position="start"><SearchOutlined /></InputAdornment>, endAdornment: <InputAdornment position="end"><IconButton onClick={() => setCommandOpen(false)}><CloseOutlined /></IconButton></InputAdornment> }} />{['Navigate', 'Workspace', 'AI'].map((group) => <Box key={group}>{matches.some((item) => item.group === group) && <><Typography className="product-dialog-label">{group}</Typography>{matches.filter((item) => item.group === group).map((command) => <Button key={command.label} className="product-command-item" startIcon={command.icon} onClick={() => execute(command)}>{command.label}</Button>)}</>}</Box>)}</Box></Dialog>
    <Dialog open={inboxOpen} onClose={() => setInboxOpen(false)} fullWidth maxWidth="sm" PaperProps={{ className: 'product-dialog product-notification-dialog' }}><Box className="product-inbox"><Stack direction="row" justifyContent="space-between" alignItems="start"><Box><Typography className="product-dialog-label">OPERATOR INBOX</Typography><Typography variant="h6">Live notifications</Typography><Typography variant="body2" color="text.secondary">{notifications.length ? 'The latest incident impact and AI workflow activity.' : 'No new operational events.'}</Typography></Box><IconButton onClick={() => setInboxOpen(false)}><CloseOutlined /></IconButton></Stack><Divider sx={{ my: 2 }} />{notifications.length ? notifications.map((item, index) => <Box className="product-notification" key={item.id || index}><Stack direction="row" justifyContent="space-between" gap={1}><Typography fontWeight={800}>{item.title}</Typography><Typography className={`notification-severity ${item.severity}`}>{item.severity}</Typography></Stack><Typography variant="body2">{item.message}</Typography><Typography variant="caption" color="text.secondary">{[item.asset_name || item.asset_id, item.incident_type, item.human_approval_required ? 'Operator review required' : null].filter(Boolean).join(' · ') || 'Facility event'} · {item.timestamp ? new Date(item.timestamp).toLocaleTimeString() : 'Live event'}</Typography></Box>) : <EmptyNotifications />}</Box></Dialog>
    <Dialog open={settingsOpen} onClose={() => setSettingsOpen(false)} fullWidth maxWidth="xs" PaperProps={{ className: 'product-dialog' }}><Box className="product-inbox"><Stack direction="row" justifyContent="space-between"><Box><Typography className="product-dialog-label">WORKSPACE</Typography><Typography variant="h6">Settings</Typography></Box><IconButton onClick={() => setSettingsOpen(false)}><CloseOutlined /></IconButton></Stack><Divider sx={{ my: 2 }} /><Typography variant="caption" color="text.secondary">CURRENT VIEW LABEL</Typography><TextField value={facility} onChange={(event) => setFacility(event.target.value)} fullWidth size="small" sx={{ mt: .7 }} /><Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mt: 2.5 }}><Box><Typography fontWeight={700}>Appearance</Typography><Typography variant="body2" color="text.secondary">{mode === 'dark' ? 'Dark' : 'Light'} mode</Typography></Box><Button onClick={toggle}>{mode === 'dark' ? 'Use light' : 'Use dark'}</Button></Stack><Button fullWidth variant="contained" sx={{ mt: 2.5 }} onClick={() => { localStorage.setItem('rigos-facility', facility); setSettingsOpen(false); }}>Save workspace</Button></Box></Dialog>
    <Dialog open={assistantOpen} onClose={() => setAssistantOpen(false)} fullWidth maxWidth="sm" PaperProps={{ className: 'product-dialog' }}><AssistantPanel onClose={() => setAssistantOpen(false)} /></Dialog>
  </Box>;
}

function EmptyNotifications() { return <Box className="product-inbox-empty"><NotificationsOutlined /><Typography fontWeight={700}>You’re all caught up</Typography><Typography variant="body2" color="text.secondary">New incidents and AI workflow updates will appear here.</Typography></Box>; }
