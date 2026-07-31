"""Frontend routing for Command Nexus conversational and operational requests."""

from __future__ import annotations

from functools import lru_cache
import logging
from pathlib import Path
import re
import sys
from typing import TYPE_CHECKING, Callable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if TYPE_CHECKING:
    from agents.knowledge import KnowledgeAgent

LOGGER = logging.getLogger(__name__)
ProgressCallback = Callable[[str], None]

OPERATIONAL_KEYWORDS = (
    "asset", "compressor", "pump", "pipeline", "tank", "valve", "maintenance",
    "inspection", "incident", "alarm", "safety", "hazard", "pressure",
    "temperature", "vibration", "flow", "gas", "refinery", "sop", "procedure",
    "equipment", "motor", "turbine", "boiler", "heat exchanger", "reactor",
    "distillation", "column", "flare", "corrosion", "shutdown", "startup",
    "trip", "failure", "process", "telemetry", "sensor", "knowledge",
    "attention", "risk", "current", "status", "facility", "report",
    "work order", "work-order", "agent", "revenue", "cost", "loss", "impact",
)


def is_operational_query(question: str) -> bool:
    """Return whether a question requires the refinery operations path."""
    normalized = re.sub(r"\s+", " ", question.strip().casefold())
    return bool(normalized and any(keyword in normalized for keyword in OPERATIONAL_KEYWORDS))


def generate_conversational_response(question: str) -> str:
    """Use Gemini for casual conversation without starting the operational path."""
    from services.llm import LLMManager

    prompt = f"""
You are Command Nexus, a polished industrial operations copilot.

Reply naturally to this casual user message: {question!r}

Keep the response concise, warm, and professional. You may introduce yourself
as an industrial operations copilot and offer help with refinery operations,
equipment, maintenance, incident response, and safety. Do not provide
operational facts, citations, or technical instructions for a casual message.
Never mention implementation, search, retrieval, documents, a knowledge base,
databases, RAG, prompts, APIs, or model internals.
"""
    try:
        return LLMManager().generate(prompt)
    except Exception as e:
        LOGGER.error(f"Conversational response failed: {e}")
        return "I'm here to help with refinery operations. What would you like to know?"


def _emit(callback: ProgressCallback | None, message: str) -> None:
    LOGGER.info(message)
    if callback is not None:
        callback(message)


