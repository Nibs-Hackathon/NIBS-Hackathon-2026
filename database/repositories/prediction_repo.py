from database.models import PredictionDB


class PredictionRepository:

    def __init__(self, session):
        self.session = session

    def create_many(self, predictions):
        if not predictions:
            return []
        self.session.add_all(predictions)
        self.session.commit()
        return predictions

    def get_recent(self, limit=100):
        return (
            self.session.query(PredictionDB)
            .order_by(PredictionDB.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_asset(self, asset_id, limit=100):
        return (
            self.session.query(PredictionDB)
            .filter(PredictionDB.asset_id == asset_id)
            .order_by(PredictionDB.created_at.desc())
            .limit(limit)
            .all()
        )
