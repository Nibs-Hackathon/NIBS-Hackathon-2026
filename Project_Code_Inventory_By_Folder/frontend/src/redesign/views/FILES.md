# Folder: frontend/src/redesign/views Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/redesign/views`

Contains 13 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/redesign/views/AIInvestigationOS.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/AIInvestigationOS.jsx`

```javascript
import { useState } from 'react';
import { Box, Button, Chip, Paper, Stack, Typography } from '@mui/material';
import { ArticleOutlined, PlayArrowOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import {
  OperatorDecisionBar, EvidenceLineage, buildEvidenceFacts, normalizeTraceStages,
  TracePanel, DecisionHistory, ProvenanceBadge,
} from '../accountability';
import { MiniGraph, Status, round, label, safeReasoning, traceLabel } from './shared';

export function AIInvestigationOS({ stages, investigation, incident, telemetry, provenance = 'live' }) {
  const navigate = useNavigate(); const objectApi = useObjectContext();
  const fallback = ['Telemetry', 'Diagnostic', 'Knowledge', 'Prediction', 'Maintenance', 'Executive report']; const pipeline = fallback.map((name, index) => stages.find((stage) => traceLabel(stage.agent, index).toLowerCase().includes(name.toLowerCase().split(' ')[0])) || { agent: name, state: index === 0 ? 'streaming' : index === 1 ? 'running' : 'queued', confidence: Math.max(.48, .92 - index * .07) }); const [expanded, setExpanded] = useState(1); const [decision, setDecision] = useState(null); const selectStage = (index) => { setExpanded(expanded === index ? null : index); objectApi.setSelection({ agentStageId: pipeline[index]?.agent || `stage-${index}`, incidentId: incident?.id || objectApi.selection.incidentId }); }; const traceStages = normalizeTraceStages(pipeline, investigation); const evidenceFacts = buildEvidenceFacts({ incident, stages: pipeline, investigation }); const readings = Array.isArray(telemetry?.readings) ? telemetry.readings : []; const overall = round(Number(investigation?.confidence ?? pipeline[1]?.confidence ?? .76) <= 1 ? Number(investigation?.confidence ?? pipeline[1]?.confidence ?? .76) * 100 : Number(investigation?.confidence ?? pipeline[1]?.confidence ?? .76));
  return <Box className="ai-flagship"><Box className="ai-flagship-head"><Box><Typography className="product-kicker">RIGOS AI INVESTIGATION</Typography><Typography className="ai-flagship-title">Watching the operational model reason</Typography><Typography>Live investigation of {incident?.asset_name || incident?.asset_id || 'the active process signal'}  -  every conclusion is traceable to evidence.</Typography><Stack direction="row" spacing={1} sx={{ mt: 1 }}>{incident?.id ? <Chip clickable label={`Linked case ${String(incident.id).slice(0, 8)}`} onClick={() => navigateTo(objectApi, navigate, 'incidents', { incidentId: incident.id, assetId: incident.asset_id || null })} /> : null}{incident?.asset_id ? <Chip clickable label={incident.asset_name || incident.asset_id} onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: incident.asset_id })} /> : null}</Stack></Box><Box className="ai-flagship-live"><i />STREAMING EXECUTION<small>{overall}% model confidence</small><ProvenanceBadge value={provenance} /></Box></Box><Box className="ai-flagship-grid"><Paper className="ai-pipeline"><Box className="ai-panel-head"><Box><Typography className="product-kicker">AGENT PIPELINE</Typography><Typography>Execution graph</Typography></Box><Chip label={`${pipeline.filter((stage) => /running|streaming/i.test(stage.state)).length} agents live`} /></Box><Box className="ai-pipeline-list">{pipeline.map((stage, index) => { const state = String(stage.state || 'queued').toLowerCase(); const confidence = round(Number(stage.confidence ?? Math.max(.45, .9 - index * .07)) <= 1 ? Number(stage.confidence ?? Math.max(.45, .9 - index * .07)) * 100 : Number(stage.confidence)); return <motion.button layout={false} type="button" key={`${stage.agent}-${index}`} className={`ai-stage ${state} ${expanded === index ? 'expanded' : ''}`} onClick={() => selectStage(index)}><span className="ai-stage-index">{index + 1}</span><Box><Typography>{traceLabel(stage.agent, index)}</Typography><Typography>{state === 'queued' ? 'Awaiting upstream evidence' : state === 'running' || state === 'streaming' ? 'Evidence streaming' : 'Execution recorded'}</Typography><i><span style={{ width: `${state === 'queued' ? 16 : state === 'running' || state === 'streaming' ? 68 : 100}%` }} /></i></Box><Box className="ai-stage-state"><b>{confidence}%</b><small>{label(state)}</small></Box>{index < pipeline.length - 1 && <em />}{expanded === index && <motion.div className="ai-stage-expanded" initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} transition={{ duration: 0.12 }}><Typography>{safeReasoning(stage.reasoning || stage.output || stage.task || `${traceLabel(stage.agent, index)} is synthesizing telemetry, process context, and prior operational evidence.`)}</Typography><Box><span>Evidence {Array.isArray(stage.evidence) ? stage.evidence.length : 3}</span><span>Artifacts {Array.isArray(stage.documents) ? stage.documents.length : 2}</span><span>Duration {stage.duration_seconds ? `${Number(stage.duration_seconds).toFixed(1)}s` : 'live'}</span></Box></motion.div>}</motion.button>; })}</Box></Paper><Paper className="ai-reasoning"><Box className="ai-panel-head"><Box><Typography className="product-kicker">REASONING TREE</Typography><Typography>Hypotheses and evidence</Typography></Box><Button size="small">Expand all</Button></Box><Box className="reasoning-tree"><Box className="reasoning-root"><b>Observed deviation</b><Typography>{incident?.incident_type ? label(incident.incident_type) : 'Telemetry excursion under investigation'}</Typography></Box><Box className="reasoning-branches"><Box><span>01</span><Typography><b>Process condition</b>Deviation exceeds expected operating envelope.<small>Telemetry  -  confidence 89%</small></Typography></Box><Box><span>02</span><Typography><b>Equipment condition</b>Health trend is consistent with emerging degradation.<small>Diagnostic finding  -  confidence 78%</small></Typography></Box><Box><span>03</span><Typography><b>Procedural context</b>Retrieved operating procedure narrows acceptable response options.<small>Knowledge link  -  confidence 84%</small></Typography></Box></Box><Box className="evidence-graph"><Typography className="product-kicker">EVIDENCE GRAPH</Typography><svg viewBox="0 0 420 128"><path d="M58 64H172M248 64H360M210 28v72"/><circle cx="42" cy="64" r="18"/><circle cx="210" cy="26" r="18"/><circle cx="210" cy="101" r="18"/><circle cx="378" cy="64" r="20"/></svg><Box><span>Sensor window</span><span>Maintenance history</span><span>Operating procedure</span><strong>Root-cause model</strong></Box></Box></Box></Paper><Paper className="ai-evidence"><Box className="ai-panel-head"><Box><Typography className="product-kicker">LIVE EVIDENCE</Typography><Typography>Data and artifacts</Typography></Box><Button size="small" startIcon={<PlayArrowOutlined />}>Replay</Button></Box><Box className="ai-telemetry"><Typography className="product-kicker">TELEMETRY WINDOW</Typography><MiniGraph values={readings.map((reading) => reading.value)} area label={readings.length ? `${readings.length} samples  -  live historian feed` : 'Telemetry stream is attaching'} /></Box><Box className="ai-documents"><Typography className="product-kicker">RETRIEVED DOCUMENTS & KNOWLEDGE LINKS</Typography>{['Operating procedure  -  transient response', 'Equipment manual  -  inspection interval', 'Prior incident  -  evidence comparison'].map((doc, index) => <Typography key={doc}><ArticleOutlined /><span>{doc}<small>{index === 0 ? 'high relevance' : 'supporting evidence'}</small></span><b>{92 - index * 7}%</b></Typography>)}</Box><Box className="ai-artifacts"><Typography className="product-kicker">GENERATED ACTIONS</Typography><Typography><i />Containment recommendation prepared</Typography><Typography><i />Maintenance work order drafted</Typography><Typography><i />Executive brief assembling</Typography></Box></Paper></Box><Paper className="ai-bottom"><Box className="ai-confidence"><Typography className="product-kicker">CONFIDENCE EVOLUTION</Typography><Box>{[42, 53, 62, 74, overall].map((value, index) => <span key={index} style={{ height: `${value}%` }}><small>{value}%</small></span>)}</Box><Typography>Signal → diagnosis → knowledge → prediction → decision</Typography></Box><Box className="ai-execution"><Typography className="product-kicker">EXECUTION TIMELINE & LOGS</Typography><Typography><i />Telemetry ingest <b>completed  -  00:00:04</b></Typography><Typography><i />Diagnostic correlation <b>streaming  -  00:00:12</b></Typography><Typography><i />Knowledge retrieval <b>3 documents linked</b></Typography><Typography><i />Approval workflow <b>{decision || 'operator review pending'}</b></Typography></Box><Box className="ai-decisions"><Typography className="product-kicker">OPERATOR DECISION</Typography><Typography>Generated actions are advisory. Approval preserves the auditable execution record.</Typography>{decision && <Typography variant="caption">Local preview: {decision}</Typography>}</Box></Paper><Box className="e5-trace-wrap"><EvidenceLineage facts={evidenceFacts} /><TracePanel stages={traceStages} selectedId={expanded != null ? traceStages[expanded]?.id : objectApi.selection.agentStageId} onSelect={(stage) => { const idx = traceStages.findIndex((row) => row.id === stage.id); if (idx >= 0) selectStage(idx); }} /><DecisionHistory entries={objectApi.audit?.recentDecisions?.filter((entry) => !incident?.id || entry.incidentId === incident.id) || []} /><OperatorDecisionBar incident={incident} objectApi={objectApi} recommendation={investigation?.recommendation || incident?.ai_recommendation} /></Box></Box>;
}
```

## frontend/src/redesign/views/AssetBottomWorkspace.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/AssetBottomWorkspace.jsx`

```javascript
import { useMemo, useState } from 'react';
import { Box, Button, Paper, Typography } from '@mui/material';
import {
  AccountTreeOutlined, BuildOutlined, DeviceHubOutlined, HistoryOutlined,
  ScienceOutlined, TimelineOutlined, DescriptionOutlined,
} from '@mui/icons-material';
import { MiniGraph, label, round } from './shared';

/**
 * Part F + H — Bottom workspace tabs; controlled focus from twin interactions.
 */
export function AssetBottomWorkspace({
  asset,
  selected,
  stream,
  readings = [],
  statusLabel,
  primaryLabel,
  bottomHeight,
  onCycleHeight,
  onOpenIncident,
  clean,
  workOrders = [],
  activeTab,
  onTabChange,
  focusTag = null,
}) {
  const [internalTab, setInternalTab] = useState('telemetry');
  const tab = activeTab || internalTab;
  const setTab = (next) => {
    onTabChange?.(next);
    setInternalTab(next);
  };

  const incidentCount = selected?.incident ? 1 : 0;
  const hasForecast = asset?.remaining_life_days != null
    || asset?.remaining_life != null
    || asset?.health != null;
  const assetWOs = useMemo(
    () => workOrders.filter((wo) => wo.assetId === asset?.id || wo.asset_id === asset?.id || wo.asset === asset?.name),
    [workOrders, asset],
  );
  const hasMaint = assetWOs.length > 0;
  const deps = clean?.(asset?.dependencies, '') || asset?.dependencies;
  const tagLabel = focusTag || asset?.tag || asset?.id;

  const tabs = [
    { id: 'telemetry', label: 'Telemetry', icon: <TimelineOutlined fontSize="small" />, show: true },
    { id: 'history', label: 'History', icon: <HistoryOutlined fontSize="small" />, show: true },
    { id: 'incidents', label: `Incidents${incidentCount ? ` (${incidentCount})` : ''}`, icon: <DeviceHubOutlined fontSize="small" />, show: incidentCount > 0 },
    { id: 'forecast', label: 'Forecast', icon: <ScienceOutlined fontSize="small" />, show: hasForecast },
    { id: 'maintenance', label: 'Maintenance', icon: <BuildOutlined fontSize="small" />, show: hasMaint },
    { id: 'relationships', label: 'Relationships', icon: <AccountTreeOutlined fontSize="small" />, show: true },
    { id: 'documents', label: 'Documents', icon: <DescriptionOutlined fontSize="small" />, show: Number(asset?.documents_count) > 0 },
  ].filter((item) => item.show);

  const active = tabs.some((item) => item.id === tab) ? tab : 'telemetry';
  const health = round(asset?.health ?? 78);
  const rull = Number(asset?.remaining_life_days ?? asset?.remaining_life ?? Math.max(8, Math.round(health * 0.9)));
  const failure = Math.min(94, Math.max(6, 100 - health));

  return (
    <Paper className="twin-bottom assets-bottom">
      <Box className="twin-bottom-tabs">
        {tabs.map((item) => (
          <Button
            key={item.id}
            className={active === item.id ? 'active' : ''}
            startIcon={item.icon}
            onClick={() => setTab(item.id)}
          >
            {item.label}
          </Button>
        ))}
        <Button size="small" sx={{ ml: 'auto' }} onClick={onCycleHeight}>
          Height {bottomHeight}% · Ctrl+B
        </Button>
      </Box>

      <Box className="twin-bottom-body assets-bottom-body" key={`${asset?.id || 'none'}-${active}-${tagLabel || ''}`}>
        {active === 'telemetry' && (
          <>
            <Box>
              <Typography className="product-kicker">TELEMETRY</Typography>
              <Typography className="twin-bottom-title">
                {tagLabel ? `Tag ${tagLabel}` : 'Primary tags'}
                {' · '}
                {clean?.(stream?.sensor_type, 'Condition') || 'Condition'}
                {' · '}
                {clean?.(stream?.unit, 'stream') || 'stream'}
              </Typography>
              <MiniGraph
                values={readings.map((reading) => reading.value)}
                area
                label={readings.length ? `${readings.length} historian samples` : 'No dedicated stream for this asset yet'}
              />
            </Box>
            <Box className="twin-bottom-events">
              <Typography className="product-kicker">DECISION CONTEXT</Typography>
              <Typography><i className="event-dot risk" />Severity <b>{statusLabel}</b></Typography>
              <Typography><i className="event-dot active" />Next action <b>{primaryLabel}</b></Typography>
              <Typography><i className="event-dot" />Downstream <b>{clean?.(asset?.dependencies, 'Process train') || 'Process train'}</b></Typography>
            </Box>
          </>
        )}

        {active === 'history' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">STATE HISTORY</Typography>
            <Typography><i className="event-dot active" />Selection updated</Typography>
            <Typography><i className="event-dot" />Last inspection <b>{clean?.(asset?.last_inspection, 'Pending') || 'Pending'}</b></Typography>
            <Typography><i className="event-dot risk" />Condition band <b>{statusLabel}</b></Typography>
          </Box>
        )}

        {active === 'incidents' && selected?.incident && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">LINKED INCIDENT</Typography>
            <Typography className="twin-bottom-title">{label(selected.incident.incident_type || selected.incident.id)}</Typography>
            <Typography variant="body2" color="text.secondary">
              {selected.incident.evidence || selected.incident.reasoning || 'Evidence packet attached to this asset.'}
            </Typography>
            <Button size="small" sx={{ mt: 1 }} variant="contained" onClick={onOpenIncident}>Open case</Button>
          </Box>
        )}

        {active === 'forecast' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">FORWARD RISK</Typography>
            <Box className="assets-bottom-metrics">
              <Typography>Failure probability <b>{failure}%</b></Typography>
              <Typography>Remaining useful life <b>{rull} days</b></Typography>
              <Typography>Health trajectory <b>{health}%</b></Typography>
            </Box>
            <MiniGraph
              values={Array.from({ length: 12 }, (_, index) => Math.max(20, health - index * 2.2))}
              area
              label="Projected health curve"
            />
          </Box>
        )}

        {active === 'maintenance' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">WORK ORDERS</Typography>
            {assetWOs.length
              ? assetWOs.map((wo, index) => (
                <Typography key={wo.id || index}>
                  <i className="event-dot active" />
                  {wo.title || wo.name || `WO ${index + 1}`}
                  <b>{wo.status || wo.Status || 'Backlog'}</b>
                </Typography>
              ))
              : <Typography variant="body2" color="text.secondary">No open work orders for this asset.</Typography>}
          </Box>
        )}

        {active === 'relationships' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">PROCESS RELATIONSHIPS</Typography>
            <Typography><i className="event-dot" />Upstream <b>Feed / prior unit</b></Typography>
            <Typography><i className="event-dot active" />Selected <b>{asset?.name || '—'}</b></Typography>
            <Typography><i className="event-dot risk" />Downstream <b>{deps || 'Process train'}</b></Typography>
          </Box>
        )}

        {active === 'documents' && (
          <Box className="assets-bottom-panel">
            <Typography className="product-kicker">DOCUMENTS</Typography>
            <Typography>{clean?.(asset?.documents_count, '0') || '0'} controlled records linked to this asset.</Typography>
          </Box>
        )}
      </Box>
    </Paper>
  );
}
```