def _live_context(
    question: str,
    asset_id: str | None,
    incident_id: str | None,
    facility: str | None,
    history: list[dict[str, str]] | None = None,
) -> list[str]:
    """Build a compact, entity-resolved snapshot for grounded questions."""
    try:
        from services.runtime import runtime
        from services.revenue_impact_calculator import revenue_service

        kernel = runtime.kernel
        assets = list(kernel.asset_service.all_assets())
        enterprise = not facility or facility in {
            "Enterprise view", "portfolio", "North Sea Portfolio",
        }
        scoped_assets = assets if enterprise else [
            asset for asset in assets if getattr(asset, "location", None) == facility
        ]
        lines = [f"Facility scope: {facility or 'Enterprise view'}"]
        if scoped_assets:
            health_values = [
                float(asset.health) for asset in scoped_assets
                if getattr(asset, "health", None) is not None
            ]
            average_health = sum(health_values) / len(health_values) if health_values else 0
            lines.extend([
                f"Assets in scope: {len(scoped_assets)}",
                f"Average asset health: {average_health:.1f}/100",
                f"Assets below 80 health: {sum(value < 80 for value in health_values)}",
            ])

        normalized_question = re.sub(r"[^a-z0-9]", "", question.casefold())
        selected_asset = kernel.asset_service.get(asset_id) if asset_id else None
        selected_name = re.sub(
            r"[^a-z0-9]",
            "",
            str(getattr(selected_asset, "name", "")).casefold(),
        )
        # Resolve a concrete asset from the current question first. Historical
        # mentions must not silently pin every later enterprise question to the
        # same valve/pump.
        explicitly_mentioned_asset = (
            selected_asset
            if selected_asset is not None and selected_name and selected_name in normalized_question
            else next(
                (
                    candidate for candidate in scoped_assets
                    if (
                        re.sub(r"[^a-z0-9]", "", str(getattr(candidate, "name", "")).casefold())
                        and re.sub(r"[^a-z0-9]", "", str(getattr(candidate, "name", "")).casefold())
                        in normalized_question
                    )
                ),
                None,
            )
        )
        uses_contextual_pronoun = bool(re.search(
            r"\b(?:this|that|selected|current)\s+"
            r"(?:asset|equipment|unit|valve|pump|compressor)\b|\b(?:it|its)\b",
            question.casefold(),
        ))
        historical_asset = None
        if uses_contextual_pronoun and selected_asset is None:
            recent_text = " ".join(
                str(item.get("text", "")) for item in (history or [])[-4:]
            )
            normalized_history = re.sub(r"[^a-z0-9]", "", recent_text.casefold())
            historical_asset = next(
                (
                    candidate for candidate in scoped_assets
                    if (
                        re.sub(r"[^a-z0-9]", "", str(getattr(candidate, "name", "")).casefold())
                        and re.sub(r"[^a-z0-9]", "", str(getattr(candidate, "name", "")).casefold())
                        in normalized_history
                    )
                ),
                None,
            )
        asset = explicitly_mentioned_asset
        if asset is None and uses_contextual_pronoun:
            asset = selected_asset or historical_asset
        events = list(kernel.event_store.all())
        selected_incident = next(
            (event for event in events if str(getattr(event, "id", "")) == str(incident_id)),
            None,
        ) if incident_id else None

        incident_aliases = {
            "gasleak": "GasLeak",
            "flowrestriction": "FlowRestriction",
            "pressurespike": "PressureSpike",
            "hightemperature": "HighTemperature",
            "highvibration": "HighVibration",
        }
        requested_incident = next(
            (canonical for alias, canonical in incident_aliases.items() if alias in normalized_question),
            None,
        )
        if asset is None and selected_incident is not None:
            asset = kernel.asset_service.get(getattr(selected_incident, "source", None))

        active_event_ids = {
            str(getattr(item.get("event"), "id", ""))
            for item in getattr(runtime.active_simulator, "active_incidents", {}).values()
        } if runtime.active_simulator else set()
        scoped_asset_ids = {str(getattr(item, "id", "")) for item in scoped_assets}
        scoped_active = [
            event for event in events
            if str(getattr(event, "id", "")) in active_event_ids
            and str(getattr(event, "source", "")) in scoped_asset_ids
        ]
        try:
            from api.adapters.operations_adapter import get_execution_reports

            report_rows = get_execution_reports(limit=500)
            scoped_reports = report_rows if enterprise else [
                report for report in report_rows
                if report.get("facility") == facility
            ]
            economic_reports = [
                report for report in scoped_reports
                if report.get("financial_impact") is not None
            ]
            if economic_reports:
                exposure_total = sum(
                    float(report.get("financial_impact") or 0)
                    for report in economic_reports
                )
                maintenance_total = sum(
                    float(report.get("maintenance_cost") or 0)
                    for report in economic_reports
                    if report.get("maintenance_cost") is not None
                )
                grouped: dict[str, dict[str, float | int]] = {}
                production_impacts = []
                for report in economic_reports:
                    incident_name = str(report.get("incident_type") or "Unclassified")
                    group = grouped.setdefault(
                        incident_name,
                        {"exposure": 0.0, "count": 0},
                    )
                    group["exposure"] = float(group["exposure"]) + float(
                        report.get("financial_impact") or 0
                    )
                    group["count"] = int(group["count"]) + 1
                    if report.get("production_impact") is not None:
                        production_impacts.append(float(report["production_impact"]))
                breakdown = "; ".join(
                    f"{name} ${values['exposure']:,.2f} across {values['count']} incident(s)"
                    for name, values in sorted(
                        grouped.items(),
                        key=lambda item: float(item[1]["exposure"]),
                        reverse=True,
                    )
                )
                lines.extend([
                    "Modeled portfolio report exposure: "
                    f"${exposure_total:,.2f} across {len(economic_reports)} "
                    f"persisted incident report(s).",
                    f"Modeled maintenance estimate total: ${maintenance_total:,.2f}.",
                    f"Modeled incident exposure breakdown: {breakdown}.",
                ])
                if production_impacts:
                    lines.append(
                        "Modeled production impact observations: "
                        f"average {sum(production_impacts) / len(production_impacts):.1f}%; "
                        f"maximum {max(production_impacts):.1f}%."
                    )
        except Exception:
            pass
        if asset is None and requested_incident:
            matching_active = [
                event for event in scoped_active
                if getattr(event, "name", None) == requested_incident
            ]
            # A unique live match is safe to resolve. If multiple sites/assets
            # match, retain portfolio scope instead of choosing one arbitrarily.
            if len(matching_active) == 1:
                asset = kernel.asset_service.get(getattr(matching_active[0], "source", None))
        relevant_events = [
            event for event in events
            if asset is None or str(getattr(event, "source", "")) == str(getattr(asset, "id", ""))
        ]
        active_events = [
            event for event in relevant_events
            if str(getattr(event, "id", "")) in active_event_ids
        ]
        incident = (
            next((event for event in active_events if getattr(event, "name", None) == requested_incident), None)
            or (selected_incident if selected_incident in relevant_events else None)
            or (active_events[-1] if active_events else None)
        )

        if asset is not None:
            asset_type = getattr(
                getattr(asset, "asset_type", None),
                "value",
                getattr(asset, "asset_type", "Unknown"),
            )
            lines.extend([
                f"Resolved asset: {asset.name} ({asset.id})",
                f"Resolved asset type: {asset_type}",
                f"Resolved asset health: {getattr(asset, 'health', 'Unknown')}",
                f"Resolved asset status: {getattr(asset, 'status', 'Unknown')}",
            ])
            if incident is not None:
                payload = getattr(incident, "payload", {}) or {}
                lines.extend([
                    f"Active incident on resolved asset: {incident.name}",
                    f"Incident id: {incident.id}",
                    f"Incident timestamp: {getattr(incident, 'timestamp', 'Unknown')}",
                    f"Trigger telemetry: {payload}",
                ])
                impact = revenue_service.calculate_incident_impact(
                    incident.name,
                    str(asset_type),
                    duration_hours=2,
                )
                lines.append(
                    "Modeled incident exposure (estimate, not booked loss): "
                    f"${impact['revenue_loss']:,.2f} over {impact['duration_hours']} hours; "
                    f"asset baseline ${impact['daily_revenue']:,.2f}/day."
                )
            elif active_events:
                lines.append(
                    "Active incidents on resolved asset: "
                    + ", ".join(event.name for event in active_events)
                )
            else:
                lines.append("Active incidents on resolved asset: none.")

            if requested_incident and not any(
                getattr(event, "name", None) == requested_incident for event in active_events
            ):
                hypothetical = revenue_service.calculate_incident_impact(
                    requested_incident,
                    str(asset_type),
                    duration_hours=2,
                )
                lines.append(
                    f"Assertion check: no active {requested_incident} is recorded on {asset.name}. "
                    f"A two-hour {requested_incident} scenario would have modeled exposure "
                    f"of ${hypothetical['revenue_loss']:,.2f}; this is hypothetical."
                )

        lines.append(
            "Active incidents in scope: "
            + (
                "; ".join(
                    f"{event.name} on {getattr(kernel.asset_service.get(event.source), 'name', event.source)}"
                    for event in scoped_active[-8:]
                )
                if scoped_active else "none"
            )
        )
        lines.append(f"Recorded incidents in runtime: {len(events)}")
        return lines
    except Exception:
        return [f"Facility scope: {facility or 'Enterprise view'}"]


