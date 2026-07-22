import streamlit as st


st.set_page_config(
    page_title="RigOS",
    page_icon="🏭",
    layout="wide"
)


# ---------------------------
# Theme
# ---------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #0b1220;
    }


    .card {

        background-color: #111827;

        padding: 20px;

        border-radius: 15px;

        border: 1px solid #263244;

        margin-bottom: 15px;

    }


    .title {

        font-size: 40px;

        font-weight: 700;

    }


    .subtitle {

        color: #9ca3af;

        font-size: 18px;

    }


    </style>

    """,
    unsafe_allow_html=True
)



# ---------------------------
# Header
# ---------------------------

st.markdown(
    """
    <div class="title">
    🏭 RigOS AI Operations Center
    </div>

    <div class="subtitle">
    Autonomous Industrial Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()



# ---------------------------
# Top Metrics
# ---------------------------


col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(
        "Facility Status",
        "🟢 ONLINE"
    )


with col2:

    st.metric(
        "Assets",
        "12"
    )


with col3:

    st.metric(
        "Active Incidents",
        "2"
    )


with col4:

    st.metric(
        "AI Agents",
        "7"
    )



st.divider()



# ---------------------------
# Asset Overview
# ---------------------------


st.subheader("🏭 Asset Overview")


assets = [

    {
        "name":"Pump A",
        "health":"85%",
        "status":"🟢 Running"
    },

    {
        "name":"Pump B",
        "health":"72%",
        "status":"🟡 Warning"
    },

    {
        "name":"Tank A",
        "health":"100%",
        "status":"🟢 Running"
    }

]



cols = st.columns(3)


for i, asset in enumerate(assets):

    with cols[i]:

        st.markdown(
            f"""
            <div class="card">

            <h3>{asset["name"]}</h3>

            <h2>{asset["health"]}</h2>

            <p>
            Status:
            {asset["status"]}
            </p>

            </div>

            """,
            unsafe_allow_html=True
        )



st.divider()



# ---------------------------
# Incident Feed
# ---------------------------


st.subheader("🚨 Recent Incidents")


incidents = [

    "Pressure Spike detected - Pump A",

    "High Temperature warning - Pump B",

    "Gas level anomaly - Tank A"

]


for incident in incidents:

    st.warning(
        incident
    )



st.divider()



# ---------------------------
# Agent Network
# ---------------------------


st.subheader("🤖 AI Agent Network")


agents = [

    ("🦺 Safety Agent","ACTIVE"),

    ("🔧 Maintenance Agent","MONITORING"),

    ("📚 Knowledge Agent","READY"),

    ("⚙️ Production Agent","READY"),

    ("👷 Incident Commander","AVAILABLE")

]


agent_cols = st.columns(3)



for i, agent in enumerate(agents):

    with agent_cols[i % 3]:

        st.markdown(
            f"""
            <div class="card">

            <h4>{agent[0]}</h4>

            <p>
            Status:
            🟢 {agent[1]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )



st.divider()



# ---------------------------
# AI Summary
# ---------------------------


st.subheader("🧠 AI System Summary")


st.info(
    """
RigOS continuously monitors industrial assets,
detects anomalies, coordinates AI agents,
retrieves operational knowledge,
and generates automated response plans.
"""
)