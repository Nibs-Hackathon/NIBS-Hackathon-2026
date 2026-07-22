import streamlit as st
import pandas as pd


st.title("🏭 Asset Monitoring")


assets = [
    {
        "Asset": "Pump A",
        "Type": "Pump",
        "Health": 82,
        "Status": "Warning",
        "Location": "Zone A"
    },
    {
        "Asset": "Pump B",
        "Type": "Pump",
        "Health": 100,
        "Status": "Running",
        "Location": "Zone A"
    },
    {
        "Asset": "Tank A",
        "Type": "Tank",
        "Health": 100,
        "Status": "Running",
        "Location": "Zone B"
    }
]


df = pd.DataFrame(assets)


st.dataframe(
    df,
    use_container_width=True
)


st.divider()


selected = st.selectbox(
    "Select Asset",
    df["Asset"]
)


asset = df[
    df["Asset"] == selected
].iloc[0]


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Health",
        f"{asset.Health}%"
    )


with col2:
    st.metric(
        "Status",
        asset.Status
    )


with col3:
    st.metric(
        "Location",
        asset.Location
    )