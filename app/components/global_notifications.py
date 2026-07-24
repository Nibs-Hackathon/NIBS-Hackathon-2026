"""Global notification component - Toast-style notifications from top-right."""

import streamlit as st
from services.notification_service import notification_service, NotificationSeverity


def render_global_notifications():
    """Render toast notifications from top-right that auto-dismiss."""
    
    notifications = notification_service.get_notifications(limit=5, unread_only=True)
    
    if not notifications:
        return
    
    # ✅ FIXED: Proper toast CSS with fixed width
    st.markdown("""
    <style>
    /* ✅ Toast container - fixed position, small width */
    .toast-container {
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 999999;
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-width: 340px;
        width: 340px;
        pointer-events: none;
    }
    .toast-item {
        pointer-events: auto;
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(13, 23, 40, 0.96);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(85, 214, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        animation: toastSlideIn 0.4s ease-out forwards,
                   toastFadeOut 0.4s ease-in 4.0s forwards;
        cursor: pointer;
        overflow: hidden;
    }
    .toast-item:hover { transform: scale(1.02); }
    .toast-item.critical { border-left: 3px solid #ff5555; }
    .toast-item.warning { border-left: 3px solid #ff8844; }
    .toast-item.success { border-left: 3px solid #4fe3b2; }
    .toast-item.info { border-left: 3px solid #55D6FF; }
    
    .toast-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        color: #f5f8ff;
        font-size: 0.82rem;
    }
    .toast-body {
        color: #c0d0e8;
        font-size: 0.75rem;
        line-height: 1.4;
        margin-left: 26px;
        margin-top: 2px;
    }
    .toast-meta {
        color: #8fa1ba;
        font-size: 0.6rem;
        margin-top: 3px;
        margin-left: 26px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .toast-close {
        margin-left: auto;
        background: none;
        border: none;
        color: #8fa1ba;
        cursor: pointer;
        font-size: 0.9rem;
        padding: 0 4px;
    }
    .toast-close:hover { color: #fff; }
    .toast-revenue { color: #ff8844; font-weight: 600; }
    .toast-time { color: #6a7a94; }
    
    @keyframes toastSlideIn {
        0% { opacity: 0; transform: translateX(60px) scale(0.95); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }
    @keyframes toastFadeOut {
        0% { opacity: 1; transform: translateX(0); max-height: 120px; padding: 10px 14px; }
        100% { opacity: 0; transform: translateX(20px); max-height: 0; padding: 0 14px; }
    }
    </style>
    <div class="toast-container" id="toastContainer">
    """, unsafe_allow_html=True)
    
    for n in notifications[:5]:
        sev_class = {
            NotificationSeverity.CRITICAL: "critical",
            NotificationSeverity.WARNING: "warning",
            NotificationSeverity.SUCCESS: "success",
        }.get(n.severity, "info")
        
        icon = {
            NotificationSeverity.CRITICAL: "🔴",
            NotificationSeverity.WARNING: "🟠",
            NotificationSeverity.SUCCESS: "🟢",
        }.get(n.severity, "🔵")
        
        meta_parts = []
        if n.revenue_impact:
            meta_parts.append(f'<span class="toast-revenue">💰 ${n.revenue_impact:,.0f}</span>')
        if n.human_approval_required:
            meta_parts.append('<span style="color:#ff5555;">👤 Approval</span>')
        
        meta_html = ' · '.join(meta_parts) if meta_parts else ''
        time_str = n.timestamp.strftime('%H:%M:%S')
        
        title_short = n.title[:30] + "..." if len(n.title) > 30 else n.title
        msg_short = n.message[:50] + "..." if len(n.message) > 50 else n.message
        
        st.markdown(f"""
        <div class="toast-item {sev_class}" onclick="this.style.display='none'">
            <div class="toast-header">
                <span>{icon}</span>
                <span>{title_short}</span>
                <button class="toast-close" onclick="event.stopPropagation(); this.parentElement.parentElement.style.display='none'">✕</button>
            </div>
            <div class="toast-body">{msg_short}</div>
            <div class="toast-meta">
                <span class="toast-time">⏱️ {time_str}</span>
                {meta_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        notification_service.mark_read(n.id)
    
    st.markdown("</div>", unsafe_allow_html=True)