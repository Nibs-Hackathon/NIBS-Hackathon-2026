import { Box, Typography } from '@mui/material';
import { SignalCard, Sparkline } from './data';
import { TwinNode } from './objects';
import { resolveTone } from '../tokens';

/** TagOverlay — live value popup on schematic */
export function TagOverlay({ label, value, unit, x = 0, y = 0, className = '', sx }) {
  return (
    <Box className={`rig-tag-overlay ${className}`} style={{ left: x, top: y }} sx={sx} role="status">
      <Typography className="rig-label" sx={{ fontSize: 9 }}>{label}</Typography>
      <Typography className="rig-data">{value}{unit ? ` ${unit}` : ''}</Typography>
    </Box>
  );
}

/** ProcessSchematic — denser P&ID with flow paths and clickable nodes */
export function ProcessSchematic({
  nodes = [], selectedId, onSelect, overlays = [], className = '', sx, height = 320,
}) {
  return (
    <Box className={`rig-process-schematic ${className}`} sx={{ minHeight: height, ...sx }} role="img" aria-label="Process schematic">
      <div className="rig-process-grid" aria-hidden />
      <svg viewBox="0 0 640 320" width="100%" height={height} className="rig-process-svg" preserveAspectRatio="xMidYMid slice">
        <defs>
          <linearGradient id="rig-pipe" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="rgba(88,216,255,0.05)" />
            <stop offset="50%" stopColor="rgba(88,216,255,0.45)" />
            <stop offset="100%" stopColor="rgba(88,216,255,0.05)" />
          </linearGradient>
          <filter id="rig-node-glow">
            <feGaussianBlur stdDeviation="4" result="b" />
            <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        <path d="M40 160 H160 M200 160 H320 M360 160 H480 M520 160 H600" stroke="url(#rig-pipe)" strokeWidth="6" fill="none" />
        <path d="M160 160 V80 H280 V160 M360 160 V240 H480 V160" stroke="rgba(148,163,184,0.28)" strokeWidth="3" fill="none" />
        <rect x="160" y="120" width="40" height="80" rx="8" fill="rgba(38,132,255,0.14)" stroke="rgba(38,132,255,0.45)" filter="url(#rig-node-glow)" />
        <rect x="320" y="110" width="40" height="100" rx="8" fill="rgba(94,77,178,0.16)" stroke="rgba(94,77,178,0.5)" />
        <rect x="480" y="130" width="40" height="60" rx="8" fill="rgba(34,160,107,0.14)" stroke="rgba(34,160,107,0.45)" />
        <circle cx="100" cy="160" r="10" fill="rgba(88,216,255,0.35)">
          <animate attributeName="opacity" values="0.35;0.9;0.35" dur="2.4s" repeatCount="indefinite" />
        </circle>
      </svg>
      {nodes.map((node, index) => (
        <TwinNode
          key={node.id || index}
          label={node.label || node.name}
          x={node.x ?? 48 + (index % 5) * 110}
          y={node.y ?? (index % 2 === 0 ? 48 : 200)}
          risk={node.risk}
          selected={selectedId === (node.id || node.name)}
          onClick={() => onSelect?.(node)}
        />
      ))}
      {overlays.map((overlay, index) => (
        <TagOverlay key={overlay.id || index} {...overlay} />
      ))}
    </Box>
  );
}

/** GaugeCluster — 2–4 radial gauges */
export function GaugeCluster({ gauges = [], className = '', sx }) {
  return (
    <Box className={`rig-gauge-cluster ${className}`} sx={sx}>
      {gauges.slice(0, 4).map((gauge, index) => {
        const value = Math.max(0, Math.min(100, Number(gauge.value) || 0));
        const color = resolveTone(gauge.tone || (value < 50 ? 'critical' : value < 80 ? 'attention' : 'nominal')).main;
        return (
          <Box key={gauge.label || index} sx={{ width: 88, textAlign: 'center' }}>
            <Box
              sx={{
                width: 72, height: 40, mx: 'auto',
                background: `conic-gradient(from 180deg, ${color} ${value * 1.8}deg, rgba(128,148,177,.16) 0)`,
                borderRadius: '72px 72px 0 0',
              }}
              role="img"
              aria-label={`${gauge.label} ${value}%`}
            />
            <Typography className="rig-label" sx={{ mt: 0.5 }}>{gauge.label}</Typography>
            <Typography className="rig-data">{Math.round(value)}%</Typography>
          </Box>
        );
      })}
    </Box>
  );
}

/** SignalPanel — bottom strip of selected tag trends */
export function SignalPanel({ signals = [], className = '', sx }) {
  return (
    <Box className={`rig-signal-panel ${className}`} sx={sx} role="region" aria-label="Signal panel">
      {signals.map((signal, index) => (
        <Box key={signal.id || signal.name || index} sx={{ minWidth: 180, flex: '0 0 auto' }}>
          <SignalCard {...signal} />
          {signal.values && <Sparkline values={signal.values} height={32} sx={{ mt: 0.5 }} />}
        </Box>
      ))}
      {!signals.length && <Typography color="text.secondary">Select tags to monitor</Typography>}
    </Box>
  );
}
