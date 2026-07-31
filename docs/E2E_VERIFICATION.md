# Phase 7 — E2E verification

Run after starting a **single** backend instance on port 8080:

```bash
npm run backend          # terminal 1
python backend/scripts/e2e_verify.py   # terminal 2
cd frontend && npm run build           # frontend compile check
cd backend && python -m pytest tests -q
```

## Automated API checklist (`e2e_verify.py`)

| Check | Endpoint / surface |
|-------|-------------------|
| Env `DATABASE_URL` + Gemini keys | `backend/.env` |
| API health | `GET /api/health` |
| Database health | `GET /api/health/database` |
| Operations spine | `GET /api/operations/live` (assets, refineries, audits, operator_actions) |
| Digital twin | `GET /api/twin-assets` |
| Predictions + stress | `GET /api/predictions/{id}?stress=` |
| Telemetry replay | `GET /api/telemetry/{id}?since=&until=` |
| Maintenance | `GET /api/maintenance` |
| Work order → ActionDB | `POST /api/maintenance/work-orders` + approve |
| Operator decisions | `POST /api/operator-actions` + `GET /api/operator-actions` |
| Incident audit detail | `GET /api/incidents/audit/{id}` |
| Executive reports + export | `GET /api/reports` + export |
| Knowledge search (RAG) | `GET /api/knowledge/search?q=` |
| Assistant with context | `POST /api/assistant/query` |
| Agent registry | `GET /api/agents` |
| Incident simulator | `POST /api/incidents/pressure-spike` |

## Latest run (2026-07-27)

| Area | Result | Notes |
|------|--------|-------|
| Backend unit tests | **PASS** | 5/5 (`pytest tests`) |
| Frontend build | **PASS** | `vite build` succeeded |
| Env Gemini keys | **PASS** | 7 `GEMINI_API_KEY_*` entries |
| Env `DATABASE_URL` | **WARN** | `tcp://` Pinggy tunnel — needs `POSTGRES_PASSWORD` (and optionally `POSTGRES_USER`, `POSTGRES_DB`) |
| API health | **WARN** | `real_services: false` when DB auth fails |
| Database health | **FAIL** | `fe_sendauth: no password supplied` |
| Operations live | **FAIL** | HTTP 503 until DB connects |

### Fix for database blocker

Your `DATABASE_URL` is a TCP tunnel host. Add credentials to `backend/.env`:

```env
DATABASE_URL=tcp://your-tunnel-host:port
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_DB=rigos
```

Or use a full URL:

```env
DATABASE_URL=postgresql://postgres:password@your-tunnel-host:port/rigos
```

Then restart the backend and re-run `python backend/scripts/e2e_verify.py`.

### Other fixes applied during verification

- **Windows startup**: `run.py` forces UTF-8 stdout so emoji logs do not crash import.
- **TCP tunnels**: `database/connection.py` maps `tcp://` URLs to `postgresql+psycopg2://` when credentials are present.

## Manual UI smoke (Playwright)

```bash
cd frontend && npm run test:e2e
```

Covers workspace route mounting (no live backend required for hero chrome).
