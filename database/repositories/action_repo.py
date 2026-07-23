from database.models import ActionDB


class ActionRepository:

    def __init__(self, session):
        self.session = session

    def create(self, action):
        self.session.add(action)
        self.session.commit()
        self.session.refresh(action)
        return action

    def create_many(self, actions):
        if not actions:
            return []
        self.session.add_all(actions)
        self.session.commit()
        return actions

    def get_recent(self, limit=100):
        return (
            self.session.query(ActionDB)
            .order_by(ActionDB.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_pending(self):
        return (
            self.session.query(ActionDB)
            .filter(ActionDB.status == "pending_approval")
            .order_by(ActionDB.created_at.desc())
            .all()
        )

    def get(self, action_id):
        return self.session.query(ActionDB).filter_by(id=action_id).first()

    def save(self, action):
        self.session.add(action)
        self.session.commit()
        self.session.refresh(action)
        return action
