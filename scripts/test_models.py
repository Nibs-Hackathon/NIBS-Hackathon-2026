from datetime import datetime
from uuid import uuid4
from models.asset import Asset
from models.enums import AssetStatus, AssetType
from models.sensor import Sensor, SensorType

# ✅ FIXED: Use correct model
sensor = Sensor(
    id=str(uuid4()),
    asset_id="PUMP-001",
    sensor_type=SensorType.PRESSURE,
    value=103.5,
    unit="PSI",
    timestamp=datetime.now(),
)

pump = Asset(
    id="PUMP-001",
    name="Main Feed Pump",
    asset_type=AssetType.PUMP,
    location="Zone A",
    health=98.2,
    status="Running",
)

print(pump.model_dump_json(indent=2))