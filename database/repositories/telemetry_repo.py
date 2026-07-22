from database.models import TelemetryDB


class TelemetryRepository:


    def __init__(self, session):

        self.session = session



    def create(self, telemetry):

        self.session.add(telemetry)

        self.session.commit()

        return telemetry



    def create_many(self, readings):

        self.session.add_all(readings)

        self.session.commit()

        return readings



    def get_asset_history(
        self,
        asset_id,
        limit=100
    ):

        return (
            self.session
            .query(TelemetryDB)
            .filter(
                TelemetryDB.asset_id == asset_id
            )
            .order_by(
                TelemetryDB.timestamp.desc()
            )
            .limit(limit)
            .all()
        )