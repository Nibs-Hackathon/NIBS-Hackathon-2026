# Folder: frontend/src/design-system/catalog Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/design-system/catalog`

Contains 12 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/design-system/catalog/actions.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/actions.jsx`

```javascript
import { Box, Button, Slider, Stack, TextField, Typography } from '@mui/material';
import { Close } from '@mui/icons-material';

/** PrimaryCTA — one per panel maximum */
export function PrimaryCTA({ children, loading, disabled, ...props }) {
  return (
    <Button variant="contained" disabled={disabled || loading} sx={{ textTransform: 'none', fontWeight: 700 }} {...props}>
      {loading ? 'Working…' : children}
    </Button>
  );
}

/** DecisionButtonGroup — Accept / Modify / Reject */
export function DecisionButtonGroup({
  onAccept, onModify, onReject, disabled = false, acceptLabel = 'Accept', modifyLabel = 'Modify', rejectLabel = 'Reject',
}) {
  return (
    <Stack direction="row" spacing={1} flexWrap="wrap">
      <Button variant="contained" color="success" disabled={disabled} onClick={onAccept} sx={{ textTransform: 'none' }}>{acceptLabel}</Button>
      <Button variant="outlined" disabled={disabled} onClick={onModify} sx={{ textTransform: 'none' }}>{modifyLabel}</Button>
      <Button variant="outlined" color="error" disabled={disabled} onClick={onReject} sx={{ textTransform: 'none' }}>{rejectLabel}</Button>
    </Stack>
  );
}

/** RationaleField — required for decisions (Epic 5 enforces ≥20 chars). Part 8: Ctrl/⌘ Enter submits. */
export function RationaleField({
  value, onChange, minLength = 20, required = true, disabled = false, label = 'Rationale',
  onSubmitShortcut, inputRef, className = '', sx,
}) {
  const len = String(value || '').trim().length;
  const invalid = required && len > 0 && len < minLength;
  const canSubmit = !disabled && (!required || len >= minLength);
  return (
    <Box className={className} sx={{ flex: 1, minWidth: 200, ...sx }}>
      <TextField
        fullWidth size="small" multiline minRows={2}
        label={label}
        value={value || ''}
        onChange={(e) => onChange?.(e.target.value)}
        disabled={disabled}
        error={invalid}
        inputRef={inputRef}
        helperText={required ? `${len}/${minLength} characters minimum · Ctrl/⌘ Enter to accept` : undefined}
        onKeyDown={(event) => {
          if ((event.metaKey || event.ctrlKey) && event.key === 'Enter' && canSubmit) {
            event.preventDefault();
            onSubmitShortcut?.();
          }
        }}
      />
    </Box>
  );
}

/** ScenarioSlider — what-if control */
export function ScenarioSlider({
  value = 0, onChange, min = 0, max = 10, step = 1, label = 'Scenario stress', className = '', sx,
}) {
  return (
    <Box className={className} sx={sx}>
      <Stack direction="row" justifyContent="space-between">
        <Typography className="rig-label">{label}</Typography>
        <Typography className="rig-data">{value}</Typography>
      </Stack>
      <Slider value={value} min={min} max={max} step={step} onChange={(_, v) => onChange?.(v)} aria-label={label} />
    </Box>
  );
}

/** FilterChipBar */
export function FilterChipBar({ chips = [], onClear, className = '', sx }) {
  return (
    <Box className={`rig-filter-chips ${className}`} sx={sx} role="list" aria-label="Active filters">
      {chips.map((chip) => (
        <Box
          component="button"
          type="button"
          key={chip.id || chip.label}
          className={`rig-filter-chip ${chip.active !== false ? 'is-active' : ''}`}
          onClick={() => chip.onRemove?.(chip)}
          role="listitem"
        >
          {chip.label}
          {chip.onRemove && <Close sx={{ fontSize: 14 }} />}
        </Box>
      ))}
      {chips.length > 0 && onClear && (
        <Button size="small" onClick={onClear} sx={{ textTransform: 'none' }}>Clear all</Button>
      )}
    </Box>
  );
}
```

## frontend/src/design-system/catalog/data.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/data.jsx`

```javascript
import { Box, Button, Stack, Typography } from '@mui/material';
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
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography className="rig-label">{name}</Typography>
        <ProvenanceBadge value={provenance} />
      </Stack>
      <Typography className="rig-kpi" sx={{ mt: 0.5 }}>
        {loading ? '—' : Number.isFinite(num) ? num.toFixed(1) : value ?? '—'}
        {unit && <Typography component="span" className="rig-data" sx={{ ml: 0.5, opacity: 0.7 }}>{unit}</Typography>}
      </Typography>
      <Box sx={{ mt: 1, height: 4, borderRadius: 99, bgcolor: 'action.hover', overflow: 'hidden' }}>
        <Box sx={{ width: `${pct}%`, height: '100%', bgcolor: t.main, transition: 'width 200ms ease' }} />
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
```

## frontend/src/design-system/catalog/executive.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/executive.jsx`

