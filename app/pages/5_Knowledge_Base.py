import streamlit as st


st.set_page_config(
    page_title="Knowledge Base",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AI Knowledge Base")

st.caption(
    "RAG-powered SOP retrieval and industrial knowledge assistant"
)


# Mock retrieved documents
documents = {
    "Pressure Spike": {
        "source": "Pressure Spike SOP",
        "content": """
Immediate Actions:

• Notify control room
• Verify sensor readings
• Reduce pump RPM by 20%
• Check discharge valve position
• Inspect pressure relief valve


Possible Causes:

• Valve blockage
• Pump cavitation
• Closed downstream valve
• Sensor malfunction


Maintenance:

• Inspect seals and bearings
• Check pipeline restrictions
• Verify pressure transmitter calibration
"""
    },


    "Gas Leak": {
        "source": "Gas Leak Emergency Procedure",
        "content": """
Emergency Response:

• Evacuate affected personnel
• Activate emergency ventilation
• Close nearby valves
• Notify emergency response team


Possible Sources:

• Flange leak
• Valve seal failure
• Pipe corrosion
"""
    }
}



st.subheader("🔎 Search SOP Knowledge")


query = st.selectbox(
    "Select Query",
    [
        "Pressure Spike",
        "Gas Leak"
    ]
)



if query:


    result = documents[query]


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Retrieved Document",
            result["source"]
        )


    with col2:

        st.metric(
            "RAG Confidence",
            "95%"
        )



    st.subheader("📄 Retrieved SOP")


    st.text(
        result["content"]
    )



    st.subheader("🤖 AI Assistant Response")


    if query == "Pressure Spike":

        st.success(
            """
Recommended Response:

1. Verify pressure sensor readings.
2. Reduce pump RPM.
3. Inspect valves and bearings.
4. Continue monitoring until pressure stabilizes.
"""
        )


    else:

        st.error(
            """
Emergency Response:

1. Evacuate affected personnel.
2. Activate ventilation.
3. Close nearby valves.
4. Notify emergency response team.
"""
        )



st.divider()


st.subheader("📂 Knowledge Sources")


sources = [
    "Pressure Spike SOP",
    "Gas Leak Emergency Procedure",
    "Maintenance Manual",
    "Safety Guidelines"
]


for source in sources:

    st.write(
        f"📄 {source}"
    )