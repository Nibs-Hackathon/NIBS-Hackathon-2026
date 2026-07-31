import { useEffect, useRef, useMemo, useState } from 'react';
import {
  Box, Button, Checkbox, FormControlLabel, Typography,
} from '@mui/material';
import { ViewSidebarOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useWorkspace } from '../../context/WorkspaceContext';
import { useObjectContext } from '../../context/ObjectContext';
import { navigateTo } from '../../context/objectNavigation';
import { getTwinAssets, createWorkOrder, recordOperatorAction, getAssetHealth, getAssetNotes, saveAssetNote } from '../../api/client';
import { mergeAssetsWithTwin } from '../../api/resourceAdapters';
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
  const [twinAssets, setTwinAssets] = useState([]);
  const [assetDetail, setAssetDetail] = useState(null);
  const [knowledgeQuery, setKnowledgeQuery] = useState('');
  const { workspace, setWorkspaceValue } = useWorkspace();

  useEffect(() => {
    let cancelled = false;
    getTwinAssets()
      .then((response) => {
        if (!cancelled) setTwinAssets(Array.isArray(response.data) ? response.data : []);
      })
      .catch(() => {
        if (!cancelled) setTwinAssets([]);
      });
    return () => { cancelled = true; };
  }, []);

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

  const safeAssets = useMemo(
    () => mergeAssetsWithTwin(
      Array.isArray(assets) ? assets.filter((asset) => asset && typeof asset === 'object') : [],
      twinAssets,
    ),
    [assets, twinAssets],
  );
  const safeIncidents = Array.isArray(incidents) ? incidents.filter((item) => item && typeof item === 'object') : [];
  const openIncidents = safeIncidents.filter(
    (item) => !['completed', 'resolved'].includes(String(item.status || '').toLowerCase()),
  );
  const safeStreams = Array.isArray(telemetryStreams) ? telemetryStreams.filter((item) => item && typeof item === 'object') : [];

  const allRows = useMemo(() => safeAssets
    .map((asset, index) => ({
      asset: {
        ...asset,
        id: asset.id ?? `asset-${index}`,
        name: clean(asset.name || asset.asset_name, `Asset ${index + 1}`),
      },
      incident: openIncidents.find((item) => item.asset_id === asset.id),
      telemetry: safeStreams.find((stream) => stream.asset_id === asset.id) || globalTelemetry,
    })), [safeAssets, openIncidents, safeStreams, globalTelemetry]);

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
  const asset = selected?.asset
    ? { ...selected.asset, ...(assetDetail?.id === selected.asset.id ? assetDetail : {}) }
    : null;
  const risk = selected ? assetRisk(asset, selected.incident) : 0;
  const stream = selected?.telemetry && typeof selected.telemetry === 'object' ? selected.telemetry : null;
  const readings = Array.isArray(stream?.readings) ? stream.readings : [];
  const signalValues = readings.map((reading) => Number(reading.value)).filter(Number.isFinite);

  useEffect(() => {
    if (!selected?.asset?.id) {
      setAssetDetail(null);
      return undefined;
    }
    const assetId = selected.asset.id;
    let cancelled = false;
    getAssetHealth(assetId)
      .then((response) => {
        if (!cancelled && response?.data) setAssetDetail(response.data);
      })
      .catch(() => {
        if (!cancelled) setAssetDetail(null);
      });
    getAssetNotes(assetId)
      .then((response) => {
        if (cancelled) return;
        const notes = Array.isArray(response.data) ? response.data : [];
        const latest = notes[0]?.note;
        if (latest != null) objectApi.setAssetNote?.(assetId, latest);
      })
      .catch(() => {});
    setKnowledgeQuery(`${selected.asset.name || ''} ${selected.asset.type || ''} maintenance`.trim());
    return () => { cancelled = true; };
  }, [selected?.asset?.id]);

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

  const createWorkOrderFor = async (row) => {
    const target = row?.asset || asset;
    if (!target) return;
    try {
      const response = await createWorkOrder({
        asset_id: target.id,
        incident_id: row?.incident?.id || selected?.incident?.id || null,
        title: `Inspect ${target.name}`,
        priority: 'P1',
        owner: 'Control operator',
        note: `Created from assets workspace for ${target.name}.`,
      });
      const created = response.data || {};
      objectApi.pushAuditDecision?.({
        id: created.id || `wo-${Date.now()}`,
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
        workOrderId: created.id,
        draftWorkOrder: {
          id: created.id || `draft-${target.id}`,
          title: created.title || `Inspect ${target.name}`,
          asset: target.name,
          assetName: target.name,
          assetId: target.id,
          status: 'Ready',
          priority: created.priority || 'P1',
          cost: created.estimated_cost,
          downtime: created.downtime,
        },
      });
      toast.success('Work order submitted for approval');
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || 'Work order could not be created');
    }
  };

  const acknowledgeWatch = async () => {
    if (!asset) return;
    try {
      await recordOperatorAction({
        asset_id: asset.id,
        incident_id: selected?.incident?.id || null,
        action_type: 'acknowledge_watch',
        decision: 'approved',
        risk_level: risk > 70 ? 'HIGH' : 'MEDIUM',
        note: `Acknowledge watch for ${asset.name}. Operator confirms elevated monitoring without immediate intervention.`,
        operator: 'Control operator',
      });
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
    } catch (error) {
      toast.error(error.response?.data?.detail?.message || 'Watch acknowledgement could not be persisted');
    }
  };

  const noteTimerRef = useRef(null);
  const persistNote = (text) => {
    if (!asset?.id) return;
    objectApi.setAssetNote?.(asset.id, text);
    if (noteTimerRef.current) clearTimeout(noteTimerRef.current);
    noteTimerRef.current = setTimeout(() => {
      saveAssetNote(asset.id, text).catch(() => {
        toast.error('Note could not be saved to the server');
      });
    }, 600);
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
            onNoteChange={persistNote}
            knowledgeQuery={knowledgeQuery}
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
