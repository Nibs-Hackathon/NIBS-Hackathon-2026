export const rigosV2Tokens = {
  color: {
    graphite: '#0A0D12', graphiteRaised: '#111722', graphiteGlass: 'rgba(17, 23, 34, 0.72)',
    cloud: '#F7F9FC', cloudGlass: 'rgba(255, 255, 255, 0.74)', ink: '#EEF4FC', inkLight: '#132238',
    muted: '#93A2B8', mutedLight: '#65758B', cyan: '#58D8FF', blue: '#287CFF', emerald: '#22C58B',
    amber: '#F5AE38', red: '#F25F5C', violet: '#9772FF', borderDark: 'rgba(164, 196, 228, 0.14)', borderLight: 'rgba(35, 66, 104, 0.12)',
  },
  spacing: { 0: 0, 1: 4, 2: 8, 3: 12, 4: 16, 5: 20, 6: 24, 8: 32, 10: 40, 12: 48, 16: 64, 20: 80, 24: 96 },
  radius: { sm: 10, md: 14, lg: 18, xl: 24, pill: 999 },
  elevation: {
    low: '0 8px 24px rgba(0, 0, 0, 0.12)', medium: '0 16px 44px rgba(0, 0, 0, 0.18)', high: '0 28px 72px rgba(0, 0, 0, 0.26)',
    glowCyan: '0 0 32px rgba(88, 216, 255, 0.22)', glowViolet: '0 0 34px rgba(151, 114, 255, 0.22)',
  },
  blur: { surface: 'blur(18px)', overlay: 'blur(28px)', dense: 'blur(44px)' },
  motion: {
    instant: '110ms', fast: '170ms', normal: '240ms', slow: '420ms', deliberate: '640ms',
    standard: 'cubic-bezier(0.2, 0.8, 0.2, 1)', enter: 'cubic-bezier(0, 0.8, 0.2, 1)', exit: 'cubic-bezier(0.4, 0, 1, 1)',
  },
  typography: {
    display: { fontSize: 'clamp(3.25rem, 8vw, 7rem)', lineHeight: 0.92, fontWeight: 800, letterSpacing: '-0.07em' },
    hero: { fontSize: 'clamp(2.35rem, 5vw, 5rem)', lineHeight: 0.96, fontWeight: 780, letterSpacing: '-0.06em' },
    heading: { fontSize: 'clamp(1.55rem, 2.5vw, 2.35rem)', lineHeight: 1.04, fontWeight: 750, letterSpacing: '-0.045em' },
    title: { fontSize: '1rem', lineHeight: 1.3, fontWeight: 750, letterSpacing: '-0.02em' },
    body: { fontSize: '0.9rem', lineHeight: 1.6, fontWeight: 500 },
    caption: { fontSize: '0.68rem', lineHeight: 1.35, fontWeight: 750, letterSpacing: '0.12em' },
    mono: { fontFamily: '"DM Mono", "SFMono-Regular", Consolas, monospace', fontSize: '0.75rem', lineHeight: 1.5, fontWeight: 500 },
  },
};

export const semanticTone = {
  neutral: { main: '#93A2B8', soft: 'rgba(147, 162, 184, 0.14)' }, info: { main: '#58D8FF', soft: 'rgba(88, 216, 255, 0.13)' },
  success: { main: '#22C58B', soft: 'rgba(34, 197, 139, 0.13)' }, warning: { main: '#F5AE38', soft: 'rgba(245, 174, 56, 0.14)' },
  danger: { main: '#F25F5C', soft: 'rgba(242, 95, 92, 0.14)' }, violet: { main: '#9772FF', soft: 'rgba(151, 114, 255, 0.14)' },
};
