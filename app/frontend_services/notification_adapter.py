"""Notification-center adapter using the existing persisted notification repository."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_session
from database.repositories.notification_repo import NotificationRepository


def _format_notification(notification) -> dict:
    return {
        "id": notification.id,
        "Severity": notification.severity.title(),
        "Time": notification.created_at.strftime("%d %b %H:%M") if notification.created_at else "Not available",
        "Source": notification.source.replace("_", " ").title(),
        "Asset": notification.asset_id or "Not specified",
        "Message": notification.summary,
        "Status": notification.status.replace("_", " ").title(),
        "Acknowledged by": notification.acknowledged_by or "Not acknowledged",
        "Requires approval": "Yes" if notification.requires_human_approval else "No",
    }


def get_notifications(limit: int = 100) -> tuple[list[dict], str | None]:
    """Return persisted notifications and a safe user-facing availability warning."""
    session = None
    try:
        session = get_session()
        notifications = NotificationRepository(session).get_recent(limit)
        return [_format_notification(notification) for notification in notifications], None
    except Exception:
        return [], "Notification persistence is temporarily unavailable."
    finally:
        if session is not None:
            session.close()


def acknowledge_notification(notification_id: str, acknowledged_by: str) -> tuple[bool, str]:
    """Persist an acknowledgement through the existing repository contract."""
    session = None
    try:
        session = get_session()
        notification = NotificationRepository(session).acknowledge(notification_id, acknowledged_by.strip() or "Operator")
        if notification is None:
            return False, "The notification no longer exists. Refresh the register and try again."
        return True, "Notification acknowledged."
    except Exception:
        return False, "Notification acknowledgement is temporarily unavailable."
    finally:
        if session is not None:
            session.close()
