# Folder: services Code Inventory

Generated: 2026-07-24T03:28:50 UTC

Contains 16 project files.

## services/__init__.py

**File path:** `services/__init__.py`

```python

```

## services/asset.py

**File path:** `services/asset.py`

```python
from models.asset import Asset


class AssetService:

    def __init__(self):

        self.assets = {}

    def register(self, asset: Asset):

        self.assets[asset.id] = asset

    def get(self, asset_id):

        return self.assets.get(asset_id)

    def all_assets(self):

        return list(self.assets.values())

    def update_health(self, asset_id, health):

        asset = self.get(asset_id)

        if asset:
            asset.health = health

    def update_status(self, asset_id, status):

        asset = self.get(asset_id)

        if asset:
            asset.status = status
```

## services/embedding.py

**File path:** `services/embedding.py`

```python

```

## services/health.py

**File path:** `services/health.py`

```python
from models.sensor import SensorType


class HealthService:

    """
    Calculates asset health from recent telemetry.
    """

    LIMITS = {
        SensorType.PRESSURE: 150,
        SensorType.TEMPERATURE: 90,
        SensorType.FLOW: 40,
        SensorType.VIBRATION: 25,
        SensorType.GAS: 15,
    }


    def calculate_health(self, readings):

        health = 100.0

        for reading in readings:

            limit = self.LIMITS.get(reading.sensor_type)

            if limit is None:
                continue


            if reading.sensor_type == SensorType.FLOW:

                if reading.value < limit:
                    health -= 5

            else:

                if reading.value > limit:
                    health -= 5


        return max(0.0, health)
```

## services/incident_manager.py

**File path:** `services/incident_manager.py`

```python
from datetime import datetime
from uuid import uuid4

from models.incident import Incident
from models.enums import IncidentSeverity


class IncidentManager:

    def __init__(self):

        self.active = {}
        self.history = []

    def create(self, event):

        incident = Incident(
            id=str(uuid4()),
            asset_id=event.source,
            title=event.name,
            description=str(event.payload),
            severity=IncidentSeverity.HIGH,
            detected_at=datetime.now(),
        )

        self.active[incident.id] = incident

        self.history.append(incident)

        return incident

    def resolve(self, incident_id):

        if incident_id in self.active:

            self.active[incident_id].resolved = True

            del self.active[incident_id]

    def list_active(self):

        return list(self.active.values())
```

## services/incident_service.py

**File path:** `services/incident_service.py`

```python
from models.sensor import SensorType
from services.kernel_factory import get_kernel

class IncidentService:

    def __init__(self, simulator):
        self.simulator = simulator


    def trigger_incident(self, incident_type):

        fault = None

        incident_type = incident_type.lower()


        if incident_type == "pressure spike":

            fault = {
                "sensor": SensorType.PRESSURE,
                "value": 155
            }


        elif incident_type == "gas leak":

            fault = {
                "sensor": SensorType.GAS,
                "value": 30
            }


        elif incident_type == "high vibration":

            fault = {
                "sensor": SensorType.VIBRATION,
                "value": 40
            }


        elif incident_type == "high temperature":

            fault = {
                "sensor": SensorType.TEMPERATURE,
                "value": 95
            }


        elif incident_type == "flow restriction":

            fault = {
                "sensor": SensorType.FLOW,
                "value": 15
            }


        telemetry, reports = self.simulator.tick(
            tick_number=1,
            fault=fault
        )


        return {
            "telemetry": telemetry,
            "reports": reports
        }
```

## services/kernel_factory.py

**File path:** `services/kernel_factory.py`

```python
"""
services/kernel_factory.py

Compatibility access point for the shared MAO kernel.
"""

from mao import MAOKernel
from services.runtime import kernel


def create_kernel() -> MAOKernel:
    """
    Return the already initialized production kernel.
    """

    return kernel



def get_kernel() -> MAOKernel:
    """
    Return the shared MAO kernel instance.
    """

    return kernel
```

## services/llm.py

**File path:** `services/llm.py`

