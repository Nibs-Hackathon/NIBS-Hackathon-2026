import streamlit as st
import re
from services.ai_config import AIConfigGenerator


def render_agent_card(report):
    """Render an agent result card with dynamic confidence thresholds."""
    
    # ✅ Get confidence thresholds from config
    try:
        config = AIConfigGenerator()
        pred_params = config.get_prediction_params()
        confidence_threshold = pred_params.get("confidence_weight", 0.55)
    except:
        confidence_threshold = 0.55
    
    if hasattr(report, 'final_summary'):
        text = report.final_summary.lower()
        
        # ✅ Dynamic agent name detection
        agent_map = {
            "safety": "🛡️ Safety Agent",
            "diagnostic": "🔍 Diagnostic Agent",
            "knowledge": "📚 Knowledge Agent",
            "maintenance": "🔧 Maintenance Agent",
            "planning": "📋 Planning Agent",
            "prediction": "🔮 Prediction Agent",
            "notification": "🔔 Notification Agent",
            "sensor": "📡 Sensor Agent",
            "report": "📊 Report Agent",
        }
        
        agent_name = "🤖 AI Agent"
        for key, name in agent_map.items():
            if f"[{key}]" in text:
                agent_name = name
                break
        
        # Remove all agent tags
        cleaned = re.sub(r'\[.*?\]', '', report.final_summary)
        
        confidence = getattr(report, 'average_confidence', confidence_threshold)
        confidence_pct = f"{confidence * 100:.0f}%" if confidence else "N/A"
        
        # ✅ Dynamic status based on confidence
        if confidence >= 0.9:
            status_text = "✅ Excellent"
            status_color = "#4fe3b2"
        elif confidence >= 0.7:
            status_text = "✅ Good"
            status_color = "#55D6FF"
        elif confidence >= 0.5:
            status_text = "⚠️ Review"
            status_color = "#ffbf69"
        else:
            status_text = "❌ Needs Review"
            status_color = "#ff718d"
        
        st.markdown(
            f"""
            <div class="agent-card">
                <h4 class="agent-title">{agent_name}</h4>
                <p class="agent-finding">{cleaned[:300]}</p>
                <div class="agent-meta">
                    <span class="agent-confidence">Confidence: {confidence_pct}</span>
                    <span class="agent-status" style="color: {status_color}">Status: {status_text}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    elif isinstance(report, dict):
        agent_name = report.get("agent_name", "Unknown Agent").title()
        finding = report.get("finding", "No finding")
        confidence = report.get("confidence", confidence_threshold)
        confidence_pct = f"{confidence * 100:.0f}%" if confidence else "N/A"
        
        st.markdown(
            f"""
            <div class="agent-card">
                <h4 class="agent-title">🤖 {agent_name}</h4>
                <p class="agent-finding">{finding[:200]}</p>
                <div class="agent-meta">
                    <span class="agent-confidence">Confidence: {confidence_pct}</span>
                    <span class="agent-status" style="color: #4fe3b2">Status: ✅ Completed</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write(f"⚠️ Unknown report format: {type(report)}")