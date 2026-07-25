# Folder: frontend/src Code Inventory

Generated: 2026-07-25T06:14:25 UTC

Contains 19 project files.

## frontend/src/api/client.js

**Folder path:** `frontend/src/api`

**File path:** `frontend/src/api/client.js`

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response [${response.config.url}]:`, response.data);
    return response;
  },
  (error) => {
    console.error(`❌ API Error [${error.config?.url}]:`, error.message);
    return Promise.reject(error);
  }
);

// ============================================
// ASSETS
// ============================================
export const getAssets = () => api.get('/assets');
export const getAssetHealth = (assetId) => api.get(`/assets/${assetId}`);

// ============================================
// TELEMETRY
// ============================================
export const getTelemetry = (assetId, limit = 30) =>
  api.get(`/telemetry/${assetId}?limit=${limit}`);

// ============================================
// INCIDENTS
// ============================================
export const getIncidents = () => api.get('/incidents');
export const triggerIncident = (type) =>
  api.post(`/incidents/${encodeURIComponent(type)}`);

// ============================================
// AGENTS
// ============================================
export const getAgents = () => api.get('/agents');
export const getAgentMetrics = () => api.get('/agent-metrics');
export const getAgentActivity = () => api.get('/agent-activity');

// ============================================
// MAINTENANCE
// ============================================
export const getMaintenancePlan = () => api.get('/maintenance');

// ============================================
// PREDICTIONS
// ============================================
export const getPredictions = (assetId, horizon = 14) =>
  api.get(`/predictions/${assetId}?horizon=${horizon}`);

// ============================================
// DASHBOARD
// ============================================
export const getDashboard = () => api.get('/dashboard');

// ============================================
// REPORTS
// ============================================
export const getReports = () => api.get('/reports');

// ============================================
// DIGITAL TWIN
// ============================================
export const getTwinAssets = () => api.get('/twin-assets');

export default api;
```

## frontend/src/App.css

**Folder path:** `frontend/src`

**File path:** `frontend/src/App.css`

```css
.counter {
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 5px;
  color: var(--accent);
  background: var(--accent-bg);
  border: 2px solid transparent;
  transition: border-color 0.3s;
  margin-bottom: 24px;

  &:hover {
    border-color: var(--accent-border);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

.hero {
  position: relative;

  .base,
  .framework,
  .vite {
    inset-inline: 0;
    margin: 0 auto;
  }

  .base {
    width: 170px;
    position: relative;
    z-index: 0;
  }

  .framework,
  .vite {
    position: absolute;
  }

  .framework {
    z-index: 1;
    top: 34px;
    height: 28px;
    transform: perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg)
      scale(1.4);
  }

  .vite {
    z-index: 0;
    top: 107px;
    height: 26px;
    width: auto;
    transform: perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg)
      scale(0.8);
  }
}

#center {
  display: flex;
  flex-direction: column;
  gap: 25px;
  place-content: center;
  place-items: center;
  flex-grow: 1;

  @media (max-width: 1024px) {
    padding: 32px 20px 24px;
    gap: 18px;
  }
}

#next-steps {
  display: flex;
  border-top: 1px solid var(--border);
  text-align: left;

  & > div {
    flex: 1 1 0;
    padding: 32px;
    @media (max-width: 1024px) {
      padding: 24px 20px;
    }
  }

  .icon {
    margin-bottom: 16px;
    width: 22px;
    height: 22px;
  }

  @media (max-width: 1024px) {
    flex-direction: column;
    text-align: center;
  }
}

#docs {
  border-right: 1px solid var(--border);

  @media (max-width: 1024px) {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
}

#next-steps ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 8px;
  margin: 32px 0 0;

  .logo {
    height: 18px;
  }

  a {
    color: var(--text-h);
    font-size: 16px;
    border-radius: 6px;
    background: var(--social-bg);
    display: flex;
    padding: 6px 12px;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    transition: box-shadow 0.3s;

    &:hover {
      box-shadow: var(--shadow);
    }
    .button-icon {
      height: 18px;
      width: 18px;
    }
  }

  @media (max-width: 1024px) {
    margin-top: 20px;
    flex-wrap: wrap;
    justify-content: center;

    li {
      flex: 1 1 calc(50% - 8px);
    }

    a {
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
    }
  }
}

#spacer {
  height: 88px;
  border-top: 1px solid var(--border);
  @media (max-width: 1024px) {
    height: 48px;
  }
}

.ticks {
  position: relative;
  width: 100%;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: -4.5px;
    border: 5px solid transparent;
  }

  &::before {
    left: 0;
    border-left-color: var(--border);
  }
  &::after {
    right: 0;
    border-right-color: var(--border);
  }
}
```

## frontend/src/App.jsx

**Folder path:** `frontend/src`

**File path:** `frontend/src/App.jsx`

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Toaster } from 'react-hot-toast';
import { theme } from './styles/theme';
import { Layout } from './components/Layout/Layout';
import { useWebSocket } from './hooks/useWebSocket';
import { useEffect } from 'react';
import toast from 'react-hot-toast';

// Pages
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import IncidentSimulator from './pages/IncidentSimulator';
import AgentMonitor from './pages/AgentMonitor';
import AIActivity from './pages/AIActivity';
import MaintenancePlanner from './pages/MaintenancePlanner';
import HealthPrediction from './pages/HealthPrediction';
import DigitalTwin from './pages/DigitalTwin';
import Reports from './pages/Reports';

function App() {
  const { data } = useWebSocket();

  // ✅ Show toast notifications when incidents happen
  useEffect(() => {
    if (data?.notifications && data.notifications.length > 0) {
      const latest = data.notifications[0];
      const emoji = {
        critical: '🔴',
        warning: '🟠',
        success: '🟢',
        info: '🔵',
      }[latest.severity] || '🔵';
      
      toast(`${emoji} ${latest.title}`, {
        duration: 4000,
        icon: emoji,
        style: {
          background: '#0d1728',
          color: '#e8f0ff',
          border: '1px solid #55D6FF33',
          borderRadius: '8px',
          padding: '10px 14px',
          maxWidth: '340px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
        },
      });
    }
  }, [data]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#0d1728',
            color: '#e8f0ff',
            border: '1px solid #55D6FF33',
            borderRadius: '8px',
            padding: '10px 14px',
            maxWidth: '340px',
            boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
          },
        }}
      />
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/incident-simulator" element={<IncidentSimulator />} />
            <Route path="/agent-monitor" element={<AgentMonitor />} />
            <Route path="/ai-activity" element={<AIActivity />} />
            <Route path="/maintenance" element={<MaintenancePlanner />} />
            <Route path="/health-prediction" element={<HealthPrediction />} />
            <Route path="/digital-twin" element={<DigitalTwin />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
```

## frontend/src/components/Layout/Header.jsx

**Folder path:** `frontend/src/components/Layout`

**File path:** `frontend/src/components/Layout/Header.jsx`

```jsx
import { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Badge,
  Chip,
} from '@mui/material';
import { Menu, NotificationsOutlined, FiberManualRecord } from '@mui/icons-material';

export function Header({ drawerWidth }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <AppBar
      position="fixed"
      sx={{
        width: { sm: `calc(100% - ${drawerWidth}px)` },
        ml: { sm: `${drawerWidth}px` },
        background: 'rgba(10, 15, 26, 0.92)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid rgba(56, 78, 112, 0.08)',
        boxShadow: 'none',
      }}
    >
      <Toolbar sx={{ minHeight: 56, justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => setMobileOpen(!mobileOpen)}
            sx={{ display: { sm: 'none' }, color: '#8899B4' }}
          >
            <Menu />
          </IconButton>

          <Typography
            variant="h6"
            noWrap
            sx={{
              color: '#E8EDF5',
              fontWeight: 600,
              letterSpacing: '-0.02em',
              fontSize: '1rem',
              display: { xs: 'none', sm: 'block' },
            }}
          >
            RIGOS
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Chip
            icon={<FiberManualRecord sx={{ fontSize: 10, color: '#10B981' }} />}
            label="OPERATIONAL"
            size="small"
            sx={{
              bgcolor: 'rgba(16, 185, 129, 0.08)',
              color: '#10B981',
              border: '1px solid rgba(16, 185, 129, 0.15)',
              fontWeight: 500,
              fontSize: '0.65rem',
              height: 24,
              '& .MuiChip-label': { px: 1.5 },
              display: { xs: 'none', sm: 'flex' },
            }}
          />

          <IconButton color="inherit" sx={{ color: '#8899B4' }}>
            <Badge badgeContent={0} color="error" sx={{ '& .MuiBadge-badge': { bgcolor: '#EF4444', fontSize: 9, height: 16, minWidth: 16 } }}>
              <NotificationsOutlined sx={{ fontSize: 20 }} />
            </Badge>
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
```

## frontend/src/components/Layout/Layout.jsx

**Folder path:** `frontend/src/components/Layout`

**File path:** `frontend/src/components/Layout/Layout.jsx`

```jsx
import { Box } from '@mui/material';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

const drawerWidth = 240;

export function Layout({ children }) {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Header drawerWidth={drawerWidth} />
      <Sidebar drawerWidth={drawerWidth} />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          ml: { sm: `${drawerWidth}px` },
          background: 'radial-gradient(circle at 85% -10%, #182e52 0, #0b1220 34%, #070b13 72%)',
          minHeight: '100vh',
        }}
      >
        {children}
      </Box>
    </Box>
  );
}
```

## frontend/src/components/Layout/Sidebar.jsx

**Folder path:** `frontend/src/components/Layout`

**File path:** `frontend/src/components/Layout/Sidebar.jsx`

```jsx
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
  Toolbar,
} from '@mui/material';
import {
  DashboardOutlined,
  DevicesOutlined,
  WarningOutlined,
  MemoryOutlined,
  TimelineOutlined,
  SettingsOutlined,
  ScienceOutlined,
  SensorsOutlined,
  DescriptionOutlined,
} from '@mui/icons-material';
import { Link, useLocation } from 'react-router-dom';

