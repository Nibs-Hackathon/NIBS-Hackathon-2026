# Folder: frontend/src/components/Shell Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/components/Shell`

Contains 1 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/components/Shell/ApplicationShell.jsx

**Folder path:** `frontend/src/components/Shell`

**File path:** `frontend/src/components/Shell/ApplicationShell.jsx`

```javascript
import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Avatar, Badge, Box, Button, Dialog, Divider, IconButton, InputAdornment, List, ListItemButton, ListItemIcon, ListItemText, Stack, TextField, Tooltip, Typography } from '@mui/material';
import { ArticleOutlined, DashboardOutlined, DevicesOutlined, KeyboardCommandKeyOutlined, LightModeOutlined, DarkModeOutlined, MemoryOutlined, NotificationsOutlined, ScienceOutlined, SensorsOutlined, SettingsOutlined, SearchOutlined, WarningAmberOutlined, BuildOutlined, CloseOutlined } from '@mui/icons-material';
import { useOperations } from '../../context/OperationsContext';
import { useColorMode } from '../../context/ColorModeContext';
import './shell.css';

const nav = [
  ['Overview', '/', DashboardOutlined], ['Assets', '/assets', DevicesOutlined], ['Incidents', '/incident-simulator', WarningAmberOutlined], ['Maintenance', '/maintenance', BuildOutlined],
  ['AI Investigation', '/agent-monitor', MemoryOutlined], ['Predictions', '/health-prediction', ScienceOutlined], ['Digital Twin', '/digital-twin', SensorsOutlined], ['Reports', '/reports', ArticleOutlined],
];

export function ApplicationShell({ children }) {
  const location = useLocation(); const navigate = useNavigate(); const { operations, connected } = useOperations(); const { mode, toggle } = useColorMode();
  const [palette, setPalette] = useState(false); const [inbox, setInbox] = useState(false); const [query, setQuery] = useState('');
  const current = nav.find((item) => item[1] === location.pathname) || nav[0];
  const state = !connected ? ['Recovering', 'warning'] : (operations.critical_incidents || []).length ? ['Investigating', 'warning'] : ['Healthy', 'success'];
  useEffect(() => { const handler = (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); setPalette(true); } if (event.key === 'Escape') setPalette(false); }; window.addEventListener('keydown', handler); return () => window.removeEventListener('keydown', handler); }, []);
  const matches = useMemo(() => nav.filter(([name]) => name.toLowerCase().includes(query.toLowerCase())), [query]);
  return <Box className="app-shell"><aside className="app-sidebar"><Box className="app-brand"><Box className="app-mark">R</Box><Box className="app-brand-copy"><Typography>RigOS</Typography><Typography>Enterprise Operations</Typography></Box></Box><Typography className="app-nav-label">Overview</Typography><List className="app-nav">{nav.slice(0, 1).map(([name, path, Icon]) => <NavItem key={path} name={name} path={path} Icon={Icon} active={path === current[1]} />)}</List><Typography className="app-nav-label">Operations</Typography><List className="app-nav">{nav.slice(1, 4).map(([name, path, Icon]) => <NavItem key={path} name={name} path={path} Icon={Icon} active={path === current[1]} />)}</List><Typography className="app-nav-label">Intelligence</Typography><List className="app-nav">{nav.slice(4).map(([name, path, Icon]) => <NavItem key={path} name={name} path={path} Icon={Icon} active={path === current[1]} />)}</List><Box className="app-sidebar-footer"><Divider /><Button startIcon={<SettingsOutlined />} fullWidth>Settings</Button></Box></aside><Box className="app-main"><header className="app-topbar"><Button className="app-search-trigger" onClick={() => setPalette(true)} startIcon={<SearchOutlined />} endIcon={<KeyboardCommandKeyOutlined />}>Search assets, incidents, reports…</Button><Stack direction="row" alignItems="center" spacing={1.25}><Box className={`app-system-state ${state[1]}`}><i />{state[0]}</Box><IconButton onClick={toggle}>{mode === 'dark' ? <LightModeOutlined /> : <DarkModeOutlined />}</IconButton><IconButton onClick={() => setInbox(true)}><Badge badgeContent={(operations.notifications || []).length} color="error"><NotificationsOutlined /></Badge></IconButton><Avatar className="app-avatar">C</Avatar><Box className="app-profile-copy"><Typography>Chief Operator</Typography><Typography>Facility Alpha</Typography></Box></Stack></header><main className="app-content"><Box className="app-context"><Typography>{current[0]}</Typography><Typography>Alpha Facility</Typography></Box>{children}</main></Box><Dialog open={palette} onClose={() => setPalette(false)} fullWidth maxWidth="sm" PaperProps={{ className: 'app-command-dialog' }}><Box className="app-command"><TextField autoFocus fullWidth value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search RigOS…" InputProps={{ startAdornment: <InputAdornment position="start"><SearchOutlined /></InputAdornment>, endAdornment: <InputAdornment position="end"><IconButton onClick={() => setPalette(false)}><CloseOutlined /></IconButton></InputAdornment> }} /><Stack sx={{ mt: 1 }}>{matches.map(([name, path, Icon]) => <Button key={path} startIcon={<Icon />} onClick={() => { navigate(path); setPalette(false); }} className="app-command-row">{name}</Button>)}</Stack></Box></Dialog><Dialog open={inbox} onClose={() => setInbox(false)} fullWidth maxWidth="xs" PaperProps={{ className: 'app-command-dialog' }}><Box className="app-inbox"><Stack direction="row" justifyContent="space-between"><Box><Typography className="app-overline">Notifications</Typography><Typography variant="h6">Operator inbox</Typography></Box><IconButton onClick={() => setInbox(false)}><CloseOutlined /></IconButton></Stack><Divider sx={{ my: 2 }} />{(operations.notifications || []).map((item, index) => <Box key={item.id || index} className="app-notification"><Typography fontWeight={700}>{item.title}</Typography><Typography variant="body2" color="text.secondary">{item.message}</Typography></Box>) || <Typography color="text.secondary">No new notifications.</Typography>}</Box></Dialog></Box>;
}

function NavItem({ name, path, Icon, active }) { return <Tooltip title={name} placement="right"><ListItemButton component={Link} to={path} className={active ? 'is-active' : ''}><ListItemIcon><Icon /></ListItemIcon><ListItemText primary={name} /></ListItemButton></Tooltip>; }
```
