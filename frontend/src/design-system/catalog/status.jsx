import { Box, Typography } from '@mui/material';
import { resolveTone, statusColors } from '../tokens';

const STATUS_ALIAS = {
  success: 'nominal', warning: 'advisory', danger: 'critical', error: 'critical',
  healthy: 'nominal', running: 'nominal', open: 'attention', high: 'attention',
  medium: 'advisory', low: 'info', idle: 'offline', complete: 'nominal',
  completed: 'nominal', failed: 'critical', working: 'ai-active', streaming: 'ai-active',
};

export function normalizeStatus(status = 'neutral') {
  const key = String(status).toLowerCase().replace(/\s+/g, '-');
  return STATUS_ALIAS[key] || (statusColors[key] ? key : key === 'neutral' ? 'neutral' : key);
}

/** StatusBadge — Nominal / Advisory / Attention / Critical / Offline / AI-active */
export function StatusBadge({ label, status, tone, live = false, className = '', sx }) {
  const resolved = normalizeStatus(status || tone || 'neutral');
  const t = resolveTone(resolved);
  const text = label ?? String(status || tone || 'nominal');
  return (
    <Box
      component="span"
      className={`rig-status-badge ${live && (resolved === 'critical' || resolved === 'attention' || resolved === 'ai-active') ? 'is-pulse' : ''} ${className}`}
      sx={{ color: t.main, backgroundColor: t.soft, ...sx }}
    >
      <i style={{ backgroundColor: t.main }} aria-hidden />
      {text}
    </Box>
  );
}

/** RiskBadge — numeric risk 0–100 with semantic color */
export function RiskBadge({ value = 0, className = '', sx }) {
  const risk = Math.max(0, Math.min(100, Number(value) || 0));
  const status = risk >= 80 ? 'critical' : risk >= 60 ? 'attention' : risk >= 40 ? 'advisory' : 'nominal';
  const t = resolveTone(status);
  return (
    <Box component="span" className={`rig-status-badge ${className}`} sx={{ color: t.main, backgroundColor: t.soft, ...sx }}>
      <Typography component="span" className="rig-data" sx={{ color: 'inherit', fontSize: '0.72rem' }}>{Math.round(risk)}</Typography>
      <Typography component="span" sx={{ fontSize: '0.62rem', opacity: 0.8 }}>/100</Typography>
    </Box>
  );
}

/** ProvenanceBadge — live | estimated | stale */
export function ProvenanceBadge({ value = 'estimated', className = '', sx }) {
  const key = String(value || 'estimated').toLowerCase();
  const safe = ['live', 'estimated', 'stale'].includes(key) ? key : 'estimated';
  const color = safe === 'live' ? statusColors.nominal.main : safe === 'stale' ? statusColors.offline.main : statusColors.advisory.main;
  return (
    <Box component="span" className={`rig-provenance ${className}`} sx={{ color, ...sx }} title={`Data provenance: ${safe}`}>
      {safe}
    </Box>
  );
}

/** ConfidenceMeter — 0–100 with threshold markers */
export function ConfidenceMeter({ value = 0, label = 'Confidence', className = '', sx }) {
  const pct = Math.max(0, Math.min(100, Number(value) || 0));
  return (
    <Box className={`rig-confidence-meter ${className}`} sx={sx}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography className="rig-label">{label}</Typography>
        <Typography className="rig-data">{pct.toFixed(2)}%</Typography>
      </Box>
      <Box className="rig-confidence-track" role="meter" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100} aria-label={label}>
        <Box className="rig-confidence-fill" style={{ width: `${pct}%` }} />
      </Box>
    </Box>
  );
}
