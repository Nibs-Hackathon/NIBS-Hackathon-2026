# Folder: frontend/src/context Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/src/context`

Contains 6 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/src/context/breadcrumbs.js

**Folder path:** `frontend/src/context`

**File path:** `frontend/src/context/breadcrumbs.js`

```javascript
/**
 * Pure breadcrumb resolver — docs/OBJECT_CONTEXT.md + DESIGN_SYSTEM.md
 */

import { WORKSPACE_LABELS, WORKSPACE_PATHS } from './objectNavigation';

/**
 * @typedef {{ label: string, workspace?: string, preserve?: object }} Crumb
 */

/**
 * @param {object} params
 * @param {string} params.facility
 * @param {string} params.workspace — key from WORKSPACE_PATHS
 * @param {object} [params.labels] — { assetName, unitLabel, incidentLabel, workOrderTitle, reportTitle, stageLabel }
 * @param {object} [params.selection]
 * @returns {Crumb[]}
 */
export function resolveBreadcrumbs({ facility, workspace, labels = {}, selection = {} }) {
  const crumbs = [
    {
      label: facility || 'Facility',
      workspace: 'command',
      preserve: {},
    },
    {
      label: WORKSPACE_LABELS[workspace] || workspace,
      workspace,
      preserve: {},
    },
  ];

  if (workspace === 'assets') {
    if (labels.unitLabel) {
      crumbs.push({
        label: labels.unitLabel,
        workspace: 'assets',
        preserve: { assetId: selection.assetId || undefined, unitId: labels.unitLabel },
      });
    }
    if (labels.assetName || selection.assetId) {
      crumbs.push({
        label: labels.assetName || selection.assetId,
        workspace: 'assets',
        preserve: { assetId: selection.assetId },
      });
    }
  }

  if (workspace === 'incidents' && (labels.incidentLabel || selection.incidentId)) {
    crumbs.push({
      label: labels.incidentLabel || selection.incidentId,
      workspace: 'incidents',
      preserve: { incidentId: selection.incidentId },
    });
  }

  if (workspace === 'investigation') {
    if (labels.incidentLabel || selection.incidentId) {
      crumbs.push({
        label: labels.incidentLabel || selection.incidentId,
        workspace: 'investigation',
        preserve: { incidentId: selection.incidentId },
      });
    }
    if (labels.stageLabel || selection.agentStageId) {
      crumbs.push({
        label: labels.stageLabel || selection.agentStageId,
        workspace: 'investigation',
        preserve: {
          incidentId: selection.incidentId,
          agentStageId: selection.agentStageId,
        },
      });
    }
  }

  if (workspace === 'maintenance' && (labels.workOrderTitle || selection.workOrderId)) {
    crumbs.push({
      label: labels.workOrderTitle || selection.workOrderId,
      workspace: 'maintenance',
      preserve: { workOrderId: selection.workOrderId },
    });
  }

  if (workspace === 'forecasting' && (labels.assetName || selection.assetId)) {
    crumbs.push({
      label: labels.assetName || selection.assetId,
      workspace: 'forecasting',
      preserve: { assetId: selection.assetId },
    });
  }

  if (workspace === 'reports' && (labels.reportTitle || selection.reportId)) {
    crumbs.push({
      label: labels.reportTitle || selection.reportId,
      workspace: 'reports',
      preserve: { reportId: selection.reportId },
    });
  }

  return crumbs;
}

export function crumbPath(crumb) {
  return WORKSPACE_PATHS[crumb.workspace] || '/';
}
```

## frontend/src/context/ColorModeContext.jsx

**Folder path:** `frontend/src/context`

**File path:** `frontend/src/context/ColorModeContext.jsx`

```javascript
import { createContext, useContext, useEffect, useMemo, useState } from 'react';

const ColorModeContext = createContext(null);

export function ColorModeProvider({ children }) {
  const [mode, setMode] = useState(() => localStorage.getItem('rigos-color-mode') || 'dark');
  useEffect(() => { localStorage.setItem('rigos-color-mode', mode); document.documentElement.dataset.rigosTheme = mode; }, [mode]);
  const value = useMemo(() => ({ mode, toggle: () => setMode((current) => current === 'dark' ? 'light' : 'dark') }), [mode]);
  return <ColorModeContext.Provider value={value}>{children}</ColorModeContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useColorMode() {
  const context = useContext(ColorModeContext);
  if (!context) throw new Error('useColorMode must be used inside ColorModeProvider');
  return context;
}
```

