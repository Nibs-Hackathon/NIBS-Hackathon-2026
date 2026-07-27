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
