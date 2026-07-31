# RigOS Object Context

**Status:** Epic 0 — architectural contract + reference implementation; **Assets Phase 0 field freeze** below  
**Code:** `frontend/src/context/ObjectContext.jsx`, `objectNavigation.js`, `breadcrumbs.js`  
**Related:** [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md), [DATA_CONTRACT.md](./DATA_CONTRACT.md), [ASSETS_WORKSPACE_REDESIGN.md](./ASSETS_WORKSPACE_REDESIGN.md)

---

## Purpose

Single source of truth for:

1. **Scope** — facility / unit / portfolio filter  
2. **Selections** — asset, incident, work order, report, agent stage  
3. **UI chrome** — WorkspacePanel open, pinned routes, **Assets pane chrome** (inspector, bottom, twin)  
4. **Drafts** — e.g. maintenance work order from Forecast  
5. **Favorites / recent / notes** — Assets explorer queues and operator notes  
6. **Navigation** — `navigateTo(workspace, payload)` that sets selection then routes  
7. **Breadcrumbs** — pure resolver: context + route → crumb trail  

Pages (Epic 3+) read ObjectContext. Cross-links (Epic 4) must use `navigateTo` only. Assets industrial OS UI must read the [Assets workspace extensions](#assets-workspace-extensions-phase-0-freeze) — do not invent parallel local state for saved views, twin camera, or favorites.

---

## Persistence model

| Key | Storage | Cleared when |
|-----|---------|--------------|
| `scope.facility` | session + local (`rigos.scope.facility`) | User switches facility |
| `scope.unit` | session | Cleared or changed |
| `selection.assetId` | session (`rigos.object.v1`) | Different asset or clear |
| `selection.incidentId` | session | Incident closed or clear |
| `selection.workOrderId` | session | Deselect card |
| `selection.reportId` | session | Different report |
| `selection.agentStageId` | session | Different stage or leave Investigation |
| `ui.workspacePanelOpen` | session | Toggle |
| `ui.pinnedRoutes` | local (`rigos-pins`) | Unpin |
| `ui.focusDecisionBar` | session | Consumed after DecisionBar focus |
| `draft.workOrder` | session | Submit or cancel |
| `audit.recentDecisions` | server + session cache | Never (append-only) |
| `favorites.assetIds` | local | Unpin / remove favorite |
| `recent.assetIds` | session | Age out (max 10) or clear |
| `ui.savedViews` | local | User deletes view |
| `ui.activeSavedViewId` | session | Switch view or clear |
| `ui.inspectorCollapsed` | session | Toggle `]` |
| `ui.bottomWorkspaceHeight` | session | Cycle Ctrl+B (`0` \| `28` \| `45`) |
| `ui.twinLayers` | session | Layer toggles |
| `ui.twinCamera` | session | Fit / pan / zoom / unit change |
| `notes.byAssetId` | session (+ server later) | User clears note |

**Rule:** Navigating between pages **never** clears selections unless the object is deselected or scope changes.

---

## Assets workspace extensions (Phase 0 freeze)

Contract for [ASSETS_WORKSPACE_REDESIGN.md](./ASSETS_WORKSPACE_REDESIGN.md). **Docs freeze now; code lands in build phases 1–6.** Do not rename these keys without updating the redesign doc + DESIGN_SYSTEM.

### Shape

```text
favorites: {
  assetIds: string[]          // bookmarks / pins; also CommandBar “Favorites”
}

recent: {
  assetIds: string[]          // max 10; most-recent first; updated on select
}

notes: {
  byAssetId: {
    [assetId: string]: {
      text: string
      updatedAt: string       // ISO
      operator?: string
    }
  }
}

ui: {
  workspacePanelOpen: boolean
  pinnedRoutes: { label: string, path: string }[]
  focusDecisionBar?: boolean

  // Assets ExplorerLayout chrome
  savedViews: SavedView[]
  activeSavedViewId: string | null
  inspectorCollapsed: boolean          // ] shortcut
  bottomWorkspaceHeight: 0 | 28 | 45   // percent of stage; default 28

  twinLayers: {
    process: boolean      // default true
    risk: boolean         // mutually exclusive heatmap modes: risk | health | deviation
    health: boolean
    deviation: boolean
    alarms: boolean
    sensors: boolean
    maintenance: boolean
  }

  twinCamera: {
    unitId: string | null     // unit-scoped topology
    zoom: number              // 1 = fit unit
    panX: number
    panY: number
    fitMode: 'unit' | 'selection' | 'free'
  }
}

SavedView: {
  id: string
  label: string
  filters: {
    severity?: string[]
    types?: string[]
    healthBand?: 'critical' | 'watch' | 'nominal' | 'all'
    hasIncident?: boolean
  }
  layers: ui.twinLayers       // snapshot
  camera: ui.twinCamera       // snapshot
  groupBy?: 'hierarchy' | 'type' | 'area'
}
```

### Behavior rules

| Field | Rule |
|-------|------|
| `favorites.assetIds` | Local persistence; explorer Favorites queue + context menu Pin |
| `recent.assetIds` | Push on asset select; dedupe; cap 10 |
| `ui.savedViews` | Named presets; activating copies filters + layers + camera into live ui |
| `ui.activeSavedViewId` | Null = ad-hoc filters; switching facility may keep views but re-resolve unit |
| `ui.inspectorCollapsed` | When true, inspector width 0; twin gains space (QA: twin ≥55%) |
| `ui.bottomWorkspaceHeight` | Default **28**; never default to 45 |
| `ui.twinLayers` | At most one of risk/health/deviation true (heatmap mode); process can stay on |
| `ui.twinCamera` | Unit-scoped; fit-to-selection on asset select (200ms ease); not persisted across facilities unless saved view |
| `notes.byAssetId` | Inspector Operator notes section; selection does not write AuditSpine |

### navigateTo options (Assets-related)

Existing: `assetId`, `incidentId`, `workOrderId`, `reportId`, `agentStageId`, `draftWorkOrder`, `focusDecisionBar`.

**Phase 0 additions (optional payload):**

| Option | Effect |
|--------|--------|
| `unitId` | Sets `scope.unit` and `ui.twinCamera.unitId`; fit unit |
| `savedViewId` | Activates saved view before focusing asset |
| `tagId` | Selects asset owning tag; Bottom Telemetry focuses series |

Breadcrumb for assets: `Facility › Assets › {Unit} › {Asset}` when unit is known (resolver must prefer `scope.unit` / asset location path).

---

## Scope filtering contract (A1)

Backend `/api/operations/live` returns **all facilities** in one snapshot. ScopeSwitcher does **not** call a scoped API in Epic 0–4.

| Entity | Client filter |
|--------|---------------|
| Assets | `asset.location === facility` (or all if portfolio) |
| Incidents / audit_logs | Match via `asset_id` → asset location, or `refinery` field if present |
| Maintenance tasks | Match asset location when `asset_id` present |
| Predicted failures | Same as assets |
| Reports | Match incident/asset when linkable; else show all in portfolio |
| Refineries | Name equals facility; portfolio shows all |

If facility string does not match any `location`, treat as portfolio (show all) and surface SyncIndicator warning once.

---

## Navigation API

```text
navigateTo(workspace, options?)
```

| `workspace` | Canonical path |
|-------------|----------------|
| `command` | `/` |
| `assets` | `/assets` |
| `incidents` | `/incidents` |
| `investigation` | `/investigation` |
| `maintenance` | `/maintenance` |
| `forecasting` | `/forecasting` |
| `reports` | `/reports` |

`options` may include: `assetId`, `incidentId`, `workOrderId`, `reportId`, `agentStageId`, `draftWorkOrder`.

Behavior:

1. Merge options into ObjectContext selection / draft  
2. Navigate to canonical path (Epic 4 also handles legacy redirects)  
3. Target page focuses primary panel per Interaction Model  

Epic 3: CTAs may call `navigateTo`; if Epic 4 flags are off, implementation may no-op navigation beyond setting context (document stub). Preferred: always navigate; selection persists.

---

## Breadcrumb resolver

Pure function: `(facility, workspace, labels) → Crumb[]`

```text
Facility › Workspace › Object › Sub-object
```

| Workspace | Object crumb | Sub-object |
|-----------|--------------|------------|
| command | — | — |
| assets | **unit** then **asset name** (Unit › Asset when unit known) | tag (optional) |
| incidents | incident id/type | — |
| investigation | incident id | stage label (optional) |
| maintenance | work order title | — |
| forecasting | asset name | — |
| reports | report title | — |

Crumb `onNavigate` uses `navigateTo` with preserved selection for that crumb level.

---

## Relationship to WorkspaceContext

| Legacy | New |
|--------|-----|
| `assetSelection` | `selection.assetId` |
| `incidentSelection` | `selection.incidentId` |
| Facility in ProductShell localStorage | `scope.facility` |

Epic 0 ships ObjectContext as the new store. `WorkspaceContext` remains until Epic 3 pages migrate; App may wrap both. Epic 6 removes WorkspaceContext.

---

## Application Shell responsibilities

| Concern | Owner |
|---------|-------|
| ObjectContext provider | App root (inside OperationsProvider) |
| WorkspaceHeader breadcrumbs | Shell reads ObjectContext + resolver |
| ⌘J WorkspacePanel | Shell toggles `ui.workspacePanelOpen` |
| ScopeSwitcher | Writes `scope.facility` |
| AuditSpine | Reads audit cache / snapshot adapters |

---

## Exit criteria (Epic 0)

- [x] Spec documented  
- [x] Reference implementation: provider, `navigateTo`, breadcrumb resolver  
- [x] Scope = client-side filter documented  
- [ ] Wired into all pages — Epic 3–4  

## Exit criteria (Assets Phase 0)

- [x] [ASSETS_WORKSPACE_REDESIGN.md](./ASSETS_WORKSPACE_REDESIGN.md) published  
- [x] Assets field freeze documented in this file  
- [x] DESIGN_SYSTEM ExplorerLayout + ObjectInspector cross-linked  
- [ ] Code: extend `ObjectContext.jsx` defaults + persistence for Assets keys — Phase 1+
