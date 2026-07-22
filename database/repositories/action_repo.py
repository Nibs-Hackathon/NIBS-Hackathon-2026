from database.models import ActionDB


class ActionRepository:

    def __init__(self, session):
        self.session = session

    def create(self, action):
        self.session.add(action)
        self.session.commit()
        self.session.refresh(action)
        return action

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
