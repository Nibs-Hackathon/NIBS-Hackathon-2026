from collections import OrderedDict

from mao.core.context import ExecutionContext


class Supervisor:
    """
    Aggregates all agent outputs into a final execution decision.
    """

    def summarize(self, context: ExecutionContext) -> dict:

        results = context.results

        if not results:
            return {
                "success": True,
                "confidence": 0.0,
                "summary": "No agents were executed.",
                "recommendations": [],
                "severity": "Unknown",
            }

        # Overall success
        success = all(result.success for result in results)

        # Average confidence
        confidence = context.execution_metrics["average_confidence"]

        # Remove duplicate recommendations
        recommendations = list(
            OrderedDict.fromkeys(
                rec
                for result in results
                for rec in result.recommendations
            )
        )

        # Confidence measures evidence quality, not incident severity.
        safety_status = str(context.metadata.get("safety", {}).get("status", "SAFE")).upper()
        maintenance_priority = str(context.metadata.get("maintenance", {}).get("priority", "LOW")).upper()
        severity = (
            "Critical" if "CRITICAL" in {safety_status, maintenance_priority}
            else "High" if safety_status == "WARNING" or maintenance_priority == "HIGH"
            else "Medium" if maintenance_priority == "MEDIUM"
            else "Low"
        )

        context.incident_level = severity

        # Human approval
        approval_required = any(
            result.requires_human_approval
            for result in results
        )

        context.requires_human_approval = approval_required

        # Store metadata
        context.metadata["confidence"] = confidence
        context.metadata["severity"] = severity
        context.metadata["approval_required"] = approval_required

        # Keep the board narrative concise. Detailed agent findings remain on
        # the execution report and evidence appendix instead of being dumped
        # into the executive summary.
        event_name = getattr(context.event, "name", "operational")
        asset_id = getattr(context.event, "source", "unknown asset")
        recommendation = recommendations[0] if recommendations else "Continue monitoring and complete operator review."
        diagnosis = ", ".join(context.metadata.get("diagnosis", {}).get("diagnosis", []))
        safety_line = context.metadata.get("safety", {}).get("status", "not established")
        maintenance_line = context.metadata.get("maintenance", {}).get("priority", "not established")
        summary = (
            f"{event_name} on asset {asset_id} was assessed at {severity.lower()} severity "
            f"with {confidence:.0%} evidence confidence. Safety status: {safety_line}; "
            f"maintenance priority: {maintenance_line}."
        )
        if diagnosis:
            summary += f" The diagnostic finding was {diagnosis}."
        summary += f" Recommended next action: {recommendation}"

        return {
            "success": success,
            "confidence": confidence,
            "summary": summary,
            "recommendations": recommendations,
            "severity": severity,
        }