```javascript
import { Box, Button, Stack, Typography } from '@mui/material';
import { StatusBadge } from './status';
import { SectionHeader } from './panels';

/** BriefDocument — structured executive summary */
export function BriefDocument({
  title, summary, sections = [], metrics = [], className = '', sx,
}) {
  return (
    <Box className={`rig-brief-document ${className}`} sx={sx}>
      <SectionHeader eyebrow="Executive brief" title={title || 'Operating brief'} />
      {summary && <Typography sx={{ mt: 1, maxWidth: '68ch' }}>{summary}</Typography>}
      {metrics.length > 0 && (
        <Stack direction="row" spacing={2} sx={{ mt: 2, flexWrap: 'wrap' }}>
          {metrics.map((metric, index) => (
            <Box key={metric.label || index}>
              <Typography className="rig-label">{metric.label}</Typography>
              <Typography className="rig-kpi" sx={{ fontSize: '1.25rem' }}>{metric.value}</Typography>
            </Box>
          ))}
        </Stack>
      )}
      {sections.map((section, index) => (
        <Box key={section.title || index} sx={{ mt: 2 }}>
          <Typography className="rig-label">{section.title}</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{section.body}</Typography>
        </Box>
      ))}
    </Box>
  );
}

/** ApprovalStamp — signatory + timestamp + status */
export function ApprovalStamp({
  signatory, timestamp, status = 'Awaiting approval', className = '', sx,
}) {
  return (
    <Box className={`rig-approval-stamp ${className}`} sx={sx}>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography className="rig-label">Approval</Typography>
        <StatusBadge status={status} label={status} />
      </Stack>
      <Typography fontWeight={700} sx={{ mt: 1 }}>{signatory || '—'}</Typography>
      {timestamp && <Typography className="rig-mono" color="text.secondary">{timestamp}</Typography>}
    </Box>
  );
}

/** EvidenceAppendixLink — jump to investigation trace */
export function EvidenceAppendixLink({ label = 'Open evidence appendix', onClick, disabled = false, className = '', sx }) {
  return (
    <Button
      className={className}
      onClick={onClick}
      disabled={disabled}
      sx={{ textTransform: 'none', justifyContent: 'flex-start', ...sx }}
    >
      {label}
    </Button>
  );
}
```

## frontend/src/design-system/catalog/index.js

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/index.js`

```javascript
/**
 * Epic 1 catalog public surface.
 * Prefer these names over legacy primitives / V2* components for new work.
 */

export {
  StatusBadge, RiskBadge, ProvenanceBadge, ConfidenceMeter, normalizeStatus,
} from './status';

export {
  MetricCard, SignalCard, HealthRing, Sparkline, ForecastChart, ThresholdLegend, EmptyState,
} from './data';

export {
  WorkspaceHeader, OperationsStrip, CommandBar, ScopeSwitcher, SyncIndicator,
  AuditSpine, Dock, Toolbar, UnitRiskMap, DecisionQueue,
} from './shell';

export {
  ObjectRow, IncidentQueueItem, WorkOrderCard, AssetTreeNode, TwinNode, ReportIndexItem,
} from './objects';

export {
  Timeline, IncidentTimeline, EventMarker, AuditEvent,
} from './time';

export {
  AgentPipeline, AgentStageCard, TracePanel, EvidencePanel, EvidenceGraph, RecommendationPanel,
} from './investigation';

export {
  ProcessSchematic, TagOverlay, GaugeCluster, SignalPanel,
} from './twin';

export {
  ObjectInspector, CaseDossier, DecisionRail, DecisionBar, DecisionSurface,
  WorkspacePanel, SectionHeader, SplitPaneHandle,
} from './panels';

export { NotificationInbox } from './panels-notifications';

export {
  PrimaryCTA, DecisionButtonGroup, RationaleField, ScenarioSlider, FilterChipBar,
} from './actions';

export {
  BriefDocument, ApprovalStamp, EvidenceAppendixLink,
} from './executive';
```

## frontend/src/design-system/catalog/investigation.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/investigation.jsx`

