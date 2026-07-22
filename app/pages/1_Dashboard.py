import streamlit as st
from ui_helpers import activity_items, metric_card, mock_assets, mock_incidents, page_heading, render_sidebar, setup_page, trend_series

setup_page("Dashboard")
render_sidebar("Executive Dashboard")
page_heading("OVERVIEW", "Operations Dashboard", "Real-time operational intelligence across the facility.")

for col, args in zip(st.columns(4), [("Fleet health", "88.4%", "+2.1% vs. prior shift", "green"), ("Assets online", "42 / 45", "3 under attention", "cyan"), ("Active incidents", "03", "1 requires escalation", "red"), ("AI decisions", "128", "94.6% confidence", "violet")]):
    with col: metric_card(*args)

st.write("")
left, right = st.columns([1.65, 1])
with left:
    st.markdown("<div class='section-label'>24-HOUR OPERATIONAL HEALTH</div>", unsafe_allow_html=True)
    st.line_chart(trend_series(), color=["#55D6FF", "#9B8CFF"], height=280)
with right:
    st.markdown("<div class='section-label'>ATTENTION QUEUE</div>", unsafe_allow_html=True)
    for item in mock_incidents():
        st.markdown(f"<div class='panel'><b>{item['Incident']}</b><br><span class='muted'>{item['Asset']} • {item['Severity']} • {item['Detected']}</span></div>", unsafe_allow_html=True)
        st.write("")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>ASSET WATCHLIST</div>", unsafe_allow_html=True)
    st.dataframe(mock_assets(), hide_index=True, use_container_width=True, height=245)
with right:
    st.markdown("<div class='section-label'>LIVE ACTIVITY</div>", unsafe_allow_html=True)
    for time, actor, text in activity_items():
        st.markdown(f"**{time} · {actor}**  \n<span class='muted'>{text}</span>", unsafe_allow_html=True)
