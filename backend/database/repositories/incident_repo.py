from database.models import IncidentDB



class IncidentRepository:


    def __init__(self, session):

        self.session = session



    def create(self, incident):

        self.session.add(incident)

        self.session.commit()

        return incident



    def get_all(self):

        return (
            self.session
            .query(IncidentDB)
            .order_by(
                IncidentDB.id.desc()
            )
            .all()
        )



    def get_by_asset(
        self,
        asset_id
    ):

        return (
            self.session
            .query(IncidentDB)
            .filter(
                IncidentDB.asset_id == asset_id
            )
            .all()
        )