```javascript
import { Box, Stack, Typography } from '@mui/material';
import { ConfidenceMeter, StatusBadge, normalizeStatus } from './status';
import { resolveTone } from '../tokens';

/** AgentStageCard */
export function AgentStageCard({
  name, state = 'queued', duration, confidence, active = false, onClick, className = '', sx,
}) {
  const status = normalizeStatus(state);
  return (
    <Box
      component="button"
      type="button"
      className={`rig-agent-stage ${active ? 'is-active' : ''} ${status === 'ai-active' || state === 'running' ? 'is-running' : ''} ${className}`}
      onClick={onClick}
      aria-pressed={active}
      sx={sx}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
        <Typography fontWeight={700}>{name}</Typography>
        <StatusBadge status={status} label={state} live={state === 'running'} />
      </Stack>
      <Stack direction="row" spacing={1.5} sx={{ mt: 1 }}>
        {duration != null && <Typography variant="caption" color="text.secondary">{duration}s</Typography>}
        {confidence != null && <Typography className="rig-data">{Math.round(confidence)}%</Typography>}
      </Stack>
    </Box>
  );
}

/** AgentPipeline — horizontal stage graph */
export function AgentPipeline({ stages = [], selectedId, onSelect, className = '', sx }) {
  return (
    <Box className={`rig-agent-pipeline ${className}`} sx={sx} role="list" aria-label="Agent pipeline">
      {stages.map((stage, index) => (
        <AgentStageCard
          key={stage.id || stage.name || index}
          name={stage.name || stage.agent || `Stage ${index + 1}`}
          state={stage.state}
          duration={stage.duration_seconds ?? stage.duration}
          confidence={stage.confidence}
          active={selectedId === (stage.id || stage.name || index)}
          onClick={() => onSelect?.(stage)}
        />
      ))}
      {!stages.length && <Typography color="text.secondary">No agents running</Typography>}
    </Box>
  );
}

/** TracePanel — expandable agent reasoning lineage */
export function TracePanel({ stages = [], selectedId, onSelect, className = '', sx }) {
  return (
    <Box className={`rig-trace-panel ${className}`} sx={sx}>
      <Typography className="rig-label">Agent trace</Typography>
      <Stack spacing={1} sx={{ mt: 1 }}>
        {stages.map((stage, index) => {
          const id = stage.id || stage.name || index;
          const open = selectedId == null || selectedId === id;
          return (
            <Box
              key={id}
              onClick={() => onSelect?.(stage)}
              sx={{
                p: 1.25, borderRadius: 1, cursor: 'pointer',
                border: '1px solid', borderColor: selectedId === id ? resolveTone('ai-active').main : 'divider',
                bgcolor: selectedId === id ? 'rgba(94,77,178,.08)' : 'transparent',
              }}
            >
              <Stack direction="row" justifyContent="space-between">
                <Typography fontWeight={700}>{stage.name || stage.agent}</Typography>
                <StatusBadge status={stage.state} label={stage.state} />
              </Stack>
              {open && (
                <Box sx={{ mt: 1 }}>
                  {stage.reasoning && <Typography variant="body2" color="text.secondary">{stage.reasoning}</Typography>}
                  {stage.inputs && <Typography className="rig-mono" sx={{ mt: 0.5 }}>in: {String(stage.inputs)}</Typography>}
                  {stage.outputs && <Typography className="rig-mono">out: {String(stage.outputs)}</Typography>}
                  {stage.modelId && <Typography className="rig-mono" color="text.secondary">model: {stage.modelId}</Typography>}
                  {stage.duration && <Typography className="rig-mono" color="text.secondary">duration: {stage.duration}</Typography>}
                </Box>
              )}
            </Box>
          );
        })}
      </Stack>
    </Box>
  );
}

/** EvidencePanel */
export function EvidencePanel({ items = [], onSelect, className = '', sx }) {
  return (
    <Box className={`rig-evidence-panel ${className}`} sx={sx}>
      <Typography className="rig-label">Evidence</Typography>
      <Stack spacing={0.75} sx={{ mt: 1 }}>
        {items.map((item, index) => (
          <Box
            key={item.id || index}
            onClick={() => onSelect?.(item)}
            sx={{ p: 1, borderRadius: 1, border: '1px solid', borderColor: 'divider', cursor: onSelect ? 'pointer' : 'default' }}
          >
            <Typography fontWeight={700}>{item.title || item.type || 'Evidence'}</Typography>
            {item.source && <Typography variant="caption" color="text.secondary">{item.source}</Typography>}
            {item.detail && <Typography variant="body2" color="text.secondary">{item.detail}</Typography>}
          </Box>
        ))}
        {!items.length && <Typography color="text.secondary">No evidence attached</Typography>}
      </Stack>
    </Box>
  );
}

/** EvidenceGraph — node-link style chips */
export function EvidenceGraph({ nodes = [], className = '', sx }) {
  return (
    <Box className={`rig-evidence-graph ${className}`} sx={sx} role="list" aria-label="Evidence graph">
      {nodes.map((node, index) => (
        <Box key={node.id || index} className="rig-evidence-node" role="listitem">
          <Typography className="rig-label" sx={{ fontSize: 9 }}>{node.type || 'node'}</Typography>
          <Typography fontWeight={700}>{node.label}</Typography>
        </Box>
      ))}
      {!nodes.length && <Typography color="text.secondary">No graph nodes</Typography>}
    </Box>
  );
}

/** RecommendationPanel */
export function RecommendationPanel({
  title = 'Recommended action', recommendation, confidence, dissent, action, className = '', sx,
}) {
  return (
    <Box className={`rig-recommendation-panel ${className}`} sx={{ borderLeft: `3px solid ${resolveTone('info').main}`, ...sx }}>
      <Typography className="rig-label">{title}</Typography>
      <Typography fontWeight={700} sx={{ mt: 0.5 }}>{recommendation}</Typography>
      {confidence != null && <ConfidenceMeter value={confidence} sx={{ mt: 1 }} />}
      {dissent && <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>Dissent: {dissent}</Typography>}
      {action && <Box sx={{ mt: 1.5 }}>{action}</Box>}
    </Box>
  );
}
```

## frontend/src/design-system/catalog/objects.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/objects.jsx`

```javascript
import { Box, Stack, Typography } from '@mui/material';
import { StatusBadge, RiskBadge } from './status';
import { resolveTone } from '../tokens';

/** ObjectRow — compact list item (ListRow base) */
export function ObjectRow({
  name, status, secondaryId, detail, selected = false, disabled = false, onClick, leading, trailing, className = '', sx,
}) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-object-row ${selected ? 'is-selected' : ''} ${className}`}
      onClick={onClick}
      disabled={disabled}
      aria-pressed={selected}
      sx={sx}
    >
      <Stack direction="row" spacing={1.25} alignItems="center" minWidth={0} flex={1}>
        {leading}
        <Box minWidth={0}>
          <Typography fontWeight={700} noWrap>{name}</Typography>
          <Stack direction="row" spacing={1} alignItems="center">
            {secondaryId && <Typography className="rig-mono" color="text.secondary" noWrap>{secondaryId}</Typography>}
            {detail && <Typography variant="caption" color="text.secondary" noWrap>{detail}</Typography>}
          </Stack>
        </Box>
      </Stack>
      <Stack direction="row" spacing={1} alignItems="center" flexShrink={0}>
        {status && <StatusBadge status={status} label={status} />}
        {trailing}
      </Stack>
    </Box>
  );
}

