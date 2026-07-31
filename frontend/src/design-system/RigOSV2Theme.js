import { createTheme } from '@mui/material/styles';
import { rigosV2Tokens } from './tokens';

export function createRigOSV2Theme(mode = 'dark') {
  const { color, radius, elevation, blur, typography } = rigosV2Tokens;
  const dark = mode === 'dark';
  const background = dark ? color.graphite : color.cloud;
  const paper = dark ? color.graphiteGlass : color.cloudGlass;
  const text = dark ? color.ink : color.inkLight;
  const secondary = dark ? color.muted : color.mutedLight;
  return createTheme({
    palette: { mode, primary: { main: color.blue }, secondary: { main: color.violet }, info: { main: color.cyan }, success: { main: color.emerald }, warning: { main: color.amber }, error: { main: color.red }, background: { default: background, paper }, text: { primary: text, secondary } },
    shape: { borderRadius: radius.md },
    typography: { fontFamily: '"IBM Plex Sans", "Segoe UI", sans-serif', h1: typography.display, h2: typography.hero, h3: typography.heading, body2: typography.body, caption: typography.caption },
    components: {
      MuiPaper: { styleOverrides: { root: { borderRadius: radius.lg, backdropFilter: blur.surface, border: `1px solid ${dark ? color.borderDark : color.borderLight}`, boxShadow: elevation.low } } },
      MuiButton: { styleOverrides: { root: { borderRadius: radius.md, textTransform: 'none', fontWeight: 750, boxShadow: 'none' } } },
    },
  });
}
