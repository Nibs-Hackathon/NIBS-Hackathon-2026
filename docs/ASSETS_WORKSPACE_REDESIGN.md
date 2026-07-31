# Assets Workspace Redesign — Industrial OS Spec

**Status:** Phase 0 contract — design only (no UI implementation in this document)  
**Layout family:** `ExplorerLayout` with `canvasVariant="twin"`  
**Related:** [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) · [OBJECT_CONTEXT.md](./OBJECT_CONTEXT.md) · [PRODUCT_AUDIT.md](./PRODUCT_AUDIT.md) · [DATA_CONTRACT.md](./DATA_CONTRACT.md)

**Mode:** Forget preserving the current Assets UI. RigOS is an Industrial Operating System, not a dashboard.

Reference products: Palantir Foundry, AVEVA PI Vision, Honeywell Forge, Siemens XHQ, AspenTech, Grafana, Datadog, Azure Industrial IoT.

---

## Part A — Brutal audit of the current Assets page

What exists today (mental model of `frontend/src/redesign/views/AssetConsole.jsx`):

```
[hero title] → [Filters (dead) + sort]
[long flat explorer] | [decorative SVG + ≤5 nodes] | [inspector stack]
[bottom tab strip with 8 mostly empty tabs + one chart]
```

### What wastes screen space
- **Product hero** above the workspace (“Critical assets” + prose) — marketing, not operations. Steals vertical pixels every visit.
- **Twin workspace head** (“DIGITAL TWIN WORKSPACE / Alpha refinery - live asset graph”) duplicates shell breadcrumbs and facility scope.
- **Bottom strip of 8 tabs** always present even when most are inert — permanent chrome with one real panel.
- **Inspector metric grid** (6+ numeric cells) without thresholds or time — dense but low signal.
- **Canvas footer** (“connected assets / telemetry 4 sec ago / linked incidents”) — status that belongs in SyncIndicator / OperationsStrip, not a second footer.

### What feels decorative
- Twin SVG pipes/tanks/pumps with **no binding to real process topology**.
- Orbit empty-state animation.
- Map legend Nominal/Watch/At risk that does not drive filtering.
- Health bar / prediction bar without provenance of the model.

### What feels fake
- **Filters** button — no filter panel.
- Bottom tabs: Sensor history, Maintenance, Knowledge, Forecast, Incidents, Documents, AI summary — **labels only**.
- “telemetry updated 4 sec ago” — hardcoded copy.
- Zoom control that only scales CSS on a static illustration.
- Only **five** map nodes for an entire facility.
- Predicted failure + AI recommendation blocks that look authoritative without lineage to TracePanel/evidence.

### What requires too much scrolling
- Flat explorer list of every asset with weak grouping.
- Inspector stacks Identity → State → Signals → Links → Actions **vertically forever**.
- Bottom workspace + inspector + twin compete for height; operator scrolls the page, not a pane.

### Poor hierarchy
- Title weight competes with selected asset name.
- Risk number, health %, badges, and recommendation all shout at the same level.
- Explorer “Group: location|type” is a toggle buried under search — hierarchy is an afterthought.
- Twin is visually centered but informationally empty → hierarchy lies.

### False affordances (imply function that doesn’t exist)
- Filters, MoreHoriz menus, bottom tabs beyond Telemetry, Fullscreen, “Documents”, “AI summary”.
- Create work order / Open incident exist; most chrome around them does not.

### Should be merged
- Hero + twin head + facility crumb → **one WorkspaceHeader / breadcrumb**.
- Sort + Filters + Group → **Saved views + filter chip bar**.
- Inspector prediction + recommendation + actions → **Decision / Next action rail** (one CTA max).
- Canvas footer sync age → shell SyncIndicator.

### Should disappear entirely
- Marketing hero on Assets.
- Decorative twin illustration as the “product”.
- Empty bottom tabs until backed by data.
- Hardcoded “4 sec ago”.
- Orbit empty animation as primary empty state.
- Duplicate “View forecast” buttons.
- Non-functional Filters / More menus (or make them real — until then, remove).

**Verdict:** Today’s Assets page is a **three-column demo dashboard with a poster twin**. It is not an industrial operating surface.

---

## Part B — Purpose

### Primary users
1. **Control room operator** (shift) — detect, localize, decide containment.
2. **Reliability / maintenance planner** — condition → work order.
3. **Process engineer** (secondary) — relationships, history, simulation.
4. **AI investigation consumer** — verify agent claims against twin + tags (not a separate mental model).