```python
"""
Centralized, failover-safe access to Gemini models.

Supports:
- Local development (.env)
- Streamlit Cloud (st.secrets)
- Multiple API keys with automatic failover
"""

import logging
import os
import socket
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


logger = logging.getLogger(__name__)


# Load local .env
PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(
    PROJECT_ROOT / ".env"
)

SUPPORTED_GEMINI_ENV_VARS = (
    "GEMINI_API_KEY_1",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_KEY_1",
    "GOOGLE_API_KEY_1",
    "GOOGLE_API_KEY_2",
    "GEMINI_API_KEY_2",
)

DEFAULT_GEMINI_MODEL = "gemini-3.6-flash"

_PROXY_ENV_VARS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)
_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _has_invalid_gemini_proxy() -> bool:
    """Return whether this process inherited the known dead loopback proxy.

    The check does not change environment variables.  It only lets the Gemini
    client opt out of proxy inheritance when a request would otherwise be sent
    to the non-listening local port that caused WinError 10061.
    """
    for name in _PROXY_ENV_VARS:
        value = os.getenv(name)
        if not value:
            continue
        try:
            proxy = urlsplit(value)
            if proxy.hostname not in _LOOPBACK_HOSTS or proxy.port is None:
                continue
            # Port 9 is the observed discarded-service proxy. For any other
            # loopback proxy, preserve it only while it has a listener.
            if proxy.port == 9:
                return True
            with socket.create_connection((proxy.hostname, proxy.port), timeout=0.15):
                pass
        except OSError:
            return True
        except ValueError:
            # Preserve normal proxy handling for malformed values rather than
            # making an assumption about a user-managed configuration.
            continue
    return False


def get_gemini_model() -> str:
    """Return the configured Gemini model without exposing credentials."""
    return os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL


class LLMManager:
    """
    Central Gemini router.

    Agents should NEVER directly call Gemini.
    They should use this class.
    """


    def __init__(
        self,
        model_name=None,
    ):

        self.model_name = model_name or get_gemini_model()

        self.keys = self._load_keys()

        self.current_key_index = 0


        if not self.keys:
            raise RuntimeError(
                "No Gemini API key was found. Copy .env.example to .env and "
                "configure one of: " + ", ".join(SUPPORTED_GEMINI_ENV_VARS) + "."
            )


        logger.info(
            "LLMManager initialized with %s Gemini key(s)",
            len(self.keys)
        )


    @staticmethod
    def _load_keys():

        key_names = SUPPORTED_GEMINI_ENV_VARS


        keys = []


        # ---------------------------------
        # Local environment (.env)
        # ---------------------------------

        for name in key_names:

            value = os.getenv(name)

            if value:
                keys.append(value)



        # ---------------------------------
        # Streamlit Cloud secrets
        # ---------------------------------

        try:

            import streamlit as st


            for name in key_names:

                if name in st.secrets:

                    keys.append(
                        st.secrets[name]
                    )


        except Exception:

            # Running outside Streamlit
            pass



        # Remove duplicates
        return list(
            dict.fromkeys(keys)
        )


    def _create_model(self, key):
        # Scope the proxy bypass to the HTTP client created by the Gemini SDK.
        # Do not mutate os.environ: other application clients retain their
        # existing proxy behavior.
        client_args = {"trust_env": False} if _has_invalid_gemini_proxy() else None
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=key,
            client_args=client_args,
        )



    def generate(self, prompt):

        """
        Generate Gemini response.

        Automatically rotates keys if one fails.
        """

        last_error = None


        total_keys = len(self.keys)


        for attempt in range(total_keys):


            index = self.current_key_index


            key = self.keys[index]


            try:

                logger.info(
                    "Using Gemini key %s",
                    index + 1
                )


                response = (
                    self
                    ._create_model(key)
                    .invoke(prompt)
                )


                content = response.content
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    return "".join(
                        part if isinstance(part, str) else part.get("text", "")
                        for part in content
                        if isinstance(part, str) or isinstance(part, dict)
                    )
                return str(content)



            except Exception as error:


                last_error = error


                logger.warning(

                    "Gemini key %s failed. Switching key.",

                    index + 1,

                    exc_info=True
                )


                # Move to next key

                self.current_key_index = (
                    self.current_key_index + 1
                ) % total_keys



        raise RuntimeError(
            "All Gemini API keys failed. "
            "Check quota, permissions, and configuration."
        ) from last_error
```

## services/persistence.py

**File path:** `services/persistence.py`