## frontend/src/context/ObjectContext.jsx

**Folder path:** `frontend/src/context`

**File path:** `frontend/src/context/ObjectContext.jsx`

```javascript
/**
 * ObjectContext — Epic 0 reference implementation.
 * Cross-workspace selection, scope, chrome, and navigation payload.
 * See docs/OBJECT_CONTEXT.md
 */

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { WORKSPACE_PATHS } from './objectNavigation';

const ObjectContext = createContext(null);

const SESSION_KEY = 'rigos.object.v1';
const FACILITY_KEY = 'rigos.scope.facility';
const PINS_KEY = 'rigos-pins';

const FAVORITES_KEY = 'rigos.favorites.assets';

const defaultTwinLayers = {
  process: true,
  risk: true,
  health: false,
  deviation: false,
  alarms: true,
  sensors: true,
  maintenance: false,
};

const defaultTwinCamera = {
  unitId: null,
  zoom: 1,
  panX: 0,
  panY: 0,
  fitMode: 'unit',
};

const defaultState = {
  scope: { facility: 'Alpha Refinery', unit: null },
  selection: {
    assetId: null,
    incidentId: null,
    workOrderId: null,
    reportId: null,
    agentStageId: null,
  },
  ui: {
    workspacePanelOpen: false,
    pinnedRoutes: [],
    focusDecisionBar: false,
    inspectorCollapsed: false,
    bottomWorkspaceHeight: 28,
    twinLayers: { ...defaultTwinLayers },
    twinCamera: { ...defaultTwinCamera },
    activeSavedViewId: null,
    savedViews: [],
  },
  favorites: { assetIds: [] },
  recent: { assetIds: [] },
  notes: { byAssetId: {} },
  draft: { workOrder: null },
  audit: { recentDecisions: [] },
};

function readSession() {
  try {
    const raw = JSON.parse(sessionStorage.getItem(SESSION_KEY) || '{}');
    const facility = localStorage.getItem(FACILITY_KEY) || raw.scope?.facility || defaultState.scope.facility;
    let pinnedRoutes = [];
    let favoriteIds = [];
    try {
      pinnedRoutes = JSON.parse(localStorage.getItem(PINS_KEY) || '[]');
    } catch {
      pinnedRoutes = [];
    }
    try {
      favoriteIds = JSON.parse(localStorage.getItem(FAVORITES_KEY) || '[]');
    } catch {
      favoriteIds = [];
    }
    return {
      ...defaultState,
      ...raw,
      scope: { ...defaultState.scope, ...raw.scope, facility },
      selection: { ...defaultState.selection, ...raw.selection },
      favorites: {
        assetIds: Array.isArray(favoriteIds) ? favoriteIds : (raw.favorites?.assetIds || []),
      },
      recent: {
        assetIds: Array.isArray(raw.recent?.assetIds) ? raw.recent.assetIds.slice(0, 10) : [],
      },
      notes: {
        byAssetId: raw.notes?.byAssetId && typeof raw.notes.byAssetId === 'object' ? raw.notes.byAssetId : {},
      },
      ui: {
        ...defaultState.ui,
        ...raw.ui,
        pinnedRoutes: Array.isArray(pinnedRoutes) ? pinnedRoutes : defaultState.ui.pinnedRoutes,
        twinLayers: { ...defaultTwinLayers, ...(raw.ui?.twinLayers || {}) },
        twinCamera: { ...defaultTwinCamera, ...(raw.ui?.twinCamera || {}) },
        bottomWorkspaceHeight: [0, 28, 45].includes(raw.ui?.bottomWorkspaceHeight)
          ? raw.ui.bottomWorkspaceHeight
          : 28,
        inspectorCollapsed: Boolean(raw.ui?.inspectorCollapsed),
      },
      draft: { ...defaultState.draft, ...raw.draft },
      audit: { ...defaultState.audit, ...raw.audit },
    };
  } catch {
    return {
      ...defaultState,
      ui: {
        ...defaultState.ui,
        twinLayers: { ...defaultTwinLayers },
        twinCamera: { ...defaultTwinCamera },
      },
    };
  }
}

function persistSession(state) {
  const { ui, scope, favorites, recent, notes, ...rest } = state;
  sessionStorage.setItem(
    SESSION_KEY,
    JSON.stringify({
      ...rest,
      scope: { facility: scope.facility, unit: scope.unit },
      recent: { assetIds: (recent?.assetIds || []).slice(0, 10) },
      notes: { byAssetId: notes?.byAssetId || {} },
      ui: {
        workspacePanelOpen: ui.workspacePanelOpen,
        focusDecisionBar: Boolean(ui.focusDecisionBar),
        inspectorCollapsed: Boolean(ui.inspectorCollapsed),
        bottomWorkspaceHeight: ui.bottomWorkspaceHeight ?? 28,
        twinLayers: ui.twinLayers || defaultTwinLayers,
        twinCamera: ui.twinCamera || defaultTwinCamera,
        activeSavedViewId: ui.activeSavedViewId || null,
        savedViews: ui.savedViews || [],
      },
    }),
  );
  if (scope.facility) localStorage.setItem(FACILITY_KEY, scope.facility);
  localStorage.setItem(PINS_KEY, JSON.stringify(ui.pinnedRoutes || []));
  localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites?.assetIds || []));
}

export function ObjectProvider({ children }) {
  const [state, setState] = useState(readSession);

  useEffect(() => {
    persistSession(state);
  }, [state]);

  const setFacility = useCallback((facility) => {
    setState((current) => ({
      ...current,
      scope: { ...current.scope, facility, unit: null },
    }));
  }, []);

  const setUnit = useCallback((unit) => {
    setState((current) => ({
      ...current,
      scope: { ...current.scope, unit },
    }));
  }, []);

  const setSelection = useCallback((patch) => {
    setState((current) => ({
      ...current,
      selection: { ...current.selection, ...patch },
    }));
  }, []);

  const clearSelection = useCallback((keys) => {
    setState((current) => {
      const selection = { ...current.selection };
      (keys || Object.keys(selection)).forEach((key) => {
        selection[key] = null;
      });
      return { ...current, selection };
    });
  }, []);

  const setWorkspacePanelOpen = useCallback((open) => {
    setState((current) => ({
      ...current,
      ui: { ...current.ui, workspacePanelOpen: Boolean(open) },
    }));
  }, []);

  const toggleWorkspacePanel = useCallback(() => {
    setState((current) => ({
      ...current,
      ui: { ...current.ui, workspacePanelOpen: !current.ui.workspacePanelOpen },
    }));
  }, []);

  const setPinnedRoutes = useCallback((pinnedRoutes) => {
    setState((current) => ({
      ...current,
      ui: { ...current.ui, pinnedRoutes },
    }));
  }, []);

  const setDraftWorkOrder = useCallback((workOrder) => {
    setState((current) => ({
      ...current,
      draft: { ...current.draft, workOrder },
    }));
  }, []);

  const setFocusDecisionBar = useCallback((focus) => {
    setState((current) => ({
      ...current,
      ui: { ...current.ui, focusDecisionBar: Boolean(focus) },
    }));
  }, []);

  const patchUi = useCallback((patch) => {
    setState((current) => ({
      ...current,
      ui: { ...current.ui, ...patch },
    }));
  }, []);

  const setTwinLayers = useCallback((patch) => {
    setState((current) => {
      const next = { ...current.ui.twinLayers, ...patch };
      // Heatmap modes are mutually exclusive
      if (patch.risk) {
        next.risk = true;
        next.health = false;
        next.deviation = false;
      } else if (patch.health) {
        next.health = true;
        next.risk = false;
        next.deviation = false;
      } else if (patch.deviation) {
        next.deviation = true;
        next.risk = false;
        next.health = false;
      }
      return { ...current, ui: { ...current.ui, twinLayers: next } };
    });
  }, []);

  const setTwinCamera = useCallback((patch) => {
    setState((current) => ({
      ...current,
      ui: {
        ...current.ui,
        twinCamera: { ...current.ui.twinCamera, ...patch },
      },
    }));
  }, []);

  const toggleFavoriteAsset = useCallback((assetId) => {
    if (!assetId) return;
    setState((current) => {
      const ids = current.favorites?.assetIds || [];
      const next = ids.includes(assetId) ? ids.filter((id) => id !== assetId) : [...ids, assetId];
      return { ...current, favorites: { assetIds: next } };
    });
  }, []);

  const pushRecentAsset = useCallback((assetId) => {
    if (!assetId) return;
    setState((current) => {
      const ids = [assetId, ...(current.recent?.assetIds || []).filter((id) => id !== assetId)].slice(0, 10);
      return { ...current, recent: { assetIds: ids } };
    });
  }, []);

  const setAssetNote = useCallback((assetId, text) => {
    if (!assetId) return;
    setState((current) => ({
      ...current,
      notes: {
        byAssetId: {
          ...(current.notes?.byAssetId || {}),
          [assetId]: String(text ?? ''),
        },
      },
    }));
  }, []);

  const cycleBottomHeight = useCallback(() => {
    setState((current) => {
      const order = [0, 28, 45];
      const idx = order.indexOf(current.ui.bottomWorkspaceHeight ?? 28);
      const next = order[(idx + 1) % order.length];
      return { ...current, ui: { ...current.ui, bottomWorkspaceHeight: next } };
    });
  }, []);

  const pushAuditDecision = useCallback((entry) => {
    setState((current) => ({
      ...current,
      audit: {
        recentDecisions: [entry, ...(current.audit.recentDecisions || [])].slice(0, 20),
      },
    }));
  }, []);

  /**
   * Apply navigation payload to context. Caller (or navigateTo helper) performs routing.
   */
  const applyNavigationPayload = useCallback((options = {}) => {
    setState((current) => {
      const selection = { ...current.selection };
      if (options.assetId !== undefined) selection.assetId = options.assetId;
      if (options.incidentId !== undefined) selection.incidentId = options.incidentId;
      if (options.workOrderId !== undefined) selection.workOrderId = options.workOrderId;
      if (options.reportId !== undefined) selection.reportId = options.reportId;
      if (options.agentStageId !== undefined) selection.agentStageId = options.agentStageId;
      const draft = { ...current.draft };
      if (options.draftWorkOrder !== undefined) draft.workOrder = options.draftWorkOrder;
      const ui = { ...current.ui };
      if (options.focusDecisionBar !== undefined) ui.focusDecisionBar = Boolean(options.focusDecisionBar);
      let scope = current.scope;
      if (options.unitId !== undefined) {
        scope = { ...scope, unit: options.unitId };
        ui.twinCamera = { ...ui.twinCamera, unitId: options.unitId, fitMode: 'unit' };
      }
      let recent = current.recent;
      if (options.assetId) {
        recent = {
          assetIds: [options.assetId, ...(current.recent?.assetIds || []).filter((id) => id !== options.assetId)].slice(0, 10),
        };
      }
      return { ...current, selection, draft, ui, scope, recent };
    });
  }, []);

  const value = useMemo(
    () => ({
      ...state,
      paths: WORKSPACE_PATHS,
      setFacility,
      setUnit,
      setSelection,
      clearSelection,
      setWorkspacePanelOpen,
      toggleWorkspacePanel,
      setPinnedRoutes,
      setDraftWorkOrder,
      setFocusDecisionBar,
      patchUi,
      setTwinLayers,
      setTwinCamera,
      toggleFavoriteAsset,
      pushRecentAsset,
      setAssetNote,
      cycleBottomHeight,
      pushAuditDecision,
      applyNavigationPayload,
    }),
    [
      state,
      setFacility,
      setUnit,
      setSelection,
      clearSelection,
      setWorkspacePanelOpen,
      toggleWorkspacePanel,
      setPinnedRoutes,
      setDraftWorkOrder,
      setFocusDecisionBar,
      patchUi,
      setTwinLayers,
      setTwinCamera,
      toggleFavoriteAsset,
      pushRecentAsset,
      setAssetNote,
      cycleBottomHeight,
      pushAuditDecision,
      applyNavigationPayload,
    ],
  );

  return <ObjectContext.Provider value={value}>{children}</ObjectContext.Provider>;
}

export function useObjectContext() {
  const context = useContext(ObjectContext);
  if (!context) {
    throw new Error('useObjectContext must be used within ObjectProvider');
  }
  return context;
}

/** Safe hook for gradual migration before provider is universal. */
export function useObjectContextOptional() {
  return useContext(ObjectContext);
}
```

