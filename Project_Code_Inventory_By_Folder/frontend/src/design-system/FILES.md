# Folder: frontend/src/design-system Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/design-system`

Contains 11 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/design-system/catalog.css

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/catalog.css`

```css
/* RigOS catalog — Epic 1. Operational surfaces; no glass blur. */

.rig-surface-0 { background: var(--rig-surface-0, #0A0D12); }
.rig-surface-1 { background: var(--rig-surface-1, #111722); border: 1px solid rgba(164, 196, 228, 0.14); }
.rig-surface-2 { background: var(--rig-surface-2, #0d1219); border: 1px solid rgba(164, 196, 228, 0.12); }

.rig-label {
  font-size: 0.62rem; font-weight: 750; letter-spacing: 0.12em; text-transform: uppercase; color: #718096;
}
.rig-kpi { font-size: 2.05rem; font-weight: 780; letter-spacing: -0.045em; font-variant-numeric: tabular-nums; line-height: 1.05; }
.rig-data { font-size: 0.8125rem; font-weight: 600; font-variant-numeric: tabular-nums; }
.rig-mono { font-family: "DM Mono", "SFMono-Regular", Consolas, monospace; font-size: 0.75rem; font-weight: 500; }

.rig-workspace-header {
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  min-height: 64px; padding: 10px 0;
}
.rig-workspace-header h1 {
  margin: 0; font-size: clamp(1.35rem, 2vw, 1.85rem); font-weight: 750; letter-spacing: -0.035em; line-height: 1.1;
}
.rig-workspace-chrome { flex-wrap: wrap; justify-content: flex-end; }
.rig-ambient {
  display: flex; flex-direction: column; align-items: flex-end; gap: 2px;
  padding: 6px 10px; border-radius: 10px; background: rgba(255,255,255,0.03);
  border: 1px solid rgba(148,163,184,0.12); min-width: 140px;
}
.rig-ambient .rig-mono { font-size: 0.8rem; color: #eef4fc; }
.rig-ai-status {
  text-transform: none !important; font-weight: 700 !important; font-size: 0.75rem !important;
  color: #cbd5e1 !important; border: 1px solid rgba(148,163,184,0.16) !important;
  background: rgba(94, 77, 178, 0.12) !important; border-radius: 999px !important; padding: 4px 10px !important;
}
.rig-ai-pulse-dot {
  width: 6px; height: 6px; border-radius: 50%; background: #9772ff; display: inline-block; margin-right: 6px;
}

.rig-operations-strip {
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)) auto; gap: 14px; align-items: stretch;
  min-height: 88px; padding: 14px 16px; border-radius: 14px;
  border: 1px solid rgba(164, 196, 228, 0.14);
  background:
    linear-gradient(135deg, rgba(38,132,255,0.08), transparent 42%),
    #111722;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
}
.rig-operations-strip .rig-strip-metric { display: flex; flex-direction: column; justify-content: center; gap: 4px; min-width: 0; }
.rig-operations-strip .rig-strip-cta { display: flex; align-items: center; }

.rig-process-schematic {
  position: relative; width: 100%; min-height: 280px; border-radius: 14px;
  border: 1px solid rgba(164, 196, 228, 0.14); background: #0b1018; overflow: hidden;
}
.rig-process-grid {
  position: absolute; inset: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(38,132,255,0.12), transparent 35%),
    linear-gradient(rgba(148,163,184,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148,163,184,0.05) 1px, transparent 1px);
  background-size: auto, 28px 28px, 28px 28px;
  pointer-events: none;
}
.rig-process-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.rig-twin-node {
  position: absolute; min-width: 88px; padding: 10px; border-radius: 10px;
  border: 1px solid rgba(164, 196, 228, 0.22); background: rgba(17, 23, 34, 0.92); cursor: pointer; text-align: center;
  transition: transform 140ms ease, border-color 140ms ease, box-shadow 140ms ease;
}
.rig-twin-node:hover { transform: translateY(-2px); }
.rig-twin-node.is-selected { border-color: #2684FF; box-shadow: 0 0 0 2px rgba(38, 132, 255, 0.28), 0 12px 28px rgba(0,0,0,0.35); }
.rig-twin-node.is-risk { border-color: #E2483D; box-shadow: 0 0 20px rgba(226,72,61,0.25); }

.rig-unit-risk-map {
  position: relative; display: block; min-height: 280px; padding: 12px;
  border-radius: 14px; border: 1px solid rgba(164, 196, 228, 0.14); background: #0d1219; overflow: hidden;
}
.rig-unit-risk-kicker { position: absolute; top: 12px; left: 14px; z-index: 2; }
.rig-unit-risk-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.rig-unit-node {
  position: absolute; transform: translate(-50%, -50%);
  min-width: 108px; padding: 10px 12px; border-radius: 12px;
  border: 1px solid rgba(164, 196, 228, 0.18); background: rgba(13, 18, 28, 0.92);
  cursor: pointer; text-align: left; color: inherit; z-index: 2;
  transition: transform 140ms ease, box-shadow 140ms ease;
}
.rig-unit-node:hover { transform: translate(-50%, calc(-50% - 3px)); }
.rig-unit-node.is-selected { outline: 2px solid #2684FF; }

.rig-agent-pipeline {
  display: flex; gap: 10px; align-items: stretch; overflow-x: auto; min-height: 140px; padding: 10px;
}
.rig-agent-stage {
  min-width: 152px; flex: 1; padding: 14px; border-radius: 12px;
  border: 1px solid rgba(164, 196, 228, 0.14);
  background: linear-gradient(180deg, rgba(94,77,178,0.12), #111722 55%);
  cursor: pointer; transition: transform 120ms ease, border-color 120ms ease;
}
.rig-agent-stage.is-active { border-color: #5E4DB2; transform: scale(1.03); box-shadow: 0 0 24px rgba(94,77,178,0.25); }
.rig-agent-stage.is-running { border-color: #5E4DB2; }

.rig-work-order-card {
  padding: 14px; border-radius: 12px; border: 1px solid rgba(164, 196, 228, 0.14);
  background: linear-gradient(180deg, rgba(255,255,255,0.03), #111722);
  cursor: pointer; text-align: left; width: 100%; color: inherit;
  transition: border-color 120ms ease, transform 120ms ease;
}
.rig-work-order-card:hover { transform: translateY(-1px); }
.rig-work-order-card.is-selected { border-color: #2684FF; box-shadow: inset 3px 0 #2684FF; }

.rig-brief-document {
  display: flex; flex-direction: column; gap: 16px; padding: 22px;
  border-radius: 14px; border: 1px solid rgba(164, 196, 228, 0.14);
  background:
    linear-gradient(180deg, rgba(255,255,255,0.03), transparent 30%),
    #111722;
}
.rig-case-dossier, .rig-evidence-panel, .rig-trace-panel, .rig-recommendation-panel {
  display: flex; flex-direction: column; gap: 12px; padding: 16px;
  border-radius: 12px; border: 1px solid rgba(164, 196, 228, 0.12);
  background: linear-gradient(180deg, rgba(255,255,255,0.025), #111722);
}

.rig-status-badge {
  display: inline-flex; align-items: center; gap: 6px; padding: 2px 8px; border-radius: 6px;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase;
}
.rig-status-badge i {
  width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
}
.rig-status-badge.is-pulse i { animation: rig-status-pulse 400ms ease infinite; }
@keyframes rig-status-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.45; } }

.rig-metric-card, .rig-signal-card, .rig-data-card {
  min-height: 96px; padding: 16px; border-radius: 10px;
  border: 1px solid rgba(164, 196, 228, 0.14); background: #111722;
}
.rig-signal-card { min-height: 72px; }
.rig-metric-card.is-loading, .rig-signal-card.is-loading { opacity: 0.65; }
.rig-metric-card .rig-kpi { transition: opacity 200ms cubic-bezier(0.2, 0.8, 0.2, 1); }

.rig-object-row, .rig-list-row {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  min-height: 64px; width: 100%; padding: 10px 12px; border: 0; border-radius: 8px;
  background: transparent; color: inherit; text-align: left; cursor: pointer;
  transition: background-color 120ms ease;
}
.rig-object-row:hover, .rig-list-row:hover { background: rgba(255, 255, 255, 0.04); }
.rig-object-row.is-selected, .rig-list-row.is-selected {
  background: rgba(38, 132, 255, 0.12); box-shadow: inset 3px 0 #2684FF;
}
.rig-object-row:disabled, .rig-list-row:disabled { opacity: 0.5; cursor: not-allowed; }

.rig-severity-stripe { width: 3px; align-self: stretch; border-radius: 2px; flex-shrink: 0; }

.rig-breadcrumbs { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 6px; }
.rig-breadcrumbs button {
  border: 0; background: transparent; color: #93A2B8; font-size: 0.75rem; cursor: pointer; padding: 0;
}
.rig-breadcrumbs button:hover { color: #EEF4FC; }
.rig-breadcrumbs span { color: #65758B; font-size: 0.75rem; }

.rig-toolbar {
  display: flex; flex-wrap: wrap; align-items: center; gap: 8px; min-height: 48px;
}
.rig-filter-chips { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.rig-filter-chip {
  display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 999px;
  border: 1px solid rgba(164, 196, 228, 0.18); background: #0d1219; font-size: 0.72rem; cursor: pointer;
}
.rig-filter-chip.is-active { border-color: #2684FF; color: #2684FF; }

.rig-object-inspector {
  width: 100%; max-width: 360px; min-width: 280px; height: 100%;
  display: flex; flex-direction: column; overflow: hidden;
  border-radius: 10px; border: 1px solid rgba(164, 196, 228, 0.12); background: #0d1219;
}
.rig-object-inspector-body { flex: 1; overflow: auto; padding: 16px; display: flex; flex-direction: column; gap: 16px; }
.rig-object-inspector-section { display: flex; flex-direction: column; gap: 8px; }
.rig-object-inspector-empty {
  flex: 1; display: grid; place-items: center; padding: 24px; text-align: center; color: #93A2B8;
}

.rig-workspace-panel {
  width: 100%; max-width: 400px; height: 100%; display: flex; flex-direction: column;
  background: #111722; border-left: 1px solid rgba(164, 196, 228, 0.14);
}
.rig-workspace-panel-tabs { display: flex; gap: 4px; padding: 12px 12px 0; }
.rig-workspace-panel-tabs button {
  flex: 1; border: 0; padding: 8px; border-radius: 8px 8px 0 0; background: transparent; color: #93A2B8; cursor: pointer;
}
.rig-workspace-panel-tabs button.is-active { background: #0d1219; color: #EEF4FC; }
.rig-workspace-panel-body { flex: 1; overflow: auto; padding: 12px; background: #0d1219; }

.rig-audit-spine {
  display: flex; align-items: center; gap: 12px; min-height: 32px; padding: 0 12px;
  border-top: 1px solid rgba(164, 196, 228, 0.12); background: #0A0D12; overflow: hidden;
}
.rig-audit-spine-track { display: flex; gap: 16px; overflow-x: auto; flex: 1; }
.rig-audit-event { display: flex; align-items: center; gap: 8px; white-space: nowrap; font-size: 0.72rem; color: #93A2B8; }

.rig-dock {
  position: fixed; right: 16px; bottom: 16px; z-index: 40;
  display: flex; gap: 4px; padding: 6px; border-radius: 12px;
  border: 1px solid rgba(164, 196, 228, 0.14); background: #111722;
}

.rig-decision-bar, .rig-decision-rail {
  display: flex; flex-wrap: wrap; align-items: flex-end; gap: 12px;
  min-height: 64px; padding: 12px 16px;
  border-top: 1px solid rgba(164, 196, 228, 0.14); background: #111722;
}
.rig-decision-rail { flex-direction: column; align-items: stretch; min-height: auto; border-top: 0; border-left: 1px solid rgba(164, 196, 228, 0.12); height: 100%; }

.rig-timeline { display: flex; flex-direction: column; gap: 0; padding: 8px 0; }
.rig-timeline-item { display: flex; gap: 12px; }
.rig-timeline-rail { width: 14px; display: flex; flex-direction: column; align-items: center; }
.rig-timeline-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.rig-timeline-line { width: 1px; flex: 1; min-height: 16px; background: rgba(164, 196, 228, 0.16); margin: 4px 0; }
.rig-timeline-body { flex: 1; padding-bottom: 16px; min-width: 0; }

.rig-sparkline, .rig-forecast-chart { width: 100%; height: 100%; }
.rig-health-ring { display: grid; place-items: center; border-radius: 50%; position: relative; }
.rig-health-ring-inner {
  position: absolute; inset: 10px; border-radius: 50%; background: #111722;
  display: grid; place-items: center; text-align: center;
}

.rig-tag-overlay {
  position: absolute; z-index: 2; padding: 6px 8px; border-radius: 6px;
  background: #111722; border: 1px solid rgba(164, 196, 228, 0.2); font-size: 0.72rem; pointer-events: none;
}

.rig-decision-queue { display: flex; flex-direction: column; gap: 4px; overflow: auto; }
.rig-signal-panel {
  display: flex; gap: 12px; overflow-x: auto; min-height: 120px; padding: 12px;
  border-top: 1px solid rgba(164, 196, 228, 0.12); background: #0d1219;
}
.rig-gauge-cluster { display: flex; gap: 16px; flex-wrap: wrap; }
.rig-confidence-meter { display: flex; flex-direction: column; gap: 6px; }
.rig-confidence-track { height: 6px; border-radius: 999px; background: rgba(164, 196, 228, 0.12); overflow: hidden; }
.rig-confidence-fill { height: 100%; border-radius: 999px; background: #5E4DB2; transition: width 200ms ease; }

.rig-evidence-graph { display: flex; flex-wrap: wrap; gap: 8px; }
.rig-evidence-node {
  padding: 8px 10px; border-radius: 8px; border: 1px solid rgba(164, 196, 228, 0.16);
  background: #0d1219; font-size: 0.75rem;
}
.rig-empty-state {
  display: grid; place-items: center; gap: 8px; padding: 30px; text-align: center;
  border: 1px dashed rgba(164, 196, 228, 0.22); border-radius: 10px; background: #0d1219; min-height: 160px;
}
.rig-split-handle {
  width: 6px; cursor: col-resize; background: transparent; border: 0; padding: 0;
  flex-shrink: 0;
}
.rig-split-handle:hover, .rig-split-handle:focus-visible { background: rgba(38, 132, 255, 0.35); }
.rig-approval-stamp {
  padding: 12px; border-radius: 8px; border: 1px solid rgba(164, 196, 228, 0.16); background: #0d1219;
}
.rig-provenance {
  display: inline-flex; padding: 1px 6px; border-radius: 4px; font-size: 0.62rem; font-weight: 700;
  letter-spacing: 0.06em; text-transform: uppercase; border: 1px solid currentColor; opacity: 0.9;
}

html[data-rigos-theme='light'] .rig-surface-1,
html[data-rigos-theme='light'] .rig-metric-card,
html[data-rigos-theme='light'] .rig-signal-card,
html[data-rigos-theme='light'] .rig-operations-strip,
html[data-rigos-theme='light'] .rig-work-order-card,
html[data-rigos-theme='light'] .rig-agent-stage,
html[data-rigos-theme='light'] .rig-evidence-panel,
html[data-rigos-theme='light'] .rig-trace-panel,
html[data-rigos-theme='light'] .rig-recommendation-panel,
html[data-rigos-theme='light'] .rig-case-dossier,
html[data-rigos-theme='light'] .rig-brief-document,
html[data-rigos-theme='light'] .rig-decision-bar,
html[data-rigos-theme='light'] .rig-dock { background: #fff; border-color: rgba(15, 23, 42, 0.1); color: #111827; }
html[data-rigos-theme='light'] .rig-label,
html[data-rigos-theme='light'] .rig-audit-event { color: #64748b; }
html[data-rigos-theme='light'] .rig-object-inspector,
html[data-rigos-theme='light'] .rig-surface-2,
html[data-rigos-theme='light'] .rig-empty-state { background: #f8fafc; border-color: rgba(15, 23, 42, 0.1); }

@media (prefers-reduced-motion: reduce) {
  .rig-status-badge.is-pulse i,
  .rig-metric-card .rig-kpi,
  .rig-agent-stage,
  .rig-object-row,
  .rig-confidence-fill { animation: none !important; transition: none !important; }
  .rig-agent-stage.is-active { transform: none; }
}
```

## frontend/src/design-system/CatalogPreview.jsx

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/CatalogPreview.jsx`

```javascript
/**
 * Isolated design-system preview — Epic 1 exit criterion.
 * Not a product page. Route: /__catalog
 */
import { useState } from 'react';
import { Box, CssBaseline, Divider, Stack, ThemeProvider, Typography } from '@mui/material';
import { useColorMode } from '../context/ColorModeContext';
import { createRigOSV2Theme } from './RigOSV2Theme';
import './catalog.css';
import './motion.css';
import {
  AgentPipeline, ApprovalStamp, AssetTreeNode, AuditSpine, BriefDocument, CaseDossier,
  CommandBar, ConfidenceMeter, DecisionBar, DecisionQueue, Dock, EmptyState,
  EvidenceAppendixLink, EvidenceGraph, EvidencePanel, FilterChipBar, ForecastChart,
  GaugeCluster, HealthRing, IncidentQueueItem, MetricCard, ObjectInspector, ObjectRow,
  OperationsStrip, PrimaryCTA, ProcessSchematic, ProvenanceBadge, RecommendationPanel,
  ReportIndexItem, RiskBadge, ScenarioSlider, ScopeSwitcher, SectionHeader, SignalCard,
  SignalPanel, Sparkline, StatusBadge, SyncIndicator, Timeline, Toolbar, TracePanel,
  UnitRiskMap, WorkOrderCard, WorkspaceHeader, WorkspacePanel,
} from './catalog';

function Section({ title, children }) {
  return (
    <Box sx={{ mb: 4 }}>
      <Typography className="rig-label" sx={{ mb: 1.5 }}>{title}</Typography>
      {children}
    </Box>
  );
}

function CatalogBody() {
  const { mode, toggle } = useColorMode();
  const [commandOpen, setCommandOpen] = useState(false);
  const [panelOpen, setPanelOpen] = useState(false);
  const [rationale, setRationale] = useState('');
  const [scenario, setScenario] = useState(2);
  const [selectedStage, setSelectedStage] = useState('sensor');

  const stages = [
    { id: 'sensor', name: 'Sensor', state: 'complete', duration: 1.2, confidence: 92, reasoning: 'Vibration spike correlated with tag PI-101.' },
    { id: 'diagnostic', name: 'Diagnostic', state: 'running', duration: 0.8, confidence: 74, reasoning: 'Evaluating bearing wear hypothesis.' },
    { id: 'maintenance', name: 'Maintenance', state: 'queued', confidence: 0 },
  ];

  return (
    <ThemeProvider theme={createRigOSV2Theme(mode)}>
      <CssBaseline />
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', color: 'text.primary', p: 3, maxWidth: 1200, mx: 'auto' }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
          <Box>
            <Typography className="rig-label">RigOS design system</Typography>
            <Typography component="h1" sx={{ fontSize: '1.75rem', fontWeight: 600 }}>Component catalog</Typography>
            <Typography variant="body2" color="text.secondary">Epic 1 isolated preview · not a product workspace</Typography>
          </Box>
          <PrimaryCTA onClick={toggle}>{mode === 'dark' ? 'Light mode' : 'Dark mode'}</PrimaryCTA>
        </Stack>

        <Section title="Shell">
          <WorkspaceHeader
            title="Command Center"
            breadcrumbs={[
              { label: 'Alpha Refinery' },
              { label: 'Command Center' },
            ]}
            scope="Alpha Refinery"
            facilities={['Alpha Refinery', 'Enterprise view']}
            connected
            syncAge={2}
            actions={<PrimaryCTA onClick={() => setCommandOpen(true)}>Open CommandBar</PrimaryCTA>}
          />
          <OperationsStrip
            metrics={[
              { label: 'Fleet health', value: '86%', detail: 'Within envelope' },
              { label: 'Open incidents', value: '2', detail: '1 critical' },
              { label: 'Assets online', value: '48' },
              { label: 'Agents active', value: '1' },
            ]}
            cta={<PrimaryCTA>Review investigation</PrimaryCTA>}
            sx={{ mt: 2 }}
          />
          <Toolbar sx={{ mt: 2 }}>
            <ScopeSwitcher value="Alpha Refinery" options={['Alpha Refinery', 'Enterprise view']} />
            <SyncIndicator connected syncAge={3} />
            <FilterChipBar chips={[{ label: 'Critical', onRemove: () => {} }]} onClear={() => {}} />
          </Toolbar>
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mt: 2 }}>
            <UnitRiskMap
              units={[
                { id: 'u1', name: 'Crude unit', health: 88 },
                { id: 'u2', name: 'Hydrotreater', health: 62, status: 'attention' },
                { id: 'u3', name: 'Utilities', health: 91 },
                { id: 'u4', name: 'Tank farm', health: 44, status: 'critical' },
              ]}
              sx={{ flex: 1 }}
            />
            <DecisionQueue
              items={[
                { id: 'i1', kind: 'incident', title: 'Pump vibration high', severity: 'critical', assetName: 'P-101', age: '12m' },
                { id: 'i2', title: 'Schedule seal inspection', status: 'Ready' },
              ]}
              sx={{ flex: 1, border: '1px solid', borderColor: 'divider', borderRadius: 1, p: 1 }}
            />
          </Stack>
          <AuditSpine
            events={[
              { who: 'A. Rao', what: 'Accepted recommendation', when: '14:02', objectLabel: 'INC-2847' },
              { who: 'System', what: 'Investigation started', when: '13:51', objectLabel: 'P-101' },
            ]}
            sx={{ mt: 2 }}
          />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Data display">
          <Stack direction="row" spacing={2} flexWrap="wrap" useFlexGap>
            <MetricCard label="Fleet health" value="86%" delta="+1.2" provenance="live" tone="nominal" sx={{ width: 200 }} />
            <SignalCard name="PI-101" value={4.2} unit="mm/s" threshold={5} provenance="live" sx={{ width: 200 }} />
            <HealthRing value={72} />
            <Box sx={{ width: 160 }}>
              <Sparkline values={[70, 72, 68, 74, 71, 69, 66]} label="Health trend" />
              <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                <StatusBadge status="critical" label="Critical" live />
                <RiskBadge value={78} />
                <ProvenanceBadge value="estimated" />
              </Stack>
            </Box>
          </Stack>
          <ForecastChart
            series={[90, 88, 85, 82, 78, 74, 70]}
            band={{ high: [92, 90, 88, 86, 84, 82, 80], low: [88, 85, 82, 78, 72, 68, 62] }}
            threshold={65}
            provenance="estimated"
            sx={{ mt: 2, maxWidth: 480 }}
          />
          <ConfidenceMeter value={81} sx={{ mt: 2, maxWidth: 320 }} />
          <EmptyState title="No assets match" description="Adjust scope or wait for telemetry sync." sx={{ mt: 2 }} />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Objects & lists">
          <ObjectRow name="P-101 Crude Pump" secondaryId="AST-1021" status="attention" selected />
          <IncidentQueueItem id="INC-2847" title="Bearing vibration anomaly" severity="critical" assetName="P-101" age="8m" />
          <WorkOrderCard title="Replace bearing assembly" priority="P1" asset="P-101" cost={18500} window="6h" sx={{ mt: 1, maxWidth: 280 }} />
          <AssetTreeNode name="Crude unit" health={88} expanded>
            <AssetTreeNode name="P-101" health={62} depth={1} selected />
          </AssetTreeNode>
          <ReportIndexItem title="Alpha weekly brief" date="2026-07-26" approvalState="Awaiting" />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Twin">
          <ProcessSchematic
            nodes={[
              { id: 'n1', label: 'Feed', x: 40, y: 70 },
              { id: 'n2', label: 'P-101', x: 190, y: 70, risk: true },
              { id: 'n3', label: 'HX-2', x: 340, y: 70 },
            ]}
            selectedId="n2"
            overlays={[{ label: 'Vibration', value: '4.2', unit: 'mm/s', x: 200, y: 20 }]}
          />
          <GaugeCluster gauges={[{ label: 'Vib', value: 72 }, { label: 'Temp', value: 54 }, { label: 'Flow', value: 88 }]} sx={{ mt: 2 }} />
          <SignalPanel
            signals={[
              { name: 'Vibration', value: 4.2, unit: 'mm/s', values: [3, 3.2, 3.8, 4.2] },
              { name: 'Temp', value: 82, unit: '°C', values: [78, 79, 81, 82] },
            ]}
            sx={{ mt: 2 }}
          />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Investigation">
          <AgentPipeline stages={stages} selectedId={selectedStage} onSelect={(s) => setSelectedStage(s.id)} />
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mt: 2 }}>
            <TracePanel stages={stages} selectedId={selectedStage} onSelect={(s) => setSelectedStage(s.id)} sx={{ flex: 1 }} />
            <EvidencePanel items={[{ title: 'Telemetry spike', source: 'PI-101', detail: '4.2 mm/s at 13:48' }]} sx={{ flex: 1 }} />
          </Stack>
          <EvidenceGraph nodes={[{ type: 'sensor', label: 'PI-101' }, { type: 'event', label: 'Spike' }, { type: 'asset', label: 'P-101' }]} sx={{ mt: 2 }} />
          <RecommendationPanel recommendation="Reduce load 8% and schedule bearing inspection within 48h." confidence={81} sx={{ mt: 2 }} />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Time & panels">
          <Timeline
            variant="incident"
            items={[
              { title: 'Detection', time: '13:48', detail: 'Vibration exceeded advisory band', status: 'attention' },
              { title: 'AI recommendation', time: '13:55', detail: 'Reduce load and inspect', decision: 'pending', status: 'ai-active' },
            ]}
          />
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mt: 2 }}>
            <ObjectInspector
              title="P-101 Crude Pump"
              subtitle="Identity"
              sections={[
                { title: 'State', content: <Stack direction="row" spacing={1}><StatusBadge status="attention" label="Attention" /><RiskBadge value={62} /></Stack> },
                { title: 'Signals', content: <Sparkline values={[70, 68, 65, 62]} /> },
              ]}
              sx={{ flex: 1 }}
            />
            <CaseDossier
              evidence={[{ title: 'Audit trail', source: 'MAO' }]}
              recommendation="Approve temporary derate"
              confidence={78}
              sx={{ flex: 1 }}
            />
          </Stack>
          <DecisionBar
            recommendation="Approve temporary derate"
            rationale={rationale}
            onRationaleChange={setRationale}
            onAccept={() => {}}
            onModify={() => {}}
            onReject={() => {}}
            sx={{ mt: 2 }}
          />
          <ScenarioSlider value={scenario} onChange={setScenario} sx={{ mt: 2, maxWidth: 360 }} />
        </Section>

        <Divider sx={{ my: 3 }} />

        <Section title="Executive">
          <BriefDocument
            title="Alpha refinery operating brief"
            summary="One critical asset requires operator decision within this shift."
            metrics={[{ label: 'Confidence', value: '81%' }, { label: 'Exposure', value: 'P1' }]}
            sections={[{ title: 'Ask', body: 'Approve temporary derate and maintenance window.' }]}
          />
          <ApprovalStamp signatory="Plant Manager" timestamp="2026-07-26 14:00" status="Awaiting approval" sx={{ mt: 2, maxWidth: 320 }} />
          <EvidenceAppendixLink sx={{ mt: 1 }} />
          <SectionHeader eyebrow="Section" title="Panel title" description="Supporting copy for section headers." sx={{ mt: 2 }} />
        </Section>

        <CommandBar
          open={commandOpen}
          onClose={() => setCommandOpen(false)}
          commands={[
            { label: 'Go to Assets', description: 'Digital twin workspace', onSelect: () => setCommandOpen(false) },
            { label: 'Toggle theme', onSelect: toggle },
          ]}
        />
        <WorkspacePanel
          open={panelOpen}
          onClose={() => setPanelOpen(false)}
          notifications={[{ id: 1, title: 'Critical vibration', message: 'P-101 exceeded band', severity: 'critical', unread: true, time: '13:48' }]}
          auditContent={<Typography variant="body2">Read-only audit slice for preview.</Typography>}
        />
        <Dock
          onCommand={() => setCommandOpen(true)}
          onCopilot={() => {}}
          onWorkspacePanel={() => setPanelOpen(true)}
          onPin={() => {}}
        />
      </Box>
    </ThemeProvider>
  );
}

export function CatalogPreview() {
  return <CatalogBody />;
}
```

## frontend/src/design-system/components.jsx

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/components.jsx`

```javascript
import { useMemo, useState } from 'react';
import {
  Box, Button, Card, CardContent, Chip, CircularProgress, Dialog, DialogContent, Divider, Drawer, IconButton,
  InputAdornment, LinearProgress, Menu, MenuItem, Paper, Stack, TextField, Tooltip, Typography,
} from '@mui/material';
import { Close, MoreHoriz, Search } from '@mui/icons-material';
import { rigosV2Tokens, semanticTone } from './tokens';

const { color, radius, elevation, motion, typography } = rigosV2Tokens;
const tone = (name = 'neutral') => semanticTone[name] || semanticTone.neutral;
const clamp = (value) => Math.max(0, Math.min(100, value || 0));

export function V2PrimaryButton({ children, loading, disabled, sx, ...props }) { return <Button variant="contained" disabled={disabled || loading} sx={{ px: 2, color: '#fff', background: `linear-gradient(135deg, ${color.blue}, ${color.violet})`, transition: `transform ${motion.fast} ${motion.standard}, box-shadow ${motion.fast} ${motion.standard}`, '&:hover': { transform: 'translateY(-1px)', boxShadow: elevation.glowViolet }, ...sx }} {...props}>{loading ? <CircularProgress size={17} color="inherit" /> : children}</Button>; }
export function V2GhostButton({ children, loading, disabled, sx, ...props }) { return <Button variant="text" disabled={disabled || loading} sx={{ color: 'text.secondary', '&:hover': { color: 'text.primary', bgcolor: 'action.hover' }, ...sx }} {...props}>{loading ? <CircularProgress size={17} /> : children}</Button>; }
export function V2CommandButton({ label = 'Search or run a command…', shortcut = '⌘ K', onClick, disabled, sx }) { return <Button onClick={onClick} disabled={disabled} variant="outlined" sx={{ justifyContent: 'space-between', minWidth: 260, color: 'text.secondary', borderColor: 'divider', bgcolor: 'action.hover', '&:hover': { borderColor: color.cyan, color: 'text.primary', transform: 'translateY(-1px)' }, ...sx }}>{label}<Typography component="span" sx={{ ...typography.mono, opacity: .65 }}>{shortcut}</Typography></Button>; }

export function V2StatusBadge({ label, tone: toneName = 'neutral', pulse = false, loading = false, sx }) { const t = tone(toneName); return <Chip label={loading ? 'Loading…' : label} size="small" sx={{ color: t.main, bgcolor: t.soft, fontWeight: 800, letterSpacing: '.07em', '&::before': { content: '""', width: 6, height: 6, borderRadius: 9, display: 'inline-block', bgcolor: t.main, mr: .75, animation: pulse ? 'rigos-v2-pulse 1.6s infinite' : 'none' }, ...sx }} />; }
export function V2AlertChip({ children, tone: toneName = 'warning', active, sx }) { const t = tone(toneName); return <Chip label={children} size="small" sx={{ color: t.main, bgcolor: active ? t.soft : 'transparent', border: `1px solid ${t.main}55`, fontWeight: 750, ...sx }} />; }

export function V2GlassCard({ children, hover = true, active = false, loading = false, sx, ...props }) { return <Card {...props} className={active ? 'rigos-v2-glow' : undefined} sx={{ overflow: 'hidden', borderRadius: radius.lg, bgcolor: 'background.paper', boxShadow: active ? elevation.glowCyan : elevation.low, transition: `transform ${motion.normal} ${motion.standard}, box-shadow ${motion.normal} ${motion.standard}`, ...(hover && { '&:hover': { transform: 'translateY(-3px)', boxShadow: elevation.medium } }), ...sx }}>{loading ? <Box className="rigos-v2-shimmer" sx={{ height: 3 }} /> : null}{children}</Card>; }
export function V2FloatingPanel({ children, active, sx }) { return <Paper className={active ? 'rigos-v2-enter' : undefined} sx={{ p: 2, borderRadius: radius.xl, boxShadow: elevation.medium, ...sx }}>{children}</Paper>; }
export function V2InspectorPanel({ open, onClose, title, subtitle, children, width = 460 }) { return <Drawer anchor="right" open={open} onClose={onClose} PaperProps={{ sx: { width: { xs: '100%', sm: width }, p: 2.5, bgcolor: 'background.paper', backdropFilter: 'blur(28px)' } }}><Stack direction="row" justifyContent="space-between"><Box><Typography sx={typography.caption} color="text.secondary">INSPECTOR</Typography><Typography variant="h5">{title}</Typography>{subtitle && <Typography variant="body2" color="text.secondary">{subtitle}</Typography>}</Box><IconButton onClick={onClose}><Close /></IconButton></Stack><Divider sx={{ my: 2 }} />{children}</Drawer>; }

export function V2HealthRing({ value, label = 'Health', size = 112, loading = false }) { const percent = clamp(value); const ringTone = percent < 50 ? tone('danger').main : percent < 80 ? tone('warning').main : tone('success').main; return <Box sx={{ width: size, height: size, borderRadius: '50%', display: 'grid', placeItems: 'center', background: `conic-gradient(${ringTone} ${percent * 3.6}deg, rgba(128,148,177,.16) 0)` }}><Box sx={{ width: size - 18, height: size - 18, borderRadius: '50%', display: 'grid', placeItems: 'center', bgcolor: 'background.paper', textAlign: 'center' }}>{loading ? <CircularProgress size={22} /> : <><Typography sx={{ fontSize: size * .22, lineHeight: 1, fontWeight: 800, color: ringTone }}>{Math.round(percent)}%</Typography><Typography variant="caption" color="text.secondary">{label}</Typography></>}</Box></Box>; }
export function V2ProgressIndicator({ value, label, tone: toneName = 'info', loading = false, sx }) { const t = tone(toneName); return <Box sx={sx}>{label && <Stack direction="row" justifyContent="space-between" sx={{ mb: .6 }}><Typography variant="caption" color="text.secondary">{label}</Typography><Typography variant="caption" sx={{ color: t.main }}>{Math.round(clamp(value))}%</Typography></Stack>}<LinearProgress variant={loading ? 'indeterminate' : 'determinate'} value={clamp(value)} sx={{ height: 6, borderRadius: 9, bgcolor: 'action.hover', '& .MuiLinearProgress-bar': { bgcolor: t.main, borderRadius: 9 } }} /></Box>; }
export function V2ConfidenceMeter({ value, label = 'Confidence', loading }) { return <V2ProgressIndicator value={value} label={label} tone="violet" loading={loading} />; }

export function V2AIAgentCard({ name, task, state = 'idle', confidence, evidenceCount, active, loading, onClick }) {
  const stateTone = state === 'failed' ? 'danger' : state === 'working' ? 'info' : state === 'complete' ? 'success' : 'neutral';
  return (
    <V2GlassCard hover active={active} loading={loading} onClick={onClick} sx={{ cursor: onClick ? 'pointer' : 'default' }}>
      <CardContent sx={{ p: 1.6 }}>
        <Stack direction="row" justifyContent="space-between">
          <Stack direction="row" spacing={1} alignItems="center">
            <Box sx={{ width: 30, height: 30, display: 'grid', placeItems: 'center', borderRadius: 2, color: tone(stateTone).main, bgcolor: tone(stateTone).soft, fontWeight: 850 }}>{name?.slice(0, 1)}</Box>
            <Box>
              <Typography sx={typography.title}>{name}</Typography>
              <Typography variant="caption" color="text.secondary">{task || 'Standing by'}</Typography>
            </Box>
          </Stack>
          <V2StatusBadge label={state} tone={stateTone} pulse={state === 'working'} />
        </Stack>
        {confidence != null && <V2ConfidenceMeter value={confidence} label={evidenceCount != null ? `${evidenceCount} evidence items` : 'Confidence'} />}
      </CardContent>
    </V2GlassCard>
  );
}
export function V2Timeline({ items = [], loading = false, onSelect }) { return <Stack spacing={0}>{items.map((item, index) => { const t = tone(item.tone || (item.state === 'failed' ? 'danger' : item.state === 'active' ? 'info' : 'success')); return <Box key={item.id || index} onClick={() => onSelect?.(item)} sx={{ display: 'flex', gap: 1.3, pb: index === items.length - 1 ? 0 : 2, cursor: onSelect ? 'pointer' : 'default' }}><Box sx={{ width: 14, display: 'flex', flexDirection: 'column', alignItems: 'center' }}><Box sx={{ mt: .55, width: 9, height: 9, borderRadius: 9, bgcolor: t.main, boxShadow: item.state === 'active' ? `0 0 15px ${t.main}` : 'none' }} />{index < items.length - 1 && <Box sx={{ width: 1, flex: 1, minHeight: 20, bgcolor: 'divider', my: .75 }} />}</Box><Box flex={1}><Stack direction="row" justifyContent="space-between"><Typography sx={typography.title}>{item.title}</Typography><Typography variant="caption" color="text.secondary">{item.time}</Typography></Stack><Typography variant="body2" color="text.secondary">{item.description}</Typography>{item.meta && <Typography sx={{ ...typography.mono, color: t.main, mt: .5 }}>{item.meta}</Typography>}</Box></Box>; })}{loading && <LinearProgress />}</Stack>; }
export function V2EvidenceCard({ title, source, confidence, children, expanded = false, onClick }) { return <V2GlassCard hover onClick={onClick} sx={{ cursor: onClick ? 'pointer' : 'default', boxShadow: expanded ? elevation.medium : elevation.low }}><CardContent sx={{ p: 1.5 }}><Stack direction="row" justifyContent="space-between"><Box><Typography sx={typography.title}>{title}</Typography><Typography variant="caption" color="text.secondary">{source}</Typography></Box>{confidence != null && <V2StatusBadge label={`${Math.round(confidence)}%`} tone="info" />}</Stack>{children && <Box sx={{ mt: 1.1 }}>{children}</Box>}</CardContent></V2GlassCard>; }
export function V2RecommendationCard({ title = 'Recommended next action', recommendation, tone: toneName = 'info', action, loading }) { const t = tone(toneName); return <V2GlassCard loading={loading} sx={{ borderLeft: `3px solid ${t.main}` }}><CardContent><Typography sx={{ ...typography.caption, color: t.main }}>{title}</Typography><Typography sx={{ ...typography.title, mt: .6 }}>{recommendation}</Typography>{action && <Box sx={{ mt: 1.5 }}>{action}</Box>}</CardContent></V2GlassCard>; }

export function V2MetricStrip({ metrics = [] }) { return <Stack direction={{ xs: 'column', md: 'row' }} divider={<Divider flexItem orientation="vertical" />} sx={{ borderRadius: radius.lg, overflow: 'hidden', bgcolor: 'background.paper', boxShadow: elevation.low }}>{metrics.map((metric, index) => <Box key={metric.label || index} sx={{ px: 2.25, py: 1.65, flex: 1 }}><Typography sx={{ ...typography.caption, color: 'text.secondary' }}>{metric.label}</Typography><Typography sx={{ ...typography.heading, color: metric.color || 'text.primary', mt: .2 }}>{metric.loading ? '—' : metric.value}</Typography><Typography variant="caption" color="text.secondary">{metric.detail}</Typography></Box>)}</Stack>; }
export function V2FacilityNode({ label, type, health, active, onClick, loading }) { const healthTone = health < 50 ? 'danger' : health < 80 ? 'warning' : 'success'; const t = tone(healthTone); return <Box onClick={onClick} className={active ? 'rigos-v2-glow' : undefined} sx={{ p: 1.25, minWidth: 108, borderRadius: radius.md, bgcolor: t.soft, border: `1px solid ${t.main}44`, cursor: onClick ? 'pointer' : 'default', transition: `transform ${motion.fast} ${motion.standard}`, '&:hover': onClick ? { transform: 'translateY(-2px)' } : {}, opacity: loading ? .65 : 1 }}><Box sx={{ width: 8, height: 8, borderRadius: 9, bgcolor: t.main, mb: .8 }} /><Typography sx={typography.title}>{label}</Typography><Typography variant="caption" color="text.secondary">{type} · {loading ? 'syncing' : `${Math.round(health)}%`}</Typography></Box>; }

export function V2NavigationItem({ icon, label, active, disabled, onClick }) { return <Button disabled={disabled} onClick={onClick} startIcon={icon} sx={{ minWidth: 0, width: '100%', justifyContent: 'flex-start', color: active ? 'primary.main' : 'text.secondary', bgcolor: active ? 'rgba(40,124,255,.10)' : 'transparent', borderRadius: radius.md, '&:hover': { bgcolor: 'action.hover', color: 'text.primary' } }}>{label}</Button>; }
export function V2SearchBar({ value, onChange, placeholder = 'Search…', loading, onSubmit, sx }) { return <TextField value={value} onChange={(event) => onChange?.(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && onSubmit?.(value)} placeholder={placeholder} fullWidth InputProps={{ startAdornment: <InputAdornment position="start">{loading ? <CircularProgress size={16} /> : <Search fontSize="small" />}</InputAdornment> }} sx={{ '& .MuiOutlinedInput-root': { borderRadius: radius.md, bgcolor: 'action.hover' }, ...sx }} />; }
export function V2SectionHeader({ eyebrow, title, description, action }) { return <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" alignItems={{ md: 'end' }} spacing={1.5}><Box>{eyebrow && <Typography sx={{ ...typography.caption, color: color.cyan }}>{eyebrow}</Typography>}<Typography sx={typography.heading}>{title}</Typography>{description && <Typography variant="body2" color="text.secondary" sx={{ mt: .6, maxWidth: 680 }}>{description}</Typography>}</Box>{action}</Stack>; }
export function V2Toolbar({ children, floating = false, sx }) { return <Stack direction={{ xs: 'column', sm: 'row' }} alignItems={{ sm: 'center' }} spacing={1} sx={{ p: 1, borderRadius: radius.lg, bgcolor: floating ? 'background.paper' : 'transparent', boxShadow: floating ? elevation.low : 'none', ...sx }}>{children}</Stack>; }

export function V2Modal({ open, onClose, title, children, actions, maxWidth = 'sm' }) { return <Dialog open={open} onClose={onClose} fullWidth maxWidth={maxWidth} PaperProps={{ sx: { borderRadius: radius.xl, bgcolor: 'background.paper', backdropFilter: 'blur(28px)' } }}><DialogContent sx={{ p: 2.5 }}><Stack direction="row" justifyContent="space-between"><Typography variant="h5">{title}</Typography><IconButton onClick={onClose}><Close /></IconButton></Stack><Box sx={{ mt: 2 }}>{children}</Box>{actions && <Stack direction="row" justifyContent="flex-end" spacing={1} sx={{ mt: 2.5 }}>{actions}</Stack>}</DialogContent></Dialog>; }
export function V2CommandPalette({ open, onClose, commands = [] }) { const [query, setQuery] = useState(''); const visible = useMemo(() => commands.filter((command) => `${command.label} ${command.description || ''}`.toLowerCase().includes(query.toLowerCase())), [commands, query]); return <V2Modal open={open} onClose={onClose} title="Command palette" maxWidth="sm"><V2SearchBar value={query} onChange={setQuery} placeholder="Search commands…" /><Stack spacing={.5} sx={{ mt: 1.5 }}>{visible.map((command, index) => <Box key={command.id || index} onClick={() => { command.onSelect?.(); onClose?.(); }} sx={{ p: 1.2, borderRadius: radius.md, cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}><Typography sx={typography.title}>{command.label}</Typography><Typography variant="caption" color="text.secondary">{command.description}</Typography></Box>)}</Stack></V2Modal>; }
export function V2DesignDrawer({ open, onClose, title, children, width }) { return <V2InspectorPanel open={open} onClose={onClose} title={title} width={width}>{children}</V2InspectorPanel>; }
export function V2ContextMenu({ anchorEl, onClose, items = [] }) { return <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={onClose}>{items.map((item, index) => <MenuItem key={item.label || index} disabled={item.disabled} onClick={() => { item.onClick?.(); onClose?.(); }}>{item.label}</MenuItem>)}</Menu>; }
export function V2HoverCard({ title, description, children }) { return <Tooltip title={<Box sx={{ p: .4 }}><Typography sx={typography.title}>{title}</Typography><Typography variant="caption">{description}</Typography></Box>} arrow><Box component="span">{children}</Box></Tooltip>; }
export function V2MoreMenu({ items }) { const [anchorEl, setAnchorEl] = useState(null); return <><IconButton onClick={(event) => setAnchorEl(event.currentTarget)}><MoreHoriz /></IconButton><V2ContextMenu anchorEl={anchorEl} onClose={() => setAnchorEl(null)} items={items} /></>; }
```

## frontend/src/design-system/index.js

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/index.js`

```javascript
// Public surface for RigOS design system.
// Epic 1 catalog is canonical for new work. Legacy primitives kept as aliases.

export { createRigOSV2Theme } from './RigOSV2Theme';
export { rigosV2Tokens, semanticTone, statusColors, resolveTone } from './tokens';

// Legacy V2* components (prefixed — no name clashes)
export * from './components';

// Legacy primitives — aliases where names overlap the catalog
export {
  RigCard,
  RigProgress,
  TelemetryChart,
  RigDrawer,
  RigModal,
  Toast,
  NotificationItem,
  RigSearch,
  FloatingPanel,
  PageHeader,
  RigToolbar,
  CommandPalette,
  AIAgentCard,
  TimelineCard,
  MetricCard as LegacyMetricCard,
  StatusBadge as LegacyStatusBadge,
  EmptyState as LegacyEmptyState,
  SectionHeader as LegacySectionHeader,
} from './primitives';

// Epic 1 catalog (canonical)
export * from './catalog';

// Epic 2 layouts + ApplicationShell
export * from './layouts';
```

## frontend/src/design-system/LayoutsPreview.jsx

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/LayoutsPreview.jsx`

```javascript
/**
 * Isolated layouts preview — Epic 2 exit criterion.
 * Route: /__layouts — placeholders only, no live data.
 */
import { useState } from 'react';
import { Box, Button, CssBaseline, Stack, ThemeProvider, Typography } from '@mui/material';
import { useColorMode } from '../context/ColorModeContext';
import { createRigOSV2Theme } from './RigOSV2Theme';
import { AuditSpine, PrimaryCTA } from './catalog';
import {
  ApplicationShell,
  ExplorerLayout,
  ExecutiveLayout,
  IncidentLayout,
  InvestigationLayout,
  KanbanLayout,
  LayoutPlaceholder,
  MissionControlLayout,
} from './layouts';
import './layouts/layouts.css';
import './catalog.css';
import './motion.css';

const LAYOUTS = [
  { id: 'mission', label: 'Mission Control' },
  { id: 'explorer', label: 'Explorer (twin)' },
  { id: 'forecast', label: 'Explorer (forecast)' },
  { id: 'incident', label: 'Incident' },
  { id: 'investigation', label: 'Investigation' },
  { id: 'kanban', label: 'Kanban' },
  { id: 'executive', label: 'Executive' },
];

function LayoutDemo({ id }) {
  switch (id) {
    case 'mission':
      return <MissionControlLayout />;
    case 'explorer':
      return <ExplorerLayout canvasVariant="twin" signalStrip={<LayoutPlaceholder label="signalStrip" />} />;
    case 'forecast':
      return <ExplorerLayout canvasVariant="forecast" />;
    case 'incident':
      return <IncidentLayout />;
    case 'investigation':
      return <InvestigationLayout />;
    case 'kanban':
      return <KanbanLayout />;
    case 'executive':
      return <ExecutiveLayout />;
    default:
      return <LayoutPlaceholder label="Unknown layout" />;
  }
}

function LayoutsBody() {
  const { mode, toggle } = useColorMode();
  const [layoutId, setLayoutId] = useState('mission');
  const isExecutive = layoutId === 'executive';

  return (
    <ThemeProvider theme={createRigOSV2Theme(mode)}>
      <CssBaseline />
      <ApplicationShell
        title={LAYOUTS.find((item) => item.id === layoutId)?.label || 'Layouts'}
        breadcrumbs={[
          { label: 'Design system' },
          { label: 'Layouts preview' },
        ]}
        scope="Alpha Refinery"
        facilities={['Alpha Refinery', 'Enterprise view']}
        connected
        syncAge={1}
        activeNavId={layoutId === 'forecast' ? 'forecasting' : layoutId === 'mission' ? 'command' : layoutId}
        onNavigate={(item) => {
          const map = {
            command: 'mission',
            assets: 'explorer',
            forecasting: 'forecast',
            incidents: 'incident',
            investigation: 'investigation',
            maintenance: 'kanban',
            reports: 'executive',
          };
          if (map[item.id]) setLayoutId(map[item.id]);
        }}
        showAuditSpine={!isExecutive}
        auditSpine={(
          <AuditSpine
            events={[
              { who: 'Preview', what: 'Layout slot demo', when: 'now', objectLabel: layoutId },
            ]}
          />
        )}
        headerActions={<PrimaryCTA onClick={toggle}>{mode === 'dark' ? 'Light' : 'Dark'}</PrimaryCTA>}
        workspacePanelAudit={<Typography variant="body2" color="text.secondary">WorkspacePanel slot — no API.</Typography>}
        notifications={[{ id: 1, title: 'Preview notice', message: 'Epic 2 placeholder', unread: true }]}
      >
        <Stack spacing={1.5} sx={{ height: '100%', minHeight: 0 }}>
          <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
            {LAYOUTS.map((item) => (
              <Button
                key={item.id}
                size="small"
                variant={layoutId === item.id ? 'contained' : 'outlined'}
                onClick={() => setLayoutId(item.id)}
                sx={{ textTransform: 'none' }}
              >
                {item.label}
              </Button>
            ))}
          </Stack>
          <Typography variant="caption" color="text.secondary">
            Epic 2 preview · slot placeholders only · resize below 1024px for tab mode
          </Typography>
          <Box sx={{ flex: 1, minHeight: 420 }}>
            <LayoutDemo id={layoutId} />
          </Box>
        </Stack>
      </ApplicationShell>
    </ThemeProvider>
  );
}

export function LayoutsPreview() {
  return <LayoutsBody />;
}
```

## frontend/src/design-system/motion.css

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/motion.css`

```css
@keyframes rigos-v2-fade-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes rigos-v2-pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: .55; transform: scale(.92); } }
@keyframes rigos-v2-glow { 0%, 100% { box-shadow: 0 0 12px rgba(88,216,255,.14); } 50% { box-shadow: 0 0 28px rgba(88,216,255,.48); } }
@keyframes rigos-v2-shimmer { from { background-position: 180% 0; } to { background-position: -180% 0; } }
.rigos-v2-enter { animation: rigos-v2-fade-up 240ms cubic-bezier(.2,.8,.2,1) both; }
.rigos-v2-ai-pulse { animation: rigos-v2-pulse 2s cubic-bezier(.2,.8,.2,1) infinite; }
.rigos-v2-glow { animation: rigos-v2-glow 2.4s ease-in-out infinite; }
.rigos-v2-shimmer { background: linear-gradient(100deg, transparent 32%, rgba(88,216,255,.26) 50%, transparent 68%); background-size: 220% 100%; animation: rigos-v2-shimmer 2.2s linear infinite; }
@media (prefers-reduced-motion: reduce) { .rigos-v2-enter, .rigos-v2-ai-pulse, .rigos-v2-glow, .rigos-v2-shimmer { animation: none !important; } }
```

## frontend/src/design-system/primitives.css

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/primitives.css`

```css
.rig-card { background:#111722; border:1px solid rgba(164,196,228,.14); border-radius:18px; box-shadow:0 8px 24px rgba(0,0,0,.12); overflow:hidden; }
.rig-label { color:#93a2b8; font-size:.68rem!important; font-weight:750!important; letter-spacing:.11em!important; text-transform:uppercase; }
.rig-metric-value { color:#eef4fc; font-size:clamp(1.8rem,3vw,2.65rem)!important; font-weight:780!important; letter-spacing:-.055em!important; line-height:1!important; font-variant-numeric:tabular-nums; }.rig-metric-trend,.rig-mono { font-family:"DM Mono",Consolas,monospace!important; font-size:.72rem!important; }
.rig-badge { display:inline-flex; align-items:center; min-height:24px; padding:0 9px; border-radius:999px; font-size:.67rem; font-weight:750; letter-spacing:.07em; text-transform:uppercase; white-space:nowrap; }.rig-badge i { width:6px; height:6px; margin-right:7px; border-radius:50%; }
.rig-agent-icon,.rig-empty-icon { display:grid; place-items:center; flex:none; width:32px; height:32px; border-radius:10px; color:#58d8ff; background:rgba(88,216,255,.1); font-weight:800; }.rig-timeline-row { display:flex; gap:12px; outline:none; }.rig-timeline-row:focus-visible { border-radius:8px; box-shadow:0 0 0 2px #58d8ff; }.rig-timeline-rail { display:flex; flex-direction:column; align-items:center; width:10px; }.rig-timeline-dot { width:8px; height:8px; margin-top:7px; border-radius:50%; }.rig-timeline-line { flex:1; width:1px; min-height:28px; margin:6px 0; background:rgba(164,196,228,.18); }
.rig-empty { display:grid; place-items:center; min-height:230px; gap:10px; text-align:center; }.rig-empty-icon { width:38px; height:38px; }.rig-chart .recharts-default-tooltip { outline:none; }.rig-overlay { background:rgba(17,23,34,.97)!important; border:1px solid rgba(164,196,228,.16); color:#eef4fc; box-shadow:-18px 0 60px rgba(0,0,0,.3); }
.rig-toast { position:fixed; top:22px; right:22px; z-index:1500; display:flex; align-items:flex-start; gap:12px; width:min(410px,calc(100vw - 32px)); padding:14px; border:1px solid rgba(164,196,228,.16); border-radius:14px; background:#171e29; box-shadow:0 18px 46px rgba(0,0,0,.32); }.rig-toast-rule { width:3px; min-height:34px; border-radius:4px; }.rig-notification { display:flex; gap:10px; padding:12px 0; border-bottom:1px solid rgba(164,196,228,.1); }.rig-notification-dot { width:6px; height:6px; margin-top:7px; border-radius:50%; }
.rig-search .MuiOutlinedInput-root { background:rgba(255,255,255,.035); border-radius:12px; }.rig-search .MuiOutlinedInput-notchedOutline { border-color:rgba(164,196,228,.16)!important; }.rig-search .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline { border-color:#58d8ff!important; }.rig-command { display:flex; align-items:center; justify-content:space-between; gap:16px; padding:11px 12px; border-radius:10px; cursor:pointer; }.rig-command kbd { padding:3px 6px; border:1px solid rgba(164,196,228,.18); border-radius:5px; color:#93a2b8; font:500 .67rem "DM Mono",monospace; }.rig-toolbar { display:flex; flex-wrap:wrap; align-items:center; gap:8px; }.rig-toolbar-float,.rig-floating-panel { border:1px solid rgba(164,196,228,.14); background:rgba(17,23,34,.92); box-shadow:0 16px 44px rgba(0,0,0,.24); backdrop-filter:blur(18px); }.rig-toolbar-float { padding:8px; border-radius:14px; }.rig-section-header { margin:36px 0 16px; }.rig-page-header { margin-bottom:30px; }.rig-page-title { color:#eef4fc; font-size:clamp(2rem,4vw,3.4rem)!important; font-weight:780!important; letter-spacing:-.06em!important; line-height:1!important; }.rig-floating-panel { position:fixed; z-index:1200; padding:14px; border-radius:16px; }.rig-floating-panel.is-bottom-right { right:24px; bottom:24px; }.rig-floating-panel.is-bottom-left { left:24px; bottom:24px; }
@media (prefers-reduced-motion:reduce) { .rig-card,.rig-command,.rig-notification { transition:none!important; } }
```

## frontend/src/design-system/primitives.jsx

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/primitives.jsx`

```javascript
import { useMemo, useState } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'motion/react';
import {
  Box, Dialog, DialogContent, Drawer, IconButton, InputAdornment, LinearProgress,
  Stack, TextField, Typography,
} from '@mui/material';
import { Close, Search, Terminal } from '@mui/icons-material';
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { semanticTone } from './tokens';

const spring = { type: 'spring', stiffness: 420, damping: 32, mass: 0.7 };
const toneFor = (name) => semanticTone[name] || semanticTone.neutral;
const MotionBox = motion.create(Box);

export function RigCard({ children, interactive = false, active = false, padding = 2, sx, ...props }) {
  const reduced = useReducedMotion();
  return <MotionBox {...props} className="rig-card" initial={false} whileHover={interactive && !reduced ? { y: -2 } : undefined} whileTap={interactive && !reduced ? { scale: 0.995 } : undefined} transition={spring} sx={{ p: padding, cursor: interactive ? 'pointer' : 'default', ...(active && { borderColor: 'rgba(88,216,255,.46)', boxShadow: '0 0 0 1px rgba(88,216,255,.08), 0 14px 40px rgba(0,0,0,.18)' }), ...sx }}>{children}</MotionBox>;
}

export function MetricCard({ label, value, detail, trend, tone = 'neutral', loading = false, children }) {
  const t = toneFor(tone);
  return <RigCard className="rig-metric" padding={2} aria-busy={loading}><Typography className="rig-label">{label}</Typography><Stack direction="row" alignItems="baseline" spacing={1} sx={{ mt: .7 }}><Typography className="rig-metric-value">{loading ? '—' : value}</Typography>{trend && <Typography className="rig-metric-trend" sx={{ color: t.main }}>{trend}</Typography>}</Stack>{detail && <Typography variant="caption" color="text.secondary">{detail}</Typography>}{children}</RigCard>;
}

export function StatusBadge({ label, tone = 'neutral', live = false, sx }) { const t = toneFor(tone); return <Box component="span" className="rig-badge" sx={{ color: t.main, backgroundColor: t.soft, ...sx }}><motion.i aria-hidden animate={live ? { opacity: [1, .45, 1], scale: [1, .82, 1] } : false} transition={{ duration: 1.7, repeat: Infinity }} style={{ backgroundColor: t.main }} />{label}</Box>; }

export function AIAgentCard({ name, description, state = 'idle', confidence, action, icon }) {
  const stateTone = { working: 'info', complete: 'success', failed: 'danger', waiting: 'warning' }[state] || 'neutral';
  return <RigCard interactive className="rig-agent-card"><Stack direction="row" justifyContent="space-between" spacing={1.5}><Stack direction="row" spacing={1.25} alignItems="center"><Box className="rig-agent-icon">{icon || name?.slice(0, 1)}</Box><Box><Typography fontWeight={750}>{name}</Typography><Typography variant="caption" color="text.secondary">{description || 'Standing by'}</Typography></Box></Stack><StatusBadge label={state} tone={stateTone} live={state === 'working'} /></Stack>{confidence != null && <RigProgress label="Confidence" value={confidence} tone={stateTone} sx={{ mt: 2 }} />}{action && <Box sx={{ mt: 1.5 }}>{action}</Box>}</RigCard>;
}

export function TimelineCard({ items = [], onSelect }) { return <RigCard padding={2}>{items.map((item, index) => { const t = toneFor(item.tone || 'neutral'); return <MotionBox key={item.id || index} role={onSelect ? 'button' : undefined} tabIndex={onSelect ? 0 : undefined} onClick={() => onSelect?.(item)} whileHover={onSelect ? { x: 2 } : undefined} className="rig-timeline-row"><Box className="rig-timeline-rail"><Box className="rig-timeline-dot" sx={{ backgroundColor: t.main }} />{index < items.length - 1 && <Box className="rig-timeline-line" />}</Box><Box sx={{ pb: index < items.length - 1 ? 2 : 0, flex: 1 }}><Stack direction="row" justifyContent="space-between" spacing={2}><Typography fontWeight={700}>{item.title}</Typography><Typography className="rig-mono">{item.time}</Typography></Stack>{item.description && <Typography variant="body2" color="text.secondary" sx={{ mt: .4 }}>{item.description}</Typography>}</Box></MotionBox>; })}</RigCard>; }

export function EmptyState({ title, description, action, icon = <Terminal fontSize="small" /> }) { return <RigCard className="rig-empty" padding={3}><Box className="rig-empty-icon">{icon}</Box><Typography fontWeight={750}>{title}</Typography><Typography variant="body2" color="text.secondary" sx={{ maxWidth: 360 }}>{description}</Typography>{action}</RigCard>; }

export function RigProgress({ label, value, tone = 'info', sx }) { const t = toneFor(tone); return <Box sx={sx}>{label && <Stack direction="row" justifyContent="space-between" sx={{ mb: .65 }}><Typography className="rig-label">{label}</Typography><Typography className="rig-mono" sx={{ color: t.main }}>{Math.round(value || 0)}%</Typography></Stack>}<LinearProgress variant="determinate" value={Math.max(0, Math.min(100, value || 0))} sx={{ '& .MuiLinearProgress-bar': { backgroundColor: t.main } }} /></Box>; }

export function TelemetryChart({ data = [], dataKey = 'value', xKey = 'time', label, tone = 'info', height = 190 }) { const t = toneFor(tone); return <RigCard padding={2} className="rig-chart"><Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}><Typography className="rig-label">{label}</Typography><StatusBadge label="Live" tone={tone} live /></Stack><Box sx={{ height }}><ResponsiveContainer width="100%" height="100%"><AreaChart data={data} margin={{ top: 6, right: 4, left: -22, bottom: 0 }}><defs><linearGradient id={`rig-chart-${dataKey}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={t.main} stopOpacity={.24} /><stop offset="100%" stopColor={t.main} stopOpacity={0} /></linearGradient></defs><XAxis dataKey={xKey} tickLine={false} axisLine={false} tick={{ fill: '#718096', fontSize: 11 }} /><YAxis tickLine={false} axisLine={false} tick={{ fill: '#718096', fontSize: 11 }} /><Tooltip contentStyle={{ background: '#161c25', border: '1px solid rgba(255,255,255,.12)', borderRadius: 10 }} /><Area type="monotone" dataKey={dataKey} stroke={t.main} strokeWidth={2} fill={`url(#rig-chart-${dataKey})`} isAnimationActive /></AreaChart></ResponsiveContainer></Box></RigCard>; }

export function RigDrawer({ open, onClose, title, subtitle, children, width = 480 }) { return <Drawer anchor="right" open={open} onClose={onClose} PaperProps={{ className: 'rig-overlay', sx: { width: { xs: '100%', sm: width } } }}><OverlayHeader title={title} subtitle={subtitle} onClose={onClose} />{children}</Drawer>; }
export function RigModal({ open, onClose, title, subtitle, children, actions, maxWidth = 'sm' }) { return <Dialog open={open} onClose={onClose} fullWidth maxWidth={maxWidth} TransitionComponent={undefined} PaperProps={{ className: 'rig-overlay' }}><DialogContent sx={{ p: 2.5 }}><OverlayHeader title={title} subtitle={subtitle} onClose={onClose} />{children}{actions && <Stack direction="row" justifyContent="flex-end" spacing={1.25} sx={{ mt: 2.5 }}>{actions}</Stack>}</DialogContent></Dialog>; }
function OverlayHeader({ title, subtitle, onClose }) { return <Stack direction="row" justifyContent="space-between" spacing={2} sx={{ mb: 2.25 }}><Box><Typography className="rig-label">SYSTEM INTERFACE</Typography><Typography variant="h6" sx={{ mt: .35 }}>{title}</Typography>{subtitle && <Typography variant="body2" color="text.secondary">{subtitle}</Typography>}</Box><IconButton aria-label="Close" onClick={onClose}><Close /></IconButton></Stack>; }

export function Toast({ open, title, message, tone = 'info', onClose }) { const t = toneFor(tone); return <AnimatePresence>{open && <MotionBox className="rig-toast" role="status" initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={spring}><Box className="rig-toast-rule" sx={{ backgroundColor: t.main }} /><Box><Typography fontWeight={750}>{title}</Typography>{message && <Typography variant="body2" color="text.secondary">{message}</Typography>}</Box><IconButton size="small" onClick={onClose} aria-label="Dismiss notification"><Close fontSize="small" /></IconButton></MotionBox>}</AnimatePresence>; }
export function NotificationItem({ title, message, time, tone = 'info', unread = false, onClick }) { const t = toneFor(tone); return <MotionBox whileHover={{ x: 2 }} onClick={onClick} className="rig-notification" sx={{ cursor: onClick ? 'pointer' : 'default' }}><Box className="rig-notification-dot" sx={{ backgroundColor: unread ? t.main : 'transparent' }} /><Box flex={1}><Stack direction="row" justifyContent="space-between" spacing={2}><Typography fontWeight={700}>{title}</Typography><Typography className="rig-mono">{time}</Typography></Stack><Typography variant="body2" color="text.secondary">{message}</Typography></Box></MotionBox>; }

export function CommandPalette({ open, onClose, commands = [] }) { const [query, setQuery] = useState(''); const filtered = useMemo(() => commands.filter((command) => `${command.label} ${command.description || ''}`.toLowerCase().includes(query.toLowerCase())), [commands, query]); return <RigModal open={open} onClose={onClose} title="Command palette" subtitle="Search actions and navigate the system"><RigSearch autoFocus value={query} onChange={setQuery} placeholder="Type a command…" /><Box sx={{ mt: 1.5 }}>{filtered.map((command, index) => <MotionBox key={command.id || index} whileHover={{ x: 2, backgroundColor: 'rgba(255,255,255,.045)' }} onClick={() => { command.onSelect?.(); onClose?.(); }} className="rig-command"><Box><Typography fontWeight={700}>{command.label}</Typography>{command.description && <Typography variant="caption" color="text.secondary">{command.description}</Typography>}</Box>{command.shortcut && <kbd>{command.shortcut}</kbd>}</MotionBox>)}</Box></RigModal>; }
export function RigSearch({ value, onChange, placeholder = 'Search…', onSubmit, ...props }) { return <TextField {...props} value={value} onChange={(event) => onChange?.(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && onSubmit?.(value)} placeholder={placeholder} fullWidth size="small" InputProps={{ startAdornment: <InputAdornment position="start"><Search fontSize="small" /></InputAdornment> }} className="rig-search" />; }
export function RigToolbar({ children, floating = false, sx }) { return <MotionBox layout className={floating ? 'rig-toolbar rig-toolbar-float' : 'rig-toolbar'} sx={sx}>{children}</MotionBox>; }
export function SectionHeader({ eyebrow, title, description, action }) { return <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" alignItems={{ md: 'end' }} spacing={1.5} className="rig-section-header"><Box>{eyebrow && <Typography className="rig-label">{eyebrow}</Typography>}<Typography variant="h5" sx={{ mt: .45 }}>{title}</Typography>{description && <Typography variant="body2" color="text.secondary" sx={{ mt: .6, maxWidth: 680 }}>{description}</Typography>}</Box>{action}</Stack>; }
export function PageHeader({ eyebrow, title, description, actions }) { return <Stack direction={{ xs: 'column', lg: 'row' }} justifyContent="space-between" alignItems={{ lg: 'end' }} spacing={2.5} className="rig-page-header"><Box>{eyebrow && <Typography className="rig-label">{eyebrow}</Typography>}<Typography component="h1" className="rig-page-title">{title}</Typography>{description && <Typography color="text.secondary" sx={{ mt: 1.25, maxWidth: 720 }}>{description}</Typography>}</Box>{actions && <Stack direction="row" spacing={1}>{actions}</Stack>}</Stack>; }
export function FloatingPanel({ children, position = 'bottom-right', sx }) { return <MotionBox className={`rig-floating-panel is-${position}`} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={spring} sx={sx}>{children}</MotionBox>; }
```

## frontend/src/design-system/README.md

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/README.md`

```markdown
# RigOS V2 design system

This package is the visual foundation for future RigOS screens. It is intentionally not mounted by the existing application during Phase 1.

## Adoption contract

1. Wrap a future V2 surface with MUI's `ThemeProvider` using `createRigOSV2Theme(mode)`.
2. Import `motion.css` once from the application entry point when V2 components are first mounted.
3. Prefer components from `src/design-system` over one-off page styling.
4. Use semantic tones (`success`, `warning`, `danger`, `info`, `violet`, `neutral`) rather than decorative color choices.

## State language

The library uses a shared state vocabulary: `hover`, `active`, `loading`, `disabled`, and `animated` (via the motion classes). Interactive primitives expose the relevant props directly; informational primitives expose active/loading presentation states where meaningful.

## Architecture decisions

- The system is MUI-compatible to preserve the current frontend dependency stack.
- Tokens are centralized in `tokens.js`; `RigOSV2Theme.js` derives light and dark themes from those tokens.
- Motion is CSS-only and respects `prefers-reduced-motion`.
- Components are presentational and data-agnostic. Pages own API calls and domain state.

## Primitives

Use `src/design-system/primitives.jsx` as the canonical reusable surface. It provides RigCard, MetricCard, StatusBadge, AIAgentCard, TimelineCard, EmptyState, TelemetryChart, RigDrawer, RigModal, Toast, NotificationItem, CommandPalette, RigSearch, RigToolbar, SectionHeader, PageHeader and FloatingPanel.

The implementation takes the structural card/layout approach of Kokonut UI, restrained state treatments from Magic UI, and the utility interactions of ReactBits. Motion powers state entrances, hover/press feedback and live-status indicators; all work is reduced or removed under `prefers-reduced-motion`.
```

## frontend/src/design-system/RigOSV2Theme.js

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/RigOSV2Theme.js`

```javascript
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
```

## frontend/src/design-system/tokens.js

**Folder path:** `frontend/src/design-system`

**File path:** `frontend/src/design-system/tokens.js`

```javascript
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
```
