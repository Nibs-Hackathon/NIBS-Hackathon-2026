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
