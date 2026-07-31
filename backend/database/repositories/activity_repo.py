from database.models import ActivityEventDB


class ActivityRepository:

    def __init__(self, session):
        self.session = session

    def create(self, activity):
        self.session.add(activity)
        self.session.commit()
        self.session.refresh(activity)
        return activity

    def get_recent(self, limit=200):
        return (
            self.session.query(ActivityEventDB)
            .order_by(ActivityEventDB.created_at.desc())
            .limit(limit)
            .all()
        )
