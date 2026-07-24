# Folder: simulator Code Inventory

Generated: 2026-07-24 07:30:05 UTC

Contains 6 project files.

## simulator/asset.py

**File path:** `simulator/asset.py`

```python
import random

from models.asset import Asset
from models.sensor import Sensor, SensorType


class SimulatedAsset:

    def __init__(self, asset: Asset):

        self.asset = asset

        self.sensors = {
            SensorType.PRESSURE: 110,
            SensorType.TEMPERATURE: 70,
            SensorType.FLOW: 60,
            SensorType.VIBRATION: 15,
            SensorType.GAS: 5,
        }


    def tick(self, fault=None):

        telemetry = []

        for sensor, value in self.sensors.items():

            if (
                fault is not None
                and fault["sensor"] == sensor
            ):

                value = fault["value"]

            else:

                value += random.uniform(-2, 2)


            self.sensors[sensor] = value


            telemetry.append(
                Sensor(
                    id=f"{self.asset.id}_{sensor.value}",
                    asset_id=self.asset.id,
                    sensor_type=sensor,
                    value=round(value, 2),
                    unit="",
                )
            )


        return telemetry
```

## simulator/event_generator.py

**File path:** `simulator/event_generator.py`

```python
from mao.events.event import Event
from models.sensor import SensorType


class EventGenerator:

    def generate(self, telemetry):

        events = []

        for reading in telemetry:

            # Pressure
            if (
                reading.sensor_type == SensorType.PRESSURE
                and reading.value > 140
            ):
                events.append(
                    Event(
                        name="PressureSpike",
                        source=reading.asset_id,
                        payload={
                            "pressure": reading.value,
                        },
                    )
                )

            # Temperature
            elif (
                reading.sensor_type == SensorType.TEMPERATURE
                and reading.value > 90
            ):
                events.append(
                    Event(
                        name="HighTemperature",
                        source=reading.asset_id,
                        payload={
                            "temperature": reading.value,
                        },
                    )
                )

            # Gas
            elif (
                reading.sensor_type == SensorType.GAS
                and reading.value > 25
            ):
                events.append(
                    Event(
                        name="GasLeak",
                        source=reading.asset_id,
                        payload={
                            "gas": reading.value,
                        },
                    )
                )

            # Vibration
            elif (
                reading.sensor_type == SensorType.VIBRATION
                and reading.value > 30
            ):
                events.append(
                    Event(
                        name="HighVibration",
                        source=reading.asset_id,
                        payload={
                            "vibration": reading.value,
                        },
                    )
                )

            # Flow
            elif (
                reading.sensor_type == SensorType.FLOW
                and reading.value < 25
            ):
                events.append(
                    Event(
                        name="FlowRestriction",
                        source=reading.asset_id,
                        payload={
                            "flow": reading.value,
                        },
                    )
                )

        return events
```

## simulator/facility.py

**File path:** `simulator/facility.py`

```python
from models.facility import Facility
from simulator.asset import SimulatedAsset
from simulator.fault_injector import FaultInjector
from models.sensor import SensorType


class SimulatedFacility:

    def __init__(self, facility: Facility):

        self.assets = [
            SimulatedAsset(asset)
            for asset in facility.assets
        ]

        self.injector = FaultInjector()

        self.injector.schedule(
            tick=10,
            asset_index=0,
            sensor=SensorType.PRESSURE,
            value=155,
        )

        self.injector.schedule(
            tick=20,
            asset_index=1,
            sensor=SensorType.TEMPERATURE,
            value=95,
        )

        self.injector.schedule(
            tick=30,
            asset_index=2,
            sensor=SensorType.GAS,
            value=35,
        )

        def tick(self, tick_number, fault=None):
            telemetry = []
            for index, asset in enumerate(self.assets):
                # ✅ FIXED: Proper fault assignment
                if fault is not None:
                    current_fault = fault
                else:
                    current_fault = self.injector.get_fault(tick_number, index)
                telemetry.extend(asset.tick(fault=current_fault))
            return telemetry
        self.injector.schedule(
            tick=50,
            asset_index=1,
            sensor=SensorType.FLOW,
            value=15,
        )

    def tick(self, tick_number, fault=None):

        telemetry = []

        for index, asset in enumerate(self.assets):

            if fault and index == 0:
                fault=  fault
            else:
                fault = self.injector.get_fault(
                    tick_number,
                    index
                )

            telemetry.extend(
                asset.tick(
                    fault=fault
                )
            )

        return telemetry
```

## simulator/fault_injector.py

**File path:** `simulator/fault_injector.py`

```python
class FaultInjector:

    def __init__(self):

        self.schedule_map = {}

    def schedule(self, tick, asset_index, sensor, value):

        self.schedule_map[(tick, asset_index)] = {
            "sensor": sensor,
            "value": value,
        }

    def get_fault(self, tick, asset_index):

        return self.schedule_map.get((tick, asset_index))
```

## simulator/sensor.py

**File path:** `simulator/sensor.py`

```python

```

## simulator/simulator.py

**File path:** `simulator/simulator.py`

```python
from simulator.event_generator import EventGenerator
from services.persistence import PersistenceService


class Simulator:

    def __init__(self, facility, kernel):

        self.facility = facility
        self.kernel = kernel

        self.state = kernel.state

        self.generator = EventGenerator()

        self.persistence = PersistenceService()


    def tick(self, tick_number,fault=None):

        telemetry = self.facility.tick(tick_number, fault)

        self.state.add_telemetry(telemetry)

        self.persistence.record_telemetry(telemetry)


        # Update asset health

        for asset in self.facility.assets:

            history = self.state.get_history(asset.asset.id)

            health = self.kernel.health.calculate_health(history)


            self.kernel.asset_service.update_health(
                asset.asset.id,
                health,
            )


            if health > 80:
                status = "Running"

            elif health > 50:
                status = "Warning"

            else:
                status = "Critical"


            self.kernel.asset_service.update_status(
                asset.asset.id,
                status,
            )


        # Handle incidents

        reports = []

        events = self.generator.generate(telemetry)


        for event in events:

            report = self.kernel.handle_event(event)

            reports.append(report)


        return telemetry, reports
```
