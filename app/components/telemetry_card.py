import streamlit as st


def render_telemetry():

    st.markdown("### 📊 Live Telemetry")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Pressure</div>
                <div class="metric-value">152 PSI</div>
                <div class="status status-critical">HIGH</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Temperature</div>
                <div class="metric-value">84 °C</div>
                <div class="status status-warning">ELEVATED</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Flow Rate</div>
                <div class="metric-value">310 L/min</div>
                <div class="status status-running">NORMAL</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">AI Status</div>
                <div class="metric-value">Running</div>
                <div class="status status-info">ACTIVE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )