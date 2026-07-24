import streamlit as st
from services.ai_config import AIConfigGenerator


def render_telemetry():
    """Render live telemetry data with dynamic thresholds."""
    st.markdown("### 📊 Live Telemetry")
    
    # ✅ Get thresholds from AI config
    try:
        config = AIConfigGenerator()
        # Use Pump as default asset type
        thresholds = config.get_thresholds("Pump")
        
        pressure_max = thresholds.get("pressure_max", 150)
        temp_max = thresholds.get("temperature_max", 85)
        flow_min = thresholds.get("flow_min", 25)
        vib_max = thresholds.get("vibration_max", 8)
    except:
        pressure_max = 150
        temp_max = 85
        flow_min = 25
        vib_max = 8
    
    # ✅ Get telemetry from session state
    if "telemetry_data" in st.session_state:
        telemetry = st.session_state.telemetry_data
    else:
        # Demo values - still within thresholds
        telemetry = {
            "pressure": pressure_max * 0.85,
            "temperature": temp_max * 0.85,
            "flow": flow_min * 3,
            "vibration": vib_max * 0.7,
        }
    
    c1, c2, c3, c4 = st.columns(4)
    
    pressure = telemetry.get("pressure", pressure_max * 0.85)
    temp = telemetry.get("temperature", temp_max * 0.85)
    flow = telemetry.get("flow", flow_min * 3)
    vibration = telemetry.get("vibration", vib_max * 0.7)
    
    # ✅ Dynamic status based on thresholds
    pressure_status = "HIGH" if pressure > pressure_max * 0.95 else "NORMAL"
    temp_status = "ELEVATED" if temp > temp_max * 0.95 else "NORMAL"
    flow_status = "WARNING" if flow < flow_min * 1.2 else "NORMAL"
    vibration_status = "HIGH" if vibration > vib_max * 0.95 else "NORMAL"

    with c1:
        st.markdown(
            f"""
            <div class="metric-card" style="padding:12px;border-radius:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:0.8rem;color:#8fa1ba;">Pressure</div>
                <div style="font-size:1.4rem;font-weight:700;color:#e8f0ff;">{pressure:.1f} PSI</div>
                <div style="font-size:0.75rem;color:#ff718d;">{pressure_status}</div>
                <div style="font-size:0.65rem;color:#8fa1ba;">Threshold: {pressure_max} PSI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card" style="padding:12px;border-radius:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:0.8rem;color:#8fa1ba;">Temperature</div>
                <div style="font-size:1.4rem;font-weight:700;color:#e8f0ff;">{temp:.1f} °C</div>
                <div style="font-size:0.75rem;color:#ffbf69;">{temp_status}</div>
                <div style="font-size:0.65rem;color:#8fa1ba;">Threshold: {temp_max} °C</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card" style="padding:12px;border-radius:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:0.8rem;color:#8fa1ba;">Flow Rate</div>
                <div style="font-size:1.4rem;font-weight:700;color:#e8f0ff;">{flow:.1f} L/min</div>
                <div style="font-size:0.75rem;color:#4fe3b2;">{flow_status}</div>
                <div style="font-size:0.65rem;color:#8fa1ba;">Threshold: {flow_min} L/min</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card" style="padding:12px;border-radius:12px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:0.8rem;color:#8fa1ba;">Vibration</div>
                <div style="font-size:1.4rem;font-weight:700;color:#e8f0ff;">{vibration:.1f} mm/s</div>
                <div style="font-size:0.75rem;color:#ff718d;">{vibration_status}</div>
                <div style="font-size:0.65rem;color:#8fa1ba;">Threshold: {vib_max} mm/s</div>
            </div>
            """,
            unsafe_allow_html=True,
        )