## frontend/src/context/objectNavigation.js

**Folder path:** `frontend/src/context`

**File path:** `frontend/src/context/objectNavigation.js`

```javascript
/**
 * Navigation API for ObjectContext — docs/OBJECT_CONTEXT.md
 * Epic 4: product routes use legacy ProductShell paths.
 */

export const WORKSPACE_PATHS = {
  command: '/',
  assets: '/assets',
  incidents: '/incident-simulator',
  investigation: '/agent-monitor',
  maintenance: '/maintenance',
  forecasting: '/health-prediction',
  reports: '/reports',
};

/** Aliases → product paths (canonical Epic 3 names still resolve). */
export const PATH_ALIASES = {
  '/incidents': '/incident-simulator',
  '/investigation': '/agent-monitor',
  '/forecasting': '/health-prediction',
  '/digital-twin': '/assets',
  '/ai-activity': '/agent-monitor',
};

export const WORKSPACE_LABELS = {
  command: 'Command Center',
  assets: 'Assets',
  incidents: 'Incidents',
  investigation: 'Investigation',
  maintenance: 'Maintenance',
  forecasting: 'Forecasting',
  reports: 'Reports',
};

export function pathToWorkspace(pathname) {
  const normalized = PATH_ALIASES[pathname] || pathname;
  const entry = Object.entries(WORKSPACE_PATHS).find(([, path]) => path === normalized);
  return entry ? entry[0] : 'command';
}

/**
 * Apply selection payload then navigate.
 */
export function navigateTo(objectApi, navigate, workspace, options = {}) {
  const path = WORKSPACE_PATHS[workspace];
  if (!path) {
    console.warn(`[RigOS] Unknown workspace: ${workspace}`);
    return;
  }
  objectApi.applyNavigationPayload(options);
  navigate(path);
}

/**
 * Client-side facility scope filter (backend returns full portfolio).
 */
export function filterByFacility(items, facility, getLocation) {
  if (!facility || facility === 'Enterprise view' || facility === 'portfolio' || facility === 'North Sea Portfolio') {
    return items || [];
  }
  const list = Array.isArray(items) ? items : [];
  const matched = list.filter((item) => getLocation(item) === facility);
  return matched.length ? matched : list;
}

export function assetLocation(asset) {
  return asset?.location || asset?.zone || asset?.refinery || null;
}

export function incidentLocation(item, assets = []) {
  if (item?.refinery || item?.location) return item.refinery || item.location;
  const asset = assets.find((a) => a.id === item?.asset_id);
  return assetLocation(asset);
}

export function taskLocation(task, assets = []) {
  if (task?.refinery || task?.location) return task.refinery || task.location;
  const asset = assets.find((a) => a.id === task?.asset_id);
  return assetLocation(asset);
}
```