const menuItems = [
  { text: 'Dashboard', icon: <DashboardOutlined />, path: '/' },
  { text: 'Assets', icon: <DevicesOutlined />, path: '/assets' },
  { text: 'Incident Simulator', icon: <WarningOutlined />, path: '/incident-simulator' },
  { text: 'Agent Monitor', icon: <MemoryOutlined />, path: '/agent-monitor' },
  { text: 'AI Activity', icon: <TimelineOutlined />, path: '/ai-activity' },
  { text: 'Maintenance Planner', icon: <SettingsOutlined />, path: '/maintenance' },
  { text: 'Health Prediction', icon: <ScienceOutlined />, path: '/health-prediction' },
  { text: 'Digital Twin', icon: <SensorsOutlined />, path: '/digital-twin' },
  { text: 'Reports', icon: <DescriptionOutlined />, path: '/reports' },
];


export function Sidebar({ drawerWidth }) {
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        display: { xs: 'none', sm: 'block' },
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          background: 'rgba(10, 15, 26, 0.98)',
          borderRight: '1px solid rgba(56, 78, 112, 0.08)',
        },
      }}
    >
      <Toolbar />
      <Box sx={{ p: 2.5, borderBottom: '1px solid rgba(56, 78, 112, 0.08)' }}>
        <Typography
          variant="h6"
          sx={{
            color: '#E8EDF5',
            fontWeight: 600,
            letterSpacing: '-0.02em',
            fontSize: '1.1rem',
          }}
        >
          RIGOS
        </Typography>
        <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.12em', fontSize: '0.6rem' }}>
          Operations Center
        </Typography>
      </Box>

      <List sx={{ mt: 1, px: 1 }}>
        {menuItems.map((item) => {
          const active = location.pathname === item.path;
          return (
            <ListItem
              component={Link}
              to={item.path}
              key={item.text}
              sx={{
                borderRadius: '6px',
                mb: 0.5,
                py: 1.2,
                px: 2,
                background: active ? 'rgba(59, 130, 246, 0.08)' : 'transparent',
                borderLeft: active ? '2px solid #3B82F6' : '2px solid transparent',
                '&:hover': {
                  background: 'rgba(59, 130, 246, 0.04)',
                },
              }}
            >
              <ListItemIcon
                sx={{
                  color: active ? '#3B82F6' : '#5A6B8A',
                  minWidth: 36,
                  '& svg': { fontSize: 20 },
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                sx={{
                  '& .MuiTypography-root': {
                    color: active ? '#E8EDF5' : '#8899B4',
                    fontWeight: active ? 500 : 400,
                    fontSize: '0.85rem',
                  },
                }}
              />
            </ListItem>
          );
        })}
      </List>

      <Box sx={{ p: 2.5, mt: 'auto', borderTop: '1px solid rgba(56, 78, 112, 0.08)' }}>
        <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', fontSize: '0.65rem' }}>
          RIGOS v2.0
        </Typography>
        <Typography variant="caption" sx={{ color: '#3A4B6A', fontSize: '0.6rem' }}>
          AI Operations Platform
        </Typography>
      </Box>
    </Drawer>
  );
}
```

## frontend/src/hooks/useWebSocket.js

**Folder path:** `frontend/src/hooks`

**File path:** `frontend/src/hooks/useWebSocket.js`

```javascript
import { useEffect, useState, useRef } from 'react';
import { toast } from 'react-hot-toast';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export function useWebSocket() {
  const [connected, setConnected] = useState(false);
  const [data, setData] = useState(null);
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      socketRef.current = new WebSocket(WS_URL);

      socketRef.current.onopen = () => {
        console.log('✅ WebSocket connected');
        setConnected(true);
        toast.success('Connected to RigOS', { duration: 2000 });
      };

      socketRef.current.onclose = () => {
        console.log('❌ WebSocket disconnected');
        setConnected(false);
        // Attempt reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      };

      socketRef.current.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'update') {
            setData(payload.data);
          }
        } catch (e) {
          console.error('WebSocket parse error:', e);
        }
      };
    };

    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  return { connected, data };
}
```

## frontend/src/index.css

**Folder path:** `frontend/src`

**File path:** `frontend/src/index.css`

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: #0b1220;
  color: #e8f0ff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(85, 214, 255, 0.25);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(85, 214, 255, 0.4);
}

/* Toast overrides */
.go3455832932 {
  background: #0d1728 !important;
  color: #e8f0ff !important;
  border: 1px solid rgba(85, 214, 255, 0.15) !important;
  border-radius: 10px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
  backdrop-filter: blur(12px) !important;
}

/* Animated glow for live indicator */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.live-dot {
  animation: pulse 2s ease-in-out infinite;
}

/* Glass morphism */
.glass {
  background: rgba(15, 27, 47, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(129, 172, 226, 0.1);
}

/* Loading shimmer */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

## frontend/src/main.jsx

**Folder path:** `frontend/src`

**File path:** `frontend/src/main.jsx`

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## frontend/src/pages/AgentMonitor.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/AgentMonitor.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  CircularProgress,
  useTheme,
} from '@mui/material';
import {
  Memory,
  CheckCircle,
  Warning,
  Error as ErrorIcon,  // ✅ Rename to avoid conflict
  Circle,
} from '@mui/icons-material';
import { getAgents, getAgentMetrics } from '../api/client';

// ✅ Rest of the code stays the same, but use ErrorIcon instead of Error
const getStatusIcon = (status) => {
  const icons = {
    'Active': <Circle sx={{ fontSize: 10, color: '#10B981' }} />,
    'Ready': <Circle sx={{ fontSize: 10, color: '#3B82F6' }} />,
    'Running': <CircularProgress size={12} sx={{ color: '#F59E0B' }} />,
    'Completed': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
    'Failed': <ErrorIcon sx={{ fontSize: 14, color: '#EF4444' }} />,  // ✅ Use ErrorIcon
    'Queued': <Warning sx={{ fontSize: 14, color: '#8B5CF6' }} />,
  };
  return icons[status] || <Circle sx={{ fontSize: 10, color: '#8899B4' }} />;
};

const AGENT_COLORS = {
  'Active': '#10B981',
  'Ready': '#3B82F6',
  'Running': '#F59E0B',
  'Completed': '#10B981',
  'Failed': '#EF4444',
  'Queued': '#8B5CF6',
};

// ✅ Mock data for when API fails
const MOCK_AGENTS = [
  { name: 'Safety', specialty: 'Risk validation', status: 'Active', confidence: '96%', currentTask: 'Checking assets' },
  { name: 'Diagnostic', specialty: 'Root cause analysis', status: 'Active', confidence: '95%', currentTask: 'Analyzing patterns' },
  { name: 'Knowledge', specialty: 'SOP retrieval', status: 'Ready', confidence: '93%', currentTask: 'Awaiting request' },
  { name: 'Maintenance', specialty: 'Maintenance planning', status: 'Ready', confidence: '94%', currentTask: 'Awaiting task' },
  { name: 'Planning', specialty: 'Recovery planning', status: 'Queued', confidence: '92%', currentTask: 'Preparing plan' },
  { name: 'Prediction', specialty: 'Failure prediction', status: 'Active', confidence: '91%', currentTask: 'Analyzing telemetry' },
  { name: 'Notification', specialty: 'Alerting', status: 'Ready', confidence: '95%', currentTask: 'Monitoring' },
  { name: 'Report', specialty: 'Report generation', status: 'Active', confidence: '94%', currentTask: 'Compiling data' },
];

const MOCK_METRICS = [
  { label: 'Agents online', value: '8 / 8', desc: 'All operational' },
  { label: 'Tasks active', value: '3', desc: 'In progress' },
  { label: 'Avg. confidence', value: '94.2%', desc: 'High accuracy' },
  { label: 'Decisions today', value: '24', desc: '8 per hour' },
];

export default function AgentMonitor() {
  const [agents, setAgents] = useState(MOCK_AGENTS);
  const [metrics, setMetrics] = useState(MOCK_METRICS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      // ✅ Use Promise.race with timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 5000)
      );
      
      const agentsPromise = getAgents();
      const metricsPromise = getAgentMetrics();
      
      const [agentsRes, metricsRes] = await Promise.race([
        Promise.all([agentsPromise, metricsPromise]),
        timeoutPromise.then(() => { throw new Error('Request timeout') })
      ]).catch(() => {
        // ✅ If timeout, use mock data
        console.log('Using mock agent data due to timeout');
        return [null, null];
      });
      
      if (agentsRes?.data) {
        setAgents(agentsRes.data);
      }
      if (metricsRes?.data) {
        setMetrics(metricsRes.data);
      }
    } catch (e) {
      console.error('Failed to load agent data, using mock data:', e);
      // Already using mock data from state
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    return AGENT_COLORS[status] || '#8899B4';
  };

  const getStatusIcon = (status) => {
    const icons = {
      'Active': <Circle sx={{ fontSize: 10, color: '#10B981' }} />,
      'Ready': <Circle sx={{ fontSize: 10, color: '#3B82F6' }} />,
      'Running': <CircularProgress size={12} sx={{ color: '#F59E0B' }} />,
      'Completed': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
      'Failed': <Error sx={{ fontSize: 14, color: '#EF4444' }} />,
      'Queued': <Warning sx={{ fontSize: 14, color: '#8B5CF6' }} />,
    };
    return icons[status] || <Circle sx={{ fontSize: 10, color: '#8899B4' }} />;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading agents...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Agent Monitor
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {agents.length} agents · {agents.filter(a => a.status === 'Active').length} active
          </Typography>
        </Box>
        <Chip
          label="● LIVE"
          sx={{ bgcolor: 'rgba(16,185,129,0.08)', color: '#10B981', border: '1px solid rgba(16,185,129,0.15)' }}
        />
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={6} sm={3} key={index}>
            <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
              <CardContent sx={{ py: 1.5 }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                  {metric.label || 'Metric'}
                </Typography>
                <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                  {metric.value || '0'}
                </Typography>
                <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.6rem' }}>
                  {metric.desc || ''}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Agent</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Specialty</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Confidence</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Current Task</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {agents.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No agents available
                </TableCell>
              </TableRow>
            ) : (
              agents.map((agent) => {
                const statusColor = getStatusColor(agent.status);
                const confidence = parseFloat(agent.confidence) || 0;

                return (
                  <TableRow
                    key={agent.name || Math.random()}
                    sx={{
                      borderBottom: '1px solid rgba(56,78,112,0.05)',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                    }}
                  >
                    <TableCell sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Memory sx={{ fontSize: 16, color: statusColor }} />
                        {agent.name || 'Unknown'}
                      </Box>
                    </TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{agent.specialty || 'N/A'}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getStatusIcon(agent.status)}
                        label={agent.status || 'Unknown'}
                        size="small"
                        sx={{
                          bgcolor: `${statusColor}15`,
                          color: statusColor,
                          border: `1px solid ${statusColor}20`,
                          fontSize: '0.65rem',
                          fontWeight: 500,
                          height: 24,
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={confidence}
                          sx={{
                            width: 60,
                            height: 4,
                            borderRadius: 2,
                            bgcolor: 'rgba(255,255,255,0.05)',
                            '& .MuiLinearProgress-bar': {
                              bgcolor: confidence > 80 ? '#10B981' : confidence > 50 ? '#F59E0B' : '#EF4444',
                            },
                          }}
                        />
                        <Typography sx={{ color: '#8899B4', fontSize: '0.75rem', minWidth: 35 }}>
                          {confidence}%
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell sx={{ color: '#8899B4', fontSize: '0.8rem' }}>
                      {agent.currentTask || 'Idle'}
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
```

