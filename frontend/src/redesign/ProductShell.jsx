import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Avatar, Badge, Box, Button, Dialog, Divider, IconButton, InputAdornment, Menu, MenuItem, Stack, TextField, Tooltip, Typography,
} from '@mui/material';
import {
  ArticleOutlined, BuildOutlined, ChevronLeftOutlined, ChevronRightOutlined, CloseOutlined, DashboardOutlined,
  DarkModeOutlined, DevicesOutlined, HistoryOutlined, LightModeOutlined, MemoryOutlined,
  NotificationsOutlined, PushPinOutlined, ScienceOutlined, SearchOutlined, SettingsOutlined, SmartToyOutlined,
  SyncOutlined, ViewSidebarOutlined, WarningAmberOutlined,
} from '@mui/icons-material';
import { AnimatePresence, LayoutGroup, motion, useReducedMotion } from 'motion/react';
import toast from 'react-hot-toast';
import { useColorMode } from '../context/ColorModeContext';
import { useOperations } from '../context/OperationsContext';
import { useObjectContext } from '../context/ObjectContext';
import { navigateTo, pathToWorkspace, WORKSPACE_LABELS } from '../context/objectNavigation';
import { markNotificationsRead } from '../api/client';
import { normalizeRefineryOptions, notificationPresentation } from '../api/resourceAdapters';
import { ScopeSwitcher } from '../design-system/catalog/shell';
import { AssistantPanel } from './AssistantPanel';
import './sync-control.css';
import './topbar-fixes.css';
import {
  AuditSpine, exportAuditLog, useOperatorAudit,
} from './accountability';

