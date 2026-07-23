"""Read-only execution-report view models from the shared MAO runtime."""

from __future__ import annotations

from services.runtime import kernel


def _duration_seconds(report) -> float | None:
    if not report.started_at or not report.completed_at:
        return None
    return max(0.0, (report.completed_at - report.started_at).total_seconds())


def _report_row(report) -> dict:
    return {
        "Report": report.id[:8],
        "Title": report.workflow_name,
        "Workflow": report.workflow_name,
        "Status": "Completed" if report.success else "Escalated",
        "Generated": report.completed_at.strftime("%d %b %H:%M") if report.completed_at else "Not available",
        "Summary": report.final_summary or "No final summary recorded.",
        "Recommendations": "\n".join(report.recommendations or []) or "No recommendation recorded.",
        "Agents": report.total_agents,
        "Confidence": f"{round(report.average_confidence * 100, 1)}%",
        "Approval required": "Yes" if report.approval_required else "No",
        "Duration": (
            f"{_duration_seconds(report):.1f} sec" if _duration_seconds(report) is not None else "Not available"
        ),
    }


def _execution_timeline(report) -> list[dict]:
    """Format the existing agent results for the selected report's audit trail."""
    return [
        {
            "Agent": result.agent_name.replace("_", " ").title(),
            "Decision": result.decision or result.summary or result.finding or "No decision recorded.",
            "Success": "Completed" if result.success else "Attention",
            "Confidence": f"{round(result.confidence * 100, 1)}%",
            "Time": result.timestamp.strftime("%d %b %H:%M:%S") if result.timestamp else "Not available",
        }
        for result in report.agent_results
    ]


def get_reports() -> dict:
    """Format runtime execution reports while preserving agent-level evidence."""
    reports = list(reversed(kernel.state.execution_reports))
    rows = [_report_row(report) for report in reports]
    durations = [duration for report in reports if (duration := _duration_seconds(report)) is not None]
    preview = rows[0] if rows else {}
    return {
        "metrics": [
            ("Reports generated", str(len(reports)), "MAO execution reports", "cyan"),
            ("Successful workflows", str(sum(report.success for report in reports)), "Completed reports", "green"),
            (
                "Average response",
                f"{sum(durations) / len(durations):.1f} sec" if durations else "Not available",
                "Recorded execution duration",
                "green",
            ),
            (
                "Pending review",
                str(sum(report.approval_required or not report.success for report in reports)),
                "Approval or escalation required",
                "amber",
            ),
        ],
        "reports": rows,
        "preview": preview,
        "timelines": {report.id[:8]: _execution_timeline(report) for report in reports},
        "is_empty": not reports,
    }
