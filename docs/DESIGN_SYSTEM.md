# RigOS Design System

**Status:** Epic 1 complete — catalog implemented in `frontend/src/design-system/catalog/`  
**Canonical package:** `frontend/src/design-system/` (extend, do not fork)  
**Preview:** `/__catalog` (isolated gallery; Storybook optional later)  
**Assets workspace contract:** [ASSETS_WORKSPACE_REDESIGN.md](./ASSETS_WORKSPACE_REDESIGN.md) (twin-first ExplorerLayout; Phase 0)

This document is the contract for typography, spacing, layouts, components, and the interaction model. Epic 1 builds components from this catalog. Epic 2 builds layouts. Epics 3–5 compose and wire them. The Assets industrial OS redesign supersedes ad-hoc twin chrome on `/assets` — implement against that doc + ExplorerLayout below.

---

## 1. Migration decision (B5)

| Decision | Rule |
|----------|------|
| **Strategy** | **Extend** existing `tokens.js` + `createRigOSV2Theme` |
| **Canonical path** | `frontend/src/design-system/` only — no parallel `src/ui` |
| **Inline theme** | Deprecate `createProductTheme` in `App.jsx` during Epic 2 shell work |
| **Old primitives** | Keep until Epic 1 P0 ships equivalents; then re-export aliases |

### Primitive → catalog migration map

| Current (`primitives.jsx` / `components.jsx`) | New catalog name | Notes |
|----------------------------------------------|------------------|-------|
| `MetricCard` | `MetricCard` | Keep; align to DataCard base |
| `StatusBadge` | `StatusBadge` | Keep; status color table below |
| `EmptyState` | `EmptyState` | Keep |
| `CommandPalette` / `V2CommandPalette` | `CommandBar` | Rename; global modal only |
| `RigToolbar` | `Toolbar` | In-layout filters |
| `PageHeader` | `WorkspaceHeader` | Replace hero pattern |
| `SectionHeader` | `SectionHeader` | Keep |
| `RigDrawer` / `FloatingPanel` / `V2InspectorPanel` | `ObjectInspector` or `WorkspacePanel` | See naming below |
| `AIAgentCard` | `AgentStageCard` | Investigation layer |
| `TimelineCard` | `Timeline` + `EventMarker` | Unify |
| `TelemetryChart` | `Sparkline` / `ForecastChart` | Split by use |
| `NotificationItem` | Inside `NotificationInbox` | WorkspacePanel tab |
| `Toast` | Keep (system) | Not in operational catalog |

---

## 2. Naming: ObjectInspector vs WorkspacePanel (B1)

| Surface | Component | Location | Shortcut | Purpose |
|---------|-----------|----------|----------|---------|
| **ObjectInspector** | `ObjectInspector` | Fixed right pane in Explorer / Kanban layouts | — | Context for selected asset, work order, report |
| **WorkspacePanel** | `WorkspacePanel` | Global slide-over | ⌘/Ctrl J | Audit feed, notifications, system chrome |

Rules:
- ⌘J toggles **WorkspacePanel** only.
- **ObjectInspector** is always visible on desktop in Explorer and Kanban layouts.
- Never name either surface “Inspector” alone in code or docs.

---

## 3. Design language

### Typography

| Role | Spec | Usage |
|------|------|-------|
| **Display** | 28px / 600 / -0.02em | Workspace titles only (one per page) |
| **Heading** | 18px / 600 / -0.01em | Panel titles |
| **Body** | 13px / 450 / 0 | Default operational text |
| **Data** | 13px / 600 / tabular nums | Metrics, timestamps, tag values |
| **KPI** | 24px / 700 / tabular nums | Primary metric in cards |
| **Label** | 11px / 650 / 0.08em caps | Section labels (OPERATIONS STRIP) |
| **Mono** | 12px / 500 | Tag IDs, case IDs, agent hashes |

**Rule:** No sentence longer than 12 words in primary operational zones.

Font stack: prefer expressive product fonts already in redesign; avoid Inter/Roboto as display. Data and mono may use system mono.

### Spacing

Base unit: **4px**. Scale: 4, 8, 12, 16, 24, 32, 48.

- Panel padding: 16px (compact), 24px (standard)
- Panel gap: 12px internal, 16px between panels
- Strip height: 48px (toolbar), 56px (operations strip), 64px (decision bar)

### Grid

- **12-column** fluid grid, 16px gutter
- Fixed panes: 240px (explorer), 280px (queue), 320px (ObjectInspector), 360px (dossier)
- Min content width: 720px before pane collapse
- Max readable line: 68 characters in brief documents

### Motion

| Allowed | Duration | Where |
|---------|----------|-------|
| Value crossfade on live data | 200ms | MetricCard, SignalCard, tags |
| Selection highlight | 120ms | ObjectRow, queue items, kanban cards |
| ObjectInspector content swap | 200ms crossfade | ObjectInspector, CaseDossier |
| Page transition | 120ms fade | Route change only |
| Status dot pulse | 400ms | Critical / Attention badges only |
| Pipeline stage enlarge | 120ms | AgentPipeline active stage |
| Nav active indicator | 120ms opacity | No spring / bounce |

| Forbidden | Reason |
|-----------|--------|
| Hero stagger reveals | Breaks 10-second scan rule |
| Decorative sweeps | Control room distraction |
| Layout shift on data tick | Breaks operator focus |
| Bounce / spring on operational panels | Unprofessional in incident context |

**Reduced motion:** Instant state change; retain color shift.

### Cards

- **Metric Card** — KPI + delta + sparkline; 96px min height
- **Signal Card** — tag name + value + unit + threshold bar; 72px
- **Object Card** — entity name + status + secondary ID; 64px list row
- **Brief Card** — document summary; flexible height
- Border: 1px neutral; left accent 3px for severity only

### Panels / surfaces

| Surface | Use |
|---------|-----|
| Surface-0 | App background |
| Surface-1 | Panel background |
| Surface-2 | Nested panel / ObjectInspector |
| Surface-overlay | CommandBar, WorkspacePanel, modals |

No glass blur in operational mode.

### Status colors

| Semantic | Color | Use |
|----------|-------|-----|
| Nominal | `#22A06B` | Within threshold |
| Advisory | `#F5A524` | Trending wrong |
| Attention | `#E56910` | Requires review |
| Critical | `#E2483D` | Immediate action |
| Offline | `#6B7785` | No signal |
| AI-active | `#5E4DB2` | Agent running (never for severity) |
| Info | `#2684FF` | Neutral information |

**Rule:** Red is never decorative. One severity color per object.

### Elevation

- Flat by default (border-defined)
- Elevation-1: dropdowns, popovers
- Elevation-2: CommandBar, WorkspacePanel, modals
- No drop shadows on data panels in dark mode

### Icons

- 16px inline, 20px toolbar, 24px empty states
- Filled for active/alert; outlined for inactive
- Severity uses color + icon, never icon alone

### Enterprise principles

1. Auditability over aesthetics
2. Object permanence (Asset / Incident / Work Order IDs persist)
3. Provenance honesty (live / estimated / stale)
4. Progressive disclosure
5. Role-aware defaults (operator / planner / executive)

### Control room principles

1. **10-second rule** — critical state in one glance
2. **No dead ends** — every alert links to next action
3. **Hands on keyboard** — CommandBar is primary navigation
4. **Color discipline** — max 2 accent colors visible simultaneously
5. **Shift continuity** — handover notes visible at login

### Dashboard density

| Tier | Row height | Use |
|------|------------|-----|
| Compact | 32px | Queues, tag lists, audit ticker |
| Standard | 48–64px | Cards, kanban, timeline events |
| Comfortable | 80px+ | Executive brief, onboarding only |

Default: compact lists, standard panels.

### Visual rhythm

- Strip → Grid → Detail on every page
- Kickers above panel titles, never above page titles
- Live indicators: 6px dot + label, top-right of panel header only
- Whitespace: 60% data, 25% structure, 15% breathing room

---

## 4. Application Shell (Epic 2)

Not a page layout — wraps all workspaces:

| Region | Content |
|--------|---------|
| Top | WorkspaceHeader (title, breadcrumbs, ScopeSwitcher, SyncIndicator) |
| Left | Primary nav |
| Center | Active workspace layout |
| Right slide-over | WorkspacePanel (⌘J) — audit + notifications |
| Bottom-right | Dock (CommandBar, copilot, WorkspacePanel, pin) |
| Bottom | AuditSpine (operational pages only; hidden on Executive) |

