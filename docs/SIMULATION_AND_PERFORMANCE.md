# Simulation and Performance Contract

## Automatic incident simulation

RigOS starts one bounded simulator thread with the backend. It warms telemetry,
then rotates incident scenarios across every instantiated refinery instead of
choosing randomly from the entire portfolio.

Default cadence:

- Telemetry tick: every 2 seconds
- Warm-up: 8 seconds
- First automatic incident: 5 seconds after warm-up
- First portfolio coverage pass: one refinery every 12 seconds
- Steady-state incidents: every 45–90 seconds
- Maximum simultaneous active incidents: 3

The first 16-facility coverage pass therefore begins producing evidence quickly
and targets every facility in roughly three minutes, excluding time spent in
the MAO workflow. Each incident still runs the real sensor, safety, diagnostic,
maintenance, planning, knowledge, prediction, notification, and report path.

Manual scenario buttons target an asset inside the currently selected facility.

## Runtime performance controls

- Health is calculated once per asset per simulation tick.
- Live telemetry remains in memory, capped at 100 readings per asset.
- Durable telemetry is sampled every fifth tick by default.
- PostgreSQL writes use batches of 1,000 rows.
- The PostgreSQL pool defaults to five base and five overflow connections.
- Runtime agent memory is capped at 1,000 entries.
- Operations snapshots are cached for four seconds and shared by REST and all
  WebSocket clients.
- WebSocket snapshots default to a five-second cadence.
- The globe renders at 48 FPS, or 30 FPS on lower-power devices, pauses when
  hidden/offscreen, and caps device pixel ratio.
- REST polling backs off while WebSocket delivery is healthy and pauses in
  hidden tabs.

All timings are configurable through the documented variables in
`backend/.env.example`.

## Honest empty states

Assets and telemetry exist for every instantiated refinery. Incidents,
investigations, maintenance work, and reports are event-driven. A facility may
legitimately show no records before its first automatic or manual scenario.
The UI displays automatic simulator state and its next target rather than
implying that simulation is disabled.
