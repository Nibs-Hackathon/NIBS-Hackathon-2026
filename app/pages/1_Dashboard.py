import streamlit as st


st.title("📊 Facility Dashboard")


assets = [
    {
        "name":"Pump A",
        "health":82,
        "status":"Warning"
    },
    {
        "name":"Pump B",
        "health":100,
        "status":"Running"
    }
]


for asset in assets:

    st.subheader(asset["name"])

    c1,c2 = st.columns(2)

    with c1:
        st.metric(
            "Health",
            f'{asset["health"]}%'
        )

    with c2:
        st.metric(
            "Status",
            asset["status"]
        )