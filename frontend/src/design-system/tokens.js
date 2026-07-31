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
    crossfade: '200ms', select: '120ms', pulse: '400ms',
    standard: 'cubic-bezier(0.2, 0.8, 0.2, 1)', enter: 'cubic-bezier(0, 0.8, 0.2, 1)', exit: 'cubic-bezier(0.4, 0, 1, 1)',
  },
  typography: {
    display: { fontSize: '1.75rem', lineHeight: 1.15, fontWeight: 600, letterSpacing: '-0.02em' },
    heading: { fontSize: '1.125rem', lineHeight: 1.25, fontWeight: 600, letterSpacing: '-0.01em' },
    body: { fontSize: '0.8125rem', lineHeight: 1.45, fontWeight: 450 },
    data: { fontSize: '0.8125rem', lineHeight: 1.35, fontWeight: 600, fontVariantNumeric: 'tabular-nums' },
    kpi: { fontSize: '2.05rem', lineHeight: 1.05, fontWeight: 780, letterSpacing: '-0.045em', fontVariantNumeric: 'tabular-nums' },
    label: { fontSize: '0.62rem', lineHeight: 1.3, fontWeight: 750, letterSpacing: '0.12em', textTransform: 'uppercase' },
    mono: { fontFamily: '"DM Mono", "SFMono-Regular", Consolas, monospace', fontSize: '0.75rem', lineHeight: 1.5, fontWeight: 500 },
    hero: { fontSize: 'clamp(2.35rem, 5vw, 5rem)', lineHeight: 0.96, fontWeight: 780, letterSpacing: '-0.06em' },
    title: { fontSize: '1rem', lineHeight: 1.3, fontWeight: 750, letterSpacing: '-0.02em' },
    caption: { fontSize: '0.68rem', lineHeight: 1.35, fontWeight: 750, letterSpacing: '0.12em' },
  },
  pane: { explorer: 240, queue: 280, inspector: 320, dossier: 360 },
  strip: { toolbar: 48, operations: 56, decision: 64, audit: 32 },
};

/** Control-room status colors from DESIGN_SYSTEM.md */
export const statusColors = {
  nominal: { main: '#22A06B', soft: 'rgba(34, 160, 107, 0.14)' },
  advisory: { main: '#F5A524', soft: 'rgba(245, 165, 36, 0.14)' },
  attention: { main: '#E56910', soft: 'rgba(229, 105, 16, 0.14)' },
  critical: { main: '#E2483D', soft: 'rgba(226, 72, 61, 0.14)' },
  offline: { main: '#6B7785', soft: 'rgba(107, 119, 133, 0.14)' },
  'ai-active': { main: '#5E4DB2', soft: 'rgba(94, 77, 178, 0.14)' },
  info: { main: '#2684FF', soft: 'rgba(38, 132, 255, 0.14)' },
};

export const semanticTone = {
  neutral: { main: '#93A2B8', soft: 'rgba(147, 162, 184, 0.14)' },
  info: statusColors.info,
  success: statusColors.nominal,
  warning: statusColors.advisory,
  danger: statusColors.critical,
  violet: { main: '#9772FF', soft: 'rgba(151, 114, 255, 0.14)' },
  nominal: statusColors.nominal,
  advisory: statusColors.advisory,
  attention: statusColors.attention,
  critical: statusColors.critical,
  offline: statusColors.offline,
  'ai-active': statusColors['ai-active'],
};

export function resolveTone(name = 'neutral') {
  return semanticTone[name] || statusColors[name] || semanticTone.neutral;
}
