"""Real-time notification service."""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class NotificationType(str, Enum):
    INCIDENT_DETECTED = "incident_detected"
    AGENTS_WORKING = "agents_working"
    AGENTS_COMPLETE = "agents_complete"
    INCIDENT_RESOLVED = "incident_resolved"
    MAINTENANCE_SCHEDULED = "maintenance_scheduled"
    REVENUE_IMPACT = "revenue_impact"


class NotificationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"


@dataclass
class Notification:
    id: str
    type: NotificationType
    severity: NotificationSeverity
    title: str
    message: str
    asset_id: Optional[str] = None
    asset_name: Optional[str] = None
    incident_type: Optional[str] = None
    revenue_impact: Optional[float] = None
    maintenance_scheduled: Optional[str] = None
    human_approval_required: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False
    metadata: dict = field(default_factory=dict)


class NotificationService:
    _instance = None
    _notifications: List[Notification] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def add_notification(self, notification: Notification) -> None:
        self._notifications.insert(0, notification)
        if len(self._notifications) > 100:
            self._notifications = self._notifications[:100]
        print(f"🔔 NOTIFICATION: {notification.title} - {notification.message}")
    
    def get_notifications(self, limit: int = 20, unread_only: bool = False) -> List[Notification]:
        notifications = self._notifications
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        return notifications[:limit]
    
    def mark_read(self, notification_id: str) -> None:
        for n in self._notifications:
            if n.id == notification_id:
                n.read = True
                break
    
    def mark_all_read(self) -> None:
        for n in self._notifications:
            n.read = True
    
    def get_unread_count(self) -> int:
        return len([n for n in self._notifications if not n.read])


notification_service = NotificationService()