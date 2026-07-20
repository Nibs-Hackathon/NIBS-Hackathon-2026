from datetime import datetime
from pydantic import BaseModel

class SensorReading(BaseModel):
    pressure: float
    temperature: float
    flow_rate: float
    vibration: float
    gas_level: float
    timestamp: datetime