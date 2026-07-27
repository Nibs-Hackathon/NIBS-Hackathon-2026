# Folder: frontend/src Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src`

Contains 4 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/App.css

**Folder path:** `frontend/src`

**File path:** `frontend/src/App.css`

```css
/* Global visual rules live in index.css and the RigOS MUI theme.
   This file is intentionally kept free of legacy Vite starter styles. */
```

## frontend/src/App.jsx

**Folder path:** `frontend/src`

**File path:** `frontend/src/App.jsx`

```javascript
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { Toaster } from 'react-hot-toast';
import { OperationsProvider } from './context/OperationsContext';
import { ColorModeProvider, useColorMode } from './context/ColorModeContext';
import { WorkspaceProvider } from './context/WorkspaceContext';
import { ObjectProvider } from './context/ObjectContext';
import { ProductShell } from './redesign/ProductShell';
import { ProductPage } from './redesign/ProductPage';
import './redesign/product.css';

const createProductTheme = (mode) => createTheme({
  palette: {
    mode,
    primary: { main: '#4f8cff' },
    success: { main: '#22c55e' },
    warning: { main: '#f59e0b' },
    error: { main: '#ef4444' },
    background: {
      default: mode === 'dark' ? '#090b0f' : '#f6f7f9',
      paper: mode === 'dark' ? '#111418' : '#fff',
    },
    text: {
      primary: mode === 'dark' ? '#f8fafc' : '#111827',
      secondary: mode === 'dark' ? '#94a3b8' : '#64748b',
    },
  },
  typography: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  },
  shape: { borderRadius: 14 },
  components: {
    MuiButton: {
      styleOverrides: {
        root: { textTransform: 'none', fontWeight: 700, borderRadius: 10, boxShadow: 'none' },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: { backgroundImage: 'none' },
      },
    },
  },
});

const PRODUCT_PATHS = [
  '/',
  '/assets',
  '/incident-simulator',
  '/agent-monitor',
  '/maintenance',
  '/health-prediction',
  '/reports',
];

function RoutedApp() {
  const { mode } = useColorMode();
  const dark = mode === 'dark';
  return (
    <ThemeProvider theme={createProductTheme(mode)}>
      <CssBaseline />
      <BrowserRouter>
        <OperationsProvider>
          <ObjectProvider>
            <WorkspaceProvider>
              <ProductShell>
                <Routes>
                  {PRODUCT_PATHS.map((path) => (
                    <Route key={path} path={path} element={<ProductPage />} />
                  ))}
                  <Route path="/digital-twin" element={<Navigate to="/assets" replace />} />
                  <Route path="/ai-activity" element={<Navigate to="/agent-monitor" replace />} />
                  <Route path="/incidents" element={<Navigate to="/incident-simulator" replace />} />
                  <Route path="/investigation" element={<Navigate to="/agent-monitor" replace />} />
                  <Route path="/forecasting" element={<Navigate to="/health-prediction" replace />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </ProductShell>
            </WorkspaceProvider>
          </ObjectProvider>
        </OperationsProvider>
      </BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: dark ? '#171b21' : '#ffffff',
            color: dark ? '#f8fafc' : '#111827',
            border: `1px solid ${dark ? 'rgba(255,255,255,.10)' : '#e5e7eb'}`,
            borderRadius: '12px',
            boxShadow: '0 12px 30px rgba(0,0,0,.16)',
          },
        }}
      />
    </ThemeProvider>
  );
}

export default function App() {
  return (
    <ColorModeProvider>
      <RoutedApp />
    </ColorModeProvider>
  );
}
```

## frontend/src/index.css

**Folder path:** `frontend/src`

**File path:** `frontend/src/index.css`

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;750;800&display=swap');

:root {
  --rigos-cyan: #55d6ff;
  --rigos-blue: #1677ff;
  --rigos-violet: #6d5dfb;
  --rigos-emerald: #12b981;
  --rigos-amber: #f59e0b;
  --rigos-red: #ef4444;
  --rigos-ease: cubic-bezier(.2,.8,.2,1);
}

* { box-sizing: border-box; }
html { min-height: 100%; background: #08111f; }
html[data-rigos-theme='light'] { background: #f4f7fb; }
body { margin: 0; min-width: 320px; min-height: 100vh; font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
button, input, textarea, select { font: inherit; }

::selection { background: rgba(85, 214, 255, .3); }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(126, 156, 190, .32); border: 2px solid transparent; border-radius: 20px; background-clip: padding-box; }
::-webkit-scrollbar-thumb:hover { background-color: rgba(85, 214, 255, .52); }

@keyframes rigos-pulse { 0%,100% { opacity: 1; transform: scale(1); } 50% { opacity: .58; transform: scale(.92); } }
@keyframes rigos-shimmer { from { background-position: 180% 0; } to { background-position: -180% 0; } }
@keyframes rigos-fade-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.live-dot { animation: rigos-pulse 2s var(--rigos-ease) infinite; }
.telemetry-shimmer { background: linear-gradient(100deg, transparent 30%, rgba(85,214,255,.24) 50%, transparent 70%); background-size: 220% 100%; animation: rigos-shimmer 2.5s linear infinite; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
}
```

## frontend/src/main.jsx

**Folder path:** `frontend/src`

**File path:** `frontend/src/main.jsx`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import './styles/premium.css';
import './design-system/primitives.css';
import './redesign/twin.css';
import './redesign/workspace-twin.css';
import './redesign/incident-management.css';
import './redesign/maintenance-planning.css';
import './redesign/ai-investigation.css';
import './redesign/forecast-terminal.css';
import './redesign/executive-briefing.css';
import './redesign/mission-control-os.css';
import './redesign/polish.css';
import './redesign/ambient.css';
import './redesign/copilot.css';
import './redesign/workspace.css';
import './redesign/final-polish.css';
import './design-system/catalog.css';
import './redesign/accountability.css';
import './redesign/interaction.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
