# Frontend / Backend Connection Audit

Audit date: 2026-07-29

## Connected and used

| Capability | Frontend path | Backend contract | Status |
|---|---|---|---|
| Portfolio snapshot | `OperationsContext` → `ProductPage` and all workspaces | `GET /api/operations/live` | Connected; primary data contract |
| Live updates | `useWebSocket` | `WS /ws` through the Vite proxy | Connected with REST fallback and reconnect backoff |
| Facility selector and globe | `MissionControlOS`, `resourceAdapters` | `operations.refineries`, `telemetry_by_refinery` | Connected; strict facility scoping |
| Asset detail and telemetry | `AssetConsole`, investigation and incident views | `GET /api/assets/{id}`, `GET /api/telemetry/{id}` | Connected |
| Asset notes | `AssetConsole` | `GET/POST /api/assets/{id}/notes` | Connected; durable writes require PostgreSQL |
| Incident injection and audit | `IncidentManagement` | `POST /api/incidents/{type}`, `GET /api/incidents/audit/{id}` | Connected |
| Agent roster and metrics | `AIInvestigationOS` | `GET /api/agents`, `GET /api/agent-metrics` | Connected |
| Maintenance | Asset, forecast, and maintenance workspaces | `GET /api/maintenance`, work-order create/approve routes | Connected; durable writes require PostgreSQL |
| Forecasting | `ForecastTerminal` | `GET /api/predictions/{asset_id}` | Connected |
| Knowledge snippets | Asset and investigation inspectors | `GET /api/knowledge/search` | Connected to local corpus with optional vector retrieval |
| Knowledge catalog | Copilot and asset Documents section | `GET /api/knowledge/documents` | Connected; browsable without PostgreSQL or simulator readiness |
| Operations copilot | Assistant panels | `POST /api/assistant/query` | Connected; local retrieval plus Gemini response generation |
| Operator decisions | Accountability controls and executive reports | `POST /api/operator-actions` | Connected; durable writes require PostgreSQL |
| Notifications | `ProductShell` | `POST /api/notifications/read` | Connected |
| Executive reports | `ExecutiveBriefing` | `GET /api/reports`, report export route | Connected and incident-linked |
| Digital twin asset detail | `AssetConsole` | `GET /api/twin-assets` | Connected |

## Available backend contracts not directly called by the current product UI

These are not broken. The UI gets equivalent information from the aggregated
operations snapshot or a more specific detail route.

- `GET /api/assets`
- `GET /api/incidents`
- `GET /api/dashboard`
- `GET /api/agent-activity`
- `GET /api/incidents/audit`
- `GET /api/operator-actions`
- `GET /api/metadata`
- `GET /api/health/database`

## Issues corrected during this audit

1. Local/demo knowledge retrieval registered an empty store.
2. The fallback FAISS path did not match the checked-in index location.
3. Markdown and text files were ignored by the ingestion job.
4. A configured but empty or unavailable PostgreSQL/pgvector knowledge table could leave the
   UI with no documents.
5. Refinery objects and their assets were generated with different
   `refinery_id` values.
6. The runtime generated only a random subset of the geographic catalog.

## Remaining environment dependencies

- PostgreSQL is required for durable notes, operator decisions, work orders,
  reports, and database-backed vector search.
- Gemini credentials are required for generated conversational answers and
  embedding-backed search.
- The checked-in local refinery corpus remains searchable when either external
  dependency is unavailable.
- The backend was not listening on port 8080 during the final live check. Restart
  it with the project Python environment before validating the endpoint in-browser.