## frontend/src/redesign/views/AssetConsole.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/AssetConsole.jsx`

```javascript
import { useEffect, useMemo, useRef, useState } from 'react';
import {
  Box, Button, Checkbox, FormControlLabel, Typography,
} from '@mui/material';
import { ViewSidebarOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useWorkspace } from '../../context/WorkspaceContext';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { FilterChipBar } from '../../design-system/catalog/actions';
import { assetRisk } from './shared';
import { DigitalTwinCanvas } from './DigitalTwinCanvas';
import { AssetExplorer, BUILTIN_VIEWS, parseAssetPath } from './AssetExplorer';
import { AssetBottomWorkspace } from './AssetBottomWorkspace';
import { AssetObjectInspector } from './AssetObjectInspector';
import './assets-workspace.css';

/**
 * Assets workspace — Parts A–I: layout, twin, explorer, bottom, selection coupling.
 */
export function AssetConsole({
  assets = [],
  incidents = [],
  telemetry: globalTelemetry = null,
  telemetryStreams = [],
  maintenance = null,
  provenance = 'live',
}) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const inspectorActionRef = useRef(null);
  const selectionSourceRef = useRef('twin');
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('risk');
  const [riskBand, setRiskBand] = useState('critical');
  const [favoritesOnly, setFavoritesOnly] = useState(false);
  const [alarmsOnly, setAlarmsOnly] = useState(false);
  const [showFullTree, setShowFullTree] = useState(false);
  const [activeViewId, setActiveViewId] = useState('shift-critical');
  const [mobilePane, setMobilePane] = useState('twin');
  const [bottomTab, setBottomTab] = useState('telemetry');
  const [focusTag, setFocusTag] = useState(null);
  const { workspace, setWorkspaceValue } = useWorkspace();

  const layers = objectApi.ui?.twinLayers || {};
  const camera = objectApi.ui?.twinCamera || { zoom: 1, panX: 0, panY: 0 };
  const inspectorCollapsed = Boolean(objectApi.ui?.inspectorCollapsed);
  const bottomHeight = objectApi.ui?.bottomWorkspaceHeight ?? 28;
  const favorites = objectApi.favorites?.assetIds || [];
  const recentIds = objectApi.recent?.assetIds || [];
  const workOrders = Array.isArray(maintenance?.tasks) ? maintenance.tasks : [];

  const clean = (value, fallback = '—') => {
    const result = String(value ?? '').trim();
    return result && !/[\u00c3\u00c2]/.test(result) ? result : fallback;
  };

  const safeAssets = Array.isArray(assets) ? assets.filter((asset) => asset && typeof asset === 'object') : [];
  const safeIncidents = Array.isArray(incidents) ? incidents.filter((item) => item && typeof item === 'object') : [];
  const safeStreams = Array.isArray(telemetryStreams) ? telemetryStreams.filter((item) => item && typeof item === 'object') : [];

  const allRows = useMemo(() => safeAssets
    .map((asset, index) => ({
      asset: {
        ...asset,
        id: asset.id ?? `asset-${index}`,
        name: clean(asset.name || asset.asset_name, `Asset ${index + 1}`),
      },
      incident: safeIncidents.find((item) => item.asset_id === asset.id),
      telemetry: safeStreams.find((stream) => stream.asset_id === asset.id) || globalTelemetry,
    })), [safeAssets, safeIncidents, safeStreams, globalTelemetry]);

  const rows = useMemo(() => allRows
    .filter(({ asset }) => `${asset.name} ${asset.location || ''} ${asset.type || ''}`.toLowerCase().includes(query.toLowerCase()))
    .filter(({ asset, incident }) => {
      if (favoritesOnly && !favorites.includes(asset.id)) return false;
      if (alarmsOnly && !incident) return false;
      const risk = assetRisk(asset, incident);
      if (riskBand === 'critical') return risk > 70 || Boolean(incident);
      if (riskBand === 'watch') return risk > 40 && risk <= 70;
      if (riskBand === 'nominal') return risk <= 40 && !incident;
      return true;
    })
    .sort((a, b) => {
      if (sort === 'health') return Number(a.asset.health) - Number(b.asset.health);
      if (sort === 'name') return String(a.asset.name).localeCompare(String(b.asset.name));
      return assetRisk(b.asset, b.incident) - assetRisk(a.asset, a.incident);
    }), [allRows, query, sort, riskBand, favoritesOnly, alarmsOnly, favorites]);

  const treeRows = showFullTree
    ? allRows.filter(({ asset }) => `${asset.name} ${asset.location || ''} ${asset.type || ''}`.toLowerCase().includes(query.toLowerCase()))
    : rows;

  const criticalRows = useMemo(
    () => allRows.filter(({ asset, incident }) => assetRisk(asset, incident) > 70 || Boolean(incident)).slice(0, 8),
    [allRows],
  );

  const selectedId = objectApi.selection.assetId ?? workspace.assetSelection ?? null;
  const setSelectedId = (id, source = 'twin') => {
    selectionSourceRef.current = source;
    objectApi.setSelection({ assetId: id });
    objectApi.pushRecentAsset?.(id);
    setWorkspaceValue('assetSelection', id);
    const row = allRows.find((item) => item.asset.id === id);
    if (row) {
      const location = row.asset.location || row.asset.zone;
      const parts = String(location || '').split(/[›>\/|]/).map((part) => part.trim()).filter(Boolean);
      const unit = parts[1] || parts[0];
      if (unit) objectApi.setUnit?.(unit);
    }
  };
  const selected = allRows.find((row) => row.asset.id === selectedId) || rows[0] || allRows[0];
  const asset = selected?.asset;
  const risk = selected ? assetRisk(asset, selected.incident) : 0;
  const stream = selected?.telemetry && typeof selected.telemetry === 'object' ? selected.telemetry : null;
  const readings = Array.isArray(stream?.readings) ? stream.readings : [];
  const signalValues = readings.map((reading) => Number(reading.value)).filter(Number.isFinite);

  useEffect(() => {
    if (!asset?.id || inspectorCollapsed) return undefined;
    if (selectionSourceRef.current === 'explorer') return undefined;
    const timer = requestAnimationFrame(() => inspectorActionRef.current?.focus?.({ preventScroll: true }));
    return () => cancelAnimationFrame(timer);
  }, [asset?.id, inspectorCollapsed]);

  useEffect(() => {
    setFocusTag(asset?.tag || asset?.id || null);
    if (bottomTab === 'incidents' && !selected?.incident) setBottomTab('telemetry');
  }, [asset?.id]);

  useEffect(() => {
    const onKey = (event) => {
      const target = event.target;
      const typing = target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable);
      if (typing) return;
      if (event.key === ']' && !event.metaKey && !event.ctrlKey && !event.altKey) {
        event.preventDefault();
        objectApi.patchUi?.({ inspectorCollapsed: !objectApi.ui?.inspectorCollapsed });
      }
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'b') {
        event.preventDefault();
        objectApi.cycleBottomHeight?.();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [objectApi]);

  const activateView = (viewId) => {
    const view = BUILTIN_VIEWS.find((item) => item.id === viewId) || BUILTIN_VIEWS[0];
    setActiveViewId(view.id);
    setRiskBand(view.riskBand || 'all');
    setFavoritesOnly(Boolean(view.favoritesOnly));
    setAlarmsOnly(Boolean(view.alarmsOnly));
    setShowFullTree(Boolean(view.showAll));
    setSort(view.sort || 'risk');
    objectApi.patchUi?.({ activeSavedViewId: view.id });
  };

  const createWorkOrderFor = (row) => {
    const target = row?.asset || asset;
    if (!target) return;
    objectApi.pushAuditDecision?.({
      id: `wo-${Date.now()}`,
      decision: 'create_work_order',
      what: `Create work order — ${target.name}`,
      who: 'Control operator',
      operator: 'Control operator',
      at: new Date().toISOString(),
      objectLabel: target.name,
      assetId: target.id,
    });
    navigateTo(objectApi, navigate, 'maintenance', {
      assetId: target.id,
      draftWorkOrder: {
        id: `draft-${target.id}`,
        title: `Inspect ${target.name}`,
        asset: target.name,
        assetName: target.name,
        assetId: target.id,
        cost: 18500,
        downtime: '8h',
        status: 'Backlog',
        priority: 'P1',
      },
    });
  };

  const acknowledgeWatch = () => {
    if (!asset) return;
    objectApi.pushAuditDecision?.({
      id: `ack-${Date.now()}`,
      decision: 'acknowledge_watch',
      what: `Acknowledge watch — ${asset.name}`,
      who: 'Control operator',
      operator: 'Control operator',
      at: new Date().toISOString(),
      objectLabel: asset.name,
      assetId: asset.id,
    });
    toast.success(`Watch acknowledged for ${asset.name}`);
  };

  const primaryAction = () => {
    if (!asset) return;
    if (selected?.incident) {
      navigateTo(objectApi, navigate, 'investigation', {
        incidentId: selected.incident.id,
        assetId: asset.id,
        focusDecisionBar: true,
      });
      return;
    }
    if (risk > 70) {
      createWorkOrderFor(selected);
      return;
    }
    if (risk > 40) {
      acknowledgeWatch();
      return;
    }
    navigateTo(objectApi, navigate, 'forecasting', { assetId: asset.id });
  };

  const primaryLabel = selected?.incident
    ? 'Open incident'
    : risk > 70
      ? 'Create work order'
      : risk > 40
        ? 'Acknowledge watch'
        : 'View forecast';

  const statusLabel = risk > 70 ? 'Critical' : risk > 40 ? 'Attention' : 'Nominal';
  const assetNote = objectApi.notes?.byAssetId?.[asset?.id] || '';

  const twinRows = useMemo(() => {
    const pool = rows.length ? rows : allRows;
    if (!asset) return pool.slice(0, 48);
    const path = parseAssetPath(asset, clean);
    const unitScoped = pool.filter((row) => {
      const rowPath = parseAssetPath(row.asset, clean);
      return rowPath.unit === path.unit && rowPath.area === path.area;
    });
    const scoped = unitScoped.length ? unitScoped : pool;
    return scoped.slice(0, 48);
  }, [rows, allRows, asset, clean]);

  const filterChips = [
    { id: 'all', label: 'All', active: riskBand === 'all' && !favoritesOnly && !alarmsOnly },
    { id: 'critical', label: `Critical (${criticalRows.length})`, active: riskBand === 'critical' },
    { id: 'watch', label: 'Watch', active: riskBand === 'watch' },
    { id: 'nominal', label: 'Nominal', active: riskBand === 'nominal' },
  ].map((chip) => ({
    ...chip,
    onRemove: () => {
      setFavoritesOnly(false);
      setAlarmsOnly(false);
      if (chip.id === 'all') setRiskBand('all');
      else setRiskBand((current) => (current === chip.id ? 'all' : chip.id));
      setActiveViewId(chip.id === 'critical' ? 'shift-critical' : 'all-facility');
    },
  }));

  const layerToggle = (key) => (event) => {
    objectApi.setTwinLayers?.({ [key]: event.target.checked });
  };

  if (!safeAssets.length) {
    return (
      <Box className="assets-os twin-empty" role="status">
        <Typography fontWeight={800}>No facility assets in scope</Typography>
        <Typography variant="body2">Switch facility scope or wait for the asset register to populate.</Typography>
      </Box>
    );
  }

  return (
    <Box
      className={`assets-os twin-workspace ${inspectorCollapsed ? 'inspector-collapsed' : ''}`}
      style={{ '--assets-bottom-h': `${bottomHeight}vh` }}
    >
      <Box className="assets-toolbar" role="toolbar" aria-label="Asset workspace">
        <FilterChipBar chips={filterChips} />
        <Box className="assets-layer-toggles" role="group" aria-label="Twin layers">
          <FormControlLabel control={<Checkbox size="small" checked={layers.process !== false} onChange={layerToggle('process')} />} label="Process" />
          <FormControlLabel control={<Checkbox size="small" checked={Boolean(layers.risk)} onChange={layerToggle('risk')} />} label="Risk" />
          <FormControlLabel control={<Checkbox size="small" checked={Boolean(layers.alarms)} onChange={layerToggle('alarms')} />} label="Alarms" />
          <FormControlLabel control={<Checkbox size="small" checked={layers.sensors !== false} onChange={layerToggle('sensors')} />} label="Sensors" />
          <FormControlLabel control={<Checkbox size="small" checked={Boolean(layers.maintenance)} onChange={layerToggle('maintenance')} />} label="Maint" />
        </Box>
        <Box sx={{ flex: 1 }} />
        <Button
          size="small"
          startIcon={<ViewSidebarOutlined />}
          onClick={() => objectApi.patchUi?.({ inspectorCollapsed: !inspectorCollapsed })}
        >
          {inspectorCollapsed ? 'Show inspector' : 'Hide inspector'}
          <Typography component="kbd" variant="caption" sx={{ ml: 0.75, opacity: 0.55 }}>]</Typography>
        </Button>
        <Button size="small" variant="outlined" disabled={!asset} onClick={() => createWorkOrderFor(selected)}>Create work order</Button>
      </Box>

      <Box className="assets-mobile-tabs" role="tablist">
        {['explorer', 'twin', 'inspector'].map((pane) => (
          <Button key={pane} className={mobilePane === pane ? 'active' : ''} onClick={() => setMobilePane(pane)}>{pane}</Button>
        ))}
      </Box>

      <Box className={`assets-body twin-workspace-grid mobile-${mobilePane}`}>
        <AssetExplorer
          rows={treeRows}
          allRows={allRows}
          selectedId={asset?.id}
          onSelect={setSelectedId}
          query={query}
          onQueryChange={setQuery}
          activeViewId={activeViewId}
          onActivateView={activateView}
          favorites={favorites}
          recentIds={recentIds}
          showFullTree={showFullTree}
          onToggleFullTree={() => setShowFullTree((value) => !value)}
          clean={clean}
        />

        <DigitalTwinCanvas
          rows={twinRows}
          selectedId={asset?.id}
          onSelect={setSelectedId}
          layers={layers}
          camera={camera}
          onCameraChange={(patch) => objectApi.setTwinCamera?.(patch)}
          onFitUnit={() => objectApi.setTwinCamera?.({ zoom: 1, panX: 0, panY: 0, fitMode: 'unit' })}
          onFitSelection={() => objectApi.setTwinCamera?.({ fitMode: 'selection', zoom: Math.max(camera.zoom || 1, 1.15) })}
          onOpenIncident={(row) => navigateTo(objectApi, navigate, 'incidents', { incidentId: row.incident.id, assetId: row.asset.id })}
          onViewForecast={(row) => navigateTo(objectApi, navigate, 'forecasting', { assetId: row.asset.id })}
          onCreateWorkOrder={createWorkOrderFor}
          onToggleFavorite={(id) => objectApi.toggleFavoriteAsset?.(id)}
          onCopyTag={(row) => {
            const tag = row.asset.tag || row.asset.id;
            navigator.clipboard?.writeText?.(String(tag));
            toast.success(`Copied ${tag}`);
          }}
          onTagClick={(row) => {
            setSelectedId(row.asset.id, 'twin');
            setFocusTag(row.asset.tag || row.asset.id);
            setBottomTab('telemetry');
            if (bottomHeight === 0) objectApi.patchUi?.({ bottomWorkspaceHeight: 28 });
          }}
          onAlarmClick={(row, event) => {
            setSelectedId(row.asset.id, 'twin');
            setBottomTab('incidents');
            if (bottomHeight === 0) objectApi.patchUi?.({ bottomWorkspaceHeight: 28 });
            if ((event?.metaKey || event?.ctrlKey) && row.incident) {
              navigateTo(objectApi, navigate, 'incidents', { incidentId: row.incident.id, assetId: row.asset.id });
            }
          }}
          isFavorite={(id) => favorites.includes(id)}
          clean={clean}
        />

        {!inspectorCollapsed && (
          <AssetObjectInspector
            asset={asset}
            selected={selected}
            risk={risk}
            statusLabel={statusLabel}
            signalValues={signalValues}
            provenance={provenance}
            primaryLabel={primaryLabel}
            primaryAction={primaryAction}
            actionRef={inspectorActionRef}
            clean={clean}
            workOrders={workOrders}
            note={assetNote}
            onNoteChange={(text) => objectApi.setAssetNote?.(asset.id, text)}
            onOpenIncident={() => selected?.incident && navigateTo(objectApi, navigate, 'incidents', {
              incidentId: selected.incident.id,
              assetId: asset.id,
            })}
            onOpenForecast={() => navigateTo(objectApi, navigate, 'forecasting', { assetId: asset.id })}
            onCreateWorkOrder={() => createWorkOrderFor(selected)}
            onOpenInvestigation={() => selected?.incident && navigateTo(objectApi, navigate, 'investigation', {
              incidentId: selected.incident.id,
              assetId: asset.id,
              focusDecisionBar: true,
            })}
          />
        )}
      </Box>

      {bottomHeight > 0 && (
        <AssetBottomWorkspace
          asset={asset}
          selected={selected}
          stream={stream}
          readings={readings}
          statusLabel={statusLabel}
          primaryLabel={primaryLabel}
          bottomHeight={bottomHeight}
          onCycleHeight={() => objectApi.cycleBottomHeight?.()}
          onOpenIncident={() => selected?.incident && navigateTo(objectApi, navigate, 'incidents', { incidentId: selected.incident.id, assetId: asset?.id })}
          clean={clean}
          workOrders={workOrders}
          activeTab={bottomTab}
          onTabChange={setBottomTab}
          focusTag={focusTag}
        />
      )}
    </Box>
  );
}
```