### Primary workflows
1. Scan facility → find abnormal unit → select equipment → confirm signals → open incident or create WO.
2. From incident/investigation → land on same asset in twin with selection preserved.
3. From forecast → stage maintenance draft without leaving asset context.
4. Bookmark critical trains for shift handover.

### Primary decisions
- Is this asset **safe to run / watch / intervene**?
- Is the alarm **process, equipment, or sensor**?
- Do I **acknowledge, escalate to incident, or schedule maintenance**?
- Which **downstream units** are exposed?

### Operator goals
- Orient in **&lt;10 seconds**.
- Never lose facility/unit/asset context.
- See **where** on the process before reading a table.
- One primary next action.

### AI goals
- Surfacing **why** (evidence + confidence + provenance) next to the object — never a floating chatbot as the main UI.
- Ranking explorer and twin overlays by **modelled risk**, not decoration.
- Drafting WO / investigation links with full audit trail.

---

## Part C — Workspace layout (complete)

Reference layout family: **ExplorerLayout** (Foundry Ontology explorer + PI Vision canvas + Forge asset pane). Canonical geometry is locked in [Design QA](#design-qa-lock-must-pass-before-build) and [DESIGN_SYSTEM.md § ExplorerLayout](./DESIGN_SYSTEM.md#explorerlayout-assets--forecast).

```mermaid
flowchart TB
  subgraph shell [ApplicationShell]
    WH[WorkspaceHeader_breadcrumbs_scope_sync]
    CB[CommandBar_overlay]
    Dock[Dock]
    WP[WorkspacePanel_audit_notifications]
    AS[AuditSpine]
  end
  subgraph assets [AssetsWorkspace]
    TB[AssetToolbar_savedViews_layers]
    subgraph body [Body_three_panes]
      EX[AssetExplorer_240to260]
      TW[DigitalTwin_flex_primary]
      OI[ObjectInspector_320_collapsible]
    end
    BW[BottomWorkspace_SignalPanel_collapsible]
  end
  WH --> TB
  TB --> body
  body --> BW
  AS --- assets
```

### Regions (every region specified)

| Region | Purpose | Priority | Width | Collapse | Sticky | Scroll | Keyboard | Interactions |
|--------|---------|----------|-------|----------|--------|--------|----------|--------------|
| **Context breadcrumbs** | Facility › Assets › Unit › Asset › Tag | P0 | full | never | in header | no | crumb activate | click crumb = navigate + preserve selection |
| **Top toolbar (Asset)** | Saved view, layer toggles, search scope, create WO | P0 | full; **40px** one row | never | under header | no | toolbar tab stop | change view = explorer+twin+overlays update together |
| **Explorer** | Hierarchical find + queues | P0 | **240–260px** max; &lt;1024 as tab | to icons+rail 64px | pane header sticky | **independent** | list arrows; Enter select | select = in-place; pin/favorite; open incident badge |
| **Digital Twin** | Primary spatial truth | **P0 primary** | `1fr` (**≥55%** content width) | never on desktop; mobile tab | toolbar sticky | pan/zoom canvas; no page scroll | focus canvas; arrows nudge selection among neighbors | click node/tag = select; right-click context; layer toggles |
| **Object Inspector** | Object dossier | P0 | **320px** default | to **0** with `]`; peek optional | Identity sticky; CTA sticky bottom | **independent** | first actionable after select | section accordions; links navigate with ID |
| **Bottom workspace** | Time-series & related records | P1 | full under twin+inspector or under all three | height **0 / 28% / 45%** (`Ctrl+B`); default **28%** | tab bar sticky | **independent** horizontal tabs + chart scroll | tab list arrows | tab change does **not** clear selection |
| **Command bar** | Global go-to asset/tag/incident | P0 | modal | overlay | — | list | ⌘K | result → Assets + select |
| **Audit spine** | Last decisions | P1 | full 32px | never | bottom sticky | horizontal | ⌘⇧A | click → related object |
| **Workspace panel** | Audit/notifications — **not** object context | P2 | 400px drawer | ⌘J | — | yes | focus trap | never duplicates ObjectInspector |

**Rule:** Page itself does not scroll (`overflow: hidden` on Assets). Only Explorer, Twin viewport, Inspector, Bottom pane scroll independently (XHQ / Foundry pattern).

---

## Part D — Digital Twin (answers + design)

Must answer continuously on-canvas:

| Question | Twin encoding |
|----------|----------------|
| **What is happening?** | Live tag values on selected train; streaming spark at node; alarm badges |
| **Why?** | On select: causal strip (“deviation vs baseline”, linked agent finding chip) — detail in Inspector/Bottom |
| **Where?** | Process flow position + unit highlight + minimap |
| **How severe?** | Risk heatmap fill + alarm severity ring (critical pulse 400ms only) |
| **What should I do?** | Single Primary CTA on twin chrome + Inspector actions |

### Twin capabilities (required)
- **Process flow** schematic per unit (P&ID-lite): vessels, pumps, exchangers, lines with flow direction.
- **Animated telemetry** on edges (velocity tied to flow tag) and node fill (health/risk).
- **Equipment selection** — single select; multi-select later for compare (phase 6).
- **Heatmaps** — risk / health / deviation modes (mutually exclusive layer).
- **Alarm overlays** — unacked / acked states from incident bus.
- **Risk overlays** — model score 0–100 banded.
- **Sensor overlays** — show/hide TagOverlay pins.
- **Pipeline flow** — directional particles; stop/slow on blocked path.
- **Status animation** — only critical/attention dots (Interaction Model animation rules).
- **Context menus** — Open incident, View forecast, Create WO, Pin, Copy tag, Show in explorer.
- **Selection** — explorer row + inspector + bottom series + breadcrumb object crumb update **together**.
- **Zoom / pan** — wheel + space-drag; fit-to-unit; fit-to-selection.
- **Minimap** — corner overview; click to pan.
- **Layers** — Process / Risk / Alarms / Sensors / Maintenance windows (checkboxes in toolbar).
- **Tag overlays** — PI Vision-style; click tag selects asset or focuses Bottom Telemetry.
- **Unit-scoped topology** — hundreds of nodes max on canvas; never 10k equipment glyphs at once.

**Remove:** static decorative SVG that isn’t a topology model.

Empty twin copy: **“Select a critical asset or click a unit.”**

---

## Part E — Object Inspector

Ordered sections (always this order). See also [DESIGN_SYSTEM.md — ObjectInspector sections (asset)](./DESIGN_SYSTEM.md#objectinspector-sections-asset).

| # | Section | Default |
|---|---------|---------|
| 1 | **Identity** — name, tag, class, location path, ProvenanceBadge | **Expanded** |
| 2 | **Current health** — StatusBadge, RiskBadge, HealthRing, last inspection | **Expanded** |
| 3 | **Signals** — Sparkline + top 3 SignalCards (threshold-aware) | **Expanded** |
| 4 | **Linked incidents** — open cases chips → Incident Center | Collapsed |
| 5 | **Forecast** — RUL / failure probability + deep link | Collapsed |
| 6 | **Maintenance** — open/draft WOs + Create WO | Collapsed |
| 7 | **Knowledge** — procedures / similar past events | Collapsed |
| 8 | **Documents** — controlled docs count + open | Collapsed |
| 9 | **Operator notes** — shift notes (persisted) | Collapsed |
| 10 | **AI recommendations** — text + confidence + “Open investigation” (lineage) | Collapsed |

**One PrimaryCTA** visible (sticky at bottom of inspector): context-dependent — `Open incident` | `Create work order` | `Acknowledge watch`.

---

## Part F — Bottom Workspace tabs

Keep **few live tabs**; hide empty.

| Tab | Role | Default |
|-----|------|---------|
| **Telemetry** | Historian for selected tags | **Always on** |
| **History** | State changes, acknowledgements | On |
| **Incidents** | Cases for this asset | On if count &gt; 0 |
| **Forecast** | Curve for selection | On when forecast data exists |
| **Maintenance** | WO timeline | On when WOs exist |
| **Relationships** | Upstream/downstream graph | On |
| **Knowledge** | Procedures / similar | Lazy |
| **Documents** | Files | Lazy |
| **Simulation** | What-if (shares Forecast scenario model) | Phase 6 |

**Remove as permanent chrome:** “AI summary” as its own tab (fold into Inspector AI + Investigation).

---

## Part G — Asset Explorer redesign

Replace flat list with **ontology tree + smart queues** (Azure Industrial / Foundry):

```
Search (tag, name, area)
Saved views: [Shift Critical] [My Pins] [Open Alarms] [Unit: Crude]
────────────────────────────────
▾ Favorites
▾ Critical now (risk≥threshold or open incident)
▾ Open incidents (asset chips)
▾ Recent (session)
────────────────────────────────
▾ Facility
   ▾ Area / Unit
      ▾ System
         Equipment (status dot, health, incident pip)
```

- **Hierarchy** — Facility → Area → Unit → System → Asset (data-driven).
- **Grouping** — saved view defines group key; not a random toggle.
- **Favorites / bookmarks** — local + server pin (`favorites.assetIds`).
- **Critical assets** — always above tree when non-empty.
- **Recent** — last 10 selections (`recent.assetIds`).
- **Open incidents** — queue jumping into twin selection.
- **Search** — indexed / server-backed at fleet scale; Enter selects first match + fits twin.
- **Filtering** — severity, type, health band, has-incident (FilterChipBar).
- **Saved views** — named filter + layer + unit camera presets (`ui.savedViews` / `ui.activeSavedViewId`).
- **Collapse rules** — expand path to selection; collapse siblings; remember per view.
- **Bookmarks** — same as favorites; appear in CommandBar.
- **Scale** — virtualized tree; default view = Critical + Open incidents + Recent + Favorites; hierarchy lazy by unit; “show all” is explicit.

---

## Part H — Interaction: click an asset

Exact coupling (no mental context change):

| Surface | Update |
|---------|--------|
| **Explorer** | Row selected; ancestors expanded; others dimmed optional |
| **Twin** | Node selected ring; camera ease to node 200ms; tag overlay for asset; neighbors remain visible |
| **Inspector** | Crossfade 200ms to sections for that ID (default expanded set only) |
| **Telemetry (Bottom)** | Series swap to asset’s primary tags; brush preserved if same unit |
| **Breadcrumbs** | `… › Assets › {Unit} › {Asset}` |
| **Audit** | No new entry (selection ≠ decision) |
| **Keyboard focus** | Moves to Inspector first actionable (or stays in explorer if arrow-navigating) |

Click **tag** on twin: select owning asset + Bottom focuses that tag.  
Click **alarm badge**: select asset + Bottom → Incidents + optional navigate to case (modifier).  
**Right-click** asset: context menu only — no route change.

---

## Part I — Challenge existing widgets (dispose / move / merge)

| Current | Action |
|---------|--------|
| Product hero | **Remove** from Assets |
| Twin marketing title block | **Remove**; use WorkspaceHeader |
| Filters dead button | **Remove** or replace with real FilterChipBar |
| Sort-only dropdown | **Merge** into Saved views |
| Decorative SVG twin | **Replace** with topology twin |
| Canvas footer stats | **Move** to SyncIndicator / toolbar |
| 8 empty bottom tabs | **Remove** until data; start with Telemetry+History+Incidents |
| Duplicate forecast buttons | **Merge** to one CTA |
| Inspector 6 flat metrics | **Merge** into Signals (threshold SignalCards) |
| Hardcoded sync copy | **Remove** |
| MoreHoriz noop | **Remove** |

---

## Part J — Deliverables

### 1. Wireframe specification (desktop)

```
┌─ Shell header: scope | breadcrumbs | sync | AI status | ⌘K ─────────────┐
├─ Asset toolbar 40px: SavedView | Layers[Process Risk Alarms Sensors] | Fit | WO ─┤
├─ Explorer ≤260 ─┬─ Twin (≥55% width, minimap, overlays) ──┬─ Inspector 320 ─┤
│ queues+tree     │ process flow + selection + tags         │ 1–3 + PrimaryCTA│
│ virtualized     │                                         │ accordions 4–10 │
├─────────────────┴──────────────────┬──────────────────────┴────────────────┤
│ Bottom default 28%: [Telemetry|History|Incidents|…]  chart/table           │
├────────────────────────────────────────────────────────────────────────────┤
│ AuditSpine ────────────────────────────────────────────────────── Dock FAB │
└────────────────────────────────────────────────────────────────────────────┘
```

Mobile &lt;1024: tabs **Explorer | Twin | Inspector**; Bottom as sheet.

### 2. Information hierarchy
1. Facility scope + selected object path  
2. Twin spatial state (what/where/severity)  
3. Explorer queues (what needs me)  
4. Inspector identity + health + next action  
5. Bottom time evidence  
6. Audit / notifications  

### 3. Interaction flow
Scan twin overlays → select → confirm signals in Bottom → PrimaryCTA (incident/WO/ack) → AuditSpine entry on decision only.

### 4. Component list (catalog-aligned)
WorkspaceHeader, ScopeSwitcher, SyncIndicator, Toolbar, FilterChipBar, SavedViewSelect, AssetTree, AssetTreeNode, SmartQueue (Critical/Recent/Incidents), ProcessSchematic, TwinNode, TagOverlay, LayerToggleBar, MiniMap, ObjectInspector, SectionHeader, StatusBadge, RiskBadge, HealthRing, SignalCard, Sparkline, ProvenanceBadge, PrimaryCTA, SignalPanel (Bottom), CommandBar, AuditSpine, WorkspacePanel, Dock, ContextMenu, EmptyState.

### 5. Layout diagram
See mermaid in Part C; geometry per Design QA lock below.

### 6. Implementation phases

| Phase | Scope |
|-------|--------|
| **0 Contract** | This document + ObjectContext field freeze + DESIGN_SYSTEM cross-links |
| **1 Chrome** | Kill hero; Asset toolbar; pane scroll model; real FilterChipBar |
| **2 Explorer** | Hierarchy + Critical/Recent/Favorites/Open incidents + saved views + virtualization |
| **3 Twin** | Topology-bound schematic, layers, minimap, tag overlays, selection camera |
| **4 Inspector** | Full section model; single PrimaryCTA; notes |
| **5 Bottom** | Telemetry+History+Incidents wired; hide empty tabs |
| **6 Polish** | Context menus, bookmarks in ⌘K, Simulation tab, multi-select compare |

---

## Design principles (non-negotiable)
- Twin is the **primary workspace**, not a chart beside a list.
- No page scroll; pane scroll only.
- No false affordances.
- Selection never clears on tab change.
- AI explains on the object — it does not replace the twin.
- Feels like **Palantir + PI Vision**: ontology left, living process center, dossier right, historian below.

---

## Design QA lock (must pass before build)

### 1. Is the Digital Twin big enough?
**Lock:** Twin ≥ **55%** content width and ≥ **50%** viewport height with Bottom collapsed. Default Bottom = **28%**. Explorer max **260px**. Inspector default **320px**, collapsible to **0** with `]`. Twin is the only pane that grows with the window.

### 2. Is there still wasted space?
**Lock:** No Assets hero. No twin marketing title. No canvas footer stats. Inspector defaults to Identity + Health + Signals + PrimaryCTA. Bottom tabs only when data exists (Telemetry always). Toolbar = one 40px row.

### 3. Does the explorer scale to 10,000 assets?
**Lock:** Virtualized tree. Default = Critical + Open incidents + Recent + Favorites. Hierarchy lazy by unit. Search indexed (not client-filter of 10k). Twin is unit-scoped.

### 4. Is the inspector too tall?
**Lock:** Sections 4–10 accordion closed by default. Internal scroll only. CTA sticky at inspector bottom.

### 5. Can an operator work without scrolling?
**Primary path without page scroll:** see risk on twin → click → read health + 3 signals → PrimaryCTA. Pane scroll allowed for explorer / deep inspector / historian. Body scroll **forbidden**.

### 6. Is the workflow obvious?
**Lock:** Critical queue above tree. Twin empty-state copy. One named PrimaryCTA. Breadcrumb always Unit › Asset.

### 7. Does it actually feel like an operating system?
**OS checklist (fail any → redesign):**
- [ ] Selection survives route changes
- [ ] ⌘K finds asset/tag; arrows drive explorer; `]` toggles inspector; `Ctrl+B` bottom
- [ ] Zero dead buttons
- [ ] Decisions write AuditSpine; selections do not
- [ ] Twin is unit topology + layers, not illustration
- [ ] No marketing hero on operational routes

### Geometry summary (1440×900 reference)

| Pane | Width | Height note |
|------|-------|-------------|
| Explorer | 240–260px | full body; virtualized |
| Twin | flex ≥55% | ≥50% vh with Bottom at 28% or collapsed |
| Inspector | 320px (collapsible) | internal scroll; CTA sticky bottom |
| Bottom | full | default 28%, toggle 0/28/45 |
| Page | — | **overflow: hidden** |

---

## ObjectContext fields (Assets) — see OBJECT_CONTEXT.md

Frozen for Phase 0+: `favorites.assetIds`, `recent.assetIds`, `ui.savedViews`, `ui.activeSavedViewId`, `ui.inspectorCollapsed`, `ui.bottomWorkspaceHeight`, `ui.twinLayers`, `ui.twinCamera`, `notes.byAssetId`. Full schema in [OBJECT_CONTEXT.md](./OBJECT_CONTEXT.md#assets-workspace-extensions-phase-0-freeze).
