from models.asset import Asset


class AssetService:

    def __init__(self):

        self.assets = {}

    def register(self, asset: Asset):

        self.assets[asset.id] = asset

    def get(self, asset_id):

        return self.assets.get(asset_id)

    def update_health(self, asset_id, health):

        asset = self.get(asset_id)

        if asset:
            asset.health = health

    def update_status(self, asset_id, status):

        asset = self.get(asset_id)

        if asset:
            asset.status = status

    def all(self):

        return list(self.assets.values())