## frontend/src/redesign/views/AssetExplorer.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/AssetExplorer.jsx`

```javascript
import { useEffect, useMemo, useRef, useState } from 'react';
import { Box, Button, MenuItem, Paper, TextField, Typography } from '@mui/material';
import { SearchOutlined, UnfoldMoreOutlined } from '@mui/icons-material';
import { assetRisk, label, round } from './shared';

const BUILTIN_VIEWS = [
  { id: 'shift-critical', label: 'Shift Critical', riskBand: 'critical', favoritesOnly: false, alarmsOnly: false, sort: 'risk' },
  { id: 'my-pins', label: 'My Pins', riskBand: 'all', favoritesOnly: true, alarmsOnly: false, sort: 'name' },
  { id: 'open-alarms', label: 'Open Alarms', riskBand: 'all', favoritesOnly: false, alarmsOnly: true, sort: 'risk' },
  { id: 'all-facility', label: 'Show all', riskBand: 'all', favoritesOnly: false, alarmsOnly: false, showAll: true, sort: 'name' },
];

const ROW_H = 36;
const OVERSCAN = 10;

export function parseAssetPath(asset, clean) {
  const cleaner = clean || ((value, fallback = '—') => String(value ?? '').trim() || fallback);
  const location = cleaner(asset.location || asset.zone, 'Facility network');
  const parts = String(location).split(/[›>\/|]/).map((part) => part.trim()).filter(Boolean);
  const area = parts[0] || location;
  const unit = parts[1] || parts[0] || 'Unit';
  const system = cleaner(label(asset.type || 'Process system'), 'Process system');
  return { facility: 'Facility', area, unit, system };
}

function useVirtualWindow(count, rowHeight = ROW_H) {
  const ref = useRef(null);
  const [range, setRange] = useState({ start: 0, end: Math.min(count, 40) });

  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    const update = () => {
      const start = Math.max(0, Math.floor(el.scrollTop / rowHeight) - OVERSCAN);
      const visible = Math.ceil(el.clientHeight / rowHeight) + OVERSCAN * 2;
      setRange({ start, end: Math.min(count, start + visible) });
    };
    update();
    el.addEventListener('scroll', update, { passive: true });
    const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(update) : null;
    ro?.observe(el);
    return () => {
      el.removeEventListener('scroll', update);
      ro?.disconnect();
    };
  }, [count, rowHeight]);

  return {
    ref,
    start: range.start,
    end: range.end,
    totalHeight: count * rowHeight,
    offsetY: range.start * rowHeight,
  };
}

/**
 * Part G + QA§3 — Queues first; lazy unit tree; windowed hierarchy rows.
 */
export function AssetExplorer({
  rows = [],
  allRows = rows,
  selectedId,
  onSelect,
  query,
  onQueryChange,
  favorites = [],
  recentIds = [],
  activeViewId,
  onActivateView,
  showFullTree,
  onToggleFullTree,
  clean,
}) {
  const [expanded, setExpanded] = useState({});

  const criticalRows = useMemo(
    () => allRows.filter(({ asset, incident }) => assetRisk(asset, incident) > 70 || Boolean(incident)).slice(0, 10),
    [allRows],
  );
  const incidentRows = useMemo(
    () => allRows.filter(({ incident }) => Boolean(incident)).slice(0, 10),
    [allRows],
  );
  const favoriteRows = useMemo(
    () => allRows.filter(({ asset }) => favorites.includes(asset.id)),
    [allRows, favorites],
  );
  const recentRows = useMemo(() => {
    const byId = new Map(allRows.map((row) => [row.asset.id, row]));
    return recentIds.map((id) => byId.get(id)).filter(Boolean).slice(0, 10);
  }, [allRows, recentIds]);

  const hierarchy = useMemo(() => {
    const root = {};
    rows.forEach((row) => {
      const path = parseAssetPath(row.asset, clean);
      const areaNode = (root[path.area] ||= {});
      const unitNode = (areaNode[path.unit] ||= {});
      const systemNode = (unitNode[path.system] ||= []);
      systemNode.push(row);
    });
    return root;
  }, [rows, clean]);

  const selectedPath = useMemo(() => {
    const row = allRows.find((item) => item.asset.id === selectedId);
    return row ? parseAssetPath(row.asset, clean) : null;
  }, [allRows, selectedId, clean]);

  useEffect(() => {
    if (!selectedPath) return;
    const areaKey = `area:${selectedPath.area}`;
    const unitKey = `${areaKey}/unit:${selectedPath.unit}`;
    const systemKey = `${unitKey}/sys:${selectedPath.system}`;
    setExpanded((current) => ({
      ...current,
      [areaKey]: true,
      [unitKey]: true,
      [systemKey]: true,
    }));
  }, [selectedPath]);

  const isExpanded = (key) => {
    if (showFullTree && expanded[key] === undefined) return true;
    return Boolean(expanded[key]);
  };

  const toggleExpand = (key) => {
    setExpanded((current) => ({ ...current, [key]: !isExpanded(key) }));
  };

  const selectFromExplorer = (id) => onSelect?.(id, 'explorer');

  const flatRows = useMemo(() => {
    const list = [];
    Object.entries(hierarchy).forEach(([area, units]) => {
      const areaKey = `area:${area}`;
      const areaCount = Object.values(units).reduce(
        (sum, systems) => sum + Object.values(systems).reduce((n, members) => n + members.length, 0),
        0,
      );
      list.push({
        kind: 'area',
        key: areaKey,
        label: area,
        count: areaCount,
        onPath: selectedPath?.area === area,
      });
      if (!isExpanded(areaKey)) return;
      Object.entries(units).forEach(([unit, systems]) => {
        const unitKey = `${areaKey}/unit:${unit}`;
        const unitCount = Object.values(systems).reduce((n, members) => n + members.length, 0);
        list.push({
          kind: 'unit',
          key: unitKey,
          label: unit,
          count: unitCount,
          onPath: selectedPath?.area === area && selectedPath?.unit === unit,
        });
        if (!isExpanded(unitKey)) return;
        Object.entries(systems).forEach(([system, members]) => {
          const systemKey = `${unitKey}/sys:${system}`;
          list.push({
            kind: 'system',
            key: systemKey,
            label: system,
            count: members.length,
            onPath: selectedPath?.area === area && selectedPath?.unit === unit && selectedPath?.system === system,
          });
          if (!isExpanded(systemKey)) return;
          members.forEach((row) => {
            list.push({
              kind: 'asset',
              key: `asset:${row.asset.id}`,
              row,
              onPath: selectedId === row.asset.id,
            });
          });
        });
      });
    });
    return list;
  // expanded + showFullTree intentionally included
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hierarchy, expanded, showFullTree, selectedPath, selectedId]);

  const virt = useVirtualWindow(flatRows.length, ROW_H);
  const windowed = flatRows.slice(virt.start, virt.end);

  const onSearchKey = (event) => {
    if (event.key !== 'Enter' || !rows.length) return;
    selectFromExplorer(rows[0].asset.id);
  };

  const renderQueue = (title, items) => {
    if (!items.length) return null;
    return (
      <Box className="assets-critical-queue">
        <Typography className="product-kicker">{title}</Typography>
        {items.map((row) => {
          const rowRisk = assetRisk(row.asset, row.incident);
          return (
            <button
              type="button"
              key={`${title}-${row.asset.id}`}
              className={`asset-tree-item ${selectedId === row.asset.id ? 'selected' : ''}`}
              onClick={() => selectFromExplorer(row.asset.id)}
            >
              <span className={`asset-tree-dot ${rowRisk > 70 ? 'critical' : rowRisk > 40 ? 'watch' : ''}`} />
              <span>
                <b>{row.asset.name}</b>
                <small>
                  {row.incident
                    ? label(row.incident.incident_type || 'Open incident')
                    : `${round(row.asset.health)}% · risk ${rowRisk}`}
                </small>
              </span>
              {row.incident ? <em className="assets-incident-pip">!</em> : <em>{rowRisk}</em>}
            </button>
          );
        })}
      </Box>
    );
  };

  const assetIds = useMemo(
    () => flatRows.filter((item) => item.kind === 'asset').map((item) => item.row.asset.id),
    [flatRows],
  );

  return (
    <Paper className="asset-explorer assets-pane">
      <Box className="asset-explorer-top">
        <Typography className="product-kicker">EXPLORER</Typography>
        <Typography variant="caption">{rows.length} in view · windowed</Typography>
      </Box>

      <TextField
        value={query}
        onChange={(event) => onQueryChange?.(event.target.value)}
        onKeyDown={onSearchKey}
        size="small"
        placeholder="Search tag, name, area"
        slotProps={{ input: { startAdornment: <SearchOutlined fontSize="small" /> } }}
      />

      <Box className="assets-saved-views">
        <TextField
          select
          size="small"
          fullWidth
          label="Saved view"
          value={activeViewId || 'shift-critical'}
          onChange={(event) => onActivateView?.(event.target.value)}
        >
          {BUILTIN_VIEWS.map((view) => (
            <MenuItem key={view.id} value={view.id}>{view.label}</MenuItem>
          ))}
        </TextField>
      </Box>

      {renderQueue('CRITICAL NOW', criticalRows)}
      {renderQueue('OPEN INCIDENTS', incidentRows)}
      {renderQueue('FAVORITES', favoriteRows)}
      {renderQueue('RECENT', recentRows)}

      <Box className="assets-tree-head">
        <Typography className="product-kicker">FACILITY HIERARCHY</Typography>
        <Button size="small" startIcon={<UnfoldMoreOutlined />} onClick={onToggleFullTree}>
          {showFullTree ? 'Queues focus' : 'Show all'}
        </Button>
      </Box>

      {!showFullTree && (
        <Typography variant="caption" className="assets-lazy-hint" color="text.secondary">
          Expand Area → Unit to load equipment (lazy). Show all mounts the full filtered tree windowed.
        </Typography>
      )}

      <Box
        className={`asset-tree assets-tree-virtual ${selectedId ? 'has-selection' : ''}`}
        ref={virt.ref}
        tabIndex={0}
        onKeyDown={(event) => {
          if (!assetIds.length) return;
          const idx = Math.max(0, assetIds.indexOf(selectedId));
          if (event.key === 'ArrowDown') {
            event.preventDefault();
            selectFromExplorer(assetIds[Math.min(assetIds.length - 1, idx + 1)]);
          }
          if (event.key === 'ArrowUp') {
            event.preventDefault();
            selectFromExplorer(assetIds[Math.max(0, idx - 1)]);
          }
          if (event.key === 'Enter' && assetIds[idx]) selectFromExplorer(assetIds[idx]);
        }}
      >
        {!flatRows.length && (
          <Typography variant="body2" color="text.secondary" sx={{ p: 1.5 }}>
            No assets match this view. Switch saved view or clear search.
          </Typography>
        )}

        <div className="assets-tree-spacer" style={{ height: virt.totalHeight }}>
          <div className="assets-tree-window" style={{ transform: `translateY(${virt.offsetY}px)` }}>
            {windowed.map((item) => {
              if (item.kind !== 'asset') {
                return (
                  <button
                    type="button"
                    key={item.key}
                    className={`asset-tree-parent assets-tree-toggle assets-virt-row is-${item.kind} ${selectedId && !item.onPath ? 'is-dimmed' : ''}`}
                    style={{ height: ROW_H }}
                    onClick={() => toggleExpand(item.key)}
                  >
                    <span>{isExpanded(item.key) ? '▾' : '▸'}</span>
                    {item.label}
                    <b>{item.count}</b>
                  </button>
                );
              }
              const row = item.row;
              const rowRisk = assetRisk(row.asset, row.incident);
              const isSelected = selectedId === row.asset.id;
              return (
                <button
                  type="button"
                  key={item.key}
                  className={`asset-tree-item assets-virt-row ${isSelected ? 'selected' : ''} ${selectedId && !isSelected ? 'is-dimmed' : ''}`}
                  style={{ height: ROW_H }}
                  onClick={() => selectFromExplorer(row.asset.id)}
                >
                  <span className={`asset-tree-dot ${rowRisk > 70 ? 'critical' : rowRisk > 40 ? 'watch' : ''}`} />
                  <span>
                    <b>{row.asset.name}</b>
                    <small>{round(row.asset.health)}% health</small>
                  </span>
                  <em>{rowRisk}</em>
                </button>
              );
            })}
          </div>
        </div>
      </Box>
    </Paper>
  );
}

export { BUILTIN_VIEWS };
```

## frontend/src/redesign/views/AssetObjectInspector.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/AssetObjectInspector.jsx`

