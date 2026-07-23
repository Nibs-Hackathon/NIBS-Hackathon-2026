import streamlit as st

from frontend_services.notification_adapter import acknowledge_notification, get_notifications
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Notification Center")
render_sidebar("Notification Center")
page_heading("OPERATOR NOTIFICATIONS", "Notification Center", "Persisted MAO notifications requiring operator awareness or acknowledgement.")

notifications, warning = get_notifications()
if warning:
    st.warning(warning)

pending = sum(notification["Status"].lower() != "acknowledged" for notification in notifications)
critical = sum(notification["Severity"].lower() == "critical" for notification in notifications)
approvals = sum(notification["Requires approval"] == "Yes" for notification in notifications)
for col, args in zip(
    st.columns(4),
    [
        ("Notifications", str(len(notifications)), "Persisted notification register", "cyan"),
        ("Pending acknowledgement", str(pending), "Awaiting operator review", "amber"),
        ("Critical", str(critical), "Severity classification", "red"),
        ("Approval required", str(approvals), "Human approval flag", "violet"),
    ],
):
    with col:
        metric_card(*args)

if not notifications:
    st.info("No persisted notifications are available. NotificationAgent outputs will appear here after a workflow runs.")
    st.stop()

severity = st.selectbox("Severity", ["All severities"] + sorted({item["Severity"] for item in notifications}))
visible = [
    item for item in notifications if severity == "All severities" or item["Severity"] == severity
]
st.markdown("<div class='section-label'>NOTIFICATION REGISTER</div>", unsafe_allow_html=True)
st.dataframe(visible, hide_index=True, height=300, column_config={"Message": st.column_config.TextColumn("Message", width="large")})

pending_items = [item for item in visible if item["Status"].lower() != "acknowledged"]
if pending_items:
    st.markdown("<div class='section-label'>ACKNOWLEDGE NOTIFICATION</div>", unsafe_allow_html=True)
    selected = st.selectbox(
        "Notification",
        pending_items,
        format_func=lambda item: f"{item['Severity']} · {item['Source']} · {item['Time']}",
    )
    operator = st.text_input("Operator name", value="Operator")
    if st.button("Acknowledge selected notification", width="stretch"):
        success, message = acknowledge_notification(selected["id"], operator)
        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)
else:
    st.success("All notifications in this view have been acknowledged.")

st.markdown("<div class='section-label'>LATEST NOTIFICATION</div>", unsafe_allow_html=True)
latest = visible[0] if visible else notifications[0]
st.markdown(
    f"<div class='panel'><b>{latest['Source']}</b> &nbsp; {status_chip(latest['Severity'])} "
    f"{status_chip(latest['Status'])}<p>{latest['Message']}</p><span class='muted'>"
    f"Asset: {latest['Asset']} · {latest['Time']} · {latest['Acknowledged by']}</span></div>",
    unsafe_allow_html=True,
)
