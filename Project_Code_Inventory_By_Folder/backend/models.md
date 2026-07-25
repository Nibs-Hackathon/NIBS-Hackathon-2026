# Folder: backend/models Code Inventory

Generated: 2026-07-25T06:14:25 UTC

Contains 12 project files.

## backend/models/__init__.py

**Folder path:** `backend/models`

**File path:** `backend/models/__init__.py`

```python

```

## backend/models/asset.py

**Folder path:** `backend/models`

**File path:** `backend/models/asset.py`

```python
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional, List


class AssetType(str, Enum):
    PUMP = "Pump"
    COMPRESSOR = "Compressor"
    PIPELINE = "Pipeline"
    VALVE = "Valve"
    TANK = "Tank"
    HEAT_EXCHANGER = "Heat Exchanger"
    REACTOR = "Reactor"
    DISTILLATION_COLUMN = "Distillation Column"
    BOILER = "Boiler"
    TURBINE = "Turbine"
    MOTOR = "Motor"
    GENERATOR = "Generator"
    HVAC = "HVAC"


class AssetStatus(str, Enum):
    RUNNING = "Running"
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"
    OFFLINE = "Offline"
    MAINTENANCE = "Maintenance"


class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    asset_type: AssetType
    refinery_id: str  # ✅ Link to refinery
    location: str
    zone: str = "Unassigned"
    health: float = 100.0
    status: str = "Running"
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class Refinery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    location: str
    assets: List[Asset] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "Active"
    metadata: dict = Field(default_factory=dict)
```

## backend/models/base.py

**Folder path:** `backend/models`

**File path:** `backend/models/base.py`

```python
"""Unified base models - single source of truth."""

from enum import Enum
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field
from uuid import uuid4


class AssetType(str, Enum):
    PUMP = "Pump"
    COMPRESSOR = "Compressor"
    PIPELINE = "Pipeline"
    VALVE = "Valve"
    TANK = "Tank"
    HEAT_EXCHANGER = "Heat Exchanger"
    REACTOR = "Reactor"
    DISTILLATION_COLUMN = "Distillation Column"
    BOILER = "Boiler"
    TURBINE = "Turbine"
    MOTOR = "Motor"
    GENERATOR = "Generator"
    HVAC = "HVAC"


class AssetStatus(str, Enum):
    RUNNING = "Running"
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"
    OFFLINE = "Offline"
    MAINTENANCE = "Maintenance"


class SensorType(str, Enum):
    PRESSURE = "Pressure"
    TEMPERATURE = "Temperature"
    FLOW = "Flow"
    VIBRATION = "Vibration"
    GAS = "Gas"


class IncidentSeverity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Asset(BaseModel):
    """Single source of truth for Asset model."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    asset_type: AssetType
    refinery_id: Optional[str] = None
    location: str = ""
    zone: str = "Unassigned"
    health: float = 100.0
    status: str = "Running"
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class SensorReading(BaseModel):
    """Single source of truth for Sensor reading."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    asset_id: str
    sensor_type: SensorType
    value: float
    unit: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


class Refinery(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    location: str = ""
    assets: List[Asset] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "Active"
    metadata: dict = Field(default_factory=dict)
```

## backend/models/enums.py

**Folder path:** `backend/models`

**File path:** `backend/models/enums.py`

```python
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
```

## backend/models/event.py

**Folder path:** `backend/models`

**File path:** `backend/models/event.py`

```python

```

## backend/models/facility.py

**Folder path:** `backend/models`

**File path:** `backend/models/facility.py`

```python
from pydantic import BaseModel
from models.asset import Asset

class Facility(BaseModel):
    id:str
    name:str
    assets:list[Asset]
```

## backend/models/incident.py

**Folder path:** `backend/models`

**File path:** `backend/models/incident.py`

```python
from datetime import datetime

from pydantic import BaseModel

from models.enums import IncidentSeverity


class Incident(BaseModel):
    id: str

    asset_id: str

    title: str

    description: str

    severity: IncidentSeverity

    detected_at: datetime

    resolved: bool = False
```

## backend/models/maintenance.py

**Folder path:** `backend/models`

**File path:** `backend/models/maintenance.py`

```python

```

## backend/models/pipeline.py

**Folder path:** `backend/models`

**File path:** `backend/models/pipeline.py`

```python

```

## backend/models/report.py

**Folder path:** `backend/models`

**File path:** `backend/models/report.py`

```python
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from mao.models.result import AgentResult


class ExecutionReport(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    event_name: str

    workflow: str

    success: bool = True

    final_summary: str = ""

    started_at: datetime = Field(default_factory=datetime.now)

    finished_at: datetime = Field(default_factory=datetime.now)

    agent_results: list[AgentResult] = Field(default_factory=list)

    metadata: dict = Field(default_factory=dict)
```

## backend/models/sensor.py

**Folder path:** `backend/models`

**File path:** `backend/models/sensor.py`

```python
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field

class SensorType(str, Enum):
    PRESSURE = "Pressure"
    TEMPERATURE = "Temperature"
    FLOW = "Flow"
    VIBRATION = "Vibration"
    GAS = "Gas"

class Sensor(BaseModel):
    id: str
    asset_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=datetime.now)
```

## backend/models/worker.py

**Folder path:** `backend/models`

**File path:** `backend/models/worker.py`

```python

```
