# RigOS

AI operations-control layer for industrial facilities. This hackathon build runs a multi-refinery simulator, detects injected faults, runs a specialised multi-agent investigation (MAO), can shut off the affected simulated asset and plan maintenance, and keeps an auditable operator trail in the Operations Center.

This is a production-quality prototype for decision support. It is not a certified industrial control system and does not command physical equipment.

## What you get

| Surface | Job |
| --- | --- |
| Mission Control | Live facility posture, incidents, revenue impact |
| Assets | Explorer + digital twin + inspector (`ExplorerLayout`) |
| Incidents / AI Investigation | Evidence, agent stages, operator decisions |
| Maintenance | Kanban work-order queue (`KanbanLayout`) |
| Reports | Executive briefing (`ExecutiveLayout`) |
| Notifications | Toast + inbox: `asset · refinery` title, event detail |

### Control loop

1. Simulator emits asset telemetry.
2. Timed or API-injected fault creates an incident.
3. MAO picks a workflow (pressure, temperature, etc.) and runs sensor → safety → diagnostic → maintenance → planning → … → report.
4. On pressure / temperature / gas hard trips, the Safety agent can shut off that specific pump/tank/asset at its refinery (simulated `Offline`), and Maintenance can auto-create work orders for restart clearance.
5. Operators approve/reject/escalate with rationale; field-work completion clears agent isolation and restores modelled running status.
6. When telemetry normalizes, the simulator resolves the physical incident with real duration.

Details: [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md).

## Stack

- **Backend:** FastAPI, MAO kernel, facility simulator, SQLAlchemy / PostgreSQL (optional), Gemini (optional)
- **Frontend:** React + Vite, MUI, RigOS design system + layout primitives
- **Realtime:** WebSocket snapshots + REST polling fallback

## Quick start

### Prerequisites

- Python 3.11+ recommended
- Node.js 20+
- Optional: PostgreSQL + Gemini API keys for full persistence / LLM paths

### 1. Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows: copy
# or: cp .env.example .env
```

For a zero-dependency local demo (no Postgres / Gemini):

```env
LOCAL_DEMO_MODE=true
```

Then:

```bash
# from repo root
npm run backend

# or
cd backend && python run.py
```

API defaults to [http://127.0.0.1:8080](http://127.0.0.1:8080) (`PORT` overrides). Set `RELOAD=true` for uvicorn auto-reload.

### 2. Frontend

```bash
# from repo root
npm install --prefix frontend
npm run dev
```

UI defaults to [http://127.0.0.1:3000](http://127.0.0.1:3000) and proxies API/WebSocket to `:8080`.

### 3. Optional full stack

Copy `backend/.env.example` → `backend/.env` and set:

- `DATABASE_URL` (PostgreSQL)
- `GEMINI_API_KEYS` (comma-separated pool)

See comments in `.env.example` for simulator cadence knobs (`RIGOS_*`).

## Demo path

1. Start backend + frontend.
2. Open Incidents (or Mission Control) and inject a pressure or temperature fault.
3. Watch agents investigate; on hard trip the asset goes **Offline** and a maintenance work order appears.
4. Review **AGENT ACTIONS EXECUTED** on the incident, then approve / complete the WO to clear isolation.
5. Check Assets, Maintenance kanban, and Executive Reports for the same incident trail.

## Scripts

| Command | Purpose |
| --- | --- |
| `npm run dev` | Frontend Vite dev server |
| `npm run backend` | FastAPI + simulator |
| `npm run build` | Production frontend build |
| `npm run lint` | Frontend ESLint |
| `npm run verify:e2e` | Backend e2e verification script |
| `cd backend && python -m pytest` | Backend tests |

## Repository map

```
backend/
  agents/          # Sensor, safety, diagnostic, maintenance, …
  api/             # FastAPI routes + adapters
  mao/             # Kernel, workflows, orchestration
  simulator/       # Facility telemetry + faults
  services/        # Runtime, actuation, notifications, …
frontend/
  src/redesign/    # Operator product shell + views
  src/design-system/
docs/              # Operating model, data contract, design system
```

## Documentation

- [Operating model](docs/OPERATING_MODEL.md)
- [Data contract](docs/DATA_CONTRACT.md)
- [Design system](docs/DESIGN_SYSTEM.md)
- [Simulation & performance](docs/SIMULATION_AND_PERFORMANCE.md)
- [E2E verification](docs/E2E_VERIFICATION.md)

## Guardrails

- Simulated commands and audit rows only — no physical I/O.
- Missing telemetry / forecasts stay unavailable rather than invented.
- AI report complete ≠ field incident resolved.
- Modelled production value is not booked revenue.

## License / hackathon

Built for the RigOS hackathon 2026 track. Treat as demo software unless your team adds auth, SCADA/historian integration, safety certification, and production hardening.
