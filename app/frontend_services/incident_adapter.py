"""Incident adapter with dynamic severity calculation from config."""

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.incident_service import IncidentService
from services.ai_config import AIConfigGenerator


def trigger_incident(incident_type):
    """Trigger an incident and return formatted results."""
    simulator = runtime.simulator
    service = IncidentService(simulator)
    result = service.trigger_incident(incident_type)
    
    try:
        import streamlit as st
        reports = result.get("reports", [])
        if reports:
            events = []
            for i, report in enumerate(reports):
                agent_name = getattr(report, 'workflow_name', 'Unknown')
                if i == 0:
                    events.append(("⏱️ 00:00", "🚨 Incident detected"))
                events.append((f"⏱️ 00:{i+2:02d}", f"🤖 {agent_name} completed"))
            
            last_report = reports[-1] if reports else None
            if last_report:
                summary = getattr(last_report, 'final_summary', '')
                if "planning" in summary.lower():
                    events.append(("⏱️ 00:12", "✅ Investigation complete"))
            
            st.session_state.incident_events = events
            st.session_state.investigation_complete = True
    except Exception as e:
        print(f"⚠️ Could not update session state: {e}")
    
    return result


def get_incidents():
    """Get all incidents from the runtime."""
    kernel = runtime.kernel
    events = kernel.event_store.all()

    incidents = []
    for event in events:
        severity = calculate_severity(event)
        incidents.append({
            "Incident": event.name,
            "Asset": event.source,
            "Severity": severity,
            "Detected": event.timestamp.strftime("%H:%M:%S") if hasattr(event, 'timestamp') else "Unknown",
            "Payload": event.payload,
        })

    return incidents


def calculate_severity(event):
    """
    Calculate severity from event payload using dynamic thresholds from AI config.
    """
    payload = getattr(event, 'payload', {})
    
    try:
        config = AIConfigGenerator()
        asset_type = payload.get("asset_type", "Pump")
        thresholds = config.get_thresholds(asset_type)
        severity_map = config.get_config().get("severity_mapping", {
            "Critical": 1, "High": 2, "Medium": 3, "Low": 4
        })
        
        severity_scores = {}
        
        if "pressure" in payload:
            pressure_max = thresholds.get("pressure_max", 150)
            pressure_val = payload["pressure"]
            ratio = pressure_val / pressure_max
            if ratio >= 1.5:
                severity_scores["pressure"] = 1
            elif ratio >= 1.2:
                severity_scores["pressure"] = 2
            elif ratio >= 1.05:
                severity_scores["pressure"] = 3
            else:
                severity_scores["pressure"] = 4
        
        if "temperature" in payload:
            temp_max = thresholds.get("temperature_max", 85)
            temp_val = payload["temperature"]
            ratio = temp_val / temp_max
            if ratio >= 1.5:
                severity_scores["temperature"] = 1
            elif ratio >= 1.2:
                severity_scores["temperature"] = 2
            elif ratio >= 1.05:
                severity_scores["temperature"] = 3
            else:
                severity_scores["temperature"] = 4
        
        if "gas" in payload:
            gas_max = thresholds.get("gas_max", 40)
            gas_val = payload["gas"]
            ratio = gas_val / gas_max
            if ratio >= 1.5:
                severity_scores["gas"] = 1
            elif ratio >= 1.2:
                severity_scores["gas"] = 2
            elif ratio >= 1.05:
                severity_scores["gas"] = 3
            else:
                severity_scores["gas"] = 4
        
        if "vibration" in payload:
            vib_max = thresholds.get("vibration_max", 8)
            vib_val = payload["vibration"]
            ratio = vib_val / vib_max
            if ratio >= 1.5:
                severity_scores["vibration"] = 1
            elif ratio >= 1.2:
                severity_scores["vibration"] = 2
            elif ratio >= 1.05:
                severity_scores["vibration"] = 3
            else:
                severity_scores["vibration"] = 4
        
        if "flow" in payload:
            flow_min = thresholds.get("flow_min", 25)
            flow_val = payload["flow"]
            ratio = flow_min / flow_val if flow_val > 0 else 10
            if ratio >= 2:
                severity_scores["flow"] = 1
            elif ratio >= 1.5:
                severity_scores["flow"] = 2
            elif ratio >= 1.2:
                severity_scores["flow"] = 3
            else:
                severity_scores["flow"] = 4
        
        if severity_scores:
            worst_score = min(severity_scores.values())
            reverse_map = {v: k for k, v in severity_map.items()}
            return reverse_map.get(worst_score, "Medium")
        
    except Exception as e:
        print(f"⚠️ Severity calculation failed: {e}")
    
    return "Medium"