# Folder: frontend/src/styles Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/styles`

Contains 2 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/styles/premium.css

**Folder path:** `frontend/src/styles`

**File path:** `frontend/src/styles/premium.css`

```css
:root { --app-bg:#090b0f; --surface:#111418; --surface-raised:#171b21; --text:#f8fafc; --muted:#94a3b8; --line:rgba(255,255,255,.08); --blue:#4f8cff; --green:#22c55e; --amber:#f59e0b; --red:#ef4444; }
.premium-page { max-width: 1540px; margin: 0 auto; padding: 12px 0 48px; }.premium-page-hero { margin-bottom: 48px; }.premium-eyebrow { color: var(--muted); font-size: .68rem !important; font-weight: 800 !important; letter-spacing: .14em !important; text-transform: uppercase; }.premium-title { max-width: 900px; margin-top: 10px !important; color: var(--text); font-size: clamp(2.9rem, 5.2vw, 5.75rem) !important; font-weight: 780 !important; line-height: .94 !important; letter-spacing: -.065em !important; }.premium-description { max-width: 660px; margin-top: 18px !important; color: var(--muted); font-size: 1rem !important; line-height: 1.65 !important; }.premium-section-header { margin: 48px 0 22px; }.premium-section-title { margin-top: 7px !important; font-size: clamp(1.5rem,2.4vw,2.25rem) !important; font-weight: 760 !important; letter-spacing: -.045em !important; }.premium-section-description { margin-top: 7px !important; color: var(--muted); }.premium-surface { border: 1px solid var(--line) !important; border-radius: 18px !important; background: var(--surface) !important; box-shadow: 0 14px 38px rgba(0,0,0,.14) !important; }.premium-surface.is-interactive { transition: transform 180ms cubic-bezier(.2,.8,.2,1), border-color 180ms ease, background 180ms ease; }.premium-surface.is-interactive:hover { transform: translateY(-2px); border-color: rgba(255,255,255,.14) !important; background: var(--surface-raised) !important; }.premium-status { height: 26px !important; border-radius: 999px !important; font-size: .66rem !important; font-weight: 800 !important; letter-spacing: .08em !important; }.premium-status i { display:inline-block; width:6px; height:6px; margin-right:7px; border-radius:50%; vertical-align:middle; }.premium-status i.is-pulsing { animation: premium-pulse 1.8s ease-in-out infinite; }.premium-stat-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:0; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }.premium-metric { min-height:126px; padding:24px 28px; border-right:1px solid var(--line); }.premium-metric:last-child { border-right:0; }.premium-metric-label { color:var(--muted); font-size:.68rem !important; font-weight:800 !important; letter-spacing:.11em !important; text-transform:uppercase; }.premium-metric-value { display:flex; align-items:center; min-height:44px; margin-top:7px !important; font-size:clamp(2rem,3.4vw,3.25rem) !important; font-weight:780 !important; letter-spacing:-.065em !important; line-height:1 !important; }.premium-metric-detail { margin-top:7px !important; color:var(--muted); font-size:.77rem !important; }.premium-search .MuiOutlinedInput-root { border-radius:12px; background:var(--surface-raised); }.premium-search .MuiOutlinedInput-notchedOutline { border-color:var(--line) !important; }.premium-progress .MuiLinearProgress-root { height:5px; margin-top:7px; border-radius:99px; background:rgba(255,255,255,.07); }.premium-empty { min-height:230px; display:grid; place-content:center; gap:9px; text-align:center; }.premium-empty-mark { width:30px; height:30px; justify-self:center; border:1px solid rgba(79,140,255,.65); border-radius:10px; box-shadow:inset 0 0 0 6px rgba(79,140,255,.08); }.premium-primary-button { border-radius:11px !important; background:var(--blue) !important; box-shadow:none !important; font-weight:750 !important; }.premium-primary-button:hover { background:#679cff !important; transform:translateY(-1px); }
@keyframes premium-pulse { 50% { opacity:.45; transform:scale(.78); } } @media (max-width:900px) { .premium-stat-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }.premium-metric:nth-child(2) { border-right:0; }.premium-metric:nth-child(-n+2) { border-bottom:1px solid var(--line); } } @media (max-width:520px) { .premium-page { padding-top:4px; }.premium-page-hero { margin-bottom:34px; }.premium-stat-grid { grid-template-columns:1fr; }.premium-metric, .premium-metric:nth-child(2) { border-right:0; border-bottom:1px solid var(--line); }.premium-metric:last-child { border-bottom:0; } }
```

## frontend/src/styles/theme.js

**Folder path:** `frontend/src/styles`

**File path:** `frontend/src/styles/theme.js`

```javascript
import { createTheme } from '@mui/material/styles';

export const createRigOSTheme = (mode) => {
  const dark = mode === 'dark';
  const canvas = dark ? '#08111F' : '#F4F7FB';
  const ink = dark ? '#EDF5FF' : '#16243A';
  const muted = dark ? '#93A5C2' : '#687A92';
  const glass = dark ? 'rgba(14, 27, 46, 0.76)' : 'rgba(255, 255, 255, 0.72)';
  const border = dark ? 'rgba(126, 174, 218, 0.14)' : 'rgba(44, 92, 138, 0.12)';

  return createTheme({
    palette: {
      mode,
      primary: { main: '#1677FF', light: '#55D6FF', dark: '#0F5CC8' },
      secondary: { main: '#6D5DFB' },
      success: { main: '#12B981' }, warning: { main: '#F59E0B' }, error: { main: '#EF4444' },
      background: { default: canvas, paper: glass },
      text: { primary: ink, secondary: muted },
    },
    typography: {
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      h4: { fontSize: 'clamp(1.65rem, 2.7vw, 2.35rem)', fontWeight: 750, letterSpacing: '-0.045em' },
      h5: { fontWeight: 700, letterSpacing: '-0.025em' },
      body2: { lineHeight: 1.55 },
    },
    shape: { borderRadius: 16 },
    components: {
      MuiCssBaseline: { styleOverrides: { body: { background: canvas, color: ink, transition: 'background .25s ease, color .25s ease' } } },
      MuiPaper: { styleOverrides: { root: { background: glass, backdropFilter: 'blur(20px)', border: `1px solid ${border}`, boxShadow: dark ? '0 18px 50px rgba(0,0,0,.22)' : '0 16px 45px rgba(54,83,118,.10)' } } },
      MuiCard: { styleOverrides: { root: { background: glass, backdropFilter: 'blur(20px)', border: `1px solid ${border}`, boxShadow: dark ? '0 16px 42px rgba(0,0,0,.18)' : '0 14px 38px rgba(54,83,118,.08)' } } },
      MuiButton: { styleOverrides: { root: { textTransform: 'none', fontWeight: 700, borderRadius: 10, boxShadow: 'none' } } },
    },
  });
};
```