---

## 5. Reusable layouts (6 only — B3)

**Forecast is not a seventh layout.** Forecasting uses `ExplorerLayout` with `canvasVariant="forecast"`.

### MissionControlLayout

| | Col 1–8 | Col 9–12 |
|--|---------|----------|
| Row 1 | OperationsStrip (full 12) | |
| Row 2 | UnitRiskMap | DecisionQueue |
| Row 3 | Sparkline row (12) | |
| Row 4 | AuditSpine / ticker (12, 32px) | |

- Responsive &lt;1024: Strip → Queue → Map → Sparklines
- Sticky: OperationsStrip top; AuditSpine bottom
- Focus: OperationsStrip

### ExplorerLayout (Assets + Forecast)

| | 240–260px | Flex (≥55% content) | 320px (collapsible) |
|--|-------|------|-------|
| Body | Explorer / watchlist | Canvas (`twin` \| `forecast`) | ObjectInspector |
| Footer | — | SignalPanel / Bottom Workspace (default **28%** vh; `0` / `28` / `45` via Ctrl+B) | — |

**Assets (`canvasVariant="twin"`)** — full industrial OS spec: [ASSETS_WORKSPACE_REDESIGN.md](./ASSETS_WORKSPACE_REDESIGN.md).

- Twin is the **primary** pane: only pane that grows with the window; ≥50% viewport height when Bottom collapsed.
- Explorer: smart queues (Critical / Incidents / Recent / Favorites) + virtualized ontology tree; max width **260px**.
- ObjectInspector: default **320px**; collapse to **0** with `]`; see [ObjectInspector sections (asset)](#objectinspector-sections-asset).
- Page body: **no document scroll** — independent pane scroll only.
- Asset toolbar (40px): SavedViewSelect + LayerToggleBar + Fit + Primary WO action — no marketing hero / twin title band.
- Responsive &lt;1024: tabs Explorer | Canvas | ObjectInspector; Bottom as sheet.
- Sticky: toolbar in header; Bottom tab bar when open; AuditSpine at shell bottom.
- Focus: Canvas (twin) after route entry; Inspector first actionable after asset select.

**Forecast (`canvasVariant="forecast"`)** — same shell; watchlist replaces asset queues; canvas is ForecastChart + ScenarioSlider.

### IncidentLayout

| | 280px | Flex | 360px |
|--|-------|------|-------|
| Body | Queue | Timeline | CaseDossier |
| Footer | DecisionBar (full width, sticky) | | |

### InvestigationLayout

| | | |
|--|--|--|
| Row 1 | AgentPipeline (full width, 120px, sticky top) | |
| Row 2 | TracePanel (60%) | EvidenceDetail (40%) |
| Row 3 | DecisionBar (sticky bottom) | |

### KanbanLayout

| | Board (5 cols × min 220px) | 360px |
|--|----------------------------|-------|
| Body | Horizontal-scroll board | ObjectInspector |

- Epic 3: **read-only board** (no drag-and-drop until backlog)

### ExecutiveLayout

| | 240px | Flex | 300px |
|--|-------|------|-------|
| Body | Report index | BriefDocument | DecisionRail |

- Non-operational: **AuditSpine hidden**

---

## 6. Component catalog

### Composition rules

| Composed | Built from |
|----------|------------|
| CaseDossier | EvidencePanel + RecommendationPanel + SectionHeader inside ObjectInspector frame |
| DecisionBar / DecisionRail | Shared DecisionSurface core (`variant="operational" \| "executive"`) |
| IncidentTimeline | Timeline `variant="incident"` |
| IncidentQueueItem / AssetTreeNode / ReportIndexItem | ListRow / ObjectRow variants |
| AuditSpine | AuditEvent rows |
| NotificationInbox | Lives inside WorkspacePanel tab |
| UnitRiskMap | ProcessSchematic + TwinNode at macro scale |
| DecisionQueue | ObjectRow / IncidentQueueItem list for Mission Control |

### Shell

| Component | Purpose |
|-----------|---------|
| WorkspaceHeader | Display title + breadcrumbs + scope + sync |
| OperationsStrip | 4 KPIs + primary CTA |
| CommandBar | Global search and actions (⌘K) |
| ScopeSwitcher | Facility / unit / portfolio |
| SyncIndicator | Connection + last update age |
| AuditSpine | Last N decisions (operational pages) |
| Dock | Command, copilot, WorkspacePanel, pin |
| Toolbar | Page-level filters (real modes only) |
| UnitRiskMap | Facility unit risk overview |
| DecisionQueue | Prioritized decisions for Mission Control |

### Data display

MetricCard, SignalCard, StatusBadge, RiskBadge, HealthRing, Sparkline, ForecastChart, ThresholdLegend, ProvenanceBadge, EmptyState

### Objects & lists

ObjectRow, IncidentQueueItem, WorkOrderCard, AssetTreeNode, TwinNode, ReportIndexItem

### Investigation & AI

AgentPipeline, AgentStageCard, TracePanel, EvidencePanel, EvidenceGraph, RecommendationPanel, DecisionBar, ConfidenceMeter

### Time & events

Timeline, IncidentTimeline (variant), EventMarker, AuditEvent

### Twin & spatial

ProcessSchematic, TagOverlay, GaugeCluster, SignalPanel, TwinNode, MiniMap, LayerToggleBar, SavedViewSelect, SmartQueue, ContextMenu

> Assets twin behavior (layers, minimap, unit scope, selection camera): [ASSETS_WORKSPACE_REDESIGN.md — Part D](./ASSETS_WORKSPACE_REDESIGN.md#part-d--digital-twin-answers--design).

### Panels

ObjectInspector, CaseDossier, DecisionRail, WorkspacePanel, NotificationInbox, SectionHeader, SplitPaneHandle

### Actions

PrimaryCTA, DecisionButtonGroup, RationaleField, ScenarioSlider, FilterChipBar

### Executive

BriefDocument, ApprovalStamp, EvidenceAppendixLink

### Epic 1 priority split

**P0 (unblock layouts):** WorkspaceHeader, OperationsStrip, MetricCard, StatusBadge, RiskBadge, ObjectRow, ObjectInspector, WorkspacePanel, AuditSpine, Toolbar, EmptyState, ProvenanceBadge, DecisionBar (shell), Timeline, CommandBar, SyncIndicator, Dock, ScopeSwitcher, SectionHeader, PrimaryCTA, FilterChipBar, UnitRiskMap, DecisionQueue

**P1 (investigation + twin + executive):** AgentPipeline, AgentStageCard, TracePanel, EvidencePanel, EvidenceGraph, RecommendationPanel, ConfidenceMeter, ProcessSchematic, TagOverlay, GaugeCluster, SignalPanel, TwinNode, AssetTreeNode, WorkOrderCard, ForecastChart, ScenarioSlider, CaseDossier, DecisionRail, BriefDocument, ApprovalStamp, IncidentQueueItem, ReportIndexItem, HealthRing, Sparkline, SignalCard

---

## 7. Interaction model

### Breadcrumbs

Pattern: `Facility › Workspace › Object › Sub-object`

Examples:
- `Alpha Refinery › Command Center`
- `Alpha Refinery › Assets › P-101 Crude Pump`
- `Alpha Refinery › Incidents › INC-2847 › Investigation`

Crumb click navigates and **preserves** object selection in ObjectContext.

### ObjectInspector sections (asset)

Canonical detail for Assets: [ASSETS_WORKSPACE_REDESIGN.md — Part E](./ASSETS_WORKSPACE_REDESIGN.md#part-e--object-inspector).

| # | Section | Default on Assets |
|---|---------|-------------------|
| 1 | Identity (name, tag, class, location path, ProvenanceBadge) | **Expanded** |
| 2 | Current health (StatusBadge, RiskBadge, HealthRing, last inspection) | **Expanded** |
| 3 | Signals (Sparkline, top 3 threshold-aware SignalCards) | **Expanded** |
| 4 | Linked incidents | Collapsed |
| 5 | Forecast (RUL / failure probability + deep link) | Collapsed |
| 6 | Maintenance (open/draft WOs) | Collapsed |
| 7 | Knowledge | Collapsed |
| 8 | Documents | Collapsed |
| 9 | Operator notes | Collapsed |
| 10 | AI recommendations (+ Open investigation lineage) | Collapsed |

**One PrimaryCTA** sticky at inspector bottom: `Open incident` | `Create work order` | `Acknowledge watch` (context-dependent). Do not stack duplicate forecast/WO buttons in the expanded stack.
### In-place vs navigate

| In-place | Navigate |
|----------|----------|
| Select row/card in current workspace | Change workspace (sidebar) |
| ObjectInspector / dossier update | Linked object in another workspace |
| Expand timeline event | CommandBar “Go to …” |
| Kanban card select | Breadcrumb parent |
| Pipeline stage select | Incident → Twin → Forecast links |

### Sticky by layout

| Layout | Sticky top | Sticky bottom |
|--------|------------|---------------|
| Mission Control | OperationsStrip | AuditSpine |
| Explorer | Toolbar (Assets: SavedView + Layers) | SignalPanel / Bottom Workspace when open |
| Incident | Queue header | DecisionBar |
| Investigation | AgentPipeline | DecisionBar |
| Kanban | Toolbar | — |
| Executive | Report index header | — |

Assets geometry QA (twin ≥55% width, page overflow hidden): [ASSETS_WORKSPACE_REDESIGN.md — Design QA](./ASSETS_WORKSPACE_REDESIGN.md#design-qa-lock-must-pass-before-build).

### Keyboard

| Shortcut | Action |
|----------|--------|
| ⌘/Ctrl K | CommandBar |
| ⌘/Ctrl J | WorkspacePanel |
| ⌘/Ctrl ⇧ A | Focus AuditSpine |
| Escape | Close overlay |
| ↑ ↓ | List navigation (explorer / queues) |
| Enter | Select / activate |
| ⌘/Ctrl Enter | Submit DecisionBar when rationale valid |
| `]` | Toggle ObjectInspector collapsed (Assets) |
| ⌘/Ctrl B | Cycle Bottom Workspace height `0 → 28% → 45%` (Assets) |

### Persistence keys (ObjectContext)

See [OBJECT_CONTEXT.md](./OBJECT_CONTEXT.md) (includes [Assets workspace extensions](./OBJECT_CONTEXT.md#assets-workspace-extensions-phase-0-freeze)) and [DATA_CONTRACT.md](./DATA_CONTRACT.md). Assets redesign: [ASSETS_WORKSPACE_REDESIGN.md](./ASSETS_WORKSPACE_REDESIGN.md).

### Epic 3 CTA rule

Cross-page CTAs may render but must call `navigateTo` (or show “Wired in Epic 4” stub). No ad-hoc `useNavigate` paths that bypass ObjectContext.

### Epic 3 AuditSpine rule

Show read-only slice from `audit_logs` / recent decisions. Epic 5 adds append, export, rationale enforcement.

---

## 8. Route map (canonical)

| Workspace | Canonical path | Legacy redirect |
|-----------|----------------|-----------------|
| Command Center | `/` | — |
| Assets | `/assets` | `/digital-twin` |
| Incidents | `/incidents` | `/incident-simulator` |
| Investigation | `/investigation` | `/agent-monitor` |
| Maintenance | `/maintenance` | — |
| Forecasting | `/forecasting` | `/health-prediction` |
| Reports | `/reports` | — |

Legacy redirects remain until Epic 3 cutover.

---

## 9. Error / empty / stale

| Condition | UI |
|-----------|-----|
| Snapshot 503 / services down | Full-page EmptyState: “Operations services unavailable” + retry |
| WebSocket disconnected | SyncIndicator “reconnecting”; retain last snapshot |
| Scope filters to zero | EmptyState in primary pane with clear-scope action |
| Provenance missing | Default ProvenanceBadge to `estimated` (never blank) |
| Stale (&gt;30s without update) | ProvenanceBadge `stale` on KPIs |

---

## Related contracts

- [OBJECT_CONTEXT.md](./OBJECT_CONTEXT.md) — store, navigateTo, breadcrumbs  
- [DATA_CONTRACT.md](./DATA_CONTRACT.md) — snapshot → page props, provenance, IDs  
- [PRODUCT_AUDIT.md](./PRODUCT_AUDIT.md) — operator audit and redesign targets  