```javascript
import { useState } from 'react';
import { Box, Button, Chip, Paper, Stack, TextField, Typography } from '@mui/material';
import { ExpandMoreOutlined } from '@mui/icons-material';
import { ProvenanceBadge } from '../accountability';
import { StatusBadge, RiskBadge } from '../../design-system/catalog/status';
import { HealthRing, SignalCard, Sparkline } from '../../design-system/catalog/data';
import { Health, label, round } from './shared';

function AccordionSection({ id, title, open, onToggle, children, count }) {
  return (
    <Box className={`assets-accordion ${open ? 'is-open' : ''}`}>
      <button type="button" className="assets-accordion-head" onClick={() => onToggle(id)} aria-expanded={open}>
        <ExpandMoreOutlined className="assets-accordion-chevron" fontSize="small" />
        <Typography className="product-kicker">{title}</Typography>
        {count != null && <em>{count}</em>}
      </button>
      {open && <Box className="assets-accordion-body">{children}</Box>}
    </Box>
  );
}

/**
 * Part E — Object Inspector: Identity/Health/Signals open; sections 4–10 accordion; sticky CTA.
 */
export function AssetObjectInspector({
  asset,
  selected,
  risk,
  statusLabel,
  signalValues = [],
  provenance = 'live',
  primaryLabel,
  primaryAction,
  actionRef,
  clean,
  workOrders = [],
  note = '',
  onNoteChange,
  onOpenIncident,
  onOpenForecast,
  onCreateWorkOrder,
  onOpenInvestigation,
}) {
  const [openSections, setOpenSections] = useState(() => new Set());

  const toggle = (id) => {
    setOpenSections((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  if (!asset) {
    return (
      <Paper className="twin-inspector assets-pane assets-inspector">
        <Typography variant="body2" color="text.secondary" sx={{ p: 2 }}>
          Select a critical asset or click a unit.
        </Typography>
      </Paper>
    );
  }

  const health = round(asset.health ?? 0);
  const rull = Number(asset.remaining_life_days ?? asset.remaining_life ?? Math.max(8, Math.round(health * 0.9)));
  const failure = Math.min(94, Math.max(6, 100 - health));
  const assetWOs = workOrders.filter(
    (wo) => wo.assetId === asset.id || wo.asset_id === asset.id || wo.asset === asset.name,
  );
  const docs = Number(asset.documents_count) || 0;
  const aiText = selected?.incident?.reasoning
    || asset.ai_recommendation
    || (risk > 70
      ? 'Condition trend supports containment planning — verify linked evidence before authorizing work.'
      : 'No elevated agent recommendation for this object.');
  const confidence = selected?.incident?.confidence != null
    ? Math.round(Number(selected.incident.confidence) <= 1
      ? Number(selected.incident.confidence) * 100
      : Number(selected.incident.confidence))
    : risk > 70 ? 78 : 54;

  return (
    <Paper className="twin-inspector p8-inspector-swap assets-pane assets-inspector" key={asset.id}>
      <Box className="twin-inspector-head assets-inspector-sticky">
        <Stack direction="row" spacing={1} alignItems="center">
          <Typography className="product-kicker">OBJECT</Typography>
          <ProvenanceBadge value={provenance} />
        </Stack>
      </Box>

      <Box className="assets-inspector-scroll">
        <Box className="p8-inspector-section assets-inspector-identity">
          <Typography className="product-kicker">IDENTITY</Typography>
          <Typography className="twin-inspector-title">{asset.name}</Typography>
          <Typography variant="caption">
            Tag {clean(asset.tag || asset.id)} · {clean(asset.location || asset.zone, 'Facility')} · {clean(label(asset.type || 'Process asset'), 'Asset')}
          </Typography>
        </Box>

        <Box className="p8-inspector-section p8-inspector-state">
          <Typography className="product-kicker">CURRENT HEALTH</Typography>
          <StatusBadge label={statusLabel} status={statusLabel} live={risk > 40} />
          <RiskBadge value={risk} />
          <HealthRing value={asset.health} size={72} />
          <Box>
            <Typography>Health</Typography>
            <b>{health}%</b>
            <Health value={asset.health} />
            <Typography variant="caption" display="block" sx={{ mt: 0.5 }}>
              Last inspection {clean(asset.last_inspection, 'Pending')}
            </Typography>
          </Box>
        </Box>

        <Box className="p8-inspector-section">
          <Typography className="product-kicker">SIGNALS</Typography>
          <Sparkline values={signalValues.length ? signalValues : [Number(asset.health) || 0]} label="Condition trend" height={36} />
          <Box className="p8-inspector-signals" sx={{ mt: 1 }}>
            <SignalCard name="Temperature" value={clean(asset.temperature)} unit="°C" threshold={120} provenance={provenance} />
            <SignalCard name="Pressure" value={clean(asset.pressure)} unit="psi" threshold={200} provenance={provenance} />
            <SignalCard name="Vibration" value={clean(asset.vibration)} unit="mm/s" threshold={12} provenance={provenance} />
          </Box>
        </Box>

        <AccordionSection id="linked" title="LINKED INCIDENTS" open={openSections.has('linked')} onToggle={toggle} count={selected?.incident ? 1 : 0}>
          {selected?.incident ? (
            <Chip
              clickable
              color="warning"
              size="small"
              label={`${label(selected.incident.incident_type || selected.incident.id)}`}
              onClick={onOpenIncident}
            />
          ) : (
            <Typography variant="body2" color="text.secondary">No open cases for this asset.</Typography>
          )}
        </AccordionSection>

        <AccordionSection id="forecast" title="FORECAST" open={openSections.has('forecast')} onToggle={toggle}>
          <Typography variant="body2">Failure probability <b>{failure}%</b></Typography>
          <Typography variant="body2">Remaining useful life <b>{rull} days</b></Typography>
          <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onOpenForecast}>Open forecast terminal</Button>
        </AccordionSection>

        <AccordionSection id="maintenance" title="MAINTENANCE" open={openSections.has('maintenance')} onToggle={toggle} count={assetWOs.length}>
          {assetWOs.length
            ? assetWOs.map((wo, index) => (
              <Typography key={wo.id || index} variant="body2">
                {wo.title || wo.name || `WO ${index + 1}`} · {wo.status || 'Backlog'}
              </Typography>
            ))
            : <Typography variant="body2" color="text.secondary">No open work orders.</Typography>}
          <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onCreateWorkOrder}>Create work order</Button>
        </AccordionSection>

        <AccordionSection id="knowledge" title="KNOWLEDGE" open={openSections.has('knowledge')} onToggle={toggle}>
          <Typography variant="body2" color="text.secondary">
            Similar past events and procedures load when retrieval is available for this tag class.
          </Typography>
        </AccordionSection>

        <AccordionSection id="documents" title="DOCUMENTS" open={openSections.has('documents')} onToggle={toggle} count={docs}>
          <Typography variant="body2">
            {docs > 0 ? `${docs} controlled records linked.` : 'No controlled documents linked yet.'}
          </Typography>
        </AccordionSection>

        <AccordionSection id="notes" title="OPERATOR NOTES" open={openSections.has('notes')} onToggle={toggle}>
          <TextField
            multiline
            minRows={3}
            fullWidth
            size="small"
            placeholder="Shift notes for this asset (session persisted)"
            value={note}
            onChange={(event) => onNoteChange?.(event.target.value)}
          />
        </AccordionSection>

        <AccordionSection id="ai" title="AI RECOMMENDATIONS" open={openSections.has('ai')} onToggle={toggle}>
          <Typography variant="body2">{aiText}</Typography>
          <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 0.75 }}>
            Confidence {confidence}% · lineage via investigation trace
          </Typography>
          {selected?.incident && (
            <Button size="small" sx={{ mt: 1, textTransform: 'none' }} onClick={onOpenInvestigation}>
              Open investigation
            </Button>
          )}
        </AccordionSection>
      </Box>

      <Box className="assets-inspector-cta">
        <Button
          ref={actionRef}
          size="small"
          variant="contained"
          fullWidth
          onClick={primaryAction}
          sx={{ textTransform: 'none', fontWeight: 700 }}
        >
          {primaryLabel}
        </Button>
      </Box>
    </Paper>
  );
}
```

## frontend/src/redesign/views/assets-workspace.css

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/assets-workspace.css`

```css
/* Assets workspace — Part C layout geometry + Part D twin chrome */

.assets-os.twin-workspace,
.assets-os {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
  height: calc(100vh - 112px);
  max-height: calc(100vh - 112px);
  overflow: hidden;
}

.assets-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  min-height: 40px;
  max-height: 72px;
  padding: 2px 0;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 5;
  background: #090b0f;
}

.assets-layer-toggles {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 0 4px;
  align-items: center;
}

.assets-layer-toggles .MuiFormControlLabel-root {
  margin: 0 2px;
}

.assets-layer-toggles .MuiFormControlLabel-label {
  font-size: 0.68rem;
  color: #94a3b8;
}

.assets-mobile-tabs {
  display: none;
  gap: 4px;
}

.assets-body.twin-workspace-grid {
  flex: 1 1 auto;
  min-height: 0;
  align-items: stretch;
  display: grid !important;
  grid-template-columns: minmax(220px, 260px) minmax(0, 1fr) 320px;
  gap: 10px;
}

.assets-os.inspector-collapsed .assets-body.twin-workspace-grid {
  grid-template-columns: minmax(220px, 260px) minmax(0, 1fr);
}

/* Twin is the only pane that grows — ≥55% of body */
.assets-body > .assets-twin,
.assets-body > .twin-canvas.assets-twin {
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.assets-pane.asset-explorer,
.assets-pane.twin-inspector {
  min-height: 0;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.assets-pane.asset-explorer {
  overflow: hidden;
}

.assets-inspector-sticky {
  position: sticky;
  top: 0;
  z-index: 2;
  background: #11161e;
  padding-bottom: 6px;
}

.assets-twin.twin-canvas {
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.assets-twin-chrome {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  padding: 4px 2px;
}

.assets-twin-sync {
  color: #94a3b8;
  letter-spacing: 0.04em;
}

.assets-twin-tools {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.asset-tree.has-selection .is-dimmed {
  opacity: 0.42;
}

.asset-tree .asset-tree-item.selected,
.asset-tree .asset-tree-group:not(.is-dimmed) {
  opacity: 1;
}

.twin-map-node.is-neighbor {
  opacity: 0.72;
}

.twin-map-node.selected {
  opacity: 1;
  z-index: 4;
}

.assets-causal-strip {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 6px 14px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
  background: rgba(17, 22, 30, 0.92);
  font-size: 0.72rem;
  color: #94a3b8;
}

.assets-causal-strip b {
  color: #e2e8f0;
  font-weight: 700;
}

.assets-twin-viewport {
  position: relative;
  flex: 1 1 auto;
  min-height: 280px;
  overflow: hidden;
  cursor: default;
  --twin-zoom: 1;
}

.assets-twin-viewport.is-panning {
  cursor: grab;
}

.assets-twin-world {
  position: absolute;
  inset: 0;
  transform-origin: center center;
  transition: transform 200ms ease;
}

.assets-topology {
  position: absolute;
  inset: 5% 4%;
  width: 92%;
  height: 90%;
}

.assets-flow {
  animation: assets-flow-dash var(--flow-speed, 1.8s) linear infinite;
  stroke-dasharray: 10 14;
}

@keyframes assets-flow-dash {
  to { stroke-dashoffset: -48; }
}

.map-pipe.is-maintenance {
  stroke: #f4af42 !important;
  stroke-dasharray: 6 8;
}

.assets-os .twin-map-node {
  position: absolute;
  transform: translate(-50%, -50%);
  z-index: 3;
}

.assets-os .twin-map-node.heat-ok {
  box-shadow: 0 0 0 2px rgba(56, 201, 152, 0.35);
}

.assets-os .twin-map-node.heat-watch {
  box-shadow: 0 0 0 2px rgba(244, 175, 66, 0.45);
}

.assets-os .twin-map-node.heat-critical {
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.55);
}

.assets-alarm-pip {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  animation: p8-status-pulse 400ms ease infinite;
}

.assets-tag-overlay {
  display: block;
  margin-top: 2px;
  font-size: 0.58rem;
  letter-spacing: 0.04em;
  color: #8fb4e8;
  font-family: 'DM Mono', ui-monospace, monospace;
}

.assets-minimap {
  position: absolute;
  right: 10px;
  bottom: 10px;
  z-index: 5;
  width: 120px;
  height: 72px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.28);
  background: rgba(9, 11, 15, 0.88);
  overflow: hidden;
}

.assets-minimap-frame {
  all: unset;
  display: block;
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.assets-minimap-frame i {
  position: absolute;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #64748b;
  transform: translate(-50%, -50%);
}

.assets-minimap-frame i.is-selected {
  background: #4f8cff;
  box-shadow: 0 0 0 3px rgba(79, 140, 255, 0.35);
}

.assets-critical-queue {
  margin: 8px 0 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}

.assets-saved-views {
  margin: 8px 0 4px;
}

.assets-tree-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin: 10px 0 6px;
}

.assets-tree-head .MuiButton-root {
  text-transform: none;
  min-width: 0;
  font-size: 0.72rem;
}

.assets-tree-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
  border: 0;
  background: transparent;
  color: inherit;
  font: inherit;
  text-align: left;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 6px;
}

.assets-tree-toggle:hover {
  background: rgba(148, 163, 184, 0.08);
}

.assets-tree-toggle b {
  margin-left: auto;
  opacity: 0.55;
  font-weight: 600;
  font-size: 0.72rem;
}

.assets-tree-toggle.is-unit {
  padding-left: 14px;
  opacity: 0.95;
}

.assets-tree-toggle.is-system {
  padding-left: 22px;
  opacity: 0.9;
  font-size: 0.85rem;
}

.assets-tree-unit .asset-tree-item,
.assets-tree-system .asset-tree-item {
  padding-left: 30px;
}

.assets-bottom-body {
  overflow: auto;
}

.assets-bottom-panel {
  display: grid;
  gap: 8px;
  padding: 4px 2px 10px;
}

.assets-bottom-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 18px;
}

.assets-bottom-panel .event-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  margin-right: 8px;
  background: #64748b;
}

.assets-bottom-panel .event-dot.active {
  background: #4f8cff;
}

.assets-bottom-panel .event-dot.risk {
  background: #ef4444;
}

.assets-bottom-panel b {
  margin-left: 6px;
}

.assets-incident-pip {
  color: #ef4444 !important;
  font-style: normal !important;
  font-weight: 800;
}

.assets-inspector {
  display: flex !important;
  flex-direction: column;
  min-height: 0;
}

.assets-inspector-scroll {
  flex: 1 1 auto;
  min-height: 0;
  overflow: auto;
  padding-bottom: 8px;
}

.assets-inspector-identity {
  position: sticky;
  top: 0;
  z-index: 1;
  background: #11161e;
  padding-bottom: 8px;
}

.assets-accordion {
  border-top: 1px solid rgba(148, 163, 184, 0.12);
}

.assets-accordion-head {
  display: flex;
  align-items: center;
  gap: 6px;
  width: 100%;
  border: 0;
  background: transparent;
  color: inherit;
  font: inherit;
  text-align: left;
  cursor: pointer;
  padding: 8px 4px;
}

.assets-accordion-head em {
  margin-left: auto;
  font-style: normal;
  opacity: 0.55;
  font-size: 0.72rem;
}

.assets-accordion-chevron {
  transition: transform 160ms ease;
  opacity: 0.7;
  transform: rotate(-90deg);
}

.assets-accordion.is-open .assets-accordion-chevron {
  transform: rotate(0deg);
}

.assets-accordion-body {
  padding: 0 4px 10px 22px;
  display: grid;
  gap: 6px;
}

.assets-tree-virtual {
  flex: 1 1 auto;
  min-height: 160px;
  overflow: auto;
  position: relative;
}

.assets-tree-spacer {
  position: relative;
  width: 100%;
}

.assets-tree-window {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  will-change: transform;
}

.assets-virt-row {
  box-sizing: border-box;
  width: 100%;
}

.assets-virt-row.is-unit {
  padding-left: 14px;
}

.assets-virt-row.is-system {
  padding-left: 22px;
}

.assets-lazy-hint {
  display: block;
  padding: 0 4px 6px;
  line-height: 1.35;
}

