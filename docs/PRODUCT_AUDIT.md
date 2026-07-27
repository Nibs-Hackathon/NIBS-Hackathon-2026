# RigOS Product Audit

**Role:** Lead Product Designer — operator-centric audit  
**Scope:** UX architecture only. No implementation commentary.  
**Design target:** [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md)

---

## Executive verdict

RigOS currently reads as a **cinematic operations demo**, not a **control-room instrument**. It prioritizes narrative hero typography, decorative live badges, and portfolio storytelling over the tight scan patterns operators use during incidents.

| Product | What they do well | Where RigOS falls short |
|---------|-------------------|-------------------------|
| **Palantir** | Object-centric investigation; entity + lineage | Context scattered; no persistent object identity across workspaces |
| **Bloomberg Terminal** | Scan density; keyboard-first; numbers over prose | KPIs buried under hero copy; marketing language in ops views |
| **Datadog** | Alert → trace → root cause in one flow | Incident, investigation, and twin split across three workspaces |
| **Grafana** | Time as primary axis | Time treated as decoration |
| **Azure Industrial** | Asset hierarchy drives navigation | Twin impressive but not the spine of navigation |

**Core diagnosis:** Optimizes for boardroom impressiveness over shift-handover survivability. An operator at 3 AM needs: *what changed, what broke, what to do, who decided* — in under 10 seconds.

### Cross-cutting failures

1. Hierarchy inversion — titles dominate; actionable state secondary  
2. Workflow fragmentation — Incident → Investigation → Twin → Maintenance = four context switches  
3. AI as theater — agent marquees show activity, not accountability  
4. Density mismatch — no Alert / Work / Brief tiers  
5. False affordances — filters, zoom, gantt, calendar imply unfinished capability  
6. Enterprise trust gap — no audit spine on every page  
7. Portfolio noise for single-site operators  

---

## Page audits

### 1. Command Center

| Field | Assessment |
|-------|------------|
| **Purpose** | Single-glance facility state: safe or not, what needs attention, where to go next |
| **Primary user** | Shift supervisor / control room operator |
| **Primary workflow** | Arrive → confirm nominal OR identify top incident → route to investigation or asset |
| **Primary visual focus** | Situation strip: “Is the plant safe right now?” |
| **Information hierarchy** | Current: hero → KPI → map → telemetry → AI → portfolio. **Wrong.** Situation must be row 1. |
| **Critical widgets** | Situation / OperationsStrip, open incident count, top incident, fleet health, UnitRiskMap |
| **Secondary widgets** | Projection sparkline, agent summary, maintenance backlog count |
| **Unused / remove** | Duplicate situation banners; decorative sweeps; portfolio when scoped to one site; AI summary prose; large hero typography; agent marquee |
| **Merge** | KPI + situation → OperationsStrip; map + nodes → UnitRiskMap |
| **Ideal layout** | MissionControlLayout |
| **Scores** | Efficiency 4/10 · AI 3/10 · Twin 5/10 · Enterprise 5/10 |

### 2. Assets (Digital Twin)

| Field | Assessment |
|-------|------------|
| **Purpose** | Navigate hierarchy, inspect condition, correlate telemetry with risk |
| **Primary user** | Reliability engineer / process operator |
| **Primary workflow** | Search/browse → twin + telemetry → threshold → escalate or schedule |
| **Primary visual focus** | Selected asset twin with live tag overlay |
| **Information hierarchy** | Explorer \| twin \| inspector buried — structure OK, emphasis wrong |
| **Critical widgets** | Asset tree, ProcessSchematic + tags, health/risk, 4h trend, linked incident |
| **Secondary widgets** | Sort/filter, gauges, related work orders |
| **Unused / remove** | Zoom without spatial model; empty filter button; marketing subtitle; redundant brief when ObjectInspector exists |
| **Merge** | Row + brief → ObjectInspector always on; bottom tabs → SignalPanel |
| **Ideal layout** | ExplorerLayout (`canvasVariant="twin"`) — full contract: [ASSETS_WORKSPACE_REDESIGN.md](./ASSETS_WORKSPACE_REDESIGN.md) |
| **Scores** | Efficiency 6/10 · AI 4/10 · Twin 7/10 · Enterprise 6/10 |

### 3. Incident Center

| Field | Assessment |
|-------|------------|
| **Purpose** | Triage cases, timeline, evidence, operator decisions |
| **Primary user** | Operations supervisor / incident commander |
| **Primary workflow** | Scan queue → select → timeline → evidence → decide → log |
| **Primary visual focus** | Selected incident timeline with decision points |
| **Information hierarchy** | Queue \| Timeline \| Evidence — correct topology, weak prioritization |
| **Critical widgets** | Priority queue, timeline, evidence, DecisionBar |
| **Secondary widgets** | Search, severity filter, confidence, impact |
| **Unused / remove** | Decision log as button (should be persistent); bottom tabs duplicating timeline; decorative case ID |
| **Merge** | Evidence + recommendation → CaseDossier; filters → Toolbar |
| **Ideal layout** | IncidentLayout |
| **Scores** | Efficiency 7/10 · AI 6/10 · Twin 2/10 · Enterprise 7/10 |