## frontend/src/context/OperationsContext.jsx

**Folder path:** `frontend/src/context`

**File path:** `frontend/src/context/OperationsContext.jsx`

```javascript
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { getOperationsLive } from '../api/client';
import { useWebSocket } from '../hooks/useWebSocket';

const OperationsContext = createContext(null);

const emptySnapshot = {
  dashboard: {}, assets: [], refineries: [], telemetry_by_refinery: [], critical_incidents: [], audit_logs: [],
  investigation: { status: 'waiting', stages: [] }, ai_activity: [],
  maintenance: { tasks: [] }, predicted_failures: [], notifications: [], reports: [],
  telemetry: { readings: [] }, critical_asset_telemetry: [],
};

const collectionKeys = ['assets', 'refineries', 'telemetry_by_refinery', 'critical_incidents', 'audit_logs', 'ai_activity', 'predicted_failures', 'notifications', 'reports', 'critical_asset_telemetry'];
const objectKeys = ['dashboard', 'investigation', 'maintenance', 'telemetry'];

function mergeOperations(current, incoming) {
  if (!incoming || typeof incoming !== 'object') return current;
  const next = { ...current, ...incoming };
  objectKeys.forEach((key) => {
    if (incoming[key] && typeof incoming[key] === 'object' && !Array.isArray(incoming[key])) next[key] = { ...(current[key] || {}), ...incoming[key] };
  });
  collectionKeys.forEach((key) => {
    if (!Array.isArray(incoming[key])) next[key] = current[key] || [];
  });
  return next;
}

export function OperationsProvider({ children }) {
  const [initialOperations, setInitialOperations] = useState(emptySnapshot);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const notifiedIds = useRef(new Set());
  const { connected, data: socketSnapshot } = useWebSocket();

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const response = await getOperationsLive();
      setInitialOperations((current) => mergeOperations(current, response.data));
      setLastUpdated(Date.now());
      setError(null);
    } catch (requestError) {
      setError(requestError);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    getOperationsLive()
      .then((response) => {
        if (!active) return;
        setInitialOperations((current) => mergeOperations(current, response.data));
        setLastUpdated(Date.now());
        setError(null);
      })
      .catch((requestError) => active && setError(requestError))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  // The REST snapshot is an independent safety net for the live socket. It
  // keeps pages populated during deploys, sleep/wake, or a temporary WS drop.
  useEffect(() => {
    const interval = setInterval(() => { refresh(); }, 10000);
    return () => clearInterval(interval);
  }, [refresh]);

  useEffect(() => {
    if (!socketSnapshot) return;
    setInitialOperations((current) => mergeOperations(current, socketSnapshot));
    setLastUpdated(Date.now());
    (socketSnapshot.notifications || []).forEach((notification) => {
      if (notifiedIds.current.has(notification.id)) return;
      notifiedIds.current.add(notification.id);
      toast(notification.title, {
        duration: 4000,
        icon: notification.severity === 'critical' ? '🔴' : notification.severity === 'warning' ? '🟠' : '🔵',
      });
    });
  }, [socketSnapshot]);

  const value = useMemo(() => {
    const operations = initialOperations;
    const telemetryReadings = operations.telemetry?.readings || [];
    const currentValue = Number(telemetryReadings.at?.(-1)?.value);
    const agents = (operations.investigation?.stages || []).map((stage) => ({ name: stage.agent, state: stage.state || 'waiting', confidence: stage.confidence, duration: stage.duration_seconds }));
    const ambient = { lastUpdated, telemetry: { value: currentValue, delta: 0, unit: operations.telemetry?.unit || '' }, agents, incidentCount: Number(operations.dashboard?.active_incidents || operations.critical_incidents?.length || 0) };
    return { operations, ambient, connected, loading: socketSnapshot ? false : loading, error: socketSnapshot ? null : error, refresh };
  }, [initialOperations, connected, loading, error, socketSnapshot, refresh, lastUpdated]);
  return <OperationsContext.Provider value={value}>{children}</OperationsContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useOperations() {
  const context = useContext(OperationsContext);
  if (!context) throw new Error('useOperations must be used inside OperationsProvider');
  return context;
}
```

