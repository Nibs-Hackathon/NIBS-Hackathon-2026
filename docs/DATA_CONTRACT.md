# RigOS Data Contract

**Status:** Epic 0  
**Source of truth (live):** `GET /api/operations/live` + `WS /ws` snapshot  
**Related:** [OBJECT_CONTEXT.md](./OBJECT_CONTEXT.md), [OPERATING_MODEL.md](./OPERATING_MODEL.md)

---

## Principles

1. Pages never read raw snapshot shape ad hoc — Epic 3 introduces **data adapters** per workspace.  
2. Canonical IDs are stable across workspaces.  
3. Provenance is honest: if unknown, default to `estimated`, never blank.  
4. No fabricated telemetry or forecasts when data is absent (see Operating Model).

---

## Snapshot top-level keys

| Key | Type | Used by |
|-----|------|---------|
| `generated_at` | ISO string | SyncIndicator, stale detection |
| `dashboard` | object | Command Center OperationsStrip |
| `assets` | array | Assets, Mission Control, Forecast, scope filter |
| `refineries` | array | Mission Control portfolio / UnitRiskMap |
| `telemetry_by_refinery` | array | Sparklines by site |
| `telemetry` | object | Focused stream (primary asset) |
| `critical_asset_telemetry` | array | Twin, Forecast, SignalPanel |
| `critical_incidents` | array | DecisionQueue highlight |
| `audit_logs` | array | Incident Center, AuditSpine (read-only Epic 3) |
| `investigation` | object | Investigation workspace |
| `ai_activity` | array | Optional agent activity |
| `maintenance` | object `{ tasks }` | Kanban |
| `predicted_failures` | array | Forecasting watchlist |
| `notifications` | array | WorkspacePanel inbox |
| `reports` | array | Executive |
| `revenue_projection` | object | Mission Control sparkline (modelled value) |

---

## Canonical IDs (A4)

| Object | Canonical field | Notes |
|--------|-----------------|-------|
| Asset | `asset.id` | Always string/uuid; required for twin / forecast / WO |
| Incident | `incident.id` (from `audit_logs` / `critical_incidents`) | Same ID for Investigation ↔ Incident links |
| Investigation | `investigation` is bound to active incident via stages / incident fields on audits | Prefer `audit_logs[0].id` or investigation’s linked incident when present |
| Work order | `task.id` in `maintenance.tasks` | Synthesize stable client id if missing (Epic 3 adapter) |
| Report | `report.id` | Fallback index only for UI key, not navigation |

**Cross-link rule:** Investigation and Incident Center always share `selection.incidentId` = `audit_logs[].id`.

---

## Provenance (A2)

### Values

| Value | Meaning |
|-------|---------|
| `live` | Verified telemetry / health from current snapshot stream |
| `estimated` | Modelled, projected, or inferred (e.g. revenue projection, sparse forecast) |
| `stale` | Last update age &gt; 30s or WS disconnected with retained snapshot |

### Mapping rules (adapters)

| Field / widget | Provenance rule |
|----------------|-----------------|
| Asset health from runtime | `live` when present |
| Telemetry readings | `live` when `readings.length > 0`; else omit / empty |
| Forecast `projected_health` | `estimated` when `forecast_available`; hide chart if unavailable |
| `revenue_projection` | Always `estimated` (`kind: modelled_production_value`) |
| KPI with no update for 30s | `stale` |
| Missing field | Component shows ProvenanceBadge `estimated` |

Backend may later add explicit `provenance` on metrics. Until then, **adapters compute** provenance; UI never invents “live” for modelled series.

---

## Page adapter shapes (Epic 3)

Adapters live under e.g. `frontend/src/adapters/` — thin pure functions.

### Command Center

```text
{
  strip: { fleetHealth, openIncidents, assetsOnline, agentsActive, cta },
  units: UnitRiskMapNode[],
  queue: DecisionQueueItem[],
  sparklines: { values, provenance, label },
  audit: AuditEvent[],
}
```

### Assets

```text
{
  tree: AssetNode[],
  selected: Asset | null,
  telemetry: Stream | null,
  linkedIncident: Incident | null,
}
```

### Incidents

```text
{
  queue: Incident[],
  selected: Incident | null,
  timeline: Event[],
  dossier: { evidence, recommendation, confidence },
}
```

### Investigation

```text
{
  incidentId,
  stages: AgentStage[],
  selectedStageId,
  evidence: EvidenceItem[],
  recommendation,
}
```

### Maintenance

```text
{
  columns: { Backlog|Ready|Scheduled|InProgress|Complete: WorkOrder[] },
  selected: WorkOrder | null,
  draft: WorkOrderDraft | null,
}
```

### Forecasting

```text
{
  watchlist: PredictedAsset[],
  selected: PredictedAsset | null,
  chart: { series, threshold, confidenceBand, provenance },
}
```

### Reports

```text
{
  index: Report[],
  selected: Report | null,
  approval: ApprovalState,
}
```

---

## Operator actions (A3 / A8)

| Action | Endpoint | Epic |
|--------|----------|------|
| Record decision | `POST /api/operator-actions` | Wired Investigation today; Epic 5 expands rationale + audit |
| Mark notifications read | `POST /api/notifications/read` | Shell |
| Executive approve | Same operator-actions or reports API | **Epic 5** — not Epic 3 local state |
| Export audit | TBD read endpoint | Epic 5 |

Immutable append-only log: verify `ActionDB` / audit persistence before Epic 5. Epic 3 AuditSpine uses `audit_logs` slice only.

---

## Stale detection

| Signal | Condition |
|--------|-----------|
| `generated_at` age | `Date.now() - generated_at > 30_000` → stale |
| `OperationsContext.connected === false` | SyncIndicator reconnecting; KPIs may show `stale` |
| Empty arrays | EmptyState, not fabricated rows |

---

## Exit criteria (Epic 0)

- [x] Snapshot keys documented  
- [x] Canonical IDs documented  
- [x] Provenance defaults documented  
- [x] Scope = client-side filter (see Object Context)  
- [ ] Adapter modules implemented — Epic 3 (undone / not shipping)  
