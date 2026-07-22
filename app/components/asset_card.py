import streamlit as st


def asset_card(
    name,
    health,
    status,
    pressure
):

    color = "🟢"

    if health < 70:
        color="🔴"
    elif health < 90:
        color="🟡"


    st.markdown(
        f"""
        <div class="card">

        <h3>{color} {name}</h3>

        <h2>{health}%</h2>

        <p>Status: {status}</p>

        <p>Pressure: {pressure} PSI</p>

        </div>
        """,
        unsafe_allow_html=True
    )