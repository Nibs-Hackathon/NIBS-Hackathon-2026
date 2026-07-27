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
