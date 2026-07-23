import streamlit as st


def render_agent_card(report):

    text = report.final_summary.lower()

    if "[safety]" in text:
        agent_name = "🛡 Safety Agent"

    elif "[diagnostic]" in text:
        agent_name = "🔍 Diagnostic Agent"

    elif "[knowledge]" in text:
        agent_name = "📚 Knowledge Agent"

    else:
        agent_name = "🤖 AI Agent"


    cleaned = (
        report.final_summary
        .replace("[safety]", "")
        .replace("[diagnostic]", "")
        .replace("[knowledge]", "")
    )


    st.markdown(
        f"""
        <div class="agent-card">

        <h3>{agent_name}</h3>

        <p>
        {cleaned}
        </p>

        <b>Status:</b> Completed ✅

        </div>
        """,
        unsafe_allow_html=True
    )