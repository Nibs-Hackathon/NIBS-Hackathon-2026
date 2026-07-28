"""Phase 7 connectivity verification — run with backend on :8080.

Usage (from repo root):
  python backend/scripts/e2e_verify.py
  python backend/scripts/e2e_verify.py --base http://localhost:8080/api
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass
class Check:
    name: str
    status: str  # pass | fail | warn | skip
    detail: str = ""


@dataclass
class Report:
    checks: list[Check] = field(default_factory=list)

    def add(self, name: str, status: str, detail: str = "") -> None:
        self.checks.append(Check(name=name, status=status, detail=detail))

    def summary(self) -> tuple[int, int, int, int]:
        counts = {"pass": 0, "fail": 0, "warn": 0, "skip": 0}
        for check in self.checks:
            counts[check.status] = counts.get(check.status, 0) + 1
        return counts["pass"], counts["fail"], counts["warn"], counts["skip"]


def request_json(
    method: str,
    url: str,
    payload: dict | None = None,
    timeout: float = 30.0,
) -> tuple[int, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else None
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body else {"error": error.reason}
        except json.JSONDecodeError:
            parsed = {"error": body or error.reason}
        return error.code, parsed


def join(base: str, path: str) -> str:
    return f"{base.rstrip('/')}/{path.lstrip('/')}"


def verify_env(report: Report) -> None:
    from pathlib import Path
    from dotenv import load_dotenv

    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    raw = (os.getenv("DATABASE_URL") or "").strip()
    if not raw:
        report.add("Env DATABASE_URL", "fail", "Missing from backend/.env")
    elif raw.startswith("tcp://") and not os.getenv("POSTGRES_PASSWORD"):
        report.add(
            "Env DATABASE_URL",
            "warn",
            "tcp:// tunnel set but POSTGRES_PASSWORD missing — persistence may fail",
        )
    else:
        report.add("Env DATABASE_URL", "pass", f"scheme={raw.split('://')[0]}")

    gemini_keys = [k for k in os.environ if k.startswith("GEMINI_API_KEY")]
    report.add(
        "Env Gemini keys",
        "pass" if gemini_keys else "warn",
        f"{len(gemini_keys)} GEMINI_API_KEY_* entries",
    )


def verify(base: str) -> Report:
    report = Report()
    verify_env(report)
    state: dict[str, Any] = {}

    status, health = request_json("GET", join(base, "/health"))
    if status == 200 and health.get("real_services"):
        report.add("API health", "pass", f"real_services={health.get('real_services')}")
    elif status == 200:
        report.add("API health", "warn", "API up but real_services is false — check DATABASE_URL")
    else:
        report.add("API health", "fail", f"HTTP {status}: {health}")
        return report

    status, db_health = request_json("GET", join(base, "/health/database"))
    if status == 200 and db_health.get("ok"):
        report.add("Database health", "pass", db_health.get("message", "connected"))
        state["db_ok"] = True
    else:
        report.add("Database health", "fail", f"HTTP {status}: {db_health}")
        state["db_ok"] = False

    status, live = request_json("GET", join(base, "/operations/live"))
    if status != 200:
        report.add("Operations live snapshot", "fail", f"HTTP {status}")
        return report

    assets = live.get("assets") or []
    refineries = live.get("refineries") or []
    audit_logs = live.get("audit_logs") or []
    operator_actions = live.get("operator_actions") or []
    investigation = live.get("investigation") or {}
    report.add(
        "Operations live snapshot",
        "pass",
        f"{len(assets)} assets, {len(refineries)} refineries, {len(audit_logs)} audits",
    )
    if refineries:
        report.add("Facilities / refineries", "pass", refineries[0].get("name", "refinery present"))
    else:
        report.add("Facilities / refineries", "warn", "No refineries in live snapshot")

    if not assets:
        report.add("Asset spine", "fail", "No assets returned")
        return report

    asset_id = assets[0].get("id")
    state["asset_id"] = asset_id
    if audit_logs:
        state["incident_id"] = audit_logs[0].get("id")

    status, twin = request_json("GET", join(base, "/twin-assets"))
    twin_rows = twin if isinstance(twin, list) else twin.get("assets", []) if isinstance(twin, dict) else []
    report.add(
        "Digital twin",
        "pass" if status == 200 and twin_rows else "warn",
        f"HTTP {status}, {len(twin_rows)} twin rows",
    )

    status, prediction = request_json("GET", join(base, f"/predictions/{urllib.parse.quote(str(asset_id))}?stress=0.2"))
    if status == 200 and prediction.get("data_available", True):
        report.add("Health predictions + stress", "pass", f"asset={asset_id}")
    else:
        report.add("Health predictions + stress", "warn", f"HTTP {status}: {prediction}")

    since = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    until = datetime.now(timezone.utc).isoformat()
    status, telemetry = request_json(
        "GET",
        join(base, f"/telemetry/{urllib.parse.quote(str(asset_id))}?limit=10&since={urllib.parse.quote(since)}&until={urllib.parse.quote(until)}"),
    )
    telemetry_rows = telemetry if isinstance(telemetry, list) else []
    report.add(
        "Telemetry replay window",
        "pass" if status == 200 else "fail",
        f"HTTP {status}, {len(telemetry_rows)} readings",
    )

    status, maintenance = request_json("GET", join(base, "/maintenance"))
    tasks = (maintenance or {}).get("tasks", []) if isinstance(maintenance, dict) else []
    report.add("Maintenance plan", "pass" if status == 200 else "fail", f"{len(tasks)} tasks")

    wo_payload = {
        "asset_id": asset_id,
        "title": "E2E verification work order",
        "priority": "P2",
        "owner": "E2E verifier",
        "note": "Automated connectivity verification work order.",
    }
    status, wo = request_json("POST", join(base, "/maintenance/work-orders"), wo_payload)
    wo_id = (wo or {}).get("id") if isinstance(wo, dict) else None
    if status in (200, 201) and wo_id:
        report.add("Work order create → ActionDB", "pass", f"id={wo_id}")
        approve_status, approved = request_json(
            "POST",
            join(base, f"/maintenance/work-orders/{urllib.parse.quote(str(wo_id))}/approve"),
            {"operator": "E2E verifier", "note": "Approved during automated verification."},
        )
        report.add(
            "Work order approve",
            "pass" if approve_status in (200, 201) else "warn",
            f"HTTP {approve_status}: {approved}",
        )
    elif not state["db_ok"]:
        report.add("Work order create → ActionDB", "skip", "Database unavailable")
    else:
        report.add("Work order create → ActionDB", "fail", f"HTTP {status}: {wo}")

    action_payload = {
        "incident_id": state.get("incident_id"),
        "asset_id": asset_id,
        "action_type": "e2e_verification",
        "decision": "approved",
        "operator": "E2E verifier",
        "risk_level": "LOW",
        "note": "Automated operator action for connectivity verification run.",
    }
    status, action = request_json("POST", join(base, "/operator-actions"), action_payload)
    action_id = (action or {}).get("id") if isinstance(action, dict) else None
    if status in (200, 201) and action_id:
        report.add("Operator action persist", "pass", f"id={action_id}")
    elif not state["db_ok"]:
        report.add("Operator action persist", "skip", "Database unavailable")
    else:
        report.add("Operator action persist", "fail", f"HTTP {status}: {action}")

    status, listed_actions = request_json("GET", join(base, "/operator-actions?limit=5"))
    listed = listed_actions if isinstance(listed_actions, list) else []
    report.add(
        "Operator actions audit spine",
        "pass" if status == 200 and (listed or operator_actions) else "warn",
        f"HTTP {status}, live={len(operator_actions)}, listed={len(listed)}",
    )

    incident_id = state.get("incident_id")
    if incident_id:
        status, audit_detail = request_json("GET", join(base, f"/incidents/audit/{urllib.parse.quote(str(incident_id))}"))
        report.add(
            "Incident audit detail",
            "pass" if status == 200 and audit_detail.get("id") == incident_id else "warn",
            f"HTTP {status}",
        )
    else:
        report.add("Incident audit detail", "skip", "No incidents in live snapshot")

    status, reports = request_json("GET", join(base, "/reports"))
    report_rows = reports if isinstance(reports, list) else (reports or {}).get("reports", [])
    report.add("Executive reports", "pass" if status == 200 else "warn", f"{len(report_rows)} reports")
    if report_rows:
        rid = report_rows[0].get("id")
        export_status, _export = request_json("GET", join(base, f"/reports/{urllib.parse.quote(str(rid))}/export?format=markdown"))
        report.add("Report export", "pass" if export_status == 200 else "warn", f"HTTP {export_status}")

    status, knowledge = request_json("GET", join(base, "/knowledge/search?q=pressure%20relief"), timeout=45.0)
    if status == 200:
        results = (knowledge or {}).get("results", [])
        report.add("Knowledge search (RAG)", "pass" if results else "warn", f"{len(results)} hits")
    elif status == 503:
        report.add("Knowledge search (RAG)", "warn", "503 — retriever unavailable (check Gemini keys / index)")
    else:
        report.add("Knowledge search (RAG)", "warn", f"HTTP {status}: {knowledge}")

    assistant_payload = {
        "question": "What is the current operational risk for this asset?",
        "asset_id": asset_id,
        "incident_id": state.get("incident_id"),
        "facility": refineries[0].get("name") if refineries else None,
    }
    status, assistant = request_json("POST", join(base, "/assistant/query"), assistant_payload, timeout=90.0)
    if status == 200 and assistant.get("answer") and not assistant.get("degraded"):
        report.add("Assistant with context", "pass", "answer received")
    elif status == 200:
        report.add("Assistant with context", "warn", "degraded or empty answer")
    else:
        report.add("Assistant with context", "warn", f"HTTP {status}")

    status, agents = request_json("GET", join(base, "/agents"))
    report.add("Agent registry", "pass" if status == 200 and agents else "warn", f"HTTP {status}")

    status, triggered = request_json("POST", join(base, "/incidents/pressure-spike"))
    if status == 200 and not (isinstance(triggered, dict) and triggered.get("error")):
        report.add("Incident simulator trigger", "pass", "pressure-spike accepted")
    else:
        report.add("Incident simulator trigger", "warn", f"HTTP {status}: {triggered}")

    stages = investigation.get("stages") or []
    report.add(
        "Investigation stages (live)",
        "pass" if stages else "warn",
        f"{len(stages)} stages in live snapshot",
    )

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="RigOS Phase 7 e2e API verification")
    parser.add_argument("--base", default="http://localhost:8080/api", help="API base URL")
    args = parser.parse_args()

    print(f"RigOS e2e verification @ {args.base}\n")
    report = verify(args.base)
    passed, failed, warned, skipped = report.summary()

    for check in report.checks:
        icon = {"pass": "OK", "fail": "FAIL", "warn": "WARN", "skip": "SKIP"}[check.status]
        line = f"[{icon}] {check.name}"
        if check.detail:
            line += f" — {check.detail}"
        print(line)

    print(f"\nTotals: {passed} pass, {failed} fail, {warned} warn, {skipped} skip")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