const nav = [
  ['Command Center', '/', DashboardOutlined, 'Overview', 'command'],
  ['Assets', '/assets', DevicesOutlined, 'Operations', 'assets'],
  ['Incidents', '/incident-simulator', WarningAmberOutlined, 'Operations', 'incidents'],
  ['Maintenance', '/maintenance', BuildOutlined, 'Operations', 'maintenance'],
  ['AI Investigation', '/agent-monitor', MemoryOutlined, 'Intelligence', 'investigation'],
  ['Forecasting', '/health-prediction', ScienceOutlined, 'Intelligence', 'forecasting'],
  ['Reports', '/reports', ArticleOutlined, 'Intelligence', 'reports'],
];
const label = (value = '') => String(value).replace(/[_-]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
const formatTime = (value) => (value ? new Date(value).toLocaleTimeString() : 'Live event');

/** Epic 4 — ProductShell wired to ObjectContext (scope, search, keyboard, breadcrumbs). */
export function ProductShell({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const reduced = useReducedMotion();
  const { mode, toggle } = useColorMode();
  const { operations = {}, ambient = {}, connected = false, refresh = async () => {} } = useOperations();
  const objectApi = useObjectContext();

  const [collapsed, setCollapsed] = useState(() => localStorage.getItem('rigos-nav-collapsed') === 'true');
  const [profileAnchor, setProfileAnchor] = useState(null);
  const [commandOpen, setCommandOpen] = useState(false);
  const [commandIndex, setCommandIndex] = useState(0);
  const [inboxOpen, setInboxOpen] = useState(false);
  const [inboxFilter, setInboxFilter] = useState('all');
  const [assistantOpen, setAssistantOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [clock, setClock] = useState(() => new Date());
  const [syncAge, setSyncAge] = useState(0);
  const auditSpineRef = useRef(null);
  const workspacePanelRef = useRef(null);
  const navRefs = useRef([]);

  const facility = objectApi.scope.facility || 'Enterprise view';
  const facilityOptions = useMemo(
    () => normalizeRefineryOptions(operations.refineries || []),
    [operations.refineries],
  );

  useEffect(() => {
    const liveRefineries = Array.isArray(operations.refineries) ? operations.refineries : [];
    if (!liveRefineries.length) return;
    if (!facilityOptions.some((option) => option.value === facility)) {
      objectApi.setFacility('Enterprise view');
    }
  }, [facility, facilityOptions, objectApi, operations.refineries]);

  const workspaceKey = pathToWorkspace(location.pathname);
  const current = nav.find((item) => item[1] === location.pathname) || nav[0];
  const workspacePanel = objectApi.ui.workspacePanelOpen;
  const pinned = objectApi.ui.pinnedRoutes || [];

  const notifications = Array.isArray(operations.notifications) ? operations.notifications : [];
  const unread = notifications.filter((item) => item && !item.read);
  const agentsWorking = Array.isArray(operations.investigation?.stages)
    ? operations.investigation.stages.filter((stage) => stage?.state === 'running').length
    : 0;
  const activeIncidents = Number(operations.dashboard?.active_incidents || 0);
  const aiLabel = !connected
    ? 'Syncing'
    : agentsWorking
      ? `${agentsWorking} agents active`
      : activeIncidents
        ? 'AI review queued'
        : 'AI monitoring';

  const auditEvents = useOperatorAudit(objectApi, operations);

  const commands = useMemo(() => {
    const items = [
      ...nav.map(([name, , Icon, group, workspace]) => ({
        label: name,
        group,
        icon: <Icon />,
        run: () => navigateTo(objectApi, navigate, workspace),
      })),
      { label: 'Open notifications', group: 'System', icon: <NotificationsOutlined />, run: () => setInboxOpen(true) },
      { label: 'Ask RigOS AI', group: 'System', icon: <SmartToyOutlined />, run: () => setAssistantOpen(true) },
      {
        label: mode === 'dark' ? 'Switch to light mode' : 'Switch to dark mode',
        group: 'System',
        icon: mode === 'dark' ? <LightModeOutlined /> : <DarkModeOutlined />,
        run: toggle,
      },
      {
        label: 'Export audit log',
        group: 'System',
        icon: <HistoryOutlined />,
        description: 'Download immutable decision trail (CSV)',
        run: () => exportAuditLog({ events: auditEvents, facility }),
      },
      {
        label: 'Toggle asset inspector',
        group: 'System',
        icon: <ViewSidebarOutlined />,
        description: 'Keyboard ] on Assets',
        run: () => {
          navigateTo(objectApi, navigate, 'assets');
          objectApi.patchUi?.({ inspectorCollapsed: !objectApi.ui?.inspectorCollapsed });
        },
      },
    ];

    const assets = operations.assets || [];
    const byId = new Map(assets.map((asset) => [asset.id, asset]));

    (objectApi.favorites?.assetIds || []).forEach((id) => {
      const asset = byId.get(id);
      if (!asset) return;
      items.push({
        label: asset.name || asset.id,
        group: 'Favorites',
        description: [asset.tag, asset.location || asset.zone].filter(Boolean).join(' · ') || asset.id,
        icon: <PushPinOutlined />,
        run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
      });
    });

    (objectApi.recent?.assetIds || []).slice(0, 10).forEach((id) => {
      const asset = byId.get(id);
      if (!asset) return;
      items.push({
        label: asset.name || asset.id,
        group: 'Recent',
        description: [asset.tag, asset.location || asset.zone].filter(Boolean).join(' · ') || asset.id,
        icon: <HistoryOutlined />,
        run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
      });
    });

    assets.forEach((asset) => {
      const tag = asset.tag || asset.id;
      items.push({
        label: asset.name || asset.id,
        group: 'Assets',
        description: [tag, asset.location || asset.zone, asset.type].filter(Boolean).join(' · '),
        icon: <DevicesOutlined />,
        run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
      });
      if (asset.tag && String(asset.tag) !== String(asset.name)) {
        items.push({
          label: String(asset.tag),
          group: 'Tags',
          description: asset.name || asset.id,
          icon: <DevicesOutlined />,
          run: () => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id }),
        });
      }
    });

    [...(operations.audit_logs || []), ...(operations.critical_incidents || [])]
      .filter((item, index, list) => list.findIndex((row) => row.id === item.id) === index)
      .slice(0, 30)
      .forEach((item) => {
        items.push({
          label: label(item.incident_type || item.title || item.id),
          group: 'Incidents',
          description: item.asset_name || item.asset_id || item.id,
          icon: <WarningAmberOutlined />,
          run: () => navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null }),
        });
      });

    (operations.maintenance?.tasks || []).slice(0, 20).forEach((task, index) => {
      const id = task.id || `wo-${index}`;
      items.push({
        label: task.title || task.Task || task.name || `Work order ${index + 1}`,
        group: 'Work orders',
        description: task.asset_name || task.Owner || id,
        icon: <BuildOutlined />,
        run: () => navigateTo(objectApi, navigate, 'maintenance', { workOrderId: id }),
      });
    });

    (operations.reports || []).slice(0, 15).forEach((report) => {
      items.push({
        label: report.title || report.name || report.id,
        group: 'Reports',
        description: report.created_at ? formatTime(report.created_at) : 'Executive brief',
        icon: <ArticleOutlined />,
        run: () => navigateTo(objectApi, navigate, 'reports', { reportId: report.id }),
      });
    });

    return items;
  }, [mode, navigate, objectApi, operations, toggle, auditEvents, facility]);

  const matches = commands.filter((item) => (
    `${item.label} ${item.group} ${item.description || ''}`.toLowerCase().includes(query.toLowerCase())
  ));

  useEffect(() => {
    const reset = window.setTimeout(() => setCommandIndex(0), 0);
    return () => window.clearTimeout(reset);
  }, [query, commandOpen]);

  useEffect(() => {
    const onKey = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setCommandOpen(true);
      }
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'j') {
        event.preventDefault();
        objectApi.toggleWorkspacePanel();
      }
      if ((event.metaKey || event.ctrlKey) && event.shiftKey && event.key.toLowerCase() === 'a') {
        event.preventDefault();
        auditSpineRef.current?.focus?.();
      }
      if (event.key === 'Escape') {
        setCommandOpen(false);
        objectApi.setWorkspacePanelOpen(false);
        setAssistantOpen(false);
      }
      if (commandOpen && matches.length) {
        if (event.key === 'ArrowDown') {
          event.preventDefault();
          setCommandIndex((value) => Math.min(matches.length - 1, value + 1));
        }
        if (event.key === 'ArrowUp') {
          event.preventDefault();
          setCommandIndex((value) => Math.max(0, value - 1));
        }
        if (event.key === 'Enter') {
          event.preventDefault();
          const command = matches[commandIndex];
          if (command) {
            command.run();
            setCommandOpen(false);
            setQuery('');
          }
        }
      }
    };
    addEventListener('keydown', onKey);
    return () => removeEventListener('keydown', onKey);
  }, [objectApi, commandOpen, matches, commandIndex]);

  /* Part 8 — focus trap while WorkspacePanel is open */
  useEffect(() => {
    if (!workspacePanel) return undefined;
    const root = workspacePanelRef.current;
    if (!root) return undefined;
    const focusables = () => [...root.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')]
      .filter((el) => !el.hasAttribute('disabled') && el.offsetParent !== null);
    const first = focusables()[0];
    first?.focus?.();
    const onKey = (event) => {
      if (event.key !== 'Tab') return;
      const items = focusables();
      if (!items.length) return;
      const firstEl = items[0];
      const lastEl = items[items.length - 1];
      if (event.shiftKey && document.activeElement === firstEl) {
        event.preventDefault();
        lastEl.focus();
      } else if (!event.shiftKey && document.activeElement === lastEl) {
        event.preventDefault();
        firstEl.focus();
      }
    };
    root.addEventListener('keydown', onKey);
    return () => root.removeEventListener('keydown', onKey);
  }, [workspacePanel]);

  const onNavKeyDown = (event, index) => {
    if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp' && event.key !== 'Home' && event.key !== 'End') return;
    event.preventDefault();
    const links = navRefs.current.filter(Boolean);
    if (!links.length) return;
    let next = index;
    if (event.key === 'ArrowDown') next = Math.min(links.length - 1, index + 1);
    if (event.key === 'ArrowUp') next = Math.max(0, index - 1);
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = links.length - 1;
    links[next]?.focus?.();
  };

  useEffect(() => {
    const reset = window.setTimeout(() => setSyncAge(0), 0);
    const timer = setInterval(() => {
      setClock(new Date());
      // Derive sync age from the OperationsContext lastUpdated timestamp when available
      const snapshotTs = ambient?.lastUpdated;
      if (snapshotTs && connected) {
        setSyncAge(Math.min(Math.round((Date.now() - snapshotTs) / 1000), 59));
      } else if (!connected) {
        setSyncAge((value) => Math.min(value + 1, 59));
      }
    }, 1000);
    return () => {
      window.clearTimeout(reset);
      clearInterval(timer);
    };
  }, [connected, operations.generated_at, ambient?.lastUpdated]);

  const updateCollapse = () => setCollapsed((value) => {
    localStorage.setItem('rigos-nav-collapsed', String(!value));
    return !value;
  });

  const openInbox = () => {
    setInboxOpen(true);
  };

  const markInboxRead = async (notificationIds = [], markAll = false) => {
    try {
      await markNotificationsRead({ notification_ids: notificationIds, mark_all: markAll });
      await refresh();
    } catch (error) {
      const detail = error?.response?.data?.detail;
      toast.error((typeof detail === 'string' ? detail : detail?.message) || 'Notification state could not be saved.');
    }
  };

  const groups = ['Overview', 'Operations', 'Intelligence', 'Assets', 'Incidents', 'Work orders', 'Reports', 'System'];

  return (
    <Box className={`os-app ${collapsed ? 'is-compact' : ''}`}>
      <LayoutGroup id="rig-os-navigation">
        <motion.aside
          layout
          transition={{ layout: reduced ? { duration: 0 } : { duration: 0.12, ease: 'easeOut' } }}
          className="os-sidebar"
        >
          <Box className="os-brand">
            <Box className="os-brand-mark">R</Box>
            {!collapsed && (
              <motion.div initial={{ opacity: 0, x: -6 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0 }}>
                <Typography>RIG OS</Typography>
                <Typography>OPERATIONS</Typography>
              </motion.div>
            )}
            <Tooltip title={collapsed ? 'Expand navigation' : 'Collapse navigation'} placement="right">
              <IconButton className="os-collapse" onClick={updateCollapse}>
                {collapsed ? <ChevronRightOutlined /> : <ChevronLeftOutlined />}
              </IconButton>
            </Tooltip>
          </Box>
          <nav className="os-nav" aria-label="Primary navigation">
            {['Overview', 'Operations', 'Intelligence'].map((group) => (
              <Box key={group} className="os-nav-group">
                {!collapsed && <Typography className="os-overline">{group}</Typography>}
                {nav.filter((item) => item[3] === group).map(([name, path, Icon, , workspace]) => {
                  const active = current[1] === path;
                  const flatIndex = nav.findIndex((item) => item[1] === path);
                  return (
                    <Tooltip key={path} title={collapsed ? name : ''} placement="right">
                      <Link
                        to={path}
                        className={active ? 'is-active' : ''}
                        ref={(node) => { navRefs.current[flatIndex] = node; }}
                        onKeyDown={(event) => onNavKeyDown(event, flatIndex)}
                        onClick={(event) => {
                          event.preventDefault();
                          navigateTo(objectApi, navigate, workspace);
                        }}
                      >
                        {active && (
                          <motion.span
                            className="os-active-pill"
                            layoutId="os-active-pill"
                            transition={{ duration: reduced ? 0 : 0.12, ease: 'easeOut' }}
                          />
                        )}
                        <Icon />
                        <AnimatePresence initial={false}>
                          {!collapsed && (
                            <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.12 }}>
                              {name}
                            </motion.span>
                          )}
                        </AnimatePresence>
                      </Link>
                    </Tooltip>
                  );
                })}
              </Box>
            ))}
          </nav>
          <Box className="os-sidebar-bottom">
            <Tooltip title={collapsed ? 'Settings' : ''} placement="right">
              <Button onClick={() => setProfileAnchor(document.querySelector('.os-profile'))} startIcon={<SettingsOutlined />}>
                {!collapsed && 'Settings'}
              </Button>
            </Tooltip>
            <Box className="os-connection">
              <motion.i
                animate={connected ? { opacity: [1, 0.5, 1] } : { opacity: [1, 0.35, 1] }}
                transition={{ repeat: Infinity, duration: connected ? 2.4 : 0.9 }}
              />
              {!collapsed && <Typography>{connected ? 'Live connection' : 'Reconnecting'}</Typography>}
            </Box>
          </Box>
        </motion.aside>
      </LayoutGroup>

      <Box className="os-stage">
        <a className="e6-skip-link" href="#main-content">Skip to main content</a>
        <header className="os-topbar" role="banner">
          <Stack className="os-topbar-primary" direction="row" spacing={1.25} sx={{ alignItems: 'center' }}>
            <Button className="os-command-trigger" onClick={() => setCommandOpen(true)} startIcon={<SearchOutlined />} endIcon={<kbd>⌘ K</kbd>} aria-label="Open command palette">
              <span className="os-command-label">Search assets, incidents, work orders…</span>
            </Button>
            <ScopeSwitcher
              className="os-facility-switcher"
              value={facility}
              options={facilityOptions}
              onChange={objectApi.setFacility}
            />
            <Box className="os-top-context">
              <Typography>{WORKSPACE_LABELS[workspaceKey] || current[0]}</Typography>
              <Typography>{facilityOptions.find((row) => row.value === facility)?.detail || facility}</Typography>
            </Box>
          </Stack>
          <Stack className="os-topbar-actions" direction="row" spacing={0.5} sx={{ alignItems: 'center' }}>
            <Box className="os-ambient">
              <Typography>{clock.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</Typography>
              <Typography>
                {connected
                  ? `${ambient?.telemetry?.value ?? '—'}${ambient?.telemetry?.unit ? ` ${ambient.telemetry.unit}` : ''} · synced ${syncAge}s ago`
                  : 'reconnecting telemetry'}
              </Typography>
            </Box>
            <Tooltip title={connected ? 'Telemetry synchronized' : 'Synchronizing telemetry'}>
              <Button
                className={`os-sync ${connected ? 'is-ready' : ''}`}
                onClick={() => { setSyncAge(0); refresh(); }}
                startIcon={(
                  <motion.span animate={connected ? false : { rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}>
                    <SyncOutlined />
                  </motion.span>
                )}
              >
                {connected ? 'Synced' : 'Syncing'}
              </Button>
            </Tooltip>
            <Tooltip title={aiLabel}>
              <Button className="os-ai-status" onClick={() => setAssistantOpen(true)} startIcon={<SmartToyOutlined />}>
                <motion.i animate={agentsWorking ? { opacity: [1, 0.45, 1] } : false} transition={{ repeat: Infinity, duration: 1.6 }} />
                {aiLabel}
              </Button>
            </Tooltip>
            <Tooltip title="Notifications">
              <IconButton onClick={openInbox} aria-label="Open notifications">
                <Badge badgeContent={unread.length} color="error"><NotificationsOutlined /></Badge>
              </IconButton>
            </Tooltip>
            <Button className="os-profile" onClick={(event) => setProfileAnchor(event.currentTarget)}>
              <Avatar>CO</Avatar>
              <Box>
                <Typography>Control operator</Typography>
                <Typography>Shift A</Typography>
              </Box>
            </Button>
          </Stack>
        </header>
        <main id="main-content" tabIndex={-1}>
          {children}
        </main>
        <Box
          ref={auditSpineRef}
          className="e5-audit-spine"
          tabIndex={-1}
          onKeyDown={(event) => {
            if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'e') {
              event.preventDefault();
              exportAuditLog({ events: auditEvents, facility });
            }
          }}
        >
          <AuditSpine events={auditEvents} />
          <Button size="small" onClick={() => exportAuditLog({ events: auditEvents, facility })} sx={{ flexShrink: 0, textTransform: 'none' }}>
            Export
          </Button>
        </Box>
      </Box>

      <Menu anchorEl={profileAnchor} open={Boolean(profileAnchor)} onClose={() => setProfileAnchor(null)} PaperProps={{ className: 'os-menu' }}>
        <MenuItem onClick={toggle}>{mode === 'dark' ? <LightModeOutlined /> : <DarkModeOutlined />} {mode === 'dark' ? 'Use light mode' : 'Use dark mode'}</MenuItem>
        <MenuItem onClick={() => { setProfileAnchor(null); setAssistantOpen(true); }}><SmartToyOutlined /> Ask RigOS AI</MenuItem>
      </Menu>

      <Dialog open={commandOpen} onClose={() => setCommandOpen(false)} fullWidth maxWidth="sm" PaperProps={{ className: 'product-dialog os-command-dialog' }}>
        <Box className="product-command">
          <TextField
            autoFocus
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search assets, incidents, work orders, reports…"
            fullWidth
            InputProps={{
              startAdornment: <InputAdornment position="start"><SearchOutlined /></InputAdornment>,
              endAdornment: <InputAdornment position="end"><IconButton onClick={() => setCommandOpen(false)}><CloseOutlined /></IconButton></InputAdornment>,
            }}
          />
          {groups.map((group) => matches.some((item) => item.group === group) && (
            <Box key={group}>
              <Typography className="product-dialog-label">{group}</Typography>
              {matches.filter((item) => item.group === group).slice(0, 8).map((command) => {
                const flatIndex = matches.indexOf(command);
                const active = flatIndex === commandIndex;
                return (
                  <Button
                    key={`${command.group}-${command.label}`}
                    className={`product-command-item${active ? ' is-active' : ''}`}
                    startIcon={command.icon}
                    onMouseEnter={() => setCommandIndex(flatIndex)}
                    onClick={() => { command.run(); setCommandOpen(false); setQuery(''); }}
                  >
                    <Box textAlign="left">
                      <Typography fontWeight={700}>{command.label}</Typography>
                      {command.description && <Typography variant="caption" color="text.secondary">{command.description}</Typography>}
                    </Box>
                  </Button>
                );
              })}
            </Box>
          ))}
          {!matches.length && <Typography sx={{ p: 2, textAlign: 'center' }} color="text.secondary">No matches</Typography>}
        </Box>
      </Dialog>

      <Dialog open={inboxOpen} onClose={() => setInboxOpen(false)} fullWidth maxWidth="md" PaperProps={{ className: 'product-dialog product-notification-dialog' }}>
        <Box className="product-inbox">
          <Stack className="notification-inbox-head" direction="row" sx={{ justifyContent: 'space-between' }}>
            <Box>
              <Typography className="product-dialog-label">OPERATOR INBOX</Typography>
              <Typography variant="h6">Operations signal center</Typography>
              <Typography variant="body2" color="text.secondary">{unread.length} unread · {notifications.length} recent events</Typography>
            </Box>
            <Stack direction="row" spacing={1} sx={{ alignItems: 'center' }}>
              {unread.length ? <Button size="small" onClick={() => markInboxRead([], true)}>Mark all read</Button> : null}
              <IconButton onClick={() => setInboxOpen(false)}><CloseOutlined /></IconButton>
            </Stack>
          </Stack>
          <Box className="notification-inbox-filters">
            {['all', 'unread', 'critical'].map((filter) => (
              <Button key={filter} className={inboxFilter === filter ? 'active' : ''} onClick={() => setInboxFilter(filter)}>
                {label(filter)}
              </Button>
            ))}
          </Box>
          <Divider />
          {notifications.filter((item) => (
            inboxFilter === 'unread' ? !item.read
              : inboxFilter === 'critical' ? /critical|warning/i.test(item.severity || '')
                : true
          )).length ? notifications.filter((item) => (
            inboxFilter === 'unread' ? !item.read
              : inboxFilter === 'critical' ? /critical|warning/i.test(item.severity || '')
                : true
          )).map((item, index) => {
            const presentation = notificationPresentation(item);
            return (
              <Box className={`product-notification severity-${item.severity || 'info'} ${item.read ? 'is-read' : 'is-unread'}`} key={item.id || index}>
                <Box className="notification-signal-icon">
                  {/critical|warning/i.test(item.severity || '') ? <WarningAmberOutlined /> : item.severity === 'success' ? <SyncOutlined /> : <NotificationsOutlined />}
                </Box>
                <Box className="notification-signal-copy">
                  <Stack direction="row" gap={1} sx={{ justifyContent: 'space-between' }}>
                    <Typography fontWeight={800}>{presentation.title}</Typography>
                    <Typography className={`notification-severity ${item.severity || 'info'}`}>{label(item.severity || 'info')}</Typography>
                  </Stack>
                  <Typography variant="body2">{presentation.detail}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {[label(item.severity || 'info'), formatTime(item.timestamp)].join(' · ')}
                  </Typography>
                </Box>
                <Stack className="notification-signal-actions" direction="row" spacing={0.5}>
                  {item.metadata?.work_order_id && (
                    <Button size="small" onClick={() => {
                      navigateTo(objectApi, navigate, 'maintenance', { workOrderId: item.metadata.work_order_id, assetId: item.asset_id || null });
                      setInboxOpen(false);
                    }}>Open work</Button>
                  )}
                  {item.metadata?.incident_id && (
                    <Button size="small" onClick={() => {
                      navigateTo(objectApi, navigate, 'incidents', { incidentId: item.metadata.incident_id, assetId: item.asset_id || null });
                      setInboxOpen(false);
                    }}>Open case</Button>
                  )}
                  {item.asset_id && (
                    <Button size="small" onClick={() => {
                      navigateTo(objectApi, navigate, 'assets', { assetId: item.asset_id });
                      setInboxOpen(false);
                    }}>Open asset</Button>
                  )}
                  {!item.read && <Button size="small" onClick={() => markInboxRead([item.id])}>Mark read</Button>}
                </Stack>
              </Box>
            );
          }) : (
            <Box className="product-inbox-empty">
              <NotificationsOutlined />
              <Typography fontWeight={700}>You’re all caught up</Typography>
            </Box>
          )}
        </Box>
      </Dialog>

      <Box className="workspace-dock" role="toolbar" aria-label="Workspace quick actions">
        <Tooltip title="Command palette (Ctrl K)"><IconButton onClick={() => setCommandOpen(true)}><SearchOutlined /></IconButton></Tooltip>
        <Tooltip title="AI copilot"><IconButton onClick={() => setAssistantOpen(true)}><SmartToyOutlined /></IconButton></Tooltip>
        <Tooltip title="Inspector and activity (Ctrl J)">
          <IconButton onClick={() => objectApi.toggleWorkspacePanel()}><ViewSidebarOutlined /></IconButton>
        </Tooltip>
        <Tooltip title="Pin current workspace">
          <IconButton
            onClick={() => {
              const entry = { label: current[0], path: current[1] };
              const next = pinned.some((item) => item.path === entry.path)
                ? pinned.filter((item) => item.path !== entry.path)
                : [...pinned, entry];
              objectApi.setPinnedRoutes(next);
            }}
          >
            <PushPinOutlined />
          </IconButton>
        </Tooltip>
      </Box>

      <AnimatePresence>
        {workspacePanel && (
          <motion.aside
            ref={workspacePanelRef}
            className="workspace-inspector is-open"
            data-focus-trap="true"
            role="dialog"
            aria-modal="true"
            aria-label="Workspace panel"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reduced ? 0 : 0.12, ease: 'easeOut' }}
          >
            <Stack direction="row" sx={{ justifyContent: 'space-between' }}>
              <Box>
                <Typography className="product-dialog-label">WORKSPACE PANEL</Typography>
                <Typography fontWeight={800}>{current[0]} · audit & notifications</Typography>
              </Box>
              <IconButton onClick={() => objectApi.setWorkspacePanelOpen(false)} aria-label="Close workspace panel"><CloseOutlined /></IconButton>
            </Stack>
            <Box className="workspace-inspector-section">
              <Typography className="product-kicker">PINNED CONTEXT</Typography>
              {pinned.length
                ? pinned.map((item) => <Button key={item.path} onClick={() => navigate(item.path)}>{item.label}</Button>)
                : <Typography variant="body2" color="text.secondary">Pin an operational workspace to keep it one action away.</Typography>}
            </Box>
            <Box className="workspace-inspector-section">
              <Typography className="product-kicker">RECENT ACTIVITY</Typography>
              <Stack spacing={1}>
                {(operations.audit_logs || []).slice(0, 4).map((item, index) => (
                  <Box
                    className="workspace-activity"
                    key={item.id || index}
                    component="button"
                    type="button"
                    onClick={() => navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null })}
                    style={{ all: 'unset', cursor: 'pointer', display: 'flex', gap: 8 }}
                  >
                    <HistoryOutlined />
                    <Box>
                      <Typography>{label(item.incident_type || item.action_type || 'Operational update')}</Typography>
                      <Typography>{formatTime(item.timestamp || item.created_at)}</Typography>
                    </Box>
                  </Box>
                ))}
                {!(operations.audit_logs || []).length && (
                  <Typography variant="body2" color="text.secondary">No recent audit events. Telemetry monitoring remains active.</Typography>
                )}
              </Stack>
            </Box>
            <Box className="workspace-inspector-section">
              <Typography className="product-kicker">QUICK ACTIONS</Typography>
              <Button onClick={() => setAssistantOpen(true)}>Ask AI about this workspace</Button>
              <Button onClick={() => setCommandOpen(true)}>Navigate or run a command</Button>
            </Box>
          </motion.aside>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {assistantOpen && (
          <motion.aside
            className="copilot-dock"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reduced ? 0 : 0.12, ease: 'easeOut' }}
          >
            <AssistantPanel onClose={() => setAssistantOpen(false)} />
          </motion.aside>
        )}
      </AnimatePresence>
    </Box>
  );
}
