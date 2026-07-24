"""Report adapter using BackendAPI."""

from app.frontend_services.backend_api import api


def get_reports():
    """Get execution reports."""
    reports_data = api.get_reports()
    
    formatted_reports = []
    for report in reports_data[-10:]:
        formatted_reports.append({
            "Report": report["id"][:8],
            "Title": report["workflow"],
            "Workflow": report["workflow"],
            "Status": "Completed" if report["success"] else "Escalated",
            "Generated": report["completed_at"][:16] if "completed_at" in report else "N/A",
        })
    
    preview = {}
    if reports_data:
        latest = reports_data[-1]
        preview = {
            "Report": latest["id"][:8],
            "Title": latest["workflow"],
            "Summary": latest["summary"][:200] + "..." if len(latest.get("summary", "")) > 200 else latest.get("summary", ""),
            "Recommendation": "Review execution report for details."
        }
    
    metrics = [
        ("Reports generated", str(len(reports_data)), "From MAO executions", "cyan"),
        ("Resolved incidents", str(sum(1 for r in reports_data if r.get("success"))), "Successful workflows", "green"),
        ("Average confidence", f"{round(sum(r.get('confidence', 0) for r in reports_data) / len(reports_data) * 100, 1)}%" if reports_data else "N/A", "Execution quality", "green"),
        ("Pending review", str(sum(1 for r in reports_data if not r.get("success"))), "Requires attention", "amber"),
    ]
    
    return {
        "metrics": metrics,
        "reports": formatted_reports,
        "preview": preview,
    }