# RigOS Operating Model

## What RigOS demonstrates

RigOS is an AI operations-control layer for industrial facilities. It consumes
simulated telemetry in this hackathon build, detects injected abnormal
conditions, coordinates a specialised multi-agent investigation, records an
operator decision, creates maintenance follow-up, and retains an audit trail.

The end-to-end control loop is:

1. The facility simulator emits asset-specific telemetry.
2. A timed or API-triggered fault produces an incident event.
3. The MAO orchestrator selects a domain workflow and runs sensor, safety,
   diagnostic, knowledge, maintenance, planning, prediction, notification,
   and reporting agents as applicable.
4. Evidence, recommendations, confidence, and execution results are stored
   against the incident.
5. The Operations Center shows the current field condition separately from
   the AI workflow status.
6. An operator can approve, reject, escalate, or request more evidence. This
   records an audit action only for board decisions.
7. On CRITICAL temperature/pressure (and related) breaches, the Safety agent
   may shut off the specific simulated pump/tank/asset at its refinery, and the
   Maintenance agent may auto-create work orders for restart clearance. These
   are simulated facility commands with ActionDB audit rows — not physical
   industrial I/O.
8. When telemetry normalizes (or audited field work completes after a shutoff),
   the simulator resolves the physical incident and stores final health plus
   the true resolution duration.

## Data provenance

| Product area | Source of truth | Important interpretation |
| --- | --- | --- |
| Asset health | Shared runtime health engine and telemetry history | Current modelled condition, not a certified integrity measurement. |
| Incident ledger | PostgreSQL `incidents` when available; runtime event history only during a database outage | `under_investigation` means field condition is still active. |
| AI investigation | Latest MAO execution report and its agent results | Agent completion does not mean the field incident is resolved. |
| Maintenance | Maintenance-agent work orders plus planning metadata | `Scheduled` is a modelled plan; no technician dispatch is performed. |
| Health forecast | Observed health slope from verified simulator telemetry | A forecast is withheld when history is insufficient. |
| Production value | Health/availability model and documented revenue assumptions | It is modelled operating value, never booked revenue. |

## Operational guardrails

- No endpoint fabricates telemetry or a forecast when verified data is absent.
- WebSocket loss retains the last verified snapshot while REST polling refreshes
  the view independently.
- An AI report is an investigation outcome, not a physical-resolution signal.
- Operator decisions are auditable and non-actuating.
- The platform must show degraded/unavailable state rather than silently
  presenting an empty facility as healthy.

## Hackathon scope and future production work

This is a production-quality prototype, not a certified industrial control
system. A field deployment requires authenticated users and roles, real
historian/SCADA integration, model validation against historical failures,
alarm-management integration, security review, observability, and safety
approval. RigOS is deliberately designed as a decision-support layer while
those integrations are introduced.
