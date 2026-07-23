"""Shared presentation and placeholder-data utilities for the Streamlit UI.

This module deliberately has no backend imports so each page remains runnable while
the Operations Center integration layer is being designed.
"""

from __future__ import annotations

import base64
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from random import Random

import streamlit as st
from streamlit.components.v1 import html as component_html

# Streamlit launched with ``streamlit run app/Home.py`` puts ``app/`` on
# sys.path. Use a frontend-specific package name to avoid shadowing the
# repository's backend ``services`` package.
from frontend_services.knowledge_agent_adapter import (
    KnowledgeAgentUnavailable,
    ask_knowledge_agent,
    is_operational_query,
)


COLORS = {
    "cyan": "#55D6FF",
    "violet": "#9B8CFF",
    "green": "#4FE3B2",
    "amber": "#FFBF69",
    "red": "#FF718D",
    "muted": "#8FA1BA",
}


@lru_cache(maxsize=1)
def nex_mascot_data_url() -> str:
    """Return the packaged NEX concept asset as a browser-safe data URL."""
    asset_path = Path(__file__).resolve().parent / "assets" / "nex_mascot.png"
    encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def setup_page(title: str, icon: str = "◈") -> None:
    """Configure a page and apply the shared enterprise dark visual system."""
    st.set_page_config(page_title=f"{title} | NIBS Ops", page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: radial-gradient(circle at 85% -10%, #182e52 0, #0b1220 34%, #070b13 72%); color: #e8f0ff; }
        [data-testid="stHeader"] { background: rgba(7, 11, 19, .78); backdrop-filter: blur(18px); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #101b30 0%, #090f1d 100%); border-right: 1px solid rgba(123, 160, 207, .14); }
        [data-testid="stSidebar"] * { color: #dce8fa; }
        [data-testid="stSidebarNav"] { padding-top: .7rem; }
        [data-testid="stSidebarNav"] a { border-radius: 10px; margin: 2px 8px; padding: 8px 10px; }
        [data-testid="stSidebarNav"] a:hover { background: rgba(85,214,255,.10); }
        .ops-brand { font-size: .74rem; letter-spacing: .22em; color: #55d6ff; font-weight: 800; }
        .ops-title { font-size: 1.6rem; font-weight: 750; margin: .15rem 0 .1rem; color: #f4f8ff; }
        .ops-subtitle, .muted { color: #8fa1ba; }
        .section-label { color: #55d6ff; font-size: .72rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .25rem; }
        .metric-card { background: linear-gradient(145deg, rgba(25,42,70,.88), rgba(13,22,39,.88)); border: 1px solid rgba(129,172,226,.16); border-radius: 16px; padding: 1rem 1.1rem; min-height: 116px; box-shadow: 0 12px 32px rgba(0,0,0,.18); }
        .metric-card, .panel { transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease; backdrop-filter: blur(14px); }
        .metric-card:hover, .panel:hover { transform: translateY(-2px); border-color: rgba(85,214,255,.38); box-shadow: 0 16px 36px rgba(0,0,0,.24); }
        .metric-value { font-size: 1.65rem; font-weight: 760; color: #f5f8ff; margin: .15rem 0; }
        .metric-label { color: #9badc5; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }
        .metric-delta { font-size: .78rem; font-weight: 650; }
        .panel { background: rgba(15,27,47,.76); border: 1px solid rgba(129,172,226,.14); border-radius: 15px; padding: 1rem 1.1rem; }
        .status { display: inline-block; border-radius: 999px; padding: .22rem .6rem; font-size: .72rem; font-weight: 750; letter-spacing: .04em; }
        .status-healthy, .status-running, .status-resolved { color:#6af0c2; background:rgba(79,227,178,.13); border:1px solid rgba(79,227,178,.3); }
        .status-warning, .status-pending { color:#ffd184; background:rgba(255,191,105,.13); border:1px solid rgba(255,191,105,.28); }
        .status-critical, .status-offline { color:#ff91a5; background:rgba(255,113,141,.13); border:1px solid rgba(255,113,141,.28); }
        .status-info { color:#8fe6ff; background:rgba(85,214,255,.13); border:1px solid rgba(85,214,255,.28); }
        .pulse { animation: pulse 1.8s ease-in-out infinite; } @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .38; } }
        .gauge { width: 128px; height: 128px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:.4rem auto; }
        .gauge-inner { width:98px; height:98px; border-radius:50%; background:#0d1728; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .timeline-row { display:grid; grid-template-columns:70px 24px 1fr; gap:10px; align-items:start; margin:.4rem 0; }
        .timeline-dot { width:13px; height:13px; border-radius:50%; background:#55d6ff; box-shadow:0 0 14px #55d6ff; margin-top:5px; }
        .twin-tile { min-height:172px; position:relative; overflow:hidden; }
        .stButton > button { border-radius: 9px; border: 1px solid rgba(85,214,255,.45); background: linear-gradient(135deg,#1686b8,#5664c9); color:#fff; font-weight:650; }
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div { background:#101d31 !important; border-color:#284569 !important; color:#e8f0ff !important; }
        [data-testid="stDataFrame"] { border: 1px solid rgba(129,172,226,.14); border-radius: 12px; overflow: hidden; }
        /* NEX is the global entry point; the legacy route remains directly addressable. */
        [data-testid="stSidebarNav"] a[href*="AI_Assistant"] { display: none !important; }
        .st-key-nex-launcher { position:fixed; left:18px; bottom:18px; z-index:10001; width:86px; height:86px; animation:nex-roam 13s cubic-bezier(.45,.05,.55,.95) infinite; will-change:transform; }
        .st-key-nex-launcher > div { height:100%; }
        .st-key-nex-launcher button { position:relative; width:82px !important; height:82px !important; min-height:82px !important; padding:0 !important; overflow:visible; border:0 !important; border-radius:50% !important; font-size:0 !important; background:radial-gradient(circle at 49% 43%,#fcfeff 0 28%,#c9d3df 29% 48%,#2b3747 49% 67%,#101a29 68% 100%) !important; box-shadow:0 10px 22px rgba(0,0,0,.42),0 0 24px rgba(85,214,255,.34),inset 0 2px 3px rgba(255,255,255,.7) !important; transform:translateZ(0); transition:transform .25s ease,box-shadow .25s ease,filter .25s ease; animation:nex-hover 4.2s ease-in-out infinite; will-change:transform; }
        .st-key-nex-launcher button::before { content:''; position:absolute; width:29px; height:29px; left:26px; top:25px; border-radius:50%; background:radial-gradient(circle at 42% 42%,#fff 0 9%,#c7fbff 10% 17%,#46dbff 18% 33%,#0c536f 34% 62%,#020d16 63%); box-shadow:0 0 9px #75ecff,0 0 22px rgba(85,214,255,.85); animation:nex-eye-idle 3s ease-in-out infinite; }
        .st-key-nex-launcher button::after { content:'COMMAND NEXUS\\A Click to open AI Assistant'; white-space:pre; position:absolute; left:96px; bottom:12px; width:180px; padding:9px 11px; border-radius:10px; color:#dff8ff; background:rgba(11,22,38,.92); border:1px solid rgba(85,214,255,.34); box-shadow:0 12px 30px rgba(0,0,0,.32); font-size:11px; font-weight:700; letter-spacing:.04em; text-align:left; opacity:0; transform:translateX(-6px); pointer-events:none; transition:opacity .2s ease,transform .2s ease; }
        .st-key-nex-launcher button:hover { transform:scale(1.08) rotate(-2deg); filter:brightness(1.08); box-shadow:0 12px 28px rgba(0,0,0,.45),0 0 36px rgba(85,214,255,.8),inset 0 2px 3px rgba(255,255,255,.78) !important; animation:nex-bounce .55s ease; }
        .st-key-nex-launcher button:hover::after { opacity:1; transform:translateX(0); }
        .st-key-nex-launcher.nex-active button { animation:nex-activate .7s cubic-bezier(.2,.8,.2,1); }
        .st-key-nex-launcher.nex-active button::before { animation:nex-thinking .7s ease-out; }
        .st-key-nex-launcher.nex-sleeping { animation-duration:24s; opacity:.66; }
        .st-key-nex-launcher.nex-sleeping button { animation-duration:8s; filter:saturate(.65); }
        .st-key-nex-launcher.nex-near button { transform:rotate(-2deg) scale(1.04); box-shadow:0 12px 30px rgba(0,0,0,.45),0 0 40px rgba(85,214,255,.85),inset 0 2px 3px rgba(255,255,255,.75) !important; }
        .st-key-nex-launcher.nex-near button::before { animation:none; transform:translate(var(--nex-eye-x,0px),var(--nex-eye-y,0px)); }
        @keyframes nex-roam { 0%,100% { transform:translate3d(0,0,0); } 25% { transform:translate3d(20px,-5px,0); } 50% { transform:translate3d(10px,-14px,0); } 75% { transform:translate3d(27px,-7px,0); } }
        @keyframes nex-hover { 0%,100% { transform:translateY(0) rotate(-1deg); } 50% { transform:translateY(-6px) rotate(2deg); } }
        @keyframes nex-eye-idle { 0%,100% { transform:translate(0,0) scale(1); opacity:.92; } 35% { transform:translate(2px,-1px) scale(1.04); opacity:1; } 70% { transform:translate(-1px,1px) scale(.94); opacity:.88; } }
        @keyframes nex-thinking { 0% { transform:scale(1); } 45% { transform:scale(1.22) rotate(140deg); box-shadow:0 0 18px #8cf5ff,0 0 38px #55d6ff; } 100% { transform:scale(1) rotate(360deg); } }
        @keyframes nex-bounce { 0%,100% { transform:scale(1.08) translateY(0); } 45% { transform:scale(1.11) translateY(-5px); } }
        @keyframes nex-activate { 0% { transform:scale(1); } 42% { transform:scale(1.2); box-shadow:0 0 0 0 rgba(85,214,255,.75),0 0 54px rgba(85,214,255,1); } 100% { transform:scale(1.03); box-shadow:0 0 0 42px rgba(85,214,255,0),0 0 26px rgba(85,214,255,.58); } }
        .st-key-nex-panel { position:fixed; left:112px; bottom:20px; z-index:10000; width:min(430px,calc(100vw - 138px)); max-height:min(670px,calc(100vh - 42px)); padding:0 2px; border:1px solid rgba(109,211,255,.3); border-radius:19px; background:linear-gradient(145deg,rgba(18,35,59,.96),rgba(7,14,27,.98)); box-shadow:0 26px 72px rgba(0,0,0,.54),0 0 34px rgba(58,177,255,.17); backdrop-filter:blur(20px); animation:nex-panel-in .36s cubic-bezier(.2,.85,.22,1); overflow:hidden; }
        .st-key-nex-panel > div { max-height:min(650px,calc(100vh - 56px)); overflow-y:auto; padding:14px 16px 12px; }
        .st-key-nex-panel [data-testid="stChatMessage"] { padding:.4rem .1rem; }
        .st-key-nex-panel [data-testid="stChatInput"] { padding-bottom:0; }
        .st-key-nex-panel .stButton button { font-size:.76rem !important; height:auto !important; min-height:0 !important; padding:.3rem .55rem !important; background:transparent !important; border-color:rgba(143,161,186,.3) !important; box-shadow:none !important; }
        @keyframes nex-panel-in { from { opacity:0; transform:translate3d(10px,12px,0) scale(.95); } to { opacity:1; transform:translate3d(0,0,0) scale(1); } }
        /* Keep Streamlit's dialog itself as the compact floating window.  Styling
           the full-screen dialog host caused its dark backdrop to become a giant panel. */
        [data-testid="stDialog"] {
            position:fixed !important; inset:auto 128px 126px auto !important;
            z-index:999998 !important; display:block !important;
            width:400px !important; max-width:calc(100vw - 152px) !important;
            height:620px !important; max-height:calc(100vh - 150px) !important;
            margin:0 !important; padding:0 !important; background:transparent !important;
            overflow:visible !important;
        }
        [data-testid="stDialog"] [role="dialog"] {
            box-sizing:border-box !important; width:100% !important; max-width:420px !important;
            height:100% !important; max-height:620px !important; margin:0 !important;
            border:1px solid rgba(109,211,255,.34); border-radius:18px !important;
            background:linear-gradient(145deg,rgba(18,35,59,.93),rgba(7,14,27,.97));
            box-shadow:0 26px 72px rgba(0,0,0,.58),0 0 34px rgba(58,177,255,.18);
            backdrop-filter:blur(20px); overflow:hidden !important;
            animation:nex-panel-in .25s cubic-bezier(.2,.85,.22,1) both;
        }
        @media (max-width:700px) {
            [data-testid="stDialog"] { right:106px !important; bottom:106px !important; width:calc(100vw - 122px) !important; max-width:400px !important; height:min(620px,calc(100vh - 126px)) !important; }
            .st-key-nex-launcher { right:8px; bottom:8px; transform:scale(.82); transform-origin:bottom right; }
            .st-key-nex-panel { right:10px; bottom:98px; width:calc(100vw - 20px); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    render_nex_global()


def render_sidebar(active: str) -> None:
    with st.sidebar:
        st.markdown("<div class='ops-brand'>NIBS • AI OPERATIONS</div>", unsafe_allow_html=True)
        st.markdown("<div class='ops-title'>Command Nexus</div>", unsafe_allow_html=True)
        st.caption("Industrial intelligence, unified.")
        st.divider()
        st.markdown("<div class='section-label'>Current workspace</div>", unsafe_allow_html=True)
        st.markdown(f"**{active}**")
        st.markdown("<span class='status status-running'>● SYSTEMS NOMINAL</span>", unsafe_allow_html=True)
        st.divider()
        st.caption("LIVE DEMO ENVIRONMENT")
        st.caption("Data shown is simulated until backend integration is enabled.")


def render_copilot_widget() -> None:
    """Compact copilot that is intentionally available on every Streamlit page."""
    messages = copilot_messages()
    with st.sidebar.expander("✦ AI COPILOT", expanded=False):
        st.caption("Industrial operations copilot")
        for message in messages[-3:]:
            marker = "You" if message["role"] == "user" else "Nexus"
            st.caption(f"**{marker}:** {message['content']}")
        prompts = ["Summarize today's incidents", "Predict asset failures", "Explain system status", "Generate executive report", "Recommend maintenance"]
        prompt = st.selectbox("Suggested prompts", ["Select a prompt…"] + prompts, key="copilot_suggestion")
        typed = st.text_input("Ask Copilot", key="copilot_input", placeholder="Ask about operations")
        if st.button("Send", key="copilot_send", use_container_width=True):
            question = typed if typed.strip() else (prompt if prompt != "Select a prompt…" else "Explain system status")
            append_copilot_backend_exchange(question)
            st.rerun()
    # TODO: Replace direct agent invocation when the backend exposes an approved
    # MAO chat/workflow endpoint connected to the running orchestration process.


def _render_nex_presence_script() -> None:
    """Run lightweight browser-only NEX awareness and sleep behavior."""
    component_html(
        """
        <script>
        (() => {
          const host = window.parent;
          let lastActivity = Date.now();
          let framePending = false;
          const launcher = () => host.document.querySelector('.st-key-nex-launcher');
          const update = (event) => {
            lastActivity = Date.now();
            if (framePending) return;
            framePending = true;
            host.requestAnimationFrame(() => {
              const node = launcher();
              if (!node) { framePending = false; return; }
              const rect = node.getBoundingClientRect();
              const dx = event.clientX - (rect.left + rect.width / 2);
              const dy = event.clientY - (rect.top + rect.height / 2);
              const close = Math.hypot(dx, dy) < 210;
              node.classList.toggle('nex-near', close);
              node.classList.remove('nex-sleeping');
              if (close) {
                const eye = node.querySelector('button');
                if (eye) {
                  eye.style.setProperty('--nex-eye-x', `${Math.max(-3, Math.min(3, dx / 34))}px`);
                  eye.style.setProperty('--nex-eye-y', `${Math.max(-2, Math.min(2, dy / 45))}px`);
                }
              }
              framePending = false;
            });
          };
          host.document.addEventListener('pointermove', update, { passive: true });
          host.setInterval(() => {
            const node = launcher();
            if (node && Date.now() - lastActivity > 60000) node.classList.add('nex-sleeping');
          }, 5000);
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def render_nex_global() -> None:
    """Render the floating NEX launcher and persistent Command Nexus panel."""
    if "nex_panel_open" not in st.session_state:
        st.session_state.nex_panel_open = False

    action = st.query_params.get("nex")
    if action == "open":
        st.session_state.nex_panel_open = True
    elif action == "close":
        st.session_state.nex_panel_open = False

    mascot_url = nex_mascot_data_url()
    # Portal the launcher to document.body so it is a sibling of Streamlit's
    # app root, never a child of the sidebar or another layout block.
    st.html(
        f"""
        <script>
        (() => {{
          const existing = document.getElementById('rigos-nex-overlay-root');
          if (existing) existing.remove();
          const root = document.createElement('div');
          root.id = 'rigos-nex-overlay-root';
          root.innerHTML = `
        <style>
        #rigos-nex-launcher {{
            position: fixed; left: 24px; bottom: 24px; z-index: 999999;
            width: 88px; height: 88px; display: block; overflow: visible;
            animation: rigos-nex-patrol 13s ease-in-out infinite;
            pointer-events: auto;
        }}
        #rigos-nex-launcher a {{ display: block; width: 100%; height: 100%; text-decoration: none; }}
        #rigos-nex-launcher img {{
            width: 84px; height: 84px; object-fit: contain; display: block;
            filter: drop-shadow(0 10px 9px rgba(0,0,0,.46)) drop-shadow(0 0 14px rgba(49,203,255,.72));
            animation: rigos-nex-float 4.2s ease-in-out infinite;
            transition: transform .22s ease, filter .22s ease;
        }}
        #rigos-nex-launcher::after {{
            content: 'Command Nexus — Click to open AI Assistant'; white-space: normal;
            position: absolute; left: 96px; bottom: 14px; width: 180px; padding: 9px 11px;
            border: 1px solid rgba(85,214,255,.36); border-radius: 10px;
            background: rgba(8,19,34,.94); color: #e6f9ff; font: 700 11px/1.45 sans-serif;
            letter-spacing: .04em; opacity: 0; transform: translateX(-6px); pointer-events: none;
            transition: opacity .2s ease, transform .2s ease;
        }}
        #rigos-nex-launcher:hover img {{ transform: scale(1.08) rotate(-2deg); filter: drop-shadow(0 12px 10px rgba(0,0,0,.48)) drop-shadow(0 0 24px rgba(49,203,255,1)); animation: rigos-nex-bounce .55s ease; }}
        #rigos-nex-launcher:hover::after {{ opacity: 1; transform: translateX(0); }}
        @keyframes rigos-nex-patrol {{ 0%,100% {{ transform: translate3d(0,0,0); }} 25% {{ transform: translate3d(17px,-5px,0); }} 50% {{ transform: translate3d(9px,-12px,0); }} 75% {{ transform: translate3d(24px,-6px,0); }} }}
        @keyframes rigos-nex-float {{ 0%,100% {{ transform: translateY(0) rotate(-1deg); }} 50% {{ transform: translateY(-6px) rotate(2deg); }} }}
        @keyframes rigos-nex-bounce {{ 0%,100% {{ transform: scale(1.08) translateY(0); }} 45% {{ transform: scale(1.11) translateY(-5px); }} }}
        @media (max-width:700px) {{ #rigos-nex-launcher {{ left: 7px; bottom: 7px; transform: scale(.84); transform-origin: bottom left; }} }}
        </style>
        <div id="rigos-nex-launcher" role="complementary" aria-label="Command Nexus AI Assistant">
          <a href="?nex=open" aria-label="Open Command Nexus">
            <img src="{mascot_url}" alt="NEX, the Command Nexus companion">
          </a>
        </div>
          `;
          document.body.appendChild(root);
        }})();
        </script>
        """,
        unsafe_allow_javascript=True,
    )

    if not st.session_state.nex_panel_open:
        return
    render_nex_chat_dialog()


@st.dialog("Command Nexus", width="large", dismissible=False)
def render_nex_chat_dialog() -> None:
    """Render the existing chat flow in Streamlit's root-level dialog portal."""
    st.markdown("<div class='section-label'>NEX OPERATIONS COPILOT</div>", unsafe_allow_html=True)
    st.caption("Operational intelligence for the current shift")
    if st.button("Close Command Nexus", key="nex_close"):
        st.session_state.nex_panel_open = False
        st.query_params["nex"] = "close"
        st.rerun()

    for message in copilot_messages()[-8:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    suggestions = [
        "Summarize today's incidents",
        "Predict asset failures",
        "Explain system status",
        "Generate executive report",
        "Recommend maintenance",
    ]
    selected = st.selectbox("Suggested prompt", ["Select a prompt"] + suggestions, key="nex_suggestion")
    use_selected = st.button("Use selected prompt", key="nex_use_suggestion", disabled=selected == "Select a prompt")
    prompt = st.chat_input("Ask Command Nexus...", key="nex_chat_input")
    question = prompt or (selected if use_selected else "")
    if question:
        # Reuse the backend's existing intent classifier so the NEX presentation
        # follows the same routing decision as the adapter. Casual prompts go
        # straight to Gemini without operational UI; refinery prompts retain the
        # operational loading state and KnowledgeAgent/RAG path.
        if is_operational_query(question):
            with st.spinner("NEX is thinking..."):
                append_copilot_backend_exchange(question)
        else:
            append_copilot_backend_exchange(question)
        st.rerun()


def render_nex_global() -> None:
    """Render the reliable fixed NEX fallback without custom portal JavaScript.

    This intentionally replaces the earlier body-portal attempt while the
    overlay is validated in the live application. ``st.html`` places a real
    image element in the Streamlit DOM and CSS fixes it to the viewport.
    """
    if "nex_panel_open" not in st.session_state:
        st.session_state.nex_panel_open = False

    action = st.query_params.get("nex")
    if action == "open":
        st.session_state.nex_panel_open = True
    elif action == "close":
        st.session_state.nex_panel_open = False

    st.html(
        f"""
        <style>
        #rigos-nex-fallback {{
            position: fixed !important; right: 24px !important; left: auto !important; bottom: 24px !important;
            z-index: 999999 !important; display: block !important; visibility: visible !important;
            opacity: 1 !important; overflow: visible !important; width: 88px; height: 88px;
            pointer-events: auto; animation: rigos-nex-fallback-float 4.2s ease-in-out infinite;
        }}
        #rigos-nex-fallback a {{ display: block; width: 100%; height: 100%; }}
        #rigos-nex-fallback img {{ width: 84px; height: 84px; object-fit: contain; display: block; filter: drop-shadow(0 10px 9px rgba(0,0,0,.46)) drop-shadow(0 0 16px rgba(49,203,255,.8)); transition: transform .2s ease, filter .2s ease; }}
        #rigos-nex-fallback:hover img {{ transform: scale(1.08) rotate(-2deg); filter: drop-shadow(0 12px 10px rgba(0,0,0,.48)) drop-shadow(0 0 26px rgba(49,203,255,1)); }}
        @media (max-width:700px) {{ #rigos-nex-fallback {{ right:10px !important; bottom:10px !important; transform:scale(.9); transform-origin:bottom right; }} }}
        @keyframes rigos-nex-fallback-float {{ 0%,100% {{ transform: translateY(0) rotate(-1deg); }} 50% {{ transform: translateY(-6px) rotate(2deg); }} }}
        </style>
        <div id="rigos-nex-fallback" role="complementary" aria-label="Command Nexus AI Assistant">
          <a href="?nex=open" aria-label="Open Command Nexus">
            <img src="{nex_mascot_data_url()}" alt="NEX, the Command Nexus companion">
          </a>
        </div>
        """,
        unsafe_allow_javascript=False,
    )

    if st.session_state.nex_panel_open:
        render_nex_chat_dialog()


def page_heading(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(f"<div class='section-label'>{eyebrow}</div><div class='ops-title'>{title}</div><div class='ops-subtitle'>{subtitle}</div>", unsafe_allow_html=True)
    st.write("")


def metric_card(label: str, value: str, delta: str, tone: str = "green") -> None:
    color = COLORS.get(tone, COLORS["green"])
    st.markdown(
        f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-delta' style='color:{color}'>{delta}</div></div>",
        unsafe_allow_html=True,
    )


def status_chip(status: str) -> str:
    key = status.lower().replace(" ", "-")
    return f"<span class='status status-{key}'>{status.upper()}</span>"


def mock_assets() -> list[dict]:
    return [
        {"Asset": "Pump A-01", "Type": "Centrifugal Pump", "Zone": "Process A", "Health": 96, "Status": "Healthy", "Last telemetry": "12 sec ago"},
        {"Asset": "Compressor C-12", "Type": "Gas Compressor", "Zone": "Process B", "Health": 82, "Status": "Warning", "Last telemetry": "18 sec ago"},
        {"Asset": "Tank T-04", "Type": "Storage Tank", "Zone": "Terminal", "Health": 91, "Status": "Healthy", "Last telemetry": "9 sec ago"},
        {"Asset": "Valve V-09", "Type": "Control Valve", "Zone": "Pipeline", "Health": 68, "Status": "Warning", "Last telemetry": "23 sec ago"},
        {"Asset": "Heat Exchanger H-03", "Type": "Heat Exchanger", "Zone": "Utilities", "Health": 43, "Status": "Critical", "Last telemetry": "31 sec ago"},
    ]


def mock_incidents() -> list[dict]:
    return [
        {"ID": "INC-2048", "Incident": "Elevated vibration", "Asset": "Compressor C-12", "Severity": "High", "Status": "Investigating", "Detected": "08:42"},
        {"ID": "INC-2047", "Incident": "Pressure variance", "Asset": "Valve V-09", "Severity": "Medium", "Status": "Monitoring", "Detected": "08:15"},
        {"ID": "INC-2046", "Incident": "Temperature excursion", "Asset": "Heat Exchanger H-03", "Severity": "Critical", "Status": "Escalated", "Detected": "07:51"},
    ]


def trend_series(points: int = 24, base: int = 88, spread: int = 6) -> dict[str, list[float]]:
    rng = Random(17)
    return {"Asset Health": [round(base + rng.uniform(-spread, spread), 1) for _ in range(points)], "Safety Index": [round(min(100, base + 4 + rng.uniform(-spread, spread)), 1) for _ in range(points)]}


def activity_items() -> list[tuple[str, str, str]]:
    return [
        ("08:42", "Diagnostic agent", "Started vibration root-cause analysis for Compressor C-12."),
        ("08:39", "Safety agent", "Validated operating envelope for Process B."),
        ("08:31", "Telemetry gateway", "Ingested 1,248 sensor readings across 42 assets."),
        ("08:15", "Workflow supervisor", "Closed INC-2043 with monitored recovery plan."),
    ]


# Phase 1 frontend demo contracts. Replace these functions with a frontend
# service adapter once the backend team exposes an approved snapshot endpoint.
# TODO: Expected contract: system metrics, active incidents, assets, and recent
# agent activity from the *running* MAO/simulator process; never create a new kernel here.
def dashboard_demo_snapshot() -> dict:
    return {
        "metrics": [
            ("Fleet health", "88.4%", "+2.1% vs. prior shift", "green"),
            ("Assets online", "42 / 45", "3 under attention", "cyan"),
            ("Active incidents", "03", "1 requires escalation", "red"),
            ("AI decisions", "128", "94.6% confidence", "violet"),
        ],
        "assets": mock_assets(),
        "incidents": mock_incidents(),
        "activity": activity_items(),
    }


def incident_simulator_demo_flow(incident_type: str, asset: str) -> list[tuple[str, str]]:
    """Existing UI-only simulator flow; this function does not submit an event."""
    return [
        ("Detect", f"Synthetic {incident_type.lower()} signal selected for {asset}."),
        ("Triage", "Classify severity, assess the safety envelope, and create an incident record."),
        ("Orchestrate", "Route specialist agents through the matching response workflow."),
        ("Recommend", "Compile evidence, SOP guidance, and recovery actions for operator review."),
    ]


def agent_monitor_demo_agents() -> list[dict]:
    """Current agent-monitor display data, isolated for future MAO registry mapping."""
    return [
        {"Agent": "Safety", "Specialty": "Risk validation", "State": "Active", "Confidence": "96%", "Current task": "Check Compressor C-12"},
        {"Agent": "Diagnostic", "Specialty": "Root-cause analysis", "State": "Active", "Confidence": "95%", "Current task": "Analyze vibration pattern"},
        {"Agent": "Knowledge", "Specialty": "SOP retrieval", "State": "Ready", "Confidence": "93%", "Current task": "Awaiting request"},
        {"Agent": "Maintenance", "Specialty": "Maintenance planning", "State": "Ready", "Confidence": "94%", "Current task": "Awaiting task"},
        {"Agent": "Planning", "Specialty": "Recovery planning", "State": "Queued", "Confidence": "92%", "Current task": "Prepare recovery sequence"},
    ]


# TODO: Map agent_monitor_demo_agents to MAOKernel.registry, scheduler, and
# StateManager report/task data through an approved read-only backend interface.


# Phase 2 frontend demo contracts. These keep current demonstration content in
# one place while defining the data each page will require from a future adapter.
# TODO: Expected asset contract: asset identity/status/health and recent sensor
# telemetry from the running simulator/state manager, exposed read-only.
def asset_monitor_demo_snapshot() -> dict:
    return {
        "assets": mock_assets(),
        "sensors": [
            {"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"},
            {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"},
            {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"},
            {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"},
        ],
    }


# TODO: Expected report contract: execution report id/title/workflow/status,
# generated time, final summary, and recommendations from MAO StateManager.
def reports_demo_snapshot() -> dict:
    return {
        "metrics": [
            ("Reports generated", "128", "+18 today", "cyan"),
            ("Resolved incidents", "41", "92% within target", "green"),
            ("Average response", "4m 18s", "42 sec faster", "green"),
            ("Pending review", "06", "2 high priority", "amber"),
        ],
        "reports": [
            {"Report": "RPT-2048", "Title": "Compressor vibration response", "Workflow": "Maintenance response", "Status": "Pending review", "Generated": recent_dates(1)[0]},
            {"Report": "RPT-2047", "Title": "Valve pressure variance", "Workflow": "Pressure response", "Status": "Completed", "Generated": recent_dates(2)[0]},
            {"Report": "RPT-2046", "Title": "Heat exchanger excursion", "Workflow": "Temperature response", "Status": "Escalated", "Generated": recent_dates(3)[0]},
        ],
        "preview": {
            "Report": "RPT-2048",
            "Title": "Compressor vibration response",
            "Summary": "Diagnostic analysis indicates a likely bearing wear pattern. The recommended action is controlled load reduction followed by inspection within 24 hours.",
            "Recommendation": "Assign maintenance technician and verify suction pressure.",
        },
    }


def copilot_messages() -> list[dict]:
    """Return the persistent UI conversation, initialized with existing demo copy."""
    if "ops_messages" not in st.session_state:
        st.session_state.ops_messages = [{"role": "assistant", "content": "Command Nexus copilot online. Ask for an operational brief or recommendation."}]
    return st.session_state.ops_messages


def copilot_diagnostics() -> list[str]:
    """Return temporary frontend diagnostics for the current Copilot session."""
    if "copilot_diagnostics" not in st.session_state:
        st.session_state.copilot_diagnostics = []
    return st.session_state.copilot_diagnostics


def _record_copilot_diagnostic(message: str, callback=None) -> None:
    entry = f"{datetime.now().strftime('%H:%M:%S')} — {message}"
    diagnostics = copilot_diagnostics()
    diagnostics.append(entry)
    del diagnostics[:-25]
    if callback is not None:
        callback(entry)


def append_copilot_backend_exchange(question: str, diagnostic_callback=None) -> bool:
    """Append an existing KnowledgeAgent answer and retain its execution trace."""
    messages = copilot_messages()
    messages.append({"role": "user", "content": question})
    _record_copilot_diagnostic("Frontend received question; beginning backend request.", diagnostic_callback)
    try:
        answer = ask_knowledge_agent(
            question,
            on_progress=lambda stage: _record_copilot_diagnostic(stage, diagnostic_callback),
        )
    except Exception as error:
        _record_copilot_diagnostic(
            f"Frontend caught {type(error).__name__}: {error}",
            diagnostic_callback,
        )
        answer = "I’m unable to complete that request right now. Please try again shortly."
        messages.append({"role": "assistant", "content": answer})
        return False
    messages.append({"role": "assistant", "content": answer})
    _record_copilot_diagnostic("Assistant answer added to the conversation.", diagnostic_callback)
    return True


# TODO: Route copilot messages through an approved MAO chat/workflow endpoint
# once one exists; retain this thin adapter only until then.


def recent_dates(count: int = 6) -> list[str]:
    return [(datetime.now() - timedelta(days=index)).strftime("%d %b") for index in range(count - 1, -1, -1)]


def prediction_series(points: int = 14) -> dict[str, list[float]]:
    """Deterministic placeholder for projected health and intervention thresholds."""
    rng = Random(41)
    current = 84.0
    health = []
    for _ in range(points):
        current += rng.uniform(-2.8, -0.4)
        health.append(round(current, 1))
    return {"Predicted health": health, "Intervention threshold": [70.0] * points}


def mock_maintenance_tasks() -> list[dict]:
    return [
        {"Priority": "P1", "Asset": "Heat Exchanger H-03", "Work order": "Inspect thermal bypass", "Window": "Today · 14:00", "Owner": "Utilities Crew", "State": "Scheduled"},
        {"Priority": "P2", "Asset": "Compressor C-12", "Work order": "Bearing and vibration inspection", "Window": "Tomorrow · 09:00", "Owner": "Rotating Equipment", "State": "Proposed"},
        {"Priority": "P3", "Asset": "Valve V-09", "Work order": "Calibrate pressure actuator", "Window": "25 Jul · 11:00", "Owner": "Instrumentation", "State": "Planned"},
    ]




def executive_metrics() -> list[tuple[str, str, str, str]]:
    return [
        ("Overall health", "88.4%", "Within mission target", "green"),
        ("Active assets", "42 / 45", "3 under attention", "cyan"),
        ("AI agents", "6 / 6", "All online", "violet"),
        ("Open incidents", "03", "1 critical", "red"),
        ("Predicted failures", "02", "Next 14 days", "amber"),
        ("Safety score", "91.2", "Operating envelope secure", "green"),
        ("Mission status", "STABLE", "Monitored operations", "green"),
        ("System confidence", "94.6%", "Evidence quality high", "cyan"),
    ]


def mock_prediction_profile() -> dict:
    return {
        "health": 82,
        "rul": "43 days",
        "failure_probability": "32%",
        "confidence": "87%",
        "historical": {"Historical health": [96, 95, 95, 93, 92, 91, 90, 88, 87, 85, 84, 82]},
        "telemetry": [
            {"Signal": "Vibration RMS", "Observed": "23.7 mm/s", "Baseline": "15.0 mm/s", "Evidence": "Elevated +58%"},
            {"Signal": "Bearing temperature", "Observed": "78.2 °C", "Baseline": "68.0 °C", "Evidence": "Rising trend"},
            {"Signal": "Runtime since service", "Observed": "4,238 h", "Baseline": "3,600 h", "Evidence": "Past service window"},
        ],
    }


def mock_agent_timeline() -> list[dict]:
    return [
        {"time": "08:42:17", "agent": "Sensor Agent", "action": "Ingested vibration anomaly from Compressor C-12", "state": "Completed", "confidence": "99%", "progress": 100},
        {"time": "08:42:20", "agent": "Prediction Agent", "action": "Calculated 32% failure probability within 14 days", "state": "Completed", "confidence": "87%", "progress": 100},
        {"time": "08:42:25", "agent": "Knowledge Agent", "action": "Retrieved bearing inspection SOP and vibration limits", "state": "Completed", "confidence": "93%", "progress": 100},
        {"time": "08:42:31", "agent": "Planner Agent", "action": "Reserved next rotating-equipment maintenance window", "state": "Running", "confidence": "89%", "progress": 72},
        {"time": "08:42:37", "agent": "Notification Agent", "action": "Prepared operations escalation message", "state": "Queued", "confidence": "96%", "progress": 38},
        {"time": "08:42:42", "agent": "Report Agent", "action": "Compiling executive decision record", "state": "Queued", "confidence": "94%", "progress": 15},
    ]


def mock_twin_assets() -> list[dict]:
    return [
        {"Asset": "Pump A-01", "Category": "Pump", "Zone": "Process A", "Status": "Healthy", "Health": 96, "Temperature": "72 °C", "Pressure": "119 bar", "RPM": "2,960", "Failure": "4%"},
        {"Asset": "Motor M-07", "Category": "Motor", "Zone": "Process A", "Status": "Healthy", "Health": 93, "Temperature": "64 °C", "Pressure": "—", "RPM": "1,485", "Failure": "7%"},
        {"Asset": "Tank T-04", "Category": "Tank", "Zone": "Terminal", "Status": "Healthy", "Health": 91, "Temperature": "38 °C", "Pressure": "4.8 bar", "RPM": "—", "Failure": "9%"},
        {"Asset": "HVAC H-02", "Category": "HVAC", "Zone": "Utilities", "Status": "Warning", "Health": 76, "Temperature": "31 °C", "Pressure": "2.1 bar", "RPM": "1,120", "Failure": "18%"},
        {"Asset": "Generator G-01", "Category": "Generator", "Zone": "Utilities", "Status": "Healthy", "Health": 89, "Temperature": "79 °C", "Pressure": "6.2 bar", "RPM": "1,500", "Failure": "11%"},
        {"Asset": "Pipeline P-03", "Category": "Pipeline", "Zone": "Pipeline", "Status": "Warning", "Health": 68, "Temperature": "46 °C", "Pressure": "137 bar", "RPM": "—", "Failure": "24%"},
        {"Asset": "Compressor C-12", "Category": "Compressor", "Zone": "Process B", "Status": "Warning", "Health": 82, "Temperature": "78 °C", "Pressure": "112 bar", "RPM": "3,585", "Failure": "32%"},
    ]


def gauge_card(label: str, value: int, detail: str, color: str = "#55D6FF") -> None:
    st.markdown(
        f"<div class='panel' style='text-align:center'><div class='metric-label'>{label}</div><div class='gauge' style='background:conic-gradient({color} {value * 3.6}deg, #22344f 0)'><div class='gauge-inner'><b style='font-size:1.45rem'>{value}%</b><span class='muted' style='font-size:.7rem'>score</span></div></div><span class='muted'>{detail}</span></div>",
        unsafe_allow_html=True,
    )


def render_health_heatmap() -> None:
    """Compact CSS heatmap for the executive dashboard; data remains demo-only."""
    cells = [("Process A", "96%", "#4FE3B2"), ("Process B", "82%", "#FFBF69"), ("Terminal", "91%", "#4FE3B2"), ("Pipeline", "68%", "#FFBF69"), ("Utilities", "43%", "#FF718D")]
    blocks = "".join(f"<div style='flex:1;min-width:100px;padding:14px 10px;border-radius:11px;background:{color}20;border:1px solid {color}66'><b>{zone}</b><br><span style='font-size:1.45rem;color:{color}'>{score}</span></div>" for zone, score, color in cells)
    st.markdown(f"<div style='display:flex;gap:10px;flex-wrap:wrap'>{blocks}</div>", unsafe_allow_html=True)
