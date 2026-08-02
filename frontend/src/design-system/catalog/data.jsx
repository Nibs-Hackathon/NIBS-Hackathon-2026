import { Box, Stack, Typography } from '@mui/material';
import { Terminal } from '@mui/icons-material';
import { ProvenanceBadge, StatusBadge } from './status';
import { resolveTone } from '../tokens';

function DataCardShell({ className = '', loading, children, sx, ...props }) {
  return (
    <Box className={`rig-data-card ${loading ? 'is-loading' : ''} ${className}`} aria-busy={loading || undefined} sx={sx} {...props}>
      {children}
    </Box>
  );
}

/** MetricCard — KPI + delta + optional sparkline + provenance */
export function MetricCard({
  label, value, detail, delta, tone = 'neutral', provenance, loading = false, children, className = '', sx,
}) {
  const t = resolveTone(tone);
  return (
    <DataCardShell className={`rig-metric-card ${className}`} loading={loading} sx={sx}>
      <Stack direction="row" justifyContent="space-between" alignItems="flex-start" spacing={1}>
        <Typography className="rig-label">{label}</Typography>
        {provenance && <ProvenanceBadge value={provenance} />}
      </Stack>
      <Stack direction="row" alignItems="baseline" spacing={1} sx={{ mt: 0.75 }}>
        <Typography className="rig-kpi">{loading ? '—' : value}</Typography>
        {delta != null && !loading && (
          <Typography className="rig-data" sx={{ color: t.main }}>{delta}</Typography>
        )}
      </Stack>
      {detail && <Typography variant="caption" color="text.secondary">{detail}</Typography>}
      {children}
    </DataCardShell>
  );
}

/** SignalCard — tag name + value + unit + threshold bar */
export function SignalCard({
  name, value, unit, threshold = 100, tone, provenance = 'live', loading = false, className = '', sx,
}) {
  const num = Number(value);
  const pct = Number.isFinite(num) && threshold ? Math.max(0, Math.min(100, (num / threshold) * 100)) : 0;
  const status = tone || (pct >= 90 ? 'critical' : pct >= 75 ? 'attention' : 'nominal');
  const t = resolveTone(status);
  return (
    <DataCardShell className={`rig-signal-card ${className}`} loading={loading} sx={sx}>
      <Stack direction="row" sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography className="rig-label">{name}</Typography>
        <ProvenanceBadge value={provenance} />
      </Stack>
      <Typography className="rig-kpi" sx={{ mt: 0.5 }}>
        {loading ? '—' : Number.isFinite(num) ? num.toFixed(1) : value ?? '—'}
        {unit && <Typography component="span" className="rig-data" sx={{ ml: 0.5, opacity: 0.7 }}>{unit}</Typography>}
      </Typography>
      <Box sx={{ mt: 1, height: 4, borderRadius: 99, bgcolor: 'action.hover', overflow: 'hidden' }}>
        <Box
          sx={{
            width: '100%',
            height: '100%',
            bgcolor: t.main,
            transformOrigin: 'left center',
            transform: `scaleX(${Math.max(0, Math.min(1, pct / 100))})`,
            transition: 'transform 200ms ease',
          }}
        />
      </Box>
    </DataCardShell>
  );
}

/** HealthRing — 0–100 with threshold ticks */
export function HealthRing({ value = 0, label = 'Health', size = 96, loading = false, className = '', sx }) {
  const pct = Math.max(0, Math.min(100, Number(value) || 0));
  const status = pct < 50 ? 'critical' : pct < 80 ? 'attention' : 'nominal';
  const color = resolveTone(status).main;
  return (
    <Box
      className={`rig-health-ring ${className}`}
      style={{ width: size, height: size, background: `conic-gradient(${color} ${pct * 3.6}deg, rgba(128,148,177,.16) 0)` }}
      sx={sx}
      role="img"
      aria-label={`${label} ${Math.round(pct)}%`}
    >
      <Box className="rig-health-ring-inner" style={{ inset: size * 0.12 }}>
        {loading ? <Typography className="rig-data">—</Typography> : (
          <>
            <Typography className="rig-kpi" sx={{ fontSize: size * 0.22, color }}>{Math.round(pct)}%</Typography>
            <Typography className="rig-label" sx={{ fontSize: 9 }}>{label}</Typography>
          </>
        )}
      </Box>
    </Box>
  );
}