## frontend/src/pages/AIActivity.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/AIActivity.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  useTheme,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Circle,
  Refresh,
  Schedule,
} from '@mui/icons-material';
import { getAgentActivity } from '../api/client';

// ✅ Mock data for when API fails
const MOCK_ACTIVITIES = [
  { time: '00:25:30', agent: 'Safety', action: 'Validated operating envelope for Zone A', status: 'Completed', confidence: '96%' },
  { time: '00:24:15', agent: 'Diagnostic', action: 'Analyzed vibration pattern for Pump A-01', status: 'Running', confidence: '95%' },
  { time: '00:23:00', agent: 'Knowledge', action: 'Retrieved SOP for pressure spike response', status: 'Completed', confidence: '93%' },
  { time: '00:22:10', agent: 'Prediction', action: 'Calculated failure probability for Compressor C-12', status: 'Completed', confidence: '91%' },
  { time: '00:21:30', agent: 'Maintenance', action: 'Generated maintenance schedule for critical assets', status: 'Queued', confidence: '94%' },
  { time: '00:20:45', agent: 'Planning', action: 'Created recovery plan for pressure incident', status: 'Completed', confidence: '92%' },
  { time: '00:19:50', agent: 'Notification', action: 'Sent alert for abnormal temperature reading', status: 'Completed', confidence: '96%' },
  { time: '00:18:30', agent: 'Report', action: 'Compiled incident summary report', status: 'In Progress', confidence: '90%' },
];

export default function AIActivity() {
  const [activities, setActivities] = useState(MOCK_ACTIVITIES);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const response = await getAgentActivity();
      const data = response.data;
      
      // ✅ Handle different response formats and filter out nulls
      let activityData = [];
      if (Array.isArray(data)) {
        // ✅ Filter out null/undefined values
        activityData = data.filter(item => item !== null && item !== undefined);
      } else if (data?.data && Array.isArray(data.data)) {
        activityData = data.data.filter(item => item !== null && item !== undefined);
      } else {
        activityData = MOCK_ACTIVITIES;
      }
      
      // ✅ Ensure each item has required fields
      const validActivities = activityData.filter(item => 
        item && typeof item === 'object' && item.status !== undefined
      );
      
      setActivities(validActivities.length > 0 ? validActivities : MOCK_ACTIVITIES);
    } catch (e) {
      console.error('Failed to load activities, using mock data:', e);
      setActivities(MOCK_ACTIVITIES);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    if (!status) return '#8899B4';
    const colors = {
      'Completed': '#10B981',
      'Running': '#F59E0B',
      'Failed': '#EF4444',
      'Queued': '#8B5CF6',
      'Pending': '#3B82F6',
      'In Progress': '#3B82F6',
    };
    return colors[status] || '#8899B4';
  };

  const getStatusDot = (status) => {
    const color = getStatusColor(status);
    return (
      <TimelineDot sx={{ 
        bgcolor: color,
        ...(status === 'Running' || status === 'In Progress' ? {
          animation: 'pulse 2s infinite',
          '@keyframes pulse': {
            '0%, 100%': { opacity: 1, transform: 'scale(1)' },
            '50%': { opacity: 0.4, transform: 'scale(0.8)' },
          }
        } : {})
      }} />
    );
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading activities...</Typography>
      </Box>
    );
  }

  // ✅ Safe filtering with null checks
  const total = activities?.length || 0;
  const completed = activities?.filter(a => a?.status === 'Completed')?.length || 0;
  const running = activities?.filter(a => a?.status === 'Running' || a?.status === 'In Progress')?.length || 0;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            AI Activity
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {total} activities recorded
          </Typography>
        </Box>
        <Chip
          label={`${running} active`}
          sx={{
            bgcolor: 'rgba(245,158,11,0.08)',
            color: '#F59E0B',
            border: '1px solid rgba(245,158,11,0.15)',
          }}
        />
      </Box>

      {/* Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {total}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Completed
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {completed}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                In Progress
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {running}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Queued
              </Typography>
              <Typography variant="h5" sx={{ color: '#8B5CF6', fontWeight: 600 }}>
                {total - completed - running}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Activity List */}
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Activity Timeline
          </Typography>
          <Chip
            label={`${activities?.length || 0} events`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.03)', color: '#5A6B8A' }}
          />
        </Box>

        {!activities || activities.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography sx={{ color: '#5A6B8A' }}>No activities recorded yet</Typography>
          </Box>
        ) : (
          <Box>
            {activities.slice(0, 20).map((activity, index) => {
              if (!activity) return null;
              const color = getStatusColor(activity.status);
              const isLast = index === activities.length - 1 || index === 19;
              
              return (
                <Box key={index}>
                  <Box sx={{ 
                    display: 'flex', 
                    alignItems: 'flex-start', 
                    gap: 2,
                    py: 1.5,
                    px: 1,
                  }}>
                    {/* Time */}
                    <Box sx={{ minWidth: 80, pt: 0.5 }}>
                      <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.7rem' }}>
                        {activity.time || 'N/A'}
                      </Typography>
                    </Box>
                    
                    {/* Dot */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 24 }}>
                      <Box sx={{ 
                        width: 12, 
                        height: 12, 
                        borderRadius: '50%', 
                        bgcolor: color,
                        ...((activity.status === 'Running' || activity.status === 'In Progress') && {
                          animation: 'pulse 2s infinite',
                        })
                      }} />
                      {!isLast && (
                        <Box sx={{ 
                          width: 1, 
                          height: 24, 
                          bgcolor: 'rgba(56,78,112,0.1)',
                          mt: 1,
                        }} />
                      )}
                    </Box>
                    
                    {/* Content */}
                    <Box sx={{ flex: 1, pt: 0.5 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                        <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                          {activity.agent || 'Unknown'}
                        </Typography>
                        <Chip
                          label={activity.status || 'Unknown'}
                          size="small"
                          sx={{
                            bgcolor: `${color}15`,
                            color: color,
                            fontSize: '0.6rem',
                            height: 18,
                            fontWeight: 500,
                          }}
                        />
                      </Box>
                      <Typography variant="caption" sx={{ color: '#8899B4', display: 'block', mt: 0.5 }}>
                        {activity.action || 'No action recorded'}
                      </Typography>
                      {activity.confidence && (
                        <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mt: 0.25 }}>
                          Confidence: {activity.confidence}
                        </Typography>
                      )}
                    </Box>
                  </Box>
                  {!isLast && <Box sx={{ borderBottom: '1px solid rgba(56,78,112,0.05)', mx: 1 }} />}
                </Box>
              );
            })}
          </Box>
        )}
      </Paper>
    </Box>
  );
}
```

## frontend/src/pages/Assets.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/Assets.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  TextField,
  MenuItem,
  LinearProgress,
  IconButton,
  Collapse,
  Card,
  CardContent,
  useTheme,
} from '@mui/material';
import {
  Search,
  ExpandMore,
  ExpandLess,
  Memory,
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  Circle,
} from '@mui/icons-material';
import { getAssets } from '../api/client';

const STATUS_COLORS = {
  'Running': '#10B981',
  'Healthy': '#10B981',
  'Warning': '#F59E0B',
  'Critical': '#EF4444',
  'Offline': '#5A6B8A',
};

export default function Assets() {
  const [assets, setAssets] = useState([]);
  const [filteredAssets, setFilteredAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    loadAssets();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [searchTerm, statusFilter, typeFilter, assets]);

  const loadAssets = async () => {
    try {
      const response = await getAssets();
      setAssets(response.data);
      setFilteredAssets(response.data);
    } catch (e) {
      console.error('Failed to load assets:', e);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = assets;
    
    if (searchTerm) {
      filtered = filtered.filter(a => 
        a.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.type?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.location?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (statusFilter !== 'all') {
      filtered = filtered.filter(a => 
        a.status?.toLowerCase() === statusFilter.toLowerCase()
      );
    }
    
    if (typeFilter !== 'all') {
      filtered = filtered.filter(a => 
        a.type?.toLowerCase() === typeFilter.toLowerCase()
      );
    }
    
    setFilteredAssets(filtered);
  };

  const getHealthColor = (health) => {
    if (health >= 80) return '#10B981';
    if (health >= 50) return '#F59E0B';
    return '#EF4444';
  };

  const getStatusColor = (status) => {
    return STATUS_COLORS[status] || '#8899B4';
  };

  const types = ['all', ...new Set(assets.map(a => a.type))].filter(Boolean);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading assets...</Typography>
      </Box>
    );
  }

  const total = assets.length;
  const online = assets.filter(a => a.status === 'Running').length;
  const warning = assets.filter(a => a.status === 'Warning').length;
  const critical = assets.filter(a => a.status === 'Critical').length;
  const avgHealth = total > 0 
  ? Math.round(assets.reduce((s, a) => s + (a.health || 0), 0) / total)
  : 0;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Asset Registry
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {total} assets monitored · {online} online · {warning} warning · {critical} critical
          </Typography>
        </Box>
        <Chip
          label={`${avgHealth}% Avg Health`}
          sx={{
            bgcolor: parseFloat(avgHealth) >= 80 ? 'rgba(16,185,129,0.08)' : 'rgba(245,158,11,0.08)',
            color: parseFloat(avgHealth) >= 80 ? '#10B981' : '#F59E0B',
          }}
        />
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total Assets
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {total}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Online
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {online}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Warning
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {warning}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Critical
              </Typography>
              <Typography variant="h5" sx={{ color: '#EF4444', fontWeight: 600 }}>
                {critical}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search assets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              slotProps={{
                input: {
                  startAdornment: <Search sx={{ color: '#5A6B8A', mr: 1, fontSize: 18 }} />,
                  sx: {
                    bgcolor: 'rgba(255,255,255,0.02)',
                    border: '1px solid rgba(56,78,112,0.1)',
                    borderRadius: '6px',
                    '&:hover': { borderColor: 'rgba(56,78,112,0.2)' },
                  }
                }
              }}
            />
          </Grid>
          <Grid item xs={6} md={3}>
            <TextField
              select
              fullWidth
              size="small"
              label="Status"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              sx={{
                '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                '& .MuiSelect-select': { color: '#E8EDF5', fontSize: '0.85rem' },
              }}
            >
              <MenuItem value="all">All Statuses</MenuItem>
              <MenuItem value="Running">Running</MenuItem>
              <MenuItem value="Healthy">Healthy</MenuItem>
              <MenuItem value="Warning">Warning</MenuItem>
              <MenuItem value="Critical">Critical</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={6} md={3}>
            <TextField
              select
              fullWidth
              size="small"
              label="Type"
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              sx={{
                '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                '& .MuiSelect-select': { color: '#E8EDF5', fontSize: '0.85rem' },
              }}
            >
              <MenuItem value="all">All Types</MenuItem>
              {types.filter(t => t !== 'all').map((type) => (
                <MenuItem key={type} value={type}>{type}</MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} md={2}>
            <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
              {filteredAssets.length} assets shown
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Asset
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Type
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Location
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Health
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Status
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Details
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredAssets.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No assets found matching your filters
                </TableCell>
              </TableRow>
            ) : (
              filteredAssets.map((asset, index) => {
                const health = asset.health || 0;
                const healthColor = getHealthColor(health);
                const statusColor = getStatusColor(asset.status);
                const isExpanded = selectedAsset?.id === asset.id && expanded;

                return (
                  <React.Fragment key={asset.id || index}>
                    <TableRow
                      sx={{
                        '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                        borderBottom: '1px solid rgba(56,78,112,0.05)',
                        cursor: 'pointer',
                      }}
                      onClick={() => {
                        if (selectedAsset?.id === asset.id) {
                          setExpanded(!expanded);
                        } else {
                          setSelectedAsset(asset);
                          setExpanded(true);
                        }
                      }}
                    >
                      <TableCell sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                        {asset.name}
                      </TableCell>
                      <TableCell sx={{ color: '#8899B4' }}>{asset.type || 'Unknown'}</TableCell>
                      <TableCell sx={{ color: '#8899B4' }}>{asset.location || 'Unassigned'}</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <LinearProgress
                            variant="determinate"
                            value={Math.round(health)}  // ✅ Round the value
                            sx={{
                                width: 80,
                                height: 4,
                                borderRadius: 2,
                                bgcolor: 'rgba(255,255,255,0.05)',
                                '& .MuiLinearProgress-bar': { bgcolor: healthColor },
                            }}
                            />
                            <Typography sx={{ color: healthColor, fontWeight: 500, fontSize: '0.8rem', minWidth: 40 }}>
                            {Math.round(health)}%  
                            </Typography>
                        
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={asset.status || 'Unknown'}
                          size="small"
                          sx={{
                            bgcolor: `${statusColor}15`,
                            color: statusColor,
                            border: `1px solid ${statusColor}20`,
                            fontSize: '0.65rem',
                            fontWeight: 500,
                            height: 24,
                          }}
                        />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" sx={{ color: '#5A6B8A' }}>
                          {isExpanded ? <ExpandLess sx={{ fontSize: 18 }} /> : <ExpandMore sx={{ fontSize: 18 }} />}
                        </IconButton>
                      </TableCell>
                    </TableRow>

                    <TableRow>
                      <TableCell colSpan={6} sx={{ p: 0, border: 'none' }}>
                        <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                          <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.01)', borderTop: '1px solid rgba(56,78,112,0.05)' }}>
                            <Grid container spacing={2}>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Asset ID
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#8899B4' }}>
                                  {asset.id}
                                </Typography>
                              </Grid>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Health Status
                                </Typography>
                                <Typography variant="body2" sx={{ color: healthColor }}>
                                  {health >= 80 ? 'Excellent' : health >= 50 ? 'Good' : 'Critical'}
                                </Typography>
                              </Grid>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Refinery
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#8899B4' }}>
                                  {asset.refinery_name || 'Unknown'}
                                </Typography>
                              </Grid>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Last Updated
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#8899B4' }}>
                                  {new Date().toLocaleTimeString()}
                                </Typography>
                              </Grid>
                            </Grid>
                          </Box>
                        </Collapse>
                      </TableCell>
                    </TableRow>
                  </React.Fragment>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
```

