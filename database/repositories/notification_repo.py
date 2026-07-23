from datetime import datetime

from database.models import NotificationDB


class NotificationRepository:

    def __init__(self, session):
        self.session = session

    def create_many(self, notifications):
        if not notifications:
            return []
        self.session.add_all(notifications)
        self.session.commit()
        return notifications

    def get_recent(self, limit=100):
        return (
            self.session.query(NotificationDB)
            .order_by(NotificationDB.created_at.desc())
            .limit(limit)
            .all()
        )

    def get(self, notification_id):
        return self.session.query(NotificationDB).filter_by(id=notification_id).first()

    def acknowledge(self, notification_id, acknowledged_by):
        notification = self.get(notification_id)
        if notification is None:
            return None
        notification.status = "acknowledged"
        notification.acknowledged_by = acknowledged_by
        notification.acknowledged_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(notification)
        return notification