def _financial_context_answer(context_lines: list[str]) -> str | None:
    """Return deterministic modeled exposure when the live context has it."""
    exposure = next(
        (
            line for line in context_lines
            if line.startswith("Modeled incident exposure (estimate")
        ),
        None,
    )
    assertion = next(
        (line for line in context_lines if line.startswith("Assertion check:")),
        None,
    )
    incident = next(
        (line for line in context_lines if line.startswith("Active incident on resolved asset:")),
        None,
    )
    asset = next(
        (line for line in context_lines if line.startswith("Resolved asset:")),
        None,
    )
    if exposure is not None or assertion is not None:
        assessment = "\n".join(
            f"- {line.split(':', 1)[-1].strip()}"
            for line in (asset, incident, assertion)
            if line
        )
        impact = (
            exposure.split(":", 1)[-1].strip()
            if exposure
            else assertion.split(":", 1)[-1].strip()
        )
        return (
            "## Situation Assessment\n"
            f"{assessment or '- The referenced operating scenario was resolved from live context.'}\n\n"
            "## Modeled Financial Exposure\n"
            f"- {impact}\n"
            "- This is a scenario estimate for operational exposure, not a booked loss, "
            "vendor quote, or approved maintenance cost.\n\n"
            "## Recommended Next Step\n"
            "- Confirm expected incident duration and the maintenance work scope before "
            "using the estimate for approval."
        )

    portfolio = [
        line for line in context_lines
        if line.startswith((
            "Modeled portfolio report exposure:",
            "Modeled maintenance estimate total:",
            "Modeled incident exposure breakdown:",
            "Modeled production impact observations:",
        ))
    ]
    active_scope = next(
        (line for line in context_lines if line.startswith("Active incidents in scope:")),
        None,
    )
    if portfolio:
        total = next(
            line for line in portfolio
            if line.startswith("Modeled portfolio report exposure:")
        )
        detail_lines = "\n".join(
            f"- {line.split(':', 1)[-1].strip()}"
            for line in portfolio[1:]
        )
        return (
            "## Situation Assessment\n"
            f"- {total.split(':', 1)[-1].strip()}\n"
            f"- {(active_scope or 'Active incidents in scope: unavailable').split(':', 1)[-1].strip()}\n\n"
            "## Modeled Financial Exposure\n"
            f"{detail_lines}\n\n"
            "## Interpretation\n"
            "- These values are modeled operational exposure from persisted incident reports. "
            "They are not booked revenue loss, invoices, or approved vendor quotations.\n"
            "- Incident totals describe the available report archive; an incident report can "
            "represent risk exposure even when the field condition is now resolved.\n\n"
            "## Recommended Next Step\n"
            "- Use the report archive to review the highest-exposure incident type, then confirm "
            "duration and production assumptions before financial approval."
        )
    return None


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Return the KnowledgeAgent registered on the shared MAO kernel."""
    try:
        from services.runtime import runtime
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise RuntimeError("KnowledgeAgent is not registered on the MAO kernel.")
        return agent
    except Exception as error:
        raise KnowledgeAgentUnavailable("Command Nexus is temporarily unavailable. Please try again shortly.") from error


def ask_knowledge_agent(
    question: str,
    on_progress: ProgressCallback | None = None,
    asset_id: str | None = None,
    incident_id: str | None = None,
    facility: str | None = None,
    history: list[dict[str, str]] | None = None,
) -> str:
    """Route casual conversation to Gemini and operational questions to KnowledgeAgent."""
    _emit(on_progress, "Command Nexus received a question.")
    normalized_question = question.strip()
    if not normalized_question:
        raise KnowledgeAgentUnavailable("Enter a question before asking Command Nexus.")

    operational_query = is_operational_query(normalized_question)
    if not operational_query:
        _emit(on_progress, "Conversational request detected.")
        try:
            return generate_conversational_response(normalized_question)
        except Exception as error:
            LOGGER.exception("Command Nexus conversational response failed")
            return "I'm here to help! What would you like to know about refinery operations?"

    context_lines = _live_context(
        normalized_question,
        asset_id,
        incident_id,
        facility,
        history,
    )
    if any(term in normalized_question.casefold() for term in ("revenue", "cost", "loss", "impact")):
        financial_answer = _financial_context_answer(context_lines)
        if financial_answer:
            _emit(on_progress, "Calculated modeled operational exposure.")
            return financial_answer
    if context_lines:
        normalized_question = (
            "Operator context:\n"
            + "\n".join(context_lines)
            + f"\n\nQuestion: {normalized_question}"
        )

    _emit(on_progress, "Preparing an operational assessment.")
    try:
        from mao.models.task import Task

        task = Task(
            name="Operator knowledge query",
            description=normalized_question,
            assigned_agent="knowledge",
        )
        agent = get_knowledge_agent()
        
        if agent.retriever is None:
            return "The knowledge base is not available. Please ensure the database is configured and has documents loaded."

        result = agent.execute(task)
        
        if not result.success or not result.summary:
            return "I couldn't find specific operational guidance for that query. Please check with your operations team."
            
        return result.summary
        
    except Exception as error:
        LOGGER.exception("Command Nexus operational response failed")
        return "I'm having trouble accessing the knowledge base right now. Please try again later."
