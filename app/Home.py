import streamlit as st


st.set_page_config(
    page_title="RigOS",
    page_icon="🏭",
    layout="wide"
)


st.title("🏭 RigOS AI Operations Center")

st.subheader(
    "Autonomous Industrial Monitoring Platform"
)


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Facility Status",
        "ONLINE"
    )


with col2:
    st.metric(
        "Active Incidents",
        "2"
    )


with col3:
    st.metric(
        "AI Agents",
        "7 Active"
    )


st.divider()


st.info(
    "Real-time AI monitoring of industrial assets"                                                                                                              
    )