```python
"""Repository-backed persistence for simulator and MAO lifecycle data."""

import logging

from database.connection import get_session
from database.models import AgentExecutionDB, ExecutionReportDB, IncidentDB, TelemetryDB
from database.repositories.agent_repo import AgentRepository
from database.repositories.incident_repo import IncidentRepository
from database.repositories.report_repo import ReportRepository
from database.repositories.telemetry_repo import TelemetryRepository


logger = logging.getLogger(__name__)


class PersistenceService:

    def record_telemetry(self, readings):
        session = get_session()
        try:
            rows = [
                TelemetryDB(
                    asset_id=reading.asset_id,
                    sensor_type=reading.sensor_type.value,
                    value=reading.value,
                    timestamp=reading.timestamp,
                )
                for reading in readings
            ]
            TelemetryRepository(session).create_many(rows)
        except Exception:
            session.rollback()
            logger.exception("Failed to persist telemetry batch.")
        finally:
            session.close()

    def record_execution(self, event, report, severity="high"):
        session = get_session()
        try:
            incident = IncidentDB(
                id=event.id,
                asset_id=event.source,
                event=event.name,
                severity=severity,
                status="completed" if report.success else "requires_review",
                report=report.final_summary,
                created_at=event.timestamp,
            )
            IncidentRepository(session).create(incident)

            stored_report = ExecutionReportDB(
                id=report.id,
                execution_id=report.execution_id,
                incident_id=event.id,
                workflow=report.workflow_name,
                success=report.success,
                summary=report.final_summary,
                recommendations=report.recommendations,
                started_at=report.started_at,
                completed_at=report.completed_at,
            )
            ReportRepository(session).create(stored_report)

            agent_rows = [
                AgentExecutionDB(
                    id=result.id,
                    incident_id=event.id,
                    agent_name=result.agent_name,
                    task=result.metadata.get("task_name", ""),
                    input=result.metadata.get("task_description", ""),
                    output=result.summary,
                    success=result.success,
                    confidence=result.confidence,
                    summary=result.summary,
                    recommendations=result.recommendations,
                    decision=result.decision,
                    evidence=result.evidence,
                    actions_required=result.actions_required,
                    requires_human_approval=result.requires_human_approval,
                    timestamp=result.timestamp,
                )
                for result in report.agent_results
            ]
            if agent_rows:
                AgentRepository(session).create_many(agent_rows)
        except Exception:
            session.rollback()
            logger.exception("Failed to persist MAO execution.")
        finally:
            session.close()
```

## services/report.py

**File path:** `services/report.py`

```python

```

## services/runtime.py

**File path:** `services/runtime.py`

```python
from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.flow_workflow import FlowWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow

from agents.safety import SafetyAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.diagnostic import DiagnosticAgent
from agents.planning import PlanningAgent
from agents.notification import NotificationAgent
from agents.prediction import PredictionAgent
from agents.report import ReportAgent
from agents.sensor import SensorAgent
from rag.embedder import Embedder
from rag.neon_vector_store import NeonVectorStore

kernel = MAOKernel()

# Configure the shared MAO instance used by Streamlit before it receives events.
for workflow in (
    PressureWorkflow(),
    TemperatureWorkflow(),
    GasWorkflow(),
    FlowWorkflow(),
    MaintenanceWorkflow(),
):
    kernel.register_workflow(workflow)
embedder = Embedder()

vector_store = NeonVectorStore(
    embedder.get_model()
)

for agent in (
    SafetyAgent(),
    KnowledgeAgent(vector_store),
    MaintenanceAgent(),
    DiagnosticAgent(),
    PlanningAgent(),
    SensorAgent(),
    PredictionAgent(),
    NotificationAgent(),
    ReportAgent(),
):
    kernel.register_agent(agent)


assets = [

    Asset(
        name="Pump A-01",
        asset_type=AssetType.PUMP,
        location="Zone A"
    ),

]


facility = Facility(
    id="rigos-alpha",
    name="RigOS Alpha",
    assets=assets
)


for asset in assets:

    kernel.asset_service.register(asset)



simulated_facility = SimulatedFacility(
    facility
)


simulator = Simulator(
    facility=simulated_facility,
    kernel=kernel
)
```

## services/sensor.py

**File path:** `services/sensor.py`

```python

```

## services/simulation.py

**File path:** `services/simulation.py`

```python

```

## services/telemetry_store.py

**File path:** `services/telemetry_store.py`

```python
from collections import defaultdict


class TelemetryStore:

    def __init__(self):

        self.history = defaultdict(list)

    def add(self, readings):

        for reading in readings:

            self.history[reading.asset_id].append(reading)

            if len(self.history[reading.asset_id]) > 100:

                self.history[reading.asset_id].pop(0)

    def get_asset_history(self, asset_id):

        return self.history[asset_id]
```

## services/vision.py

**File path:** `services/vision.py`

```python

```

## services/weather.py

**File path:** `services/weather.py`

```python

```
