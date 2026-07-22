import streamlit as st


st.title("🤖 AI Agent Network")


agents = [
    "🦺 Safety Agent",
    "🔧 Maintenance Agent",
    "📚 Knowledge Agent",
    "⚙️ Production Agent",
    "📜 Compliance Agent",
    "🌦️ Weather Agent",
    "👷 Incident Commander"
]


for agent in agents:

    st.success(
        f"{agent} - ACTIVE"
    )