/** IncidentQueueItem */
export function IncidentQueueItem({
  id, title, severity, age, assetName, selected = false, onClick, className = '', sx,
}) {
  const status = severity || 'attention';
  const t = resolveTone(status);
  return (
    <Box
      component="button"
      type="button"
      className={`rig-list-row ${selected ? 'is-selected' : ''} ${className}`}
      onClick={onClick}
      aria-pressed={selected}
      sx={sx}
    >
      <Box className="rig-severity-stripe" style={{ backgroundColor: t.main }} aria-hidden />
      <Box flex={1} minWidth={0} textAlign="left">
        <Typography fontWeight={700} noWrap>{title || 'Incident'}</Typography>
        <Typography variant="caption" color="text.secondary" noWrap>
          {[assetName, age, id].filter(Boolean).join(' · ')}
        </Typography>
      </Box>
      <StatusBadge status={status} label={severity || status} />
    </Box>
  );
}

/** WorkOrderCard — kanban card */
export function WorkOrderCard({
  title, priority, asset, cost, window, selected = false, onClick, className = '', sx,
}) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-work-order-card ${selected ? 'is-selected' : ''} ${className}`}
      onClick={onClick}
      aria-pressed={selected}
      sx={sx}
    >
      <Stack direction="row" justifyContent="space-between" spacing={1}>
        <Typography fontWeight={700}>{title}</Typography>
        {priority && <StatusBadge status={priority === 'P1' ? 'critical' : 'advisory'} label={priority} />}
      </Stack>
      {asset && <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.5 }}>{asset}</Typography>}
      <Stack direction="row" spacing={1.5} sx={{ mt: 1 }}>
        {cost != null && <Typography className="rig-data">{typeof cost === 'number' ? `$${cost.toLocaleString()}` : cost}</Typography>}
        {window && <Typography variant="caption" color="text.secondary">{window}</Typography>}
      </Stack>
    </Box>
  );
}

/** AssetTreeNode */
export function AssetTreeNode({
  name, health, depth = 0, selected = false, onClick, expanded, onToggle, children, className = '', sx,
}) {
  const status = health < 50 ? 'critical' : health < 80 ? 'attention' : 'nominal';
  return (
    <Box className={className} sx={sx}>
      <ObjectRow
        name={name}
        status={status}
        detail={health != null ? `${Math.round(health)}%` : undefined}
        selected={selected}
        onClick={onClick}
        leading={
          onToggle ? (
            <Box
              component="button"
              type="button"
              onClick={(e) => { e.stopPropagation(); onToggle(); }}
              sx={{ border: 0, background: 'transparent', color: 'text.secondary', cursor: 'pointer', width: 20 }}
              aria-expanded={expanded}
            >
              {expanded ? '−' : '+'}
            </Box>
          ) : (
            <Box sx={{ width: depth * 12 }} />
          )
        }
        trailing={health != null ? <RiskBadge value={100 - health} /> : null}
        sx={{ pl: 1 + depth * 1.5 }}
      />
      {expanded && children}
    </Box>
  );
}

/** TwinNode — schematic anchor */
export function TwinNode({
  label, x = 0, y = 0, risk = false, selected = false, onClick, className = '', sx,
}) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-twin-node ${selected ? 'is-selected' : ''} ${risk ? 'is-risk' : ''} ${className}`}
      style={{ left: x, top: y }}
      onClick={onClick}
      aria-pressed={selected}
      sx={sx}
    >
      <Typography className="rig-label" sx={{ fontSize: 9 }}>{label}</Typography>
    </Box>
  );
}

/** ReportIndexItem */
export function ReportIndexItem({
  title, date, approvalState, selected = false, onClick, className = '', sx,
}) {
  return (
    <ObjectRow
      name={title}
      detail={date}
      status={approvalState}
      selected={selected}
      onClick={onClick}
      className={className}
      sx={sx}
    />
  );
}
```

## frontend/src/design-system/catalog/panels-notifications.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/panels-notifications.jsx`

```javascript
import { Box, Stack, Typography } from '@mui/material';
import { StatusBadge } from './status';
import { resolveTone } from '../tokens';

/** NotificationInbox — lives inside WorkspacePanel */
export function NotificationInbox({ items = [], onSelect, className = '', sx }) {
  if (!items.length) {
    return <Typography color="text.secondary" className={className} sx={sx}>No notifications</Typography>;
  }
  return (
    <Stack spacing={0.5} className={className} sx={sx} role="list" aria-label="Notifications">
      {items.map((item, index) => {
        const t = resolveTone(item.tone || item.severity || 'info');
        return (
          <Box
            key={item.id || index}
            role="listitem"
            onClick={() => onSelect?.(item)}
            sx={{
              p: 1.25, borderRadius: 1, cursor: onSelect ? 'pointer' : 'default',
              borderLeft: `3px solid ${t.main}`, bgcolor: item.unread ? 'rgba(38,132,255,.06)' : 'transparent',
              '&:hover': onSelect ? { bgcolor: 'action.hover' } : undefined,
            }}
          >
            <Stack direction="row" justifyContent="space-between" spacing={1}>
              <Typography fontWeight={700}>{item.title}</Typography>
              {item.time && <Typography className="rig-mono" color="text.secondary">{item.time}</Typography>}
            </Stack>
            {item.message && <Typography variant="body2" color="text.secondary">{item.message}</Typography>}
            {item.severity && <StatusBadge status={item.severity} label={item.severity} sx={{ mt: 0.5 }} />}
          </Box>
        );
      })}
    </Stack>
  );
}
```

## frontend/src/design-system/catalog/panels.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/panels.jsx`

