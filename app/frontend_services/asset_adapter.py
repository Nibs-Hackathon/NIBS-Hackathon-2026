from services.runtime import kernel


def get_assets():

    assets = kernel.asset_service.all_assets()

    return {
        "assets": [
            {
                "id": asset.id,
                "Asset": asset.name,
                "Type": asset.asset_type,
                "Zone": asset.location,
                "Health": asset.health,
                "Status": asset.status,
                "Last telemetry": "N/A",
            }
            for asset in assets
        ],
        "sensors": [],
        "history": []
    }