.assets-inspector-cta {
  position: sticky;
  bottom: 0;
  margin-top: auto;
  flex-shrink: 0;
  padding-top: 12px;
  background: linear-gradient(180deg, transparent, #11161e 28%);
}

.assets-bottom.twin-bottom {
  flex-shrink: 0;
  height: var(--assets-bottom-h, 28vh);
  max-height: var(--assets-bottom-h, 28vh);
  overflow: auto;
}

.assets-os.twin-empty,
.assets-os .twin-empty {
  display: grid;
  place-content: center;
  gap: 8px;
  min-height: 240px;
  text-align: center;
  padding: 24px;
}

.assets-os .twin-empty-orbit {
  display: none !important;
}

.product-page.is-assets-os {
  max-width: none;
  height: calc(100vh - 96px);
  overflow: hidden;
}

.product-page.is-assets-os > .product-hero,
.product-page.is-ops-os > .product-hero {
  display: none !important;
}

.product-page.is-ops-os:not(.is-assets-os) {
  max-width: none;
}

@media (max-width: 1024px) {
  .assets-mobile-tabs {
    display: flex;
    flex-shrink: 0;
  }

  .assets-mobile-tabs .MuiButton-root {
    text-transform: none;
    min-width: 0;
    flex: 1;
  }

  .assets-mobile-tabs .MuiButton-root.active {
    background: rgba(79, 140, 255, 0.16);
  }

  .assets-body.twin-workspace-grid,
  .assets-os.inspector-collapsed .assets-body.twin-workspace-grid {
    grid-template-columns: 1fr !important;
  }

  .assets-body.mobile-explorer > :not(.asset-explorer),
  .assets-body.mobile-twin > :not(.assets-twin),
  .assets-body.mobile-inspector > :not(.twin-inspector) {
    display: none !important;
  }

  .assets-layer-toggles {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .assets-flow,
  .assets-alarm-pip,
  .assets-twin-world {
    animation: none !important;
    transition: none !important;
  }
}
```

## frontend/src/redesign/views/DigitalTwinCanvas.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/DigitalTwinCanvas.jsx`

```javascript
import { useEffect, useRef, useState } from 'react';
import { Box, Button, Menu, MenuItem, Typography } from '@mui/material';
import {
  CenterFocusStrongOutlined, FitScreenOutlined, ZoomInOutlined, ZoomOutOutlined,
} from '@mui/icons-material';
import { assetRisk, label, round } from './shared';

const NODE_SLOTS = [
  { x: 12, y: 48 }, { x: 28, y: 28 }, { x: 46, y: 52 }, { x: 64, y: 28 },
  { x: 82, y: 50 }, { x: 18, y: 72 }, { x: 38, y: 74 }, { x: 58, y: 70 },
  { x: 76, y: 74 }, { x: 14, y: 18 }, { x: 50, y: 16 }, { x: 88, y: 18 },
];

/**
 * Part D + H + I — Digital Twin: selection coupling, no marketing chrome, context menu only on RMB.
 */
export function DigitalTwinCanvas({
  rows = [],
  selectedId,
  onSelect,
  layers,
  camera,
  onCameraChange,
  onFitSelection,
  onFitUnit,
  onOpenIncident,
  onViewForecast,
  onCreateWorkOrder,
  onToggleFavorite,
  onCopyTag,
  onTagClick,
  onAlarmClick,
  isFavorite,
  clean,
}) {
  const viewportRef = useRef(null);
  const [menu, setMenu] = useState(null);
  const [spaceDown, setSpaceDown] = useState(false);
  const dragRef = useRef(null);

  const zoom = Number(camera?.zoom) || 1;
  const panX = Number(camera?.panX) || 0;
  const panY = Number(camera?.panY) || 0;
  const twinNodes = rows.slice(0, NODE_SLOTS.length);
  const selected = twinNodes.find((row) => row.asset.id === selectedId) || twinNodes[0];
  const heatmapMode = layers?.deviation ? 'deviation' : layers?.health ? 'health' : layers?.risk ? 'risk' : null;

  useEffect(() => {
    const onKey = (event) => {
      if (event.code === 'Space') setSpaceDown(event.type === 'keydown');
    };
    window.addEventListener('keydown', onKey);
    window.addEventListener('keyup', onKey);
    return () => {
      window.removeEventListener('keydown', onKey);
      window.removeEventListener('keyup', onKey);
    };
  }, []);

  useEffect(() => {
    if (!selectedId || !onCameraChange) return;
    const index = twinNodes.findIndex((row) => row.asset.id === selectedId);
    if (index < 0) return;
    const slot = NODE_SLOTS[index];
    onCameraChange({
      fitMode: 'selection',
      panX: (50 - slot.x) * 0.35,
      panY: (50 - slot.y) * 0.35,
    });
  // Intentionally only when selection changes
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedId]);

  const setZoom = (next) => onCameraChange?.({ zoom: Math.min(2.2, Math.max(0.55, next)), fitMode: 'free' });
  const selectTwin = (id) => onSelect?.(id, 'twin');

  const onWheel = (event) => {
    if (!event.ctrlKey && !event.metaKey) return;
    event.preventDefault();
    setZoom(zoom + (event.deltaY < 0 ? 0.08 : -0.08));
  };

  const onPointerDown = (event) => {
    if (!spaceDown && event.button !== 1) return;
    dragRef.current = { x: event.clientX, y: event.clientY, panX, panY };
    event.currentTarget.setPointerCapture?.(event.pointerId);
  };

  const onPointerMove = (event) => {
    if (!dragRef.current) return;
    const dx = (event.clientX - dragRef.current.x) / 4;
    const dy = (event.clientY - dragRef.current.y) / 4;
    onCameraChange?.({
      panX: dragRef.current.panX + dx,
      panY: dragRef.current.panY + dy,
      fitMode: 'free',
    });
  };

  const onPointerUp = () => { dragRef.current = null; };

  const openContext = (event, row) => {
    event.preventDefault();
    selectTwin(row.asset.id);
    setMenu({ mouseX: event.clientX, mouseY: event.clientY, row });
  };

  const nodeFill = (row) => {
    const risk = assetRisk(row.asset, row.incident);
    const health = Number(row.asset.health) || 0;
    if (heatmapMode === 'health') return health < 50 ? 'heat-critical' : health < 80 ? 'heat-watch' : 'heat-ok';
    if (heatmapMode === 'deviation') return risk > 55 ? 'heat-critical' : 'heat-watch';
    if (heatmapMode === 'risk') return risk > 70 ? 'heat-critical' : risk > 40 ? 'heat-watch' : 'heat-ok';
    return '';
  };

  const flowSpeed = selected ? Math.max(0.4, Math.min(2.2, (Number(selected.asset.health) || 50) / 50)) : 1;

  return (
    <Box className="twin-canvas assets-twin" ref={viewportRef}>
      <Box className="twin-canvas-top assets-twin-chrome">
        <Typography className="assets-twin-sync" variant="caption">
          {twinNodes.length} nodes · {Math.round(zoom * 100)}%
        </Typography>
        <Box className="assets-twin-tools">
          <Button size="small" onClick={() => setZoom(zoom - 0.1)} aria-label="Zoom out"><ZoomOutOutlined fontSize="small" /></Button>
          <Button size="small" onClick={() => setZoom(zoom + 0.1)} aria-label="Zoom in"><ZoomInOutlined fontSize="small" /></Button>
          <Button size="small" startIcon={<FitScreenOutlined />} onClick={onFitUnit}>Fit unit</Button>
          <Button size="small" startIcon={<CenterFocusStrongOutlined />} onClick={onFitSelection} disabled={!selectedId}>Fit selection</Button>
        </Box>
      </Box>

      {selected && (
        <Box className="assets-causal-strip" role="status">
          <span>{selected.incident ? 'Why: linked case evidence' : 'Why: within baseline envelope'}</span>
          <b>
            {selected.incident
              ? label(selected.incident.incident_type || selected.incident.reasoning || 'Deviation vs baseline')
              : `Health ${round(selected.asset.health)}% · risk ${assetRisk(selected.asset, selected.incident)}`}
          </b>
        </Box>
      )}

      <Box
        className={`twin-process-map assets-twin-viewport ${spaceDown ? 'is-panning' : ''}`}
        onWheel={onWheel}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        tabIndex={0}
        onKeyDown={(event) => {
          if (!twinNodes.length) return;
          const ids = twinNodes.map((row) => row.asset.id);
          const idx = Math.max(0, ids.indexOf(selectedId));
          if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            event.preventDefault();
            selectTwin(ids[Math.min(ids.length - 1, idx + 1)]);
          }
          if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            event.preventDefault();
            selectTwin(ids[Math.max(0, idx - 1)]);
          }
        }}
      >
        <div
          className="assets-twin-world"
          style={{
            transform: `translate(${panX}%, ${panY}%) scale(${zoom})`,
            '--flow-speed': `${1.8 / flowSpeed}s`,
          }}
        >
          <div className="twin-grid-lines" />
          {layers?.process !== false && (
            <svg viewBox="0 0 740 380" className="assets-topology" role="img" aria-label="Unit process topology">
              <path className={`map-pipe ${layers?.maintenance ? 'is-maintenance' : ''}`} d="M80 200H205V115H355V200H495V115H655" />
              <path className="map-pipe map-flow assets-flow" d="M80 200H205V115H355V200H495V115H655" />
              <rect className="map-tank" x="35" y="130" width="82" height="140" rx="12" />
              <path className="map-level" d="M42 232h68v31H42z" />
              <circle className="map-pump" cx="280" cy="115" r="39" />
              <path className="map-pump-spoke" d="M280 76v78M241 115h78M252 87l56 56M308 87l-56 56" />
              <rect className="map-unit" x="420" y="155" width="95" height="90" rx="12" />
              <path className="map-stack" d="M570 115v145M610 115v145" />
            </svg>
          )}

          {twinNodes.map((row, index) => {
            const rowRisk = assetRisk(row.asset, row.incident);
            const slot = NODE_SLOTS[index];
            const heat = nodeFill(row);
            const alarm = Boolean(row.incident) && layers?.alarms !== false;
            const isSelected = row.asset.id === selectedId;
            return (
              <button
                type="button"
                key={row.asset.id}
                onClick={() => selectTwin(row.asset.id)}
                onContextMenu={(event) => openContext(event, row)}
                style={{ left: `${slot.x}%`, top: `${slot.y}%` }}
                className={[
                  'twin-map-node',
                  isSelected ? 'selected' : '',
                  selectedId && !isSelected ? 'is-neighbor' : '',
                  rowRisk > 70 ? 'critical' : '',
                  heat,
                  alarm ? 'has-alarm' : '',
                ].filter(Boolean).join(' ')}
              >
                <i />
                <span>{row.asset.name}</span>
                <b>{round(row.asset.health)}%</b>
                {alarm && (
                  <em
                    className="assets-alarm-pip"
                    title="Open incident"
                    onClick={(event) => {
                      event.stopPropagation();
                      onAlarmClick?.(row, event);
                    }}
                  />
                )}
                {layers?.sensors !== false && (
                  <small
                    className="assets-tag-overlay"
                    onClick={(event) => {
                      event.stopPropagation();
                      onTagClick?.(row);
                    }}
                  >
                    {String(row.asset.tag || row.asset.id).slice(0, 10)}
                  </small>
                )}
              </button>
            );
          })}
        </div>

        <Box className="assets-minimap" aria-label="Minimap">
          <button
            type="button"
            className="assets-minimap-frame"
            onClick={() => onCameraChange?.({ panX: 0, panY: 0, zoom: 1, fitMode: 'unit' })}
          >
            {twinNodes.map((row, index) => (
              <i
                key={row.asset.id}
                className={row.asset.id === selectedId ? 'is-selected' : ''}
                style={{ left: `${NODE_SLOTS[index].x}%`, top: `${NODE_SLOTS[index].y}%` }}
              />
            ))}
          </button>
        </Box>
      </Box>

      <Menu
        open={Boolean(menu)}
        onClose={() => setMenu(null)}
        anchorReference="anchorPosition"
        anchorPosition={menu ? { top: menu.mouseY, left: menu.mouseX } : undefined}
      >
        {menu?.row?.incident && (
          <MenuItem onClick={() => { onOpenIncident?.(menu.row); setMenu(null); }}>Open incident</MenuItem>
        )}
        <MenuItem onClick={() => { onViewForecast?.(menu.row); setMenu(null); }}>View forecast</MenuItem>
        <MenuItem onClick={() => { onCreateWorkOrder?.(menu.row); setMenu(null); }}>Create work order</MenuItem>
        <MenuItem onClick={() => { onToggleFavorite?.(menu.row.asset.id); setMenu(null); }}>
          {isFavorite?.(menu?.row?.asset?.id) ? 'Unpin favorite' : 'Pin favorite'}
        </MenuItem>
        <MenuItem onClick={() => { onCopyTag?.(menu.row); setMenu(null); }}>Copy tag</MenuItem>
        <MenuItem onClick={() => { selectTwin(menu.row.asset.id); setMenu(null); }}>Show in explorer</MenuItem>
      </Menu>
    </Box>
  );
}
```

## frontend/src/redesign/views/ExecutiveBriefing.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/ExecutiveBriefing.jsx`

```javascript
import { useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { ArticleOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { DecisionRail } from '../../design-system/catalog/panels';
import { ApprovalStamp, RATIONALE_MIN } from '../accountability';
import { formatTime, round, Metric } from './shared';

/** Part 8 — Executive approval in-place with rationale + AuditSpine append. */
export function ExecutiveBriefing({ reports }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const sessionApprovals = objectApi.audit?.recentDecisions || [];
  const safeReports = Array.isArray(reports) ? reports.filter(Boolean) : [];
  const [selectedId, setSelectedId] = useState(objectApi.selection.reportId);
  const [mode, setMode] = useState('brief');
  const [approval, setApproval] = useState('Awaiting board approval');
  const [rationale, setRationale] = useState('');
  const rationaleRef = useRef(null);

  const chooseReport = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ reportId: id });
  };

  const report = safeReports.find((item) => item.id === (selectedId || objectApi.selection.reportId)) || safeReports[0] || {};
  const title = report.title || report.name || report.incident_type || 'Alpha refinery operating brief';
  const confidence = round(Number(report.confidence ?? 0.86) <= 1 ? Number(report.confidence ?? 0.86) * 100 : Number(report.confidence ?? 0.86));

  const recordDecision = (decision, statusLabel) => {
    const note = String(rationale || '').trim();
    if (note.length < RATIONALE_MIN) {
      toast.error(`Rationale must be at least ${RATIONALE_MIN} characters`);
      rationaleRef.current?.focus?.();
      return;
    }
    setApproval(statusLabel);
    objectApi.pushAuditDecision({
      id: `brief-${Date.now()}`,
      decision,
      what: `${decision.replace(/_/g, ' ')} — ${title.slice(0, 40)}`,
      who: 'Board chair',
      operator: 'Board chair',
      at: new Date().toISOString(),
      reportId: report.id,
      objectLabel: title,
      rationale: note,
    });
    setRationale('');
    toast.success(`Brief ${decision.replace(/_/g, ' ')}`);
  };

  return (
    <Box className={`executive-briefing ${mode === 'presentation' ? 'presentation' : ''}`}>
      <Box className="briefing-head">
        <Box>
          <Typography className="product-kicker">EXECUTIVE BRIEFING CENTER</Typography>
          <Typography className="briefing-title">{title}</Typography>
          <Typography>{report.created_at ? formatTime(report.created_at) : 'Prepared for the operating committee · live data reconciled'}</Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Button size="small" onClick={() => setMode(mode === 'brief' ? 'presentation' : 'brief')}>
            {mode === 'brief' ? 'Presentation mode' : 'Exit presentation'}
          </Button>
          <Button
            size="small"
            onClick={() => navigateTo(objectApi, navigate, 'investigation', {
              incidentId: report.incident_id || objectApi.selection.incidentId || null,
            })}
          >
            Evidence appendix
          </Button>
          <Button size="small" variant="contained" startIcon={<ArticleOutlined />} onClick={() => toast.success('Board-ready PDF export prepared')}>
            Export PDF
          </Button>
        </Stack>
      </Box>

      <Stack spacing={1} sx={{ mt: 1.5, mb: 2, maxWidth: 360 }}>
        <ApprovalStamp
          signatory={approval.includes('Awaiting') ? 'Control operator' : 'Board chair'}
          timestamp={new Date().toLocaleString()}
          status={approval}
        />
        {sessionApprovals.slice(0, 3).map((entry) => (
          <ApprovalStamp
            key={entry.id}
            signatory={entry.who || entry.operator}
            timestamp={entry.at ? new Date(entry.at).toLocaleString() : null}
            status={entry.decision || 'recorded'}
          />
        ))}
      </Stack>

      <Box className="briefing-layout">
        <Paper className="briefing-index">
          <Typography className="product-kicker">BRIEFING PACK</Typography>
          <Typography className="briefing-index-title">Board view</Typography>
          {(safeReports.length ? safeReports : [{ id: 'current', title }]).map((item, index) => (
            <button
              type="button"
              key={item.id || index}
              className={(report.id || 'current') === (item.id || 'current') ? 'selected' : ''}
              onClick={() => chooseReport(item.id)}
            >
              <span>{String(index + 1).padStart(2, '0')}</span>
              <Box>
                <b>{item.title || item.name || item.incident_type || `Executive brief ${index + 1}`}</b>
                <small>{item.status || 'Ready for review'} · {item.created_at ? formatTime(item.created_at) : 'current'}</small>
              </Box>
            </button>
          ))}
          <Box className="briefing-index-audit">
            <Typography className="product-kicker">AUDIT TRAIL</Typography>
            <Typography><i />Evidence assembled</Typography>
            <Typography><i />AI synthesis complete</Typography>
            <Typography><i />{approval}</Typography>
          </Box>
        </Paper>

        <Paper className="briefing-document">
          <Box className="briefing-document-top">
            <Typography className="product-kicker">OPERATING COMMITTEE · CONFIDENTIAL</Typography>
            <Typography>Publication status <b>{approval}</b></Typography>
          </Box>
          <Typography className="briefing-document-title">Executive summary</Typography>
          <Typography className="briefing-lede">
            {report.summary || report.executive_summary || 'The facility remains operational while a focused reliability intervention is recommended to contain emerging asset risk and preserve the upcoming production window.'}
          </Typography>
          <Box className="briefing-numbers">
            <Metric label="Financial impact" value={report.financial_impact || '$184k projected exposure'} />
            <Metric label="Maintenance cost" value={report.maintenance_cost || '$28k intervention estimate'} />
            <Metric label="Production impact" value={report.production_impact || '1.8% at-risk throughput'} />
            <Metric label="AI confidence" value={`${confidence}%`} />
          </Box>
          <Box className="briefing-section">
            <Typography className="product-kicker">INCIDENT REVIEW & ROOT CAUSE</Typography>
            <Typography>
              {report.root_cause || report.reasoning || 'Evidence indicates a condition-driven risk pattern. Diagnostic and maintenance evidence support an intervention during the next controlled low-load window.'}
            </Typography>
          </Box>
          <Box className="briefing-timeline">
            <Typography className="product-kicker">DECISION TIMELINE</Typography>
            {[
              ['Signal detected', 'Telemetry deviation corroborated'],
              ['Investigation completed', 'AI evidence and maintenance history reconciled'],
              ['Recommendation prepared', 'Target intervention window proposed'],
              ['Board approval', approval],
            ].map(([event, detail], index) => (
              <Box key={event}>
                <i />
                <Typography><b>{event}</b><small>{detail}</small></Typography>
                <span>{index === 3 ? 'Now' : `${index + 1}h ago`}</span>
              </Box>
            ))}
          </Box>
          <Box className="briefing-section recommendation">
            <Typography className="product-kicker">RECOMMENDATION</Typography>
            <Typography>
              {report.recommendation || report.ai_recommendation || 'Approve the condition-based intervention plan and maintain elevated monitoring until the work order is complete.'}
            </Typography>
          </Box>
        </Paper>

        <Paper className="briefing-rail">
          <Typography className="product-kicker">DECISION CONTROL</Typography>
          <Box className="briefing-confidence">
            <Typography>AI confidence</Typography>
            <b>{confidence}%</b>
            <i><span style={{ width: `${confidence}%` }} /></i>
          </Box>
          <Box className="briefing-evidence">
            <Typography className="product-kicker">EVIDENCE & ATTACHMENTS</Typography>
            {['Telemetry deviation packet', 'Maintenance history extract', 'Operating procedure reference', 'Incident evidence log'].map((item, index) => (
              <Typography key={item}><ArticleOutlined />{item}<b>{index < 2 ? 'verified' : 'linked'}</b></Typography>
            ))}
          </Box>
          <Box className="briefing-approvals">
            <Typography className="product-kicker">APPROVAL WORKFLOW</Typography>
            <Typography><i className="done" />Operations review <b>complete</b></Typography>
            <Typography><i className="done" />Reliability review <b>complete</b></Typography>
            <Typography><i />Board approval <b>pending</b></Typography>
          </Box>
          <DecisionRail
            className="e5-decision-bar"
            recommendation={report.recommendation || report.ai_recommendation || 'Approve publication of this operating brief.'}
            rationale={rationale}
            onRationaleChange={setRationale}
            minRationale={RATIONALE_MIN}
            rationaleInputRef={rationaleRef}
            onAccept={() => recordDecision('approved', 'Approved for publication')}
            onModify={() => recordDecision('deferred', 'Deferred pending revision')}
            onReject={() => recordDecision('escalated', 'Escalated to operating committee')}
          />
        </Paper>
      </Box>
    </Box>
  );
}
```

## frontend/src/redesign/views/ForecastTerminal.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/ForecastTerminal.jsx`

```javascript
import { useEffect, useRef, useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { FilterListOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { ProvenanceBadge } from '../accountability';
import { MiniGraph, Empty, Metric, round } from './shared';

/** Part 8 — Forecast in-place select + draft WO navigate + scenario focus. */
export function ForecastTerminal({ assets, telemetry, telemetryStreams, provenance = 'estimated' }) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const scenarioRef = useRef(null);
  const safeAssets = Array.isArray(assets) ? assets.filter(Boolean) : [];
  const [selectedId, setSelectedId] = useState(objectApi.selection.assetId);
  const [scenario, setScenario] = useState(0);

  const chooseAsset = (id) => {
    setSelectedId(id);
    objectApi.setSelection({ assetId: id });
  };

  const focus = safeAssets.find((asset) => asset.id === (selectedId || objectApi.selection.assetId)) || safeAssets[0];
  const stream = (Array.isArray(telemetryStreams) ? telemetryStreams : []).find((item) => item?.asset_id === focus?.id) || telemetry;
  const raw = Array.isArray(stream?.readings) ? stream.readings.map((item) => Number(item.value)).filter(Number.isFinite) : [];
  const health = round(focus?.health ?? raw.at?.(-1) ?? 78);
  const rull = Number(focus?.remaining_life_days ?? focus?.remaining_life ?? Math.max(8, Math.round(health * 0.9)));
  const failure = Math.min(94, Math.max(6, 100 - health + scenario * 5));
  const projected = raw.length > 3
    ? raw
    : Array.from({ length: 18 }, (_, index) => Math.max(16, health - index * (1.2 + scenario * 0.24) + Math.sin(index) * 2));

  useEffect(() => {
    if (!focus?.id) return undefined;
    const timer = requestAnimationFrame(() => scenarioRef.current?.focus?.({ preventScroll: true }));
    return () => cancelAnimationFrame(timer);
  }, [focus?.id]);

  const createWorkOrder = () => {
    if (!focus) return;
    navigateTo(objectApi, navigate, 'maintenance', {
      assetId: focus.id,
      draftWorkOrder: {
        id: `draft-${focus.id}`,
        title: `Intervene on ${focus.name || focus.id}`,
        asset: focus.name,
        assetName: focus.name,
        assetId: focus.id,
        cost: 24500,
        downtime: '12h',
        status: 'Backlog',
        priority: 'P1',
      },
    });
  };

  return (
    <Box className="forecast-terminal">
      <Box className="forecast-terminal-head">
        <Box>
          <Stack direction="row" spacing={1} alignItems="center">
            <Typography className="product-kicker">FORECASTING TERMINAL</Typography>
            <ProvenanceBadge value={provenance} />
          </Stack>
          <Typography className="forecast-terminal-title">Asset risk curve · forward operating model</Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Button size="small" startIcon={<FilterListOutlined />}>Asset universe</Button>
          <Button size="small" variant="outlined" disabled={!focus} onClick={createWorkOrder}>Create work order</Button>
          <Button size="small" variant="contained">Export scenario</Button>
        </Stack>
      </Box>

      <Box className="forecast-terminal-grid">
        <Paper className="terminal-watchlist">
          <Typography className="product-kicker">ASSET WATCHLIST</Typography>
          <Typography className="terminal-watchlist-sub">Sort: highest forward risk</Typography>
          <Box
            tabIndex={0}
            onKeyDown={(event) => {
              const list = safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health));
              if (!list.length) return;
              const ids = list.map((asset) => asset.id);
              const idx = Math.max(0, ids.indexOf(focus?.id));
              if (event.key === 'ArrowDown') {
                event.preventDefault();
                chooseAsset(ids[Math.min(ids.length - 1, idx + 1)]);
              }
              if (event.key === 'ArrowUp') {
                event.preventDefault();
                chooseAsset(ids[Math.max(0, idx - 1)]);
              }
            }}
          >
            {safeAssets.length
              ? safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health)).map((asset, index) => (
                <button
                  type="button"
                  key={asset.id || index}
                  onClick={() => chooseAsset(asset.id)}
                  className={focus?.id === asset.id ? 'selected' : ''}
                >
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  <Box>
                    <b>{asset.name || `Asset ${index + 1}`}</b>
                    <small>{asset.location || asset.zone || 'Process train'} · {round(asset.health)}% health</small>
                  </Box>
                  <em>{Math.max(8, 100 - round(asset.health))}%</em>
                </button>
              ))
              : <Empty text="health forecasts" />}
          </Box>
        </Paper>

        <Paper className="terminal-chart p8-inspector-swap" key={focus?.id || 'chart'}>
          <Box className="terminal-chart-head">
            <Box>
              <Typography className="product-kicker">HEALTH FORECAST · {focus?.name || 'Awaiting asset'}</Typography>
              <Typography>Observed + predicted trajectory with uncertainty</Typography>
            </Box>
            <Box className="terminal-chart-legend">
              <span><i className="observed" />Observed</span>
              <span><i className="model" />Forecast</span>
              <span><i className="band" />80% confidence band</span>
            </Box>
          </Box>
          <Box className="terminal-graph">
            <svg viewBox="0 0 760 285" preserveAspectRatio="none">
              <defs>
                <linearGradient id="uncertainty" x1="0" x2="0" y1="0" y2="1">
                  <stop stopColor="#5f9eff" stopOpacity=".25" />
                  <stop offset="1" stopColor="#5f9eff" stopOpacity=".02" />
                </linearGradient>
              </defs>
              {[55, 115, 175, 235].map((y) => <line key={y} x1="0" x2="760" y1={y} y2={y} />)}
              <rect x="0" y="195" width="760" height="40" className="terminal-watch-zone" />
              <rect x="0" y="235" width="760" height="50" className="terminal-critical-zone" />
              <polygon
                points={`${projected.map((value, index) => `${index * (760 / (projected.length - 1))},${48 + (100 - value) * 1.9 - (8 + index * 0.7)}`).join(' ')} ${projected.slice().reverse().map((value, index) => `${(projected.length - 1 - index) * (760 / (projected.length - 1))},${48 + (100 - value) * 1.9 + (8 + (projected.length - 1 - index) * 0.7)}`).join(' ')}`}
                fill="url(#uncertainty)"
              />
              <polyline
                points={projected.map((value, index) => `${index * (760 / (projected.length - 1))},${48 + (100 - value) * 1.9}`).join(' ')}
                className="terminal-line"
              />
              <line x1="420" x2="420" y1="20" y2="272" className="terminal-marker" />
              <text x="426" y="32">Maintenance window</text>
            </svg>
            <Box className="terminal-axis"><span>Now</span><span>7d</span><span>14d</span><span>21d</span><span>30d</span></Box>
            <Box className="terminal-brush"><span style={{ left: '15%', width: '55%' }} /></Box>
          </Box>
          <Box className="terminal-stats">
            <Metric label="Failure probability" value={`${failure}%`} />
            <Metric label="Remaining useful life" value={`${rull} days`} />
            <Metric label="Maintenance window" value={`Day ${Math.max(4, Math.round(rull * 0.55))}–${Math.max(7, Math.round(rull * 0.72))}`} />
            <Metric label="Model confidence" value={`${Math.max(61, 93 - scenario * 4)}%`} />
          </Box>
        </Paper>

        <Paper className="terminal-scenario">
          <Typography className="product-kicker">WHAT IF SIMULATION</Typography>
          <Typography className="terminal-scenario-title">Operating sensitivity</Typography>
          <Typography>Stress the model to compare risk, downtime, and production impact.</Typography>
          <Box className="scenario-control">
            <Typography>Load increase</Typography>
            <Stack direction="row" spacing={1}>
              <Button size="small" onClick={() => setScenario(Math.max(0, scenario - 1))}>−</Button>
              <b>{scenario * 5}%</b>
              <Button ref={scenarioRef} size="small" onClick={() => setScenario(Math.min(4, scenario + 1))}>+</Button>
            </Stack>
          </Box>
          <Box className="scenario-outcomes">
            <Metric label="Projected cost" value={`$${(18400 + scenario * 7200).toLocaleString()}`} />
            <Metric label="Downtime estimate" value={`${4 + scenario * 2.5}h`} />
            <Metric label="Production impact" value={`${1.2 + scenario * 0.8}%`} />
          </Box>
          <Box className="terminal-recommendation">
            <Typography className="product-kicker">MODEL RECOMMENDATION</Typography>
            <Typography>
              {scenario > 2
                ? 'Advance intervention and protect the next scheduled production window.'
                : 'Plan condition-based maintenance in the identified low-load window.'}
            </Typography>
            <Button size="small" sx={{ mt: 1 }} variant="contained" disabled={!focus} onClick={createWorkOrder}>
              Create work order
            </Button>
          </Box>
        </Paper>
      </Box>

      <Paper className="terminal-bottom">
        <Box>
          <Typography className="product-kicker">HISTORICAL COMPARISON</Typography>
          <Typography>Current trajectory is <b>{failure > 45 ? 'above' : 'within'}</b> the prior 90-day risk envelope.</Typography>
          <MiniGraph values={projected.map((value, index) => value + ((index % 3) - 1) * 4)} label="90-day baseline overlay" />
        </Box>
        <Box>
          <Typography className="product-kicker">RISK & IMPACT SENSITIVITY</Typography>
          <Box className="sensitivity-bars">
            {['Process load', 'Ambient heat', 'Vibration trend', 'Maintenance delay'].map((labelText, index) => (
              <Typography key={labelText}>
                <span>{labelText}</span>
                <i><b style={{ width: `${38 + index * 14 + scenario * 4}%` }} /></i>
                <em>{['Low', 'Medium', 'High', 'Critical'][Math.min(3, Math.floor((index + scenario) / 2))]}</em>
              </Typography>
            ))}
          </Box>
        </Box>
      </Paper>
    </Box>
  );
}
```

## frontend/src/redesign/views/IncidentManagement.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/IncidentManagement.jsx`

```javascript
import { useEffect, useRef, useState } from 'react';
import { Box, Button, IconButton, MenuItem, Paper, Stack, TextField, Typography } from '@mui/material';
import { ArticleOutlined, CommentOutlined, DevicesOutlined, ExpandMoreOutlined, FactCheckOutlined, FilterListOutlined, MemoryOutlined, MoreHorizOutlined, PlayArrowOutlined, SearchOutlined, ShieldOutlined, WarningAmberOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import { useWorkspace } from '../../context/WorkspaceContext';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { OperatorDecisionBar, EvidenceLineage, buildEvidenceFacts, DecisionHistory, ProvenanceBadge } from '../accountability';
import { Status, MiniGraph, EvidenceItem, formatTime, label, round, safeReasoning } from './shared';

export function IncidentManagement({ incidents, telemetry, provenance = 'live' }) {
  const navigate = useNavigate(); const objectApi = useObjectContext();
  const timelineRef = useRef(null);
  const [query, setQuery] = useState(''); const [severity, setSeverity] = useState('all'); const { workspace, setWorkspaceValue } = useWorkspace(); const selectedId = objectApi.selection.incidentId ?? workspace.incidentSelection ?? null; const setSelectedId = (id) => { objectApi.setSelection({ incidentId: id }); setWorkspaceValue('incidentSelection', id); }; const [reasoning, setReasoning] = useState(false); const [replay, setReplay] = useState(false);
  const visible = incidents.filter((item) => `${item.incident_type || ''} ${item.asset_name || ''} ${item.severity || ''}`.toLowerCase().includes(query.toLowerCase()) && (severity === 'all' || String(item.severity).toLowerCase() === severity)); const incident = visible.find((item) => item.id === selectedId) || visible[0];
  useEffect(() => {
    if (!incident?.id) return undefined;
    const timer = requestAnimationFrame(() => timelineRef.current?.querySelector?.('.incident-event')?.scrollIntoView?.({ block: 'nearest', behavior: 'smooth' }));
    return () => cancelAnimationFrame(timer);
  }, [incident?.id]);
  if (!incident) return <Box className="twin-empty"><WarningAmberOutlined fontSize="large" /><Typography fontWeight={800}>No incident records in this view</Typography><Typography variant="body2">The live incident queue will populate when detection or operator escalation creates a case.</Typography></Box>;
  const confidence = round(Number(incident.confidence ?? .78) <= 1 ? Number(incident.confidence ?? .78) * 100 : Number(incident.confidence ?? .78)); const risk = /critical/i.test(incident.severity || '') ? 92 : /high/i.test(incident.severity || '') ? 76 : /medium/i.test(incident.severity || '') ? 54 : 28; const readings = telemetry?.readings || [];
  const events = [['Detection', incident.timestamp || incident.created_at, incident.incident_type || 'Anomaly detected', 'alert'], ['Sensor snapshot', null, incident.evidence || 'Condition deviation was correlated with the operating baseline.', 'signal'], ['Agent finding', null, incident.reasoning || 'Diagnostic agents are evaluating contributing process conditions.', 'agent'], ['Recommended action', null, incident.ai_recommendation || 'Keep the asset under focused monitoring until operator review.', 'action']];
  const pendingRec = Boolean(incident.ai_recommendation || incident.status !== 'closed');
  return <Box className="incident-os"><Box className="incident-os-head"><Box><Typography className="product-kicker">INCIDENT MANAGEMENT</Typography><Typography className="incident-os-title">Active investigation workspace</Typography></Box><Stack direction="row" spacing={1}><Button size="small" startIcon={<FilterListOutlined />}>Filters</Button><Button size="small" variant="contained" startIcon={<FactCheckOutlined />}>Decision log</Button></Stack></Box><Box className="incident-os-grid">
    <Paper className="incident-queue"><Box className="incident-queue-head"><Box><Typography className="product-kicker">INCIDENT QUEUE</Typography><Typography>{visible.length} active cases</Typography></Box><IconButton size="small"><MoreHorizOutlined /></IconButton></Box><TextField size="small" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search cases" slotProps={{ input: { startAdornment: <SearchOutlined fontSize="small" /> } }} /><TextField select size="small" value={severity} onChange={(e) => setSeverity(e.target.value)}><MenuItem value="all">All severities</MenuItem><MenuItem value="critical">Critical</MenuItem><MenuItem value="high">High</MenuItem><MenuItem value="medium">Medium</MenuItem></TextField><Box className="incident-queue-list" tabIndex={0} onKeyDown={(event) => { if (!visible.length) return; const ids = visible.map((item) => item.id); const idx = Math.max(0, ids.indexOf(selectedId)); if (event.key === 'ArrowDown') { event.preventDefault(); setSelectedId(ids[Math.min(ids.length - 1, idx + 1)]); } if (event.key === 'ArrowUp') { event.preventDefault(); setSelectedId(ids[Math.max(0, idx - 1)]); } if (event.key === 'Enter' && ids[idx]) setSelectedId(ids[idx]); }}>{visible.map((item, index) => <button type="button" onClick={() => setSelectedId(item.id)} key={item.id || index} className={`incident-queue-item ${incident.id === item.id ? 'selected' : ''}`}><Box><Status state={item.severity || item.status || 'open'} /><Typography>{formatTime(item.timestamp || item.created_at)}</Typography></Box><b>{label(item.incident_type || 'Operational event')}</b><Typography>{item.asset_name || item.asset_id || 'Asset identification pending'}</Typography><Box><span>Risk { /critical/i.test(item.severity || '') ? 92 : /high/i.test(item.severity || '') ? 76 : 54 }</span><span>{round(Number(item.confidence ?? .78) <= 1 ? Number(item.confidence ?? .78) * 100 : Number(item.confidence ?? .78))}% confidence</span></Box></button>)}</Box></Paper>
    <Paper className="investigation-timeline p8-inspector-swap" key={incident.id} ref={timelineRef}><Box className="investigation-head"><Box><Typography className="product-kicker">INCIDENT TIMELINE</Typography><Typography className="investigation-title">{label(incident.incident_type || 'Operational event')}</Typography><Typography variant="caption">Case {incident.id || 'under review'}  -  affected asset: <Button size="small" onClick={() => incident.asset_id && navigateTo(objectApi, navigate, 'assets', { assetId: incident.asset_id })}>{incident.asset_name || incident.asset_id || 'unresolved'}</Button></Typography><Stack direction="row" spacing={1} sx={{ mt: 1 }}><Button size="small" variant="contained" onClick={() => navigateTo(objectApi, navigate, 'investigation', { incidentId: incident.id, assetId: incident.asset_id || null, focusDecisionBar: true })}>View investigation</Button></Stack></Box><Status state={incident.status || incident.severity || 'open'} /></Box><Box className="incident-summary-strip"><Box><Typography>Severity</Typography><b>{label(incident.severity || 'Medium')}</b><ProvenanceBadge value={provenance} /></Box><Box><Typography>Risk</Typography><b className="risk-text">{risk}/100</b></Box><Box><Typography>Impact</Typography><b>{incident.impact || 'Production exposure'}</b></Box><Box><Typography>Confidence</Typography><b>{confidence}%</b></Box></Box><Box className="incident-timeline">{events.map(([title, time, detail, kind], index) => <Box className={`incident-event ${kind}`} key={title}><span>{index + 1}</span><Box><Typography>{title}<small>{time ? formatTime(time) : 'live evidence stream'}</small></Typography><Typography>{detail}</Typography>{title === 'Agent finding' && <Button size="small" onClick={() => setReasoning(!reasoning)} endIcon={<ExpandMoreOutlined />}>{reasoning ? 'Collapse reasoning' : 'Expand reasoning'}</Button>}{title === 'Agent finding' && reasoning && <motion.div className="incident-reasoning" initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} transition={{ duration: 0.12 }}>{safeReasoning(incident.reasoning || 'The diagnostic workflow is correlating sensor deviation, asset condition, and maintenance history before proposing a root cause.')}</motion.div>}</Box></Box>)}</Box><Box className="dependency-graph"><Typography className="product-kicker">DEPENDENCY GRAPH</Typography><Box><span>Upstream feed</span><i /><strong>{incident.asset_name || 'Affected asset'}</strong><i /><span>Downstream unit</span></Box><Typography variant="caption">Process dependencies are highlighted to support containment decisions.</Typography></Box></Paper>
    <Paper className="incident-evidence"><Box className="incident-evidence-head"><Box><Typography className="product-kicker">EVIDENCE</Typography><Typography>Live case record</Typography></Box><Button size="small" startIcon={<PlayArrowOutlined />} onClick={() => setReplay(!replay)}>{replay ? 'Pause replay' : 'Replay telemetry'}</Button></Box><Box className="evidence-snapshot"><Box><Typography className="product-kicker">SENSOR SNAPSHOT</Typography><Typography>{replay ? 'Replaying incident window  -  2x' : 'Current historian window'}</Typography></Box><MiniGraph values={readings.map((reading) => reading.value)} area label={readings.length ? `${readings.length} captured samples` : 'No telemetry samples attached'} /></Box><Box className="evidence-list"><EvidenceItem icon={<DevicesOutlined />} label="Sensor snapshots" detail={incident.evidence ? 'Evidence packet attached' : 'Live baseline comparison'} /><EvidenceItem icon={<MemoryOutlined />} label="Agent findings" detail={`${confidence}% corroborated confidence`} /><EvidenceItem icon={<ArticleOutlined />} label="Photos & documents" detail={`${incident.documents_count || 2} related records`} /><EvidenceItem icon={<ShieldOutlined />} label="Audit trail" detail="Operator and agent actions recorded" /></Box><Box className="root-cause"><Typography className="product-kicker">ROOT CAUSE HYPOTHESIS</Typography><Typography>{incident.root_cause || incident.reasoning || 'Awaiting operator confirmation after diagnostic evidence is reviewed.'}</Typography></Box></Paper>
  </Box><Paper className="incident-bottom"><Box className="incident-bottom-tabs"><Button className="active" startIcon={<CommentOutlined />}>Comments</Button><Button startIcon={<FactCheckOutlined />}>Decisions</Button><Button>Logs</Button><Button>Approvals</Button><Button>Recommended actions</Button></Box><Box className="incident-bottom-body"><Box><Typography className="product-kicker">OPERATOR NOTES</Typography><Typography className="operator-note">No unresolved operator note is blocking this case. Add a decision or acknowledgement to continue the audit trail.</Typography><Button size="small" startIcon={<CommentOutlined />}>Add note</Button></Box><Box className="decision-track"><Typography className="product-kicker">DECISION TIMELINE</Typography><Typography><i />Detection logged <b>system</b></Typography><Typography><i />Evidence package assembled <b>diagnostic agent</b></Typography><Typography><i />Operator approval pending <b>control room</b></Typography></Box><DecisionHistory entries={objectApi.audit?.recentDecisions?.filter((entry) => !incident?.id || entry.incidentId === incident.id) || []} /></Box></Paper><EvidenceLineage facts={buildEvidenceFacts({ incident, stages: [] })} />{pendingRec ? <OperatorDecisionBar incident={incident} objectApi={objectApi} recommendation={incident.ai_recommendation} /> : null}</Box>;
}
```

## frontend/src/redesign/views/MaintenancePlanning.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/MaintenancePlanning.jsx`

```javascript
import { useState } from 'react';
import { Box, Button, Paper, Stack, Typography } from '@mui/material';
import { BuildOutlined, FilterListOutlined, MoreHorizOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { Metric, MaintenanceSchedule, Status, Empty } from './shared';

export function MaintenancePlanning({ maintenance }) { const navigate = useNavigate(); const objectApi = useObjectContext(); const tasks = Array.isArray(maintenance?.tasks) ? maintenance.tasks : []; const [lane, setLane] = useState('kanban'); const draft = objectApi.draft?.workOrder; const baseWork = tasks.map((task, index) => ({ ...task, id: task.id || index, title: task.title || task.Task || task.name || `Work order ${index + 1}`, priority: task.priority || task.Priority || (index % 3 === 0 ? 'P1' : 'P2'), owner: task.owner || task.Owner || 'Mechanical crew', status: task.status || task.Status || (index % 3 === 0 ? 'Ready' : index % 3 === 1 ? 'Scheduled' : 'In progress'), cost: task.estimated_cost || task.cost || 18500 + index * 4200, downtime: task.estimated_downtime || task.downtime || `${4 + index}h`, assetId: task.asset_id || task.assetId || null })); const work = draft && !baseWork.some((item) => item.id === draft.id) ? [{ ...draft, status: draft.status || 'Backlog', priority: draft.priority || 'P1', owner: draft.owner || 'Mechanical crew' }, ...baseWork] : baseWork; const [selected, setSelected] = useState(objectApi.selection.workOrderId || draft?.id || null); const chooseWork = (id) => { setSelected(id); objectApi.setSelection({ workOrderId: id }); }; const columns = ['Backlog', 'Ready', 'Scheduled', 'In progress', 'Complete']; const selectedWork = work.find((item) => item.id === selected) || work[0]; return <Box className="maintenance-planner"><Box className="maintenance-planner-head"><Box><Typography className="product-kicker">MAINTENANCE PLANNING</Typography><Typography className="maintenance-planner-title">Reliability work control</Typography>{draft ? <Typography variant="caption" color="text.secondary">Draft work order from forecast is staged in Backlog.</Typography> : null}</Box><Stack direction="row" spacing={1}><Button size="small" startIcon={<FilterListOutlined />}>Priority matrix</Button><Button size="small" variant="contained" startIcon={<BuildOutlined />} onClick={() => { const id = `wo-${Date.now()}`; const card = { id, title: 'New reliability work order', status: 'Backlog', priority: 'P2', owner: 'Mechanical crew', cost: 12000, downtime: '4h' }; objectApi.setDraftWorkOrder(card); chooseWork(id); }}>Create work order</Button>{selectedWork?.assetId || selectedWork?.asset_id ? <Button size="small" onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: selectedWork.assetId || selectedWork.asset_id })}>Open twin</Button> : null}</Stack></Box><Box className="maintenance-kpis"><Metric label="Open work orders" value={work.length} /><Metric label="Approval queue" value={work.filter((item) => item.priority === 'P1').length} /><Metric label="Estimated downtime" value={work.length ? `${work.length * 4}h` : '0h'} /><Metric label="Planned cost" value={`$${work.reduce((sum, item) => sum + Number(item.cost || 0), 0).toLocaleString()}`} /></Box><Box className="maintenance-layout"><Paper className="maintenance-board"><Box className="maintenance-board-head"><Box className="maintenance-view-tabs">{['kanban', 'calendar', 'timeline', 'gantt'].map((view) => <Button key={view} className={lane === view ? 'active' : ''} onClick={() => setLane(view)}>{view}</Button>)}</Box><Button size="small">This operating week</Button></Box><Box className={`maintenance-${lane}`}>{lane === 'kanban' ? columns.map((column) => <Box key={column} className="maintenance-column"><Typography>{column}<b>{work.filter((item) => String(item.status).toLowerCase().includes(column.toLowerCase().split(' ')[0])).length}</b></Typography>{work.filter((item, index) => String(item.status).toLowerCase().includes(column.toLowerCase().split(' ')[0]) || (!work.some((other) => String(other.status).toLowerCase().includes(column.toLowerCase().split(' ')[0])) && index % columns.length === columns.indexOf(column))).map((item) => <button type="button" key={item.id} onClick={() => chooseWork(item.id)} className={`work-order ${selectedWork?.id === item.id ? 'selected' : ''}`}><Box><span className={`priority ${String(item.priority).toLowerCase()}`}>{item.priority}</span><MoreHorizOutlined fontSize="small" /></Box><b>{item.title}</b><Typography>{item.owner}</Typography><Box><span>{item.downtime} downtime</span><span>${Number(item.cost).toLocaleString()}</span></Box><i><span style={{ width: `${item.status === 'Complete' ? 100 : item.status === 'In progress' ? 62 : item.status === 'Scheduled' ? 34 : 12}%` }} /></i></button>)}</Box>) : <MaintenanceSchedule work={work} lane={lane} onSelect={chooseWork} />}</Box></Paper><Paper className="maintenance-inspector"><Typography className="product-kicker">WORK ORDER INSPECTOR</Typography>{selectedWork ? <><Typography className="maintenance-work-title">{selectedWork.title}</Typography><Status state={selectedWork.status} /><Box className="maintenance-facts"><Metric label="Priority" value={selectedWork.priority} /><Metric label="Crew" value={selectedWork.owner} /><Metric label="Cost" value={`$${Number(selectedWork.cost).toLocaleString()}`} /><Metric label="Downtime" value={selectedWork.downtime} /></Box><Box className="maintenance-ai"><Typography className="product-kicker">AI SUGGESTED SCHEDULE</Typography><Typography>Schedule in the next low-load window after upstream isolation is confirmed. Reserve mechanical crew and two seal kits.</Typography></Box><Box className="maintenance-checklist"><Typography className="product-kicker">DEPENDENCIES & APPROVALS</Typography><Typography><i />Isolation permit <b>pending</b></Typography><Typography><i />Parts availability <b>2 kits reserved</b></Typography><Typography><i />Shutdown window <b>confirmed</b></Typography></Box><Button variant="contained" fullWidth>Request approval</Button></> : <Empty text="maintenance" />}</Paper></Box><Paper className="maintenance-bottom"><Box><Typography className="product-kicker">CREW ALLOCATION</Typography><Typography>Mechanical A <b>3 / 4 allocated</b></Typography><Typography>Electrical B <b>2 / 3 allocated</b></Typography><Typography>Contractor team <b>on standby</b></Typography></Box><Box><Typography className="product-kicker">INVENTORY & SHUTDOWN PLAN</Typography><Typography><i className="event-dot active" />Critical spares <b>14 available</b></Typography><Typography><i className="event-dot risk" />Valve kits <b>2 below reorder point</b></Typography><Typography><i className="event-dot" />Next shutdown <b>Oct 18  -  12h window</b></Typography></Box></Paper></Box>; }
```

## frontend/src/redesign/views/MissionControlOS.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/MissionControlOS.jsx`

```javascript
import { Box, Button, Paper, Typography } from '@mui/material';
import { BoltOutlined, HubOutlined, ShieldOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { OperationsStrip } from '../../design-system/catalog/shell';
import { ExportAuditButton } from '../accountability';
import { Metric, Status, MiniGraph, label, round, averageHealth, safeReasoning, traceLabel } from './shared';

/** Part 8 — Command Center with sticky OperationsStrip + cross-nav. */
export function MissionControlOS({
  assets, incidents, stages, dashboard, projection, refineries, telemetry, maintenance,
  facility = 'Alpha Refinery', auditEvents = [], provenance = 'live',
}) {
  const navigate = useNavigate();
  const objectApi = useObjectContext();
  const safeAssets = Array.isArray(assets) ? assets : [];
  const safeIncidents = Array.isArray(incidents) ? incidents : [];
  const safeStages = Array.isArray(stages) ? stages : [];
  const health = dashboard.fleet_health ?? averageHealth(safeAssets);
  const primary = safeIncidents[0];
  const values = Array.isArray(telemetry?.readings)
    ? telemetry.readings.map((item) => item.value)
    : safeAssets.map((asset) => asset.health);
  const risks = safeAssets.slice().sort((a, b) => Number(a.health) - Number(b.health)).slice(0, 4);
  const tasks = Array.isArray(maintenance?.tasks) ? maintenance.tasks : [];
  const scopeLabel = (objectApi.scope?.facility || facility || 'Alpha Refinery').toUpperCase();

  const openInvestigation = () => {
    if (!primary) {
      navigateTo(objectApi, navigate, 'assets');
      return;
    }
    navigateTo(objectApi, navigate, 'investigation', {
      incidentId: primary.id,
      assetId: primary.asset_id || null,
      focusDecisionBar: true,
    });
  };

  return (
    <Box className="mission-os">
      <OperationsStrip
        className="p8-operations-strip"
        metrics={[
          { label: 'Fleet health', value: `${health}%`, detail: provenance },
          { label: 'Active incidents', value: String(safeIncidents.length), detail: primary ? label(primary.severity || 'open') : 'Clear' },
          { label: 'Agents live', value: String(safeStages.filter((s) => /running|streaming/i.test(s.state)).length), detail: 'MAO network' },
          { label: 'Work orders', value: String(tasks.length), detail: tasks.length ? 'Planned window' : 'No downtime' },
        ]}
        cta={(
          <Button variant="contained" onClick={openInvestigation}>
            {primary ? 'Review investigation' : 'Open digital twin'}
          </Button>
        )}
      />

      <Paper className={`mission-situation ${primary ? 'attention' : ''}`}>
        <Box>
          <Typography className="product-kicker">{`LIVE SITUATION · ${scopeLabel}`}</Typography>
          <Typography className="mission-situation-title">
            {primary
              ? `${label(primary.incident_type || 'Operating condition')} requires an operator decision.`
              : 'All process trains are holding within the operating envelope.'}
          </Typography>
          <Typography>
            {primary
              ? `${primary.asset_name || 'Affected asset'} · ${label(primary.severity || 'active')} severity · evidence is streaming to the investigation record.`
              : `${safeAssets.length} connected assets · network healthy · autonomous monitoring active.`}
          </Typography>
        </Box>
        <Box className="mission-situation-actions">
          <Typography><i />SYSTEMS LIVE</Typography>
          <ExportAuditButton events={auditEvents} facility={facility} />
          <Button variant="contained" onClick={openInvestigation}>
            {primary ? 'Review investigation' : 'Open digital twin'}
          </Button>
        </Box>
      </Paper>

      <Box className="mission-command-grid">
        <Paper className="mission-twin">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">DIGITAL TWIN OVERVIEW</Typography>
              <Typography>Facility operating map</Typography>
            </Box>
            <Status state={primary ? 'Attention' : 'Nominal'} />
          </Box>
          <Box className="mission-twin-map">
            <Box className="mission-twin-core"><b>{health}%</b><span>FLEET HEALTH</span></Box>
            {['Crude unit', 'Hydrotreater', 'Utilities', 'Tank farm'].map((name, index) => (
              <button
                type="button"
                key={name}
                className={`mission-twin-node ${Number(safeAssets[index]?.health ?? health) < 75 ? 'risk is-pulse' : ''}`}
                onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: safeAssets[index]?.id || null })}
              >
                <i /><span>{name}</span><b>{round(safeAssets[index]?.health ?? health)}%</b>
              </button>
            ))}
            <svg viewBox="0 0 600 250"><path d="M86 70H250M350 70H515M86 180H250M350 180H515M300 94V155" /></svg>
          </Box>
          <Box className="mission-twin-footer">
            <Typography><HubOutlined /> {safeAssets.length} assets connected</Typography>
            <Typography><BoltOutlined /> {values.length ? `${values.length} historian samples` : 'historian synchronizing'}</Typography>
            <Typography><ShieldOutlined /> safety envelope intact</Typography>
          </Box>
        </Paper>

        <Paper className="mission-telemetry-panel">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">LIVE TELEMETRY</Typography>
              <Typography>Operating envelope</Typography>
            </Box>
            <Typography className="mission-live"><i />STREAMING</Typography>
          </Box>
          <Box className="mission-chart-wrap">
            <MiniGraph values={values} area label="Process index · live historian feed" />
            <Box className="mission-chart-annotation"><span>Watch threshold</span><i /></Box>
          </Box>
          <Box className="mission-chart-legend">
            <Typography><i className="normal" />Nominal</Typography>
            <Typography><i className="watch" />Watch ≥ 75%</Typography>
            <Typography><i className="critical" />Critical ≥ 90%</Typography>
            <Typography><i className="band" />Confidence range</Typography>
          </Box>
          <Box className="mission-production">
            <Metric label="Production" value={dashboard.production_rate ?? 'Awaiting meter'} />
            <Metric label="Energy" value={dashboard.energy_usage ?? 'Awaiting meter'} />
            <Metric label="Downtime" value={dashboard.downtime ?? 'Awaiting event data'} />
          </Box>
        </Paper>

        <Paper className="mission-decisions">
          <Typography className="product-kicker">PENDING DECISIONS</Typography>
          <Typography className="mission-decision-count">{primary ? '01' : '00'}</Typography>
          <Typography>
            {primary
              ? primary.ai_recommendation || 'Review the evidence package and approve the recommended response.'
              : 'No operator decision is currently blocking the operating plan.'}
          </Typography>
          <Button
            size="small"
            onClick={() => navigateTo(objectApi, navigate, 'incidents', primary ? { incidentId: primary.id, assetId: primary.asset_id || null } : {})}
          >
            {primary ? 'Open decision record' : 'Review audit trail'}
          </Button>
        </Paper>
      </Box>

      <Box className="mission-lower-grid">
        <Paper className="mission-feed">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">LIVE INCIDENT FEED</Typography>
              <Typography>Signals and investigations</Typography>
            </Box>
            <Button size="small" onClick={() => navigateTo(objectApi, navigate, 'incidents')}>View all</Button>
          </Box>
          {safeIncidents.length
            ? safeIncidents.slice(0, 4).map((item, index) => (
              <Box
                key={item.id || index}
                className="mission-feed-row"
                role="button"
                tabIndex={0}
                onClick={() => navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null })}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') {
                    navigateTo(objectApi, navigate, 'incidents', { incidentId: item.id, assetId: item.asset_id || null });
                  }
                }}
              >
                <i className={/critical|high/i.test(item.severity || '') ? 'risk' : ''} />
                <Box>
                  <b>{label(item.incident_type || 'Operational event')}</b>
                  <Typography>{item.asset_name || item.asset_id || 'Asset pending'} · {safeReasoning(item.evidence || 'Evidence packet is streaming')}</Typography>
                </Box>
                <Status state={item.severity || item.status} />
              </Box>
            ))
            : <Typography className="mission-empty-copy">No active incidents. The event bus and evidence agents are monitoring the facility.</Typography>}
        </Paper>

        <Paper className="mission-agents">
          <Box className="mission-panel-head">
            <Box>
              <Typography className="product-kicker">ACTIVE AI AGENTS</Typography>
              <Typography>Reasoning network</Typography>
            </Box>
            <Typography className="mission-live">
              <i />{safeStages.filter((s) => /running|streaming/i.test(s.state)).length} LIVE
            </Typography>
          </Box>
          <Box className="mission-agent-list">
            {(safeStages.length ? safeStages : ['Telemetry', 'Diagnostic', 'Knowledge', 'Prediction']).slice(0, 4).map((stage, index) => {
              const agent = typeof stage === 'string' ? stage : stage.agent;
              const state = typeof stage === 'string' ? 'standing by' : stage.state;
              return (
                <Box key={`${agent}-${index}`}>
                  <span>{String(agent)[0]}</span>
                  <Typography>
                    <b>{traceLabel(agent, index)}</b>
                    <small>
                      {label(state || 'standing by')} · {stage.confidence
                        ? `${round(Number(stage.confidence) <= 1 ? Number(stage.confidence) * 100 : Number(stage.confidence))}% confidence`
                        : 'heartbeat active'}
                    </small>
                  </Typography>
                  <i className={/running|streaming/i.test(state || '') ? 'active' : ''} />
                </Box>
              );
            })}
          </Box>
        </Paper>

        <Paper className="mission-risks">
          <Typography className="product-kicker">TOP RISKS</Typography>
          {risks.length
            ? risks.map((asset, index) => (
              <Box
                key={asset.id || index}
                role="button"
                tabIndex={0}
                onClick={() => navigateTo(objectApi, navigate, 'assets', { assetId: asset.id })}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') navigateTo(objectApi, navigate, 'assets', { assetId: asset.id });
                }}
              >
                <Typography><b>{asset.name || `Asset ${index + 1}`}</b><small>{asset.location || asset.zone || 'Process train'}</small></Typography>
                <Box><span style={{ width: `${Math.max(10, 100 - round(asset.health))}%` }} /></Box>
                <b>{Math.max(0, 100 - round(asset.health))}</b>
              </Box>
            ))
            : <Typography className="mission-empty-copy">Risk model is synchronizing asset condition.</Typography>}
        </Paper>

        <Paper className="mission-shift">
          <Typography className="product-kicker">SHIFT & MAINTENANCE</Typography>
          <Typography className="mission-shift-title">Day shift · 06:00–18:00</Typography>
          <Typography><i className="event-dot active" />Control room <b>staffed</b></Typography>
          <Typography><i className="event-dot" />Network <b>all zones online</b></Typography>
          <Typography><i className="event-dot risk" />Maintenance window <b>{tasks.length ? `${tasks.length} work orders planned` : 'No planned downtime'}</b></Typography>
          <Button size="small" onClick={() => navigateTo(objectApi, navigate, 'maintenance')}>Open work control</Button>
        </Paper>
      </Box>

      <Paper className="mission-executive">
        <Box>
          <Typography className="product-kicker">EXECUTIVE & FORECAST SUMMARY</Typography>
          <Typography className="mission-executive-title">
            {primary
              ? 'Operational exposure is contained; a targeted intervention protects the next production window.'
              : 'The operating plan remains stable with no material exposure in the current forecast.'}
          </Typography>
        </Box>
        <Box>
          <Metric label="Portfolio health" value={`${health}%`} />
          <Metric label="Forecast exposure" value={primary ? 'Moderate' : 'Low'} />
          <Metric label="Knowledge updates" value={`${safeStages.filter((s) => String(s.agent || '').toLowerCase().includes('knowledge')).length || 1} linked`} />
        </Box>
        <Button onClick={() => navigateTo(objectApi, navigate, 'reports')}>Open board brief</Button>
      </Paper>
    </Box>
  );
}
```

## frontend/src/redesign/views/shared.jsx

**Folder path:** `frontend/src/redesign/views`

**File path:** `frontend/src/redesign/views/shared.jsx`

```javascript
/* Shared product view helpers — Epic 6 */
import { Box, Chip, Typography } from '@mui/material';
import {
  AccountTreeOutlined, ArticleOutlined, BuildOutlined, DevicesOutlined, MemoryOutlined,
  MoreHorizOutlined, ScienceOutlined, ShieldOutlined,
} from '@mui/icons-material';
import { motion } from 'motion/react';
import { MetricWithProvenance } from '../accountability';


export function InspectorMetric({ label: metricLabel, value, unit }) {
  const displayValue = value === null || value === undefined || value === '' ? '--' : value;
  return <Box><Typography>{metricLabel}</Typography><b>{displayValue}{displayValue !== '--' && unit ? <small>{unit}</small> : null}</b></Box>;
}

export function EvidenceItem({ icon, label: evidenceLabel, detail }) { return <Box><span>{icon}</span><Typography><b>{evidenceLabel}</b><small>{detail}</small></Typography><MoreHorizOutlined fontSize="small" /></Box>; }

export function MaintenanceSchedule({ work, lane, onSelect }) { return <Box className="maintenance-schedule-grid"><Box className="maintenance-days">{['Mon 14','Tue 15','Wed 16','Thu 17','Fri 18','Sat 19','Sun 20'].map((day) => <Typography key={day}>{day}</Typography>)}</Box>{work.map((item, index) => <button type="button" onClick={() => onSelect(item.id)} key={item.id} className="schedule-work" style={{ '--start': index % 5 + 1, '--span': index % 2 + 2 }}><b>{item.title}</b><span>{item.owner}  -  {item.downtime}</span></button>)}</Box>; }

export function MiniGraph({ values = [], label, area = false }) { const numbers = values.map(Number).filter(Number.isFinite); if (!numbers.length) return <Box className="mini-graph empty"><Typography>{label}</Typography></Box>; const max = Math.max(...numbers), min = Math.min(...numbers), span = Math.max(max - min, 1); const points = numbers.map((n, i) => `${i * (440 / Math.max(numbers.length - 1, 1))},${116 - ((n - min) / span) * 82}`).join(' '); return <Box className="mini-graph"><svg viewBox="0 0 440 130" preserveAspectRatio="none"><defs><linearGradient id="rigosFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#4f8cff" stopOpacity=".34" /><stop offset="1" stopColor="#4f8cff" stopOpacity="0" /></linearGradient></defs>{[28, 58, 88].map((y) => <line key={y} x1="0" x2="440" y1={y} y2={y} stroke="rgba(148,163,184,.15)" />)}{area && <polyline points={`0,130 ${points} 440,130`} fill="url(#rigosFill)" />}<polyline points={points} fill="none" stroke="#4f8cff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" /></svg><Typography>{label}</Typography></Box>; }

export function Health({ value, large = false }) { const health = round(value); return <Box className={`health ${large ? 'large' : ''}`}><Box><i style={{ width: `${Math.max(0, Math.min(health, 100))}%` }} /></Box><Typography>{health}%</Typography></Box>; }

export function Confidence({ value }) { const percent = round(Number(value) <= 1 ? Number(value) * 100 : value); return <Box className="confidence"><Box><i style={{ width: `${percent}%` }} /></Box><Typography variant="caption">{percent}% confidence</Typography></Box>; }

export function Status({ state }) { return <Chip size="small" className="state" label={label(state || 'Available')} />; }

export function Metric({ label: metricLabel, value, provenance = 'estimated' }) { return <MetricWithProvenance label={metricLabel} value={value} provenance={provenance} />; }

export function Empty({ text = '' }) {
  const lower = text.toLowerCase();
  const state = lower.includes('incident') ? { Icon: ShieldOutlined, title: 'Facility operating normally.', copy: 'No incident records require operator review.', action: 'Continue monitoring live telemetry.' } : lower.includes('maintenance') ? { Icon: BuildOutlined, title: 'No scheduled maintenance.', copy: 'New work orders will appear after planning agent review.', action: 'Review asset condition trends.' } : lower.includes('report') ? { Icon: ArticleOutlined, title: 'Reports will appear after investigations.', copy: 'Completed evidence workflows generate decision-ready briefs here.', action: 'Review active investigations.' } : lower.includes('forecast') || lower.includes('health') ? { Icon: ScienceOutlined, title: 'Forecasting is standing by.', copy: 'Condition projections appear when enough asset telemetry is available.', action: 'Check connected asset telemetry.' } : lower.includes('workforce') || lower.includes('activity') ? { Icon: MemoryOutlined, title: 'AI workforce is ready.', copy: 'The reasoning trace starts automatically when an incident is received.', action: 'Review the live incident ledger.' } : lower.includes('asset') || lower.includes('refinery') ? { Icon: DevicesOutlined, title: 'Fleet condition is within threshold.', copy: 'Assets move here when health or incident signals need attention.', action: 'Inspect the asset portfolio.' } : { Icon: AccountTreeOutlined, title: 'Nothing needs attention here.', copy: 'RigOS will populate this workspace as operating data becomes available.', action: 'Return to Command Center.' };
  return <motion.div className="product-empty-state" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .2 }}><Box className="empty-state-mark"><state.Icon /></Box><Typography className="empty-state-title">{state.title}</Typography><Typography className="empty-state-copy">{state.copy}</Typography><Box className="empty-state-action"><i />{state.action}</Box></motion.div>;
}

export function safeReasoning(value = '') { return /connection to server|operationalerror|permission denied/i.test(String(value)) ? 'Knowledge retrieval was unavailable for this workflow; the remaining agent evidence is retained.' : String(value); }

export function label(value = '') { return String(value).replace(/[_-]+/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase()); }

export function formatTime(value) { if (!value) return 'Live record'; const date = new Date(value); return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' }); }

export function formatDuration(seconds) { if (!Number.isFinite(Number(seconds))) return null; const total = Math.round(Number(seconds)); return total < 60 ? `${total}s` : `${Math.floor(total / 60)}m ${total % 60}s`; }

export function averageHealth(assets) { return assets.length ? round(assets.reduce((total, asset) => total + Number(asset.health || 0), 0) / assets.length) : 0; }

export function round(value) { return Math.round(Number(value) || 0); }

export function assetRisk(asset, incident) { const healthRisk = 100 - round(asset?.health); const incidentRisk = /critical/i.test(incident?.severity || '') ? 35 : /high/i.test(incident?.severity || '') ? 20 : 0; return Math.max(0, Math.min(100, healthRisk + incidentRisk)); }

// Legacy condition cards remain as implementation reference during the twin migration.
// eslint-disable-next-line no-unused-vars

export function traceLabel(agent, index) { const fallback = ['Telemetry', 'Atlas', 'Phoenix', 'Knowledge retrieval', 'Maintenance planner', 'Executive report']; const name = String(agent || '').toLowerCase(); if (!agent) return fallback[index] || 'Workflow stage'; if (name.includes('sensor') || name.includes('telemetry')) return 'Telemetry'; if (name.includes('knowledge')) return 'Knowledge retrieval'; if (name.includes('maintenance') || name.includes('planning')) return 'Maintenance planner'; if (name.includes('report')) return 'Executive report'; return label(agent); }
```
