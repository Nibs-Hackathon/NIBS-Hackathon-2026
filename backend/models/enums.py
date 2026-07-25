from enum import Enum

class AssetType(str, Enum):
    PUMP = "Pump"
    COMPRESSOR = "Compressor"
    PIPELINE = "Pipeline"
    VALVE = "Valve"
    TANK = "Tank"
    HEAT_EXCHANGER = "Heat Exchanger"
    DRILL = "Drill"

class AssetStatus(str, Enum):
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"
    OFFLINE = "Offline"
    
class IncidentSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class FacilityStatus(str, Enum):
    RUNNING = "Running"
    MAINTENANCE = "Maintenance"
    SHUTDOWN = "Shutdown"
    EMERGENCY = "Emergency"