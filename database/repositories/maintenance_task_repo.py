from database.models import MaintenanceTaskDB


class MaintenanceTaskRepository:

    def __init__(self, session):
        self.session = session

    def create_many(self, tasks):
        if not tasks:
            return []
        self.session.add_all(tasks)
        self.session.commit()
        return tasks

    def get_recent(self, limit=200):
        return (
            self.session.query(MaintenanceTaskDB)
            .order_by(MaintenanceTaskDB.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_asset(self, asset_id, limit=100):
        return (
            self.session.query(MaintenanceTaskDB)
            .filter(MaintenanceTaskDB.asset_id == asset_id)
            .order_by(MaintenanceTaskDB.created_at.desc())
            .limit(limit)
            .all()
        )
