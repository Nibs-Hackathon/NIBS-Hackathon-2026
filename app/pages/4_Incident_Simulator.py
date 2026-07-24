import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import time
import json
from datetime import datetime

from components.phase_one_views import render_incident_response_flow, render_live_signal_banner
from frontend_services.incident_adapter import trigger_incident, get_incidents
from frontend_services.asset_adapter import get_assets
from ui_helpers import (
    incident_simulator_demo_flow,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip,
    metric_card
)
from components.incident_card import render_incident_card
from components.agent_card import render_agent_card
from components.telemetry_card import render_telemetry
from components.timeline import render_timeline
from components.investigation_progress import render_investigation_progress
from components.global_notifications import render_global_notifications

setup_page("Incident Simulator")
render_sidebar("Incident Simulator")
render_global_notifications()

page_heading(
    "🎯 SCENARIO LAB",
    "Incident Simulator",
    "Safely exercise AI detection, triage, and response workflows using synthetic events.",
)
render_live_signal_banner(
    "🎮 SCENARIO DESIGN MODE",
    "Configure and launch simulated incidents to test AI response capabilities.",
    "Info",
)
st.write("")

# ✅ Get dynamic assets from backend
asset_data = get_assets()
all_assets = asset_data.get("assets", [])

if all_assets:
    asset_options = [
        f"{a['name']} ({a.get('location', 'Unknown')})"
        for a in all_assets
    ]
else:
    from services.ai_config import AIConfigGenerator
    config = AIConfigGenerator()
    asset_types = list(config.get_config().get("asset_types", {}).keys())
    asset_options = [f"{t} (Demo)" for t in asset_types[:5]]

from services.ai_config import AIConfigGenerator
_config = AIConfigGenerator()
_workflows = _config.get_config().get("workflow_sequences", {})
incident_types = [k.replace("_", " ").title() for k in _workflows.keys()]

if not incident_types:
    incident_types = ["Pressure Spike", "High Temperature", "Gas Leak", "High Vibration", "Flow Restriction"]

severity_levels = list(_config.get_config().get("severity_mapping", {}).keys())
if not severity_levels:
    severity_levels = ["Low", "Medium", "High", "Critical"]

# ✅ Incident type icons
incident_icons = {
    "Pressure Spike": "📈",
    "High Temperature": "🌡️",
    "Gas Leak": "💨",
    "High Vibration": "📳",
    "Flow Restriction": "🚫",
}

left, right = st.columns([1, 1.35])
with left:
    st.markdown("<div class='section-label'>⚙️ CONFIGURE SCENARIO</div>", unsafe_allow_html=True)
    
    asset = st.selectbox("🎯 Affected asset", asset_options, key="sim_asset")
    incident_type = st.selectbox(
        "🚨 Incident type", 
        incident_types, 
        key="sim_incident_type",
        format_func=lambda x: f"{incident_icons.get(x, '')} {x}"
    )
    severity = st.select_slider(
        "⚠️ Severity", 
        options=severity_levels, 
        value=severity_levels[-2] if len(severity_levels) >= 2 else "High", 
        key="sim_severity"
    )
    
    # ✅ Scenario presets
    # ✅ FIXED: Use session_state directly without conflicting with widget keys
    st.markdown("<div class='section-label'>📋 SCENARIO PRESETS</div>", unsafe_allow_html=True)
    preset_col1, preset_col2 = st.columns(2)

    with preset_col1:
        if st.button("🔥 Critical Gas Leak", use_container_width=True, key="preset_gas"):
            # ✅ Use a different approach - set values and rerun
            st.session_state.preset_asset = asset_options[0] if asset_options else ""
            st.session_state.preset_incident_type = "Gas Leak"
            st.session_state.preset_severity = "Critical"
            st.rerun()

    with preset_col2:
        if st.button("⚡ Pressure Spike", use_container_width=True, key="preset_pressure"):
            st.session_state.preset_asset = asset_options[0] if asset_options else ""
            st.session_state.preset_incident_type = "Pressure Spike"
            st.session_state.preset_severity = "High"
            st.rerun()

    # ✅ Apply presets if they exist
    if "preset_asset" in st.session_state and st.session_state.preset_asset:
        # Update the widget values through session state
        st.session_state.sim_asset = st.session_state.preset_asset
        st.session_state.sim_incident_type = st.session_state.preset_incident_type
        st.session_state.sim_severity = st.session_state.preset_severity
        # Clear presets after applying
        del st.session_state.preset_asset
        del st.session_state.preset_incident_type
        del st.session_state.preset_severity
        st.rerun()
    
    # ✅ Initialize session state keys
    if "sim_incident_triggered" not in st.session_state:
        st.session_state.sim_incident_triggered = False
    if "sim_incident_results" not in st.session_state:
        st.session_state.sim_incident_results = None
    if "sim_launch" not in st.session_state:
        st.session_state.sim_launch = False
    if "sim_history" not in st.session_state:
        st.session_state.sim_history = []
    
    # ✅ Launch button with animation
    if st.button("🚀 Launch simulated incident", width='stretch', type="primary", key="sim_launch_btn"):        
        st.session_state.sim_launch = True
        st.session_state.sim_incident_triggered = False
        st.session_state.sim_incident_results = None
        st.rerun()
    