```javascript
import { useState } from 'react';
import { Box, Drawer, IconButton, Stack, Tab, Tabs, Typography } from '@mui/material';
import { Close } from '@mui/icons-material';
import { EmptyState } from './data';
import { DecisionButtonGroup, RationaleField, PrimaryCTA } from './actions';
import { NotificationInbox } from './panels-notifications';
import { EvidencePanel, RecommendationPanel } from './investigation';

/** SectionHeader */
export function SectionHeader({ eyebrow, title, description, action, className = '', sx }) {
  return (
    <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" alignItems={{ sm: 'flex-end' }} spacing={1} className={className} sx={sx}>
      <Box>
        {eyebrow && <Typography className="rig-label">{eyebrow}</Typography>}
        <Typography sx={{ fontSize: '1.125rem', fontWeight: 600, letterSpacing: '-0.01em', mt: 0.35 }}>{title}</Typography>
        {description && <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{description}</Typography>}
      </Box>
      {action}
    </Stack>
  );
}

/** SplitPaneHandle */
export function SplitPaneHandle({ onMouseDown, className = '', sx, orientation = 'vertical' }) {
  return (
    <Box
      component="button"
      type="button"
      className={`rig-split-handle ${className}`}
      aria-label="Resize panels"
      onMouseDown={onMouseDown}
      sx={{
        ...(orientation === 'horizontal' ? { height: 6, width: '100%', cursor: 'row-resize' } : {}),
        ...sx,
      }}
    />
  );
}

/** ObjectInspector — fixed right pane for selected object */
export function ObjectInspector({
  title, subtitle, empty = false, emptyTitle = 'Select an object', emptyDescription = 'Choose an asset, incident, or work order to inspect.',
  children, sections, footer, width, className = '', sx,
}) {
  return (
    <Box className={`rig-object-inspector ${className}`} sx={{ maxWidth: width || 360, ...sx }} role="complementary" aria-label="Object inspector">
      {(title || subtitle) && (
        <Box sx={{ p: 2, borderBottom: '1px solid rgba(164,196,228,.12)' }}>
          {subtitle && <Typography className="rig-label">{subtitle}</Typography>}
          {title && <Typography fontWeight={700}>{title}</Typography>}
        </Box>
      )}
      <Box className="rig-object-inspector-body">
        {empty ? (
          <Box className="rig-object-inspector-empty">
            <EmptyState title={emptyTitle} description={emptyDescription} />
          </Box>
        ) : (
          <>
            {sections?.map((section, index) => (
              <Box key={section.id || section.title || index} className="rig-object-inspector-section">
                {section.title && <Typography className="rig-label">{section.title}</Typography>}
                {section.content}
              </Box>
            ))}
            {children}
          </>
        )}
      </Box>
      {footer && <Box sx={{ p: 1.5, borderTop: '1px solid rgba(164,196,228,.12)' }}>{footer}</Box>}
    </Box>
  );
}

/** WorkspacePanel — global ⌘J slide-over */
export function WorkspacePanel({
  open, onClose, auditContent, notifications = [], onNotificationClick, width = 400, className = '', sx,
}) {
  const [tab, setTab] = useState(0);
  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{ className: `rig-workspace-panel ${className}`, sx: { width: { xs: '100%', sm: width }, ...sx } }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ px: 2, pt: 2 }}>
        <Typography className="rig-label">Workspace panel</Typography>
        <IconButton onClick={onClose} aria-label="Close workspace panel"><Close /></IconButton>
      </Stack>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} className="rig-workspace-panel-tabs" sx={{ px: 1 }}>
        <Tab label="Audit" />
        <Tab label="Notifications" />
      </Tabs>
      <Box className="rig-workspace-panel-body">
        {tab === 0 && (auditContent || <Typography color="text.secondary">No audit activity</Typography>)}
        {tab === 1 && <NotificationInbox items={notifications} onSelect={onNotificationClick} />}
      </Box>
    </Drawer>
  );
}

/**
 * DecisionSurface — shared core for DecisionBar + DecisionRail
 * variant: operational | executive
 */
export function DecisionSurface({
  variant = 'operational',
  recommendation,
  rationale, onRationaleChange,
  onAccept, onModify, onReject,
  disabled = false, busy = false,
  minRationale = 0,
  rationaleInputRef,
  acceptLabel, modifyLabel, rejectLabel,
  children, className = '', sx,
}) {
  const rationaleOk = minRationale <= 0 || String(rationale || '').trim().length >= minRationale;
  const actionsDisabled = disabled || busy || !rationaleOk;
  const shellClass = variant === 'executive' ? 'rig-decision-rail' : 'rig-decision-bar';
  const labels = variant === 'executive'
    ? { acceptLabel: acceptLabel || 'Approve', modifyLabel: modifyLabel || 'Defer', rejectLabel: rejectLabel || 'Escalate' }
    : { acceptLabel, modifyLabel, rejectLabel };
  return (
    <Box className={`${shellClass} ${className}`} sx={sx} role="region" aria-label={variant === 'executive' ? 'Decision rail' : 'Decision bar'} data-decision-surface={variant}>
      {recommendation && (
        <Box sx={{ flex: variant === 'executive' ? undefined : 1, minWidth: 160 }}>
          <Typography className="rig-label">Recommendation</Typography>
          <Typography fontWeight={700}>{recommendation}</Typography>
        </Box>
      )}
      <RationaleField
        value={rationale}
        onChange={onRationaleChange}
        minLength={minRationale > 0 ? minRationale : 20}
        required={minRationale > 0}
        disabled={disabled || busy}
        inputRef={rationaleInputRef}
        onSubmitShortcut={() => { if (!actionsDisabled) onAccept?.(); }}
      />
      <DecisionButtonGroup
        disabled={actionsDisabled}
        onAccept={onAccept}
        onModify={onModify}
        onReject={onReject}
        {...labels}
      />
      {children}
    </Box>
  );
}

/** DecisionBar — sticky operational (Epic 5: rationale required by default) */
export function DecisionBar({ minRationale = 20, ...props }) {
  return <DecisionSurface variant="operational" minRationale={minRationale} {...props} />;
}

/** DecisionRail — executive */
export function DecisionRail(props) {
  return <DecisionSurface variant="executive" {...props} />;
}

/** CaseDossier — EvidencePanel + RecommendationPanel composition */
export function CaseDossier({
  title = 'Case dossier', evidence = [], recommendation, confidence, children, className = '', sx,
}) {
  return (
    <Box className={`rig-case-dossier ${className}`} sx={sx}>
      <SectionHeader eyebrow="Dossier" title={title} />
      <EvidencePanel items={evidence} />
      {recommendation && <RecommendationPanel recommendation={recommendation} confidence={confidence} />}
      {children}
    </Box>
  );
}

export { PrimaryCTA };
```

