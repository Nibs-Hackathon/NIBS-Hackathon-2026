from database.models import AssetDB



class AssetRepository:


    def __init__(self, session):

        self.session = session



    def create(self, asset):

        self.session.add(asset)

        self.session.commit()

        return asset



    def get_all(self):

        return (
            self.session
            .query(AssetDB)
            .all()
        )



    def get(
        self,
        asset_id
    ):

        return (
            self.session
            .query(AssetDB)
            .filter_by(
                id=asset_id
            )
            .first()
        )