/** Sparkline — inline trend, no axes unless expanded */
export function Sparkline({ values = [], color, height = 40, label, className = '', sx }) {
  const pts = (Array.isArray(values) ? values : []).map(Number).filter(Number.isFinite);
  if (!pts.length) {
    return <Box className={className} sx={{ height, ...sx }} aria-label={label || 'No trend data'} />;
  }
  const min = Math.min(...pts);
  const max = Math.max(...pts);
  const span = max - min || 1;
  const w = 120;
  const h = height;
  const path = pts.map((v, i) => {
    const x = (i / Math.max(pts.length - 1, 1)) * w;
    const y = h - ((v - min) / span) * (h - 4) - 2;
    return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`;
  }).join(' ');
  const stroke = color || resolveTone('info').main;
  return (
    <Box className={`rig-sparkline ${className}`} sx={{ height, ...sx }}>
      <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={height} aria-label={label || 'Trend'} role="img">
        <path d={path} fill="none" stroke={stroke} strokeWidth="1.75" vectorEffect="non-scaling-stroke" />
      </svg>
    </Box>
  );
}

/** ForecastChart — series + optional confidence band + threshold */
export function ForecastChart({
  series = [], band, threshold, provenance = 'estimated', height = 180, label = 'Forecast', className = '', sx,
}) {
  const pts = (Array.isArray(series) ? series : []).map(Number).filter(Number.isFinite);
  const w = 320;
  const h = height;
  const all = [...pts, ...(band?.high || []), ...(band?.low || []), threshold].filter(Number.isFinite);
  const min = all.length ? Math.min(...all) : 0;
  const max = all.length ? Math.max(...all) : 100;
  const span = max - min || 1;
  const toY = (v) => h - ((v - min) / span) * (h - 16) - 8;
  const toX = (i, n) => (i / Math.max(n - 1, 1)) * (w - 8) + 4;
  const line = pts.map((v, i) => `${i === 0 ? 'M' : 'L'}${toX(i, pts.length).toFixed(1)} ${toY(v).toFixed(1)}`).join(' ');
  return (
    <Box className={`rig-forecast-chart ${className}`} sx={sx}>
      <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
        <Typography className="rig-label">{label}</Typography>
        <ProvenanceBadge value={provenance} />
      </Stack>
      <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={height} role="img" aria-label={label}>
        {threshold != null && Number.isFinite(Number(threshold)) && (
          <line x1="0" y1={toY(Number(threshold))} x2={w} y2={toY(Number(threshold))} stroke={resolveTone('critical').main} strokeDasharray="4 4" strokeWidth="1" />
        )}
        {band?.high?.length && band?.low?.length && (
          <path
            d={[
              ...band.high.map((v, i) => `${i === 0 ? 'M' : 'L'}${toX(i, band.high.length).toFixed(1)} ${toY(v).toFixed(1)}`),
              ...[...band.low].reverse().map((v, i, arr) => `L${toX(arr.length - 1 - i, band.low.length).toFixed(1)} ${toY(v).toFixed(1)}`),
              'Z',
            ].join(' ')}
            fill="rgba(94, 77, 178, 0.15)"
          />
        )}
        {pts.length > 1 && <path d={line} fill="none" stroke={resolveTone('info').main} strokeWidth="2" />}
      </svg>
      <ThresholdLegend />
    </Box>
  );
}

/** ThresholdLegend */
export function ThresholdLegend({ className = '', sx }) {
  return (
    <Stack direction="row" spacing={2} className={className} sx={{ mt: 0.75, ...sx }}>
      {[['nominal', 'Nominal'], ['advisory', 'Warning'], ['critical', 'Critical']].map(([key, text]) => (
        <Stack key={key} direction="row" spacing={0.75} alignItems="center">
          <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: resolveTone(key).main }} />
          <Typography variant="caption" color="text.secondary">{text}</Typography>
        </Stack>
      ))}
    </Stack>
  );
}

/** EmptyState */
export function EmptyState({ title = 'Nothing here', description, action, icon, className = '', sx }) {
  return (
    <Box className={`rig-empty-state ${className}`} sx={sx} role="status">
      <Box sx={{ color: 'text.secondary' }}>{icon || <Terminal fontSize="small" />}</Box>
      <Typography fontWeight={700}>{title}</Typography>
      {description && <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 360 }}>{description}</Typography>}
      {action}
    </Box>
  );
}

export { StatusBadge };