### 4. AI Investigation

| Field | Assessment |
|-------|------------|
| **Purpose** | Observe multi-agent reasoning, validate, intervene before action |
| **Primary user** | Senior operator / AI oversight lead |
| **Primary workflow** | Monitor pipeline → expand stage → evidence → accept/modify/reject + rationale |
| **Primary visual focus** | Agent pipeline with current stage enlarged |
| **Information hierarchy** | Too many equal panels; pipeline + reasoning compete |
| **Critical widgets** | Pipeline, active agent detail, evidence chain, DecisionBar + rationale |
| **Secondary widgets** | Confidence, model version, elapsed time, linked incident |
| **Unused / remove** | Streaming badge; hero “watching the model” copy; duplicate confidence |
| **Merge** | Reasoning + evidence → TracePanel; stage click scrolls trace |
| **Ideal layout** | InvestigationLayout |
| **Scores** | Efficiency 5/10 · AI 8/10 · Twin 3/10 · Enterprise 6/10 |

### 5. Maintenance Planning

| Field | Assessment |
|-------|------------|
| **Purpose** | Prioritize work orders, schedule, balance downtime vs risk |
| **Primary user** | Maintenance planner / reliability coordinator |
| **Primary workflow** | Backlog by risk → schedule → assign → confirm window → complete |
| **Primary visual focus** | Risk-prioritized kanban |
| **Information hierarchy** | Fatal: four view tabs imply scheduling; only kanban is real |
| **Critical widgets** | Kanban, work order detail, cost/downtime, asset + forecast chip |
| **Secondary widgets** | Crew, parts, approval |
| **Unused / remove** | Calendar, timeline, gantt tabs until functional |
| **Merge** | Card + detail → ObjectInspector |
| **Ideal layout** | KanbanLayout (read-only board in Epic 3) |
| **Scores** | Efficiency 4/10 · AI 2/10 · Twin 4/10 · Enterprise 5/10 |

### 6. Forecasting

| Field | Assessment |
|-------|------------|
| **Purpose** | Degradation trajectories, what-if, preventive action |
| **Primary user** | Reliability engineer / planning analyst |
| **Primary workflow** | Watchlist → select → RUL curve → scenario → create work order |
| **Primary visual focus** | Forecast chart with confidence band and failure threshold |
| **Information hierarchy** | Good structure; watchlist narrow; time axis weak |
| **Critical widgets** | Watchlist, ForecastChart, RUL, ScenarioSlider, Create work order |
| **Secondary widgets** | History, model confidence, sensor attribution |
| **Unused / remove** | Modelled data labeled as live; decorative terminal chrome |
| **Merge** | What-if + chart → scenario canvas in ExplorerLayout |
| **Ideal layout** | ExplorerLayout (`canvasVariant="forecast"`) |
| **Scores** | Efficiency 7/10 · AI 5/10 · Twin 5/10 · Enterprise 6/10 |

### 7. Executive Reports

| Field | Assessment |
|-------|------------|
| **Purpose** | Leadership summary; approve capital or risk acceptance |
| **Primary user** | Plant manager / executive committee |
| **Primary workflow** | Select brief → review → appendix → approve/defer/escalate → distribute |
| **Primary visual focus** | Executive summary with decision status |
| **Information hierarchy** | Acceptable; presentation mode gimmick without projector workflow |
| **Critical widgets** | Brief, key metrics, risk acceptance, approval, appendix link |
| **Secondary widgets** | History, confidence, agent attribution |
| **Unused / remove** | Presentation mode → export; marketing kickers; duplicate CC metrics |
| **Merge** | List + brief master-detail |
| **Ideal layout** | ExecutiveLayout (AuditSpine hidden) |
| **Scores** | Efficiency 6/10 · AI 4/10 · Twin 1/10 · Enterprise 5/10 |

---

## Redesign roadmap (product)

| Phase | Focus |
|-------|-------|
| A | Control room foundation — OperationsStrip, AuditSpine, density tiers |
| B | Workflow unification — one Incident object, three lenses; honest Maintenance |
| C | AI accountability — Agent Trace, mandatory rationale, evidence lineage |
| D | Enterprise trust — handover, export, role stamps, provenance |
| E | Portfolio scale — scope switch, multi-site rollup |

Implementation epics: see plan Epics 0–6. Epic 0 freezes this contract; Epics 1–6 build it.