with right:
    asset_name = asset.split(" (")[0] if " (" in asset else asset
    render_incident_response_flow(incident_simulator_demo_flow(incident_type, asset_name))

# ✅ SHOW RESULTS IF INCIDENT WAS LAUNCHED
if st.session_state.sim_launch:
    
    # ✅ RUN INCIDENT ONLY ONCE
    if not st.session_state.sim_incident_triggered:
        
        asset_name = asset.split(" (")[0] if " (" in asset else asset
        
        st.success(f"🚨 Simulation launched for {asset_name}")
        
        with st.spinner("🧠 AI agents are analyzing the incident..."):
            # ✅ Execute the incident ONCE
            simulator_result = trigger_incident(incident_type)
            # ✅ Store results and mark as triggered
            st.session_state.sim_incident_results = simulator_result
            st.session_state.sim_incident_triggered = True
            
            # ✅ Add to history
            st.session_state.sim_history.append({
                "timestamp": datetime.now(),
                "asset": asset_name,
                "incident_type": incident_type,
                "severity": severity,
                "result": "Success" if simulator_result.get("reports") else "Failed",
                "reports_count": len(simulator_result.get("reports", [])),
            })
        
        # ✅ Display results
        render_incident_card(
            asset_name,
            incident_type,
            severity,
            "✅ AI Investigation Complete" if simulator_result.get("reports") else "Processing"
        )

        render_telemetry()
        render_timeline()
        render_investigation_progress()

        reports = simulator_result.get("reports", [])
        
        if reports:
            st.markdown("### 🤖 Agent Investigation Results")
            
            # ✅ Show all agent results in tabs
            tabs = st.tabs([f"{i+1}. Agent Result" for i in range(min(len(reports), 5))])
            for i, tab in enumerate(tabs):
                if i < len(reports):
                    with tab:
                        render_agent_card(reports[i])
            
            # ✅ Show all recommendations
            all_recommendations = []
            for report in reports:
                if hasattr(report, 'recommendations') and report.recommendations:
                    all_recommendations.extend(report.recommendations)
            
            if all_recommendations:
                st.markdown("### ✅ System Recommendations")
                unique_recommendations = list(dict.fromkeys(all_recommendations))
                for rec in unique_recommendations[:5]:
                    st.markdown(f"""
                    <div style="padding: 8px 12px; margin: 4px 0; background: rgba(79, 227, 178, 0.1); border-radius: 6px; border-left: 3px solid #4fe3b2;">
                        {rec}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No incident reports generated. Make sure the simulation is running.")

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("✅ Approve Response Plan", use_container_width=True, key="sim_approve"):
                st.success("✅ Response approved. Incident will be resolved.")
                # ✅ Mark as resolved
                st.session_state.sim_launch = False
                st.session_state.sim_incident_triggered = False
                time.sleep(1)
                st.rerun()

        with c2:
            if st.button("🔄 Run Investigation Again", use_container_width=True, key="sim_rerun"):
                st.session_state.sim_launch = False
                st.session_state.sim_incident_triggered = False
                st.rerun()

        with c3:
            if st.button("📄 Export Incident Report", use_container_width=True, key="sim_report"):
                # ✅ Generate report
                report_data = {
                    "incident_type": incident_type,
                    "asset": asset_name,
                    "severity": severity,
                    "timestamp": datetime.now().isoformat(),
                    "agent_results": len(reports),
                    "recommendations": all_recommendations[:5] if all_recommendations else [],
                }
                st.download_button(
                    label="📥 Download Report",
                    data=json.dumps(report_data, indent=2),
                    file_name=f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True,
                )
    
    # ✅ If already triggered, just show cached results
    else:
        simulator_result = st.session_state.sim_incident_results
        asset_name = asset.split(" (")[0] if " (" in asset else asset
        
        render_incident_card(
            asset_name,
            incident_type,
            severity,
            "✅ AI Investigation Complete" if simulator_result and simulator_result.get("reports") else "Processing"
        )

        render_telemetry()
        render_timeline()
        render_investigation_progress()

        reports = simulator_result.get("reports", []) if simulator_result else []
        
        if reports:
            st.markdown("### 🤖 Agent Investigation Results")
            tabs = st.tabs([f"{i+1}. Agent Result" for i in range(min(len(reports), 5))])
            for i, tab in enumerate(tabs):
                if i < len(reports):
                    with tab:
                        render_agent_card(reports[i])
            
            all_recommendations = []
            for report in reports:
                if hasattr(report, 'recommendations') and report.recommendations:
                    all_recommendations.extend(report.recommendations)
            
            if all_recommendations:
                st.markdown("### ✅ System Recommendations")
                unique_recommendations = list(dict.fromkeys(all_recommendations))
                for rec in unique_recommendations[:5]:
                    st.markdown(f"""
                    <div style="padding: 8px 12px; margin: 4px 0; background: rgba(79, 227, 178, 0.1); border-radius: 6px; border-left: 3px solid #4fe3b2;">
                        {rec}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No incident reports generated.")

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("✅ Approve Response Plan", use_container_width=True, key="sim_approve2"):
                st.success("✅ Response approved. Incident will be resolved.")
                st.session_state.sim_launch = False
                st.session_state.sim_incident_triggered = False
                time.sleep(1)
                st.rerun()

        with c2:
            if st.button("🔄 Run Investigation Again", use_container_width=True, key="sim_rerun2"):
                st.session_state.sim_launch = False
                st.session_state.sim_incident_triggered = False
                st.rerun()

        with c3:
            if st.button("📄 Export Incident Report", use_container_width=True, key="sim_report2"):
                report_data = {
                    "incident_type": incident_type,
                    "asset": asset_name,
                    "severity": severity,
                    "timestamp": datetime.now().isoformat(),
                    "agent_results": len(reports),
                    "recommendations": all_recommendations[:5] if all_recommendations else [],
                }
                st.download_button(
                    label="📥 Download Report",
                    data=json.dumps(report_data, indent=2),
                    file_name=f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True,
                )

st.write("")
st.markdown("<div class='section-label'>📜 RECENT SIMULATED SCENARIOS</div>", unsafe_allow_html=True)

# ✅ Use actual incidents if available
actual_incidents = get_incidents()[-5:]

if st.session_state.sim_history:
    display_data = []
    for h in st.session_state.sim_history[-5:]:
        display_data.append({
            "Scenario": f"SIM-{len(st.session_state.sim_history) - st.session_state.sim_history.index(h):03d}",
            "Type": h.get("incident_type", "Unknown"),
            "Asset": h.get("asset", "Unknown"),
            "Severity": h.get("severity", "Medium"),
            "Result": "✅ Resolved" if h.get("result") == "Success" else "⚠️ Review",
            "Reports": h.get("reports_count", 0),
            "Time": h.get("timestamp", datetime.now()).strftime("%H:%M:%S"),
        })
    st.dataframe(display_data, hide_index=True, use_container_width=True)
elif actual_incidents:
    display_data = [
        {
            "Scenario": f"SIM-{i+1:03d}",
            "Type": inc.get("Incident", "Unknown"),
            "Asset": inc.get("Asset", "Unknown"),
            "Severity": inc.get("Severity", "Medium"),
            "Result": "✅ Resolved" if inc.get("Severity") != "Critical" else "⚠️ Review",
            "Reports": 5,
            "Time": inc.get("Detected", "00:00:00"),
        }
        for i, inc in enumerate(actual_incidents)
    ]
    st.dataframe(display_data, hide_index=True, use_container_width=True)
else:
    st.info("No incidents triggered yet. Launch a simulation to see results here.")