## frontend/src/pages/Dashboard.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/Dashboard.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  Devices,
  Warning,
  CheckCircle,
  Speed,
} from '@mui/icons-material';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { getAssets, getTelemetry } from '../api/client';

const COLORS = ['#EF4444', '#EF4444', '#F59E0B', '#3B82F6', '#10B981'];
const HEALTH_RANGES = ['Critical', 'Poor', 'Warning', 'Good', 'Excellent'];

export default function Dashboard() {
  const [assets, setAssets] = useState([]);
  const [telemetry, setTelemetry] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [refreshCount, setRefreshCount] = useState(0);

  // ✅ Load data function
  const loadData = async () => {
    try {
      const assetsRes = await getAssets();
      setAssets(assetsRes.data || []);

      if (assetsRes.data && assetsRes.data.length > 0) {
        const teleRes = await getTelemetry(assetsRes.data[0].id);
        setTelemetry(teleRes.data || []);
      }
    } catch (e) {
      console.error('Failed to load data:', e);
    } finally {
      setLoading(false);
      setLastUpdate(new Date());
      setRefreshCount(prev => prev + 1);
    }
  };

  // ✅ Initial load + auto-refresh every 3 seconds
  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, []);

  const totalAssets = assets.length;
  const healthyCount = assets.filter((a) => a.status === 'Running').length;
  const avgHealth = totalAssets > 0
    ? Math.round(assets.reduce((s, a) => s + (a.health || 0), 0) / totalAssets)
    : 0;
  const criticalCount = assets.filter((a) => a.health < 50).length;
  const warningCount = assets.filter((a) => a.health >= 50 && a.health < 80).length;

  const healthRanges = [
    { name: 'Critical', value: 0, color: '#EF4444' },
    { name: 'Poor', value: 0, color: '#EF4444' },
    { name: 'Warning', value: 0, color: '#F59E0B' },
    { name: 'Good', value: 0, color: '#3B82F6' },
    { name: 'Excellent', value: 0, color: '#10B981' },
  ];
  assets.forEach((a) => {
    const h = a.health || 0;
    if (h <= 20) healthRanges[0].value++;
    else if (h <= 40) healthRanges[1].value++;
    else if (h <= 60) healthRanges[2].value++;
    else if (h <= 80) healthRanges[3].value++;
    else healthRanges[4].value++;
  });

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '50vh', gap: 3 }}>
        <Typography variant="h6" sx={{ color: '#3B82F6' }}>Loading dashboard...</Typography>
        <LinearProgress sx={{ width: 200, height: 3, borderRadius: 2, bgcolor: 'rgba(59,130,246,0.1)' }} />
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Operations Dashboard
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            Real-time monitoring · Last updated {formatTime(lastUpdate)} · Refresh #{refreshCount}
          </Typography>
        </Box>
        <Chip
          label="● LIVE"
          sx={{
            bgcolor: 'rgba(16, 185, 129, 0.08)',
            color: '#10B981',
            border: '1px solid rgba(16, 185, 129, 0.15)',
            fontWeight: 500,
            fontSize: '0.7rem',
          }}
        />
      </Box>

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  Fleet Health
                </Typography>
                <Speed sx={{ fontSize: 18, color: avgHealth > 80 ? '#10B981' : '#F59E0B' }} />
              </Box>
              <Typography variant="h3" sx={{ color: avgHealth > 80 ? '#10B981' : '#F59E0B', fontWeight: 600, my: 1 }}>
                {avgHealth}%
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: '#10B981' }} />
                  <Typography variant="caption" sx={{ color: '#8899B4' }}>{healthyCount}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: '#F59E0B' }} />
                  <Typography variant="caption" sx={{ color: '#8899B4' }}>{warningCount}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: '#EF4444' }} />
                  <Typography variant="caption" sx={{ color: '#8899B4' }}>{criticalCount}</Typography>
                </Box>
              </Box>
              <LinearProgress
                variant="determinate"
                value={avgHealth}
                sx={{ mt: 1.5, height: 2, borderRadius: 2, bgcolor: 'rgba(255,255,255,0.04)' }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  Total Assets
                </Typography>
                <Devices sx={{ fontSize: 18, color: '#3B82F6' }} />
              </Box>
              <Typography variant="h3" sx={{ color: '#E8EDF5', fontWeight: 600, my: 1 }}>
                {totalAssets}
              </Typography>
              <Typography variant="caption" sx={{ color: '#8899B4' }}>
                {healthyCount} online · {warningCount} warning · {criticalCount} critical
              </Typography>
              <Box sx={{ display: 'flex', gap: 0.5, mt: 1.5 }}>
                <Box sx={{ flex: 1, height: 2, borderRadius: 2, bgcolor: '#10B981', opacity: healthyCount / totalAssets || 0 }} />
                <Box sx={{ flex: 1, height: 2, borderRadius: 2, bgcolor: '#F59E0B', opacity: warningCount / totalAssets || 0 }} />
                <Box sx={{ flex: 1, height: 2, borderRadius: 2, bgcolor: '#EF4444', opacity: criticalCount / totalAssets || 0 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  Telemetry
                </Typography>
                <TrendingUp sx={{ fontSize: 18, color: '#3B82F6' }} />
              </Box>
              <Typography variant="h3" sx={{ color: '#E8EDF5', fontWeight: 600, my: 1 }}>
                {telemetry.length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#8899B4' }}>
                Data points in stream
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  System Status
                </Typography>
                <CheckCircle sx={{ fontSize: 18, color: '#10B981' }} />
              </Box>
              <Typography variant="h3" sx={{ color: '#10B981', fontWeight: 600, my: 1 }}>
                NOMINAL
              </Typography>
              <Typography variant="caption" sx={{ color: '#8899B4' }}>
                All systems operational
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Telemetry Chart */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Telemetry Stream
          </Typography>
          <Chip label={`${telemetry.length} readings`} size="small" sx={{ bgcolor: 'rgba(59,130,246,0.06)', color: '#8899B4', border: '1px solid rgba(56,78,112,0.1)', fontSize: '0.6rem' }} />
        </Box>
        {telemetry.length > 0 ? (
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={telemetry.slice(-30)}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" />
              <XAxis dataKey="timestamp" stroke="#5A6B8A" tick={{ fontSize: 10 }} />
              <YAxis stroke="#5A6B8A" tick={{ fontSize: 10 }} />
              <Tooltip
                contentStyle={{
                  background: '#121C2E',
                  border: '1px solid rgba(56,78,112,0.15)',
                  borderRadius: '6px',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
                }}
                labelStyle={{ color: '#8899B4' }}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#3B82F6"
                strokeWidth={1.5}
                fill="url(#colorValue)"
                name="Sensor Value"
              />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <Box sx={{ textAlign: 'center', py: 6 }}>
            <Typography sx={{ color: '#5A6B8A' }}>No telemetry data available</Typography>
          </Box>
        )}
      </Paper>

      {/* Health Distribution */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
              Asset Health Distribution
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4, flexWrap: 'wrap' }}>
              {/* ✅ Pie Chart */}
              <Box sx={{ width: 200, height: 200 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={healthRanges}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={80}
                      dataKey="value"
                      paddingAngle={2}
                    >
                      {healthRanges.map((entry, i) => (
                        <Cell key={i} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        background: '#121C2E',
                        border: '1px solid rgba(56,78,112,0.15)',
                        borderRadius: '6px',
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
              
              {/* ✅ Legend */}
              <Box>
                {healthRanges.filter(h => h.value > 0).map((item) => (
                  <Box key={item.name} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: item.color }} />
                    <Typography variant="body2" sx={{ color: '#8899B4', fontSize: '0.8rem' }}>
                      {item.name}: <strong style={{ color: '#E8EDF5' }}>{item.value}</strong>
                    </Typography>
                  </Box>
                ))}
                {healthRanges.every(h => h.value === 0) && (
                  <Typography sx={{ color: '#5A6B8A' }}>No asset data available</Typography>
                )}
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
              Asset Health Leaders
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {assets
                .sort((a, b) => (b.health || 0) - (a.health || 0))
                .slice(0, 5)
                .map((asset, index) => {
                  const health = Math.round(asset.health || 0);
                  const color = health >= 80 ? '#10B981' : health >= 50 ? '#F59E0B' : '#EF4444';
                  return (
                    <Box
                      key={asset.id}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 2,
                        p: 1.5,
                        borderRadius: 1,
                        bgcolor: 'rgba(255,255,255,0.02)',
                        border: '1px solid rgba(255,255,255,0.03)',
                      }}
                    >
                      <Typography sx={{ color: '#5A6B8A', fontWeight: 500, minWidth: 24, fontSize: '0.75rem' }}>
                        {String(index + 1).padStart(2, '0')}
                      </Typography>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500, fontSize: '0.85rem' }}>
                          {asset.name}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.65rem' }}>
                          {asset.type || 'Unknown'}
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <LinearProgress
                          variant="determinate"
                          value={health}
                          sx={{
                            width: 80,
                            height: 3,
                            borderRadius: 2,
                            bgcolor: 'rgba(255,255,255,0.04)',
                            '& .MuiLinearProgress-bar': {
                              bgcolor: color,
                            },
                          }}
                        />
                        <Typography sx={{ color, fontWeight: 500, minWidth: 40, fontSize: '0.8rem' }}>
                          {health}%
                        </Typography>
                      </Box>
                    </Box>
                  );
                })}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
```

## frontend/src/pages/DigitalTwin.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/DigitalTwin.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  useTheme,
} from '@mui/material';
import {
  Sensors,
  LocationOn,
  CheckCircle,
  Warning,
  Error,
  Circle,
} from '@mui/icons-material';
import { getAssets } from '../api/client';

export default function DigitalTwin() {
  const theme = useTheme();
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await getAssets();
      setAssets(response.data || []);
    } catch (e) {
      console.error('Failed to load assets:', e);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'Running': '#10B981',
      'Healthy': '#10B981',
      'Warning': '#F59E0B',
      'Critical': '#EF4444',
      'Offline': '#5A6B8A',
    };
    return colors[status] || '#8899B4';
  };

  const getHealthColor = (health) => {
    if (health >= 80) return '#10B981';
    if (health >= 50) return '#F59E0B';
    return '#EF4444';
  };

  // Group assets by zone
  const zones = assets.reduce((acc, asset) => {
    const zone = asset.location || 'Unassigned';
    if (!acc[zone]) acc[zone] = [];
    acc[zone].push(asset);
    return acc;
  }, {});

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading digital twin...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Digital Twin
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {assets.length} assets · {Object.keys(zones).length} zones
          </Typography>
        </Box>
        <Chip
          label="● LIVE"
          sx={{ bgcolor: 'rgba(16,185,129,0.08)', color: '#10B981', border: '1px solid rgba(16,185,129,0.15)' }}
        />
      </Box>

      <Grid container spacing={3}>
        {Object.entries(zones).map(([zoneName, zoneAssets]) => {
          const avgHealth = zoneAssets.reduce((s, a) => s + (a.health || 0), 0) / zoneAssets.length;
          const healthColor = getHealthColor(avgHealth);
          const healthyCount = zoneAssets.filter(a => a.status === 'Running').length;

          return (
            <Grid item xs={12} md={6} key={zoneName}>
              <Paper sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LocationOn sx={{ color: '#3B82F6', fontSize: 18 }} />
                    <Typography variant="h6" sx={{ color: '#E8EDF5', fontWeight: 500, fontSize: '1rem' }}>
                      {zoneName}
                    </Typography>
                  </Box>
                  <Chip
                    label={`${healthyCount}/${zoneAssets.length} online`}
                    size="small"
                    sx={{
                      bgcolor: avgHealth >= 80 ? 'rgba(16,185,129,0.08)' : 'rgba(245,158,11,0.08)',
                      color: avgHealth >= 80 ? '#10B981' : '#F59E0B',
                      fontSize: '0.6rem',
                    }}
                  />
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <LinearProgress
                    variant="determinate"
                    value={avgHealth}
                    sx={{
                      flex: 1,
                      height: 6,
                      borderRadius: 3,
                      bgcolor: 'rgba(255,255,255,0.05)',
                      '& .MuiLinearProgress-bar': { bgcolor: healthColor },
                    }}
                  />
                  <Typography sx={{ color: healthColor, fontWeight: 600, minWidth: 45 }}>
                    {Math.round(avgHealth)}%
                  </Typography>
                </Box>

                <Grid container spacing={1}>
                  {zoneAssets.slice(0, 6).map((asset) => {
                    const statusColor = getStatusColor(asset.status);
                    const health = asset.health || 0;
                    return (
                      <Grid item xs={6} key={asset.id}>
                        <Card sx={{ bgcolor: 'rgba(255,255,255,0.02)' }}>
                          <CardContent sx={{ py: 1, px: 1.5 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <Typography variant="caption" sx={{ color: '#E8EDF5', fontWeight: 500, fontSize: '0.7rem' }}>
                                {asset.name}
                              </Typography>
                              <Chip
                                size="small"
                                sx={{
                                  width: 8,
                                  height: 8,
                                  minWidth: 8,
                                  bgcolor: statusColor,
                                  borderRadius: '50%',
                                  '& .MuiChip-label': { display: 'none' },
                                }}
                              />
                            </Box>
                            <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.6rem' }}>
                              {asset.type || 'Unknown'} · {health}%
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    );
                  })}
                </Grid>
                {zoneAssets.length > 6 && (
                  <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mt: 1 }}>
                    + {zoneAssets.length - 6} more assets
                  </Typography>
                )}
              </Paper>
            </Grid>
          );
        })}
      </Grid>

      {Object.keys(zones).length === 0 && (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography sx={{ color: '#5A6B8A' }}>No assets available for digital twin view</Typography>
        </Paper>
      )}
    </Box>
  );
}
```

## frontend/src/pages/HealthPrediction.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/HealthPrediction.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
  useTheme,
} from '@mui/material';
import {
  Science,
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
  Timeline,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import { getAssets, getPredictions } from '../api/client';

export default function HealthPrediction() {
  const theme = useTheme();
  const [assets, setAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [horizon, setHorizon] = useState(14);

  useEffect(() => {
    loadAssets();
  }, []);

  useEffect(() => {
    if (selectedAsset) {
      loadPrediction();
    }
  }, [selectedAsset, horizon]);

  const loadAssets = async () => {
    try {
      const response = await getAssets();
      setAssets(response.data || []);
      if (response.data?.length > 0) {
        setSelectedAsset(response.data[0].id);
      }
    } catch (e) {
      console.error('Failed to load assets:', e);
    } finally {
      setLoading(false);
    }
  };

  const loadPrediction = async () => {
    try {
      const response = await getPredictions(selectedAsset, horizon);
      setPrediction(response.data);
    } catch (e) {
      console.error('Failed to load prediction:', e);
    }
  };

  const getSelectedAssetName = () => {
    const asset = assets.find(a => a.id === selectedAsset);
    return asset?.name || 'Unknown Asset';
  };

  // Generate mock prediction data if none exists
  const getChartData = () => {
    if (prediction?.historical?.length) {
      return prediction.historical.map((h, i) => ({
        day: i + 1,
        health: h,
      }));
    }
    // Mock data
    const data = [];
    let health = 95;
    for (let i = 0; i < horizon; i++) {
      health -= Math.random() * 2 + 0.5;
      health = Math.max(0, health);
      data.push({
        day: i + 1,
        health: Math.round(health * 10) / 10,
      });
    }
    return data;
  };

  const getHealthStatus = (health) => {
    if (health >= 80) return { label: 'Excellent', color: '#10B981', icon: <CheckCircle /> };
    if (health >= 60) return { label: 'Good', color: '#3B82F6', icon: <CheckCircle /> };
    if (health >= 40) return { label: 'Warning', color: '#F59E0B', icon: <Warning /> };
    return { label: 'Critical', color: '#EF4444', icon: <Warning /> };
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading predictions...</Typography>
      </Box>
    );
  }

  const currentHealth = prediction?.health || 85;
  const status = getHealthStatus(currentHealth);
  const chartData = getChartData();

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Health Prediction
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            AI-powered asset health forecasting
          </Typography>
        </Box>
        <Chip
          label={`${horizon} day forecast`}
          sx={{ bgcolor: 'rgba(59,130,246,0.08)', color: '#3B82F6', border: '1px solid rgba(59,130,246,0.15)' }}
        />
      </Box>

      {/* Asset Selector */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <FormControl fullWidth size="small">
              <InputLabel sx={{ color: '#5A6B8A' }}>Select Asset</InputLabel>
              <Select
                value={selectedAsset}
                onChange={(e) => setSelectedAsset(e.target.value)}
                label="Select Asset"
                sx={{ color: '#E8EDF5' }}
              >
                {assets.map((asset) => (
                  <MenuItem key={asset.id} value={asset.id}>
                    {asset.name} ({asset.type || 'Unknown'})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth size="small">
              <InputLabel sx={{ color: '#5A6B8A' }}>Forecast Horizon</InputLabel>
              <Select
                value={horizon}
                onChange={(e) => setHorizon(e.target.value)}
                label="Forecast Horizon"
                sx={{ color: '#E8EDF5' }}
              >
                <MenuItem value={7}>7 Days</MenuItem>
                <MenuItem value={14}>14 Days</MenuItem>
                <MenuItem value={30}>30 Days</MenuItem>
                <MenuItem value={60}>60 Days</MenuItem>
                <MenuItem value={90}>90 Days</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="body2" sx={{ color: '#5A6B8A', textAlign: 'right' }}>
              Asset: <strong style={{ color: '#E8EDF5' }}>{getSelectedAssetName()}</strong>
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Current Health
              </Typography>
              <Typography variant="h5" sx={{ color: status.color, fontWeight: 600 }}>
                {currentHealth}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Status
              </Typography>
              <Typography variant="h5" sx={{ color: status.color, fontWeight: 600, fontSize: '1rem' }}>
                {status.label}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                RUL
              </Typography>
              <Typography variant="h5" sx={{ color: '#3B82F6', fontWeight: 600, fontSize: '1rem' }}>
                {prediction?.rul || '365 days'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Failure Probability
              </Typography>
              <Typography variant="h5" sx={{ color: prediction?.failureProbability > 50 ? '#EF4444' : '#10B981', fontWeight: 600, fontSize: '1rem' }}>
                {prediction?.failureProbability || '5%'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Prediction Chart */}
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Health Forecast
          </Typography>
          <Chip
            label={`${horizon} days`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.03)', color: '#5A6B8A' }}
          />
        </Box>
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="day" stroke="#5A6B8A" label={{ value: 'Days', position: 'bottom', fill: '#5A6B8A' }} />
            <YAxis stroke="#5A6B8A" domain={[0, 100]} label={{ value: 'Health %', angle: -90, position: 'left', fill: '#5A6B8A' }} />
            <Tooltip
              contentStyle={{
                background: '#121C2E',
                border: '1px solid rgba(56,78,112,0.15)',
                borderRadius: '6px',
              }}
            />
            <Line
              type="monotone"
              dataKey="health"
              stroke="#3B82F6"
              strokeWidth={2}
              dot={{ fill: '#3B82F6', r: 4 }}
              name="Health %"
            />
          </LineChart>
        </ResponsiveContainer>
      </Paper>
    </Box>
  );
}
```

## frontend/src/pages/IncidentSimulator.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/IncidentSimulator.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Button,
  Chip,
  TextField,
  MenuItem,
  Alert,
  List,
  ListItem,
  ListItemText,
  Divider,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  useTheme,
  Fade,
  Grow,
} from '@mui/material';
import { CircularProgress } from '@mui/material';
import {
  Warning,
  PlayArrow,
  History,
  CheckCircle,
  Error,
  Circle,
  Refresh,
  Delete,
  TrendingUp,
  TrendingDown,
  FlashOn,
  Whatshot,
} from '@mui/icons-material';
import { triggerIncident, getIncidents } from '../api/client';

const INCIDENT_TYPES = [
  { value: 'pressure spike', label: 'Pressure Spike', icon: '📈', color: '#EF4444', desc: 'Sudden pressure increase' },
  { value: 'gas leak', label: 'Gas Leak', icon: '💨', color: '#F59E0B', desc: 'Gas concentration detected' },
  { value: 'high temperature', label: 'High Temperature', icon: '🌡️', color: '#F97316', desc: 'Temperature threshold exceeded' },
  { value: 'high vibration', label: 'High Vibration', icon: '📳', color: '#8B5CF6', desc: 'Abnormal vibration detected' },
  { value: 'flow restriction', label: 'Flow Restriction', icon: '🚫', color: '#3B82F6', desc: 'Flow rate below minimum' },
];

const SEVERITY_COLORS = {
  'Low': '#10B981',
  'Medium': '#F59E0B',
  'High': '#F97316',
  'Critical': '#EF4444',
};

export default function IncidentSimulator() {
  const theme = useTheme();
  const [incidentType, setIncidentType] = useState('pressure spike');
  const [severity, setSeverity] = useState('High');
  const [triggering, setTriggering] = useState(false);
  const [incidentHistory, setIncidentHistory] = useState([]);
  const [activeIncidents, setActiveIncidents] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  // Load incidents
  useEffect(() => {
    loadIncidents();
    const interval = setInterval(loadIncidents, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadIncidents = async () => {
    try {
      const response = await getIncidents();
      const incidents = response.data || [];
      setActiveIncidents(incidents);
    } catch (e) {
      console.error('Failed to load incidents:', e);
    }
  };

  const handleTrigger = async () => {
    setTriggering(true);
    setResult(null);
    setLoading(true);
    setShowSuccess(false);

    try {
      const response = await triggerIncident(incidentType);
      setResult({
        success: true,
        message: `Incident triggered successfully`,
        id: response.data?.id || 'unknown',
        type: incidentType,
        severity: severity,
      });
      setShowSuccess(true);

      // Add to history
      setIncidentHistory(prev => [
        {
          id: Date.now(),
          type: incidentType,
          severity: severity,
          timestamp: new Date().toISOString(),
          status: 'Triggered',
          message: response.data?.message || 'Incident triggered',
        },
        ...prev.slice(0, 49),
      ]);

      await loadIncidents();

      setTimeout(() => setShowSuccess(false), 3000);

    } catch (e) {
      console.error('Failed to trigger incident:', e);
      setResult({
        success: false,
        message: `Failed to trigger incident: ${e.message || 'Unknown error'}`,
      });
    } finally {
      setTriggering(false);
      setLoading(false);
      setTimeout(() => setResult(null), 5000);
    }
  };

  const getIncidentIcon = (type) => {
    const found = INCIDENT_TYPES.find(t => t.value === type);
    return found ? found.icon : '⚡';
  };

  const getIncidentColor = (type) => {
    const found = INCIDENT_TYPES.find(t => t.value === type);
    return found ? found.color : '#8899B4';
  };

  const getSeverityColor = (sev) => {
    return SEVERITY_COLORS[sev] || '#8899B4';
  };

  const getSeverityIcon = (sev) => {
    const icons = {
      'Low': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
      'Medium': <Warning sx={{ fontSize: 14, color: '#F59E0B' }} />,
      'High': <Error sx={{ fontSize: 14, color: '#F97316' }} />,
      'Critical': <FlashOn sx={{ fontSize: 14, color: '#EF4444' }} />,
    };
    return icons[sev] || <Circle sx={{ fontSize: 14, color: '#8899B4' }} />;
  };

  const selectedType = INCIDENT_TYPES.find(t => t.value === incidentType);

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Incident Simulator
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            Trigger and test incident response workflows
          </Typography>
        </Box>
        <Chip
          label={`${activeIncidents.length} Active`}
          sx={{
            bgcolor: activeIncidents.length > 0 ? 'rgba(239,68,68,0.08)' : 'rgba(16,185,129,0.08)',
            color: activeIncidents.length > 0 ? '#EF4444' : '#10B981',
            border: `1px solid ${activeIncidents.length > 0 ? 'rgba(239,68,68,0.15)' : 'rgba(16,185,129,0.15)'}`,
            fontWeight: 500,
          }}
        />
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Total Triggered
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {incidentHistory.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Active
              </Typography>
              <Typography variant="h5" sx={{ color: activeIncidents.length > 0 ? '#EF4444' : '#10B981', fontWeight: 600 }}>
                {activeIncidents.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Most Common
              </Typography>
              <Typography variant="h5" sx={{ color: '#3B82F6', fontWeight: 600, fontSize: '1rem' }}>
                {incidentHistory.length > 0 
                  ? Object.entries(
                      incidentHistory.reduce((acc, i) => {
                        acc[i.type] = (acc[i.type] || 0) + 1;
                        return acc;
                      }, {})
                    ).sort((a, b) => b[1] - a[1])[0]?.[0] || 'None'
                  : 'None'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Avg Severity
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {incidentHistory.length > 0 
                  ? Object.entries(
                      incidentHistory.reduce((acc, i) => {
                        const sev = i.severity || 'Low';
                        acc[sev] = (acc[sev] || 0) + 1;
                        return acc;
                      }, {})
                    ).sort((a, b) => b[1] - a[1])[0]?.[0] || 'Low'
                  : 'Low'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Trigger Panel - Left */}
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
              Configure Incident
            </Typography>

            {/* Type Preview */}
            {selectedType && (
              <Box 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 2, 
                  p: 2, 
                  mb: 2, 
                  borderRadius: 1,
                  bgcolor: `${selectedType.color}10`,
                  border: `1px solid ${selectedType.color}20`,
                }}
              >
                <Box sx={{ fontSize: 32 }}>{selectedType.icon}</Box>
                <Box>
                  <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                    {selectedType.label}
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
                    {selectedType.desc}
                  </Typography>
                </Box>
              </Box>
            )}

            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  select
                  fullWidth
                  label="Incident Type"
                  value={incidentType}
                  onChange={(e) => setIncidentType(e.target.value)}
                  sx={{
                    '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                    '& .MuiSelect-select': { color: '#E8EDF5' },
                  }}
                  SelectProps={{
                    renderValue: (value) => {
                      const found = INCIDENT_TYPES.find(t => t.value === value);
                      return found ? `${found.icon} ${found.label}` : value;
                    },
                  }}
                >
                  {INCIDENT_TYPES.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.icon} {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  select
                  fullWidth
                  label="Severity"
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                  sx={{
                    '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                    '& .MuiSelect-select': { color: '#E8EDF5' },
                  }}
                >
                  {['Low', 'Medium', 'High', 'Critical'].map((option) => (
                    <MenuItem key={option} value={option}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getSeverityIcon(option)}
                        {option}
                      </Box>
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={triggering ? <CircularProgress size={20} color="inherit" /> : <PlayArrow />}
                  onClick={handleTrigger}
                  disabled={triggering}
                  sx={{
                    bgcolor: '#EF4444',
                    '&:hover': { bgcolor: '#DC2626' },
                    py: 1.5,
                    fontWeight: 600,
                    borderRadius: '8px',
                  }}
                >
                  {triggering ? 'Triggering...' : 'Trigger Incident'}
                </Button>
              </Grid>
            </Grid>

            {result && (
              <Fade in={!!result}>
                <Alert
                  severity={result.success ? 'success' : 'error'}
                  sx={{ mt: 2, borderRadius: '8px' }}
                >
                  {result.message}
                  {result.id && (
                    <Typography variant="caption" sx={{ display: 'block', color: 'inherit', opacity: 0.7 }}>
                      ID: {result.id}
                    </Typography>
                  )}
                </Alert>
              </Fade>
            )}

            {/* Quick Presets */}
            <Box sx={{ mt: 2 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mb: 1 }}>
                Quick Presets:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {INCIDENT_TYPES.map((type) => (
                  <Chip
                    key={type.value}
                    label={`${type.icon} ${type.label}`}
                    size="small"
                    onClick={() => setIncidentType(type.value)}
                    sx={{
                      bgcolor: incidentType === type.value ? `${type.color}20` : 'rgba(255,255,255,0.03)',
                      border: incidentType === type.value ? `1px solid ${type.color}40` : '1px solid rgba(56,78,112,0.1)',
                      cursor: 'pointer',
                      color: incidentType === type.value ? '#E8EDF5' : '#8899B4',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.06)' },
                    }}
                  />
                ))}
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Active Incidents - Right */}
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
                Active Incidents
              </Typography>
              <IconButton size="small" onClick={loadIncidents} sx={{ color: '#5A6B8A' }}>
                <Refresh sx={{ fontSize: 16 }} />
              </IconButton>
            </Box>

            {activeIncidents.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 6 }}>
                <Typography sx={{ color: '#5A6B8A' }}>
                  No active incidents
                </Typography>
                <Typography variant="caption" sx={{ color: '#3A4B6A' }}>
                  Trigger an incident to see it here
                </Typography>
              </Box>
            ) : (
              <Box sx={{ maxHeight: 350, overflow: 'auto' }}>
                {activeIncidents.slice(0, 10).map((incident) => (
                  <Box
                    key={incident.id}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      p: 1.5,
                      mb: 1,
                      borderRadius: 1,
                      bgcolor: 'rgba(255,255,255,0.02)',
                      border: '1px solid rgba(56,78,112,0.05)',
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Box sx={{ fontSize: 24 }}>{getIncidentIcon(incident.name)}</Box>
                      <Box>
                        <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                          {incident.name || 'Unknown'}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
                          Asset: {incident.asset_id || 'Unknown'}
                        </Typography>
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Chip
                        label="Active"
                        size="small"
                        sx={{
                          bgcolor: 'rgba(239,68,68,0.12)',
                          color: '#EF4444',
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                      <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
                        {incident.timestamp ? new Date(incident.timestamp).toLocaleTimeString() : ''}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            )}

            {activeIncidents.length > 10 && (
              <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mt: 1, textAlign: 'center' }}>
                + {activeIncidents.length - 10} more incidents
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* History Section */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Incident History
          </Typography>
          <Chip
            label={`${incidentHistory.length} incidents`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.03)', color: '#5A6B8A' }}
          />
        </Box>

        {incidentHistory.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 2 }}>
            <Typography sx={{ color: '#5A6B8A', fontSize: '0.85rem' }}>
              No incidents triggered yet
            </Typography>
          </Box>
        ) : (
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Time</TableCell>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Type</TableCell>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Severity</TableCell>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {incidentHistory.slice(0, 20).map((incident) => (
                  <TableRow key={incident.id} sx={{ borderBottom: '1px solid rgba(56,78,112,0.03)' }}>
                    <TableCell sx={{ color: '#5A6B8A', fontSize: '0.75rem' }}>
                      {new Date(incident.timestamp).toLocaleTimeString()}
                    </TableCell>
                    <TableCell sx={{ color: '#E8EDF5', fontSize: '0.8rem' }}>
                      {getIncidentIcon(incident.type)} {incident.type}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={incident.severity}
                        size="small"
                        sx={{
                          bgcolor: `${getSeverityColor(incident.severity)}15`,
                          color: getSeverityColor(incident.severity),
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={incident.status}
                        size="small"
                        sx={{
                          bgcolor: 'rgba(16,185,129,0.08)',
                          color: '#10B981',
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Box>
  );
}
```

## frontend/src/pages/MaintenancePlanner.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/MaintenancePlanner.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  useTheme,
  Alert,
} from '@mui/material';
import {
  Build,
  CheckCircle,
  Warning,
  Error,
  Circle,
  Schedule,
  PriorityHigh,
} from '@mui/icons-material';
import { getMaintenancePlan } from '../api/client';

// ✅ Mock data for when API fails
const MOCK_TASKS = [
  { priority: 'P1', asset: 'Heat Exchanger H-03', workOrder: 'Inspect thermal bypass', owner: 'Utilities Crew', state: 'Scheduled' },
  { priority: 'P1', asset: 'Compressor C-12', workOrder: 'Bearing and vibration inspection', owner: 'Rotating Equipment', state: 'In Progress' },
  { priority: 'P2', asset: 'Valve V-09', workOrder: 'Calibrate pressure actuator', owner: 'Instrumentation', state: 'Pending' },
  { priority: 'P2', asset: 'Pump A-01', workOrder: 'Replace seals and gaskets', owner: 'Rotating Equipment', state: 'Scheduled' },
  { priority: 'P3', asset: 'Tank T-04', workOrder: 'Inspect level sensors', owner: 'Instrumentation', state: 'Pending' },
  { priority: 'P3', asset: 'Pipeline P-03', workOrder: 'Corrosion inspection', owner: 'Pipeline Crew', state: 'Completed' },
];

const PRIORITY_COLORS = {
  'P1': '#EF4444',
  'P2': '#F59E0B',
  'P3': '#3B82F6',
  'P4': '#10B981',
};

const PRIORITY_LABELS = {
  'P1': 'Critical',
  'P2': 'High',
  'P3': 'Medium',
  'P4': 'Low',
};

export default function MaintenancePlanner() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const response = await getMaintenancePlan();
      const data = response.data;
      
      // ✅ Handle different response formats
      let taskArray = [];
      if (Array.isArray(data)) {
        taskArray = data;
      } else if (data?.tasks && Array.isArray(data.tasks)) {
        taskArray = data.tasks;
      } else if (data?.data && Array.isArray(data.data)) {
        taskArray = data.data;
      } else {
        taskArray = MOCK_TASKS;
      }
      
      setTasks(taskArray.length > 0 ? taskArray : MOCK_TASKS);
    } catch (e) {
      console.error('Failed to load maintenance plan, using mock data:', e);
      setTasks(MOCK_TASKS);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    return PRIORITY_COLORS[priority] || '#8899B4';
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading maintenance plan...</Typography>
      </Box>
    );
  }

  const totalTasks = tasks.length;
  const criticalTasks = tasks.filter(t => t.priority === 'P1').length;
  const completedTasks = tasks.filter(t => t.state === 'Completed').length;
  const inProgressTasks = tasks.filter(t => t.state === 'In Progress').length;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Maintenance Planner
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {totalTasks} tasks · {criticalTasks} critical
          </Typography>
        </Box>
        <Chip
          label={`${completedTasks}/${totalTasks} completed`}
          sx={{
            bgcolor: 'rgba(16,185,129,0.08)',
            color: '#10B981',
            border: '1px solid rgba(16,185,129,0.15)',
          }}
        />
      </Box>

      {/* Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total Tasks
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {totalTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Critical
              </Typography>
              <Typography variant="h5" sx={{ color: '#EF4444', fontWeight: 600 }}>
                {criticalTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Completed
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {completedTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                In Progress
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {inProgressTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Task Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Priority</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Asset</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Work Order</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Owner</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No maintenance tasks scheduled
                </TableCell>
              </TableRow>
            ) : (
              tasks.map((task, index) => {
                const priorityColor = getPriorityColor(task.priority);
                const isCompleted = task.state === 'Completed';
                const isCritical = task.priority === 'P1';
                const isInProgress = task.state === 'In Progress';
                
                let statusColor = '#5A6B8A';
                if (isCompleted) statusColor = '#10B981';
                else if (isInProgress) statusColor = '#F59E0B';
                else if (isCritical) statusColor = '#EF4444';

                const icon = isCompleted ? 
                  <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} /> : 
                  isCritical ? 
                  <Error sx={{ fontSize: 14, color: '#EF4444' }} /> :
                  <Warning sx={{ fontSize: 14, color: '#F59E0B' }} />;

                return (
                  <TableRow
                    key={index}
                    sx={{
                      borderBottom: '1px solid rgba(56,78,112,0.05)',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                      opacity: isCompleted ? 0.6 : 1,
                    }}
                  >
                    <TableCell>
                      <Chip
                        icon={icon}
                        label={`${task.priority} - ${PRIORITY_LABELS[task.priority] || ''}`}
                        size="small"
                        sx={{
                          bgcolor: `${priorityColor}15`,
                          color: priorityColor,
                          border: `1px solid ${priorityColor}20`,
                          fontSize: '0.65rem',
                          fontWeight: 500,
                          height: 24,
                        }}
                      />
                    </TableCell>
                    <TableCell sx={{ color: '#E8EDF5' }}>{task.asset || 'N/A'}</TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{task.workOrder || task.description || 'N/A'}</TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{task.owner || 'Unassigned'}</TableCell>
                    <TableCell>
                      <Chip
                        label={task.state || 'Pending'}
                        size="small"
                        sx={{
                          bgcolor: `${statusColor}15`,
                          color: statusColor,
                          border: `1px solid ${statusColor}20`,
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Summary Alert */}
      {criticalTasks > 0 && (
        <Alert severity="error" sx={{ mt: 2 }}>
          <Typography variant="body2">
            ⚠️ {criticalTasks} critical task(s) require immediate attention!
          </Typography>
        </Alert>
      )}
    </Box>
  );
}
```

## frontend/src/pages/Reports.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/Reports.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Alert,
} from '@mui/material';
import {
  Description,
  Download,
  CheckCircle,
  Warning,
  Error,
  Circle,
  Refresh,
} from '@mui/icons-material';
import { getReports } from '../api/client';

// ✅ Mock data for when API fails
const MOCK_REPORTS = [
  { id: 'RPT-0001', title: 'Incident Response Report', workflow: 'Pressure Response', status: 'Completed', generated: '2026-07-25 00:25:00', summary: 'Pressure spike resolved successfully', recommendations: ['Inspect relief valve', 'Monitor pressure'] },
  { id: 'RPT-0002', title: 'Maintenance Summary', workflow: 'Maintenance Response', status: 'Pending', generated: '2026-07-25 00:20:00', summary: 'Maintenance tasks scheduled', recommendations: ['Schedule inspection'] },
  { id: 'RPT-0003', title: 'Asset Health Report', workflow: 'Health Check', status: 'Completed', generated: '2026-07-25 00:15:00', summary: 'All assets within parameters', recommendations: ['Continue monitoring'] },
  { id: 'RPT-0004', title: 'Safety Analysis', workflow: 'Safety Check', status: 'Escalated', generated: '2026-07-25 00:10:00', summary: 'Safety concern detected', recommendations: ['Immediate inspection required'] },
  { id: 'RPT-0005', title: 'Prediction Report', workflow: 'Prediction', status: 'In Progress', generated: '2026-07-25 00:05:00', summary: 'Calculating failure probabilities', recommendations: [] },
];

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await getReports();
      // ✅ Ensure reports is always an array
      const data = response.data;
      if (Array.isArray(data)) {
        setReports(data);
      } else if (data && typeof data === 'object') {
        // If it's an object, try to find array property
        const arrayData = data.reports || data.tasks || data.results || data.items;
        if (Array.isArray(arrayData)) {
          setReports(arrayData);
        } else {
          console.warn('Reports data is not an array, using mock data');
          setReports(MOCK_REPORTS);
        }
      } else {
        setReports(MOCK_REPORTS);
      }
    } catch (e) {
      console.error('Failed to load reports, using mock data:', e);
      setReports(MOCK_REPORTS);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'Completed': '#10B981',
      'Pending': '#F59E0B',
      'Escalated': '#EF4444',
      'In Progress': '#3B82F6',
    };
    return colors[status] || '#8899B4';
  };

  const getStatusIcon = (status) => {
    const icons = {
      'Completed': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
      'Pending': <Warning sx={{ fontSize: 14, color: '#F59E0B' }} />,
      'Escalated': <Error sx={{ fontSize: 14, color: '#EF4444' }} />,
      'In Progress': <Circle sx={{ fontSize: 10, color: '#3B82F6' }} />,
    };
    return icons[status] || <Circle sx={{ fontSize: 10, color: '#8899B4' }} />;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading reports...</Typography>
      </Box>
    );
  }

  const totalReports = reports.length;
  const completedReports = reports.filter(r => r.status === 'Completed').length;
  const pendingReports = reports.filter(r => r.status === 'Pending').length;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Reports & Intelligence
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {totalReports} reports generated
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={loadData}
          sx={{
            borderColor: 'rgba(56,78,112,0.2)',
            color: '#8899B4',
            '&:hover': { borderColor: 'rgba(56,78,112,0.4)' },
          }}
        >
          Refresh
        </Button>
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total Reports
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {totalReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Completed
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {completedReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Pending Review
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {pendingReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Escalated
              </Typography>
              <Typography variant="h5" sx={{ color: '#EF4444', fontWeight: 600 }}>
                {totalReports - completedReports - pendingReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Report</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Title</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Workflow</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Generated</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reports.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No reports generated yet
                </TableCell>
              </TableRow>
            ) : (
              reports.map((report, index) => {
                const statusColor = getStatusColor(report.status);
                return (
                  <TableRow
                    key={index}
                    sx={{
                      borderBottom: '1px solid rgba(56,78,112,0.05)',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                      cursor: 'pointer',
                    }}
                    onClick={() => setSelectedReport(selectedReport === index ? null : index)}
                  >
                    <TableCell sx={{ color: '#3B82F6', fontWeight: 500, fontSize: '0.8rem' }}>
                      {report.id || `RPT-${String(index + 1).padStart(4, '0')}`}
                    </TableCell>
                    <TableCell sx={{ color: '#E8EDF5' }}>{report.title || report.workflow || 'Untitled'}</TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{report.workflow || 'N/A'}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getStatusIcon(report.status)}
                        label={report.status || 'Unknown'}
                        size="small"
                        sx={{
                          bgcolor: `${statusColor}15`,
                          color: statusColor,
                          border: `1px solid ${statusColor}20`,
                          fontSize: '0.65rem',
                          fontWeight: 500,
                          height: 24,
                        }}
                      />
                    </TableCell>
                    <TableCell sx={{ color: '#5A6B8A', fontSize: '0.75rem' }}>
                      {report.generated || report.timestamp || 'N/A'}
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        startIcon={<Download sx={{ fontSize: 14 }} />}
                        sx={{
                          color: '#3B82F6',
                          fontSize: '0.65rem',
                          textTransform: 'none',
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          // Download logic
                        }}
                      >
                        Export
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {selectedReport !== null && reports[selectedReport] && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
            Report Detail
          </Typography>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ color: '#E8EDF5' }}>
              {reports[selectedReport].summary || 'No summary available for this report.'}
            </Typography>
          </Alert>
          <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
            Recommendations: {reports[selectedReport].recommendations?.length || 0}
          </Typography>
        </Paper>
      )}
    </Box>
  );
}
```

## frontend/src/styles/theme.js

**Folder path:** `frontend/src/styles`

**File path:** `frontend/src/styles/theme.js`

```javascript
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3B82F6',      // Industrial blue
      light: '#60A5FA',
      dark: '#1D4ED8',
    },
    secondary: {
      main: '#10B981',      // Status green
      light: '#34D399',
      dark: '#059669',
    },
    error: {
      main: '#EF4444',      // Alert red
    },
    warning: {
      main: '#F59E0B',      // Warning amber
    },
    info: {
      main: '#3B82F6',
    },
    success: {
      main: '#10B981',
    },
    background: {
      default: '#0A0F1A',
      paper: 'rgba(18, 28, 46, 0.92)',
    },
    text: {
      primary: '#E8EDF5',
      secondary: '#8899B4',
    },
  },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    h1: {
      fontWeight: 600,
      color: '#E8EDF5',
      fontSize: '2.25rem',
      letterSpacing: '-0.02em',
    },
    h4: {
      fontWeight: 600,
      color: '#E8EDF5',
      letterSpacing: '-0.01em',
    },
    h5: {
      fontWeight: 500,
      color: '#E8EDF5',
    },
    h6: {
      fontWeight: 500,
      color: '#8899B4',
      textTransform: 'uppercase',
      letterSpacing: '0.08em',
      fontSize: '0.75rem',
    },
    body1: {
      color: '#E8EDF5',
    },
    body2: {
      color: '#8899B4',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'rgba(18, 28, 46, 0.85)',
          border: '1px solid rgba(56, 78, 112, 0.15)',
          borderRadius: '8px',
          boxShadow: '0 4px 24px rgba(0,0,0,0.3)',
          transition: 'all 0.2s ease',
          '&:hover': {
            borderColor: 'rgba(59, 130, 246, 0.2)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'rgba(18, 28, 46, 0.85)',
          border: '1px solid rgba(56, 78, 112, 0.12)',
          borderRadius: '8px',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: 'rgba(10, 15, 26, 0.98)',
          borderRight: '1px solid rgba(56, 78, 112, 0.1)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'rgba(10, 15, 26, 0.92)',
          backdropFilter: 'blur(12px)',
          borderBottom: '1px solid rgba(56, 78, 112, 0.08)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '6px',
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
  },
});
```