## frontend/src/design-system/catalog/shell.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/shell.jsx`

```javascript
import { useMemo, useState } from 'react';
import {
  Badge, Box, Button, Dialog, DialogContent, IconButton, MenuItem, Stack, TextField, Tooltip, Typography,
} from '@mui/material';
import {
  NotificationsOutlined, PushPinOutlined, SearchOutlined, SmartToyOutlined, SyncOutlined, ViewSidebarOutlined,
} from '@mui/icons-material';
import { motion } from 'motion/react';
import { MetricCard } from './data';
import { StatusBadge, normalizeStatus } from './status';
import { AuditEvent } from './time';
import { ObjectRow, IncidentQueueItem } from './objects';
import { resolveTone } from '../tokens';

/** WorkspaceHeader — title + breadcrumbs + ambient ops chrome */
export function WorkspaceHeader({
  title, breadcrumbs = [], scope, onScopeChange, facilities = [], syncAge, connected = true,
  onSync, clock, telemetryLabel, aiLabel, agentsActive = 0, unreadCount = 0, onAiClick, onInbox,
  actions, className = '', sx,
}) {
  return (
    <Box className={`rig-workspace-header ${className}`} sx={sx}>
      <Box sx={{ minWidth: 0 }}>
        {breadcrumbs.length > 0 && (
          <nav className="rig-breadcrumbs" aria-label="Breadcrumb">
            {breadcrumbs.map((crumb, index) => (
              <Box key={`${crumb.label}-${index}`} component="span" sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.75 }}>
                {index > 0 && <span aria-hidden>›</span>}
                <button type="button" onClick={() => crumb.onNavigate?.(crumb)} disabled={!crumb.onNavigate}>
                  {crumb.label}
                </button>
              </Box>
            ))}
          </nav>
        )}
        <Typography component="h1">{title}</Typography>
      </Box>
      <Stack direction="row" spacing={1} alignItems="center" flexShrink={0} className="rig-workspace-chrome">
        {(clock || telemetryLabel) && (
          <Box className="rig-ambient">
            {clock && <Typography className="rig-mono">{clock}</Typography>}
            {telemetryLabel && <Typography variant="caption" color="text.secondary">{telemetryLabel}</Typography>}
          </Box>
        )}
        {scope !== undefined && (
          <ScopeSwitcher value={scope} onChange={onScopeChange} options={facilities} />
        )}
        <SyncIndicator connected={connected} syncAge={syncAge} onRefresh={onSync} />
        {aiLabel && (
          <Tooltip title={aiLabel}>
            <Button
              className="rig-ai-status"
              size="small"
              onClick={onAiClick}
              startIcon={<SmartToyOutlined fontSize="small" />}
            >
              <motion.i
                className="rig-ai-pulse-dot"
                animate={agentsActive ? { opacity: [1, 0.4, 1] } : false}
                transition={{ repeat: Infinity, duration: 1.6 }}
              />
              {aiLabel}
            </Button>
          </Tooltip>
        )}
        {onInbox && (
          <Tooltip title="Notifications">
            <IconButton onClick={onInbox} aria-label="Open notifications" size="small">
              <Badge badgeContent={unreadCount} color="error">
                <NotificationsOutlined fontSize="small" />
              </Badge>
            </IconButton>
          </Tooltip>
        )}
        {actions}
      </Stack>
    </Box>
  );
}

/** ScopeSwitcher */
export function ScopeSwitcher({ value, onChange, options = ['Alpha Refinery', 'North Sea Portfolio', 'Enterprise view'], className = '', sx }) {
  return (
    <TextField
      select size="small" value={value || options[0]} onChange={(e) => onChange?.(e.target.value)}
      className={className} sx={{ minWidth: 160, ...sx }} aria-label="Facility scope"
    >
      {options.map((opt) => <MenuItem key={opt} value={opt}>{opt}</MenuItem>)}
    </TextField>
  );
}

/** SyncIndicator */
export function SyncIndicator({ connected = true, syncAge, onRefresh, className = '', sx }) {
  const label = connected
    ? (syncAge != null ? `Synced ${syncAge}s ago` : 'Live')
    : 'Reconnecting';
  return (
    <Stack direction="row" spacing={0.75} alignItems="center" className={className} sx={sx}>
      <StatusBadge label={connected ? 'Live' : 'Offline'} status={connected ? 'nominal' : 'offline'} live={connected} />
      <Typography variant="caption" color="text.secondary">{label}</Typography>
      {onRefresh && (
        <IconButton size="small" onClick={onRefresh} aria-label="Refresh telemetry"><SyncOutlined fontSize="small" /></IconButton>
      )}
    </Stack>
  );
}

/** OperationsStrip — 4 KPIs + CTA */
export function OperationsStrip({ metrics = [], cta, className = '', sx }) {
  const items = metrics.slice(0, 4);
  while (items.length < 4) items.push({ label: '—', value: '—' });
  return (
    <Box className={`rig-operations-strip ${className}`} sx={sx} role="region" aria-label="Operations strip">
      {items.map((metric, index) => (
        <Box key={metric.label || index} className="rig-strip-metric">
          <Typography className="rig-label">{metric.label}</Typography>
          <Typography className="rig-kpi">{metric.value}</Typography>
          {metric.detail && <Typography variant="caption" color="text.secondary">{metric.detail}</Typography>}
        </Box>
      ))}
      <Box className="rig-strip-cta">{cta}</Box>
    </Box>
  );
}

/** CommandBar — global modal search/actions */
export function CommandBar({ open, onClose, commands = [], placeholder = 'Search or run a command…' }) {
  const [query, setQuery] = useState('');
  const filtered = useMemo(
    () => commands.filter((c) => `${c.label} ${c.description || ''} ${c.group || ''}`.toLowerCase().includes(query.toLowerCase())),
    [commands, query],
  );
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" PaperProps={{ sx: { bgcolor: '#111722', backgroundImage: 'none' } }}>
      <DialogContent sx={{ p: 2 }}>
        <Typography className="rig-label" sx={{ mb: 1 }}>Command</Typography>
        <TextField
          autoFocus fullWidth size="small" value={query} onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          InputProps={{ startAdornment: <SearchOutlined fontSize="small" sx={{ mr: 1, color: 'text.secondary' }} /> }}
        />
        <Stack spacing={0.5} sx={{ mt: 1.5, maxHeight: 320, overflow: 'auto' }}>
          {filtered.map((command, index) => (
            <Button
              key={command.id || index}
              onClick={() => { command.onSelect?.(); onClose?.(); }}
              sx={{ justifyContent: 'space-between', textTransform: 'none', color: 'text.primary' }}
            >
              <Box textAlign="left">
                <Typography fontWeight={700}>{command.label}</Typography>
                {command.description && <Typography variant="caption" color="text.secondary">{command.description}</Typography>}
              </Box>
              {command.shortcut && <kbd className="rig-mono">{command.shortcut}</kbd>}
            </Button>
          ))}
          {!filtered.length && <Typography color="text.secondary" sx={{ p: 2, textAlign: 'center' }}>No matches</Typography>}
        </Stack>
      </DialogContent>
    </Dialog>
  );
}

/** Toolbar */
export function Toolbar({ children, className = '', sx }) {
  return <Box className={`rig-toolbar ${className}`} role="toolbar" sx={sx}>{children}</Box>;
}

/** AuditSpine — last N decisions */
export function AuditSpine({ events = [], className = '', sx, tabIndex }) {
  return (
    <Box className={`rig-audit-spine ${className}`} sx={sx} role="status" aria-label="Audit spine" tabIndex={tabIndex}>
      <Typography className="rig-label" sx={{ flexShrink: 0 }}>Audit</Typography>
      <Box className="rig-audit-spine-track">
        {events.length
          ? events.map((event, index) => <AuditEvent key={event.id || index} {...event} />)
          : <Typography variant="caption" color="text.secondary">No recent decisions</Typography>}
      </Box>
    </Box>
  );
}

/** Dock — quick actions */
export function Dock({
  onCommand, onCopilot, onWorkspacePanel, onPin, className = '', sx,
}) {
  return (
    <Box className={`rig-dock ${className}`} role="toolbar" aria-label="Workspace dock" sx={sx}>
      <Tooltip title="Command (Ctrl K)"><IconButton onClick={onCommand} aria-label="Command bar"><SearchOutlined /></IconButton></Tooltip>
      <Tooltip title="AI copilot"><IconButton onClick={onCopilot} aria-label="AI copilot"><SmartToyOutlined /></IconButton></Tooltip>
      <Tooltip title="Workspace panel (Ctrl J)"><IconButton onClick={onWorkspacePanel} aria-label="Workspace panel"><ViewSidebarOutlined /></IconButton></Tooltip>
      <Tooltip title="Pin workspace"><IconButton onClick={onPin} aria-label="Pin workspace"><PushPinOutlined /></IconButton></Tooltip>
    </Box>
  );
}

/** UnitRiskMap — facility schematic with risk-tinted nodes */
export function UnitRiskMap({ units = [], onSelect, selectedId, className = '', sx }) {
  const positions = [
    { x: 18, y: 28 }, { x: 52, y: 22 }, { x: 78, y: 38 },
    { x: 28, y: 62 }, { x: 58, y: 68 }, { x: 82, y: 70 },
  ];
  return (
    <Box className={`rig-unit-risk-map ${className}`} sx={sx} role="list" aria-label="Unit risk map">
      <Typography className="rig-label rig-unit-risk-kicker">Facility risk map</Typography>
      <svg className="rig-unit-risk-svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden>
        <defs>
          <radialGradient id="rig-unit-glow" cx="50%" cy="40%" r="60%">
            <stop offset="0%" stopColor="rgba(38,132,255,0.18)" />
            <stop offset="100%" stopColor="rgba(10,13,18,0)" />
          </radialGradient>
        </defs>
        <rect width="100" height="100" fill="url(#rig-unit-glow)" />
        <path d="M12 48 H88 M35 20 V78 M65 18 V82" stroke="rgba(148,163,184,0.22)" strokeWidth="0.6" fill="none" />
        <path d="M20 35 Q50 28 80 42" stroke="rgba(88,216,255,0.2)" strokeWidth="0.5" fill="none" />
      </svg>
      {units.map((unit, index) => {
        const risk = Number(unit.risk ?? (100 - (unit.health ?? 100)));
        const status = normalizeStatus(unit.status) || (risk >= 70 ? 'critical' : risk >= 40 ? 'attention' : 'nominal');
        const t = resolveTone(status);
        const id = unit.id || unit.name || index;
        const pos = positions[index % positions.length];
        return (
          <Box
            component="button"
            type="button"
            key={id}
            role="listitem"
            className={`rig-unit-node ${selectedId === id ? 'is-selected' : ''} ${risk >= 40 ? 'is-risk' : ''}`}
            onClick={() => onSelect?.(unit)}
            style={{
              left: `${pos.x}%`,
              top: `${pos.y}%`,
              borderColor: `${t.main}88`,
              boxShadow: risk >= 40 ? `0 0 18px ${t.main}44` : undefined,
            }}
            aria-pressed={selectedId === id}
          >
            <Typography fontWeight={750} fontSize={12}>{unit.name || unit.label}</Typography>
            <Typography className="rig-mono" sx={{ fontSize: 10, color: t.main }}>
              {unit.health != null ? `${Math.round(unit.health)}%` : `${Math.round(risk)} risk`}
            </Typography>
          </Box>
        );
      })}
      {!units.length && <Typography color="text.secondary" sx={{ p: 2 }}>No units in scope</Typography>}
    </Box>
  );
}

/** DecisionQueue — prioritized list for Mission Control */
export function DecisionQueue({ items = [], onSelect, selectedId, className = '', sx }) {
  return (
    <Box className={`rig-decision-queue ${className}`} sx={sx} role="list" aria-label="Decision queue">
      {items.map((item, index) => {
        if (item.kind === 'incident' || item.severity) {
          return (
            <IncidentQueueItem
              key={item.id || index}
              {...item}
              selected={selectedId === item.id}
              onClick={() => onSelect?.(item)}
            />
          );
        }
        return (
          <ObjectRow
            key={item.id || index}
            name={item.title || item.name}
            status={item.status}
            secondaryId={item.id}
            selected={selectedId === item.id}
            onClick={() => onSelect?.(item)}
          />
        );
      })}
      {!items.length && <Typography color="text.secondary" sx={{ p: 1 }}>No pending decisions</Typography>}
    </Box>
  );
}

export { MetricCard };
```