## frontend/src/context/WorkspaceContext.jsx

**Folder path:** `frontend/src/context`

**File path:** `frontend/src/context/WorkspaceContext.jsx`

```javascript
import { createContext, useContext, useEffect, useMemo, useState } from 'react';

const WorkspaceContext = createContext(null);
const STORAGE_KEY = 'rigos.workspace.v1';

function readWorkspace() {
  try { return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '{}'); } catch { return {}; }
}

export function WorkspaceProvider({ children }) {
  const [workspace, setWorkspace] = useState(readWorkspace);
  useEffect(() => { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(workspace)); }, [workspace]);
  const value = useMemo(() => ({
    workspace,
    setWorkspaceValue: (key, value) => setWorkspace((current) => ({ ...current, [key]: value })),
  }), [workspace]);
  return <WorkspaceContext.Provider value={value}>{children}</WorkspaceContext.Provider>;
}

export function useWorkspace() {
  const context = useContext(WorkspaceContext);
  // Keep route-level UI usable during React Fast Refresh, when a context
  // provider can briefly be remounted after its consumers.
  const [fallbackWorkspace, setFallbackWorkspace] = useState(readWorkspace);
  useEffect(() => {
    if (!context) sessionStorage.setItem(STORAGE_KEY, JSON.stringify(fallbackWorkspace));
  }, [context, fallbackWorkspace]);
  const fallback = useMemo(() => ({
    workspace: fallbackWorkspace,
    setWorkspaceValue: (key, value) => setFallbackWorkspace((current) => ({ ...current, [key]: value })),
  }), [fallbackWorkspace]);
  return context || fallback;
}
```