## frontend/src/design-system/catalog/status.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/status.jsx`

```javascript
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
        <Typography className="rig-data">{Math.round(pct)}%</Typography>
      </Box>
      <Box className="rig-confidence-track" role="meter" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100} aria-label={label}>
        <Box className="rig-confidence-fill" style={{ width: `${pct}%` }} />
      </Box>
    </Box>
  );
}
```

## frontend/src/design-system/catalog/time.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/time.jsx`

```javascript
import { Box, Stack, Typography } from '@mui/material';
import { StatusBadge, normalizeStatus } from './status';
import { resolveTone } from '../tokens';

/** EventMarker */
export function EventMarker({ title, time, detail, status = 'info', className = '', sx }) {
  const t = resolveTone(normalizeStatus(status));
  return (
    <Box className={`rig-timeline-item ${className}`} sx={sx}>
      <Box className="rig-timeline-rail">
        <Box className="rig-timeline-dot" style={{ backgroundColor: t.main }} />
        <Box className="rig-timeline-line" />
      </Box>
      <Box className="rig-timeline-body">
        <Stack direction="row" justifyContent="space-between" spacing={1}>
          <Typography fontWeight={700}>{title}</Typography>
          {time && <Typography className="rig-mono" color="text.secondary">{time}</Typography>}
        </Stack>
        {detail && <Typography variant="body2" color="text.secondary" sx={{ mt: 0.35 }}>{detail}</Typography>}
      </Box>
    </Box>
  );
}

/** Timeline — variant="incident" adds decision markers styling */
export function Timeline({ items = [], variant = 'default', onSelect, className = '', sx }) {
  return (
    <Box className={`rig-timeline ${className}`} sx={sx} role="list" aria-label={variant === 'incident' ? 'Incident timeline' : 'Timeline'}>
      {items.map((item, index) => (
        <Box
          key={item.id || index}
          role="listitem"
          onClick={() => onSelect?.(item)}
          sx={{ cursor: onSelect ? 'pointer' : 'default' }}
        >
          <EventMarker
            title={item.title}
            time={item.time}
            detail={item.description || item.detail}
            status={item.status || item.tone || (item.decision ? 'ai-active' : 'info')}
          />
          {variant === 'incident' && item.decision && (
            <Typography className="rig-label" sx={{ ml: 3.5, mb: 1.5, color: resolveTone('ai-active').main }}>
              Decision · {item.decision}
            </Typography>
          )}
        </Box>
      ))}
      {!items.length && <Typography color="text.secondary" sx={{ p: 1 }}>No events</Typography>}
    </Box>
  );
}

/** IncidentTimeline — alias */
export function IncidentTimeline(props) {
  return <Timeline {...props} variant="incident" />;
}

/** AuditEvent — immutable log row */
export function AuditEvent({ who, what, when, objectLabel, className = '', sx }) {
  return (
    <Box className={`rig-audit-event ${className}`} sx={sx}>
      <StatusBadge status="info" label="Audit" />
      <Typography component="span" className="rig-data">{who || 'Operator'}</Typography>
      <Typography component="span">{what}</Typography>
      {objectLabel && <Typography component="span" className="rig-mono">{objectLabel}</Typography>}
      {when && <Typography component="span" className="rig-mono">{when}</Typography>}
    </Box>
  );
}
```

## frontend/src/design-system/catalog/twin.jsx

**Folder path:** `frontend/src/design-system/catalog`

**File path:** `frontend/src/design-system/catalog/twin.jsx`

```javascript
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
```
