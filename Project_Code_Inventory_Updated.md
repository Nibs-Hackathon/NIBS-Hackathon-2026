# Project Code Inventory (Updated)

Generated: 2026-07-25T06:06:30 UTC

## Scope

This document contains the complete text source for 183 project files (18992 lines). It excludes Git metadata, virtual environments, dependency directories, generated/build output, binary data, generated inventory files, and secret-bearing `.env` files.

## Project root

`C:/Users/Abeer_1ewl9m1/Documents/rigos-hackathon-2026`

## Included folder paths

- `.`
- `backend/`
- `backend/agents/`
- `backend/api/`
- `backend/api/adapters/`
- `backend/api/adapters/frontend_services/`
- `backend/api/websocket/`
- `backend/data/`
- `backend/database/`
- `backend/database/migrations/`
- `backend/database/migrations/versions/`
- `backend/database/repositories/`
- `backend/mao/`
- `backend/mao/core/`
- `backend/mao/events/`
- `backend/mao/memory/`
- `backend/mao/models/`
- `backend/mao/tools/`
- `backend/mao/workflows/`
- `backend/models/`
- `backend/rag/`
- `backend/services/`
- `backend/simulator/`
- `frontend/`
- `frontend/src/`
- `frontend/src/api/`
- `frontend/src/components/`
- `frontend/src/components/Layout/`
- `frontend/src/hooks/`
- `frontend/src/pages/`
- `frontend/src/styles/`

## Source files

## backend/agents/__init__.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/__init__.py`

```python

```

## backend/agents/base.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/base.py`

```python
from abc import ABC, abstractmethod

from mao.models.result import AgentResult


class Agent(ABC):

    name = ""

    def think(self, task):
        print(
            f"[{self.name}] analyzing '{task.name}'"
        )

    @abstractmethod
    def execute(self, task, context) -> AgentResult:
        """
        Every agent must return an AgentResult.
        """
        pass

    def validate_result(self, result: AgentResult):

        if not isinstance(result, AgentResult):
            raise TypeError(
                f"{self.name} must return AgentResult."
            )

        required_fields = [
            "finding",
            "confidence",
            "recommendations",
            "success",
            "summary",
        ]

        for field in required_fields:

            if not hasattr(result, field):
                raise ValueError(
                    f"{self.name}: Missing field '{field}'"
                )

        if not 0 <= result.confidence <= 1:
            raise ValueError(
                f"{self.name}: Confidence must be between 0 and 1."
            )

        return True

    def reflect(self, result: AgentResult):

        print(
            f"""
==============================
Agent: {self.name}
==============================

Finding:
{result.finding}

Confidence:
{result.confidence:.2f}

Recommendations:
{len(result.recommendations)}

Evidence:
{len(result.evidence)}

Requires Approval:
{result.requires_human_approval}

Summary:
{result.summary}

==============================
"""
        )

    def run(self, task, context):

        self.think(task)

        result = self.execute(
            task,
            context,
        )

        self.validate_result(result)

        self.reflect(result)

        return result
```

## backend/agents/diagnostic.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/diagnostic.py`

```python
"""Production Diagnostic Agent with dynamic thresholds."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class DiagnosticAgent(Agent):
    """Diagnostic agent using Gemini-generated thresholds."""

    name = "diagnostic"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()
        self._thresholds_cache = {}

    def _get_thresholds(self, context):
        """Get thresholds for the asset type."""
        asset_type = self._get_asset_type(context) or "Pump"
        cache_key = f"thresholds_{asset_type}"
        if cache_key in self._thresholds_cache:
            return self._thresholds_cache[cache_key]
        
        thresholds = self.config.get_thresholds(asset_type)
        self._thresholds_cache[cache_key] = thresholds
        return thresholds

    def _get_asset_type(self, context):
        """Extract asset type from context."""
        if isinstance(context, dict):
            return context.get("asset_type")
        
        event = getattr(context, "event", None)
        if event:
            payload = getattr(event, "payload", {})
            return payload.get("asset_type")
        
        return None

    def execute(self, task, context):
        telemetry = self._extract_telemetry(context)
        safety = self._get_safety(context)
        thresholds = self._get_thresholds(context)

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", telemetry.get("gas", 0))
        vibration = telemetry.get("vibration", 0)
        flow = telemetry.get("flow_rate", 0)

        diagnosis = []
        evidence = []

        # ✅ Dynamic thresholds from Gemini
        if pressure >= thresholds.get("pressure_max", 150):
            diagnosis.append("Pressure surge")
            evidence.append("Pressure exceeded safe operating threshold.")

        if temperature >= thresholds.get("temperature_max", 85):
            diagnosis.append("Equipment overheating")
            evidence.append("Temperature above recommended operating range.")

        if gas >= thresholds.get("gas_max", 40):
            diagnosis.append("Possible gas leak")
            evidence.append("Gas concentration indicates potential leak.")

        if vibration >= thresholds.get("vibration_max", 8):
            diagnosis.append("Mechanical wear")
            evidence.append("High vibration suggests bearing or shaft wear.")

        if flow and flow <= thresholds.get("flow_min", 25):
            diagnosis.append("Flow restriction")
            evidence.append("Low flow rate indicates blockage or valve restriction.")

        if not diagnosis:
            diagnosis.append("System operating normally")

        confidence = 0.95 if safety.get("status") != "SAFE" else 0.90

        recommendations = []
        if "Pressure surge" in diagnosis:
            recommendations.append("Inspect pressure relief valve.")
        if "Equipment overheating" in diagnosis:
            recommendations.append("Check cooling system.")
        if "Possible gas leak" in diagnosis:
            recommendations.append("Inspect pipelines and gas sensors.")
        if "Mechanical wear" in diagnosis:
            recommendations.append("Inspect rotating equipment.")
        if "Flow restriction" in diagnosis:
            recommendations.append("Inspect valves and pipelines.")
        if not recommendations:
            recommendations.append("Continue monitoring.")

        metadata = {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "evidence": evidence,
            "thresholds": thresholds,  # ✅ Track thresholds used
            "source": "DiagnosticAgent",
        }

        self._store_metadata(context, metadata)

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=", ".join(diagnosis),
            confidence=confidence,
            evidence=evidence,
            recommendations=recommendations,
            required_action="Maintenance inspection" if diagnosis != ["System operating normally"] else "None",
            requires_human_approval=False,
            metadata=metadata,
            summary=f"Diagnosis complete: {', '.join(diagnosis)}",
        )

    def _extract_telemetry(self, context):
        if isinstance(context, dict):
            event = context.get("event")
            if isinstance(event, dict):
                return event.get("payload", {})
            return context.get("payload", {})

        event = getattr(context, "event", None)
        if event is None:
            return {}
        return getattr(event, "payload", {}) or {}

    def _get_safety(self, context):
        if isinstance(context, dict):
            return context.get("metadata", {}).get("safety", {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get("safety", {})

    def _store_metadata(self, context, metadata):
        if isinstance(context, dict):
            context.setdefault("metadata", {})["diagnosis"] = metadata
            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["diagnosis"] = metadata
```

## backend/agents/knowledge.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/knowledge.py`

```python
"""Knowledge agent shared by MAO workflows and Command Nexus."""

from __future__ import annotations

from pathlib import Path

from agents.base import Agent
from mao.models.result import AgentResult


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FAISS_INDEX_PATH = PROJECT_ROOT / "data" / "faiss_index"


class KnowledgeAgent(Agent):
    """Retrieve refinery guidance for workflows and create grounded chat answers."""

    name = "knowledge"

    def __init__(self, vector_store=None):
        super().__init__()
        self.retriever = None
        self.llm = None
        if vector_store is not None:
            from rag.retriever import Retriever
            self.retriever = Retriever(vector_store)

    def _initialize_services(self, require_llm: bool) -> None:
        """Lazily load the persisted retrieval index and, for chat, Gemini."""
        if self.retriever is None:
            from rag.embedder import Embedder
            from rag.retriever import Retriever
            from rag.vector_store import VectorStore

            embedder = Embedder()
            store = VectorStore(embedder.get_model())
            store.load(str(FAISS_INDEX_PATH))
            self.retriever = Retriever(store.db)

        if require_llm and self.llm is None:
            from services.llm import LLMManager
            self.llm = LLMManager()

    def think(self, task):
        print(f"[knowledge] Preparing guidance for '{task.name}'.")

    def execute(self, task, context=None) -> AgentResult:
        """Support MAO workflow context and direct Command Nexus requests."""
        workflow_execution = context is not None
        self._initialize_services(require_llm=not workflow_execution)

        findings = self._get_metadata(context, "diagnosis").get("diagnosis", [])
        query = " ".join(findings) if findings else task.description
        documents = self.retriever.retrieve(query)

        references, summaries, source_labels, context_parts = self._document_details(documents)
        execution_plan = self._get_metadata(context, "planning").get("execution_plan", [])
        recommendations = list(execution_plan)
        if summaries:
            recommendations.append("Review retrieved operating procedures before execution.")

        metadata = {
            "query": query,
            "references": references,
            "documents": summaries,
            "sources": source_labels,
        }
        self._store_metadata(context, metadata)

        if workflow_execution:
            return AgentResult(
                agent_name=self.name,
                success=True,
                finding=f"{len(documents)} knowledge document(s) retrieved.",
                confidence=0.94,
                evidence=references,
                recommendations=recommendations,
                required_action="Consult retrieved documentation",
                requires_human_approval=False,
                metadata=metadata,
                summary=f"Knowledge retrieval completed with {len(documents)} matching document(s).",
            )

        answer = self.llm.generate(self._chat_prompt(query, "\n\n".join(context_parts)))
        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.95,
            evidence=source_labels,
            recommendations=["Follow approved operating procedures", "Verify operating limits"],
            metadata={"documents_used": len(documents), "sources": source_labels},
            summary=answer,
        )

    @staticmethod
    def _document_details(documents):
        references, summaries, source_labels, context_parts = [], [], [], []
        for index, document in enumerate(documents, start=1):
            metadata = document.metadata or {}
            source = Path(str(metadata.get("source", "Operational reference"))).name
            page = metadata.get("page")
            label = f"[{index}] {source}" + (f", page {page + 1}" if isinstance(page, int) else "")
            references.append(str(metadata.get("source", "Unknown")))
            summaries.append(document.page_content[:300])
            source_labels.append(label)
            context_parts.append(f"{label}\n{document.page_content}")
        return references, summaries, source_labels, context_parts

    @staticmethod
    def _chat_prompt(query: str, reference_material: str) -> str:
        return f"""
You are Command Nexus, an experienced refinery operations engineer.

Deliver a confident, concise, professional operational response using ONLY the
technical reference material supplied below. Do not copy passages verbatim.
Do not invent operating limits, causes, actions, or citations that the material
does not support. Never mention implementation details such as retrieval,
documents, a knowledge base, databases, RAG, prompts, models, or internal
systems.

For safety-critical matters, be exact. If the supplied material does not
establish a fact, say that it is not established by the available operating
information. Give a brief operational rationale without revealing hidden
chain-of-thought.

Question:
{query}

Technical reference material:
{reference_material}

Respond in Markdown with every section below, using concise bullets where
appropriate. Do not rename the headings:

## Situation Assessment
## Immediate Actions
## Safety Considerations
## Possible Root Causes
## Recommended Maintenance
## Operational Impact
## References

Only cite source-backed operational statements in **References**, using the
supplied labels, for example [1].
"""

    @staticmethod
    def _get_metadata(context, key):
        if isinstance(context, dict):
            return context.get("metadata", {}).get(key, {})
        if not hasattr(context, "metadata"):
            return {}
        return context.metadata.get(key, {})

    @staticmethod
    def _store_metadata(context, metadata) -> None:
        if context is None:
            return
        if isinstance(context, dict):
            context.setdefault("metadata", {})["knowledge"] = metadata
            return
        if not hasattr(context, "metadata"):
            context.metadata = {}
        context.metadata["knowledge"] = metadata

    def reflect(self, result):
        print("[knowledge] Operational assessment completed.")
```

## backend/agents/maintenance.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/maintenance.py`

```python
"""Production Maintenance Agent with dynamic priority levels."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class MaintenanceAgent(Agent):
    """Maintenance agent using Gemini-generated priorities."""

    name = "maintenance"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        diagnosis = self._get_metadata(context, "diagnosis")
        safety = self._get_metadata(context, "safety")

        findings = diagnosis.get("diagnosis", [])
        incident_type = getattr(task, "name", "default")

        work_orders = []
        priority = "LOW"
        downtime = "None"

        # ✅ Get priority from Gemini
        priority_level = self.config.get_priority_level(incident_type, safety.get("status", "Medium"))

        if "Pressure surge" in findings:
            work_orders.append("Inspect pressure relief system")
            if priority_level <= 2:
                priority = "HIGH"
            downtime = "2-4 hours"

        if "Equipment overheating" in findings:
            work_orders.append("Inspect cooling system")
            if priority_level <= 2:
                priority = "HIGH"
            downtime = "3-5 hours"

        if "Possible gas leak" in findings:
            work_orders.append("Emergency pipeline inspection")
            priority = "CRITICAL"
            downtime = "Immediate shutdown"

        if "Mechanical wear" in findings:
            work_orders.append("Replace worn bearings")
            if priority != "CRITICAL":
                priority = "MEDIUM"
            downtime = "4-6 hours"

        if "Flow restriction" in findings:
            work_orders.append("Inspect valves and clean pipeline")
            if priority == "LOW":
                priority = "MEDIUM"
            downtime = "2 hours"

        if not work_orders:
            work_orders.append("No maintenance required")

        metadata = {
            "priority": priority,
            "priority_level": priority_level,
            "downtime": downtime,
            "work_orders": work_orders,
            "risk_status": safety.get("status", "SAFE"),
        }

        self._store_metadata(context, metadata)

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Maintenance Priority: {priority}",
            confidence=0.95,
            evidence=work_orders,
            recommendations=work_orders,
            required_action=priority,
            requires_human_approval=(priority in ("HIGH", "CRITICAL")),
            metadata=metadata,
            summary=f"{len(work_orders)} maintenance task(s) generated. Priority: {priority}.",
        )

    def _get_metadata(self, context, key):
        if isinstance(context, dict):
            return context.get("metadata", {}).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(self, context, metadata):
        if isinstance(context, dict):
            context.setdefault("metadata", {})["maintenance"] = metadata
            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["maintenance"] = metadata
```

## backend/agents/notification.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/notification.py`

```python
"""Runtime notification agent with dynamic severity levels."""

from __future__ import annotations

from agents.base import Agent
from mao.models.notification import Notification
from mao.models.result import AgentResult
from services.config_services import ConfigService


class NotificationAgent(Agent):
    """Create structured in-memory notifications from workflow metadata."""

    name = "notification"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        safety = context.metadata.get("safety", {})
        maintenance = context.metadata.get("maintenance", {})
        prediction = context.metadata.get("prediction", {})
        
        # ✅ Get dynamic severity
        severity = self._severity(safety, maintenance, prediction)
        
        notifications = []

        if severity != "INFO":
            notification = Notification(
                source=self.name,
                severity=severity,
                summary=self._summary(severity, prediction),
                asset_id=getattr(context.event, "source", None),
                requires_human_approval=(severity == "CRITICAL"),
                metadata={
                    "safety_status": safety.get("status", "SAFE"),
                    "maintenance_priority": maintenance.get("priority", "LOW"),
                    "failure_probability": prediction.get("failure_probability", 0),
                    "gemini_severity": severity,  # ✅ Track Gemini-generated severity
                },
            )
            context.state.add_notification(notification)
            notifications.append(notification)

        metadata = {
            "notification_count": len(notifications),
            "severity": severity,
            "notification_ids": [notification.id for notification in notifications],
        }
        context.metadata["notification"] = metadata
        
        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Created {len(notifications)} runtime notification(s).",
            confidence=0.95,
            evidence=[notification.summary for notification in notifications],
            recommendations=(
                ["Review the runtime notification queue."]
                if notifications
                else ["No operator notification is required."]
            ),
            required_action="Review notification" if notifications else "None",
            requires_human_approval=severity == "CRITICAL",
            metadata=metadata,
            summary=f"Notification evaluation completed with severity {severity}.",
        )

    def _severity(self, safety, maintenance, prediction) -> str:
        """Determine severity with dynamic thresholds."""
        failure_prob = prediction.get("failure_probability", 0)
        
        # Get incident type for dynamic thresholds
        incident_type = safety.get("incident_type", "default")
        
        # Get dynamic priority level
        priority_level = self.config.get_priority_level(incident_type, safety.get("status", "Medium"))
        
        # Critical if:
        # - Safety is CRITICAL
        # - Maintenance is CRITICAL
        # - Failure probability >= 70
        # - Gemini priority level <= 1 (Highest)
        if (
            safety.get("status") == "CRITICAL"
            or maintenance.get("priority") == "CRITICAL"
            or failure_prob >= 70
            or priority_level <= 1
        ):
            return "CRITICAL"
        
        # Warning if:
        # - Safety is WARNING
        # - Maintenance is HIGH
        # - Failure probability >= 40
        # - Gemini priority level <= 3
        if (
            safety.get("status") == "WARNING"
            or maintenance.get("priority") == "HIGH"
            or failure_prob >= 40
            or priority_level <= 3
        ):
            return "WARNING"
        
        return "INFO"

    @staticmethod
    def _summary(severity, prediction) -> str:
        probability = prediction.get("failure_probability", 0)
        return (
            f"{severity.title()} operational notification: predicted failure probability "
            f"is {probability}%."
        )
```

## backend/agents/planning.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/planning.py`

```python
"""Production Planning Agent with Gemini-generated sequences."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class PlanningAgent(Agent):
    """Planning agent using Gemini-generated workflow sequences."""

    name = "planning"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        safety = self._get_metadata(context, "safety")
        diagnosis = self._get_metadata(context, "diagnosis")
        maintenance = self._get_metadata(context, "maintenance")

        status = safety.get("status", "SAFE")
        findings = diagnosis.get("diagnosis", [])
        work_orders = maintenance.get("work_orders", [])
        priority = maintenance.get("priority", "LOW")

        # ✅ Get Gemini-generated execution plan
        incident_type = getattr(task, "name", "default")
        agent_sequence = self.config.get_workflow_sequence(incident_type)

        execution_plan = []

        # Add critical steps based on status
        if status == "CRITICAL":
            execution_plan.append("Immediately reduce operating load.")
            execution_plan.append("Notify control room.")

        # Add specific responses
        if "Possible gas leak" in findings:
            execution_plan.append("Isolate affected pipeline section.")

        if "Pressure surge" in findings:
            execution_plan.append("Stabilize system pressure.")

        if "Equipment overheating" in findings:
            execution_plan.append("Start cooling procedure.")

        # Add maintenance work orders
        execution_plan.extend(work_orders)

        # Add agent sequence as steps
        execution_plan.append(f"Execute agent sequence: {' → '.join(agent_sequence)}")

        if not execution_plan:
            execution_plan.append("Continue normal operation.")

        estimated_duration = self._estimate_duration(priority)

        metadata = {
            "priority": priority,
            "execution_plan": execution_plan,
            "estimated_duration": estimated_duration,
            "status": status,
            "agent_sequence": agent_sequence,  # ✅ Track sequence used
        }

        self._store_metadata(context, metadata)

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Execution plan created ({priority} priority)",
            confidence=0.96,
            evidence=execution_plan,
            recommendations=execution_plan,
            required_action="Execute plan",
            requires_human_approval=(status == "CRITICAL"),
            metadata=metadata,
            summary=f"Operational plan generated with {len(execution_plan)} step(s).",
        )

    def _estimate_duration(self, priority):
        mapping = {
            "LOW": "15-30 minutes",
            "MEDIUM": "30-60 minutes",
            "HIGH": "1-3 hours",
            "CRITICAL": "Immediate",
        }
        return mapping.get(priority, "Unknown")

    def _get_metadata(self, context, key):
        if isinstance(context, dict):
            return context.get("metadata", {}).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(self, context, metadata):
        if isinstance(context, dict):
            context.setdefault("metadata", {})["planning"] = metadata
            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["planning"] = metadata
```

## backend/agents/prediction.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/prediction.py`

```python
"""Dynamic asset-risk prediction agent with Gemini-generated thresholds."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class PredictionAgent(Agent):
    """Estimate health and risk from telemetry using dynamic thresholds."""

    name = "prediction"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        asset_id = getattr(context.event, "source", None) if context else None
        readings = context.state.get_history(asset_id) if (context and asset_id) else []
        health_service = context.health_service if context else None
        
        health = (
            health_service.calculate_health(readings)
            if health_service is not None and readings
            else 100.0
        )
        
        # ✅ Get dynamic thresholds for asset type
        asset_type = self._get_asset_type(context) or "Pump"
        thresholds = self.config.get_thresholds(asset_type)
        
        # Calculate degradation rate using dynamic thresholds
        degradation_rate = self._degradation_rate(readings, health_service, thresholds)
        
        # Dynamic failure probability calculation
        failure_probability = (
            min(
                100,
                round(((100 - health) * 0.85) + min(20, degradation_rate * 4)),
            )
            if readings
            else 0
        )
        
        rul_days = (
            max(1, min(365, round(health / max(degradation_rate, 0.25))))
            if readings
            else 365
        )
        
        confidence = min(0.95, round(0.55 + min(len(readings), 20) * 0.02, 2))

        evidence = [
            f"Telemetry samples evaluated: {len(readings)}",
            f"Calculated health: {round(health, 1)}%",
            f"Observed degradation rate: {round(degradation_rate, 2)} health points/sample",
            f"Asset type: {asset_type}",
            f"Thresholds used: {thresholds}",
        ]
        
        metadata = {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "health": round(health, 1),
            "failure_probability": failure_probability,
            "rul_days": rul_days,
            "confidence": confidence,
            "evidence": evidence,
            "thresholds": thresholds,  # ✅ Track thresholds used
            "method": "deterministic_telemetry_heuristic_with_gemini_thresholds",
        }
        
        if context:
            context.metadata["prediction"] = metadata

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=(
                f"Failure probability is {failure_probability}% with an estimated "
                f"remaining useful life of {rul_days} day(s)."
            ),
            confidence=confidence,
            evidence=evidence,
            recommendations=self._recommendations(failure_probability),
            required_action=(
                "Schedule maintenance review" if failure_probability >= 40 else "Continue monitoring"
            ),
            requires_human_approval=failure_probability >= 70,
            metadata=metadata,
            summary=(
                f"Dynamic prediction completed: health {round(health, 1)}%, "
                f"failure probability {failure_probability}%, RUL {rul_days} day(s)."
            ),
        )

    def _get_asset_type(self, context):
        """Extract asset type from context."""
        if not context:
            return None
        
        if isinstance(context, dict):
            return context.get("asset_type")
        
        # Try to get from metadata
        if hasattr(context, "metadata"):
            sensor_metadata = context.metadata.get("sensor", {})
            return sensor_metadata.get("asset_type")
        
        # Try from event payload
        event = getattr(context, "event", None)
        if event:
            payload = getattr(event, "payload", {})
            return payload.get("asset_type")
        
        return None

    @staticmethod
    def _degradation_rate(readings, health_service, thresholds) -> float:
        """Calculate degradation rate using dynamic thresholds."""
        if len(readings) < 2 or health_service is None:
            return 0.25
        
        # Use thresholds to weight degradation
        baseline = health_service.calculate_health(readings[:1])
        current = health_service.calculate_health(readings)
        raw_rate = (baseline - current) / (len(readings) - 1)
        
        # Apply threshold-based adjustment
        adjustment = 1.0
        for reading in readings:
            sensor_type = reading.sensor_type.value if hasattr(reading.sensor_type, 'value') else str(reading.sensor_type)
            value = reading.value
            
            if "pressure" in sensor_type.lower():
                if value > thresholds.get("pressure_max", 150):
                    adjustment = 1.5
            elif "temperature" in sensor_type.lower():
                if value > thresholds.get("temperature_max", 85):
                    adjustment = 1.3
            elif "gas" in sensor_type.lower():
                if value > thresholds.get("gas_max", 40):
                    adjustment = 1.8
            elif "vibration" in sensor_type.lower():
                if value > thresholds.get("vibration_max", 8):
                    adjustment = 1.4
        
        return max(0.25, raw_rate * adjustment)

    @staticmethod
    def _recommendations(failure_probability: int) -> list[str]:
        if failure_probability >= 70:
            return ["Escalate for immediate engineering review."]
        if failure_probability >= 40:
            return ["Plan a maintenance inspection during the next safe window."]
        return ["Continue monitoring telemetry for trend changes."]
```

## backend/agents/report.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/report.py`

```python
"""Report aggregation agent with dynamic formatting."""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class ReportAgent(Agent):
    """Compile prior AgentResult objects with dynamic formatting."""

    name = "report"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        prior_results = list(context.results)
        
        # ✅ Get dynamic workflow sequence for context
        incident_type = getattr(task, "name", "default")
        agent_sequence = self.config.get_workflow_sequence(incident_type)
        
        recommendations = list(
            OrderedDict.fromkeys(
                recommendation
                for result in prior_results
                for recommendation in result.recommendations
            )
        )
        
        evidence = [
            f"{result.agent_name}: {result.finding}"
            for result in prior_results
            if result.finding
        ]
        
        confidence = (
            round(sum(result.confidence for result in prior_results) / len(prior_results), 2)
            if prior_results
            else 0.0
        )
        
        # ✅ Add execution trace
        execution_trace = [
            f"{i+1}. {agent_name}"
            for i, agent_name in enumerate(agent_sequence)
        ]
        
        metadata = {
            "source_agents": [result.agent_name for result in prior_results],
            "result_count": len(prior_results),
            "agent_sequence": agent_sequence,  # ✅ Track sequence used
            "execution_trace": execution_trace,
            "completed_at": datetime.now().isoformat(),
        }
        context.metadata["report"] = metadata

        return AgentResult(
            agent_name=self.name,
            success=all(result.success for result in prior_results),
            finding=f"Compiled {len(prior_results)} agent result(s) for the execution report.",
            confidence=confidence,
            evidence=evidence,
            recommendations=recommendations,
            required_action="Review execution report",
            requires_human_approval=any(
                result.requires_human_approval for result in prior_results
            ),
            metadata=metadata,
            summary=f"Report compiled with {len(prior_results)} results. Sequence: {' → '.join(agent_sequence)}",
        )
```

## backend/agents/safety.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/safety.py`

```python
"""Production Safety Agent with dynamic thresholds."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class SafetyAgent(Agent):
    """Safety assessment agent using Gemini-generated thresholds."""

    name = "safety"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()
        self._thresholds_cache = {}

    def _get_thresholds(self, context):
        """Get thresholds for the asset type."""
        asset_type = self._get_asset_type(context) or "Pump"
        cache_key = f"thresholds_{asset_type}"
        if cache_key in self._thresholds_cache:
            return self._thresholds_cache[cache_key]
        
        thresholds = self.config.get_thresholds(asset_type)
        self._thresholds_cache[cache_key] = thresholds
        return thresholds

    def _get_asset_type(self, context):
        """Extract asset type from context."""
        if isinstance(context, dict):
            return context.get("asset_type")
        
        # Try to get from event or metadata
        event = getattr(context, "event", None)
        if event:
            payload = getattr(event, "payload", {})
            return payload.get("asset_type")
        
        return None

    def _get_risk_weights(self, incident_type):
        """Get risk weights for the incident type."""
        return self.config.get_risk_weights(incident_type or "default")

    def execute(self, task, context):
        telemetry = self._extract_telemetry(context)
        thresholds = self._get_thresholds(context)
        weights = self._get_risk_weights(getattr(task, "name", "default"))

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", telemetry.get("gas", 0))
        vibration = telemetry.get("vibration", 0)

        alerts = []
        risk_score = 0

        # ✅ Dynamic thresholds from Gemini
        if pressure >= thresholds.get("pressure_max", 150):
            alerts.append(f"High pressure detected ({pressure} PSI)")
            risk_score += weights.get("pressure_weight", 30)

        if temperature >= thresholds.get("temperature_max", 85):
            alerts.append(f"High temperature detected ({temperature} °C)")
            risk_score += weights.get("temperature_weight", 25)

        if gas >= thresholds.get("gas_max", 40):
            alerts.append(f"Gas concentration elevated ({gas})")
            risk_score += weights.get("gas_weight", 35)

        if vibration >= thresholds.get("vibration_max", 8):
            alerts.append(f"Abnormal vibration detected ({vibration})")
            risk_score += weights.get("vibration_weight", 20)

        risk_score = min(risk_score, 100)

        # Status based on risk score
        if risk_score >= 80:
            status = "CRITICAL"
        elif risk_score >= 40:
            status = "WARNING"
        else:
            status = "SAFE"

        # Recommendations based on status
        recommendations = []
        if status == "CRITICAL":
            recommendations.extend([
                "Reduce operating load immediately",
                "Notify control room",
                "Inspect affected equipment",
            ])
        elif status == "WARNING":
            recommendations.extend([
                "Increase monitoring frequency",
                "Schedule inspection",
            ])
        else:
            recommendations.append("Continue normal operation")

        metadata = {
            "status": status,
            "risk_score": risk_score,
            "alerts": alerts,
            "telemetry": telemetry,
            "thresholds": thresholds,  # ✅ Track which thresholds were used
            "confidence": 0.96,
        }

        self._store_metadata(context, metadata)

        summary = f"Safety assessment completed. Status: {status}. Risk Score: {risk_score}/100."
        finding = alerts[0] if alerts else "No safety issues detected."

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=finding,
            confidence=0.96,
            evidence=alerts,
            recommendations=recommendations,
            required_action="Immediate intervention" if status == "CRITICAL" else "Continue monitoring",
            requires_human_approval=(status == "CRITICAL"),
            metadata=metadata,
            summary=summary,
        )

    def _extract_telemetry(self, context):
        if isinstance(context, dict):
            event = context.get("event")
            if isinstance(event, dict):
                return event.get("payload", {})
            return context.get("payload", {})

        event = getattr(context, "event", None)
        if event is None:
            return {}
        return getattr(event, "payload", {}) or {}

    def _store_metadata(self, context, metadata):
        if isinstance(context, dict):
            context.setdefault("metadata", {})["safety"] = metadata
            return

        if not hasattr(context, "metadata"):
            context.metadata = {}
        context.metadata["safety"] = metadata
```

## backend/agents/sensor.py

**Folder path:** `backend/agents`

**File path:** `backend/agents/sensor.py`

```python
"""Sensor observation agent with dynamic enrichment."""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from services.config_services import ConfigService


class SensorAgent(Agent):
    """Summarize telemetry with dynamic enrichment."""

    name = "sensor"

    def __init__(self):
        super().__init__()
        self.config = ConfigService()

    def execute(self, task, context):
        event = getattr(context, "event", None)
        payload = getattr(event, "payload", {}) or {}
        asset_id = getattr(event, "source", None)
        readings = context.state.get_history(asset_id) if asset_id else []

        signals = [
            f"{signal}: {value}"
            for signal, value in payload.items()
        ]
        
        # ✅ Get dynamic thresholds for context
        asset_type = payload.get("asset_type", "Pump")
        thresholds = self.config.get_thresholds(asset_type)
        
        # Check if any signal exceeds thresholds
        anomalies = []
        for signal, value in payload.items():
            signal_lower = signal.lower()
            if "pressure" in signal_lower and value > thresholds.get("pressure_max", 150):
                anomalies.append(f"Pressure exceeds threshold: {value} > {thresholds.get('pressure_max')}")
            elif "temperature" in signal_lower and value > thresholds.get("temperature_max", 85):
                anomalies.append(f"Temperature exceeds threshold: {value} > {thresholds.get('temperature_max')}")
            elif "gas" in signal_lower and value > thresholds.get("gas_max", 40):
                anomalies.append(f"Gas exceeds threshold: {value} > {thresholds.get('gas_max')}")
            elif "vibration" in signal_lower and value > thresholds.get("vibration_max", 8):
                anomalies.append(f"Vibration exceeds threshold: {value} > {thresholds.get('vibration_max')}")
        
        metadata = {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "event_name": getattr(event, "name", "Unknown"),
            "signals": dict(payload),
            "history_samples": len(readings),
            "anomaly_observed": bool(payload),
            "anomalies": anomalies,
            "thresholds": thresholds,  # ✅ Track thresholds used
        }
        context.metadata["sensor"] = metadata

        finding = (
            f"Observed {len(signals)} telemetry signal(s) for the incoming event."
            + (f" Found {len(anomalies)} anomalies." if anomalies else " No anomalies detected.")
        )
        
        recommendations = []
        if anomalies:
            recommendations.append("Investigate anomalous readings.")
            recommendations.append("Refer to dynamic thresholds for guidance.")
        else:
            recommendations.append("Continue the configured response workflow.")
        
        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=finding,
            confidence=0.9 if signals else 0.5,
            evidence=signals + anomalies,
            recommendations=recommendations,
            required_action="Telemetry metadata recorded",
            requires_human_approval=bool(anomalies),
            metadata=metadata,
            summary=(
                f"Sensor observation recorded with {len(readings)} history sample(s). "
                f"Anomalies: {len(anomalies)}"
            ),
        )
```

## backend/api/adapters/__init__.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/__init__.py`

```python
"""Frontend-facing adapters for existing RigOS backend modules."""

from api.adapters.backend_api_new import api, BackendAPI

# Import all adapters directly
from api.adapters.dashboard_adapter import get_dashboard
from api.adapters.asset_adapter import get_assets
from api.adapters.agent_adapter import get_agents, get_agent_metrics
from api.adapters.report_adapter import get_reports
from api.adapters.control_adapter import get_control_state
from api.adapters.telemetry_adapter import get_asset_telemetry
from api.adapters.health_adapter import get_asset_health
from api.adapters.health_prediction_adapter import get_health_prediction
from api.adapters.knowledge_adapter import KnowledgeSearchError, search_knowledge
from api.adapters.knowledge_agent_adapter import KnowledgeAgentUnavailable, ask_knowledge_agent, is_operational_query
from api.adapters.incident_adapter import trigger_incident, get_incidents
from api.adapters.maintenance_adapter import get_maintenance_plan
from api.adapters.digital_twin_adapter import get_twin_assets
from api.adapters.agent_activity_adapter import get_agent_activity

__all__ = [
    "api",
    "BackendAPI",
    "get_dashboard",
    "get_assets",
    "get_agents",
    "get_agent_metrics",
    "get_reports",
    "get_control_state",
    "get_asset_telemetry",
    "get_asset_health",
    "get_health_prediction",
    "KnowledgeSearchError",
    "search_knowledge",
    "KnowledgeAgentUnavailable",
    "ask_knowledge_agent",
    "is_operational_query",
    "trigger_incident",
    "get_incidents",
    "get_maintenance_plan",
    "get_twin_assets",
    "get_agent_activity",
]
```

## backend/api/adapters/agent_activity_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/agent_activity_adapter.py`

```python
"""Activity view-model sourced from live MAO state and persisted audit events."""

from datetime import datetime
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_session
from database.repositories.activity_repo import ActivityRepository
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _format_time(timestamp) -> str:
    return timestamp.strftime("%H:%M:%S") if timestamp else "Unknown"


def _runtime_activity() -> list[dict]:
    kernel = runtime.kernel
    return [
        {
            "time": _format_time(getattr(result, "timestamp", None)),
            "agent": result.agent_name,
            "action": result.summary or result.finding or "No summary recorded.",
            "state": "Completed" if result.success else "Failed",
            "confidence": f"{round(result.confidence * 100)}%",
            "progress": 100,
            "timestamp": getattr(result, "timestamp", None),
        }
        for result in kernel.state.agent_results
    ]


def _persisted_activity() -> tuple[list[dict], str | None]:
    """Load immutable activity records without blocking live state rendering."""
    session = None
    try:
        session = get_session()
        events = ActivityRepository(session).get_recent()
        return [
            {
                "time": _format_time(event.created_at),
                "agent": event.source,
                "action": event.summary,
                "state": event.status.title(),
                "confidence": (
                    f"{round(event.confidence * 100)}%"
                    if event.confidence is not None
                    else "Not available"
                ),
                "progress": 100 if event.status.lower() == "completed" else 0,
                "timestamp": event.created_at,
            }
            for event in events
        ], None
    except Exception:
        return [], "Persisted activity is temporarily unavailable."
    finally:
        if session is not None:
            session.close()


def get_agent_activity() -> tuple[list[dict], str | None]:
    """Return the combined live MAO and persisted activity timeline."""
    runtime_events = _runtime_activity()
    persisted_events, warning = _persisted_activity()
    activity = runtime_events + persisted_events
    activity.sort(key=lambda event: event["timestamp"] or datetime.min, reverse=True)
    return activity, warning


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return summary metrics from current MAO agent results."""
    kernel = runtime.kernel
    results = kernel.state.agent_results

    if not results:
        return [
            ("Activities today", "0", "Waiting for execution", "cyan"),
            ("Completed workflows", "0", "No executions", "green"),
            ("Human reviews", "0", "No pending review", "amber"),
            ("Avg confidence", "0%", "No data", "violet"),
        ]

    completed = sum(result.success for result in results)
    confidence = sum(result.confidence for result in results) / len(results)
    reviews = sum(result.requires_human_approval for result in results)

    return [
        ("Activities today", str(len(results)), "From MAO execution", "cyan"),
        ("Completed workflows", str(completed), "Successful executions", "green"),
        ("Human reviews", str(reviews), "Approval required", "amber"),
        ("Avg confidence", f"{round(confidence * 100, 1)}%", "Agent confidence", "violet"),
    ]
```

## backend/api/adapters/agent_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/agent_adapter.py`

```python
"""Agent adapter using BackendAPI."""

from __future__ import annotations

from api.adapters.backend_api_new import api


def get_agents() -> list[dict[str, str]]:
    """Return registered agents and their latest execution state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=20)
    
    # Map agent names to latest results
    latest_results = {}
    for a in activity:
        if a["agent_name"] not in latest_results:
            latest_results[a["agent_name"]] = a
    
    agents = []
    for agent in agents_data:
        name = agent["name"]
        result = latest_results.get(name)
        agents.append({
            "Agent": name.replace("_", " ").title(),
            "Specialty": name.title(),
            "State": "Active" if result and result.get("success") else "Ready",
            "Confidence": f"{round(result.get('confidence', 0) * 100)}%" if result else "N/A",
            "Current task": result.get("finding", "Awaiting task")[:50] if result else "Awaiting task",
        })
    return agents


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return monitor metrics calculated from the live state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=50)
    status = api.get_simulation_status()
    
    registered = len(agents_data)
    results = len(activity)
    success_count = sum(1 for a in activity if a.get("success"))
    avg_confidence = sum(a.get("confidence", 0) for a in activity) / len(activity) if activity else 0
    
    return [
        ("Agents registered", str(registered), "Shared MAO registry", "green"),
        ("Tasks active", str(status.get("reports", 0)), "Execution reports", "amber"),
        ("Avg. confidence", f"{round(avg_confidence * 100, 1)}%" if avg_confidence else "N/A", "From completed agent results", "cyan"),
        ("Decisions recorded", str(results), "MAO agent executions", "violet"),
    ]
```

## backend/api/adapters/asset_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/asset_adapter.py`

```python
"""Asset adapter using BackendAPI."""

from api.adapters.backend_api_new import api


def get_assets():
    """Get all assets with telemetry history."""
    assets = api.get_assets()
    
    # Get telemetry for each asset
    for asset in assets:
        telemetry = api.get_asset_telemetry(asset["id"], limit=1)
        if telemetry:
            asset["Last telemetry"] = telemetry[-1].get("timestamp", "N/A")[:19] if "timestamp" in telemetry[-1] else "N/A"
        else:
            asset["Last telemetry"] = "No data"
    
    return {
        "assets": assets,
        "sensors": [
            {"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"},
            {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"},
            {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"},
            {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"},
        ],
        "history": []
    }
```

## backend/api/adapters/backend_api_new.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/backend_api_new.py`

```python
"""Unified backend API for frontend access with caching and refinery support."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from functools import lru_cache
import time
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.config_services import ConfigService


class BackendAPI:
    """Single interface for frontend to access backend data with caching."""

    def __init__(self):
        self.config = ConfigService()
        self._cache_ttl = 5
        self._cache_timestamps = {}
        self._kernel = None
        self._simulator = None

    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_timestamps:
            return False
        return (time.time() - self._cache_timestamps[key]) < self._cache_ttl

    def _invalidate_cache(self, key: str = None):
        if key:
            self._cache_timestamps.pop(key, None)
            if hasattr(self, f"_{key}_cached"):
                getattr(self, f"_{key}_cached").cache_clear()
        else:
            self._cache_timestamps.clear()
            for attr in dir(self):
                if attr.startswith("_") and attr.endswith("_cached"):
                    getattr(self, attr).cache_clear()

    def _get_runtime(self):
        """Lazy load runtime to avoid circular imports."""
        if self._kernel is None or self._simulator is None:
            from services.runtime import runtime
            self._kernel = runtime.kernel
            self._simulator = runtime.simulator
        return self._kernel, self._simulator

    @property
    def kernel(self):
        return self._get_runtime()[0]

    @property
    def simulator(self):
        return self._get_runtime()[1]

    def get_refineries(self) -> List[Dict]:
        """Get all refineries with their assets."""
        refineries = getattr(self.kernel, "_refineries", [])
        return [
            {
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "status": r.status,
                "asset_count": len(r.assets),
                "assets": [
                    {
                        "id": a.id,
                        "name": a.name,
                        "type": a.asset_type.value if hasattr(a.asset_type, 'value') else str(a.asset_type),
                        "health": a.health,
                        "status": a.status,
                        "zone": getattr(a, "zone", "Unassigned"),
                    }
                    for a in r.assets
                ]
            }
            for r in refineries
        ]

    def get_refinery_assets(self, refinery_id: str) -> List[Dict]:
        """Get assets for a specific refinery."""
        refineries = getattr(self.kernel, "_refineries", [])
        for refinery in refineries:
            if refinery.id == refinery_id:
                return [
                    {
                        "id": a.id,
                        "name": a.name,
                        "type": a.asset_type.value if hasattr(a.asset_type, 'value') else str(a.asset_type),
                        "health": a.health,
                        "status": a.status,
                        "zone": getattr(a, "zone", "Unassigned"),
                        "refinery_id": refinery.id,
                        "refinery_name": refinery.name,
                    }
                    for a in refinery.assets
                ]
        return []

    def get_assets_by_type(self, refinery_id: str, asset_type: str) -> List[Dict]:
        """Get assets of a specific type in a refinery."""
        all_assets = self.get_refinery_assets(refinery_id)
        return [a for a in all_assets if a.get("type", "").lower() == asset_type.lower()]

    @lru_cache(maxsize=32)
    def _get_assets_cached(self) -> List[Dict]:
        """Cached version of get_assets."""
        assets = self.kernel.asset_service.all_assets()
        return [
            {
                "id": asset.id,
                "name": asset.name,
                "type": asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type),
                "location": asset.location,
                "zone": getattr(asset, "zone", "Unassigned"),
                "health": asset.health,
                "status": asset.status,
                "refinery_id": getattr(asset, "refinery_id", None),
            }
            for asset in assets
        ]

    def get_assets(self, force_refresh: bool = False) -> List[Dict]:
        """Get all assets from all refineries with caching."""
        if force_refresh:
            self._invalidate_cache("get_assets")
        return self._get_assets_cached()

    @lru_cache(maxsize=128)
    def _get_asset_telemetry_cached(self, asset_id: str, limit: int = 100) -> tuple:
        """Cached version of get_asset_telemetry."""
        readings = self.kernel.state.get_history(asset_id)
        if limit:
            readings = readings[-limit:]
        return tuple([
            {
                "timestamp": r.timestamp.isoformat() if hasattr(r, 'timestamp') else datetime.now().isoformat(),
                "sensor_type": r.sensor_type.value if hasattr(r.sensor_type, 'value') else str(r.sensor_type),
                "value": float(r.value) if hasattr(r, 'value') else 0,
                "unit": getattr(r, 'unit', ''),
            }
            for r in readings
        ])

    def get_asset_telemetry(self, asset_id: str, limit: int = 100, force_refresh: bool = False) -> List[Dict]:
        """Get telemetry history for an asset with caching."""
        if force_refresh:
            self._invalidate_cache("get_asset_telemetry")
        return list(self._get_asset_telemetry_cached(asset_id, limit))

    def get_asset_health(self, asset_id: str) -> Dict:
        """Get health for a specific asset."""
        readings = self.kernel.state.get_history(asset_id)
        health = self.kernel.health.calculate_health(readings)
        return {
            "health": health,
            "readings": len(readings),
            "status": "Running" if health > 80 else "Warning" if health > 50 else "Critical",
        }

    @lru_cache(maxsize=32)
    def _get_incidents_cached(self) -> tuple:
        """Cached version of get_incidents."""
        events = self.kernel.event_store.all()
        return tuple([
            {
                "id": event.id,
                "name": event.name,
                "asset_id": event.source,
                "payload": event.payload,
                "timestamp": event.timestamp.isoformat(),
            }
            for event in events
        ])

    def get_incidents(self, force_refresh: bool = False) -> List[Dict]:
        """Get all incidents from the runtime with caching."""
        if force_refresh:
            self._invalidate_cache("get_incidents")
        return list(self._get_incidents_cached())

    def trigger_incident(self, incident_type: str) -> Dict:
        """Trigger a simulated incident."""
        from services.incident_service import IncidentService
        service = IncidentService(self.simulator)
        result = service.trigger_incident(incident_type)
        self._invalidate_cache("get_incidents")
        self._invalidate_cache("get_agent_activity")
        return result

    @lru_cache(maxsize=32)
    def _get_agents_cached(self) -> List[Dict]:
        """Cached version of get_agents."""
        agents = self.kernel.registry.all()
        results = self.kernel.state.agent_results
        result_map = {r.agent_name: r for r in results}
        return [
            {
                "name": agent.name,
                "status": "Active" if agent.name in result_map else "Ready",
                "last_result": result_map.get(agent.name),
            }
            for agent in agents
        ]

    def get_agents(self, force_refresh: bool = False) -> List[Dict]:
        """Get registered agents and their status with caching."""
        if force_refresh:
            self._invalidate_cache("get_agents")
        return self._get_agents_cached()

    @lru_cache(maxsize=32)
    def _get_agent_activity_cached(self, limit: int = 50) -> tuple:
        """Cached version of get_agent_activity."""
        results = self.kernel.state.agent_results[-limit:]
        return tuple([
            {
                "agent_name": r.agent_name,
                "finding": r.finding,
                "confidence": r.confidence,
                "success": r.success,
                "timestamp": r.timestamp.isoformat(),
                "summary": r.summary,
                "recommendations": r.recommendations,
            }
            for r in results
        ])

    def get_agent_activity(self, limit: int = 50, force_refresh: bool = False) -> List[Dict]:
        """Get recent agent activity with caching."""
        if force_refresh:
            self._invalidate_cache("get_agent_activity")
        return list(self._get_agent_activity_cached(limit))

    @lru_cache(maxsize=32)
    def _get_reports_cached(self) -> tuple:
        """Cached version of get_reports."""
        reports = self.kernel.state.execution_reports
        return tuple([
            {
                "id": r.id,
                "workflow": r.workflow_name,
                "success": r.success,
                "summary": r.final_summary,
                "started_at": r.started_at.isoformat(),
                "completed_at": r.completed_at.isoformat(),
                "confidence": r.average_confidence,
                "agent_results": len(r.agent_results),
            }
            for r in reports
        ])

    def get_reports(self, force_refresh: bool = False) -> List[Dict]:
        """Get execution reports with caching."""
        if force_refresh:
            self._invalidate_cache("get_reports")
        return list(self._get_reports_cached())

    def get_dynamic_thresholds(self, asset_type: str) -> Dict:
        """Get Gemini-generated thresholds for an asset type."""
        return self.config.get_thresholds(asset_type)

    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Get Gemini-generated workflow sequence."""
        return self.config.get_workflow_sequence(incident_type)

    def refresh_config(self) -> Dict:
        """Refresh all configurations and clear caches."""
        self.config.refresh()
        self._invalidate_cache()
        return {"status": "refreshed", "cache_cleared": True}

    def get_simulation_status(self) -> Dict:
        """Get current simulation status."""
        return {
            "running": getattr(self.kernel, "_simulation_running", False),
            "events": len(self.kernel.event_store.all()),
            "reports": len(self.kernel.state.execution_reports),
            "agent_results": len(self.kernel.state.agent_results),
            "assets": len(self.kernel.asset_service.all_assets()),
        }

    def step_simulation(self) -> Dict:
        """Advance simulation by one tick."""
        from services.simulator_controller import sim_controller
        telemetry, reports = sim_controller.step()
        self._invalidate_cache()
        return {
            "telemetry_count": len(telemetry),
            "reports_count": len(reports),
        }


# ✅ Create the singleton instance
_api_instance = None


def _get_api_instance():
    global _api_instance
    if _api_instance is None:
        _api_instance = BackendAPI()
    return _api_instance


# ✅ Export api as a property that lazy-loads
class _ApiProxy:
    def __getattr__(self, name):
        return getattr(_get_api_instance(), name)


api = _ApiProxy()
BackendAPI = BackendAPI
```

## backend/api/adapters/control_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/control_adapter.py`

```python
"""Control adapter using BackendAPI."""

from api.adapters.backend_api_new import api


def get_control_state() -> dict:
    """Return a facility snapshot derived from live state."""
    assets = api.get_assets()
    incidents = api.get_incidents()
    status = api.get_simulation_status()
    
    if not assets:
        return {
            "facility_mode": "NO ASSETS",
            "throughput": "N/A",
            "safety": "0 / 0",
            "queue": "0",
            "zones": [],
            "summary": "No assets are registered with the shared MAO runtime.",
        }
    
    healthy_assets = [a for a in assets if a.get("status", "").lower() in {"running", "healthy"}]
    average_health = sum(a.get("health", 0) for a in assets) / len(assets) if assets else 0
    facility_mode = "RUNNING" if healthy_assets else "ATTENTION"
    
    # Group by zone
    zones: dict[str, dict] = {}
    for asset in assets:
        zone = asset.get("location", "Unassigned")
        zones.setdefault(zone, {"assets": 0, "health": []})
        zones[zone]["assets"] += 1
        zones[zone]["health"].append(asset.get("health", 0))
    
    zone_snapshot = []
    for name, data in sorted(zones.items()):
        average_zone_health = sum(data["health"]) / len(data["health"]) if data["health"] else 0
        zone_snapshot.append({
            "Zone": name,
            "State": "Nominal" if average_zone_health >= 80 else "Attention",
            "Health": f"{round(average_zone_health)}%",
            "Assets": data["assets"],
        })
    
    return {
        "facility_mode": facility_mode,
        "throughput": f"{round((len(healthy_assets) / len(assets)) * 100, 1)}%" if assets else "N/A",
        "safety": f"{len(healthy_assets)} / {len(assets)}",
        "queue": str(len(incidents)),
        "zones": zone_snapshot,
        "summary": f"{len(healthy_assets)} of {len(assets)} registered assets are operating normally; average asset health is {round(average_health, 1)}%.",
    }
```

## backend/api/adapters/dashboard_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/dashboard_adapter.py`

```python
"""Dashboard adapter using BackendAPI."""

from api.adapters.backend_api_new import api
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def calculate_severity(event):
    """Calculate severity from event payload."""
    payload = event.get("payload", {})

    if "gas" in payload:
        return "Critical"
    if "pressure" in payload:
        return "Critical" if payload["pressure"] > 160 else "High"
    if "temperature" in payload:
        return "Critical" if payload["temperature"] > 100 else "High"
    if "vibration" in payload:
        return "Critical" if payload["vibration"] > 40 else "High"
    if "flow" in payload:
        return "Medium"
    return "Unknown"


def get_dashboard():
    """Get dashboard data using BackendAPI with caching."""
    # Get data from API (uses caching internally)
    assets = api.get_assets()
    incidents = api.get_incidents()
    activity = api.get_agent_activity(limit=5)

    # ✅ Use runtime.kernel
    kernel = runtime.kernel

    # Calculate metrics
    total_assets = len(assets)
    healthy_assets = sum(1 for a in assets if a.get("status") == "Running")
    avg_health = sum(a.get("health", 0) for a in assets) / total_assets if total_assets else 0

    metrics = [
        ("Fleet health", f"{avg_health:.1f}%", "Calculated from assets", "green"),
        ("Assets online", f"{healthy_assets} / {total_assets}", "Connected", "cyan"),
        ("Active incidents", str(len(incidents)), "From EventStore", "red"),
        ("AI decisions", str(len(kernel.state.agent_results)), "Agent executions", "violet"),
    ]

    # Format incidents
    formatted_incidents = []
    for incident in incidents[-10:]:
        formatted_incidents.append({
            "Incident": incident.get("name", "Unknown"),
            "Asset": incident.get("asset_id", "Unknown"),
            "Severity": calculate_severity(incident),
            "Detected": incident.get("timestamp", "").split("T")[1][:8] if "T" in incident.get("timestamp", "") else "",
        })

    # Format activity
    formatted_activity = []
    for a in activity[:5]:
        timestamp = a.get("timestamp", "")
        time_str = timestamp.split("T")[1][:8] if "T" in timestamp else ""
        formatted_activity.append((
            time_str,
            a.get("agent_name", "Unknown"),
            a.get("summary", "")[:100],
        ))

    return {
        "metrics": metrics,
        "incidents": formatted_incidents,
        "assets": assets,
        "activity": formatted_activity,
    }
```

## backend/api/adapters/digital_twin_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/digital_twin_adapter.py`

```python
"""Read-only asset and telemetry view-model for the Digital Twin page."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _reading_value(readings: list[Any], sensor_type: str) -> str:
    for reading in reversed(readings):
        reading_type = getattr(reading.sensor_type, "value", reading.sensor_type)
        if str(reading_type).lower() == sensor_type.lower():
            value = getattr(reading, "value", "N/A")
            unit = getattr(reading, "unit", "")
            return f"{value} {unit}".strip()
    return "Not available"


def _maintenance_recommendation(asset_id: str) -> str:
    kernel = runtime.kernel
    for result in reversed(kernel.state.agent_results):
        if result.agent_name != "maintenance":
            continue
        if result.metadata.get("asset_id") != asset_id:
            continue
        recommendations = result.recommendations or result.evidence
        if recommendations:
            return recommendations[0]
    return "No maintenance recommendation is available for this asset."


def get_twin_assets() -> list[dict]:
    """Return current assets and latest observed telemetry from the runtime."""
    kernel = runtime.kernel
    assets = []
    for asset in kernel.asset_service.all_assets():
        readings = kernel.state.get_history(asset.id)
        health = kernel.health.calculate_health(readings) if readings else asset.health
        
        # ✅ Get actual telemetry values
        temp = _reading_value(readings, "temperature")
        pressure = _reading_value(readings, "pressure")
        rpm = _reading_value(readings, "rpm")
        
        assets.append({
            "id": asset.id,
            "Asset": asset.name,
            "Category": getattr(asset.asset_type, "value", str(asset.asset_type)),
            "Zone": asset.location or "Unassigned",
            "Status": asset.status or ("Healthy" if health >= 80 else "Attention"),
            "Health": round(health, 1),
            "Temperature": temp,
            "Pressure": pressure,
            "RPM": rpm,
            "Failure": "Not available",
            "Recommendation": _maintenance_recommendation(asset.id),
        })
    return assets
```

## backend/api/adapters/frontend_services/__init__.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/__init__.py`

```python
"""Frontend-facing adapters for existing RigOS backend modules."""

from app.frontend_services.backend_api_new import api, BackendAPI

# Import all adapters directly
from app.frontend_services.dashboard_adapter import get_dashboard
from app.frontend_services.asset_adapter import get_assets
from app.frontend_services.agent_adapter import get_agents, get_agent_metrics
from app.frontend_services.report_adapter import get_reports
from app.frontend_services.control_adapter import get_control_state
from app.frontend_services.telemetry_adapter import get_asset_telemetry
from app.frontend_services.health_adapter import get_asset_health
from app.frontend_services.health_prediction_adapter import get_health_prediction
from app.frontend_services.knowledge_adapter import KnowledgeSearchError, search_knowledge
from app.frontend_services.knowledge_agent_adapter import KnowledgeAgentUnavailable, ask_knowledge_agent, is_operational_query
from app.frontend_services.incident_adapter import trigger_incident, get_incidents
from app.frontend_services.maintenance_adapter import get_maintenance_plan
from app.frontend_services.digital_twin_adapter import get_twin_assets
from app.frontend_services.agent_activity_adapter import get_agent_activity

__all__ = [
    "api",
    "BackendAPI",
    "get_dashboard",
    "get_assets",
    "get_agents",
    "get_agent_metrics",
    "get_reports",
    "get_control_state",
    "get_asset_telemetry",
    "get_asset_health",
    "get_health_prediction",
    "KnowledgeSearchError",
    "search_knowledge",
    "KnowledgeAgentUnavailable",
    "ask_knowledge_agent",
    "is_operational_query",
    "trigger_incident",
    "get_incidents",
    "get_maintenance_plan",
    "get_twin_assets",
    "get_agent_activity",
]
```

## backend/api/adapters/frontend_services/agent_activity_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/agent_activity_adapter.py`

```python
"""Activity view-model sourced from live MAO state and persisted audit events."""

from datetime import datetime
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_session
from database.repositories.activity_repo import ActivityRepository
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _format_time(timestamp) -> str:
    return timestamp.strftime("%H:%M:%S") if timestamp else "Unknown"


def _runtime_activity() -> list[dict]:
    kernel = runtime.kernel
    return [
        {
            "time": _format_time(getattr(result, "timestamp", None)),
            "agent": result.agent_name,
            "action": result.summary or result.finding or "No summary recorded.",
            "state": "Completed" if result.success else "Failed",
            "confidence": f"{round(result.confidence * 100)}%",
            "progress": 100,
            "timestamp": getattr(result, "timestamp", None),
        }
        for result in kernel.state.agent_results
    ]


def _persisted_activity() -> tuple[list[dict], str | None]:
    """Load immutable activity records without blocking live state rendering."""
    session = None
    try:
        session = get_session()
        events = ActivityRepository(session).get_recent()
        return [
            {
                "time": _format_time(event.created_at),
                "agent": event.source,
                "action": event.summary,
                "state": event.status.title(),
                "confidence": (
                    f"{round(event.confidence * 100)}%"
                    if event.confidence is not None
                    else "Not available"
                ),
                "progress": 100 if event.status.lower() == "completed" else 0,
                "timestamp": event.created_at,
            }
            for event in events
        ], None
    except Exception:
        return [], "Persisted activity is temporarily unavailable."
    finally:
        if session is not None:
            session.close()


def get_agent_activity() -> tuple[list[dict], str | None]:
    """Return the combined live MAO and persisted activity timeline."""
    runtime_events = _runtime_activity()
    persisted_events, warning = _persisted_activity()
    activity = runtime_events + persisted_events
    activity.sort(key=lambda event: event["timestamp"] or datetime.min, reverse=True)
    return activity, warning


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return summary metrics from current MAO agent results."""
    kernel = runtime.kernel
    results = kernel.state.agent_results

    if not results:
        return [
            ("Activities today", "0", "Waiting for execution", "cyan"),
            ("Completed workflows", "0", "No executions", "green"),
            ("Human reviews", "0", "No pending review", "amber"),
            ("Avg confidence", "0%", "No data", "violet"),
        ]

    completed = sum(result.success for result in results)
    confidence = sum(result.confidence for result in results) / len(results)
    reviews = sum(result.requires_human_approval for result in results)

    return [
        ("Activities today", str(len(results)), "From MAO execution", "cyan"),
        ("Completed workflows", str(completed), "Successful executions", "green"),
        ("Human reviews", str(reviews), "Approval required", "amber"),
        ("Avg confidence", f"{round(confidence * 100, 1)}%", "Agent confidence", "violet"),
    ]
```

## backend/api/adapters/frontend_services/agent_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/agent_adapter.py`

```python
"""Agent adapter using BackendAPI."""

from __future__ import annotations

from app.frontend_services.backend_api_new import api


def get_agents() -> list[dict[str, str]]:
    """Return registered agents and their latest execution state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=20)
    
    # Map agent names to latest results
    latest_results = {}
    for a in activity:
        if a["agent_name"] not in latest_results:
            latest_results[a["agent_name"]] = a
    
    agents = []
    for agent in agents_data:
        name = agent["name"]
        result = latest_results.get(name)
        agents.append({
            "Agent": name.replace("_", " ").title(),
            "Specialty": name.title(),
            "State": "Active" if result and result.get("success") else "Ready",
            "Confidence": f"{round(result.get('confidence', 0) * 100)}%" if result else "N/A",
            "Current task": result.get("finding", "Awaiting task")[:50] if result else "Awaiting task",
        })
    return agents


def get_agent_metrics() -> list[tuple[str, str, str, str]]:
    """Return monitor metrics calculated from the live state."""
    agents_data = api.get_agents()
    activity = api.get_agent_activity(limit=50)
    status = api.get_simulation_status()
    
    registered = len(agents_data)
    results = len(activity)
    success_count = sum(1 for a in activity if a.get("success"))
    avg_confidence = sum(a.get("confidence", 0) for a in activity) / len(activity) if activity else 0
    
    return [
        ("Agents registered", str(registered), "Shared MAO registry", "green"),
        ("Tasks active", str(status.get("reports", 0)), "Execution reports", "amber"),
        ("Avg. confidence", f"{round(avg_confidence * 100, 1)}%" if avg_confidence else "N/A", "From completed agent results", "cyan"),
        ("Decisions recorded", str(results), "MAO agent executions", "violet"),
    ]
```

## backend/api/adapters/frontend_services/asset_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/asset_adapter.py`

```python
"""Asset adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api


def get_assets():
    """Get all assets with telemetry history."""
    assets = api.get_assets()
    
    # Get telemetry for each asset
    for asset in assets:
        telemetry = api.get_asset_telemetry(asset["id"], limit=1)
        if telemetry:
            asset["Last telemetry"] = telemetry[-1].get("timestamp", "N/A")[:19] if "timestamp" in telemetry[-1] else "N/A"
        else:
            asset["Last telemetry"] = "No data"
    
    return {
        "assets": assets,
        "sensors": [
            {"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"},
            {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"},
            {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"},
            {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"},
        ],
        "history": []
    }
```

## backend/api/adapters/frontend_services/backend_api_new.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/backend_api_new.py`

```python
"""Unified backend API for frontend access with caching and refinery support."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from functools import lru_cache
import time
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.config_services import ConfigService


class BackendAPI:
    """Single interface for frontend to access backend data with caching."""

    def __init__(self):
        self.config = ConfigService()
        self._cache_ttl = 5
        self._cache_timestamps = {}
        self._kernel = None
        self._simulator = None

    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache_timestamps:
            return False
        return (time.time() - self._cache_timestamps[key]) < self._cache_ttl

    def _invalidate_cache(self, key: str = None):
        if key:
            self._cache_timestamps.pop(key, None)
            if hasattr(self, f"_{key}_cached"):
                getattr(self, f"_{key}_cached").cache_clear()
        else:
            self._cache_timestamps.clear()
            for attr in dir(self):
                if attr.startswith("_") and attr.endswith("_cached"):
                    getattr(self, attr).cache_clear()

    def _get_runtime(self):
        """Lazy load runtime to avoid circular imports."""
        if self._kernel is None or self._simulator is None:
            from services.runtime import runtime
            self._kernel = runtime.kernel
            self._simulator = runtime.simulator
        return self._kernel, self._simulator

    @property
    def kernel(self):
        return self._get_runtime()[0]

    @property
    def simulator(self):
        return self._get_runtime()[1]

    def get_refineries(self) -> List[Dict]:
        """Get all refineries with their assets."""
        refineries = getattr(self.kernel, "_refineries", [])
        return [
            {
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "status": r.status,
                "asset_count": len(r.assets),
                "assets": [
                    {
                        "id": a.id,
                        "name": a.name,
                        "type": a.asset_type.value if hasattr(a.asset_type, 'value') else str(a.asset_type),
                        "health": a.health,
                        "status": a.status,
                        "zone": getattr(a, "zone", "Unassigned"),
                    }
                    for a in r.assets
                ]
            }
            for r in refineries
        ]

    def get_refinery_assets(self, refinery_id: str) -> List[Dict]:
        """Get assets for a specific refinery."""
        refineries = getattr(self.kernel, "_refineries", [])
        for refinery in refineries:
            if refinery.id == refinery_id:
                return [
                    {
                        "id": a.id,
                        "name": a.name,
                        "type": a.asset_type.value if hasattr(a.asset_type, 'value') else str(a.asset_type),
                        "health": a.health,
                        "status": a.status,
                        "zone": getattr(a, "zone", "Unassigned"),
                        "refinery_id": refinery.id,
                        "refinery_name": refinery.name,
                    }
                    for a in refinery.assets
                ]
        return []

    def get_assets_by_type(self, refinery_id: str, asset_type: str) -> List[Dict]:
        """Get assets of a specific type in a refinery."""
        all_assets = self.get_refinery_assets(refinery_id)
        return [a for a in all_assets if a.get("type", "").lower() == asset_type.lower()]

    @lru_cache(maxsize=32)
    def _get_assets_cached(self) -> List[Dict]:
        """Cached version of get_assets."""
        assets = self.kernel.asset_service.all_assets()
        return [
            {
                "id": asset.id,
                "name": asset.name,
                "type": asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type),
                "location": asset.location,
                "zone": getattr(asset, "zone", "Unassigned"),
                "health": asset.health,
                "status": asset.status,
                "refinery_id": getattr(asset, "refinery_id", None),
            }
            for asset in assets
        ]

    def get_assets(self, force_refresh: bool = False) -> List[Dict]:
        """Get all assets from all refineries with caching."""
        if force_refresh:
            self._invalidate_cache("get_assets")
        return self._get_assets_cached()

    @lru_cache(maxsize=128)
    @lru_cache(maxsize=128)
    def _get_asset_telemetry_cached(self, asset_id: str, limit: int = 100) -> tuple:
        """Cached version of get_asset_telemetry."""
        readings = self.kernel.state.get_history(asset_id)
        if limit:
            readings = readings[-limit:]
        return tuple([
            {
                "timestamp": r.timestamp.isoformat() if hasattr(r, 'timestamp') else datetime.now().isoformat(),
                "sensor_type": r.sensor_type.value if hasattr(r.sensor_type, 'value') else str(r.sensor_type),
                "value": float(r.value) if hasattr(r, 'value') else 0,
                "unit": getattr(r, 'unit', ''),
            }
            for r in readings
    ])

    def get_asset_telemetry(self, asset_id: str, limit: int = 100, force_refresh: bool = False) -> List[Dict]:
        """Get telemetry history for an asset with caching."""
        if force_refresh:
            self._invalidate_cache("get_asset_telemetry")
        return list(self._get_asset_telemetry_cached(asset_id, limit))

    def get_asset_health(self, asset_id: str) -> Dict:
        """Get health for a specific asset."""
        readings = self.kernel.state.get_history(asset_id)
        health = self.kernel.health.calculate_health(readings)
        return {
            "health": health,
            "readings": len(readings),
            "status": "Running" if health > 80 else "Warning" if health > 50 else "Critical",
        }

    @lru_cache(maxsize=32)
    def _get_incidents_cached(self) -> tuple:
        """Cached version of get_incidents."""
        events = self.kernel.event_store.all()
        return tuple([
            {
                "id": event.id,
                "name": event.name,
                "asset_id": event.source,
                "payload": event.payload,
                "timestamp": event.timestamp.isoformat(),
            }
            for event in events
        ])

    def get_incidents(self, force_refresh: bool = False) -> List[Dict]:
        """Get all incidents from the runtime with caching."""
        if force_refresh:
            self._invalidate_cache("get_incidents")
        return list(self._get_incidents_cached())

    def trigger_incident(self, incident_type: str) -> Dict:
        """Trigger a simulated incident."""
        from services.incident_service import IncidentService
        service = IncidentService(self.simulator)
        result = service.trigger_incident(incident_type)
        self._invalidate_cache("get_incidents")
        self._invalidate_cache("get_agent_activity")
        return result

    @lru_cache(maxsize=32)
    def _get_agents_cached(self) -> List[Dict]:
        """Cached version of get_agents."""
        agents = self.kernel.registry.all()
        results = self.kernel.state.agent_results
        result_map = {r.agent_name: r for r in results}
        return [
            {
                "name": agent.name,
                "status": "Active" if agent.name in result_map else "Ready",
                "last_result": result_map.get(agent.name),
            }
            for agent in agents
        ]

    def get_agents(self, force_refresh: bool = False) -> List[Dict]:
        """Get registered agents and their status with caching."""
        if force_refresh:
            self._invalidate_cache("get_agents")
        return self._get_agents_cached()

    @lru_cache(maxsize=32)
    def _get_agent_activity_cached(self, limit: int = 50) -> tuple:
        """Cached version of get_agent_activity."""
        results = self.kernel.state.agent_results[-limit:]
        return tuple([
            {
                "agent_name": r.agent_name,
                "finding": r.finding,
                "confidence": r.confidence,
                "success": r.success,
                "timestamp": r.timestamp.isoformat(),
                "summary": r.summary,
                "recommendations": r.recommendations,
            }
            for r in results
        ])

    def get_agent_activity(self, limit: int = 50, force_refresh: bool = False) -> List[Dict]:
        """Get recent agent activity with caching."""
        if force_refresh:
            self._invalidate_cache("get_agent_activity")
        return list(self._get_agent_activity_cached(limit))

    @lru_cache(maxsize=32)
    def _get_reports_cached(self) -> tuple:
        """Cached version of get_reports."""
        reports = self.kernel.state.execution_reports
        return tuple([
            {
                "id": r.id,
                "workflow": r.workflow_name,
                "success": r.success,
                "summary": r.final_summary,
                "started_at": r.started_at.isoformat(),
                "completed_at": r.completed_at.isoformat(),
                "confidence": r.average_confidence,
                "agent_results": len(r.agent_results),
            }
            for r in reports
        ])

    def get_reports(self, force_refresh: bool = False) -> List[Dict]:
        """Get execution reports with caching."""
        if force_refresh:
            self._invalidate_cache("get_reports")
        return list(self._get_reports_cached())

    def get_dynamic_thresholds(self, asset_type: str) -> Dict:
        """Get Gemini-generated thresholds for an asset type."""
        return self.config.get_thresholds(asset_type)

    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Get Gemini-generated workflow sequence."""
        return self.config.get_workflow_sequence(incident_type)

    def refresh_config(self) -> Dict:
        """Refresh all configurations and clear caches."""
        self.config.refresh()
        self._invalidate_cache()
        return {"status": "refreshed", "cache_cleared": True}

    def get_simulation_status(self) -> Dict:
        """Get current simulation status."""
        return {
            "running": getattr(self.kernel, "_simulation_running", False),
            "events": len(self.kernel.event_store.all()),
            "reports": len(self.kernel.state.execution_reports),
            "agent_results": len(self.kernel.state.agent_results),
            "assets": len(self.kernel.asset_service.all_assets()),
        }

    def step_simulation(self) -> Dict:
        """Advance simulation by one tick."""
        from services.simulator_controller import sim_controller
        telemetry, reports = sim_controller.step()
        self._invalidate_cache()
        return {
            "telemetry_count": len(telemetry),
            "reports_count": len(reports),
        }


# ✅ Create the singleton instance
_api_instance = None


def _get_api_instance():
    global _api_instance
    if _api_instance is None:
        _api_instance = BackendAPI()
    return _api_instance


# ✅ Export api as a property that lazy-loads
class _ApiProxy:
    def __getattr__(self, name):
        return getattr(_get_api_instance(), name)


api = _ApiProxy()
BackendAPI = BackendAPI
```

## backend/api/adapters/frontend_services/control_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/control_adapter.py`

```python
"""Control adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api


def get_control_state() -> dict:
    """Return a facility snapshot derived from live state."""
    assets = api.get_assets()
    incidents = api.get_incidents()
    status = api.get_simulation_status()
    
    if not assets:
        return {
            "facility_mode": "NO ASSETS",
            "throughput": "N/A",
            "safety": "0 / 0",
            "queue": "0",
            "zones": [],
            "summary": "No assets are registered with the shared MAO runtime.",
        }
    
    healthy_assets = [a for a in assets if a.get("status", "").lower() in {"running", "healthy"}]
    average_health = sum(a.get("health", 0) for a in assets) / len(assets) if assets else 0
    facility_mode = "RUNNING" if healthy_assets else "ATTENTION"
    
    # Group by zone
    zones: dict[str, dict] = {}
    for asset in assets:
        zone = asset.get("location", "Unassigned")
        zones.setdefault(zone, {"assets": 0, "health": []})
        zones[zone]["assets"] += 1
        zones[zone]["health"].append(asset.get("health", 0))
    
    zone_snapshot = []
    for name, data in sorted(zones.items()):
        average_zone_health = sum(data["health"]) / len(data["health"]) if data["health"] else 0
        zone_snapshot.append({
            "Zone": name,
            "State": "Nominal" if average_zone_health >= 80 else "Attention",
            "Health": f"{round(average_zone_health)}%",
            "Assets": data["assets"],
        })
    
    return {
        "facility_mode": facility_mode,
        "throughput": f"{round((len(healthy_assets) / len(assets)) * 100, 1)}%" if assets else "N/A",
        "safety": f"{len(healthy_assets)} / {len(assets)}",
        "queue": str(len(incidents)),
        "zones": zone_snapshot,
        "summary": f"{len(healthy_assets)} of {len(assets)} registered assets are operating normally; average asset health is {round(average_health, 1)}%.",
    }
```

## backend/api/adapters/frontend_services/dashboard_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/dashboard_adapter.py`

```python
"""Dashboard adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def calculate_severity(event):
    """Calculate severity from event payload."""
    payload = event.get("payload", {})

    if "gas" in payload:
        return "Critical"
    if "pressure" in payload:
        return "Critical" if payload["pressure"] > 160 else "High"
    if "temperature" in payload:
        return "Critical" if payload["temperature"] > 100 else "High"
    if "vibration" in payload:
        return "Critical" if payload["vibration"] > 40 else "High"
    if "flow" in payload:
        return "Medium"
    return "Unknown"


def get_dashboard():
    """Get dashboard data using BackendAPI with caching."""
    # Get data from API (uses caching internally)
    assets = api.get_assets()
    incidents = api.get_incidents()
    activity = api.get_agent_activity(limit=5)

    # ✅ Use runtime.kernel
    kernel = runtime.kernel

    # Calculate metrics
    total_assets = len(assets)
    healthy_assets = sum(1 for a in assets if a.get("status") == "Running")
    avg_health = sum(a.get("health", 0) for a in assets) / total_assets if total_assets else 0

    metrics = [
        ("Fleet health", f"{avg_health:.1f}%", "Calculated from assets", "green"),
        ("Assets online", f"{healthy_assets} / {total_assets}", "Connected", "cyan"),
        ("Active incidents", str(len(incidents)), "From EventStore", "red"),
        ("AI decisions", str(len(kernel.state.agent_results)), "Agent executions", "violet"),
    ]

    # Format incidents
    formatted_incidents = []
    for incident in incidents[-10:]:
        formatted_incidents.append({
            "Incident": incident.get("name", "Unknown"),
            "Asset": incident.get("asset_id", "Unknown"),
            "Severity": calculate_severity(incident),
            "Detected": incident.get("timestamp", "").split("T")[1][:8] if "T" in incident.get("timestamp", "") else "",
        })

    # Format activity
    formatted_activity = []
    for a in activity[:5]:
        timestamp = a.get("timestamp", "")
        time_str = timestamp.split("T")[1][:8] if "T" in timestamp else ""
        formatted_activity.append((
            time_str,
            a.get("agent_name", "Unknown"),
            a.get("summary", "")[:100],
        ))

    return {
        "metrics": metrics,
        "incidents": formatted_incidents,
        "assets": assets,
        "activity": formatted_activity,
    }
```

## backend/api/adapters/frontend_services/digital_twin_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/digital_twin_adapter.py`

```python
"""Read-only asset and telemetry view-model for the Digital Twin page."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _reading_value(readings: list[Any], sensor_type: str) -> str:
    for reading in reversed(readings):
        reading_type = getattr(reading.sensor_type, "value", reading.sensor_type)
        if str(reading_type).lower() == sensor_type.lower():
            value = getattr(reading, "value", "N/A")
            unit = getattr(reading, "unit", "")
            return f"{value} {unit}".strip()
    return "Not available"


def _maintenance_recommendation(asset_id: str) -> str:
    kernel = runtime.kernel
    for result in reversed(kernel.state.agent_results):
        if result.agent_name != "maintenance":
            continue
        if result.metadata.get("asset_id") != asset_id:
            continue
        recommendations = result.recommendations or result.evidence
        if recommendations:
            return recommendations[0]
    return "No maintenance recommendation is available for this asset."


def get_twin_assets() -> list[dict]:
    """Return current assets and latest observed telemetry from the runtime."""
    kernel = runtime.kernel
    assets = []
    for asset in kernel.asset_service.all_assets():
        readings = kernel.state.get_history(asset.id)
        health = kernel.health.calculate_health(readings) if readings else asset.health
        
        # ✅ Get actual telemetry values
        temp = _reading_value(readings, "temperature")
        pressure = _reading_value(readings, "pressure")
        rpm = _reading_value(readings, "rpm")
        
        assets.append({
            "id": asset.id,
            "Asset": asset.name,
            "Category": getattr(asset.asset_type, "value", str(asset.asset_type)),
            "Zone": asset.location or "Unassigned",
            "Status": asset.status or ("Healthy" if health >= 80 else "Attention"),
            "Health": round(health, 1),
            "Temperature": temp,
            "Pressure": pressure,
            "RPM": rpm,
            "Failure": "Not available",
            "Recommendation": _maintenance_recommendation(asset.id),
        })
    return assets
```

## backend/api/adapters/frontend_services/health_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/health_adapter.py`

```python
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def get_asset_health(asset_id):
    kernel = runtime.kernel
    readings = kernel.state.get_history(asset_id)

    health = kernel.health.calculate_health(
        readings
    )

    return {
        "health": health,
        "readings": readings
    }
```

## backend/api/adapters/frontend_services/health_prediction_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/health_prediction_adapter.py`

```python
"""Health prediction using computation engine."""

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.computation_engine import ComputationEngine


def get_health_prediction(asset_id, horizon_days=14):
    """Get health prediction using the computation engine."""
    kernel = runtime.kernel
    engine = ComputationEngine()
    
    readings = kernel.state.get_history(asset_id)
    asset = kernel.asset_service.get(asset_id)
    
    if not asset or not readings:
        return {
            "health": 100,
            "rul": "365 days",
            "failure_probability": "0%",
            "confidence": "Low",
            "historical": {"Historical health": []},
            "predicted": {"Predicted health": [], "Intervention threshold": []},
            "telemetry": []
        }
    
    # Get current metrics
    metrics = engine.compute_asset(asset, readings)
    
    # Calculate historical health
    historical = []
    for i in range(len(readings)):
        h = engine._calculate_health(
            readings[:i+1],
            engine.config.get_thresholds(metrics["asset_type"]),
            {}  # weights
        )
        historical.append(round(h, 1))
    
    # Predict future health
    current_health = metrics["health"]
    degradation_rate = metrics["degradation_rate"]
    
    predicted = []
    for day in range(horizon_days):
        health = current_health - (degradation_rate * 5 * (day + 1))
        predicted.append(round(max(0, health), 1))
    
    # Format RUL
    rul_days = metrics["rul_days"]
    if rul_days >= 365:
        rul_str = "365+ days"
    elif rul_days >= 90:
        rul_str = f"{int(rul_days)} days"
    elif rul_days >= 30:
        rul_str = f"{int(rul_days)} days"
    elif rul_days >= 7:
        rul_str = f"{int(rul_days)} days"
    else:
        rul_str = f"{int(rul_days)} days"
    
    return {
        "health": round(metrics["health"]),
        "rul": rul_str,
        "failure_probability": f"{metrics['failure_probability']:.1f}%",
        "confidence": f"{metrics['confidence'] * 100:.1f}%",
        "historical": {"Historical health": historical},
        "predicted": {
            "Predicted health": predicted,
            "Intervention threshold": [70] * horizon_days
        },
        "telemetry": format_telemetry(readings)
    }


def format_telemetry(readings):
    """Format telemetry for display."""
    data = []
    for reading in readings[-10:]:
        data.append({
            "Sensor": reading.sensor_type.value,
            "Observed": reading.value,
            "Time": reading.timestamp.strftime("%H:%M:%S")
        })
    return data
```

## backend/api/adapters/frontend_services/incident_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/incident_adapter.py`

```python
"""Incident adapter with dynamic severity calculation from config."""

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.incident_service import IncidentService
from services.ai_config import AIConfigGenerator


def trigger_incident(incident_type):
    """Trigger an incident and return formatted results."""
    simulator = runtime.simulator
    service = IncidentService(simulator)
    result = service.trigger_incident(incident_type)
    
    try:
        import streamlit as st
        reports = result.get("reports", [])
        if reports:
            events = []
            for i, report in enumerate(reports):
                agent_name = getattr(report, 'workflow_name', 'Unknown')
                if i == 0:
                    events.append(("⏱️ 00:00", "🚨 Incident detected"))
                events.append((f"⏱️ 00:{i+2:02d}", f"🤖 {agent_name} completed"))
            
            last_report = reports[-1] if reports else None
            if last_report:
                summary = getattr(last_report, 'final_summary', '')
                if "planning" in summary.lower():
                    events.append(("⏱️ 00:12", "✅ Investigation complete"))
            
            st.session_state.incident_events = events
            st.session_state.investigation_complete = True
    except Exception as e:
        print(f"⚠️ Could not update session state: {e}")
    
    return result


def get_incidents():
    """Get all incidents from the runtime."""
    kernel = runtime.kernel
    events = kernel.event_store.all()

    incidents = []
    for event in events:
        severity = calculate_severity(event)
        incidents.append({
            "Incident": event.name,
            "Asset": event.source,
            "Severity": severity,
            "Detected": event.timestamp.strftime("%H:%M:%S") if hasattr(event, 'timestamp') else "Unknown",
            "Payload": event.payload,
        })

    return incidents


def calculate_severity(event):
    """
    Calculate severity from event payload using dynamic thresholds from AI config.
    """
    payload = getattr(event, 'payload', {})
    
    try:
        config = AIConfigGenerator()
        asset_type = payload.get("asset_type", "Pump")
        thresholds = config.get_thresholds(asset_type)
        severity_map = config.get_config().get("severity_mapping", {
            "Critical": 1, "High": 2, "Medium": 3, "Low": 4
        })
        
        severity_scores = {}
        
        if "pressure" in payload:
            pressure_max = thresholds.get("pressure_max", 150)
            pressure_val = payload["pressure"]
            ratio = pressure_val / pressure_max
            if ratio >= 1.5:
                severity_scores["pressure"] = 1
            elif ratio >= 1.2:
                severity_scores["pressure"] = 2
            elif ratio >= 1.05:
                severity_scores["pressure"] = 3
            else:
                severity_scores["pressure"] = 4
        
        if "temperature" in payload:
            temp_max = thresholds.get("temperature_max", 85)
            temp_val = payload["temperature"]
            ratio = temp_val / temp_max
            if ratio >= 1.5:
                severity_scores["temperature"] = 1
            elif ratio >= 1.2:
                severity_scores["temperature"] = 2
            elif ratio >= 1.05:
                severity_scores["temperature"] = 3
            else:
                severity_scores["temperature"] = 4
        
        if "gas" in payload:
            gas_max = thresholds.get("gas_max", 40)
            gas_val = payload["gas"]
            ratio = gas_val / gas_max
            if ratio >= 1.5:
                severity_scores["gas"] = 1
            elif ratio >= 1.2:
                severity_scores["gas"] = 2
            elif ratio >= 1.05:
                severity_scores["gas"] = 3
            else:
                severity_scores["gas"] = 4
        
        if "vibration" in payload:
            vib_max = thresholds.get("vibration_max", 8)
            vib_val = payload["vibration"]
            ratio = vib_val / vib_max
            if ratio >= 1.5:
                severity_scores["vibration"] = 1
            elif ratio >= 1.2:
                severity_scores["vibration"] = 2
            elif ratio >= 1.05:
                severity_scores["vibration"] = 3
            else:
                severity_scores["vibration"] = 4
        
        if "flow" in payload:
            flow_min = thresholds.get("flow_min", 25)
            flow_val = payload["flow"]
            ratio = flow_min / flow_val if flow_val > 0 else 10
            if ratio >= 2:
                severity_scores["flow"] = 1
            elif ratio >= 1.5:
                severity_scores["flow"] = 2
            elif ratio >= 1.2:
                severity_scores["flow"] = 3
            else:
                severity_scores["flow"] = 4
        
        if severity_scores:
            worst_score = min(severity_scores.values())
            reverse_map = {v: k for k, v in severity_map.items()}
            return reverse_map.get(worst_score, "Medium")
        
    except Exception as e:
        print(f"⚠️ Severity calculation failed: {e}")
    
    return "Medium"
```

## backend/api/adapters/frontend_services/knowledge_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/knowledge_adapter.py`

```python
"""Read-only Knowledge Base access through the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


class KnowledgeSearchError(RuntimeError):
    """Raised when the registered knowledge retrieval path is unavailable."""


__all__ = ["KnowledgeSearchError", "search_knowledge"]

def search_knowledge(query: str) -> list[dict[str, str]]:
    """Return normalized Neon retrieval results from the registered KnowledgeAgent."""
    normalized_query = query.strip()
    if not normalized_query:
        return []

    try:
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise KnowledgeSearchError("Knowledge Agent is not available. Please ensure the knowledge base is loaded.")
        if agent.retriever is None:
            raise KnowledgeSearchError("Knowledge retriever is not initialized. Please build the knowledge base first.")
    except KnowledgeSearchError:
        raise
    except Exception as error:
        raise KnowledgeSearchError(f"Knowledge service unavailable: {str(error)[:100]}") from error

    try:
        documents = agent.retriever.retrieve(normalized_query)
    except Exception as error:
        raise KnowledgeSearchError(f"Retrieval failed: {str(error)[:100]}") from error

    results = []
    for document in documents:
        metadata = document.metadata or {}
        source = str(metadata.get("source", "Unknown source"))
        results.append(
            {
                "content": document.page_content,
                "source": source,
                "filename": Path(source).name or source,
            }
        )
    return results
```

## backend/api/adapters/frontend_services/knowledge_agent_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/knowledge_agent_adapter.py`

```python
"""Frontend routing for Command Nexus conversational and operational requests."""

from __future__ import annotations

from functools import lru_cache
import logging
from pathlib import Path
import re
import sys
from typing import TYPE_CHECKING, Callable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if TYPE_CHECKING:
    from agents.knowledge import KnowledgeAgent

LOGGER = logging.getLogger(__name__)
ProgressCallback = Callable[[str], None]

OPERATIONAL_KEYWORDS = (
    "asset", "compressor", "pump", "pipeline", "tank", "valve", "maintenance",
    "inspection", "incident", "alarm", "safety", "hazard", "pressure",
    "temperature", "vibration", "flow", "gas", "refinery", "sop", "procedure",
    "equipment", "motor", "turbine", "boiler", "heat exchanger", "reactor",
    "distillation", "column", "flare", "corrosion", "shutdown", "startup",
    "trip", "failure", "process", "telemetry", "sensor", "knowledge",
)


def is_operational_query(question: str) -> bool:
    """Return whether a question requires the refinery operations path."""
    normalized = re.sub(r"\s+", " ", question.strip().casefold())
    return bool(normalized and any(keyword in normalized for keyword in OPERATIONAL_KEYWORDS))


def generate_conversational_response(question: str) -> str:
    """Use Gemini for casual conversation without starting the operational path."""
    from services.llm import LLMManager

    prompt = f"""
You are Command Nexus, a polished industrial operations copilot.

Reply naturally to this casual user message: {question!r}

Keep the response concise, warm, and professional. You may introduce yourself
as an industrial operations copilot and offer help with refinery operations,
equipment, maintenance, incident response, and safety. Do not provide
operational facts, citations, or technical instructions for a casual message.
Never mention implementation, search, retrieval, documents, a knowledge base,
databases, RAG, prompts, APIs, or model internals.
"""
    try:
        return LLMManager().generate(prompt)
    except Exception as e:
        LOGGER.error(f"Conversational response failed: {e}")
        return "I'm here to help with refinery operations. What would you like to know?"


def _emit(callback: ProgressCallback | None, message: str) -> None:
    LOGGER.info(message)
    if callback is not None:
        callback(message)


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Return the KnowledgeAgent registered on the shared MAO kernel."""
    try:
        from services.runtime import runtime
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise RuntimeError("KnowledgeAgent is not registered on the MAO kernel.")
        return agent
    except Exception as error:
        raise KnowledgeAgentUnavailable("Command Nexus is temporarily unavailable. Please try again shortly.") from error


def ask_knowledge_agent(question: str, on_progress: ProgressCallback | None = None) -> str:
    """Route casual conversation to Gemini and operational questions to KnowledgeAgent."""
    _emit(on_progress, "Command Nexus received a question.")
    normalized_question = question.strip()
    if not normalized_question:
        raise KnowledgeAgentUnavailable("Enter a question before asking Command Nexus.")

    if not is_operational_query(normalized_question):
        _emit(on_progress, "Conversational request detected.")
        try:
            return generate_conversational_response(normalized_question)
        except Exception as error:
            LOGGER.exception("Command Nexus conversational response failed")
            return "I'm here to help! What would you like to know about refinery operations?"

    _emit(on_progress, "Preparing an operational assessment.")
    try:
        from mao.models.task import Task

        task = Task(
            name="Operator knowledge query",
            description=normalized_question,
            assigned_agent="knowledge",
        )
        agent = get_knowledge_agent()
        
        if agent.retriever is None:
            return "The knowledge base is not available. Please ensure the database is configured and has documents loaded."

        result = agent.execute(task)
        
        if not result.success or not result.summary:
            return "I couldn't find specific operational guidance for that query. Please check with your operations team."
            
        return result.summary
        
    except Exception as error:
        LOGGER.exception("Command Nexus operational response failed")
        return "I'm having trouble accessing the knowledge base right now. Please try again later."
```

## backend/api/adapters/frontend_services/maintenance_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/maintenance_adapter.py`

```python
"""Read-only maintenance planning data from the shared MAO runtime."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _result_index() -> dict[tuple[str, str], Any]:
    """Index completed agent output by its workflow task and assigned agent."""
    kernel = runtime.kernel
    return {
        (result.metadata.get("task_name", ""), result.agent_name): result
        for result in kernel.state.agent_results
    }


def _task_asset_name(task: Any, result: Any | None) -> str:
    """Resolve an asset label only when it is present in live task/result data."""
    kernel = runtime.kernel
    input_data = getattr(task, "input_data", {}) or {}
    output_data = getattr(task, "output_data", {}) or {}
    for source in (input_data, output_data, getattr(result, "metadata", {}) or {}):
        asset_id = source.get("asset_name") or source.get("asset_id")
        if asset_id:
            asset = kernel.asset_service.get(asset_id)
            return asset.name if asset else str(asset_id)
    return "Not specified"


def _priority_label(priority: int) -> str:
    return f"P{max(1, min(int(priority), 3))}"


def get_maintenance_plan() -> dict:
    """Format state-manager tasks and agent output for the planner UI."""
    kernel = runtime.kernel
    results = _result_index()
    rows = []
    for task in kernel.state.get_tasks():
        result = results.get((task.name, task.assigned_agent))
        rows.append(
            {
                "Priority": _priority_label(task.priority),
                "Asset": _task_asset_name(task, result),
                "Work order": task.description,
                "Owner": task.assigned_agent.replace("_", " ").title(),
                "State": "Completed" if result and result.success else task.status.value.title(),
                "Confidence": (
                    f"{round(result.confidence * 100)}%" if result else "Not available"
                ),
            }
        )

    maintenance_results = [
        result for result in kernel.state.agent_results if result.agent_name == "maintenance"
    ]
    planning_results = [
        result for result in kernel.state.agent_results if result.agent_name == "planning"
    ]
    latest_maintenance = maintenance_results[-1] if maintenance_results else None
    latest_plan = planning_results[-1] if planning_results else None
    owners = defaultdict(int)
    for row in rows:
        owners[row["Owner"]] += 1

    rationale = []
    if latest_plan:
        rationale = latest_plan.recommendations or latest_plan.evidence
    elif latest_maintenance:
        rationale = latest_maintenance.recommendations or latest_maintenance.evidence

    return {
        "tasks": rows,
        "metrics": [
            ("Planned work", str(len(rows)), "From MAO task state", "cyan"),
            ("High priority", str(sum(row["Priority"] == "P1" for row in rows)), "P1 workflow tasks", "red"),
            ("Assigned teams", str(len(owners)), "Derived from task owners", "green"),
            ("Maintenance results", str(len(maintenance_results)), "Live MAO outputs", "violet"),
        ],
        "rationale": rationale,
        "priority": (
            latest_maintenance.metadata.get("priority", "Not available")
            if latest_maintenance
            else "Not available"
        ),
        "downtime": (
            latest_maintenance.metadata.get("downtime", "Not available")
            if latest_maintenance
            else "Not available"
        ),
    }
```

## backend/api/adapters/frontend_services/report_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/report_adapter.py`

```python
"""Report adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api


def get_reports():
    """Get execution reports."""
    reports_data = api.get_reports()
    
    formatted_reports = []
    for report in reports_data[-10:]:
        formatted_reports.append({
            "Report": report["id"][:8],
            "Title": report["workflow"],
            "Workflow": report["workflow"],
            "Status": "Completed" if report["success"] else "Escalated",
            "Generated": report["completed_at"][:16] if "completed_at" in report else "N/A",
        })
    
    preview = {}
    if reports_data:
        latest = reports_data[-1]
        preview = {
            "Report": latest["id"][:8],
            "Title": latest["workflow"],
            "Summary": latest["summary"][:200] + "..." if len(latest.get("summary", "")) > 200 else latest.get("summary", ""),
            "Recommendation": "Review execution report for details."
        }
    
    metrics = [
        ("Reports generated", str(len(reports_data)), "From MAO executions", "cyan"),
        ("Resolved incidents", str(sum(1 for r in reports_data if r.get("success"))), "Successful workflows", "green"),
        ("Average confidence", f"{round(sum(r.get('confidence', 0) for r in reports_data) / len(reports_data) * 100, 1)}%" if reports_data else "N/A", "Execution quality", "green"),
        ("Pending review", str(sum(1 for r in reports_data if not r.get("success"))), "Requires attention", "amber"),
    ]
    
    return {
        "metrics": metrics,
        "reports": formatted_reports,
        "preview": preview,
    }
```

## backend/api/adapters/frontend_services/telemetry_adapter.py

**Folder path:** `backend/api/adapters/frontend_services`

**File path:** `backend/api/adapters/frontend_services/telemetry_adapter.py`

```python
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def get_asset_telemetry(asset_id):
    kernel = runtime.kernel
    readings = kernel.state.get_history(asset_id)

    history = []

    for reading in readings:
        history.append(
            {
                "Timestamp": reading.timestamp,
                "Sensor": reading.sensor_type,
                "Value": reading.value,
                "Unit": reading.unit,
            }
        )

    return {
        "history": history,
        "latest": history[-1] if history else None,
    }
```

## backend/api/adapters/health_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/health_adapter.py`

```python
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def get_asset_health(asset_id):
    kernel = runtime.kernel
    readings = kernel.state.get_history(asset_id)

    health = kernel.health.calculate_health(
        readings
    )

    return {
        "health": health,
        "readings": readings
    }
```

## backend/api/adapters/health_prediction_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/health_prediction_adapter.py`

```python
"""Health prediction using computation engine."""

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.computation_engine import ComputationEngine


def get_health_prediction(asset_id, horizon_days=14):
    """Get health prediction using the computation engine."""
    kernel = runtime.kernel
    engine = ComputationEngine()
    
    readings = kernel.state.get_history(asset_id)
    asset = kernel.asset_service.get(asset_id)
    
    if not asset or not readings:
        return {
            "health": 100,
            "rul": "365 days",
            "failure_probability": "0%",
            "confidence": "Low",
            "historical": {"Historical health": []},
            "predicted": {"Predicted health": [], "Intervention threshold": []},
            "telemetry": []
        }
    
    # Get current metrics
    metrics = engine.compute_asset(asset, readings)
    
    # Calculate historical health
    historical = []
    for i in range(len(readings)):
        h = engine._calculate_health(
            readings[:i+1],
            engine.config.get_thresholds(metrics["asset_type"]),
            {}  # weights
        )
        historical.append(round(h, 1))
    
    # Predict future health
    current_health = metrics["health"]
    degradation_rate = metrics["degradation_rate"]
    
    predicted = []
    for day in range(horizon_days):
        health = current_health - (degradation_rate * 5 * (day + 1))
        predicted.append(round(max(0, health), 1))
    
    # Format RUL
    rul_days = metrics["rul_days"]
    if rul_days >= 365:
        rul_str = "365+ days"
    elif rul_days >= 90:
        rul_str = f"{int(rul_days)} days"
    elif rul_days >= 30:
        rul_str = f"{int(rul_days)} days"
    elif rul_days >= 7:
        rul_str = f"{int(rul_days)} days"
    else:
        rul_str = f"{int(rul_days)} days"
    
    return {
        "health": round(metrics["health"]),
        "rul": rul_str,
        "failure_probability": f"{metrics['failure_probability']:.1f}%",
        "confidence": f"{metrics['confidence'] * 100:.1f}%",
        "historical": {"Historical health": historical},
        "predicted": {
            "Predicted health": predicted,
            "Intervention threshold": [70] * horizon_days
        },
        "telemetry": format_telemetry(readings)
    }


def format_telemetry(readings):
    """Format telemetry for display."""
    data = []
    for reading in readings[-10:]:
        data.append({
            "Sensor": reading.sensor_type.value,
            "Observed": reading.value,
            "Time": reading.timestamp.strftime("%H:%M:%S")
        })
    return data
```

## backend/api/adapters/incident_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/incident_adapter.py`

```python
"""Incident adapter with dynamic severity calculation from config."""

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime
from services.incident_service import IncidentService
from services.ai_config import AIConfigGenerator


def trigger_incident(incident_type):
    """Trigger an incident and return formatted results."""
    simulator = runtime.simulator
    service = IncidentService(simulator)
    result = service.trigger_incident(incident_type)
    
    try:
        import streamlit as st
        reports = result.get("reports", [])
        if reports:
            events = []
            for i, report in enumerate(reports):
                agent_name = getattr(report, 'workflow_name', 'Unknown')
                if i == 0:
                    events.append(("⏱️ 00:00", "🚨 Incident detected"))
                events.append((f"⏱️ 00:{i+2:02d}", f"🤖 {agent_name} completed"))
            
            last_report = reports[-1] if reports else None
            if last_report:
                summary = getattr(last_report, 'final_summary', '')
                if "planning" in summary.lower():
                    events.append(("⏱️ 00:12", "✅ Investigation complete"))
            
            st.session_state.incident_events = events
            st.session_state.investigation_complete = True
    except Exception as e:
        print(f"⚠️ Could not update session state: {e}")
    
    return result


def get_incidents():
    """Get all incidents from the runtime."""
    kernel = runtime.kernel
    events = kernel.event_store.all()

    incidents = []
    for event in events:
        severity = calculate_severity(event)
        incidents.append({
            "Incident": event.name,
            "Asset": event.source,
            "Severity": severity,
            "Detected": event.timestamp.strftime("%H:%M:%S") if hasattr(event, 'timestamp') else "Unknown",
            "Payload": event.payload,
        })

    return incidents


def calculate_severity(event):
    """
    Calculate severity from event payload using dynamic thresholds from AI config.
    """
    payload = getattr(event, 'payload', {})
    
    try:
        config = AIConfigGenerator()
        asset_type = payload.get("asset_type", "Pump")
        thresholds = config.get_thresholds(asset_type)
        severity_map = config.get_config().get("severity_mapping", {
            "Critical": 1, "High": 2, "Medium": 3, "Low": 4
        })
        
        severity_scores = {}
        
        if "pressure" in payload:
            pressure_max = thresholds.get("pressure_max", 150)
            pressure_val = payload["pressure"]
            ratio = pressure_val / pressure_max
            if ratio >= 1.5:
                severity_scores["pressure"] = 1
            elif ratio >= 1.2:
                severity_scores["pressure"] = 2
            elif ratio >= 1.05:
                severity_scores["pressure"] = 3
            else:
                severity_scores["pressure"] = 4
        
        if "temperature" in payload:
            temp_max = thresholds.get("temperature_max", 85)
            temp_val = payload["temperature"]
            ratio = temp_val / temp_max
            if ratio >= 1.5:
                severity_scores["temperature"] = 1
            elif ratio >= 1.2:
                severity_scores["temperature"] = 2
            elif ratio >= 1.05:
                severity_scores["temperature"] = 3
            else:
                severity_scores["temperature"] = 4
        
        if "gas" in payload:
            gas_max = thresholds.get("gas_max", 40)
            gas_val = payload["gas"]
            ratio = gas_val / gas_max
            if ratio >= 1.5:
                severity_scores["gas"] = 1
            elif ratio >= 1.2:
                severity_scores["gas"] = 2
            elif ratio >= 1.05:
                severity_scores["gas"] = 3
            else:
                severity_scores["gas"] = 4
        
        if "vibration" in payload:
            vib_max = thresholds.get("vibration_max", 8)
            vib_val = payload["vibration"]
            ratio = vib_val / vib_max
            if ratio >= 1.5:
                severity_scores["vibration"] = 1
            elif ratio >= 1.2:
                severity_scores["vibration"] = 2
            elif ratio >= 1.05:
                severity_scores["vibration"] = 3
            else:
                severity_scores["vibration"] = 4
        
        if "flow" in payload:
            flow_min = thresholds.get("flow_min", 25)
            flow_val = payload["flow"]
            ratio = flow_min / flow_val if flow_val > 0 else 10
            if ratio >= 2:
                severity_scores["flow"] = 1
            elif ratio >= 1.5:
                severity_scores["flow"] = 2
            elif ratio >= 1.2:
                severity_scores["flow"] = 3
            else:
                severity_scores["flow"] = 4
        
        if severity_scores:
            worst_score = min(severity_scores.values())
            reverse_map = {v: k for k, v in severity_map.items()}
            return reverse_map.get(worst_score, "Medium")
        
    except Exception as e:
        print(f"⚠️ Severity calculation failed: {e}")
    
    return "Medium"
```

## backend/api/adapters/knowledge_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/knowledge_adapter.py`

```python
"""Read-only Knowledge Base access through the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


class KnowledgeSearchError(RuntimeError):
    """Raised when the registered knowledge retrieval path is unavailable."""


__all__ = ["KnowledgeSearchError", "search_knowledge"]

def search_knowledge(query: str) -> list[dict[str, str]]:
    """Return normalized Neon retrieval results from the registered KnowledgeAgent."""
    normalized_query = query.strip()
    if not normalized_query:
        return []

    try:
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise KnowledgeSearchError("Knowledge Agent is not available. Please ensure the knowledge base is loaded.")
        if agent.retriever is None:
            raise KnowledgeSearchError("Knowledge retriever is not initialized. Please build the knowledge base first.")
    except KnowledgeSearchError:
        raise
    except Exception as error:
        raise KnowledgeSearchError(f"Knowledge service unavailable: {str(error)[:100]}") from error

    try:
        documents = agent.retriever.retrieve(normalized_query)
    except Exception as error:
        raise KnowledgeSearchError(f"Retrieval failed: {str(error)[:100]}") from error

    results = []
    for document in documents:
        metadata = document.metadata or {}
        source = str(metadata.get("source", "Unknown source"))
        results.append(
            {
                "content": document.page_content,
                "source": source,
                "filename": Path(source).name or source,
            }
        )
    return results
```

## backend/api/adapters/knowledge_agent_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/knowledge_agent_adapter.py`

```python
"""Frontend routing for Command Nexus conversational and operational requests."""

from __future__ import annotations

from functools import lru_cache
import logging
from pathlib import Path
import re
import sys
from typing import TYPE_CHECKING, Callable

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if TYPE_CHECKING:
    from agents.knowledge import KnowledgeAgent

LOGGER = logging.getLogger(__name__)
ProgressCallback = Callable[[str], None]

OPERATIONAL_KEYWORDS = (
    "asset", "compressor", "pump", "pipeline", "tank", "valve", "maintenance",
    "inspection", "incident", "alarm", "safety", "hazard", "pressure",
    "temperature", "vibration", "flow", "gas", "refinery", "sop", "procedure",
    "equipment", "motor", "turbine", "boiler", "heat exchanger", "reactor",
    "distillation", "column", "flare", "corrosion", "shutdown", "startup",
    "trip", "failure", "process", "telemetry", "sensor", "knowledge",
)


def is_operational_query(question: str) -> bool:
    """Return whether a question requires the refinery operations path."""
    normalized = re.sub(r"\s+", " ", question.strip().casefold())
    return bool(normalized and any(keyword in normalized for keyword in OPERATIONAL_KEYWORDS))


def generate_conversational_response(question: str) -> str:
    """Use Gemini for casual conversation without starting the operational path."""
    from services.llm import LLMManager

    prompt = f"""
You are Command Nexus, a polished industrial operations copilot.

Reply naturally to this casual user message: {question!r}

Keep the response concise, warm, and professional. You may introduce yourself
as an industrial operations copilot and offer help with refinery operations,
equipment, maintenance, incident response, and safety. Do not provide
operational facts, citations, or technical instructions for a casual message.
Never mention implementation, search, retrieval, documents, a knowledge base,
databases, RAG, prompts, APIs, or model internals.
"""
    try:
        return LLMManager().generate(prompt)
    except Exception as e:
        LOGGER.error(f"Conversational response failed: {e}")
        return "I'm here to help with refinery operations. What would you like to know?"


def _emit(callback: ProgressCallback | None, message: str) -> None:
    LOGGER.info(message)
    if callback is not None:
        callback(message)


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Return the KnowledgeAgent registered on the shared MAO kernel."""
    try:
        from services.runtime import runtime
        kernel = runtime.kernel
        agent = kernel.registry.get("knowledge")
        if agent is None:
            raise RuntimeError("KnowledgeAgent is not registered on the MAO kernel.")
        return agent
    except Exception as error:
        raise KnowledgeAgentUnavailable("Command Nexus is temporarily unavailable. Please try again shortly.") from error


def ask_knowledge_agent(question: str, on_progress: ProgressCallback | None = None) -> str:
    """Route casual conversation to Gemini and operational questions to KnowledgeAgent."""
    _emit(on_progress, "Command Nexus received a question.")
    normalized_question = question.strip()
    if not normalized_question:
        raise KnowledgeAgentUnavailable("Enter a question before asking Command Nexus.")

    if not is_operational_query(normalized_question):
        _emit(on_progress, "Conversational request detected.")
        try:
            return generate_conversational_response(normalized_question)
        except Exception as error:
            LOGGER.exception("Command Nexus conversational response failed")
            return "I'm here to help! What would you like to know about refinery operations?"

    _emit(on_progress, "Preparing an operational assessment.")
    try:
        from mao.models.task import Task

        task = Task(
            name="Operator knowledge query",
            description=normalized_question,
            assigned_agent="knowledge",
        )
        agent = get_knowledge_agent()
        
        if agent.retriever is None:
            return "The knowledge base is not available. Please ensure the database is configured and has documents loaded."

        result = agent.execute(task)
        
        if not result.success or not result.summary:
            return "I couldn't find specific operational guidance for that query. Please check with your operations team."
            
        return result.summary
        
    except Exception as error:
        LOGGER.exception("Command Nexus operational response failed")
        return "I'm having trouble accessing the knowledge base right now. Please try again later."
```

## backend/api/adapters/maintenance_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/maintenance_adapter.py`

```python
"""Read-only maintenance planning data from the shared MAO runtime."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def _result_index() -> dict[tuple[str, str], Any]:
    """Index completed agent output by its workflow task and assigned agent."""
    kernel = runtime.kernel
    return {
        (result.metadata.get("task_name", ""), result.agent_name): result
        for result in kernel.state.agent_results
    }


def _task_asset_name(task: Any, result: Any | None) -> str:
    """Resolve an asset label only when it is present in live task/result data."""
    kernel = runtime.kernel
    input_data = getattr(task, "input_data", {}) or {}
    output_data = getattr(task, "output_data", {}) or {}
    for source in (input_data, output_data, getattr(result, "metadata", {}) or {}):
        asset_id = source.get("asset_name") or source.get("asset_id")
        if asset_id:
            asset = kernel.asset_service.get(asset_id)
            return asset.name if asset else str(asset_id)
    return "Not specified"


def _priority_label(priority: int) -> str:
    return f"P{max(1, min(int(priority), 3))}"


def get_maintenance_plan() -> dict:
    """Format state-manager tasks and agent output for the planner UI."""
    kernel = runtime.kernel
    results = _result_index()
    rows = []
    for task in kernel.state.get_tasks():
        result = results.get((task.name, task.assigned_agent))
        rows.append(
            {
                "Priority": _priority_label(task.priority),
                "Asset": _task_asset_name(task, result),
                "Work order": task.description,
                "Owner": task.assigned_agent.replace("_", " ").title(),
                "State": "Completed" if result and result.success else task.status.value.title(),
                "Confidence": (
                    f"{round(result.confidence * 100)}%" if result else "Not available"
                ),
            }
        )

    maintenance_results = [
        result for result in kernel.state.agent_results if result.agent_name == "maintenance"
    ]
    planning_results = [
        result for result in kernel.state.agent_results if result.agent_name == "planning"
    ]
    latest_maintenance = maintenance_results[-1] if maintenance_results else None
    latest_plan = planning_results[-1] if planning_results else None
    owners = defaultdict(int)
    for row in rows:
        owners[row["Owner"]] += 1

    rationale = []
    if latest_plan:
        rationale = latest_plan.recommendations or latest_plan.evidence
    elif latest_maintenance:
        rationale = latest_maintenance.recommendations or latest_maintenance.evidence

    return {
        "tasks": rows,
        "metrics": [
            ("Planned work", str(len(rows)), "From MAO task state", "cyan"),
            ("High priority", str(sum(row["Priority"] == "P1" for row in rows)), "P1 workflow tasks", "red"),
            ("Assigned teams", str(len(owners)), "Derived from task owners", "green"),
            ("Maintenance results", str(len(maintenance_results)), "Live MAO outputs", "violet"),
        ],
        "rationale": rationale,
        "priority": (
            latest_maintenance.metadata.get("priority", "Not available")
            if latest_maintenance
            else "Not available"
        ),
        "downtime": (
            latest_maintenance.metadata.get("downtime", "Not available")
            if latest_maintenance
            else "Not available"
        ),
    }
```

## backend/api/adapters/report_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/report_adapter.py`

```python
"""Report adapter using BackendAPI."""

from api.adapters.backend_api_new import api


def get_reports():
    """Get execution reports."""
    reports_data = api.get_reports()
    
    formatted_reports = []
    for report in reports_data[-10:]:
        formatted_reports.append({
            "Report": report["id"][:8],
            "Title": report["workflow"],
            "Workflow": report["workflow"],
            "Status": "Completed" if report["success"] else "Escalated",
            "Generated": report["completed_at"][:16] if "completed_at" in report else "N/A",
        })
    
    preview = {}
    if reports_data:
        latest = reports_data[-1]
        preview = {
            "Report": latest["id"][:8],
            "Title": latest["workflow"],
            "Summary": latest["summary"][:200] + "..." if len(latest.get("summary", "")) > 200 else latest.get("summary", ""),
            "Recommendation": "Review execution report for details."
        }
    
    metrics = [
        ("Reports generated", str(len(reports_data)), "From MAO executions", "cyan"),
        ("Resolved incidents", str(sum(1 for r in reports_data if r.get("success"))), "Successful workflows", "green"),
        ("Average confidence", f"{round(sum(r.get('confidence', 0) for r in reports_data) / len(reports_data) * 100, 1)}%" if reports_data else "N/A", "Execution quality", "green"),
        ("Pending review", str(sum(1 for r in reports_data if not r.get("success"))), "Requires attention", "amber"),
    ]
    
    return {
        "metrics": metrics,
        "reports": formatted_reports,
        "preview": preview,
    }
```

## backend/api/adapters/telemetry_adapter.py

**Folder path:** `backend/api/adapters`

**File path:** `backend/api/adapters/telemetry_adapter.py`

```python
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def get_asset_telemetry(asset_id):
    kernel = runtime.kernel
    readings = kernel.state.get_history(asset_id)

    history = []

    for reading in readings:
        history.append(
            {
                "Timestamp": reading.timestamp,
                "Sensor": reading.sensor_type,
                "Value": reading.value,
                "Unit": reading.unit,
            }
        )

    return {
        "history": history,
        "latest": history[-1] if history else None,
    }
```

## backend/api/main.py

**Folder path:** `backend/api`

**File path:** `backend/api/main.py`

```python
"""FastAPI backend for RigOS."""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
import asyncio
from datetime import datetime
import time

# Add parent directory to path
BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

print(f"📁 Backend root: {BACKEND_ROOT}")

# ============================================
# FORCE LOAD REAL SERVICES
# ============================================

REAL_SERVICES_AVAILABLE = False
backend_api = None
notification_service = None
runtime = None

try:
    print("🔄 Loading real services...")
    
    # Force import of services
    from services.runtime import runtime as _runtime
    runtime = _runtime
    print("✅ runtime loaded")
    
    from services.notification_service import notification_service as _notification
    notification_service = _notification
    print("✅ notification_service loaded")
    
    # Import adapters
    from api.adapters.backend_api_new import api as _backend_api
    backend_api = _backend_api
    print("✅ backend_api loaded")
    
    REAL_SERVICES_AVAILABLE = True
    print(f"✅ Real services loaded successfully!")
    print(f"✅ Assets available: {len(runtime.kernel.asset_service.all_assets())}")
    
except Exception as e:
    print(f"⚠️ Real services failed to load: {e}")
    import traceback
    traceback.print_exc()
    
    # Create mock fallbacks
    class MockRuntime:
        class MockKernel:
            class MockAssetService:
                def all_assets(self):
                    return []
            asset_service = MockAssetService()
            state = None
            event_store = None
            registry = None
            _simulation_running = False
        kernel = MockKernel()
    runtime = MockRuntime()
    
    class MockNotificationService:
        def get_notifications(self, limit=5, unread_only=True):
            return []
    notification_service = MockNotificationService()
    
    class MockBackendAPI:
        def get_assets(self):
            return []
        def get_incidents(self):
            return []
        def get_asset_telemetry(self, asset_id, limit):
            return []
        def trigger_incident(self, incident_type):
            return {"id": "mock-1", "type": incident_type, "status": "triggered"}
    backend_api = MockBackendAPI()

app = FastAPI(title="RigOS API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "RigOS API is running",
        "real_services": REAL_SERVICES_AVAILABLE,
        "assets_count": len(backend_api.get_assets()) if hasattr(backend_api, 'get_assets') else 0
    }

@app.get("/api/assets")
async def get_assets():
    try:
        return backend_api.get_assets()
    except Exception as e:
        print(f"⚠️ Error fetching assets: {e}")
        return []

@app.get("/api/incidents")
async def get_incidents():
    try:
        return backend_api.get_incidents()
    except Exception as e:
        print(f"⚠️ Error fetching incidents: {e}")
        return []

@app.post("/api/incidents/{incident_type}")
async def trigger_incident(incident_type: str):
    try:
        result = backend_api.trigger_incident(incident_type)
        return result
    except Exception as e:
        print(f"⚠️ Error triggering incident: {e}")
        return {"error": str(e)}

@app.get("/api/telemetry/{asset_id}")
async def get_telemetry(asset_id: str, limit: int = 30):
    try:
        return backend_api.get_asset_telemetry(asset_id, limit)
    except Exception as e:
        print(f"⚠️ Error fetching telemetry: {e}")
        import random
        data = []
        for i in range(min(limit, 20)):
            data.append({
                "timestamp": datetime.now().isoformat(),
                "value": 70 + random.randint(-10, 10),
                "sensor_type": "Pressure"
            })
        return data

@app.get("/api/predictions/{asset_id}")
async def get_prediction(asset_id: str, horizon: int = 14):
    try:
        from api.adapters.health_prediction_adapter import get_health_prediction
        return get_health_prediction(asset_id, horizon)
    except Exception as e:
        print(f"⚠️ Error fetching prediction: {e}")
        return {"health": 85, "rul": "365 days", "failure_probability": "15%", "confidence": "92%"}

@app.get("/api/dashboard")
async def get_dashboard():
    try:
        from api.adapters.dashboard_adapter import get_dashboard
        return get_dashboard()
    except Exception as e:
        print(f"⚠️ Error fetching dashboard: {e}")
        return {"total_assets": 0, "healthy_count": 0, "incident_count": 0, "avg_health": 0}

# ============================================
# WEBSOCKET
# ============================================

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            try:
                assets = backend_api.get_assets()
                incidents = backend_api.get_incidents()
                
                notifications = []
                try:
                    raw_notifications = notification_service.get_notifications(limit=5, unread_only=True)
                    for n in raw_notifications[:5]:
                        notifications.append({
                            "id": getattr(n, 'id', 'unknown'),
                            "title": getattr(n, 'title', 'Notification'),
                            "message": getattr(n, 'message', ''),
                            "severity": getattr(n, 'severity', 'info'),
                            "timestamp": n.timestamp.isoformat() if hasattr(n, 'timestamp') else datetime.now().isoformat(),
                            "revenue_impact": getattr(n, 'revenue_impact', None)
                        })
                except Exception as e:
                    pass
                
                await websocket.send_json({
                    "type": "update",
                    "data": {
                        "assets": assets,
                        "incidents": incidents,
                        "notifications": notifications,
                        "timestamp": datetime.now().isoformat()
                    }
                })
                
            except Exception as e:
                print(f"⚠️ WebSocket update error: {e}")
            
            await asyncio.sleep(2)
            
    except Exception as e:
        print(f"⚠️ WebSocket disconnected: {e}")
        manager.disconnect(websocket)

@app.on_event("startup")
async def startup_event():
    """Print startup status."""
    print("=" * 50)
    print("🚀 RIGOS API STARTUP")
    print("=" * 50)
    print(f"✅ Real services: {REAL_SERVICES_AVAILABLE}")
    if REAL_SERVICES_AVAILABLE:
        try:
            assets = backend_api.get_assets()
            print(f"✅ Assets loaded: {len(assets)}")
        except Exception as e:
            print(f"⚠️ Could not load assets: {e}")
    print("=" * 50)

# ============================================
# AGENT ROUTES
# ============================================

@app.get("/api/agents")
async def get_agents():
    try:
        from api.adapters.agent_adapter import get_agents as agents
        return agents()
    except Exception as e:
        print(f"⚠️ Error fetching agents: {e}")
        return []

@app.get("/api/agent-metrics")
async def get_agent_metrics():
    try:
        from api.adapters.agent_adapter import get_agent_metrics as metrics
        return metrics()
    except Exception as e:
        print(f"⚠️ Error fetching agent metrics: {e}")
        return []

@app.get("/api/agent-activity")
async def get_agent_activity():
    try:
        from api.adapters.agent_activity_adapter import get_agent_activity as activity
        return activity()
    except Exception as e:
        print(f"⚠️ Error fetching agent activity: {e}")
        return []

# ============================================
# MAINTENANCE ROUTES
# ============================================

@app.get("/api/maintenance")
async def get_maintenance():
    try:
        from api.adapters.maintenance_adapter import get_maintenance_plan as plan
        return plan()
    except Exception as e:
        print(f"⚠️ Error fetching maintenance plan: {e}")
        return {"tasks": []}

# ============================================
# REPORTS ROUTES
# ============================================

@app.get("/api/reports")
async def get_reports():
    try:
        from api.adapters.report_adapter import get_reports as reports
        return reports()
    except Exception as e:
        print(f"⚠️ Error fetching reports: {e}")
        return []

# ============================================
# DIGITAL TWIN ROUTES
# ============================================

@app.get("/api/twin-assets")
async def get_twin_assets():
    try:
        from api.adapters.digital_twin_adapter import get_twin_assets as twin
        return twin()
    except Exception as e:
        print(f"⚠️ Error fetching twin assets: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## backend/api/websocket/manager.py

**Folder path:** `backend/api/websocket`

**File path:** `backend/api/websocket/manager.py`

```python
"""WebSocket manager for real-time updates."""

import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            # Send mock updates
            await websocket.send_json({
                "type": "update",
                "data": {
                    "assets": [
                        {"id": "1", "name": "Pump A-01", "health": 95, "status": "Running"},
                        {"id": "2", "name": "Compressor C-12", "health": 82, "status": "Running"},
                    ],
                    "incidents": [],
                    "notifications": [
                        {
                            "id": "1",
                            "title": "System Online",
                            "message": "All systems operational",
                            "severity": "info",
                            "timestamp": datetime.now().isoformat()
                        }
                    ],
                    "timestamp": datetime.now().isoformat()
                }
            })
            
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

## backend/data/ai_config.json

**Folder path:** `backend/data`

**File path:** `backend/data/ai_config.json`

```json
{
  "asset_types": {
    "Pump": {
      "thresholds": {
        "pressure_max": 150,
        "temperature_max": 85,
        "gas_max": 40,
        "vibration_max": 8,
        "flow_min": 25
      },
      "weight": {
        "pressure_weight": 30,
        "temperature_weight": 25,
        "gas_weight": 35,
        "vibration_weight": 20,
        "flow_weight": 10
      },
      "degradation_rate": 0.5,
      "critical_health": 50
    },
    "Compressor": {
      "thresholds": {
        "pressure_max": 160,
        "temperature_max": 90,
        "gas_max": 35,
        "vibration_max": 10,
        "flow_min": 30
      },
      "weight": {
        "pressure_weight": 35,
        "temperature_weight": 20,
        "gas_weight": 25,
        "vibration_weight": 30,
        "flow_weight": 10
      },
      "degradation_rate": 0.6,
      "critical_health": 50
    },
    "Tank": {
      "thresholds": {
        "pressure_max": 50,
        "temperature_max": 60,
        "gas_max": 50,
        "vibration_max": 3,
        "flow_min": 5
      },
      "weight": {
        "pressure_weight": 40,
        "temperature_weight": 15,
        "gas_weight": 35,
        "vibration_weight": 5,
        "flow_weight": 5
      },
      "degradation_rate": 0.2,
      "critical_health": 40
    },
    "Valve": {
      "thresholds": {
        "pressure_max": 200,
        "temperature_max": 120,
        "gas_max": 30,
        "vibration_max": 5,
        "flow_min": 10
      },
      "weight": {
        "pressure_weight": 35,
        "temperature_weight": 20,
        "gas_weight": 25,
        "vibration_weight": 10,
        "flow_weight": 10
      },
      "degradation_rate": 0.4,
      "critical_health": 50
    },
    "Pipeline": {
      "thresholds": {
        "pressure_max": 180,
        "temperature_max": 100,
        "gas_max": 45,
        "vibration_max": 6,
        "flow_min": 50
      },
      "weight": {
        "pressure_weight": 40,
        "temperature_weight": 20,
        "gas_weight": 25,
        "vibration_weight": 5,
        "flow_weight": 10
      },
      "degradation_rate": 0.3,
      "critical_health": 45
    },
    "Heat Exchanger": {
      "thresholds": {
        "pressure_max": 130,
        "temperature_max": 250,
        "gas_max": 20,
        "vibration_max": 4,
        "flow_min": 40
      },
      "weight": {
        "pressure_weight": 20,
        "temperature_weight": 45,
        "gas_weight": 15,
        "vibration_weight": 5,
        "flow_weight": 15
      },
      "degradation_rate": 0.4,
      "critical_health": 50
    },
    "Reactor": {
      "thresholds": {
        "pressure_max": 220,
        "temperature_max": 350,
        "gas_max": 60,
        "vibration_max": 7,
        "flow_min": 20
      },
      "weight": {
        "pressure_weight": 30,
        "temperature_weight": 35,
        "gas_weight": 20,
        "vibration_weight": 10,
        "flow_weight": 5
      },
      "degradation_rate": 0.7,
      "critical_health": 60
    },
    "Boiler": {
      "thresholds": {
        "pressure_max": 250,
        "temperature_max": 400,
        "gas_max": 50,
        "vibration_max": 6,
        "flow_min": 35
      },
      "weight": {
        "pressure_weight": 35,
        "temperature_weight": 40,
        "gas_weight": 15,
        "vibration_weight": 5,
        "flow_weight": 5
      },
      "degradation_rate": 0.6,
      "critical_health": 55
    },
    "Turbine": {
      "thresholds": {
        "pressure_max": 190,
        "temperature_max": 300,
        "gas_max": 25,
        "vibration_max": 12,
        "flow_min": 45
      },
      "weight": {
        "pressure_weight": 25,
        "temperature_weight": 25,
        "gas_weight": 10,
        "vibration_weight": 35,
        "flow_weight": 5
      },
      "degradation_rate": 0.8,
      "critical_health": 60
    },
    "Motor": {
      "thresholds": {
        "pressure_max": 80,
        "temperature_max": 110,
        "gas_max": 15,
        "vibration_max": 9,
        "flow_min": 15
      },
      "weight": {
        "pressure_weight": 10,
        "temperature_weight": 40,
        "gas_weight": 10,
        "vibration_weight": 35,
        "flow_weight": 5
      },
      "degradation_rate": 0.5,
      "critical_health": 50
    },
    "Generator": {
      "thresholds": {
        "pressure_max": 90,
        "temperature_max": 115,
        "gas_max": 20,
        "vibration_max": 9,
        "flow_min": 20
      },
      "weight": {
        "pressure_weight": 10,
        "temperature_weight": 40,
        "gas_weight": 15,
        "vibration_weight": 30,
        "flow_weight": 5
      },
      "degradation_rate": 0.5,
      "critical_health": 50
    },
    "Distillation Column": {
      "thresholds": {
        "pressure_max": 140,
        "temperature_max": 280,
        "gas_max": 45,
        "vibration_max": 5,
        "flow_min": 60
      },
      "weight": {
        "pressure_weight": 30,
        "temperature_weight": 35,
        "gas_weight": 20,
        "vibration_weight": 5,
        "flow_weight": 10
      },
      "degradation_rate": 0.4,
      "critical_health": 50
    }
  },
  "workflow_sequences": {
    "pressure_spike": [
      "sensor",
      "safety",
      "diagnostic",
      "knowledge",
      "maintenance",
      "planning",
      "prediction",
      "notification",
      "report"
    ],
    "gas_leak": [
      "sensor",
      "safety",
      "diagnostic",
      "knowledge",
      "maintenance",
      "planning",
      "prediction",
      "notification",
      "report"
    ],
    "high_temperature": [
      "sensor",
      "safety",
      "diagnostic",
      "knowledge",
      "maintenance",
      "planning",
      "prediction",
      "notification",
      "report"
    ],
    "high_vibration": [
      "sensor",
      "safety",
      "diagnostic",
      "knowledge",
      "maintenance",
      "planning",
      "prediction",
      "notification",
      "report"
    ],
    "flow_restriction": [
      "sensor",
      "safety",
      "diagnostic",
      "knowledge",
      "maintenance",
      "planning",
      "prediction",
      "notification",
      "report"
    ]
  },
  "severity_mapping": {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
  },
  "health_status_mapping": {
    "healthy": 80,
    "warning": 50,
    "critical": 30
  },
  "prediction": {
    "confidence_weight": 0.55,
    "sample_weight": 0.02,
    "max_samples": 20,
    "rul_max_days": 365,
    "rul_min_days": 1
  },
  "notification": {
    "critical_failure_threshold": 70,
    "warning_failure_threshold": 40,
    "info_failure_threshold": 0
  }
}
```

## backend/database/__init__.py

**Folder path:** `backend/database`

**File path:** `backend/database/__init__.py`

```python
from database.base import Base
from database.connection import engine

from database import models
```

## backend/database/__init__database.py

**Folder path:** `backend/database`

**File path:** `backend/database/__init__database.py`

```python
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


from database.base import Base
from database.connection import engine

# Import models so SQLAlchemy knows them
from database import models


print("Creating Neon tables...")


Base.metadata.create_all(
    bind=engine
)


print("Database initialization complete.")
```

## backend/database/base.py

**Folder path:** `backend/database`

**File path:** `backend/database/base.py`

```python
from sqlalchemy.orm import declarative_base


Base = declarative_base()
```

## backend/database/bootstrap.py

**Folder path:** `backend/database`

**File path:** `backend/database/bootstrap.py`

```python
"""Development-only schema bootstrap. Production uses Alembic migrations."""

from database.base import Base
from database.connection import engine
from database import models  # noqa: F401


def create_schema():
    Base.metadata.create_all(engine)
```

## backend/database/connection.py

**Folder path:** `backend/database`

**File path:** `backend/database/connection.py`

```python
"""Optimized database connection with pooling and query caching."""

import os
from pathlib import Path
from functools import lru_cache
from contextlib import contextmanager
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Add it to .env locally or Streamlit Secrets.")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Scoped session for thread safety
db_session = scoped_session(SessionLocal)


@contextmanager
def get_session_context():
    """Context manager for database sessions with automatic cleanup."""
    session = db_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ✅ SIMPLE SESSION FUNCTION (returns a session, NOT a context manager)
def get_session():
    """Return a database session."""
    return db_session()


# ✅ Cache for frequently accessed data
_cache_data = {}
_cache_timestamps = {}
_CACHE_TTL = 5


def cached_query(key: str, func, *args, **kwargs):
    """Get cached data or compute it."""
    now = time.time()
    if key in _cache_data and now - _cache_timestamps.get(key, 0) < _CACHE_TTL:
        return _cache_data[key]
    
    result = func(*args, **kwargs)
    _cache_data[key] = result
    _cache_timestamps[key] = now
    return result


def invalidate_cache(key: str = None):
    """Invalidate cache for a key or all keys."""
    if key:
        _cache_data.pop(key, None)
        _cache_timestamps.pop(key, None)
    else:
        _cache_data.clear()
        _cache_timestamps.clear()


@lru_cache(maxsize=128)
def get_all_assets_cached():
    """Cache all assets for 5 seconds."""
    session = get_session()
    try:
        from database.models import AssetDB
        return session.query(AssetDB).all()
    finally:
        session.close()


def invalidate_asset_cache():
    """Invalidate the asset cache when new assets are added."""
    get_all_assets_cached.cache_clear()
```

## backend/database/migrations/env.py

**Folder path:** `backend/database/migrations`

**File path:** `backend/database/migrations/env.py`

```python
from logging.config import fileConfig

from alembic import context

from database.base import Base
from database.connection import DATABASE_URL
from database import models  # noqa: F401


config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = context.config.attributes.get("connection")
    if connectable is None:
        from sqlalchemy import create_engine

        connectable = create_engine(DATABASE_URL, pool_pre_ping=True)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## backend/database/migrations/script.py.mako

**Folder path:** `backend/database/migrations`

**File path:** `backend/database/migrations/script.py.mako`

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa


revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
```

## backend/database/migrations/versions/0001_operational_records.py

**Folder path:** `backend/database/migrations/versions`

**File path:** `backend/database/migrations/versions/0001_operational_records.py`

```python
"""Add operational incident, report, action, and activity records.

Revision ID: 0001_operational_records
Revises:
Create Date: 2026-07-22
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_operational_records"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("incidents", sa.Column("status", sa.String(), nullable=True))
    op.add_column("incidents", sa.Column("created_at", sa.DateTime(), nullable=True))

    op.add_column("agent_execution", sa.Column("input", sa.Text(), nullable=True))
    op.add_column("agent_execution", sa.Column("output", sa.Text(), nullable=True))
    op.add_column("agent_execution", sa.Column("recommendations", sa.JSON(), nullable=True))
    op.add_column("agent_execution", sa.Column("decision", sa.String(), nullable=True))
    op.add_column("agent_execution", sa.Column("evidence", sa.JSON(), nullable=True))
    op.add_column("agent_execution", sa.Column("actions_required", sa.JSON(), nullable=True))
    op.add_column(
        "agent_execution",
        sa.Column("requires_human_approval", sa.Boolean(), nullable=True),
    )
    op.add_column("agent_execution", sa.Column("incident_id", sa.String(), nullable=True))

    op.create_table(
        "execution_reports",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("execution_id", sa.String(), nullable=False, unique=True),
        sa.Column("incident_id", sa.String(), nullable=True),
        sa.Column("workflow", sa.String(), nullable=False),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "actions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("incident_id", sa.String(), nullable=True),
        sa.Column("asset_id", sa.String(), nullable=True),
        sa.Column("action_type", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("risk_level", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("requires_human_approval", sa.Boolean(), nullable=False),
        sa.Column("requested_by", sa.String(), nullable=True),
        sa.Column("approved_by", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("executed_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "activity_events",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("incident_id", sa.String(), nullable=True),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table("activity_events")
    op.drop_table("actions")
    op.drop_table("execution_reports")
    op.drop_column("agent_execution", "incident_id")
    op.drop_column("agent_execution", "requires_human_approval")
    op.drop_column("agent_execution", "actions_required")
    op.drop_column("agent_execution", "evidence")
    op.drop_column("agent_execution", "decision")
    op.drop_column("agent_execution", "recommendations")
    op.drop_column("agent_execution", "output")
    op.drop_column("agent_execution", "input")
    op.drop_column("incidents", "created_at")
    op.drop_column("incidents", "status")
```

## backend/database/migrations/versions/0002_add_knowledge_source.py

**Folder path:** `backend/database/migrations/versions`

**File path:** `backend/database/migrations/versions/0002_add_knowledge_source.py`

```python
"""Add the source metadata required for Neon knowledge retrieval.

Revision ID: 0002_add_knowledge_source
Revises: 0001_operational_records
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_add_knowledge_source"
down_revision = "0001_operational_records"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE knowledge ADD COLUMN IF NOT EXISTS source TEXT")
    op.execute(
        "ALTER TABLE knowledge ALTER COLUMN embedding TYPE vector(3072) "
        "USING embedding::vector(3072)"
    )


def downgrade():
    op.execute(
        "ALTER TABLE knowledge ALTER COLUMN embedding TYPE vector(384) "
        "USING embedding::vector(384)"
    )
    op.drop_column("knowledge", "source")
```

## backend/database/models.py

**Folder path:** `backend/database`

**File path:** `backend/database/models.py`

```python
from sqlalchemy import Boolean, Column, DateTime, Float, JSON, String, Text
from database.base import Base
from datetime import datetime
from pgvector.sqlalchemy import Vector
from uuid import uuid4


class AssetDB(Base):

    __tablename__="assets"


    id = Column(
        String,
        primary_key=True,
        default=lambda:str(uuid4())
    )

    name = Column(String)

    asset_type = Column(String)

    location = Column(String)

    health = Column(Float, default=100)

    status = Column(String)



class TelemetryDB(Base):

    __tablename__="telemetry"


    id = Column(
        String,
        primary_key=True,
        default=lambda:str(uuid4())
    )

    asset_id = Column(String)

    sensor_type = Column(String)

    value = Column(Float)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

class IncidentDB(Base):

    __tablename__ = "incidents"

    id = Column(
        String,
        primary_key=True,
        default=lambda:str(uuid4())
    )

    asset_id = Column(String)
    event = Column(String)
    severity = Column(String)
    status = Column(String, default="detected")
    report = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeDB(Base):

    __tablename__ = "knowledge"

    id = Column(
        String,
        primary_key=True,
        default=lambda:str(uuid4())
    )

    content = Column(Text)
    source = Column(Text)
    embedding = Column(
        Vector(3072)
    )

class AgentExecutionDB(Base):

    __tablename__ = "agent_execution"


    id = Column(
        String,
        primary_key=True
    )

    agent_name = Column(String)

    task = Column(String)

    input = Column(Text)

    output = Column(Text)

    success = Column(Boolean)

    confidence = Column(Float)

    summary = Column(Text)

    recommendations = Column(JSON, default=list)

    decision = Column(String)

    evidence = Column(JSON, default=list)

    actions_required = Column(JSON, default=list)

    requires_human_approval = Column(Boolean, default=False)

    incident_id = Column(String)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )


class ExecutionReportDB(Base):

    __tablename__ = "execution_reports"

    id = Column(String, primary_key=True)
    execution_id = Column(String, unique=True, nullable=False)
    incident_id = Column(String)
    workflow = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)
    summary = Column(Text, nullable=False)
    recommendations = Column(JSON, default=list)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)


class ActionDB(Base):

    __tablename__ = "actions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    incident_id = Column(String)
    asset_id = Column(String)
    action_type = Column(String, nullable=False)
    payload = Column(JSON, default=dict)
    risk_level = Column(String, nullable=False)
    status = Column(String, default="pending_approval")
    requires_human_approval = Column(Boolean, default=True)
    requested_by = Column(String)
    approved_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime)


class ActivityEventDB(Base):

    __tablename__ = "activity_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    incident_id = Column(String)
    source = Column(String, nullable=False)
    status = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    evidence = Column(JSON, default=list)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## backend/database/repositories/action_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/action_repo.py`

```python
from database.models import ActionDB


class ActionRepository:

    def __init__(self, session):
        self.session = session

    def create(self, action):
        self.session.add(action)
        self.session.commit()
        self.session.refresh(action)
        return action

    def get_pending(self):
        return (
            self.session.query(ActionDB)
            .filter(ActionDB.status == "pending_approval")
            .order_by(ActionDB.created_at.desc())
            .all()
        )

    def get(self, action_id):
        return self.session.query(ActionDB).filter_by(id=action_id).first()

    def save(self, action):
        self.session.add(action)
        self.session.commit()
        self.session.refresh(action)
        return action
```

## backend/database/repositories/activity_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/activity_repo.py`

```python
from database.models import ActivityEventDB


class ActivityRepository:

    def __init__(self, session):
        self.session = session

    def create(self, activity):
        self.session.add(activity)
        self.session.commit()
        self.session.refresh(activity)
        return activity

    def get_recent(self, limit=200):
        return (
            self.session.query(ActivityEventDB)
            .order_by(ActivityEventDB.created_at.desc())
            .limit(limit)
            .all()
        )
```

## backend/database/repositories/agent_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/agent_repo.py`

```python
from database.models import AgentExecutionDB


class AgentRepository:
    def __init__(self, session):
        self.session = session

    def create(self, execution):
        self.session.add(execution)
        self.session.commit()
        self.session.refresh(execution)
        return execution

    def create_many(self, executions):
        self.session.add_all(executions)
        self.session.commit()
        return executions

    def get_all(self):
        return self.session.query(AgentExecutionDB).order_by(AgentExecutionDB.timestamp.desc()).all()

    def get_recent(self, limit=20):
        return self.session.query(AgentExecutionDB).order_by(AgentExecutionDB.timestamp.desc()).limit(limit).all()

    def get_success_rate(self, agent_name=None):
        query = self.session.query(AgentExecutionDB)
        if agent_name:
            query = query.filter(AgentExecutionDB.agent_name == agent_name)
        executions = query.all()
        if not executions:
            return 0.0
        successful = sum(1 for e in executions if e.success)
        return (successful / len(executions)) * 100
```

## backend/database/repositories/asset_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/asset_repo.py`

```python
"""Optimized Asset Repository with batch operations."""

from database.models import AssetDB
from sqlalchemy import text
from typing import List, Optional


class AssetRepository:
    def __init__(self, session):
        self.session = session

    def create(self, asset):
        self.session.add(asset)
        self.session.commit()
        return asset

    def create_batch(self, assets: List[AssetDB]) -> List[AssetDB]:
        """Batch insert for better performance."""
        self.session.add_all(assets)
        self.session.commit()
        return assets

    def get_all(self):
        return self.session.query(AssetDB).all()

    def get(self, asset_id):
        return self.session.query(AssetDB).filter_by(id=asset_id).first()

    def bulk_update_health(self, updates: dict):
        """Bulk update asset health in one query."""
        if not updates:
            return
        
        case_parts = []
        id_list = []
        for asset_id, health in updates.items():
            case_parts.append(f"WHEN '{asset_id}' THEN {health}")
            id_list.append(f"'{asset_id}'")
        
        if not case_parts:
            return
        
        stmt = f"""
            UPDATE assets 
            SET health = CASE id {' '.join(case_parts)} END,
                status = CASE 
                    WHEN health >= 80 THEN 'Running'
                    WHEN health >= 50 THEN 'Warning'
                    ELSE 'Critical'
                END
            WHERE id IN ({','.join(id_list)})
        """
        
        self.session.execute(text(stmt))
        self.session.commit()
```

## backend/database/repositories/incident_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/incident_repo.py`

```python
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
```

## backend/database/repositories/knowledge_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/knowledge_repo.py`

```python
from database.models import KnowledgeDB

class KnowledgeRepository:

    def __init__(self, session):
        self.session = session

    def create(self, knowledge):
        self.session.add(knowledge)
        self.session.commit()
        self.session.refresh(knowledge)
        return knowledge

    def create_many(self, documents):
        self.session.add_all(documents)
        self.session.commit()
        return documents

    def similarity_search(self, embedding, limit=5):
        results = (
            self.session
            .query(KnowledgeDB)
            .order_by(
                KnowledgeDB.embedding.cosine_distance(embedding)
            )
            .limit(limit)
            .all()
        )
        return results

    def get_all(self):
        """Return all knowledge chunks from the database."""
        return self.session.query(KnowledgeDB).all()

    def delete_all(self):
        """Delete all knowledge chunks from the database."""
        try:
            deleted = self.session.query(KnowledgeDB).delete()
            self.session.commit()
            return deleted
        except Exception:
            self.session.rollback()
            raise
```

## backend/database/repositories/report_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/report_repo.py`

```python
from database.models import ExecutionReportDB


class ReportRepository:

    def __init__(self, session):
        self.session = session

    def create(self, report):
        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return report

    def get_recent(self, limit=100):
        return (
            self.session.query(ExecutionReportDB)
            .order_by(ExecutionReportDB.completed_at.desc())
            .limit(limit)
            .all()
        )
```

## backend/database/repositories/telemetry_repo.py

**Folder path:** `backend/database/repositories`

**File path:** `backend/database/repositories/telemetry_repo.py`

```python
from database.models import TelemetryDB


class TelemetryRepository:


    def __init__(self, session):

        self.session = session



    def create(self, telemetry):

        self.session.add(telemetry)

        self.session.commit()

        return telemetry



    def create_many(self, readings):
        """Create many telemetry readings in smaller batches."""
        if not readings:
            return
        
        # ✅ Split into smaller batches to avoid connection issues
        batch_size = 50
        for i in range(0, len(readings), batch_size):
            batch = readings[i:i + batch_size]
            self.session.add_all(batch)
            try:
                self.session.commit()
            except Exception:
                self.session.rollback()
                raise
        
        return readings



    def get_asset_history(
        self,
        asset_id,
        limit=100
    ):

        return (
            self.session
            .query(TelemetryDB)
            .filter(
                TelemetryDB.asset_id == asset_id
            )
            .order_by(
                TelemetryDB.timestamp.desc()
            )
            .limit(limit)
            .all()
        )
```

## backend/database/seed_demo.py

**Folder path:** `backend/database`

**File path:** `backend/database/seed_demo.py`

```python

```

## backend/fix_imports.py

**Folder path:** `backend`

**File path:** `backend/fix_imports.py`

```python
"""Fix import paths in adapters."""

import os
import re
from pathlib import Path

# ✅ Use absolute path
ADAPTERS_DIR = Path(__file__).resolve().parent / "api" / "adapters"

print(f"📁 Looking for adapters in: {ADAPTERS_DIR}")

if not ADAPTERS_DIR.exists():
    print(f"❌ Directory not found: {ADAPTERS_DIR}")
    print("Creating directory...")
    ADAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {ADAPTERS_DIR}")
    print("⚠️ Copy adapter files from original project first!")
    exit()

# Map of old imports to new imports
import_map = {
    "from services.runtime import kernel": "from services.runtime import runtime",
    "from services.runtime import simulator": "from services.runtime import runtime",
    "from services.runtime import get_kernel": "from services.runtime import runtime",
    "from app.frontend_services": "from api.adapters",
}

files_fixed = 0
files_skipped = 0

for filename in os.listdir(ADAPTERS_DIR):
    if not filename.endswith('.py'):
        continue
    
    filepath = ADAPTERS_DIR / filename
    modified = False
    
    try:
        # ✅ Use utf-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # ✅ Fallback to latin-1 if utf-8 fails
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️ Could not read {filename}: {e}")
            continue
    
    # Replace imports
    for old, new in import_map.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    # Also fix: from services.runtime import kernel → from services.runtime import runtime
    if "from services.runtime import kernel" in content:
        content = content.replace("from services.runtime import kernel", "from services.runtime import runtime")
        modified = True
    
    # Fix: kernel. → runtime.kernel.
    if "kernel." in content and "runtime.kernel" not in content:
        # Only replace if kernel is imported from runtime
        if "from services.runtime import runtime" in content:
            content = content.replace("kernel.", "runtime.kernel.")
            modified = True
    
    if modified:
        # ✅ Write with utf-8 encoding
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {filename}")
        files_fixed += 1
    else:
        print(f"⏭️ Skipped: {filename}")
        files_skipped += 1

print(f"\n📊 Summary: {files_fixed} files fixed, {files_skipped} files skipped")
```

## backend/mao/__init__.py

**Folder path:** `backend/mao`

**File path:** `backend/mao/__init__.py`

```python
from .kernel import MAOKernel

__all__ = [
    "MAOKernel",
]
```

## backend/mao/core/context.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/context.py`

```python
from datetime import datetime
from uuid import uuid4
from typing import Any, Dict, List, Optional


class ExecutionContext:

    def __init__(
        self,
        event,
        state_manager,
        memory_manager,
        logger,
        health_service=None,
    ):

        # Unique execution information
        self.execution_id = str(uuid4())
        self.started_at = datetime.now()

        # Event information
        self.event = event
        self.workflow = None

        # Shared services
        self.state = state_manager
        self.memory = memory_manager
        self.logger = logger
        self.health_service = health_service

        # Agent execution
        self.results: List[Any] = []
        self.last_result: Optional[Any] = None

        # Shared knowledge between agents
        self.shared_evidence: List[str] = []
        self.shared_recommendations: List[str] = []

        # Incident state
        self.incident_level: Optional[str] = None
        self.requires_shutdown: bool = False
        self.requires_human_approval: bool = False

        # Runtime metrics
        self.execution_metrics: Dict[str, Any] = {
            "agents_executed": 0,
            "successful_agents": 0,
            "failed_agents": 0,
            "average_confidence": 0.0,
        }

        # Flexible storage for workflows/agents
        self.metadata: Dict[str, Any] = {}

    def add_result(self, result):
        """
        Register an agent result and update execution state.
        """

        self.results.append(result)
        self.last_result = result

        if result.evidence:
            self.shared_evidence.extend(result.evidence)

        if result.recommendations:
            self.shared_recommendations.extend(result.recommendations)

        self.execution_metrics["agents_executed"] += 1

        if result.success:
            self.execution_metrics["successful_agents"] += 1
        else:
            self.execution_metrics["failed_agents"] += 1

        if result.requires_human_approval:
            self.requires_human_approval = True

        if self.results:
            total = sum(r.confidence for r in self.results)
            self.execution_metrics["average_confidence"] = round(
                total / len(self.results),
                2,
            )
```

## backend/mao/core/exceptions.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/exceptions.py`

```python
class MAOException(Exception):
    """Base exception for the MAO Kernel."""


class AgentNotFound(MAOException):
    pass


class WorkflowNotFound(MAOException):
    pass


class ToolNotFound(MAOException):
    pass


class PolicyViolation(MAOException):
    pass


class TaskExecutionFailed(MAOException):
    pass
```

## backend/mao/core/executor.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/executor.py`

```python
"""Optimized executor with parallel processing and timeout."""

import concurrent.futures
import time
from typing import Optional
from mao.models.result import AgentResult
from mao.core.exceptions import AgentNotFound


class Executor:
    def __init__(self, registry, max_workers: int = 4, timeout: int = 30):
        self.registry = registry
        self.max_workers = max_workers
        self.timeout = timeout
        self.execution_stats = {}

    def execute(self, task, context):
        agent = self.registry.get(task.assigned_agent)

        if agent is None:
            raise AgentNotFound(f"Agent '{task.assigned_agent}' not found.")

        start = time.time()
        
        try:
            # Execute with timeout
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(agent.run, task, context)
                try:
                    result = future.result(timeout=self.timeout)
                except concurrent.futures.TimeoutError:
                    raise TimeoutError(f"Agent {agent.name} exceeded {self.timeout}s timeout")

            elapsed = time.time() - start
            
            # Track stats
            self.execution_stats[agent.name] = {
                "last_execution": elapsed,
                "total_executions": self.execution_stats.get(agent.name, {}).get("total_executions", 0) + 1,
                "avg_time": 0
            }
            
            stats = self.execution_stats[agent.name]
            total = stats["total_executions"]
            avg = (stats.get("avg_time", 0) * (total - 1) + elapsed) / total
            stats["avg_time"] = round(avg, 2)

        except Exception as e:
            elapsed = time.time() - start
            result = AgentResult(
                agent_name=agent.name,
                success=False,
                finding="Agent execution failed.",
                confidence=0.0,
                summary=str(e),
                recommendations=["Review execution logs."],
                metadata={"exception": type(e).__name__, "execution_time": elapsed},
            )

        result.metadata.update({
            "task_name": task.name,
            "task_description": task.description,
            "event_name": context.event.name,
            "asset_id": context.event.source,
            "execution_time": elapsed,
        })

        return result

    def get_stats(self):
        """Get execution statistics for all agents."""
        return self.execution_stats
```

## backend/mao/core/logger.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/logger.py`

```python
from datetime import datetime


class KernelLogger:

    def __init__(self):

        self.logs = []

    def info(self, source, message):

        self.logs.append(
            {
                "time": datetime.now(),

                "source": source,

                "message": message,
            }
        )

        print(f"[{source}] {message}")
```

## backend/mao/core/registry.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/registry.py`

```python
from typing import Dict


class AgentRegistry:
    """
    Stores every registered agent.
    """

    def __init__(self):

        self._agents: Dict[str, object] = {}

    def register(self, agent):

        self._agents[agent.name] = agent

    def get(self, name):

        return self._agents.get(name)

    def remove(self, name):

        self._agents.pop(name, None)

    def all(self):

        return list(self._agents.values())

    def exists(self, name):

        return name in self._agents
```

## backend/mao/core/scheduler.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/scheduler.py`

```python
import heapq

from itertools import count


class Scheduler:

    def __init__(self):

        self._queue = []

        self._counter = count()

    def submit(self, task):

        heapq.heappush(
            self._queue,

            (task.priority,

             next(self._counter),

             task)
        )

    def next(self):

        if not self._queue:

            return None

        return heapq.heappop(self._queue)[2]

    def empty(self):

        return len(self._queue) == 0
```

## backend/mao/core/state_manager.py

**Folder path:** `backend/mao/core`

**File path:** `backend/mao/core/state_manager.py`

```python
from collections import defaultdict


class StateManager:

    def __init__(self):

        # Assets
        self.assets = {}

        # Last 100 telemetry readings per asset
        self.telemetry = defaultdict(list)

        # Events
        self.events = []

        # Reports
        self.execution_reports = []

        # Agent Results
        self.agent_results = []

        # Workflow Tasks
        self.tasks = []

        # Runtime Notifications
        self.notifications = []

        # Memory
        self.memory = []


    # -------------------------
    # Assets
    # -------------------------

    def add_asset(self, asset):

        self.assets[asset.id] = asset


    def get_asset(self, asset_id):

        return self.assets.get(asset_id)



    # -------------------------
    # Telemetry
    # -------------------------

    def add_telemetry(self, readings):

        for reading in readings:

            history = self.telemetry[reading.asset_id]

            history.append(reading)

            if len(history) > 100:

                history.pop(0)



    def get_history(self, asset_id):

        return self.telemetry.get(asset_id, [])



    # -------------------------
    # Events
    # -------------------------

    def add_event(self, event):

        self.events.append(event)



    # -------------------------
    # Reports
    # -------------------------

    def add_report(self, report):

        self.execution_reports.append(report)



    # -------------------------
    # Agent Results
    # -------------------------

    def add_agent_result(self, result):

        self.agent_results.append(result)



    # -------------------------
    # Tasks
    # -------------------------

    def add_task(self, task):

        self.tasks.append(task)


    def get_tasks(self):

        return self.tasks


    def clear_tasks(self):

        self.tasks.clear()


    # -------------------------
    # Notifications
    # -------------------------

    def add_notification(self, notification):

        self.notifications.append(notification)

        if len(self.notifications) > 200:

            self.notifications.pop(0)


    def get_notifications(self):

        return self.notifications



    # -------------------------
    # Memory
    # -------------------------

    def add_memory(self, item):

        self.memory.append(item)


    def get_memory(self):

        return self.memory
```

## backend/mao/events/event_bus.py

**Folder path:** `backend/mao/events`

**File path:** `backend/mao/events/event_bus.py`

```python
from collections import defaultdict


class EventBus:

    def __init__(self):

        self._subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):

        self._subscribers[event_name].append(callback)

    def publish(self, event):

        if event.name not in self._subscribers:
            return

        for callback in self._subscribers[event.name]:

            callback(event)
```

## backend/mao/events/event_store.py

**Folder path:** `backend/mao/events`

**File path:** `backend/mao/events/event_store.py`

```python
class EventStore:

    def __init__(self):

        self.events = []

    def save(self, event):

        self.events.append(event)

    def all(self):

        return self.events
```

## backend/mao/events/event.py

**Folder path:** `backend/mao/events`

**File path:** `backend/mao/events/event.py`

```python
from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    source: str

    payload: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=datetime.now)
```

## backend/mao/kernel.py

**Folder path:** `backend/mao`

**File path:** `backend/mao/kernel.py`

```python
from mao.core.executor import Executor
from mao.core.logger import KernelLogger
from mao.core.registry import AgentRegistry
from mao.core.scheduler import Scheduler
from mao.core.state_manager import StateManager

from mao.events.event_bus import EventBus
from mao.events.event_store import EventStore

from mao.memory.memory_manager import MemoryManager

from mao.orchestrator import Orchestrator

from mao.workflows.planner import Planner
from mao.workflows.supervisor import Supervisor
from mao.workflows.workflow_engine import WorkflowEngine

from services.asset import AssetService
from services.health import HealthService
from services.persistence import PersistenceService



class MAOKernel:

    def __init__(self):

        # Core

        self.registry = AgentRegistry()

        self.scheduler = Scheduler()

        self.state = StateManager()

        self.logger = KernelLogger()

        self.memory = MemoryManager()



        # Services

        self.asset_service = AssetService()

        self.health = HealthService()

        self.persistence = PersistenceService()



        # Events

        self.event_bus = EventBus()

        self.event_store = EventStore()



        # Workflow

        self.planner = Planner()

        self.workflow_engine = WorkflowEngine()

        self.supervisor = Supervisor()



        # Executor

        self.executor = Executor(
            self.registry
        )



        # Orchestrator

        self.orchestrator = Orchestrator(

            planner=self.planner,

            workflow_engine=self.workflow_engine,

            scheduler=self.scheduler,

            executor=self.executor,

            supervisor=self.supervisor,

            state_manager=self.state,

            memory_manager=self.memory,

            logger=self.logger,

            event_store=self.event_store,

            health_service=self.health,

        )



    def register_agent(self, agent):

        self.registry.register(agent)



    def register_workflow(self, workflow):

        self.workflow_engine.register(workflow)



    def handle_event(self, event):

        # Run MAO pipeline

        report = self.orchestrator.run(event)



        # Store report




        # Store agent outputs

        for result in report.agent_results:

            self.state.add_agent_result(result)

        self.persistence.record_execution(event, report)



        return report
```

## backend/mao/memory/memory_manager.py

**Folder path:** `backend/mao/memory`

**File path:** `backend/mao/memory/memory_manager.py`

```python

from typing import Any


class MemoryManager:

    def __init__(self):

        self.execution_reports = []

        self.agent_results = []

        self.events = []


    # -------------------------

    def remember_report(self, report):

        self.execution_reports.append(report)



    # -------------------------

    def remember_result(self, result):

        self.agent_results.append(result)



    # -------------------------

    def remember_event(self, event):

        self.events.append(event)



    # -------------------------

    def latest_report(self):

        if not self.execution_reports:

            return None


        return self.execution_reports[-1]
```

## backend/mao/models/execution_report.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/execution_report.py`

```python
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from mao.models.result import AgentResult


class ExecutionReport(BaseModel):

    # Report identifiers
    id: str = Field(default_factory=lambda: str(uuid4()))
    execution_id: str

    # Workflow information
    workflow_name: str
    success: bool

    # Timing
    started_at: datetime
    completed_at: datetime

    # Agent outputs
    agent_results: list[AgentResult]

    # Final decision
    final_summary: str
    recommendations: list[str] = Field(default_factory=list)

    # Execution metrics
    total_agents: int = 0
    successful_agents: int = 0
    failed_agents: int = 0
    average_confidence: float = 0.0

    # Approval & Incident
    approval_required: bool = False
    incident_severity: str = "Unknown"

    # Optional metadata
    metadata: dict = Field(default_factory=dict)
```

## backend/mao/models/notification.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/notification.py`

```python
"""Runtime-only notification model for MAO workflow outputs."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Notification:
    """A structured operator notification held in StateManager memory."""

    source: str
    severity: str
    summary: str
    asset_id: str | None = None
    requires_human_approval: bool = False
    metadata: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
```

## backend/mao/models/result.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/result.py`

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4


@dataclass
class AgentResult:

    agent_name: str

    success: bool

    id: str = field(default_factory=lambda: str(uuid4()))

    finding: str = ""

    confidence: float = 0.0

    evidence: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    required_action: str = ""

    requires_human_approval: bool = True

    metadata: Dict = field(default_factory=dict)

    summary: str = ""

    decision: str = ""

    actions_required: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.now)
```

## backend/mao/models/task.py

**Folder path:** `backend/mao/models`

**File path:** `backend/mao/models/task.py`

```python
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    description: str

    assigned_agent: str

    priority: int = 1

    status: TaskStatus = TaskStatus.PENDING

    input_data: dict = Field(default_factory=dict)

    output_data: dict = Field(default_factory=dict)
```

## backend/mao/orchestrator.py

**Folder path:** `backend/mao`

**File path:** `backend/mao/orchestrator.py`

```python
"""Optimized Orchestrator with parallel agent execution."""

import concurrent.futures
import time
from datetime import datetime
from mao.core.context import ExecutionContext
from mao.models.execution_report import ExecutionReport


class Orchestrator:
    def __init__(
        self,
        *,
        planner,
        workflow_engine,
        scheduler,
        executor,
        supervisor,
        state_manager,
        memory_manager,
        logger,
        event_store,
        health_service=None,
    ):
        self.planner = planner
        self.workflow_engine = workflow_engine        
        self.scheduler = scheduler
        self.executor = executor
        self.supervisor = supervisor

        self.state = state_manager
        self.memory = memory_manager
        self.logger = logger
        self.event_store = event_store
        self.health_service = health_service

    def run(self, event):
        context = ExecutionContext(
            event=event,
            state_manager=self.state,
            memory_manager=self.memory,
            logger=self.logger,
            health_service=self.health_service,
        )

        self.logger.info("Kernel", f"[{context.execution_id}] Received event '{event.name}'")

        self.state.add_event(event)
        self.event_store.save(event)

        workflow_name = self.planner.choose_workflow(event)
        context.workflow = workflow_name

        self.logger.info("Planner", f"[{context.execution_id}] Selected workflow '{workflow_name}'")

        tasks = self.workflow_engine.create_tasks(workflow_name, event)

        self.logger.info("WorkflowEngine", f"[{context.execution_id}] Generated {len(tasks)} task(s)")

        # Schedule tasks
        for task in tasks:
            self.scheduler.submit(task)

        # ✅ Execute tasks in parallel
        def execute_task(task):
            result = self.executor.execute(task, context)
            context.add_result(result)
            self.state.add_task(task)
            return result

        start = time.time()
        
        # Extract all tasks first
        all_tasks = []
        while not self.scheduler.empty():
            all_tasks.append(self.scheduler.next())
        
        # Execute in parallel with ThreadPoolExecutor
        if all_tasks:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(execute_task, task): task for task in all_tasks}
                
                for future in concurrent.futures.as_completed(futures):
                    task = futures[future]
                    try:
                        result = future.result(timeout=30)
                    except Exception as e:
                        self.logger.info("Executor", f"Task {task.name} failed: {e}")

        elapsed = time.time() - start
        self.logger.info("Executor", f"[{context.execution_id}] All agents completed in {elapsed:.2f}s")

        # Aggregate results
        decision = self.supervisor.summarize(context)

        report = ExecutionReport(
            execution_id=context.execution_id,
            workflow_name=workflow_name,
            success=decision["success"],
            started_at=context.started_at,
            completed_at=datetime.now(),
            agent_results=context.results,
            final_summary=decision["summary"],
            recommendations=decision["recommendations"],
            total_agents=context.execution_metrics["agents_executed"],
            successful_agents=context.execution_metrics["successful_agents"],
            failed_agents=context.execution_metrics["failed_agents"],
            average_confidence=context.execution_metrics["average_confidence"],
            approval_required=context.requires_human_approval,
            incident_severity=context.incident_level or "Unknown",
            metadata=context.metadata,
        )

        self.state.add_report(report)
        self.memory.remember_event(event)
        self.memory.remember_report(report)

        for result in report.agent_results:
            self.memory.remember_result(result)

        return report
```

## backend/mao/tools/tool_registry.py

**Folder path:** `backend/mao/tools`

**File path:** `backend/mao/tools/tool_registry.py`

```python

```

## backend/mao/workflows/flow_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/flow_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class FlowWorkflow(Workflow):

    name = "flow_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Assess risks caused by restricted flow.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Flow Diagnosis",
                description="Determine the cause of flow restriction.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve flow restriction operating procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for restricted flow.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a flow recovery procedure.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## backend/mao/workflows/gas_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/gas_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class GasWorkflow(Workflow):

    name = "gas_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Assess gas leak hazards.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Gas Leak Diagnosis",
                description="Identify the source of the gas leak.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve gas leak emergency procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend repair actions for the gas leak.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a gas leak recovery plan.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## backend/mao/workflows/intelligence_tasks.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/intelligence_tasks.py`

```python
"""Reusable intelligence stages appended to established operational workflows."""

from mao.models.task import Task


def intelligence_tasks() -> tuple[Task, Task, Task, Task]:
    """Return the common MAO intelligence stages with stable priorities."""
    return (
        Task(
            name="Sensor Observation",
            description="Record telemetry anomaly metadata without generating events.",
            assigned_agent="sensor",
            priority=1,
        ),
        Task(
            name="Failure Risk Prediction",
            description="Estimate deterministic health, failure probability, and RUL.",
            assigned_agent="prediction",
            priority=7,
        ),
        Task(
            name="Operator Notification",
            description="Create structured runtime notifications when escalation is needed.",
            assigned_agent="notification",
            priority=8,
        ),
        Task(
            name="Report Compilation",
            description="Compile agent outputs for the existing execution report.",
            assigned_agent="report",
            priority=9,
        ),
    )
```

## backend/mao/workflows/maintenance_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/maintenance_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class MaintenanceWorkflow(Workflow):

    name = "maintenance_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Verify equipment is safe before maintenance.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Equipment Diagnosis",
                description="Analyze equipment condition.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve Manual",
                description="Retrieve maintenance manuals and procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Planning",
                description="Generate maintenance recommendations.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Execution Plan",
                description="Create the maintenance execution plan.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## backend/mao/workflows/planner.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/planner.py`

```python
"""
mao/workflows/planner.py

Workflow Planner

Determines which workflow should execute based on the
incoming event and telemetry payload.

Supports both:
    • Explicit event names
    • Automatic telemetry-based routing
"""

from __future__ import annotations

from typing import Any


class Planner:
    """
    Selects the most appropriate workflow for an incoming event.
    """

    EVENT_MAP = {
        "PressureSpike": "pressure_response",
        "HighTemperature": "temperature_response",
        "GasLeak": "gas_response",
        "HighVibration": "maintenance_response",
        "FlowRestriction": "flow_response",
    }

    def choose_workflow(self, event: Any) -> str:
        """
        Determine which workflow should handle an event.

        Priority:
            1. Telemetry inspection
            2. Event-name lookup
            3. Default workflow
        """

        payload = getattr(event, "payload", {}) or {}

        workflow = self._workflow_from_payload(payload)

        if workflow is not None:
            return workflow

        return self.EVENT_MAP.get(
            getattr(event, "name", ""),
            "default",
        )

    def _workflow_from_payload(
        self,
        payload: dict,
    ) -> str | None:
        """
        Infer workflow directly from telemetry.
        """

        pressure = payload.get("pressure")
        temperature = payload.get("temperature")
        gas = payload.get("gas_level")
        vibration = payload.get("vibration")
        flow = payload.get("flow_rate")

        if pressure is not None and pressure >= 150:
            return "pressure_response"

        if temperature is not None and temperature >= 85:
            return "temperature_response"

        if gas is not None and gas >= 40:
            return "gas_response"

        if vibration is not None and vibration >= 8:
            return "maintenance_response"

        if flow is not None and flow <= 25:
            return "flow_response"

        return None
```

## backend/mao/workflows/policy_engine.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/policy_engine.py`

```python

```

## backend/mao/workflows/pressure_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/pressure_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class PressureWorkflow(Workflow):

    name = "pressure_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Analyze safety impact of the pressure spike.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Root Cause Analysis",
                description="Determine the likely cause of the pressure spike.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve the pressure spike operating procedure.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for the affected equipment.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Generate the recovery and restart plan.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## backend/mao/workflows/supervisor.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/supervisor.py`

```python
from collections import OrderedDict

from mao.core.context import ExecutionContext


class Supervisor:
    """
    Aggregates all agent outputs into a final execution decision.
    """

    def summarize(self, context: ExecutionContext) -> dict:

        results = context.results

        if not results:
            return {
                "success": True,
                "confidence": 0.0,
                "summary": "No agents were executed.",
                "recommendations": [],
                "severity": "Unknown",
            }

        # Overall success
        success = all(result.success for result in results)

        # Average confidence
        confidence = round(
            sum(result.confidence for result in results)
            / len(results),
            2,
        )

        # Remove duplicate recommendations
        recommendations = list(
            OrderedDict.fromkeys(
                rec
                for result in results
                for rec in result.recommendations
            )
        )

        # Collect findings
        findings = [
            f"[{result.agent_name}] {result.finding}"
            for result in results
            if result.finding
        ]

        # Collect summaries
        summaries = [
            f"[{result.agent_name}] {result.summary}"
            for result in results
            if result.summary
        ]

        # Determine overall severity
        severity = "Low"

        if confidence >= 0.90:
            severity = "Critical"
        elif confidence >= 0.75:
            severity = "High"
        elif confidence >= 0.50:
            severity = "Medium"

        context.incident_level = severity

        # Human approval
        approval_required = any(
            result.requires_human_approval
            for result in results
        )

        context.requires_human_approval = approval_required

        # Store metadata
        context.metadata["confidence"] = confidence
        context.metadata["severity"] = severity
        context.metadata["approval_required"] = approval_required

        # Executive summary
        summary_parts = []

        if findings:
            summary_parts.append("Key Findings")
            summary_parts.extend(findings)

        if summaries:
            summary_parts.append("")
            summary_parts.append("Agent Analysis")
            summary_parts.extend(summaries)

        summary = "\n".join(summary_parts)

        return {
            "success": success,
            "confidence": confidence,
            "summary": summary,
            "recommendations": recommendations,
            "severity": severity,
        }
```

## backend/mao/workflows/temperature_workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/temperature_workflow.py`

```python
from mao.workflows.workflow import Workflow
from mao.workflows.intelligence_tasks import intelligence_tasks
from mao.models.task import Task


class TemperatureWorkflow(Workflow):

    name = "temperature_response"

    def build(self, event):

        intelligence = intelligence_tasks()

        return [

            intelligence[0],

            Task(
                name="Safety Check",
                description="Evaluate overheating risks.",
                assigned_agent="safety",
                priority=2,
            ),

            Task(
                name="Temperature Diagnosis",
                description="Determine the cause of abnormal temperature.",
                assigned_agent="diagnostic",
                priority=3,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve overheating operating procedures.",
                assigned_agent="knowledge",
                priority=4,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for overheating equipment.",
                assigned_agent="maintenance",
                priority=5,
            ),

            Task(
                name="Recovery Plan",
                description="Create a safe recovery procedure.",
                assigned_agent="planning",
                priority=6,
            ),

            *intelligence[1:],
        ]
```

## backend/mao/workflows/workflow_engine.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/workflow_engine.py`

```python
from mao.workflows.workflow import Workflow


class WorkflowEngine:

    def __init__(self):

        self._workflows: dict[str, Workflow] = {}

    def register(self, workflow: Workflow):

        self._workflows[workflow.name] = workflow

    def get(self, name: str):

        return self._workflows.get(name)

    def exists(self, name):

        return name in self._workflows

    def create_tasks(self, workflow_name, event):

        workflow = self.get(workflow_name)

        if workflow is None:

            raise ValueError(
                f"Workflow '{workflow_name}' not found."
            )

        return workflow.build(event)
```

## backend/mao/workflows/workflow.py

**Folder path:** `backend/mao/workflows`

**File path:** `backend/mao/workflows/workflow.py`

```python
from abc import ABC, abstractmethod

from mao.events.event import Event
from mao.models.task import Task


class Workflow(ABC):
    """
    Base class for all workflows.
    """

    name: str = "workflow"

    @abstractmethod
    def build(self, event: Event) -> list[Task]:
        """
        Convert an event into executable tasks.
        """
        raise NotImplementedError
```

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

## backend/rag/__init__.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/__init__.py`

```python

```

## backend/rag/chunker.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/chunker.py`

```python

```

## backend/rag/citation.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/citation.py`

```python

```

## backend/rag/embedder.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/embedder.py`

```python
"""Gemini Embedding Manager for RigOS."""

from __future__ import annotations

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ✅ Correct import
from services.llm import _has_invalid_gemini_proxy

logger = logging.getLogger(__name__)

load_dotenv()


class Embedder:
    """Singleton wrapper around Google's Gemini embedding model."""

    _model: Optional[GoogleGenerativeAIEmbeddings] = None

    # ✅ Fixed: Removed duplicates, supports up to 7 keys
    API_KEY_ENVIRONMENTS = (
        "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3",
        "GOOGLE_API_KEY_4", "GOOGLE_API_KEY_5", "GOOGLE_API_KEY_6",
        "GOOGLE_API_KEY_7",
        "GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3",
        "GEMINI_API_KEY_4", "GEMINI_API_KEY_5", "GEMINI_API_KEY_6",
        "GEMINI_API_KEY_7",
        "GOOGLE_API_KEY", "GEMINI_API_KEY",
    )

    def __init__(self):
        if Embedder._model is None:
            self._initialize()

    def _initialize(self) -> None:
        """Initialize Gemini embeddings once."""
        api_key = None
        selected_variable = None

        for variable in self.API_KEY_ENVIRONMENTS:
            value = os.getenv(variable)
            if value:
                api_key = value
                selected_variable = variable
                break

        if api_key is None:
            raise RuntimeError(
                "No Gemini API key found.\n\n"
                "Expected one of:\n"
                + "\n".join(f" - {v}" for v in self.API_KEY_ENVIRONMENTS)
            )

        logger.info("Initializing Gemini embeddings using %s", selected_variable)

        Embedder._model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key,
            client_args={"trust_env": False} if _has_invalid_gemini_proxy() else None,
        )

        logger.info("Gemini embeddings initialized successfully.")

    def get_model(self) -> GoogleGenerativeAIEmbeddings:
        """Return the embedding model."""
        if Embedder._model is None:
            self._initialize()
        return Embedder._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple documents."""
        return self.get_model().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query."""
        return self.get_model().embed_query(text)

    def __repr__(self) -> str:
        return "Embedder(model='models/gemini-embedding-001', dimensions=3072)"
```

## backend/rag/ingestion.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/ingestion.py`

```python
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embedder import Embedder
from rag.neon_vector_store import NeonVectorStore



class KnowledgeIngestion:


    def __init__(self):

        embedder = Embedder()

        self.vector_store = NeonVectorStore(
            embedder.get_model()
        )



    def ingest_folder(self, folder):

        documents = []


        for file in Path(folder).rglob("*.pdf"):

            print(
                f"Loading: {file}"
            )

            loader = PyPDFLoader(
                str(file)
            )

            docs = loader.load()

            documents.extend(docs)



        if not documents:

            raise RuntimeError(
                "No PDF documents found in docs/"
            )



        splitter = RecursiveCharacterTextSplitter(

            chunk_size=800,

            chunk_overlap=100

        )


        chunks = splitter.split_documents(
            documents
        )


        print(
            f"Created {len(chunks)} chunks"
        )



        self.vector_store.create(
            chunks
        )


        print(
            "Stored embeddings in Neon pgvector"
        )


        return len(chunks)
```

## backend/rag/knowledge.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/knowledge.py`

```python

```

## backend/rag/llm_manager.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/llm_manager.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

__all__ = ["LLMManager"]
```

## backend/rag/llm.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/llm.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

CloudLLM = LLMManager

__all__ = ["CloudLLM", "LLMManager"]
```

## backend/rag/loader.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/loader.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:


    def load(self, path):

        loader = PyPDFLoader(path)

        documents = loader.load()

        return documents
```

## backend/rag/neon_vector_store.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/neon_vector_store.py`

```python
from sqlalchemy import text
from langchain_core.documents import Document

from database.connection import get_session
from database.models import KnowledgeDB
from uuid import uuid4


class NeonVectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self._db = None

    def create(self, documents):
        """Create the vector store from a list of documents."""
        session = get_session()
        try:
            for doc in documents:
                vector = self.embeddings.embed_query(doc.page_content)
                row = KnowledgeDB(
                    id=str(uuid4()),
                    content=doc.page_content,
                    source=doc.metadata.get("source", "unknown"),
                    embedding=vector
                )
                session.add(row)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add_documents(self, documents):
        """Add documents to an existing vector store."""
        session = get_session()
        try:
            for doc in documents:
                vector = self.embeddings.embed_query(doc.page_content)
                row = KnowledgeDB(
                    id=str(uuid4()),
                    content=doc.page_content,
                    source=doc.metadata.get("source", "unknown"),
                    embedding=vector
                )
                session.add(row)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def clear(self):
        """Remove all indexed chunks."""
        session = get_session()
        try:
            deleted = session.query(KnowledgeDB).delete()
            session.commit()
            return deleted
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def count(self):
        """Return the number of searchable chunks."""
        session = get_session()
        try:
            return session.query(KnowledgeDB).count()
        finally:
            session.close()

    def similarity_search(self, query, k=5):
        """Search by query string."""
        session = get_session()
        try:
            vector = self.embeddings.embed_query(query)

            results = session.execute(
                text("""
                    SELECT content, source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                """),
                {"vector": str(vector), "limit": k}
            )

            documents = []
            for row in results:
                documents.append(
                    Document(
                        page_content=row.content,
                        metadata={"source": row.source},
                    )
                )
            return documents
        finally:
            session.close()

    def similarity_search_by_vector(self, embedding, k=5):
        """Search by embedding vector."""
        session = get_session()
        try:
            results = session.execute(
                text("""
                    SELECT content, source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                """),
                {"vector": str(embedding), "limit": k}
            )

            documents = []
            for row in results:
                documents.append(
                    Document(
                        page_content=row.content,
                        metadata={"source": row.source},
                    )
                )
            return documents
        finally:
            session.close()

    def get(self):
        """Return self for compatibility."""
        return self

    def as_retriever(self, search_kwargs=None):
        """Return a retriever interface."""
        from rag.retriever import Retriever
        return Retriever(self)
```

## backend/rag/parser.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/parser.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    def load(self, path):

        loader = PyPDFLoader(path)

        return loader.load()
```

## backend/rag/pipeline.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/pipeline.py`

```python
from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.embedder import Embedder
from rag.vector_store import VectorStore


from pathlib import Path
from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.embedder import Embedder
from rag.vector_store import VectorStore

# Default path for FAISS index
DEFAULT_INDEX_PATH = "./data/faiss_index"


class RAGPipeline:

    def build(self, pdfs, index_path=DEFAULT_INDEX_PATH):
        """Build a FAISS vector store from PDF files."""
        loader = DocumentLoader()
        splitter = DocumentSplitter()
        embedder = Embedder()

        docs = []
        for pdf in pdfs:
            docs.extend(loader.load(pdf))

        chunks = splitter.split(docs)
        
        # ✅ FIXED: Use create() instead of build()
        store = VectorStore(embedder)
        store.create(chunks)
        
        # ✅ FIXED: Pass path to save()
        store.save(index_path)

        return store
```

## backend/rag/reranker.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/reranker.py`

```python

```

## backend/rag/retriever.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/retriever.py`

```python
class Retriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store


    def retrieve(self, query):
        if hasattr(self.vector_store, "similarity_search"):
            return self.vector_store.similarity_search(query)

        db = self.vector_store.get()
        if db is None:
            return []
        return db.similarity_search(query)
```

## backend/rag/splitter.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/splitter.py`

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=800,

            chunk_overlap=150,

        )

    def split(self, docs):

        return self.splitter.split_documents(docs)
```

## backend/rag/vector_store.py

**Folder path:** `backend/rag`

**File path:** `backend/rag/vector_store.py`

```python
import faiss

from langchain_community.vectorstores import FAISS


class VectorStore:


    def __init__(self, embeddings):

        self.embeddings = embeddings

        self.db = None



    def create(self, documents):

        self.db = FAISS.from_documents(

            documents,

            self.embeddings

        )



    def save(self, path):

        self.db.save_local(path)



    def load(self, path):

        self.db = FAISS.load_local(

            path,

            self.embeddings,

            allow_dangerous_deserialization=True

        )


    def get(self):

        return self.db
```

## backend/requirements.txt

**Folder path:** `backend`

**File path:** `backend/requirements.txt`

```
# UI
streamlit
# API
fastapi
uvicorn
# Database
sqlalchemy
psycopg2-binary
pgvector
# Environment / config
python-dotenv
# Validation
pydantic
# Logging
loguru
agno
llama-index
# Vector databases
chromadb
# Embeddings
sentence-transformers
# Google Gemini
google-generativeai
langchain-google-genai
# OpenAI fallback
openai
langchain-openai
# LangChain core
langchain
langchain-community
langchain-huggingface
# PDF loading
pypdf
# FAISS vector store
faiss-cpu
# Utilities
uuid64
streamlit
plotly
pandas
python-dotenv
requests
sqlalchemy
psycopg2-binary
pgvector
langchain
langchain-community
langchain-google-genai
sentence-transformers
faiss-cpu
pypdf
# Streamlit UI and domain models
streamlit==1.59.2
pydantic==2.13.4
python-dotenv==1.2.2
# PostgreSQL persistence
SQLAlchemy==2.0.51
alembic==1.18.5
psycopg2-binary==2.9.12
pgvector==0.5.0
# Retrieval-augmented knowledge agent
langchain-community==0.4.2
langchain-google-genai==4.2.7
langchain-huggingface==1.2.2
langchain-text-splitters==1.1.2
sentence-transformers==5.6.0
transformers==5.14.1
torch==2.13.0
faiss-cpu==1.14.3
pypdf==6.14.2
alembic
torchvision
```

## backend/run.py

**Folder path:** `backend`

**File path:** `backend/run.py`

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
```

## backend/services/__init__.py

**Folder path:** `backend/services`

**File path:** `backend/services/__init__.py`

```python
"""Services module exports - NO circular imports."""

# ✅ Lazy imports to avoid circular issues
def get_asset_service():
    from services.asset import AssetService
    return AssetService

def get_health_service():
    from services.health import HealthService
    return HealthService

def get_llm_manager():
    from services.llm import LLMManager
    return LLMManager

def get_persistence_service():
    from services.persistence import PersistenceService
    return PersistenceService

def get_config_service():
    from services.config_services import ConfigService
    return ConfigService

def get_simulator_controller():
    from services.simulator_controller import SimulatorController, sim_controller
    return SimulatorController, sim_controller

def get_runtime():
    from services.runtime import kernel, simulator
    return kernel, simulator

def get_ai_config():
    """Get the AI Configuration Generator (singleton)."""
    from services.ai_config import AIConfigGenerator
    return AIConfigGenerator()

def get_computation_engine():
    """Get the Computation Engine (singleton)."""
    from services.computation_engine import ComputationEngine
    return ComputationEngine()


# ✅ Direct imports (safe ones - no circular issues)
from services.asset import AssetService
from services.health import HealthService
from services.llm import LLMManager
from services.persistence import PersistenceService
from services.config_services import ConfigService
from services.simulator_controller import SimulatorController, sim_controller
from services.ai_config import AIConfigGenerator
from services.computation_engine import ComputationEngine

# ✅ LAZY LOAD - Don't import kernel/simulator at module level!
# Remove this line that causes circular import:
# from services.runtime import kernel, simulator

__all__ = [
    "AssetService",
    "HealthService",
    "LLMManager",
    "PersistenceService",
    "ConfigService",
    "SimulatorController",
    "sim_controller",
    "AIConfigGenerator",
    "ComputationEngine",
    "get_ai_config",
    "get_computation_engine",
    # "kernel",  # REMOVED - causes circular import
    # "simulator",  # REMOVED - causes circular import
]
```

## backend/services/ai_config.py

**Folder path:** `backend/services`

**File path:** `backend/services/ai_config.py`

```python
"""AI Configuration Generator - Runs once on startup to generate all thresholds and rules."""

import json
import re
import time
from typing import Dict, List, Any
from services.llm import LLMManager


class AIConfigGenerator:
    """Generate all configuration using AI once at startup."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if AIConfigGenerator._config is None:
            self.llm = LLMManager()
            self._generate_all_config()
    
    def _generate_all_config(self):
        """Generate ALL configuration in ONE AI call."""
        print("\n" + "="*60)
        print("🤖 AI CONFIGURATION GENERATOR")
        print("="*60)
        print("Generating all thresholds and rules...")
        
        prompt = self._build_prompt()
        
        try:
            response = self.llm.generate(prompt, use_cache=True)
            config = self._parse_response(response)
            AIConfigGenerator._config = config
            self._save_to_file(config)
            print("✅ AI configuration generated successfully!")
        except Exception as e:
            print(f"⚠️ AI config generation failed: {e}")
            AIConfigGenerator._config = self._get_default_config()
            print("✅ Using default configuration as fallback")
        
        print("="*60 + "\n")
    
    def _build_prompt(self) -> str:
        """Build the comprehensive AI prompt."""
        return """
You are an industrial operations configuration expert. Generate a complete operational configuration for a refinery.

Return ONLY a JSON object with the following structure:

{
    "asset_types": {
        "Pump": {
            "thresholds": {
                "pressure_max": 150,
                "temperature_max": 85,
                "gas_max": 40,
                "vibration_max": 8,
                "flow_min": 25
            },
            "weight": {
                "pressure_weight": 30,
                "temperature_weight": 25,
                "gas_weight": 35,
                "vibration_weight": 20,
                "flow_weight": 10
            },
            "degradation_rate": 0.5,
            "critical_health": 50
        },
        "Compressor": {
            "thresholds": {
                "pressure_max": 160,
                "temperature_max": 90,
                "gas_max": 35,
                "vibration_max": 10,
                "flow_min": 30
            },
            "weight": {
                "pressure_weight": 35,
                "temperature_weight": 20,
                "gas_weight": 25,
                "vibration_weight": 30,
                "flow_weight": 10
            },
            "degradation_rate": 0.6,
            "critical_health": 50
        }
    },
    "workflow_sequences": {
        "pressure_spike": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "gas_leak": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "high_temperature": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "high_vibration": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
        "flow_restriction": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]
    },
    "severity_mapping": {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    },
    "health_status_mapping": {
        "healthy": 80,
        "warning": 50,
        "critical": 30
    },
    "prediction": {
        "confidence_weight": 0.55,
        "sample_weight": 0.02,
        "max_samples": 20,
        "rul_max_days": 365,
        "rul_min_days": 1
    },
    "notification": {
        "critical_failure_threshold": 70,
        "warning_failure_threshold": 40,
        "info_failure_threshold": 0
    }
}

Generate for ALL asset types: Pump, Compressor, Tank, Valve, Pipeline, Heat Exchanger, Reactor, Boiler, Turbine, Motor, Generator, Distillation Column.

Use realistic industrial values. Respond with ONLY valid JSON, no other text.
"""
    
    def _parse_response(self, response: str) -> Dict:
        """Parse JSON from AI response."""
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            return json.loads(json_str)
        raise ValueError("No JSON found in response")
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "asset_types": {
                "Pump": {
                    "thresholds": {"pressure_max": 150, "temperature_max": 85, "gas_max": 40, "vibration_max": 8, "flow_min": 25},
                    "weight": {"pressure_weight": 30, "temperature_weight": 25, "gas_weight": 35, "vibration_weight": 20, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Compressor": {
                    "thresholds": {"pressure_max": 160, "temperature_max": 90, "gas_max": 35, "vibration_max": 10, "flow_min": 30},
                    "weight": {"pressure_weight": 35, "temperature_weight": 20, "gas_weight": 25, "vibration_weight": 30, "flow_weight": 10},
                    "degradation_rate": 0.6,
                    "critical_health": 50
                },
                "Tank": {
                    "thresholds": {"pressure_max": 120, "temperature_max": 80, "gas_max": 45, "vibration_max": 5, "flow_min": 20},
                    "weight": {"pressure_weight": 20, "temperature_weight": 30, "gas_weight": 40, "vibration_weight": 10, "flow_weight": 10},
                    "degradation_rate": 0.3,
                    "critical_health": 50
                },
                "Valve": {
                    "thresholds": {"pressure_max": 140, "temperature_max": 85, "gas_max": 40, "vibration_max": 7, "flow_min": 15},
                    "weight": {"pressure_weight": 25, "temperature_weight": 25, "gas_weight": 30, "vibration_weight": 20, "flow_weight": 15},
                    "degradation_rate": 0.4,
                    "critical_health": 50
                },
                "Pipeline": {
                    "thresholds": {"pressure_max": 130, "temperature_max": 80, "gas_max": 50, "vibration_max": 6, "flow_min": 10},
                    "weight": {"pressure_weight": 30, "temperature_weight": 15, "gas_weight": 45, "vibration_weight": 10, "flow_weight": 10},
                    "degradation_rate": 0.3,
                    "critical_health": 50
                },
                "Heat Exchanger": {
                    "thresholds": {"pressure_max": 145, "temperature_max": 100, "gas_max": 30, "vibration_max": 9, "flow_min": 25},
                    "weight": {"pressure_weight": 20, "temperature_weight": 35, "gas_weight": 20, "vibration_weight": 25, "flow_weight": 15},
                    "degradation_rate": 0.7,
                    "critical_health": 50
                },
                "Reactor": {
                    "thresholds": {"pressure_max": 155, "temperature_max": 95, "gas_max": 35, "vibration_max": 8, "flow_min": 20},
                    "weight": {"pressure_weight": 30, "temperature_weight": 25, "gas_weight": 25, "vibration_weight": 20, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Boiler": {
                    "thresholds": {"pressure_max": 170, "temperature_max": 120, "gas_max": 25, "vibration_max": 10, "flow_min": 30},
                    "weight": {"pressure_weight": 35, "temperature_weight": 30, "gas_weight": 15, "vibration_weight": 20, "flow_weight": 10},
                    "degradation_rate": 0.8,
                    "critical_health": 50
                },
                "Turbine": {
                    "thresholds": {"pressure_max": 140, "temperature_max": 100, "gas_max": 30, "vibration_max": 12, "flow_min": 25},
                    "weight": {"pressure_weight": 25, "temperature_weight": 20, "gas_weight": 20, "vibration_weight": 35, "flow_weight": 10},
                    "degradation_rate": 0.6,
                    "critical_health": 50
                },
                "Motor": {
                    "thresholds": {"pressure_max": 120, "temperature_max": 95, "gas_max": 30, "vibration_max": 15, "flow_min": 20},
                    "weight": {"pressure_weight": 15, "temperature_weight": 25, "gas_weight": 15, "vibration_weight": 45, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Generator": {
                    "thresholds": {"pressure_max": 130, "temperature_max": 100, "gas_max": 25, "vibration_max": 14, "flow_min": 25},
                    "weight": {"pressure_weight": 20, "temperature_weight": 30, "gas_weight": 15, "vibration_weight": 35, "flow_weight": 10},
                    "degradation_rate": 0.5,
                    "critical_health": 50
                },
                "Distillation Column": {
                    "thresholds": {"pressure_max": 125, "temperature_max": 110, "gas_max": 30, "vibration_max": 7, "flow_min": 15},
                    "weight": {"pressure_weight": 25, "temperature_weight": 35, "gas_weight": 25, "vibration_weight": 15, "flow_weight": 10},
                    "degradation_rate": 0.4,
                    "critical_health": 50
                }
            },
            "workflow_sequences": {
                "pressure_spike": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "gas_leak": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "high_temperature": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "high_vibration": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"],
                "flow_restriction": ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]
            },
            "severity_mapping": {"Critical": 1, "High": 2, "Medium": 3, "Low": 4},
            "health_status_mapping": {"healthy": 80, "warning": 50, "critical": 30},
            "prediction": {"confidence_weight": 0.55, "sample_weight": 0.02, "max_samples": 20, "rul_max_days": 365, "rul_min_days": 1},
            "notification": {"critical_failure_threshold": 70, "warning_failure_threshold": 40, "info_failure_threshold": 0}
        }
    
    def _save_to_file(self, config: Dict):
        """Save config to file for cache."""
        try:
            import json
            from pathlib import Path
            config_path = Path(__file__).resolve().parents[1] / "data" / "ai_config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Config saved to {config_path}")
        except Exception as e:
            print(f"⚠️ Could not save config: {e}")
    
    def get_config(self) -> Dict:
        """Get the generated configuration."""
        return AIConfigGenerator._config or self._get_default_config()
    
    def get_asset_config(self, asset_type: str) -> Dict:
        """Get config for a specific asset type."""
        config = self.get_config()
        return config.get("asset_types", {}).get(asset_type, config.get("asset_types", {}).get("Pump", {}))
    
    def get_thresholds(self, asset_type: str) -> Dict:
        """Get thresholds for a specific asset type."""
        asset_config = self.get_asset_config(asset_type)
        return asset_config.get("thresholds", {})
    
    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Get workflow sequence for an incident type."""
        config = self.get_config()
        return config.get("workflow_sequences", {}).get(incident_type, ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"])
    
    def get_prediction_params(self) -> Dict:
        """Get prediction parameters."""
        config = self.get_config()
        return config.get("prediction", {})
    
    def get_severity_priority(self, severity: str) -> int:
        """Get priority for a severity level."""
        config = self.get_config()
        return config.get("severity_mapping", {}).get(severity, 3)
```

## backend/services/asset.py

**Folder path:** `backend/services`

**File path:** `backend/services/asset.py`

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

## backend/services/computation_engine.py

**Folder path:** `backend/services`

**File path:** `backend/services/computation_engine.py`

```python
"""Real-time computation engine - Runs every 10-15 seconds."""

import time
import math
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import deque
from services.ai_config import AIConfigGenerator
from models.sensor import SensorType


class ComputationEngine:
    """Computes health, failure probability, RUL in real-time."""
    
    _instance = None
    _last_computation = 0
    _computation_interval = 10  # seconds
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.config = AIConfigGenerator()
        self._history_cache: Dict[str, deque] = {}
        self._health_cache: Dict[str, float] = {}
        self._failure_cache: Dict[str, float] = {}
        self._rul_cache: Dict[str, float] = {}
        self._last_tick = 0
        self._kernel = None  # ✅ Will be set lazily
    
    @property
    def kernel(self):
        """Lazy load kernel to avoid circular imports."""
        if self._kernel is None:
            from services.runtime import runtime
            self._kernel = runtime.kernel
        return self._kernel
    
    def should_compute(self, tick: int) -> bool:
        """Check if computation should run (every 10-15 seconds)."""
        now = time.time()
        if now - self._last_computation >= self._computation_interval:
            self._last_computation = now
            return True
        return False
    
    def compute_all(self, tick: int, telemetry: List[Any], assets: List[Any]) -> Dict:
        """Compute everything for all assets."""
        if not self.should_compute(tick):
            return self._get_cached_results()
        
        print(f"🧮 Computing health metrics at tick {tick}...")
        start = time.time()
        
        results = {}
        for asset in assets:
            asset_telemetry = [t for t in telemetry if t.asset_id == asset.id]
            result = self.compute_asset(asset, asset_telemetry)
            results[asset.id] = result
        
        elapsed = time.time() - start
        print(f"✅ Computation completed in {elapsed:.3f}s for {len(assets)} assets")
        
        return results
    
    def compute_asset(self, asset: Any, telemetry: List[Any]) -> Dict:
        """Compute metrics for a single asset."""
        if not telemetry:
            return {
                "health": 100.0,
                "failure_probability": 0.0,
                "rul_days": 365,
                "confidence": 0.0,
                "status": "Running",
                "degradation_rate": 0.0,
            }
        
        # Get asset type config
        asset_type = asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type)
        config = self.config.get_asset_config(asset_type)
        thresholds = config.get("thresholds", {})
        weights = config.get("weight", {})
        degradation_rate_base = config.get("degradation_rate", 0.5)
        critical_health = config.get("critical_health", 50)
        
        # 1. Calculate health
        health = self._calculate_health(telemetry, thresholds, weights)
        
        # 2. Calculate degradation rate
        degradation_rate = self._calculate_degradation_rate(telemetry, degradation_rate_base)
        
        # 3. Calculate failure probability
        failure_probability = self._calculate_failure_probability(health, degradation_rate)
        
        # 4. Calculate RUL
        rul_days = self._calculate_rul(health, degradation_rate)
        
        # 5. Calculate confidence
        confidence = self._calculate_confidence(len(telemetry))
        
        # 6. Determine status
        status = self._determine_status(health, critical_health)
        
        return {
            "health": round(health, 1),
            "failure_probability": round(failure_probability, 1),
            "rul_days": round(rul_days, 1),
            "confidence": round(confidence, 2),
            "status": status,
            "degradation_rate": round(degradation_rate, 3),
            "telemetry_count": len(telemetry),
            "asset_type": asset_type,
        }
    
    def _calculate_health(self, telemetry: List[Any], thresholds: Dict, weights: Dict) -> float:
        """Calculate health based on telemetry violations."""
        health = 100.0
        violations = {}
        
        for reading in telemetry:
            sensor_type = reading.sensor_type
            
            # ✅ Check each sensor against thresholds with zero protection
            if sensor_type == SensorType.PRESSURE:
                limit = thresholds.get("pressure_max", 150)
                if limit > 0 and reading.value > limit:  # ✅ Check limit > 0
                    violation = (reading.value - limit) / limit * 100
                    violations["pressure"] = max(violations.get("pressure", 0), violation)
            
            elif sensor_type == SensorType.TEMPERATURE:
                limit = thresholds.get("temperature_max", 85)
                if limit > 0 and reading.value > limit:  # ✅ Check limit > 0
                    violation = (reading.value - limit) / limit * 100
                    violations["temperature"] = max(violations.get("temperature", 0), violation)
            
            elif sensor_type == SensorType.GAS:
                limit = thresholds.get("gas_max", 40)
                if limit > 0 and reading.value > limit:  # ✅ Check limit > 0
                    violation = (reading.value - limit) / limit * 100
                    violations["gas"] = max(violations.get("gas", 0), violation)
            
            elif sensor_type == SensorType.VIBRATION:
                limit = thresholds.get("vibration_max", 8)
                if limit > 0 and reading.value > limit:  # ✅ Check limit > 0
                    violation = (reading.value - limit) / limit * 100
                    violations["vibration"] = max(violations.get("vibration", 0), violation)
            
            elif sensor_type == SensorType.FLOW:
                limit = thresholds.get("flow_min", 25)
                if limit > 0 and reading.value < limit:  # ✅ Check limit > 0
                    violation = (limit - reading.value) / limit * 100
                    violations["flow"] = max(violations.get("flow", 0), violation)
        
        # Apply weighted violations
        total_weight = 0
        weighted_violation = 0
        
        for sensor, violation in violations.items():
            weight = weights.get(f"{sensor}_weight", 20)
            total_weight += weight
            weighted_violation += violation * (weight / 100)
        
        # Reduce health based on violations
        if total_weight > 0:
            health = max(0, health - weighted_violation)
        
        # Apply degradation over time (exponential decay)
        degradation_factor = min(1, len(telemetry) / 1000)
        health = health * (1 - 0.001 * degradation_factor)
        
        return max(0, min(100, health))
    
    def _calculate_degradation_rate(self, telemetry: List[Any], base_rate: float) -> float:
        """Calculate degradation rate from telemetry trends."""
        if len(telemetry) < 2:
            return base_rate
        
        # Calculate trend
        values = []
        for reading in telemetry:
            if reading.sensor_type == SensorType.VIBRATION:
                values.append(reading.value)
            elif reading.sensor_type == SensorType.TEMPERATURE:
                values.append(reading.value * 0.5)
        
        if len(values) < 2:
            return base_rate
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # Convert slope to degradation rate (0.1 to 2.0)
        rate = abs(slope) * 0.1
        degradation_rate = max(0.1, min(2.0, rate + base_rate * 0.5))
        
        return degradation_rate
    
    def _calculate_failure_probability(self, health: float, degradation_rate: float) -> float:
        """Calculate failure probability from health and degradation."""
        health_factor = (100 - health) / 100
        degradation_factor = min(1, degradation_rate / 1.0)
        probability = health_factor * 0.7 + degradation_factor * 0.3
        probability = 1 - math.exp(-probability * 3)
        return min(100, max(0, probability * 100))
    
    def _calculate_rul(self, health: float, degradation_rate: float) -> float:
        """Calculate Remaining Useful Life in days."""
        if degradation_rate <= 0:
            return 365
        rul = health / (degradation_rate * 5)
        return max(1, min(365, rul))
    
    def _calculate_confidence(self, sample_count: int) -> float:
        """Calculate confidence based on sample count."""
        confidence = 0.55 + min(sample_count, 20) * 0.02
        return min(0.95, confidence)
    
    def _determine_status(self, health: float, critical_health: float) -> str:
        """Determine status from health value."""
        if health >= 80:
            return "Running"
        elif health >= critical_health:
            return "Warning"
        elif health >= 30:
            return "Critical"
        else:
            return "Offline"
    
    def _get_cached_results(self) -> Dict:
        """Return cached results if computation not needed."""
        return {}
    
    def get_asset_health(self, asset_id: str) -> Optional[float]:
        """Get cached health for an asset."""
        return self._health_cache.get(asset_id)
    
    def get_asset_failure_probability(self, asset_id: str) -> Optional[float]:
        """Get cached failure probability for an asset."""
        return self._failure_cache.get(asset_id)
    
    def get_asset_rul(self, asset_id: str) -> Optional[float]:
        """Get cached RUL for an asset."""
        return self._rul_cache.get(asset_id)
```

## backend/services/config_services.py

**Folder path:** `backend/services`

**File path:** `backend/services/config_services.py`

```python
"""Optimized Gemini-powered dynamic configuration service with precomputation."""

import json
import re
import time
from typing import Any, Dict, List, Optional
from functools import lru_cache
from services.llm import LLMManager


class ConfigService:
    """Generate and cache operational configurations using Gemini."""

    _instance = None
    _cache: Dict[str, Any] = {}
    _precomputed: Dict[str, Any] = {}
    _precomputed_done = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.llm = LLMManager()
        if not ConfigService._precomputed_done:
            self._precompute_defaults()
            ConfigService._precomputed_done = True

    def _precompute_defaults(self):
        """Precompute common configurations for all asset types."""
        asset_types = ["Pump", "Compressor", "Tank", "Valve", "Pipeline", "Heat Exchanger", "Reactor", "Boiler", "Turbine"]
        
        for asset_type in asset_types:
            cache_key = f"thresholds_{asset_type}_default"
            if cache_key not in self._precomputed:
                try:
                    self._precomputed[cache_key] = self._generate_thresholds(asset_type)
                except:
                    self._precomputed[cache_key] = self._get_default_thresholds(asset_type)
        
        print(f"✅ Precomputed thresholds for {len(asset_types)} asset types")

    @lru_cache(maxsize=128)
    def _generate_thresholds(self, asset_type: str) -> Dict[str, float]:
        """Generate thresholds with caching."""
        prompt = f"""
You are an industrial operations configuration expert.

Generate operational thresholds for a {asset_type} asset.

Return ONLY a JSON object with these fields:
- pressure_max: float (maximum safe pressure in PSI)
- temperature_max: float (maximum safe temperature in °C)
- gas_max: float (maximum safe gas concentration in ppm)
- vibration_max: float (maximum safe vibration in mm/s)
- flow_min: float (minimum safe flow rate in L/min)

Use realistic values for {asset_type} equipment.
Respond with ONLY valid JSON, no other text.
"""
        try:
            response = self.llm.generate(prompt, use_cache=True)
            return self._parse_json(response)
        except Exception as e:
            print(f"⚠️ Gemini config generation failed: {e}")
            return self._get_default_thresholds(asset_type)

    def _parse_json(self, response: str) -> Dict:
        """Extract JSON from Gemini response."""
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            return json.loads(json_str)
        raise ValueError("No JSON found in response")

    def _get_default_thresholds(self, asset_type: str) -> Dict:
        """Fallback thresholds when Gemini is unavailable."""
        defaults = {
            "Pump": {"pressure_max": 150, "temperature_max": 85, "gas_max": 40, "vibration_max": 8, "flow_min": 25},
            "Compressor": {"pressure_max": 160, "temperature_max": 90, "gas_max": 35, "vibration_max": 10, "flow_min": 30},
            "Tank": {"pressure_max": 120, "temperature_max": 80, "gas_max": 45, "vibration_max": 5, "flow_min": 20},
            "Valve": {"pressure_max": 140, "temperature_max": 85, "gas_max": 40, "vibration_max": 7, "flow_min": 15},
            "Pipeline": {"pressure_max": 130, "temperature_max": 80, "gas_max": 50, "vibration_max": 6, "flow_min": 10},
            "Heat Exchanger": {"pressure_max": 145, "temperature_max": 100, "gas_max": 30, "vibration_max": 9, "flow_min": 25},
            "Reactor": {"pressure_max": 155, "temperature_max": 95, "gas_max": 35, "vibration_max": 8, "flow_min": 20},
            "Boiler": {"pressure_max": 170, "temperature_max": 120, "gas_max": 25, "vibration_max": 10, "flow_min": 30},
            "Turbine": {"pressure_max": 140, "temperature_max": 100, "gas_max": 30, "vibration_max": 12, "flow_min": 25},
        }
        return defaults.get(asset_type, defaults["Pump"])

    def get_thresholds(self, asset_type: str, context: Optional[str] = None) -> Dict[str, float]:
        """Get thresholds - uses precomputed values for speed."""
        # ✅ Check precomputed first (super fast)
        precomputed_key = f"thresholds_{asset_type}_default"
        if precomputed_key in self._precomputed:
            return self._precomputed[precomputed_key]
        
        cache_key = f"thresholds_{asset_type}_{context or 'default'}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        thresholds = self._generate_thresholds(asset_type)
        self._cache[cache_key] = thresholds
        return thresholds

    def get_workflow_sequence(self, incident_type: str) -> List[str]:
        """Generate agent sequence for an incident type."""
        cache_key = f"workflow_{incident_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
For an industrial {incident_type} incident, list the agents that should respond in order.

Available agents: sensor, safety, diagnostic, knowledge, maintenance, planning, prediction, notification, report

Return ONLY a JSON array of agent names.
Example: ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]
"""

        try:
            response = self.llm.generate(prompt, use_cache=True)
            sequence = self._parse_json(response)
            if isinstance(sequence, list):
                self._cache[cache_key] = sequence
                return sequence
        except Exception:
            pass

        return ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]

    def get_priority_level(self, incident_type: str, severity: str) -> int:
        """Generate priority level for an incident."""
        prompt = f"""
For an industrial {incident_type} incident with {severity} severity, assign a priority level.

Priority is 1 (highest) to 9 (lowest).
Return ONLY an integer.
"""

        try:
            response = self.llm.generate(prompt, use_cache=True)
            numbers = re.findall(r'\d+', response)
            if numbers:
                priority = int(numbers[0])
                return max(1, min(9, priority))
        except Exception:
            pass

        severity_map = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        return severity_map.get(severity, 3)

    def get_risk_weights(self, incident_type: str) -> Dict[str, int]:
        """Generate risk weights for different sensors."""
        cache_key = f"risk_weights_{incident_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
For a {incident_type} incident, assign risk weights (0-100) to each sensor type.

Return ONLY a JSON object with:
- pressure_weight: int
- temperature_weight: int
- gas_weight: int
- vibration_weight: int
- flow_weight: int

Sum of all weights should be 100.
"""

        try:
            response = self.llm.generate(prompt, use_cache=True)
            weights = self._parse_json(response)
            self._cache[cache_key] = weights
            return weights
        except Exception:
            pass

        return {"pressure_weight": 30, "temperature_weight": 25, "gas_weight": 35, "vibration_weight": 20, "flow_weight": 10}

    def clear_cache(self):
        """Clear the configuration cache."""
        self._cache = {}
        print("✅ Config cache cleared")

    def refresh(self):
        """Refresh all configurations by clearing cache."""
        self.clear_cache()
        return {"status": "refreshed", "cache_size": 0}
```

## backend/services/embedding.py

**Folder path:** `backend/services`

**File path:** `backend/services/embedding.py`

```python

```

## backend/services/health.py

**Folder path:** `backend/services`

**File path:** `backend/services/health.py`

```python
"""Health service using the computation engine with AI-generated thresholds."""

from models.sensor import SensorType
from services.computation_engine import ComputationEngine


class HealthService:
    """
    Calculates asset health from recent telemetry using AI-generated thresholds.
    """

    def __init__(self):
        self.engine = ComputationEngine()
        self._threshold_cache = {}

    def calculate_health(self, readings):
        """
        Calculate health from readings using AI-generated thresholds.
        
        Args:
            readings: List of sensor readings for an asset
            
        Returns:
            float: Health score (0-100)
        """
        if not readings:
            return 100.0

        # Get asset type from first reading
        asset_id = readings[0].asset_id
        asset = self.engine.kernel.asset_service.get(asset_id)
        asset_type = asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type)
        
        # Get thresholds from AI config
        thresholds = self.engine.config.get_thresholds(asset_type)
        weights = self.engine.config.get_asset_config(asset_type).get("weight", {})
        
        # Calculate health using the engine
        health = self.engine._calculate_health(readings, thresholds, weights)
        
        return max(0.0, min(100.0, health))

    def calculate_health_with_limits(self, readings, limits=None):
        """
        Calculate health with custom limits (fallback method).
        
        Args:
            readings: List of sensor readings
            limits: Optional custom limits dict
            
        Returns:
            float: Health score (0-100)
        """
        if not readings:
            return 100.0

        if limits is None:
            limits = {
                SensorType.PRESSURE: 150,
                SensorType.TEMPERATURE: 90,
                SensorType.FLOW: 40,
                SensorType.VIBRATION: 25,
                SensorType.GAS: 15,
            }

        health = 100.0

        for reading in readings:
            limit = limits.get(reading.sensor_type)
            if limit is None:
                continue

            if reading.sensor_type == SensorType.FLOW:
                if reading.value < limit:
                    health -= 5
            else:
                if reading.value > limit:
                    health -= 5

        return max(0.0, health)

    def get_health_metrics(self, asset, telemetry):
        """
        Get full health metrics for an asset using computation engine.
        
        Args:
            asset: Asset object
            telemetry: List of telemetry readings
            
        Returns:
            dict: Full health metrics
        """
        return self.engine.compute_asset(asset, telemetry)

    def get_asset_health_status(self, asset_id):
        """
        Get cached health status for an asset.
        
        Args:
            asset_id: ID of the asset
            
        Returns:
            dict: Health status including health, status, failure probability
        """
        health = self.engine.get_asset_health(asset_id)
        failure_prob = self.engine.get_asset_failure_probability(asset_id)
        rul = self.engine.get_asset_rul(asset_id)
        
        if health is None:
            return {"health": 100, "status": "Running", "failure_probability": 0, "rul": "365 days"}
        
        return {
            "health": health,
            "status": self.engine._determine_status(health, 50),
            "failure_probability": failure_prob or 0,
            "rul": rul or 365
        }
```

## backend/services/incident_manager.py

**Folder path:** `backend/services`

**File path:** `backend/services/incident_manager.py`

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

## backend/services/incident_service.py

**Folder path:** `backend/services`

**File path:** `backend/services/incident_service.py`

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

## backend/services/kernel_factory.py

**Folder path:** `backend/services`

**File path:** `backend/services/kernel_factory.py`

```python
"""
services/kernel_factory.py

Compatibility access point for the shared MAO kernel.
"""

from mao import MAOKernel
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def create_kernel() -> MAOKernel:
    """
    Return the already initialized production kernel.
    """
    return runtime.kernel


def get_kernel() -> MAOKernel:
    """
    Return the shared MAO kernel instance.
    """
    return runtime.kernel
```

## backend/services/llm.py

**Folder path:** `backend/services`

**File path:** `backend/services/llm.py`

```python
"""Centralized, failover-safe access to Gemini models with multi-key rotation and caching."""

import hashlib
import logging
import os
import socket
import time
from pathlib import Path
from typing import Optional, Dict, List
from collections import deque
from datetime import datetime
from urllib.parse import urlsplit

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# ✅ SUPPORTED ENV VARS - ALL POSSIBLE NAMING CONVENTIONS
SUPPORTED_GEMINI_ENV_VARS = (
    # Standard naming
    "GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3",
    "GEMINI_API_KEY_4", "GEMINI_API_KEY_5", "GEMINI_API_KEY_6",
    "GEMINI_API_KEY_7", "GEMINI_API_KEY_8", "GEMINI_API_KEY_9",
    "GEMINI_API_KEY_10",
    # Alternative naming
    "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3",
    "GOOGLE_API_KEY_4", "GOOGLE_API_KEY_5", "GOOGLE_API_KEY_6",
    "GOOGLE_API_KEY_7",
    # Single key fallback
    "GEMINI_API_KEY", "GOOGLE_API_KEY",
)

DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"

_PROXY_ENV_VARS = (
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
    "http_proxy", "https_proxy", "all_proxy",
)
_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _has_invalid_gemini_proxy() -> bool:
    """Return whether this process inherited the known dead loopback proxy."""
    for name in _PROXY_ENV_VARS:
        value = os.getenv(name)
        if not value:
            continue
        try:
            proxy = urlsplit(value)
            if proxy.hostname not in _LOOPBACK_HOSTS or proxy.port is None:
                continue
            if proxy.port == 9:
                return True
            with socket.create_connection((proxy.hostname, proxy.port), timeout=0.15):
                pass
        except OSError:
            return True
        except ValueError:
            continue
    return False


class RateLimiter:
    """Simple rate limiter for API calls with per-key tracking."""

    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.call_timestamps: Dict[str, deque] = {}

    def wait_if_needed(self, key: str):
        """Wait if rate limit would be exceeded for a specific key."""
        now = time.time()

        if key not in self.call_timestamps:
            self.call_timestamps[key] = deque(maxlen=self.calls_per_minute)

        timestamps = self.call_timestamps[key]

        while timestamps and now - timestamps[0] > 60:
            timestamps.popleft()

        if len(timestamps) >= self.calls_per_minute:
            oldest = timestamps[0]
            wait_time = 60 - (now - oldest) + 0.5
            if wait_time > 0:
                logger.warning(f"Rate limit reached for key, waiting {wait_time:.2f}s")
                time.sleep(wait_time)

        timestamps.append(time.time())


class KeyStatus:
    """Track status of each API key."""

    def __init__(self, key: str, index: int):
        self.key = key
        self.index = index
        self.failures = 0
        self.successes = 0
        self.last_used: Optional[float] = None
        self.last_error: Optional[str] = None
        self.is_active = True
        self.cooldown_until: Optional[float] = None
        self.total_requests = 0

    def record_success(self):
        self.successes += 1
        self.failures = 0
        self.last_used = time.time()
        self.total_requests += 1
        self.is_active = True

    def record_failure(self, error: str):
        self.failures += 1
        self.last_error = error
        self.total_requests += 1

        # ✅ More aggressive cooldown - 30 seconds instead of 60
        if self.failures >= 3:
            self.is_active = False
            self.cooldown_until = time.time() + 30
            logger.warning(f"Key {self.index + 1} deactivated for 30s due to {self.failures} failures")

    def reactivate_if_ready(self):
        if not self.is_active and self.cooldown_until:
            if time.time() >= self.cooldown_until:
                self.is_active = True
                self.failures = 0
                self.cooldown_until = None
                logger.info(f"Key {self.index + 1} reactivated after cooldown")
                return True
        return False

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.successes / self.total_requests) * 100

    @property
    def is_available(self) -> bool:
        if not self.is_active:
            return False
        if self.cooldown_until and time.time() < self.cooldown_until:
            return False
        return True

    def to_dict(self) -> Dict:
        return {
            "index": self.index + 1,
            "key_preview": self.key[:8] + "..." + self.key[-4:],
            "is_active": self.is_active,
            "is_available": self.is_available,
            "failures": self.failures,
            "successes": self.successes,
            "total_requests": self.total_requests,
            "success_rate": f"{self.success_rate:.1f}%",
            "last_used": datetime.fromtimestamp(self.last_used).strftime("%H:%M:%S") if self.last_used else "Never",
            "last_error": self.last_error or "None",
        }


# Response Cache
_response_cache: Dict[str, tuple] = {}
_CACHE_MAX_SIZE = 100


class LLMManager:
    """Central Gemini router with automatic multi-key rotation and caching."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        self.keys = self._load_keys()
        self.current_key_index = 0
        self.key_statuses: Dict[str, KeyStatus] = {}
        self.rate_limiter = RateLimiter(calls_per_minute=60)

        for idx, key in enumerate(self.keys):
            self.key_statuses[key] = KeyStatus(key, idx)

        if not self.keys:
            raise RuntimeError(
                "No Gemini API key was found. Configure one of:\n"
                + "\n".join(f"  - {var}" for var in SUPPORTED_GEMINI_ENV_VARS)
            )

        logger.info(f"LLMManager initialized with {len(self.keys)} Gemini key(s)")

    def _load_keys(self) -> List[str]:
        """✅ Load API keys from ALL possible sources."""
        keys = []
        seen = set()

        # 1. Check environment variables
        print("\n🔑 Loading Gemini API Keys...")
        for var in SUPPORTED_GEMINI_ENV_VARS:
            value = os.getenv(var)
            if value and value not in seen:
                seen.add(value)
                keys.append(value)
                print(f"  ✅ Loaded from {var}: {value[:8]}...{value[-4:]}")

        # 2. Check .env file directly
        try:
            env_path = PROJECT_ROOT / ".env"
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('GEMINI_API_KEY') or line.startswith('GOOGLE_API_KEY'):
                            if '=' in line:
                                key = line.split('=', 1)[1].strip()
                                if key and key not in seen:
                                    seen.add(key)
                                    keys.append(key)
                                    print(f"  ✅ Loaded from .env: {key[:8]}...{key[-4:]}")
        except Exception as e:
            print(f"  ⚠️ Could not read .env: {e}")

        # 3. Check Streamlit secrets
        try:
            import streamlit as st
            for var in SUPPORTED_GEMINI_ENV_VARS:
                if var in st.secrets:
                    value = st.secrets[var]
                    if value and value not in seen:
                        seen.add(value)
                        keys.append(value)
                        print(f"  ✅ Loaded from secrets[{var}]: {value[:8]}...{value[-4:]}")
        except Exception:
            pass

        print(f"\n✅ Total keys loaded: {len(keys)}\n")
        return keys

    def _get_next_available_key(self) -> Optional[str]:
        """✅ Get the next available API key with rotation."""
        total_keys = len(self.keys)
        attempts = 0

        # Try all keys in rotation
        while attempts < total_keys:
            idx = self.current_key_index
            key = self.keys[idx]
            self.current_key_index = (self.current_key_index + 1) % total_keys

            status = self.key_statuses[key]
            
            # Try to reactivate if cooldown expired
            if not status.is_active:
                status.reactivate_if_ready()

            if status.is_available:
                status.last_used = time.time()
                return key

            attempts += 1

        # If all keys are exhausted, try to reactivate one
        for key in self.keys:
            status = self.key_statuses[key]
            if status.reactivate_if_ready():
                return key

        # Last resort: use first key (even if it's failing)
        return self.keys[0]

    def _create_model(self, key: str):
        """Create a Gemini model instance."""
        client_args = {"trust_env": False} if _has_invalid_gemini_proxy() else None
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=key,
            client_args=client_args,
            temperature=0.3,
        )

    def generate(self, prompt: str, max_retries_per_key: int = 2, use_cache: bool = True) -> str:
        """✅ Generate Gemini response with automatic multi-key rotation."""
        
        # Check cache first
        if use_cache:
            cache_key = hashlib.md5(prompt.encode()).hexdigest()
            if cache_key in _response_cache:
                cached_response, cached_time = _response_cache[cache_key]
                if time.time() - cached_time < 300:
                    logger.info(f"✅ Cache hit for prompt (key: {cache_key[:8]})")
                    return cached_response
                else:
                    del _response_cache[cache_key]
        
        last_error = None
        
        # ✅ Try each key in rotation
        for attempt in range(len(self.keys) * max_retries_per_key):
            try:
                key = self._get_next_available_key()
                if key is None:
                    raise RuntimeError("No available API keys")

                status = self.key_statuses[key]
                logger.info(f"Using Gemini key {status.index + 1}/{len(self.keys)}")

                self.rate_limiter.wait_if_needed(key)
                response = self._create_model(key).invoke(prompt)

                status.record_success()

                content = response.content
                if isinstance(content, str):
                    response_text = content
                elif isinstance(content, list):
                    response_text = "".join(
                        part if isinstance(part, str) else part.get("text", "")
                        for part in content
                        if isinstance(part, str) or isinstance(part, dict)
                    )
                else:
                    response_text = str(content)
                
                # Cache the response
                if use_cache and response_text:
                    cache_key = hashlib.md5(prompt.encode()).hexdigest()
                    _response_cache[cache_key] = (response_text, time.time())
                    
                    if len(_response_cache) > _CACHE_MAX_SIZE:
                        oldest_keys = sorted(_response_cache.keys(), key=lambda k: _response_cache[k][1])[:10]
                        for key in oldest_keys:
                            del _response_cache[key]
                
                return response_text

            except Exception as error:
                last_error = error
                error_str = str(error)
                
                # ✅ Handle rate limiting specially
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    logger.warning(f"⚠️ Key {status.index + 1} rate limited (429). Moving to next key.")
                    # ✅ Don't deactivate on rate limit - just use next key
                    if key and key in self.key_statuses:
                        status = self.key_statuses[key]
                        status.failures += 1
                        status.last_error = error_str
                    time.sleep(0.5)
                else:
                    if key and key in self.key_statuses:
                        status = self.key_statuses[key]
                        status.record_failure(error_str)
                        logger.warning(f"Key {status.index + 1} failed: {error_str[:100]}")
                    time.sleep(0.5)
                
                continue

        raise RuntimeError(
            f"All {len(self.keys)} Gemini API keys failed. Last error: {last_error}"
        ) from last_error

    def get_key_status(self) -> Dict[str, any]:
        """Get status of all API keys for monitoring."""
        return {
            "total_keys": len(self.keys),
            "model": self.model_name,
            "current_index": self.current_key_index + 1,
            "keys": [self.key_statuses[key].to_dict() for key in self.keys],
            "summary": {
                "active_keys": sum(1 for s in self.key_statuses.values() if s.is_active),
                "available_keys": sum(1 for s in self.key_statuses.values() if s.is_available),
                "total_requests": sum(s.total_requests for s in self.key_statuses.values()),
                "overall_success_rate": (
                    sum(s.successes for s in self.key_statuses.values()) /
                    max(1, sum(s.total_requests for s in self.key_statuses.values())) * 100
                ),
            }
        }

    def reset_key(self, key_index: int) -> bool:
        """Reset a specific key's status."""
        try:
            key = self.keys[key_index - 1]
            status = self.key_statuses[key]
            status.failures = 0
            status.is_active = True
            status.cooldown_until = None
            status.last_error = None
            logger.info(f"Key {key_index} reset successfully")
            return True
        except (IndexError, KeyError):
            return False

    def clear_cache(self):
        """Clear the response cache."""
        global _response_cache
        _response_cache.clear()
        logger.info("LLM response cache cleared")
```

## backend/services/maintenance_scheduler.py

**Folder path:** `backend/services`

**File path:** `backend/services/maintenance_scheduler.py`

```python
"""Maintenance scheduling service."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field


class MaintenancePriority(str, Enum):
    CRITICAL = "critical"   # Within 24 hours
    HIGH = "high"          # Within 3 days
    MEDIUM = "medium"      # Within 7 days
    LOW = "low"            # Within 30 days


@dataclass
class MaintenanceTask:
    """Maintenance task data."""
    id: str
    asset_id: str
    asset_name: str
    asset_type: str
    priority: MaintenancePriority
    description: str
    scheduled_date: datetime
    estimated_duration_hours: float
    estimated_cost: float
    assigned_team: str
    status: str = "scheduled"  # scheduled, in_progress, completed, cancelled
    created_at: datetime = field(default_factory=datetime.now)


class MaintenanceScheduler:
    """Schedule maintenance based on asset health and RUL."""
    
    _instance = None
    _tasks: List[MaintenanceTask] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def schedule_maintenance(self, asset: Dict, metrics: Dict) -> Optional[MaintenanceTask]:
        """Schedule maintenance for an asset based on its health."""
        health = metrics.get("health", 100)
        failure_probability = metrics.get("failure_probability", 0)
        rul_days = metrics.get("rul_days", 365)
        
        # Determine priority
        if failure_probability > 70 or rul_days < 7:
            priority = MaintenancePriority.CRITICAL
            scheduled_date = datetime.now() + timedelta(hours=12)
            duration = 6
        elif failure_probability > 40 or rul_days < 30:
            priority = MaintenancePriority.HIGH
            scheduled_date = datetime.now() + timedelta(days=1)
            duration = 4
        elif failure_probability > 20 or rul_days < 60:
            priority = MaintenancePriority.MEDIUM
            scheduled_date = datetime.now() + timedelta(days=3)
            duration = 2
        else:
            priority = MaintenancePriority.LOW
            scheduled_date = datetime.now() + timedelta(days=7)
            duration = 1
        
        # Check if already scheduled
        for task in self._tasks:
            if task.asset_id == asset.get("id") and task.status == "scheduled":
                return None
        
        # Estimate cost
        cost = self._estimate_cost(asset.get("type", "Pump"), duration, priority)
        
        task = MaintenanceTask(
            id=f"MT-{len(self._tasks) + 1:04d}",
            asset_id=asset.get("id", "unknown"),
            asset_name=asset.get("name", "Unknown Asset"),
            asset_type=asset.get("type", "Pump"),
            priority=priority,
            description=self._generate_description(asset, metrics),
            scheduled_date=scheduled_date,
            estimated_duration_hours=duration,
            estimated_cost=cost,
            assigned_team=self._assign_team(asset.get("type", "Pump")),
        )
        
        self._tasks.append(task)
        return task
    
    def _estimate_cost(self, asset_type: str, duration_hours: float, priority: MaintenancePriority) -> float:
        """Estimate maintenance cost."""
        base_costs = {
            "Pump": 500,
            "Compressor": 1000,
            "Tank": 300,
            "Valve": 200,
            "Pipeline": 800,
            "Heat Exchanger": 1200,
            "Reactor": 2000,
            "Boiler": 1500,
            "Turbine": 2500,
            "Motor": 400,
            "Generator": 1800,
            "Distillation Column": 3000,
        }
        
        base = base_costs.get(asset_type, 500)
        
        # Priority multiplier
        priority_multiplier = {
            MaintenancePriority.CRITICAL: 2.0,
            MaintenancePriority.HIGH: 1.5,
            MaintenancePriority.MEDIUM: 1.0,
            MaintenancePriority.LOW: 0.7,
        }
        
        return base * (duration_hours / 2) * priority_multiplier.get(priority, 1.0)
    
    def _assign_team(self, asset_type: str) -> str:
        """Assign maintenance team based on asset type."""
        team_map = {
            "Pump": "Rotating Equipment",
            "Compressor": "Rotating Equipment",
            "Tank": "Tank & Vessel",
            "Valve": "Instrumentation",
            "Pipeline": "Pipeline",
            "Heat Exchanger": "Utilities",
            "Reactor": "Process",
            "Boiler": "Utilities",
            "Turbine": "Rotating Equipment",
            "Motor": "Electrical",
            "Generator": "Electrical",
            "Distillation Column": "Process",
        }
        return team_map.get(asset_type, "General Maintenance")
    
    def _generate_description(self, asset: Dict, metrics: Dict) -> str:
        """Generate maintenance description."""
        health = metrics.get("health", 100)
        failure_prob = metrics.get("failure_probability", 0)
        
        if health < 40:
            return f"Emergency maintenance required - asset health at {health:.0f}%"
        elif health < 60:
            return f"Priority maintenance - asset health at {health:.0f}%, failure risk {failure_prob:.0f}%"
        elif health < 80:
            return f"Routine maintenance - asset health at {health:.0f}%, failure risk {failure_prob:.0f}%"
        else:
            return f"Preventive maintenance - asset health at {health:.0f}%"
    
    def get_upcoming_tasks(self, days: int = 7) -> List[MaintenanceTask]:
        """Get maintenance tasks scheduled in the next N days."""
        cutoff = datetime.now() + timedelta(days=days)
        return [t for t in self._tasks if t.scheduled_date <= cutoff and t.status == "scheduled"]
    
    def get_tasks_by_priority(self) -> Dict[MaintenancePriority, List[MaintenanceTask]]:
        """Get tasks grouped by priority."""
        result = {p: [] for p in MaintenancePriority}
        for task in self._tasks:
            if task.status == "scheduled":
                result[task.priority].append(task)
        return result
    
    def get_next_maintenance_date(self, asset_id: str) -> Optional[datetime]:
        """Get the next scheduled maintenance date for an asset."""
        tasks = [t for t in self._tasks if t.asset_id == asset_id and t.status == "scheduled"]
        if tasks:
            return min(t.scheduled_date for t in tasks)
        return None


# Singleton
maintenance_scheduler = MaintenanceScheduler()
```

## backend/services/notification_service.py

**Folder path:** `backend/services`

**File path:** `backend/services/notification_service.py`

```python
"""Real-time notification service."""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class NotificationType(str, Enum):
    INCIDENT_DETECTED = "incident_detected"
    AGENTS_WORKING = "agents_working"
    AGENTS_COMPLETE = "agents_complete"
    INCIDENT_RESOLVED = "incident_resolved"
    MAINTENANCE_SCHEDULED = "maintenance_scheduled"
    REVENUE_IMPACT = "revenue_impact"


class NotificationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"


@dataclass
class Notification:
    id: str
    type: NotificationType
    severity: NotificationSeverity
    title: str
    message: str
    asset_id: Optional[str] = None
    asset_name: Optional[str] = None
    incident_type: Optional[str] = None
    revenue_impact: Optional[float] = None
    maintenance_scheduled: Optional[str] = None
    human_approval_required: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False
    metadata: dict = field(default_factory=dict)


class NotificationService:
    _instance = None
    _notifications: List[Notification] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def add_notification(self, notification: Notification) -> None:
        self._notifications.insert(0, notification)
        if len(self._notifications) > 100:
            self._notifications = self._notifications[:100]
        print(f"🔔 NOTIFICATION: {notification.title} - {notification.message}")
    
    def get_notifications(self, limit: int = 20, unread_only: bool = False) -> List[Notification]:
        notifications = self._notifications
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        return notifications[:limit]
    
    def mark_read(self, notification_id: str) -> None:
        for n in self._notifications:
            if n.id == notification_id:
                n.read = True
                break
    
    def mark_all_read(self) -> None:
        for n in self._notifications:
            n.read = True
    
    def get_unread_count(self) -> int:
        return len([n for n in self._notifications if not n.read])


notification_service = NotificationService()
```

## backend/services/persistence.py

**Folder path:** `backend/services`

**File path:** `backend/services/persistence.py`

```python
"""Persistence service with buffer and sync saving."""

import logging
import time
from threading import Lock, Thread
from collections import deque
from datetime import datetime
from typing import List, Any

from database.connection import get_session
from database.models import AgentExecutionDB, ExecutionReportDB, IncidentDB, TelemetryDB
from database.repositories.agent_repo import AgentRepository
from database.repositories.incident_repo import IncidentRepository
from database.repositories.report_repo import ReportRepository
from database.repositories.telemetry_repo import TelemetryRepository

logger = logging.getLogger(__name__)


class PersistenceService:
    """Handles database persistence with buffer and sync saving."""
    
    def __init__(self):
        self._buffer = deque(maxlen=5000)  # Buffer up to 5000 readings
        self._lock = Lock()
        self._running = True
        self._flush_thread = None
        self._start_flush_thread()
    
    def _start_flush_thread(self):
        """Start background thread to flush buffer."""
        self._flush_thread = Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()
    
    def _flush_loop(self):
        """Background loop to flush buffer every 5 seconds."""
        while self._running:
            time.sleep(5)
            self._flush_buffer()
    
    def _flush_buffer(self):
        """Flush buffered telemetry to database."""
        if not self._buffer:
            return
        
        with self._lock:
            # Get all items from buffer
            items = list(self._buffer)
            self._buffer.clear()
        
        if not items:
            return
        
        # Save in batches
        batch_size = 100
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            self._save_telemetry_sync(batch)
    
    def record_telemetry(self, readings):
        """Add telemetry to buffer (non-blocking)."""
        if not readings:
            return
        
        with self._lock:
            for reading in readings:
                self._buffer.append(reading)
    
    def _save_telemetry_sync(self, readings):
        """Save telemetry to database synchronously."""
        if not readings:
            return
        
        session = None
        try:
            session = get_session()
            if session is None:
                return
            
            rows = [
                TelemetryDB(
                    asset_id=reading.asset_id,
                    sensor_type=reading.sensor_type.value if hasattr(reading.sensor_type, 'value') else str(reading.sensor_type),
                    value=float(reading.value) if hasattr(reading, 'value') else 0,
                    timestamp=getattr(reading, 'timestamp', datetime.now()),
                )
                for reading in readings
            ]
            
            TelemetryRepository(session).create_many(rows)
            
        except Exception as e:
            logger.exception(f"Failed to persist telemetry batch: {e}")
            # Put back in buffer if it fails
            with self._lock:
                for reading in readings:
                    self._buffer.append(reading)
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    def record_execution(self, event, report, severity="high"):
        """Save execution to database synchronously."""
        # Run in a separate thread to not block
        Thread(target=self._record_execution_sync, args=(event, report, severity), daemon=True).start()
    
    def _record_execution_sync(self, event, report, severity):
        """Sync version for execution."""
        session = None
        try:
            session = get_session()
            if session is None:
                return
            
            # Create incident
            incident = IncidentDB(
                id=getattr(event, 'id', 'unknown'),
                asset_id=getattr(event, 'source', 'unknown'),
                event=getattr(event, 'name', 'unknown'),
                severity=severity,
                status="completed" if getattr(report, 'success', False) else "requires_review",
                report=getattr(report, 'final_summary', ''),
                created_at=getattr(event, 'timestamp', datetime.now()),
            )
            IncidentRepository(session).create(incident)

            # Create execution report
            stored_report = ExecutionReportDB(
                id=getattr(report, 'id', 'unknown'),
                execution_id=getattr(report, 'execution_id', 'unknown'),
                incident_id=getattr(event, 'id', 'unknown'),
                workflow=getattr(report, 'workflow_name', 'unknown'),
                success=getattr(report, 'success', False),
                summary=getattr(report, 'final_summary', ''),
                recommendations=getattr(report, 'recommendations', []),
                started_at=getattr(report, 'started_at', datetime.now()),
                completed_at=getattr(report, 'completed_at', datetime.now()),
            )
            ReportRepository(session).create(stored_report)

            # Create agent results
            agent_results = getattr(report, 'agent_results', [])
            if agent_results:
                agent_rows = [
                    AgentExecutionDB(
                        id=getattr(result, 'id', 'unknown'),
                        incident_id=getattr(event, 'id', 'unknown'),
                        agent_name=getattr(result, 'agent_name', 'unknown'),
                        task=result.metadata.get("task_name", "") if hasattr(result, 'metadata') else "",
                        input=result.metadata.get("task_description", "") if hasattr(result, 'metadata') else "",
                        output=getattr(result, 'summary', ''),
                        success=getattr(result, 'success', False),
                        confidence=getattr(result, 'confidence', 0.0),
                        summary=getattr(result, 'summary', ''),
                        recommendations=getattr(result, 'recommendations', []),
                        decision=getattr(result, 'decision', ''),
                        evidence=getattr(result, 'evidence', []),
                        actions_required=getattr(result, 'actions_required', []),
                        requires_human_approval=getattr(result, 'requires_human_approval', False),
                        timestamp=getattr(result, 'timestamp', datetime.now()),
                    )
                    for result in agent_results
                ]
                AgentRepository(session).create_many(agent_rows)
            
            session.commit()
            
        except Exception as e:
            if session:
                session.rollback()
            logger.exception(f"Failed to persist execution: {e}")
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    def shutdown(self):
        """Shutdown the service and flush remaining data."""
        self._running = False
        self._flush_buffer()


# ✅ Singleton instance
_persistence = None


def get_persistence():
    """Get the singleton persistence service."""
    global _persistence
    if _persistence is None:
        _persistence = PersistenceService()
    return _persistence
```

## backend/services/refinery_generator.py

**Folder path:** `backend/services`

**File path:** `backend/services/refinery_generator.py`

```python
"""Generate multiple refineries with hundreds of assets."""

from typing import List, Dict
from models.asset import Asset, AssetType, Refinery
from uuid import uuid4
import random


class RefineryGenerator:
    """Generate realistic refinery assets for simulation."""

    REFINERY_NAMES = [
        "RigOS Alpha Refinery",
        "North Terminal Refinery",
        "South Coast Refinery",
        "East Valley Refinery",
        "West Port Refinery",
        "Central Hub Refinery",
        "Gulf Coast Refinery",
        "Pacific Refinery",
        "Atlantic Refinery",
        "Midwest Refinery",
    ]

    ZONES = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E", "Zone F"]

    PUMP_NAMES = ["Pump A", "Pump B", "Pump C", "Pump D", "Pump E", "Pump F", "Pump G", "Pump H"]
    COMPRESSOR_NAMES = ["Compressor C-01", "Compressor C-02", "Compressor C-03", "Compressor C-04"]
    VALVE_NAMES = ["Valve V-01", "Valve V-02", "Valve V-03", "Valve V-04", "Valve V-05"]
    HEAT_EXCHANGER_NAMES = ["HX-01", "HX-02", "HX-03", "HX-04"]
    TANK_NAMES = ["Tank T-01", "Tank T-02", "Tank T-03", "Tank T-04"]
    REACTOR_NAMES = ["Reactor R-01", "Reactor R-02"]
    PIPELINE_NAMES = ["Pipeline P-01", "Pipeline P-02", "Pipeline P-03"]

    @classmethod
    def generate_assets_for_refinery(cls, refinery_name: str, asset_count: int = 50) -> List[Asset]:
        """Generate assets for a refinery."""
        assets = []
        refinery_id = str(uuid4())

        # Determine how many of each type
        pumps = asset_count // 5
        compressors = asset_count // 10
        valves = asset_count // 8
        heat_exchangers = asset_count // 12
        tanks = asset_count // 15
        reactors = asset_count // 20
        pipelines = asset_count // 15
        others = asset_count - (pumps + compressors + valves + heat_exchangers + tanks + reactors + pipelines)

        # Generate Pumps
        for i in range(pumps):
            name = f"Pump {chr(65 + i % 26)}-{i // 26 + 1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.PUMP,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(70, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Compressors
        for i in range(compressors):
            name = f"Compressor C-{i+1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.COMPRESSOR,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(65, 98),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.6, 0.25, 0.1, 0.05])[0],
            ))

        # Generate Valves
        for i in range(valves):
            name = f"Valve V-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.VALVE,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(60, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.65, 0.25, 0.08, 0.02])[0],
            ))

        # Generate Heat Exchangers
        for i in range(heat_exchangers):
            name = f"HX-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.HEAT_EXCHANGER,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(50, 95),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.5, 0.25, 0.15, 0.1])[0],
            ))

        # Generate Tanks
        for i in range(tanks):
            name = f"Tank T-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.TANK,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(70, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Reactors
        for i in range(reactors):
            name = f"Reactor R-{i+1:02d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.REACTOR,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(60, 95),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.55, 0.25, 0.15, 0.05])[0],
            ))

        # Generate Pipelines
        for i in range(pipelines):
            name = f"Pipeline P-{i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=AssetType.PIPELINE,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(65, 100),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.7, 0.2, 0.08, 0.02])[0],
            ))

        # Generate Other assets
        other_types = [AssetType.MOTOR, AssetType.GENERATOR, AssetType.BOILER, AssetType.TURBINE, AssetType.DISTILLATION_COLUMN]
        for i in range(others):
            asset_type = random.choice(other_types)
            name = f"{asset_type.value} {i+1:03d}"
            assets.append(Asset(
                name=name,
                asset_type=asset_type,
                refinery_id=refinery_id,
                location=refinery_name,
                zone=random.choice(cls.ZONES),
                health=random.uniform(60, 98),
                status=random.choices(["Running", "Healthy", "Warning", "Critical"], weights=[0.6, 0.25, 0.1, 0.05])[0],
            ))

        return assets

    @classmethod
    def generate_refineries(cls, count: int = 5, assets_per_refinery: int = 50) -> List[Refinery]:
        """Generate multiple refineries with assets."""
        refineries = []
        selected_names = random.sample(cls.REFINERY_NAMES, min(count, len(cls.REFINERY_NAMES)))

        for name in selected_names:
            assets = cls.generate_assets_for_refinery(name, assets_per_refinery)
            refineries.append(Refinery(
                id=str(uuid4()),
                name=name,
                location=random.choice(["Texas", "Louisiana", "California", "Alaska", "Oklahoma", "Alberta"]),
                assets=assets,
                status=random.choices(["Active", "Active", "Active", "Maintenance"])[0],
            ))

        return refineries
```

## backend/services/report.py

**Folder path:** `backend/services`

**File path:** `backend/services/report.py`

```python

```

## backend/services/revenue_impact_calculator.py

**Folder path:** `backend/services`

**File path:** `backend/services/revenue_impact_calculator.py`

```python
"""Revenue impact calculation service."""

from typing import Dict, Optional
from services.ai_config import AIConfigGenerator


class RevenueService:
    """Calculate revenue impact based on asset health and incidents."""
    
    _instance = None
    
    # Revenue per asset per day (in $)
    ASSET_REVENUE = {
        "Pump": 5000,
        "Compressor": 8000,
        "Tank": 3000,
        "Valve": 2000,
        "Pipeline": 6000,
        "Heat Exchanger": 7000,
        "Reactor": 12000,
        "Boiler": 9000,
        "Turbine": 15000,
        "Motor": 4000,
        "Generator": 10000,
        "Distillation Column": 20000,
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_asset_revenue(self, asset_type: str) -> float:
        """Get daily revenue for an asset type."""
        return self.ASSET_REVENUE.get(asset_type, 5000)
    
    def calculate_asset_health_impact(self, asset_health: float, asset_type: str, 
                                       failure_probability: float, rul_days: float) -> Dict:
        """Calculate revenue impact for a single asset."""
        daily_revenue = self.get_asset_revenue(asset_type)
        
        # Health factor (0-1)
        health_factor = asset_health / 100.0
        
        # Degradation factor
        degradation_factor = max(0, min(1, (100 - asset_health) / 50))
        
        # Current revenue contribution
        current_revenue = daily_revenue * health_factor
        
        # Projected revenue loss
        projected_loss = daily_revenue * degradation_factor * 0.3
        
        # If failure is imminent (RUL < 30 days)
        if rul_days < 30:
            failure_loss = daily_revenue * (1 - health_factor) * 0.5
        else:
            failure_loss = 0
        
        total_impact = projected_loss + failure_loss
        
        return {
            "daily_revenue": daily_revenue,
            "current_contribution": round(current_revenue, 2),
            "projected_loss": round(projected_loss, 2),
            "failure_loss": round(failure_loss, 2),
            "total_impact": round(total_impact, 2),
            "health_factor": round(health_factor, 3),
            "degradation_factor": round(degradation_factor, 3),
        }
    
    def calculate_company_revenue_impact(self, assets: list) -> Dict:
        """Calculate total revenue impact across all assets."""
        total_revenue = 0
        total_current = 0
        total_projected_loss = 0
        total_failure_loss = 0
        total_health = 0
        
        for asset in assets:
            asset_type = asset.get("type", "Pump")
            health = asset.get("health", 100)
            failure_prob = asset.get("failure_probability", 0)
            rul = asset.get("rul_days", 365)
            
            result = self.calculate_asset_health_impact(
                health, asset_type, failure_prob, rul
            )
            
            total_revenue += result["daily_revenue"]
            total_current += result["current_contribution"]
            total_projected_loss += result["projected_loss"]
            total_failure_loss += result["failure_loss"]
            total_health += health
        
        avg_health = total_health / len(assets) if assets else 0
        
        return {
            "total_potential_revenue": round(total_revenue, 2),
            "current_revenue": round(total_current, 2),
            "projected_loss": round(total_projected_loss, 2),
            "failure_loss": round(total_failure_loss, 2),
            "total_impact": round(total_projected_loss + total_failure_loss, 2),
            "avg_health": round(avg_health, 1),
            "revenue_efficiency": round((total_current / total_revenue) * 100 if total_revenue else 0, 1),
        }
    
    def calculate_incident_impact(self, incident_type: str, asset_type: str, 
                                   duration_hours: float = 4) -> Dict:
        """Calculate revenue impact of a specific incident."""
        daily_revenue = self.get_asset_revenue(asset_type)
        
        # Incident severity multipliers
        severity_multipliers = {
            "Pressure Spike": 0.3,
            "High Temperature": 0.25,
            "Gas Leak": 0.5,
            "High Vibration": 0.2,
            "Flow Restriction": 0.15,
        }
        
        multiplier = severity_multipliers.get(incident_type, 0.2)
        
        # Revenue loss = daily_revenue * (duration/24) * multiplier
        revenue_loss = daily_revenue * (duration_hours / 24) * multiplier
        
        return {
            "incident_type": incident_type,
            "duration_hours": duration_hours,
            "daily_revenue": daily_revenue,
            "revenue_loss": round(revenue_loss, 2),
            "severity_multiplier": multiplier,
        }


# Singleton
revenue_service = RevenueService()
```

## backend/services/runtime.py

**Folder path:** `backend/services`

**File path:** `backend/services/runtime.py`

```python
"""Runtime module - lazy initialization with auto-start simulation."""

import time
import threading
from mao import MAOKernel
from models.asset import Asset, AssetType
from models.facility import Facility
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
from services.refinery_generator import RefineryGenerator

# Global instances
_kernel = None
_simulator = None
_refineries = None
_vector_store = None
_initialized = False
_simulation_thread = None
_simulation_running = False


def get_kernel():
    """Lazy-initialize and return the shared MAO kernel."""
    global _kernel, _initialized
    if _kernel is None:
        _kernel = _initialize_kernel()
        _initialized = True
    return _kernel


def is_initialized():
    """Check if kernel is already initialized."""
    return _initialized


def get_simulator():
    """Lazy-initialize and return the shared simulator."""
    global _simulator
    if _simulator is None:
        _simulator = _initialize_simulator()
    return _simulator


def _initialize_kernel():
    """Initialize the MAO kernel with all agents and workflows."""
    print("🚀 Initializing MAO Kernel...")
    start = time.time()
    
    # ✅ Generate AI configuration ONCE on startup
    try:
        from services.ai_config import AIConfigGenerator
        ai_config = AIConfigGenerator()
        print("✅ AI Configuration generated successfully")
    except Exception as e:
        print(f"⚠️ AI Config generation failed: {e}")
    
    kernel = MAOKernel()
    
    # Register workflows
    for workflow in (
        PressureWorkflow(),
        TemperatureWorkflow(),
        GasWorkflow(),
        FlowWorkflow(),
        MaintenanceWorkflow(),
    ):
        kernel.register_workflow(workflow)
    
    # Initialize vector store
    global _vector_store
    try:
        embedder = Embedder()
        _vector_store = NeonVectorStore(embedder.get_model())
        print("✅ Vector store initialized")
    except Exception as e:
        print(f"⚠️ Vector store failed: {e}")
        _vector_store = None
    
    # Register all agents
    for agent in (
        SafetyAgent(),
        KnowledgeAgent(_vector_store),
        MaintenanceAgent(),
        DiagnosticAgent(),
        PlanningAgent(),
        SensorAgent(),
        PredictionAgent(),
        NotificationAgent(),
        ReportAgent(),
    ):
        kernel.register_agent(agent)
    
    # Generate refineries
    global _refineries
    _refineries = RefineryGenerator.generate_refineries(count=5, assets_per_refinery=50)
    
    for refinery in _refineries:
        for asset in refinery.assets:
            kernel.asset_service.register(asset)
    
    kernel._refineries = _refineries
    
    elapsed = time.time() - start
    print(f"✅ Kernel initialized in {elapsed:.2f}s with {sum(len(r.assets) for r in _refineries)} assets")
    
    # Persist to database
    _persist_assets_to_database(kernel)
    
    # ✅ AUTO-START SIMULATION (but don't block)
    _start_auto_simulation(kernel)
    
    return kernel


def _start_auto_simulation(kernel):
    """Start the simulation automatically in background."""
    global _simulation_thread, _simulation_running
    
    if _simulation_running:
        return
    
    _simulation_running = True
    _simulation_thread = threading.Thread(
        target=_auto_simulation_loop,
        args=(kernel,),
        daemon=True
    )
    _simulation_thread.start()
    print("✅ Auto-simulation started in background")


def _auto_simulation_loop(kernel):
    """Background thread that runs the simulation automatically - 15-45s intervals."""
    import random
    
    from simulator.simulator import Simulator
    from simulator.facility import SimulatedFacility
    
    # ✅ Create simulator
    all_assets = []
    for refinery in _refineries:
        all_assets.extend(refinery.assets)
    
    facility = Facility(
        id="rigos-alpha",
        name="RigOS Global",
        assets=all_assets
    )
    
    simulated_facility = SimulatedFacility(facility)
    simulator = Simulator(
        facility=simulated_facility,
        kernel=kernel
    )
    
    tick = 0
    incident_counter = 0
    
    # ✅ WARM-UP - 30 seconds with no faults
    print("🔄 Simulation warming up (30 seconds)...")
    try:
        for _ in range(30):
            tick += 1
            telemetry, reports = simulator.tick(tick)
            for reading in telemetry:
                kernel.state.add_telemetry([reading])
            for asset in simulated_facility.assets:
                history = kernel.state.get_history(asset.asset.id)
                if history:
                    health = kernel.health.calculate_health(history)
                    kernel.asset_service.update_health(asset.asset.id, health)
            time.sleep(1.0)
    except Exception as e:
        print(f"⚠️ Warm-up error: {e}")
    
    print("✅ Simulation running. Incidents every 15-45 seconds.")
    
    # ✅ Run with timer-based incidents
    while _simulation_running:
        try:
            # ✅ Generate random wait time (15-45 seconds)
            wait_time = random.randint(15, 45)
            print(f"⏳ Next incident in {wait_time} seconds...")
            
            # ✅ Wait for the interval (with regular ticks)
            for _ in range(wait_time):
                if not _simulation_running:
                    break
                tick += 1
                try:
                    telemetry, reports = simulator.tick(tick)
                except RuntimeError as e:
                    if "cannot schedule new futures" in str(e):
                        print("⚠️ Persistence pool shutdown, continuing...")
                        # Retry without persistence
                        telemetry, reports = simulator.tick(tick)
                    else:
                        raise
                
                # ✅ Update state
                for reading in telemetry:
                    kernel.state.add_telemetry([reading])
                
                for asset in simulated_facility.assets:
                    history = kernel.state.get_history(asset.asset.id)
                    if history:
                        health = kernel.health.calculate_health(history)
                        kernel.asset_service.update_health(asset.asset.id, health)
                
                for report in reports:
                    kernel.state.add_report(report)
                    for result in report.agent_results:
                        kernel.state.add_agent_result(result)
                
                time.sleep(1.0)
            
            if not _simulation_running:
                break
            
            # ✅ TRIGGER INCIDENT
            if all_assets:
                asset = random.choice(all_assets)
                sensor_types = ["pressure", "temperature", "vibration", "gas", "flow"]
                sensor = random.choice(sensor_types)
                
                fault_values = {
                    "pressure": {"sensor": "pressure", "value": random.randint(155, 180)},
                    "temperature": {"sensor": "temperature", "value": random.randint(90, 110)},
                    "vibration": {"sensor": "vibration", "value": random.randint(12, 20)},
                    "gas": {"sensor": "gas", "value": random.randint(45, 70)},
                    "flow": {"sensor": "flow", "value": random.randint(10, 20)},
                }
                
                fault = fault_values[sensor]
                incident_counter += 1
                print(f"💥 [#{incident_counter}] {sensor.upper()} fault on {asset.name} (value: {fault['value']})")
                
                # ✅ Inject fault
                try:
                    for sim_asset in simulated_facility.assets:
                        if sim_asset.asset.id == asset.id:
                            telemetry, reports = simulator.tick(tick, fault, target_asset_id=asset.id)
                            break
                    else:
                        telemetry, reports = simulator.tick(tick)
                except RuntimeError as e:
                    if "cannot schedule new futures" in str(e):
                        print("⚠️ Persistence error during fault injection, continuing...")
                        continue
                    else:
                        raise
                
                # ✅ Process incident
                for reading in telemetry:
                    kernel.state.add_telemetry([reading])
                
                for asset_obj in simulated_facility.assets:
                    history = kernel.state.get_history(asset_obj.asset.id)
                    if history:
                        health = kernel.health.calculate_health(history)
                        kernel.asset_service.update_health(asset_obj.asset.id, health)
                
                for report in reports:
                    kernel.state.add_report(report)
                    for result in report.agent_results:
                        kernel.state.add_agent_result(result)
            
        except Exception as e:
            print(f"⚠️ Simulation error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(2)


def _persist_assets_to_database(kernel):
    """Persist all assets and refineries to database."""
    try:
        from database.connection import get_session
        from database.models import AssetDB
        from database.repositories.asset_repo import AssetRepository
        
        session = get_session()
        repo = AssetRepository(session)
        
        existing = repo.get_all()
        if not existing or len(existing) == 0:
            count = 0
            for refinery in kernel._refineries:
                for asset in refinery.assets:
                    asset_db = AssetDB(
                        id=asset.id,
                        name=asset.name,
                        asset_type=asset.asset_type.value if hasattr(asset.asset_type, 'value') else str(asset.asset_type),
                        location=refinery.name,
                        health=asset.health,
                        status=asset.status,
                    )
                    session.add(asset_db)
                    count += 1
            session.commit()
            print(f"✅ Persisted {count} assets to database")
        else:
            print(f"✅ Assets already exist in database ({len(existing)} found)")
        
        session.close()
    except Exception as e:
        print(f"⚠️ Could not persist assets to database: {e}")


def _initialize_simulator():
    """Initialize the simulator with all assets."""
    from simulator.facility import SimulatedFacility
    from simulator.simulator import Simulator
    
    kernel = get_kernel()
    
    all_assets = []
    for refinery in _refineries:
        all_assets.extend(refinery.assets)
    
    facility = Facility(
        id="rigos-alpha",
        name="RigOS Global",
        assets=all_assets
    )
    
    simulated_facility = SimulatedFacility(facility)
    simulator = Simulator(
        facility=simulated_facility,
        kernel=kernel
    )
    
    return simulator


# ✅ Runtime proxy for lazy loading
class _RuntimeProxy:
    @property
    def kernel(self):
        return get_kernel()
    
    @property
    def simulator(self):
        return get_simulator()


# ✅ Export runtime - the single entry point
runtime = _RuntimeProxy()
```

## backend/services/sensor.py

**Folder path:** `backend/services`

**File path:** `backend/services/sensor.py`

```python

```

## backend/services/simulation.py

**Folder path:** `backend/services`

**File path:** `backend/services/simulation.py`

```python

```

## backend/services/simulator_controller.py

**Folder path:** `backend/services`

**File path:** `backend/services/simulator_controller.py`

```python
"""Optimized Simulator controller - NO circular imports."""

import threading
import time
from typing import Dict, List, Optional, Any


class SimulatorController:
    """Controls the simulation lifecycle with UI integration and auto-refresh."""

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.tick_count = 0
        self._latest_telemetry: List[Any] = []
        self._latest_reports: List[Any] = []
        self._config_refresh_interval = 30
        self._simulator = None
        self._kernel = None

    @property
    def simulator(self):
        """Lazy load simulator."""
        if self._simulator is None:
            from services.runtime import get_simulator
            self._simulator = get_simulator()
        return self._simulator

    @property
    def kernel(self):
        """Lazy load kernel."""
        if self._kernel is None:
            from services.runtime import get_kernel
            self._kernel = get_kernel()
        return self._kernel

    def start(self, interval: float = 1.0):
        if self.running:
            return

        self.running = True
        self.kernel._simulation_running = True
        self._thread = threading.Thread(
            target=self._run,
            args=(interval,),
            daemon=True
        )
        self._thread.start()
        print(f"✅ Simulation started with interval {interval}s")

    def stop(self):
        self.running = False
        self.kernel._simulation_running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("⏹️ Simulation stopped")

    def step(self) -> tuple[List[Any], List[Any]]:
        self.tick_count += 1
        
        if self.tick_count % self._config_refresh_interval == 0:
            self._refresh_config()
        
        telemetry, reports = self.simulator.tick(self.tick_count)
        self._latest_telemetry = telemetry
        self._latest_reports = reports
        return telemetry, reports

    def _run(self, interval: float):
        while self.running:
            try:
                self.step()
            except Exception as e:
                print(f"⚠️ Simulation error: {e}")
                continue
            time.sleep(interval)

    def _refresh_config(self):
        try:
            from services.config_services import ConfigService
            ConfigService().clear_cache()
            
            from simulator.event_generator import EventGenerator
            EventGenerator().clear_cache()
            
            print(f"🔄 [Tick {self.tick_count}] Refreshed Gemini configuration")
        except Exception as e:
            print(f"⚠️ Config refresh failed: {e}")

    def get_latest_telemetry(self) -> List[Any]:
        return self._latest_telemetry

    def get_latest_reports(self) -> List[Any]:
        return self._latest_reports

    def get_status(self) -> Dict:
        return {
            "running": self.running,
            "ticks": self.tick_count,
            "assets": len(self.kernel.asset_service.all_assets()),
            "events": len(self.kernel.event_store.all()),
            "reports": len(self.kernel.state.execution_reports),
            "agent_results": len(self.kernel.state.agent_results),
        }


sim_controller = SimulatorController()
```

## backend/services/telemetry_store.py

**Folder path:** `backend/services`

**File path:** `backend/services/telemetry_store.py`

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

## backend/services/vision.py

**Folder path:** `backend/services`

**File path:** `backend/services/vision.py`

```python

```

## backend/services/weather.py

**Folder path:** `backend/services`

**File path:** `backend/services/weather.py`

```python

```

## backend/simulator/asset.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/asset.py`

```python
import random
import math
from models.asset import Asset
from models.sensor import Sensor, SensorType


class SimulatedAsset:
    def __init__(self, asset: Asset):
        self.asset = asset
        
        # ✅ Base values with realistic ranges - STABLE by default
        self.sensors = {
            SensorType.PRESSURE: 105.0 + random.uniform(-5, 5),   # Stable around 100-110
            SensorType.TEMPERATURE: 72.0 + random.uniform(-3, 3), # Stable around 69-75
            SensorType.FLOW: 55.0 + random.uniform(-5, 5),        # Stable around 50-60
            SensorType.VIBRATION: 3.0 + random.uniform(-0.5, 0.5),# Stable around 2.5-3.5
            SensorType.GAS: 2.0 + random.uniform(-0.3, 0.3),      # Stable around 1.7-2.3
        }
        
        # ✅ Very slow trend changes
        self.trends = {
            SensorType.PRESSURE: 0,
            SensorType.TEMPERATURE: 0,
            SensorType.FLOW: 0,
            SensorType.VIBRATION: 0,
            SensorType.GAS: 0,
        }
        
        self.degradation = 0.0
        self._fault_active = False
        self._fault_sensor = None
        self._fault_ticks = 0
        self._fault_original_value = None
        self._trend_counter = 0  # ✅ Track how long since last trend change

    def tick(self, fault=None):
        """Generate telemetry for one tick."""
        telemetry = []
        
        # ✅ Handle fault
        if fault and not self._fault_active:
            self._fault_active = True
            self._fault_sensor = fault["sensor"]
            self._fault_original_value = self.sensors.get(fault["sensor"], 100)
            self._fault_ticks = 0
        
        for sensor_type, base_value in self.sensors.items():
            value = base_value
            
            # ✅ Apply active fault
            if self._fault_active and sensor_type == self._fault_sensor:
                self._fault_ticks += 1
                
                # ✅ Fault decays back to normal over 5-8 ticks
                decay_factor = max(0, 1 - (self._fault_ticks / 8))
                if self._fault_original_value:
                    target_value = self._fault_original_value * (1 + random.uniform(-0.03, 0.03))
                    value = target_value + (self._fault_original_value * 0.3 * decay_factor)
                    
                    # ✅ Clamp to realistic range
                    if sensor_type == SensorType.PRESSURE:
                        value = min(160, max(90, value))
                    elif sensor_type == SensorType.TEMPERATURE:
                        value = min(95, max(60, value))
                    elif sensor_type == SensorType.VIBRATION:
                        value = min(12, max(2, value))
                    
                    # ✅ If decayed enough, deactivate fault
                    if self._fault_ticks > 8 or abs(value - self._fault_original_value) < 2:
                        self._fault_active = False
                        self._fault_sensor = None
                        self._fault_original_value = None
                        value = self._fault_original_value if self._fault_original_value else base_value
                else:
                    value = base_value
                    self._fault_active = False
            
            else:
                # ✅ Normal variation - VERY STABLE
                # Change trend direction only occasionally
                self._trend_counter += 1
                if self._trend_counter > random.randint(10, 30):  # Change every 10-30 ticks
                    self.trends[sensor_type] = random.choice([-1, 0, 1])
                    self._trend_counter = 0
                
                # ✅ Apply trend very slowly
                value += self.trends[sensor_type] * random.uniform(0.02, 0.08)  # Very slow change
                
                # ✅ Add tiny natural noise
                value += random.gauss(0, 0.2)  # Very small noise
                
                # ✅ Keep within realistic ranges
                ranges = {
                    SensorType.PRESSURE: (90, 150),
                    SensorType.TEMPERATURE: (60, 90),
                    SensorType.FLOW: (30, 80),
                    SensorType.VIBRATION: (1, 8),
                    SensorType.GAS: (1, 5),
                }
                min_val, max_val = ranges.get(sensor_type, (0, 100))
                value = max(min_val, min(max_val, value))
            
            # ✅ Store updated value
            self.sensors[sensor_type] = value
            
            # ✅ Create telemetry reading
            telemetry.append(
                Sensor(
                    id=f"{self.asset.id}_{sensor_type.value}",
                    asset_id=self.asset.id,
                    sensor_type=sensor_type,
                    value=round(value, 2),
                    unit=self._get_unit(sensor_type),
                )
            )
        
        return telemetry

    def _get_unit(self, sensor_type):
        units = {
            SensorType.PRESSURE: "PSI",
            SensorType.TEMPERATURE: "°C",
            SensorType.FLOW: "L/min",
            SensorType.VIBRATION: "mm/s",
            SensorType.GAS: "ppm",
        }
        return units.get(sensor_type, "")
```

## backend/simulator/event_generator.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/event_generator.py`

```python
"""Optimized event generator - ONLY generates events from injected faults."""

from mao.events.event import Event


class EventGenerator:
    
    def __init__(self):
        self._faults = []  # Store injected faults

    def add_fault(self, fault, asset_id, asset_type):
        """Add a fault that will generate an event."""
        self._faults.append({
            "fault": fault,
            "asset_id": asset_id,
            "asset_type": asset_type
        })

    def generate(self, telemetry):
        """
        ✅ ONLY generate events from injected faults.
        No auto-detection from telemetry.
        """
        events = []
        
        if not self._faults:
            return events
        
        # Process each fault
        for fault_data in self._faults:
            fault = fault_data["fault"]
            asset_id = fault_data["asset_id"]
            asset_type = fault_data["asset_type"]
            
            sensor = fault.get("sensor", "")
            value = fault.get("value", 0)
            
            # Map sensor to event name
            event_map = {
                "pressure": "PressureSpike",
                "temperature": "HighTemperature",
                "vibration": "HighVibration",
                "gas": "GasLeak",
                "flow": "FlowRestriction",
            }
            
            event_name = event_map.get(sensor, "Unknown")
            
            event = Event(
                name=event_name,
                source=asset_id,
                payload={sensor: value, "asset_type": asset_type}
            )
            events.append(event)
        
        # Clear faults after generating
        self._faults = []
        
        return events
    
    def clear_cache(self):
        """Clear all stored faults."""
        self._faults = []
```

## backend/simulator/facility.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/facility.py`

```python
from models.facility import Facility
from simulator.asset import SimulatedAsset
from models.sensor import SensorType


class SimulatedFacility:
    def __init__(self, facility: Facility):
        self.assets = [
            SimulatedAsset(asset)
            for asset in facility.assets
        ]
        self.active_faults = {}

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Generate telemetry with optional targeted fault."""
        telemetry = []
        
        for asset in self.assets:
            current_fault = None
            
            # ✅ Check if this asset has an active fault
            if target_asset_id and asset.asset.id == target_asset_id:
                if fault:
                    current_fault = fault
                    self.active_faults[asset.asset.id] = {
                        "sensor": fault.get("sensor"),
                        "value": fault.get("value"),
                        "tick": tick_number,
                        "active": True
                    }
            elif asset.asset.id in self.active_faults:
                fault_data = self.active_faults[asset.asset.id]
                if fault_data.get("active", False):
                    ticks_active = tick_number - fault_data.get("tick", tick_number)
                    # ✅ Fault lasts 5 ticks then auto-resolves
                    if ticks_active > 5:
                        fault_data["active"] = False
                        print(f"✅ Fault resolved for {asset.asset.name} after {ticks_active} ticks")
                    else:
                        current_fault = {
                            "sensor": fault_data.get("sensor"),
                            "value": fault_data.get("value")
                        }
            
            telemetry.extend(asset.tick(fault=current_fault))
        
        return telemetry
```

## backend/simulator/fault_injector.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/fault_injector.py`

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

## backend/simulator/sensor.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/sensor.py`

```python

```

## backend/simulator/simulator.py

**Folder path:** `backend/simulator`

**File path:** `backend/simulator/simulator.py`

```python
"""Simulator with proper incident cooldown and rate limiting."""

import random
from datetime import datetime
from uuid import uuid4
import time

from services.computation_engine import ComputationEngine
from services.revenue_impact_calculator import revenue_service
from services.maintenance_scheduler import maintenance_scheduler
from services.ai_config import AIConfigGenerator


class Simulator:
    def __init__(self, facility, kernel):
        self.facility = facility
        self.kernel = kernel
        self.state = kernel.state
        
        # ✅ Lazy load these
        self.generator = None
        self.persistence = None
        self.computation_engine = ComputationEngine()
        self.notification_service = None
        self.config = AIConfigGenerator()
        
        # ✅ Track active incidents with proper cooldown
        self.active_incidents = {}        # asset_id -> incident_data
        self.resolved_incidents = {}      # asset_id -> resolution_tick
        self._incident_cooldown_ticks = 20  # ✅ 20 ticks cooldown
        self._last_incident_time = 0
        self.incident_resolution_count = 0
        self._notification_sent = {}
        self._incident_count = 0

    def _get_generator(self):
        if self.generator is None:
            from simulator.event_generator import EventGenerator
            self.generator = EventGenerator()
        return self.generator

    def _get_persistence(self):
        if self.persistence is None:
            from services.persistence import get_persistence
            self.persistence = get_persistence()
        return self.persistence

    def _get_notification_service(self):
        if self.notification_service is None:
            from services.notification_service import NotificationService, Notification, NotificationType, NotificationSeverity
            self._Notification = Notification
            self._NotificationType = NotificationType
            self._NotificationSeverity = NotificationSeverity
            self.notification_service = NotificationService()
        return self.notification_service

    def tick(self, tick_number, fault=None, target_asset_id=None):
        """Run one simulation tick."""
        
        # Generate telemetry
        telemetry = self.facility.tick(tick_number, fault, target_asset_id)
        self.state.add_telemetry(telemetry)
        
        # ✅ Use the fixed persistence
        try:
            self._get_persistence().record_telemetry(telemetry)
        except Exception as e:
            # Log but don't crash the simulation
            print(f"⚠️ Telemetry save failed: {e}")
        
        # Update asset health
        for asset in self.facility.assets:
            history = self.state.get_history(asset.asset.id)
            if history:
                metrics = self.computation_engine.compute_asset(asset.asset, history)
                self.kernel.asset_service.update_health(asset.asset.id, metrics["health"])
                self.kernel.asset_service.update_status(asset.asset.id, metrics["status"])
        
        # ... rest of code

        # Update asset health
        for asset in self.facility.assets:
            history = self.state.get_history(asset.asset.id)
            if history:
                metrics = self.computation_engine.compute_asset(asset.asset, history)
                self.kernel.asset_service.update_health(asset.asset.id, metrics["health"])
                self.kernel.asset_service.update_status(asset.asset.id, metrics["status"])

        # ✅ Add injected fault to generator if present
        if fault and target_asset_id:
            asset = self.kernel.asset_service.get(target_asset_id)
            asset_type = asset.asset_type.value if asset and hasattr(asset.asset_type, 'value') else "Pump"
            self._get_generator().add_fault(fault, target_asset_id, asset_type)

        # ✅ Process events - ONLY from injected faults
        reports = []
        events = self._get_generator().generate(telemetry)
        
        for event in events:
            asset_id = event.source
            
            # ✅ Check if asset is in cooldown
            if asset_id in self.resolved_incidents:
                resolved_tick = self.resolved_incidents[asset_id]
                if tick_number - resolved_tick < self._incident_cooldown_ticks:
                    continue  # ✅ Skip during cooldown
                else:
                    del self.resolved_incidents[asset_id]
            
            # ✅ Check if incident already active
            if asset_id in self.active_incidents:
                # ✅ Check if values normalized
                if self._check_values_normalized(asset_id):
                    asset = self.kernel.asset_service.get(asset_id)
                    asset_name = asset.name if asset else asset_id
                    self._resolve_incident(asset_id, tick_number, asset_name)
                    self.resolved_incidents[asset_id] = tick_number
                continue  # ✅ Don't trigger new incident
            
            # ✅ TRIGGER NEW INCIDENT
            asset = self.kernel.asset_service.get(asset_id)
            asset_name = asset.name if asset else asset_id
            report = self._trigger_incident(event, asset, asset_name, tick_number)
            if report:
                reports.append(report)

        return telemetry, reports

    def _can_trigger_for_asset(self, asset_id, tick_number):
        """Check if an asset can have a new incident."""
        if asset_id in self.resolved_incidents:
            resolved_tick = self.resolved_incidents[asset_id]
            if tick_number - resolved_tick < self._incident_cooldown_ticks:
                return False
            else:
                del self.resolved_incidents[asset_id]
        
        if asset_id in self.active_incidents:
            return False
        
        return True

    def _trigger_incident(self, event, asset, asset_name, tick_number):
        """Trigger a new incident."""
        
        asset_id = event.source
        asset_type = asset.asset_type.value if asset and hasattr(asset.asset_type, 'value') else "Pump"
        
        # ✅ Store active incident
        self.active_incidents[asset_id] = {
            "event": event,
            "start_time": datetime.now(),
            "tick": tick_number,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "resolved": False,
        }
        
        self._last_incident_time = tick_number
        self._notification_sent[asset_id] = False
        
        # ✅ Run MAO agents
        report = self.kernel.handle_event(event)
        self._incident_count += 1
        
        # ✅ Send notifications (only once)
        self._send_notifications(event, asset_name, asset_id, asset_type)
        
        print(f"🚨 Incident #{self._incident_count}: {event.name} on {asset_name}")
        
        return report

    def _send_notifications(self, event, asset_name, asset_id, asset_type):
        """Send notifications for an incident (only once)."""
        
        if self._notification_sent.get(asset_id, False):
            return
        
        self._notification_sent[asset_id] = True
        
        notification_service = self._get_notification_service()
        Notification = self._Notification
        NotificationType = self._NotificationType
        NotificationSeverity = self._NotificationSeverity
        
        # ✅ Incident detected
        notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.INCIDENT_DETECTED,
                severity=NotificationSeverity.CRITICAL,
                title=f"🚨 {event.name}",
                message=f"{asset_name}",
                asset_id=asset_id,
                asset_name=asset_name,
                incident_type=event.name,
            )
        )
        
        # ✅ Revenue impact
        impact = revenue_service.calculate_incident_impact(event.name, asset_type, duration_hours=2)
        notification_service.add_notification(
            Notification(
                id=str(uuid4()),
                type=NotificationType.REVENUE_IMPACT,
                severity=NotificationSeverity.WARNING if impact['revenue_loss'] > 1000 else NotificationSeverity.INFO,
                title="💰 Revenue Impact",
                message=f"${impact['revenue_loss']:,.0f}",
                asset_id=asset_id,
                asset_name=asset_name,
                revenue_impact=impact['revenue_loss'],
            )
        )

    def _resolve_incident(self, asset_id, tick_number, asset_name):
        """Resolve an active incident."""
        if asset_id in self.active_incidents:
            self.incident_resolution_count += 1
            
            notification_service = self._get_notification_service()
            Notification = self._Notification
            NotificationType = self._NotificationType
            NotificationSeverity = self._NotificationSeverity
            
            # ✅ Send resolution notification
            notification_service.add_notification(
                Notification(
                    id=str(uuid4()),
                    type=NotificationType.INCIDENT_RESOLVED,
                    severity=NotificationSeverity.SUCCESS,
                    title="✅ Resolved",
                    message=asset_name,
                    asset_id=asset_id,
                    asset_name=asset_name,
                )
            )
            
            # ✅ Remove from active incidents
            del self.active_incidents[asset_id]
            
            print(f"✅ Resolved: {asset_name}")

    def _check_values_normalized(self, asset_id):
        """Check if telemetry values have returned to normal range."""
        history = self.state.get_history(asset_id)
        if not history:
            return True
        
        recent = history[-5:]
        violations = 0
        
        for reading in recent:
            asset = self.kernel.asset_service.get(asset_id)
            asset_type = asset.asset_type.value if asset and hasattr(asset.asset_type, 'value') else "Pump"
            thresholds = self.config.get_thresholds(asset_type)
            
            sensor_type = reading.sensor_type.value if hasattr(reading.sensor_type, 'value') else str(reading.sensor_type)
            
            if sensor_type == "Pressure":
                if reading.value > thresholds.get("pressure_max", 150) * 0.85:
                    violations += 1
            elif sensor_type == "Temperature":
                if reading.value > thresholds.get("temperature_max", 85) * 0.85:
                    violations += 1
            elif sensor_type == "Vibration":
                if reading.value > thresholds.get("vibration_max", 8) * 0.85:
                    violations += 1
            elif sensor_type == "Gas":
                if reading.value > thresholds.get("gas_max", 40) * 0.85:
                    violations += 1
            elif sensor_type == "Flow":
                if reading.value < thresholds.get("flow_min", 25) * 1.15:
                    violations += 1
        
        return violations < 2
```

## backend/test_db.py

**Folder path:** `backend`

**File path:** `backend/test_db.py`

```python
"""Check if tables exist in database."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from database.connection import engine
from sqlalchemy import inspect, text

print("=" * 50)
print("🔍 Checking database tables")
print("=" * 50)

# Test connection first
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print("✅ Connected to:", result.fetchone()[0][:50])
        result = conn.execute(text("SELECT current_database(), current_user"))
        db, user = result.fetchone()
        print(f"✅ Database: {db}, User: {user}")
except Exception as e:
    print("❌ Connection failed:", e)
    sys.exit(1)

# Check if vector extension exists
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
        if result.fetchone():
            print("✅ pgvector extension: INSTALLED")
        else:
            print("❌ pgvector extension: NOT INSTALLED")
except Exception as e:
    print("⚠️ Could not check pgvector:", e)

# List all tables
print("\n📊 Tables in database:")
inspector = inspect(engine)
tables = inspector.get_table_names()

if tables:
    print(f"   Found {len(tables)} table(s):")
    for t in sorted(tables):
        # Get column count for each table
        columns = inspector.get_columns(t)
        print(f"   - {t} ({len(columns)} columns)")
else:
    print("   ❌ No tables found!")

# Check specific tables we need
print("\n🔍 Checking required tables:")
required_tables = ['assets', 'telemetry', 'incidents', 'agent_execution', 'execution_reports', 'knowledge']

for table in required_tables:
    if table in tables:
        print(f"   ✅ {table}: EXISTS")
    else:
        print(f"   ❌ {table}: MISSING")

print("\n" + "=" * 50)
```

## frontend/.gitignore

**Folder path:** `frontend`

**File path:** `frontend/.gitignore`

```
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

## frontend/eslint.config.js

**Folder path:** `frontend`

**File path:** `frontend/eslint.config.js`

```javascript
import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])
```

## frontend/index.html

**Folder path:** `frontend`

**File path:** `frontend/index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## frontend/package-lock.json

**Folder path:** `frontend`

**File path:** `frontend/package-lock.json`

```json
{
  "name": "frontend",
  "version": "0.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "frontend",
      "version": "0.0.0",
      "dependencies": {
        "@emotion/react": "^11.14.0",
        "@emotion/styled": "^11.14.1",
        "@mui/icons-material": "^9.2.0",
        "@mui/lab": "^9.0.0-beta.6",
        "@mui/material": "^9.2.0",
        "axios": "^1.18.1",
        "react": "^19.2.7",
        "react-dom": "^19.2.7",
        "react-hot-toast": "^2.6.0",
        "react-router-dom": "^7.18.1",
        "recharts": "^3.10.0",
        "socket.io-client": "^4.8.3"
      },
      "devDependencies": {
        "@eslint/js": "^10.0.1",
        "@types/react": "^19.2.17",
        "@types/react-dom": "^19.2.3",
        "@vitejs/plugin-react": "^6.0.3",
        "eslint": "^10.6.0",
        "eslint-plugin-react-hooks": "^7.1.1",
        "eslint-plugin-react-refresh": "^0.5.3",
        "globals": "^17.7.0",
        "vite": "^8.1.1"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.29.7.tgz",
      "integrity": "sha512-Aup7aUOfpbAUg2ROOJN6Iw5f9DMBlzu0mIkm/malLQFN/YQgO48wCj0Kxa3sEHJvPVFg7siR+qRInwXd2qhQKw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.29.7",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/compat-data": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/compat-data/-/compat-data-7.29.7.tgz",
      "integrity": "sha512-locTkQyKvwIEgBzVrn8693ebc97F2U8ZHjbXwDXJ5Fn2TCpNwTlKcaKLkdHop5c/icOFE7qt7Q9JC5hnKNa6Gg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/core": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/core/-/core-7.29.7.tgz",
      "integrity": "sha512-RgHBCvtjbOK2gXSNBNIkNoEc9qoVEtau3hj8gEqKQuL3HZAibKarWFEI3Lfm6EYKkLalOh8eSrj9b+ch9H/VBA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.7",
        "@babel/generator": "^7.29.7",
        "@babel/helper-compilation-targets": "^7.29.7",
        "@babel/helper-module-transforms": "^7.29.7",
        "@babel/helpers": "^7.29.7",
        "@babel/parser": "^7.29.7",
        "@babel/template": "^7.29.7",
        "@babel/traverse": "^7.29.7",
        "@babel/types": "^7.29.7",
        "@jridgewell/remapping": "^2.3.5",
        "convert-source-map": "^2.0.0",
        "debug": "^4.1.0",
        "gensync": "^1.0.0-beta.2",
        "json5": "^2.2.3",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/babel"
      }
    },
    "node_modules/@babel/generator": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/generator/-/generator-7.29.7.tgz",
      "integrity": "sha512-DkXD5OJQaAQIdZ1bt3UZdEnHAn9Imd3IVBdX03UFe+ony9Ojw5pzr9YVKGDY1jt+Gcn/FnGkNf8r+Vj5NOJWtQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.29.7",
        "@babel/types": "^7.29.7",
        "@jridgewell/gen-mapping": "^0.3.12",
        "@jridgewell/trace-mapping": "^0.3.28",
        "jsesc": "^3.0.2"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-compilation-targets/-/helper-compilation-targets-7.29.7.tgz",
      "integrity": "sha512-wem6WaBj4NaVYVdNhLPPVacES6ZJ+KBBfSkTMD3YZxbP3rm3Di85tJU5ljaUNhaOynt+Aj0xruhYuzQBt8n71g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.29.7",
        "@babel/helper-validator-option": "^7.29.7",
        "browserslist": "^4.24.0",
        "lru-cache": "^5.1.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-globals": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-globals/-/helper-globals-7.29.7.tgz",
      "integrity": "sha512-3nQVUAtvkKH9zahfWgw96Jc/uFOmjACE1kQz82E2lqWmHBgjzbNlsC22nuQTfahmWeQtTq5nQ/4Nnd2A1wj4zA==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-imports": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-imports/-/helper-module-imports-7.29.7.tgz",
      "integrity": "sha512-ejHwrQQYcm9xnTivShn2IDOlIzInN34AXskvq9QicvCtEzq1Vzclu/tKF8Jq1Cg8JG2GL6/EmjgsCT7lXepE3g==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.29.7",
        "@babel/types": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-transforms": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-transforms/-/helper-module-transforms-7.29.7.tgz",
      "integrity": "sha512-UPUVSyXbOh627KiCIGQSgwWzGeBKLkaJ9PJEdrngIwMSzxLR4jS4+f1f1jb7VzBbg8nFLaYotvVPFCTqdrmTAg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.29.7",
        "@babel/helper-validator-identifier": "^7.29.7",
        "@babel/traverse": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-string-parser": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-string-parser/-/helper-string-parser-7.29.7.tgz",
      "integrity": "sha512-Pb5ijPrZ89GDH8223L4UP8i6QApWxs04RbPQJTeWDV0/keR2E36MeKnyr6LYmUUvqRRI+Iv87SuF1W6ErINzYw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.29.7.tgz",
      "integrity": "sha512-qehxGkRj55h/ff8EMaJ+cYhyaKlHIxqYDn682wQD7RNp9UujOQsHog2uS0r2vzr4pW+sXf90NeeayjcNaX3fFg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-option": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-option/-/helper-validator-option-7.29.7.tgz",
      "integrity": "sha512-N9ZErrD+yW5geCDtBqnOoxmR8+tNKiGuxKlDpuJxfsqpa2dFcexaziGAE/qoHLiDDreVNMupxGmSoNlyvsA3gw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helpers": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/helpers/-/helpers-7.29.7.tgz",
      "integrity": "sha512-1k2lAGRMfHTcwuNYcCNUmaUffmQv8KWMfh2iJUUeRlwlwH4FdNG7mfPI10NPfLHJFThE4Tyr4mv7kTNZOiPuBg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.29.7",
        "@babel/types": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/parser": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/parser/-/parser-7.29.7.tgz",
      "integrity": "sha512-hnORnjP/1P/zFEndoeX+n+t1RwWRJiJpM/jO7FW32Kn9r5+sJB2JWOdYo4L6k78j15eCwY3Gm/7364B1EMwtNg==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.29.7"
      },
      "bin": {
        "parser": "bin/babel-parser.js"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@babel/runtime": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/runtime/-/runtime-7.29.7.tgz",
      "integrity": "sha512-Nq8OhGWiZIZGV6hLHoyAKLLcJihP/xFeBMGJoUrxTX2psI8dCifzLhZISFb+VWS3wFMRDmCGw5R+dOySCqPLhw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/template": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/template/-/template-7.29.7.tgz",
      "integrity": "sha512-puq+Gf35oI24FeN11LkoUQFqv9uwNeWpxXZi/Ji3rRIoKAzKnxRaZ+Gkj0vKS9ZCiTESfng1N9LyOyXvo+m+Gg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.7",
        "@babel/parser": "^7.29.7",
        "@babel/types": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/traverse": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/traverse/-/traverse-7.29.7.tgz",
      "integrity": "sha512-EhlfNQtZ+NK22w5BM61ciuiq1m58ed33Wr1Xan//ZRTy6hgjnwyCffRYwzsGXdASJSUJ1guZILsErh1eQcl+zw==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.7",
        "@babel/generator": "^7.29.7",
        "@babel/helper-globals": "^7.29.7",
        "@babel/parser": "^7.29.7",
        "@babel/template": "^7.29.7",
        "@babel/types": "^7.29.7",
        "debug": "^4.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/types": {
      "version": "7.29.7",
      "resolved": "https://registry.npmjs.org/@babel/types/-/types-7.29.7.tgz",
      "integrity": "sha512-4zBIxpPzowiZpusoFkyGVwakdRJUyuH5PxQ/PrqghfdFWWasvnCdPfQXHrenDai+gyLARulZjZowCOj6fjT4pA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-string-parser": "^7.29.7",
        "@babel/helper-validator-identifier": "^7.29.7"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@emnapi/core": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@emnapi/core/-/core-1.11.1.tgz",
      "integrity": "sha512-RSvbQmHzdKzNsLYa/wHrbc3KN4sYLKAdPZxqiM2HATqv/SBk2/ENSHpvXGaLOMcsAyz0poEGqkmmKYG3OWiJEQ==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@emnapi/wasi-threads": "1.2.2",
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/runtime": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/@emnapi/runtime/-/runtime-1.11.1.tgz",
      "integrity": "sha512-vgj7R3y3Wgx24IQaGPA/R6YFXLHVMOZ0uVEyIQPaWs+rd1AzfEMXlAC22FYwO1XkKR6NPsq7mUandH8oIRdZFw==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emnapi/wasi-threads": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/@emnapi/wasi-threads/-/wasi-threads-1.2.2.tgz",
      "integrity": "sha512-c95qOXkHdydNKhscBTebqEC1CVAZpyqOfVfBzQ1qgzyl3gfeldUjIggDbIZgDKsHLgnsM+igH7TJ/eAasaVuMA==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@emotion/babel-plugin": {
      "version": "11.13.5",
      "resolved": "https://registry.npmjs.org/@emotion/babel-plugin/-/babel-plugin-11.13.5.tgz",
      "integrity": "sha512-pxHCpT2ex+0q+HH91/zsdHkw/lXd468DIN2zvfvLtPKLLMo6gQj7oLObq8PhkrxOZb/gGCq03S3Z7PDhS8pduQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.16.7",
        "@babel/runtime": "^7.18.3",
        "@emotion/hash": "^0.9.2",
        "@emotion/memoize": "^0.9.0",
        "@emotion/serialize": "^1.3.3",
        "babel-plugin-macros": "^3.1.0",
        "convert-source-map": "^1.5.0",
        "escape-string-regexp": "^4.0.0",
        "find-root": "^1.1.0",
        "source-map": "^0.5.7",
        "stylis": "4.2.0"
      }
    },
    "node_modules/@emotion/babel-plugin/node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/@emotion/cache": {
      "version": "11.14.0",
      "resolved": "https://registry.npmjs.org/@emotion/cache/-/cache-11.14.0.tgz",
      "integrity": "sha512-L/B1lc/TViYk4DcpGxtAVbx0ZyiKM5ktoIyafGkH6zg/tj+mA+NE//aPYKG0k8kCHSHVJrpLpcAlOBEXQ3SavA==",
      "license": "MIT",
      "dependencies": {
        "@emotion/memoize": "^0.9.0",
        "@emotion/sheet": "^1.4.0",
        "@emotion/utils": "^1.4.2",
        "@emotion/weak-memoize": "^0.4.0",
        "stylis": "4.2.0"
      }
    },
    "node_modules/@emotion/hash": {
      "version": "0.9.2",
      "resolved": "https://registry.npmjs.org/@emotion/hash/-/hash-0.9.2.tgz",
      "integrity": "sha512-MyqliTZGuOm3+5ZRSaaBGP3USLw6+EGykkwZns2EPC5g8jJ4z9OrdZY9apkl3+UP9+sdz76YYkwCKP5gh8iY3g==",
      "license": "MIT"
    },
    "node_modules/@emotion/is-prop-valid": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/@emotion/is-prop-valid/-/is-prop-valid-1.4.0.tgz",
      "integrity": "sha512-QgD4fyscGcbbKwJmqNvUMSE02OsHUa+lAWKdEUIJKgqe5IwRSKd7+KhibEWdaKwgjLj0DRSHA9biAIqGBk05lw==",
      "license": "MIT",
      "dependencies": {
        "@emotion/memoize": "^0.9.0"
      }
    },
    "node_modules/@emotion/memoize": {
      "version": "0.9.0",
      "resolved": "https://registry.npmjs.org/@emotion/memoize/-/memoize-0.9.0.tgz",
      "integrity": "sha512-30FAj7/EoJ5mwVPOWhAyCX+FPfMDrVecJAM+Iw9NRoSl4BBAQeqj4cApHHUXOVvIPgLVDsCFoz/hGD+5QQD1GQ==",
      "license": "MIT"
    },
    "node_modules/@emotion/react": {
      "version": "11.14.0",
      "resolved": "https://registry.npmjs.org/@emotion/react/-/react-11.14.0.tgz",
      "integrity": "sha512-O000MLDBDdk/EohJPFUqvnp4qnHeYkVP5B0xEG0D/L7cOKP9kefu2DXn8dj74cQfsEzUqh+sr1RzFqiL1o+PpA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.3",
        "@emotion/babel-plugin": "^11.13.5",
        "@emotion/cache": "^11.14.0",
        "@emotion/serialize": "^1.3.3",
        "@emotion/use-insertion-effect-with-fallbacks": "^1.2.0",
        "@emotion/utils": "^1.4.2",
        "@emotion/weak-memoize": "^0.4.0",
        "hoist-non-react-statics": "^3.3.1"
      },
      "peerDependencies": {
        "react": ">=16.8.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@emotion/serialize": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/@emotion/serialize/-/serialize-1.3.3.tgz",
      "integrity": "sha512-EISGqt7sSNWHGI76hC7x1CksiXPahbxEOrC5RjmFRJTqLyEK9/9hZvBbiYn70dw4wuwMKiEMCUlR6ZXTSWQqxA==",
      "license": "MIT",
      "dependencies": {
        "@emotion/hash": "^0.9.2",
        "@emotion/memoize": "^0.9.0",
        "@emotion/unitless": "^0.10.0",
        "@emotion/utils": "^1.4.2",
        "csstype": "^3.0.2"
      }
    },
    "node_modules/@emotion/sheet": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/@emotion/sheet/-/sheet-1.4.0.tgz",
      "integrity": "sha512-fTBW9/8r2w3dXWYM4HCB1Rdp8NLibOw2+XELH5m5+AkWiL/KqYX6dc0kKYlaYyKjrQ6ds33MCdMPEwgs2z1rqg==",
      "license": "MIT"
    },
    "node_modules/@emotion/styled": {
      "version": "11.14.1",
      "resolved": "https://registry.npmjs.org/@emotion/styled/-/styled-11.14.1.tgz",
      "integrity": "sha512-qEEJt42DuToa3gurlH4Qqc1kVpNq8wO8cJtDzU46TjlzWjDlsVyevtYCRijVq3SrHsROS+gVQ8Fnea108GnKzw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.3",
        "@emotion/babel-plugin": "^11.13.5",
        "@emotion/is-prop-valid": "^1.3.0",
        "@emotion/serialize": "^1.3.3",
        "@emotion/use-insertion-effect-with-fallbacks": "^1.2.0",
        "@emotion/utils": "^1.4.2"
      },
      "peerDependencies": {
        "@emotion/react": "^11.0.0-rc.0",
        "react": ">=16.8.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@emotion/unitless": {
      "version": "0.10.0",
      "resolved": "https://registry.npmjs.org/@emotion/unitless/-/unitless-0.10.0.tgz",
      "integrity": "sha512-dFoMUuQA20zvtVTuxZww6OHoJYgrzfKM1t52mVySDJnMSEa08ruEvdYQbhvyu6soU+NeLVd3yKfTfT0NeV6qGg==",
      "license": "MIT"
    },
    "node_modules/@emotion/use-insertion-effect-with-fallbacks": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/@emotion/use-insertion-effect-with-fallbacks/-/use-insertion-effect-with-fallbacks-1.2.0.tgz",
      "integrity": "sha512-yJMtVdH59sxi/aVJBpk9FQq+OR8ll5GT8oWd57UpeaKEVGab41JWaCFA7FRLoMLloOZF/c/wsPoe+bfGmRKgDg==",
      "license": "MIT",
      "peerDependencies": {
        "react": ">=16.8.0"
      }
    },
    "node_modules/@emotion/utils": {
      "version": "1.4.2",
      "resolved": "https://registry.npmjs.org/@emotion/utils/-/utils-1.4.2.tgz",
      "integrity": "sha512-3vLclRofFziIa3J2wDh9jjbkUz9qk5Vi3IZ/FSTKViB0k+ef0fPV7dYrUIugbgupYDx7v9ud/SjrtEP8Y4xLoA==",
      "license": "MIT"
    },
    "node_modules/@emotion/weak-memoize": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/@emotion/weak-memoize/-/weak-memoize-0.4.0.tgz",
      "integrity": "sha512-snKqtPW01tN0ui7yu9rGv69aJXr/a/Ywvl11sUjNtEcRc+ng/mQriFL0wLXMef74iHa/EkftbDzU9F8iFbH+zg==",
      "license": "MIT"
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.10.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.10.1.tgz",
      "integrity": "sha512-cuadcxVFE8sDK6iWJbs8Sn0av2Nrh2QSGQhVlBW9AaAHqHwjWsZHT8LJ4hFGPh7ASBV2deFdM7H/DPjulmh8rg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "eslint-visitor-keys": "^3.4.3"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || >=8.0.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-3.4.3.tgz",
      "integrity": "sha512-wpc+LXeiyiisxPlEkUzU6svyS1frIO3Mgxj1fdy7Pm8Ygzguax2N3Fa/D/ag1WqbOprdI+uY6wMUl8/a2G+iag==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint-community/regexpp": {
      "version": "4.12.2",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.2.tgz",
      "integrity": "sha512-EriSTlt5OC9/7SXkRSCAhfSxxoSUgBm33OH+IkwbdpgoqsSsUg7y3uh+IICI/Qg4BBWr3U2i39RpmycbxMq4ew==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^12.0.0 || ^14.0.0 || >=16.0.0"
      }
    },
    "node_modules/@eslint/config-array": {
      "version": "0.23.5",
      "resolved": "https://registry.npmjs.org/@eslint/config-array/-/config-array-0.23.5.tgz",
      "integrity": "sha512-Y3kKLvC1dvTOT+oGlqNQ1XLqK6D1HU2YXPc52NmAlJZbMMWDzGYXMiPRJ8TYD39muD/OTjlZmNJ4ib7dvSrMBA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/object-schema": "^3.0.5",
        "debug": "^4.3.1",
        "minimatch": "^10.2.4"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/config-helpers": {
      "version": "0.6.0",
      "resolved": "https://registry.npmjs.org/@eslint/config-helpers/-/config-helpers-0.6.0.tgz",
      "integrity": "sha512-ii6Bw9jJ2zi2cWA2Z+9/QZ/+3DX6kwaV5Q986D/CdP3Lap3w/pgQZ373FV7byY/i7L4IRH/G43I5dz1ClsCbpA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/core": "^1.2.1"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/core": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/@eslint/core/-/core-1.2.1.tgz",
      "integrity": "sha512-MwcE1P+AZ4C6DWlpin/OmOA54mmIZ/+xZuJiQd4SyB29oAJjN30UW9wkKNptW2ctp4cEsvhlLY/CsQ1uoHDloQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@types/json-schema": "^7.0.15"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/js": {
      "version": "10.0.1",
      "resolved": "https://registry.npmjs.org/@eslint/js/-/js-10.0.1.tgz",
      "integrity": "sha512-zeR9k5pd4gxjZ0abRoIaxdc7I3nDktoXZk2qOv9gCNWx3mVwEn32VRhyLaRsDiJjTs0xq/T8mfPtyuXu7GWBcA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      },
      "funding": {
        "url": "https://eslint.org/donate"
      },
      "peerDependencies": {
        "eslint": "^10.0.0"
      },
      "peerDependenciesMeta": {
        "eslint": {
          "optional": true
        }
      }
    },
    "node_modules/@eslint/object-schema": {
      "version": "3.0.5",
      "resolved": "https://registry.npmjs.org/@eslint/object-schema/-/object-schema-3.0.5.tgz",
      "integrity": "sha512-vqTaUEgxzm+YDSdElad6PiRoX4t8VGDjCtt05zn4nU810UIx/uNEV7/lZJ6KwFThKZOzOxzXy48da+No7HZaMw==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/plugin-kit": {
      "version": "0.7.2",
      "resolved": "https://registry.npmjs.org/@eslint/plugin-kit/-/plugin-kit-0.7.2.tgz",
      "integrity": "sha512-+CNAzxglkrpNf/kKywqQfk74QjtceuOE7Qm+AF8miRvPF/wmmK5+OJOgVh3AVTT3RP2mH3+FOaxlE5v72owk0A==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/core": "^1.2.1",
        "levn": "^0.4.1"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@humanfs/core": {
      "version": "0.19.2",
      "resolved": "https://registry.npmjs.org/@humanfs/core/-/core-0.19.2.tgz",
      "integrity": "sha512-UhXNm+CFMWcbChXywFwkmhqjs3PRCmcSa/hfBgLIb7oQ5HNb1wS0icWsGtSAUNgefHeI+eBrA8I1fxmbHsGdvA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@humanfs/types": "^0.15.0"
      },
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanfs/node": {
      "version": "0.16.8",
      "resolved": "https://registry.npmjs.org/@humanfs/node/-/node-0.16.8.tgz",
      "integrity": "sha512-gE1eQNZ3R++kTzFUpdGlpmy8kDZD/MLyHqDwqjkVQI0JMdI1D51sy1H958PNXYkM2rAac7e5/CnIKZrHtPh3BQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@humanfs/core": "^0.19.2",
        "@humanfs/types": "^0.15.0",
        "@humanwhocodes/retry": "^0.4.0"
      },
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanfs/types": {
      "version": "0.15.0",
      "resolved": "https://registry.npmjs.org/@humanfs/types/-/types-0.15.0.tgz",
      "integrity": "sha512-ZZ1w0aoQkwuUuC7Yf+7sdeaNfqQiiLcSRbfI08oAxqLtpXQr9AIVX7Ay7HLDuiLYAaFPu8oBYNq/QIi9URHJ3Q==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanwhocodes/module-importer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/module-importer/-/module-importer-1.0.1.tgz",
      "integrity": "sha512-bxveV4V8v5Yb4ncFTT3rPSgZBOpCkjfK0y4oVVVJwIuDVBRMDXrPyXRL988i5ap9m9bnyEEjWfm5WkBmtffLfA==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=12.22"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@humanwhocodes/retry": {
      "version": "0.4.3",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/retry/-/retry-0.4.3.tgz",
      "integrity": "sha512-bV0Tgo9K4hfPCek+aMAn81RppFKv2ySDQeMoSZuvTASywNTnVJCArCZE2FWqpvIatKu7VMRLWlR1EazvVhDyhQ==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=18.18"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/remapping": {
      "version": "2.3.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/remapping/-/remapping-2.3.5.tgz",
      "integrity": "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@mui/core-downloads-tracker": {
      "version": "9.2.0",
      "resolved": "https://registry.npmjs.org/@mui/core-downloads-tracker/-/core-downloads-tracker-9.2.0.tgz",
      "integrity": "sha512-+XMav+ZaXkZKUFUgzjrfMEedfyJKxxviAske2q8N8CWDMeqZdDU2lWMkiUPiB388hGaDqhwvOAwkrsc/pUyp8g==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      }
    },
    "node_modules/@mui/icons-material": {
      "version": "9.2.0",
      "resolved": "https://registry.npmjs.org/@mui/icons-material/-/icons-material-9.2.0.tgz",
      "integrity": "sha512-VgBd3z7Qc3vd/thcNSMC03nHRh/U4DzMUd+1dRyJTbm/hGo7+N6N4GDuJZDNHa6LZhhwG6Cu1X3DNvrVv8sNag==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@mui/material": "^9.2.0",
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/lab": {
      "version": "9.0.0-beta.6",
      "resolved": "https://registry.npmjs.org/@mui/lab/-/lab-9.0.0-beta.6.tgz",
      "integrity": "sha512-y92D7zcvX2OCzFFu4IbYKAVj3cayuFHX6OZm0LdsLDPlUi55zjUhjR9pjI23nCGAQXRPmWE/3BZjCyFiYYpNqQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2",
        "@mui/system": "^9.2.0",
        "@mui/types": "^9.1.1",
        "@mui/utils": "^9.2.0",
        "clsx": "^2.1.1",
        "prop-types": "^15.8.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@emotion/react": "^11.5.0",
        "@emotion/styled": "^11.3.0",
        "@mui/material": "^9.2.0",
        "@mui/material-pigment-css": "^9.2.0",
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@emotion/react": {
          "optional": true
        },
        "@emotion/styled": {
          "optional": true
        },
        "@mui/material-pigment-css": {
          "optional": true
        },
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/material": {
      "version": "9.2.0",
      "resolved": "https://registry.npmjs.org/@mui/material/-/material-9.2.0.tgz",
      "integrity": "sha512-+YTRSgGKGrrRo2XJZXs7JRA6qHoHWvNtxyqxnrRJTBmIuLOUpxxh7m4G9lF4tWberxGFY+EqkkRPgJCl+fSMJg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2",
        "@mui/core-downloads-tracker": "^9.2.0",
        "@mui/system": "^9.2.0",
        "@mui/types": "^9.1.1",
        "@mui/utils": "^9.2.0",
        "@popperjs/core": "^2.11.8",
        "@types/react-transition-group": "^4.4.12",
        "clsx": "^2.1.1",
        "csstype": "^3.2.3",
        "prop-types": "^15.8.1",
        "react-is": "^19.2.6",
        "react-transition-group": "^4.4.5"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@emotion/react": "^11.5.0",
        "@emotion/styled": "^11.3.0",
        "@mui/material-pigment-css": "^9.2.0",
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@emotion/react": {
          "optional": true
        },
        "@emotion/styled": {
          "optional": true
        },
        "@mui/material-pigment-css": {
          "optional": true
        },
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/private-theming": {
      "version": "9.2.0",
      "resolved": "https://registry.npmjs.org/@mui/private-theming/-/private-theming-9.2.0.tgz",
      "integrity": "sha512-w9wpyDxGPGnAACPB2hKhCDmILJIAvQxrfjUbIAEa0AznX1rOjaz5N+yB1uuw8ixnJcpEh/tPbD9oEe19wcWPHw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2",
        "@mui/utils": "^9.2.0",
        "prop-types": "^15.8.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/styled-engine": {
      "version": "9.1.1",
      "resolved": "https://registry.npmjs.org/@mui/styled-engine/-/styled-engine-9.1.1.tgz",
      "integrity": "sha512-neaYKdJfvEG54q8efHLJR7swpHG/gfSv9xGqW5iTSMsubD7yPCPFrhVBt284j1DOF3uZaaDJSHQL7gz6jGF21Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2",
        "@emotion/cache": "^11.14.0",
        "@emotion/serialize": "^1.3.3",
        "@emotion/sheet": "^1.4.0",
        "csstype": "^3.2.3",
        "prop-types": "^15.8.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@emotion/react": "^11.4.1",
        "@emotion/styled": "^11.3.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@emotion/react": {
          "optional": true
        },
        "@emotion/styled": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/system": {
      "version": "9.2.0",
      "resolved": "https://registry.npmjs.org/@mui/system/-/system-9.2.0.tgz",
      "integrity": "sha512-YvUJwKoGVtbnOm2PyPi5TvX2d1rOA6sqSpEWVs4WmXNIaFTuYmNUaVdU2o1NKUEe31URnD3E8ZVUMcsLQXwcYg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2",
        "@mui/private-theming": "^9.2.0",
        "@mui/styled-engine": "^9.1.1",
        "@mui/types": "^9.1.1",
        "@mui/utils": "^9.2.0",
        "clsx": "^2.1.1",
        "csstype": "^3.2.3",
        "prop-types": "^15.8.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@emotion/react": "^11.5.0",
        "@emotion/styled": "^11.3.0",
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@emotion/react": {
          "optional": true
        },
        "@emotion/styled": {
          "optional": true
        },
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/types": {
      "version": "9.1.1",
      "resolved": "https://registry.npmjs.org/@mui/types/-/types-9.1.1.tgz",
      "integrity": "sha512-Zjt7u8wNvDg40rPTGoL+TnfkpuSKjwubsNSFRH1KAVZLcaV4I3AFNHIFbvH7p4F3alEibSbdd90xAgn5Rnfndg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2"
      },
      "peerDependencies": {
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@mui/utils": {
      "version": "9.2.0",
      "resolved": "https://registry.npmjs.org/@mui/utils/-/utils-9.2.0.tgz",
      "integrity": "sha512-OsUH5zhlSOM4xmLl53+agug1M1UyWb4zxFxWQCqwKTKUeQPvTENtg3JhrroBD2qpCLKsX5W/DYGERJ4mBUbc8g==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.29.2",
        "@mui/types": "^9.1.1",
        "@types/prop-types": "^15.7.15",
        "clsx": "^2.1.1",
        "prop-types": "^15.8.1",
        "react-is": "^19.2.6"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/mui-org"
      },
      "peerDependencies": {
        "@types/react": "^17.0.0 || ^18.0.0 || ^19.0.0",
        "react": "^17.0.0 || ^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        }
      }
    },
    "node_modules/@napi-rs/wasm-runtime": {
      "version": "1.1.6",
      "resolved": "https://registry.npmjs.org/@napi-rs/wasm-runtime/-/wasm-runtime-1.1.6.tgz",
      "integrity": "sha512-ZLv/JdUfkvOy9eCnnBaGfiO+XimbjebAeO+MRQqD/B+FR1tnRN0tpKSJHRbE8sFfS6aqsXZ67TQjfwfsxULVbg==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@tybys/wasm-util": "^0.10.3"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/Brooooooklyn"
      },
      "peerDependencies": {
        "@emnapi/core": "^1.7.1",
        "@emnapi/runtime": "^1.7.1"
      }
    },
    "node_modules/@oxc-project/types": {
      "version": "0.139.0",
      "resolved": "https://registry.npmjs.org/@oxc-project/types/-/types-0.139.0.tgz",
      "integrity": "sha512-r9gHphtCs+1M7J0pw6Sn/hh/Wpa/iQrOOkrNAlVLF/gHq+/CJmHIWKKUUhdWjcD6CIa8idarspCsASiXCXvFUw==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/Boshen"
      }
    },
    "node_modules/@popperjs/core": {
      "version": "2.11.8",
      "resolved": "https://registry.npmjs.org/@popperjs/core/-/core-2.11.8.tgz",
      "integrity": "sha512-P1st0aksCrn9sGZhp8GMYwBnQsbvAWsZAX44oXNNvLHGqAOcoVxmjZiohstwQ7SqKnbR47akdNi+uleWD8+g6A==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/popperjs"
      }
    },
    "node_modules/@reduxjs/toolkit": {
      "version": "2.12.0",
      "resolved": "https://registry.npmjs.org/@reduxjs/toolkit/-/toolkit-2.12.0.tgz",
      "integrity": "sha512-KiT+RzZbp6mQET+Mg+h2c97+9j1sNflUxQkIHI7Yuzf6Peu+OYpmkn6nbHWmLLWj+1ZODUJFwGZ7gx3L9R9EOw==",
      "license": "MIT",
      "dependencies": {
        "@standard-schema/spec": "^1.0.0",
        "@standard-schema/utils": "^0.3.0",
        "immer": "^11.0.0",
        "redux": "^5.0.1",
        "redux-thunk": "^3.1.0",
        "reselect": "^5.1.0"
      },
      "peerDependencies": {
        "react": "^16.9.0 || ^17.0.0 || ^18 || ^19",
        "react-redux": "^7.2.1 || ^8.1.3 || ^9.0.0"
      },
      "peerDependenciesMeta": {
        "react": {
          "optional": true
        },
        "react-redux": {
          "optional": true
        }
      }
    },
    "node_modules/@rolldown/binding-android-arm64": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-android-arm64/-/binding-android-arm64-1.1.5.tgz",
      "integrity": "sha512-lZg8fqIv2v7FF237bwMgzGZEJvGL79/s5knJ/i6FmsGF4XXlzccZ4jb+TrFIxtSSxFtIpdsgrPZeMk1I9AFcyQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-darwin-arm64": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-darwin-arm64/-/binding-darwin-arm64-1.1.5.tgz",
      "integrity": "sha512-51Bnx9pNiMRKSUNtBfySkNJ9vMU9Hh3I1ozDd6gyPPYzaXCfnptUcEZxXGYFn+ul2dtcMUiqGR1Yai2K10uoTw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-darwin-x64": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-darwin-x64/-/binding-darwin-x64-1.1.5.tgz",
      "integrity": "sha512-Tm+gbfC0aHu1tBA/JvKQh32S0K6YgCHkiAF4/W6xX0K0RmNuc94VeK419dJoE65R5aRxmo+noZQSWrAMF6yb6g==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-freebsd-x64": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-freebsd-x64/-/binding-freebsd-x64-1.1.5.tgz",
      "integrity": "sha512-JMzDKCCXq93YccG5gz3hvOs1oXRKAf0XYpfOS88e+wZrC8Iugj6j68867vrYZkvpDDpKn/KoKORThmchMpF6TA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-arm-gnueabihf": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-arm-gnueabihf/-/binding-linux-arm-gnueabihf-1.1.5.tgz",
      "integrity": "sha512-uML21j2K5TfPGutKxub+M+nLjZIrWjXQ5Grx4lCe/nimTj9B4L63zHpjXLl4y0L3mcm2htEQIb06oCG/szerNw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-arm64-gnu": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-arm64-gnu/-/binding-linux-arm64-gnu-1.1.5.tgz",
      "integrity": "sha512-navSiuTMogvnQoZoM/v+l3ZWo50/NTwSHSzheABx/RCnmUPaKwq9qSo4Br2OYRs21+Fz8uFqITZM3H4opOB0/Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-arm64-musl": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-arm64-musl/-/binding-linux-arm64-musl-1.1.5.tgz",
      "integrity": "sha512-lAryqH7IteztmCXQXk0etKj4wBQ7Gx5S6LjKhsgp9zb8I5bsuvU/2llH1hDQcjsFeqIsovMVN339/8pUDDBXxA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-ppc64-gnu": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-ppc64-gnu/-/binding-linux-ppc64-gnu-1.1.5.tgz",
      "integrity": "sha512-fsK/sNBnxzBlL4O1JNrZakVQxPspqpED5dLtNsZS9oOKmtSpdNIzxH2kkol5HYTWJN47sE20ztMJPxfZ89qGOg==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-s390x-gnu": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-s390x-gnu/-/binding-linux-s390x-gnu-1.1.5.tgz",
      "integrity": "sha512-gLYb4BIadlfTOYT5gO503n8zQjXflgzpD0FcyKh0Mzx3rqCZKnHoJWV9xe1KXUJ5lx2JfcSHr/mhzS0PC/McAA==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-x64-gnu": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-x64-gnu/-/binding-linux-x64-gnu-1.1.5.tgz",
      "integrity": "sha512-FjcpEKUyJygHgs1o50VYNvkt5+7Le/VEdYt0AkRpkL33MnyQfwr8l5mXwMmfmTbyMPr5vJLC+8/Gd9gXnwU1QQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-linux-x64-musl": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-linux-x64-musl/-/binding-linux-x64-musl-1.1.5.tgz",
      "integrity": "sha512-Me+PfPI2TMeOQk0gYWfLQZtTktrmzbr8cDboqX83XKc7UrgAi55gF+2dUkWdxd19n55Essp2yeca+O9N5rBxHg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-openharmony-arm64": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-openharmony-arm64/-/binding-openharmony-arm64-1.1.5.tgz",
      "integrity": "sha512-yc5WrLzXks6zCQfn9Oxr8pORKyl/pF+QjHmW/Qx3qu0oyrrNC+y2JLTU1E2rcWYAmzlnqngWXHQjy51VzW70Vw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-wasm32-wasi": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-wasm32-wasi/-/binding-wasm32-wasi-1.1.5.tgz",
      "integrity": "sha512-VbQGPX2b4r48TAMIM2cjgluIM1HYutm4pcTEJsle7iEP7sB1dFqtPLBVbdLAZCxy1txCcPxf4QFf4v8uvltPqA==",
      "cpu": [
        "wasm32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "@emnapi/core": "1.11.1",
        "@emnapi/runtime": "1.11.1",
        "@napi-rs/wasm-runtime": "^1.1.6"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-win32-arm64-msvc": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-win32-arm64-msvc/-/binding-win32-arm64-msvc-1.1.5.tgz",
      "integrity": "sha512-gHv82k63z4qpV5+Q1y/12KrK0ltWBukVDI8nZcbT7Tt/ZlOIVwppazneq0F93oDxTo3IgAMEDIoQh3E2n6mVsw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/binding-win32-x64-msvc": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/@rolldown/binding-win32-x64-msvc/-/binding-win32-x64-msvc-1.1.5.tgz",
      "integrity": "sha512-tTZuDBPw85tEN5PQi1pnEBzDy0Z49HtScLAbD5t6hyeU92A95pRWaSMw1GZZi/RwgSgUIl0xrSlXIT/9QzvYSA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      }
    },
    "node_modules/@rolldown/pluginutils": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@rolldown/pluginutils/-/pluginutils-1.0.1.tgz",
      "integrity": "sha512-2j9bGt5Jh8hj+vPtgzPtl72j0yRxHAyumoo6TNfAjsLB04UtpSvPbPcDcBMxz7n+9CYB0c1GxQFxYRg2jimqGw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@socket.io/component-emitter": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@socket.io/component-emitter/-/component-emitter-3.1.2.tgz",
      "integrity": "sha512-9BCxFwvbGg/RsZK9tjXd8s4UcwR0MWeFQ1XEKIQVVvAGJyINdrqKMcTRyLoK8Rse1GjzLV9cwjWV1olXRWEXVA==",
      "license": "MIT"
    },
    "node_modules/@standard-schema/spec": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@standard-schema/spec/-/spec-1.1.0.tgz",
      "integrity": "sha512-l2aFy5jALhniG5HgqrD6jXLi/rUWrKvqN/qJx6yoJsgKhblVd+iqqU4RCXavm/jPityDo5TCvKMnpjKnOriy0w==",
      "license": "MIT"
    },
    "node_modules/@standard-schema/utils": {
      "version": "0.3.0",
      "resolved": "https://registry.npmjs.org/@standard-schema/utils/-/utils-0.3.0.tgz",
      "integrity": "sha512-e7Mew686owMaPJVNNLs55PUvgz371nKgwsc4vxE49zsODpJEnxgxRo2y/OKrqueavXgZNMDVj3DdHFlaSAeU8g==",
      "license": "MIT"
    },
    "node_modules/@tybys/wasm-util": {
      "version": "0.10.3",
      "resolved": "https://registry.npmjs.org/@tybys/wasm-util/-/wasm-util-0.10.3.tgz",
      "integrity": "sha512-F3fo1MYrRJYL3zER0OUOmkutjr1Vp23m7OsSgp7nq4SP6OqX6C/56XFIPAl5bt3zaBRjmW7SGz3u/6LwFpYcOg==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "dependencies": {
        "tslib": "^2.4.0"
      }
    },
    "node_modules/@types/d3-array": {
      "version": "3.2.2",
      "resolved": "https://registry.npmjs.org/@types/d3-array/-/d3-array-3.2.2.tgz",
      "integrity": "sha512-hOLWVbm7uRza0BYXpIIW5pxfrKe0W+D5lrFiAEYR+pb6w3N2SwSMaJbXdUfSEv+dT4MfHBLtn5js0LAWaO6otw==",
      "license": "MIT"
    },
    "node_modules/@types/d3-color": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/@types/d3-color/-/d3-color-3.1.3.tgz",
      "integrity": "sha512-iO90scth9WAbmgv7ogoq57O9YpKmFBbmoEoCHDB2xMBY0+/KVrqAaCDyCE16dUspeOvIxFFRI+0sEtqDqy2b4A==",
      "license": "MIT"
    },
    "node_modules/@types/d3-ease": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/@types/d3-ease/-/d3-ease-3.0.2.tgz",
      "integrity": "sha512-NcV1JjO5oDzoK26oMzbILE6HW7uVXOHLQvHshBUW4UMdZGfiY6v5BeQwh9a9tCzv+CeefZQHJt5SRgK154RtiA==",
      "license": "MIT"
    },
    "node_modules/@types/d3-interpolate": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/@types/d3-interpolate/-/d3-interpolate-3.0.4.tgz",
      "integrity": "sha512-mgLPETlrpVV1YRJIglr4Ez47g7Yxjl1lj7YKsiMCb27VJH9W8NVM6Bb9d8kkpG/uAQS5AmbA48q2IAolKKo1MA==",
      "license": "MIT",
      "dependencies": {
        "@types/d3-color": "*"
      }
    },
    "node_modules/@types/d3-path": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/@types/d3-path/-/d3-path-3.1.1.tgz",
      "integrity": "sha512-VMZBYyQvbGmWyWVea0EHs/BwLgxc+MKi1zLDCONksozI4YJMcTt8ZEuIR4Sb1MMTE8MMW49v0IwI5+b7RmfWlg==",
      "license": "MIT"
    },
    "node_modules/@types/d3-scale": {
      "version": "4.0.9",
      "resolved": "https://registry.npmjs.org/@types/d3-scale/-/d3-scale-4.0.9.tgz",
      "integrity": "sha512-dLmtwB8zkAeO/juAMfnV+sItKjlsw2lKdZVVy6LRr0cBmegxSABiLEpGVmSJJ8O08i4+sGR6qQtb6WtuwJdvVw==",
      "license": "MIT",
      "dependencies": {
        "@types/d3-time": "*"
      }
    },
    "node_modules/@types/d3-shape": {
      "version": "3.1.8",
      "resolved": "https://registry.npmjs.org/@types/d3-shape/-/d3-shape-3.1.8.tgz",
      "integrity": "sha512-lae0iWfcDeR7qt7rA88BNiqdvPS5pFVPpo5OfjElwNaT2yyekbM0C9vK+yqBqEmHr6lDkRnYNoTBYlAgJa7a4w==",
      "license": "MIT",
      "dependencies": {
        "@types/d3-path": "*"
      }
    },
    "node_modules/@types/d3-time": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/@types/d3-time/-/d3-time-3.0.4.tgz",
      "integrity": "sha512-yuzZug1nkAAaBlBBikKZTgzCeA+k1uy4ZFwWANOfKw5z5LRhV0gNA7gNkKm7HoK+HRN0wX3EkxGk0fpbWhmB7g==",
      "license": "MIT"
    },
    "node_modules/@types/d3-timer": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/@types/d3-timer/-/d3-timer-3.0.2.tgz",
      "integrity": "sha512-Ps3T8E8dZDam6fUyNiMkekK3XUsaUEik+idO9/YjPtfj2qruF8tFBXS7XhtE4iIXBLxhmLjP3SXpLhVf21I9Lw==",
      "license": "MIT"
    },
    "node_modules/@types/esrecurse": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/@types/esrecurse/-/esrecurse-4.3.1.tgz",
      "integrity": "sha512-xJBAbDifo5hpffDBuHl0Y8ywswbiAp/Wi7Y/GtAgSlZyIABppyurxVueOPE8LUQOxdlgi6Zqce7uoEpqNTeiUw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/estree": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.9.tgz",
      "integrity": "sha512-GhdPgy1el4/ImP05X05Uw4cw2/M93BCUmnEvWZNStlCzEKME4Fkk+YpoA5OiHNQmoS7Cafb8Xa3Pya8m1Qrzeg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/json-schema": {
      "version": "7.0.15",
      "resolved": "https://registry.npmjs.org/@types/json-schema/-/json-schema-7.0.15.tgz",
      "integrity": "sha512-5+fP8P8MFNC+AyZCDxrB2pkZFPGzqQWUzpSeuuVLvm8VMcorNYavBqoFcxK8bQz4Qsbn4oUEEem4wDLfcysGHA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/parse-json": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/@types/parse-json/-/parse-json-4.0.2.tgz",
      "integrity": "sha512-dISoDXWWQwUquiKsyZ4Ng+HX2KsPL7LyHKHQwgGFEA3IaKac4Obd+h2a/a6waisAoepJlBcx9paWqjA8/HVjCw==",
      "license": "MIT"
    },
    "node_modules/@types/prop-types": {
      "version": "15.7.15",
      "resolved": "https://registry.npmjs.org/@types/prop-types/-/prop-types-15.7.15.tgz",
      "integrity": "sha512-F6bEyamV9jKGAFBEmlQnesRPGOQqS2+Uwi0Em15xenOxHaf2hv6L8YCVn3rPdPJOiJfPiCnLIRyvwVaqMY3MIw==",
      "license": "MIT"
    },
    "node_modules/@types/react": {
      "version": "19.2.17",
      "resolved": "https://registry.npmjs.org/@types/react/-/react-19.2.17.tgz",
      "integrity": "sha512-MXfmqaVPEVgkBT/aY0aGCkRWWtByiYQXo3xdQ8r5RzuFrPiRn8Gar2tQdXSUQ2GKV3bkXckek89V8wQBY2Q/Aw==",
      "license": "MIT",
      "dependencies": {
        "csstype": "^3.2.2"
      }
    },
    "node_modules/@types/react-dom": {
      "version": "19.2.3",
      "resolved": "https://registry.npmjs.org/@types/react-dom/-/react-dom-19.2.3.tgz",
      "integrity": "sha512-jp2L/eY6fn+KgVVQAOqYItbF0VY/YApe5Mz2F0aykSO8gx31bYCZyvSeYxCHKvzHG5eZjc+zyaS5BrBWya2+kQ==",
      "dev": true,
      "license": "MIT",
      "peerDependencies": {
        "@types/react": "^19.2.0"
      }
    },
    "node_modules/@types/react-transition-group": {
      "version": "4.4.12",
      "resolved": "https://registry.npmjs.org/@types/react-transition-group/-/react-transition-group-4.4.12.tgz",
      "integrity": "sha512-8TV6R3h2j7a91c+1DXdJi3Syo69zzIZbz7Lg5tORM5LEJG7X/E6a1V3drRyBRZq7/utz7A+c4OgYLiLcYGHG6w==",
      "license": "MIT",
      "peerDependencies": {
        "@types/react": "*"
      }
    },
    "node_modules/@types/use-sync-external-store": {
      "version": "0.0.6",
      "resolved": "https://registry.npmjs.org/@types/use-sync-external-store/-/use-sync-external-store-0.0.6.tgz",
      "integrity": "sha512-zFDAD+tlpf2r4asuHEj0XH6pY6i0g5NeAHPn+15wk3BV6JA69eERFXC1gyGThDkVa1zCyKr5jox1+2LbV/AMLg==",
      "license": "MIT"
    },
    "node_modules/@vitejs/plugin-react": {
      "version": "6.0.4",
      "resolved": "https://registry.npmjs.org/@vitejs/plugin-react/-/plugin-react-6.0.4.tgz",
      "integrity": "sha512-XcCQz0TBpBgljhj0gMuuDj49i6Ytqh5q1osT/Gp5uAVJUCTWxyskk/l1jwYYiu2xcNHHipdMz40EGfM1VdamVg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@rolldown/pluginutils": "^1.0.1"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      },
      "peerDependencies": {
        "@rolldown/plugin-babel": "^0.1.7 || ^0.2.0",
        "babel-plugin-react-compiler": "^1.0.0",
        "vite": "^8.0.0"
      },
      "peerDependenciesMeta": {
        "@rolldown/plugin-babel": {
          "optional": true
        },
        "babel-plugin-react-compiler": {
          "optional": true
        }
      }
    },
    "node_modules/acorn": {
      "version": "8.17.0",
      "resolved": "https://registry.npmjs.org/acorn/-/acorn-8.17.0.tgz",
      "integrity": "sha512-xRQbDb9BnwDafYNn6Vwl839DYVjqXYb1XVGtWAZ1kcDc6iwAL4hg3B1dZlRiuENFeO2H53gFG3in621AdERVAg==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "acorn": "bin/acorn"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/acorn-jsx": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/acorn-jsx/-/acorn-jsx-5.3.2.tgz",
      "integrity": "sha512-rq9s+JNhf0IChjtDXxllJ7g41oZk5SlXtp0LHwyA5cejwn7vKmKp4pPri6YEePv2PU65sAsegbXtIinmDFDXgQ==",
      "dev": true,
      "license": "MIT",
      "peerDependencies": {
        "acorn": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/agent-base": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/agent-base/-/agent-base-6.0.2.tgz",
      "integrity": "sha512-RZNwNclF7+MS/8bDg70amg32dyeZGZxiDuQmZxKLAlQjr3jGyLx+4Kkk58UO7D2QdgFIQCovuSuZESne6RG6XQ==",
      "license": "MIT",
      "dependencies": {
        "debug": "4"
      },
      "engines": {
        "node": ">= 6.0.0"
      }
    },
    "node_modules/ajv": {
      "version": "6.15.0",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-6.15.0.tgz",
      "integrity": "sha512-fgFx7Hfoq60ytK2c7DhnF8jIvzYgOMxfugjLOSMHjLIPgenqa7S7oaagATUq99mV6IYvN2tRmC0wnTYX6iPbMw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.1",
        "fast-json-stable-stringify": "^2.0.0",
        "json-schema-traverse": "^0.4.1",
        "uri-js": "^4.2.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/asynckit": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/asynckit/-/asynckit-0.4.0.tgz",
      "integrity": "sha512-Oei9OH4tRh0YqU3GxhX79dM/mwVgvbZJaSNaRk+bshkj0S5cfHcgYakreBjrHwatXKbz+IoIdYLxrKim2MjW0Q==",
      "license": "MIT"
    },
    "node_modules/axios": {
      "version": "1.18.1",
      "resolved": "https://registry.npmjs.org/axios/-/axios-1.18.1.tgz",
      "integrity": "sha512-3nTvFlvpn9Zu/RkHUqtc7/+al4UpRW5az71ap5zccp6e8RAYEzhMTecX8Dz1wWDYrPpUoB1HAQEGEAEvUr7S9g==",
      "license": "MIT",
      "dependencies": {
        "follow-redirects": "^1.16.0",
        "form-data": "^4.0.5",
        "https-proxy-agent": "^5.0.1",
        "proxy-from-env": "^2.1.0"
      }
    },
    "node_modules/babel-plugin-macros": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/babel-plugin-macros/-/babel-plugin-macros-3.1.0.tgz",
      "integrity": "sha512-Cg7TFGpIr01vOQNODXOOaGz2NpCU5gl8x1qJFbb6hbZxR7XrcE2vtbAsTAbJ7/xwJtUuJEw8K8Zr/AE0LHlesg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.12.5",
        "cosmiconfig": "^7.0.0",
        "resolve": "^1.19.0"
      },
      "engines": {
        "node": ">=10",
        "npm": ">=6"
      }
    },
    "node_modules/balanced-match": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-4.0.4.tgz",
      "integrity": "sha512-BLrgEcRTwX2o6gGxGOCNyMvGSp35YofuYzw9h1IMTRmKqttAZZVU67bdb9Pr2vUHA8+j3i2tJfjO6C6+4myGTA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "18 || 20 || >=22"
      }
    },
    "node_modules/baseline-browser-mapping": {
      "version": "2.11.1",
      "resolved": "https://registry.npmjs.org/baseline-browser-mapping/-/baseline-browser-mapping-2.11.1.tgz",
      "integrity": "sha512-HYXq73DDpCtNzOmrFsm9eSwCvWCql0RzqjpDzXN9EadiLJ4DNat0nsZ/Bzmy+Ud12mb4/zKDY0cQ805ZzN+i0A==",
      "dev": true,
      "license": "Apache-2.0",
      "bin": {
        "baseline-browser-mapping": "dist/cli.cjs"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/brace-expansion": {
      "version": "5.0.8",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-5.0.8.tgz",
      "integrity": "sha512-JZyDyq3D4AUifKTPOB7DELf6XsB3WdPuNxCtob1vFXPsSXhdAiHBWJ/tJ8HAc9aH84BK+5JFZLNkJKx3G9kzQg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^4.0.2"
      },
      "engines": {
        "node": "20 || >=22"
      }
    },
    "node_modules/browserslist": {
      "version": "4.28.7",
      "resolved": "https://registry.npmjs.org/browserslist/-/browserslist-4.28.7.tgz",
      "integrity": "sha512-JxV13hNrFxqjOc8alRbq9dK1MM79NEXYpma2B2J4wAtpWS5zIEIKqWPGCl7N4o7Uc7B7itylh7SuDujATRyyTw==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "baseline-browser-mapping": "^2.10.44",
        "caniuse-lite": "^1.0.30001806",
        "electron-to-chromium": "^1.5.393",
        "node-releases": "^2.0.51",
        "update-browserslist-db": "^1.2.3"
      },
      "bin": {
        "browserslist": "cli.js"
      },
      "engines": {
        "node": "^6 || ^7 || ^8 || ^9 || ^10 || ^11 || ^12 || >=13.7"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/callsites": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/callsites/-/callsites-3.1.0.tgz",
      "integrity": "sha512-P8BjAsXvZS+VIDUI11hHCQEv74YT67YUi5JJFNWIqL235sBmjX4+qx9Muvls5ivyNENctx46xQLQ3aTuE7ssaQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/caniuse-lite": {
      "version": "1.0.30001806",
      "resolved": "https://registry.npmjs.org/caniuse-lite/-/caniuse-lite-1.0.30001806.tgz",
      "integrity": "sha512-72Cuvd95zbSYPKq6Fhg8eDJRlzgWDf7/mtoZv6Qe/DYNCEBdNxoA3+rZAU2ZhGCpZlns3EssFavaZomckT5Uuw==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/caniuse-lite"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "CC-BY-4.0"
    },
    "node_modules/clsx": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/clsx/-/clsx-2.1.1.tgz",
      "integrity": "sha512-eYm0QWBtUrBWZWG0d386OGAw16Z995PiOVo2B7bjWSbHedGl5e0ZWaq65kOGgUSNesEIDkB9ISbTg/JK9dhCZA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/combined-stream": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/combined-stream/-/combined-stream-1.0.8.tgz",
      "integrity": "sha512-FQN4MRfuJeHf7cBbBMJFXhKSDq+2kAArBlmRBvcvFE5BB1HZKXtSFASDhdlz9zOYwxh8lDdnvmMOe/+5cdoEdg==",
      "license": "MIT",
      "dependencies": {
        "delayed-stream": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/convert-source-map": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-2.0.0.tgz",
      "integrity": "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/cookie": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/cookie/-/cookie-1.1.1.tgz",
      "integrity": "sha512-ei8Aos7ja0weRpFzJnEA9UHJ/7XQmqglbRwnf2ATjcB9Wq874VKH9kfjjirM6UhU2/E5fFYadylyhFldcqSidQ==",
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/cosmiconfig": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/cosmiconfig/-/cosmiconfig-7.1.0.tgz",
      "integrity": "sha512-AdmX6xUzdNASswsFtmwSt7Vj8po9IuqXm0UXz7QKPuEUmPB4XyjGfaAr2PSuELMwkRMVH1EpIkX5bTZGRB3eCA==",
      "license": "MIT",
      "dependencies": {
        "@types/parse-json": "^4.0.0",
        "import-fresh": "^3.2.1",
        "parse-json": "^5.0.0",
        "path-type": "^4.0.0",
        "yaml": "^1.10.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/cosmiconfig/node_modules/yaml": {
      "version": "1.10.3",
      "resolved": "https://registry.npmjs.org/yaml/-/yaml-1.10.3.tgz",
      "integrity": "sha512-vIYeF1u3CjlhAFekPPAk2h/Kv4T3mAkMox5OymRiJQB0spDP10LHvt+K7G9Ny6NuuMAb25/6n1qyUjAcGNf/AA==",
      "license": "ISC",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/csstype": {
      "version": "3.2.3",
      "resolved": "https://registry.npmjs.org/csstype/-/csstype-3.2.3.tgz",
      "integrity": "sha512-z1HGKcYy2xA8AGQfwrn0PAy+PB7X/GSj3UVJW9qKyn43xWa+gl5nXmU4qqLMRzWVLFC8KusUX8T/0kCiOYpAIQ==",
      "license": "MIT"
    },
    "node_modules/d3-array": {
      "version": "3.2.4",
      "resolved": "https://registry.npmjs.org/d3-array/-/d3-array-3.2.4.tgz",
      "integrity": "sha512-tdQAmyA18i4J7wprpYq8ClcxZy3SC31QMeByyCFyRt7BVHdREQZ5lpzoe5mFEYZUWe+oq8HBvk9JjpibyEV4Jg==",
      "license": "ISC",
      "dependencies": {
        "internmap": "1 - 2"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-color": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/d3-color/-/d3-color-3.1.0.tgz",
      "integrity": "sha512-zg/chbXyeBtMQ1LbD/WSoW2DpC3I0mpmPdW+ynRTj/x2DAWYrIY7qeZIHidozwV24m4iavr15lNwIwLxRmOxhA==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-ease": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/d3-ease/-/d3-ease-3.0.1.tgz",
      "integrity": "sha512-wR/XK3D3XcLIZwpbvQwQ5fK+8Ykds1ip7A2Txe0yxncXSdq1L9skcG7blcedkOX+ZcgxGAmLX1FrRGbADwzi0w==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-format": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/d3-format/-/d3-format-3.1.2.tgz",
      "integrity": "sha512-AJDdYOdnyRDV5b6ArilzCPPwc1ejkHcoyFarqlPqT7zRYjhavcT3uSrqcMvsgh2CgoPbK3RCwyHaVyxYcP2Arg==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-interpolate": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/d3-interpolate/-/d3-interpolate-3.0.1.tgz",
      "integrity": "sha512-3bYs1rOD33uo8aqJfKP3JWPAibgw8Zm2+L9vBKEHJ2Rg+viTR7o5Mmv5mZcieN+FRYaAOWX5SJATX6k1PWz72g==",
      "license": "ISC",
      "dependencies": {
        "d3-color": "1 - 3"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-path": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/d3-path/-/d3-path-3.1.0.tgz",
      "integrity": "sha512-p3KP5HCf/bvjBSSKuXid6Zqijx7wIfNW+J/maPs+iwR35at5JCbLUT0LzF1cnjbCHWhqzQTIN2Jpe8pRebIEFQ==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-scale": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/d3-scale/-/d3-scale-4.0.2.tgz",
      "integrity": "sha512-GZW464g1SH7ag3Y7hXjf8RoUuAFIqklOAq3MRl4OaWabTFJY9PN/E1YklhXLh+OQ3fM9yS2nOkCoS+WLZ6kvxQ==",
      "license": "ISC",
      "dependencies": {
        "d3-array": "2.10.0 - 3",
        "d3-format": "1 - 3",
        "d3-interpolate": "1.2.0 - 3",
        "d3-time": "2.1.1 - 3",
        "d3-time-format": "2 - 4"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-shape": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/d3-shape/-/d3-shape-3.2.0.tgz",
      "integrity": "sha512-SaLBuwGm3MOViRq2ABk3eLoxwZELpH6zhl3FbAoJ7Vm1gofKx6El1Ib5z23NUEhF9AsGl7y+dzLe5Cw2AArGTA==",
      "license": "ISC",
      "dependencies": {
        "d3-path": "^3.1.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-time": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/d3-time/-/d3-time-3.1.0.tgz",
      "integrity": "sha512-VqKjzBLejbSMT4IgbmVgDjpkYrNWUYJnbCGo874u7MMKIWsILRX+OpX/gTk8MqjpT1A/c6HY2dCA77ZN0lkQ2Q==",
      "license": "ISC",
      "dependencies": {
        "d3-array": "2 - 3"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-time-format": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/d3-time-format/-/d3-time-format-4.1.0.tgz",
      "integrity": "sha512-dJxPBlzC7NugB2PDLwo9Q8JiTR3M3e4/XANkreKSUxF8vvXKqm1Yfq4Q5dl8budlunRVlUUaDUgFt7eA8D6NLg==",
      "license": "ISC",
      "dependencies": {
        "d3-time": "1 - 3"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/d3-timer": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/d3-timer/-/d3-timer-3.0.1.tgz",
      "integrity": "sha512-ndfJ/JxxMd3nw31uyKoY2naivF+r29V+Lc0svZxe1JvvIRmi8hUsrMvdOwgS1o6uBHmiz91geQ0ylPP0aj1VUA==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/decimal.js-light": {
      "version": "2.5.1",
      "resolved": "https://registry.npmjs.org/decimal.js-light/-/decimal.js-light-2.5.1.tgz",
      "integrity": "sha512-qIMFpTMZmny+MMIitAB6D7iVPEorVw6YQRWkvarTkT4tBeSLLiHzcwj6q0MmYSFCiVpiqPJTJEYIrpcPzVEIvg==",
      "license": "MIT"
    },
    "node_modules/deep-is": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/deep-is/-/deep-is-0.1.4.tgz",
      "integrity": "sha512-oIPzksmTg4/MriiaYGO+okXDT7ztn/w3Eptv/+gSIdMdKsJo0u4CfYNFJPy+4SKMuCqGw2wxnA+URMg3t8a/bQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/delayed-stream": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz",
      "integrity": "sha512-ZySD7Nf91aLB0RxL4KGrKHBXl7Eds1DAmEdcoVawXnLD7SDhpNgtuII2aAkg7a7QS41jxPSZ17p4VdGnMHk3MQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/detect-libc": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/detect-libc/-/detect-libc-2.1.2.tgz",
      "integrity": "sha512-Btj2BOOO83o3WyH59e8MgXsxEQVcarkUOpEYrubB0urwnN10yQ364rsiByU11nZlqWYZm05i/of7io4mzihBtQ==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/dom-helpers": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/dom-helpers/-/dom-helpers-5.2.1.tgz",
      "integrity": "sha512-nRCa7CK3VTrM2NmGkIy4cbK7IZlgBE/PYMn55rrXefr5xXDP0LdtfPnblFDoVdcAfslJ7or6iqAUnx0CCGIWQA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.8.7",
        "csstype": "^3.0.2"
      }
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/electron-to-chromium": {
      "version": "1.5.396",
      "resolved": "https://registry.npmjs.org/electron-to-chromium/-/electron-to-chromium-1.5.396.tgz",
      "integrity": "sha512-yHiw2Y3C3H9U6TMbOfoWK/BPreiOPXRfTWPBwQBoZG6/8TB6eOPnsy5oaRYuatR7Fw2SJ4kKforgufeo7fq0EQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/engine.io-client": {
      "version": "6.6.6",
      "resolved": "https://registry.npmjs.org/engine.io-client/-/engine.io-client-6.6.6.tgz",
      "integrity": "sha512-iY6QdftLQ9pyiPoX082bpf/u1UewnOaJrtJIF9T0++QB34lZrj0uP+Q/bj8AlUsAxqhnkTV2BS8SBZSxOmoV5Q==",
      "license": "MIT",
      "dependencies": {
        "@socket.io/component-emitter": "~3.1.0",
        "debug": "~4.4.1",
        "engine.io-parser": "~5.2.1",
        "ws": "~8.21.0",
        "xmlhttprequest-ssl": "~2.1.1"
      }
    },
    "node_modules/engine.io-parser": {
      "version": "5.2.3",
      "resolved": "https://registry.npmjs.org/engine.io-parser/-/engine.io-parser-5.2.3.tgz",
      "integrity": "sha512-HqD3yTBfnBxIrbnM1DoD6Pcq8NECnh8d4As1Qgh0z5Gg3jRRIqijury0CL3ghu/edArpUYiYqQiDUQBIs4np3Q==",
      "license": "MIT",
      "engines": {
        "node": ">=10.0.0"
      }
    },
    "node_modules/error-ex": {
      "version": "1.3.4",
      "resolved": "https://registry.npmjs.org/error-ex/-/error-ex-1.3.4.tgz",
      "integrity": "sha512-sqQamAnR14VgCr1A618A3sGrygcpK+HEbenA/HiEAkkUwcZIIB/tgWqHFxWgOyDh4nB4JCRimh79dR5Ywc9MDQ==",
      "license": "MIT",
      "dependencies": {
        "is-arrayish": "^0.2.1"
      }
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.2.tgz",
      "integrity": "sha512-HWcBoN6NileqtSydK2FqHbS/LoDd2pqrnQHLyJzBj4kOp/ky2MWMN694xOfkK8/SnUsW2DH7EfyVlydKCsm1Zw==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-set-tostringtag": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/es-set-tostringtag/-/es-set-tostringtag-2.1.0.tgz",
      "integrity": "sha512-j6vWzfrGVfyXxge+O0x5sh6cvxAog0a/4Rdd2K36zCMV5eJ+/+tOAngRO8cODMNWbVRdVlmGZQL2YS3yR8bIUA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-toolkit": {
      "version": "1.50.0",
      "resolved": "https://registry.npmjs.org/es-toolkit/-/es-toolkit-1.50.0.tgz",
      "integrity": "sha512-OyZKhUVvEep9ITEiwHn8GKnMRQIVqoSIX7WnRbkWgJkllCujilqP2rD0u979tkl8wqyc8ICwlc1UBVv/Sl1G6w==",
      "license": "MIT",
      "workspaces": [
        "docs",
        "benchmarks",
        "tests/types"
      ]
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/escape-string-regexp": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-4.0.0.tgz",
      "integrity": "sha512-TtpcNJ3XAzx3Gq8sWRzJaVajRs0uVxA2YAkdb1jm2YkPz4G6egUFAyA3n5vtEIZefPk5Wa4UXbKuS5fKkJWdgA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint": {
      "version": "10.7.0",
      "resolved": "https://registry.npmjs.org/eslint/-/eslint-10.7.0.tgz",
      "integrity": "sha512-GVTD7s1vdIl6UYvAfriOPeY1Df8LIZjfofLvHwde+erDHGGuHyuM6xoxRxmHiebhYuD2p1vN4wWh0XzPARSGDQ==",
      "dev": true,
      "license": "MIT",
      "workspaces": [
        "packages/*"
      ],
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.8.0",
        "@eslint-community/regexpp": "^4.12.2",
        "@eslint/config-array": "^0.23.5",
        "@eslint/config-helpers": "^0.6.0",
        "@eslint/core": "^1.2.1",
        "@eslint/plugin-kit": "^0.7.2",
        "@humanfs/node": "^0.16.6",
        "@humanwhocodes/module-importer": "^1.0.1",
        "@humanwhocodes/retry": "^0.4.2",
        "@types/estree": "^1.0.6",
        "ajv": "^6.14.0",
        "cross-spawn": "^7.0.6",
        "debug": "^4.3.2",
        "escape-string-regexp": "^4.0.0",
        "eslint-scope": "^9.1.2",
        "eslint-visitor-keys": "^5.0.1",
        "espree": "^11.2.0",
        "esquery": "^1.7.0",
        "esutils": "^2.0.2",
        "fast-deep-equal": "^3.1.3",
        "file-entry-cache": "^8.0.0",
        "find-up": "^5.0.0",
        "glob-parent": "^6.0.2",
        "ignore": "^5.2.0",
        "imurmurhash": "^0.1.4",
        "is-glob": "^4.0.0",
        "json-stable-stringify-without-jsonify": "^1.0.1",
        "minimatch": "^10.2.4",
        "natural-compare": "^1.4.0",
        "optionator": "^0.9.3"
      },
      "bin": {
        "eslint": "bin/eslint.js"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      },
      "funding": {
        "url": "https://eslint.org/donate"
      },
      "peerDependencies": {
        "jiti": "*"
      },
      "peerDependenciesMeta": {
        "jiti": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-plugin-react-hooks": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react-hooks/-/eslint-plugin-react-hooks-7.1.1.tgz",
      "integrity": "sha512-f2I7Gw6JbvCexzIInuSbZpfdQ44D7iqdWX01FKLvrPgqxoE7oMj8clOfto8U6vYiz4yd5oKu39rRSVOe1zRu0g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.24.4",
        "@babel/parser": "^7.24.4",
        "hermes-parser": "^0.25.1",
        "zod": "^3.25.0 || ^4.0.0",
        "zod-validation-error": "^3.5.0 || ^4.0.0"
      },
      "engines": {
        "node": ">=18"
      },
      "peerDependencies": {
        "eslint": "^3.0.0 || ^4.0.0 || ^5.0.0 || ^6.0.0 || ^7.0.0 || ^8.0.0-0 || ^9.0.0 || ^10.0.0"
      }
    },
    "node_modules/eslint-plugin-react-refresh": {
      "version": "0.5.3",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react-refresh/-/eslint-plugin-react-refresh-0.5.3.tgz",
      "integrity": "sha512-5EMmLCV98Pi4o/f/3DP/v/tNqLHMIc9I8LKClNDWhZ9JTho89/kQcitCXQBMG7sAfVRK0Ie3T2EDOzp1YXYiVA==",
      "dev": true,
      "license": "MIT",
      "peerDependencies": {
        "eslint": "^9 || ^10"
      }
    },
    "node_modules/eslint-scope": {
      "version": "9.1.2",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-9.1.2.tgz",
      "integrity": "sha512-xS90H51cKw0jltxmvmHy2Iai1LIqrfbw57b79w/J7MfvDfkIkFZ+kj6zC3BjtUwh150HsSSdxXZcsuv72miDFQ==",
      "dev": true,
      "license": "BSD-2-Clause",
      "dependencies": {
        "@types/esrecurse": "^4.3.1",
        "@types/estree": "^1.0.8",
        "esrecurse": "^4.3.0",
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-visitor-keys": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-5.0.1.tgz",
      "integrity": "sha512-tD40eHxA35h0PEIZNeIjkHoDR4YjjJp34biM0mDvplBe//mB+IHCqHDGV7pxF+7MklTvighcCPPZC7ynWyjdTA==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/espree": {
      "version": "11.2.0",
      "resolved": "https://registry.npmjs.org/espree/-/espree-11.2.0.tgz",
      "integrity": "sha512-7p3DrVEIopW1B1avAGLuCSh1jubc01H2JHc8B4qqGblmg5gI9yumBgACjWo4JlIc04ufug4xJ3SQI8HkS/Rgzw==",
      "dev": true,
      "license": "BSD-2-Clause",
      "dependencies": {
        "acorn": "^8.16.0",
        "acorn-jsx": "^5.3.2",
        "eslint-visitor-keys": "^5.0.1"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/esquery": {
      "version": "1.7.0",
      "resolved": "https://registry.npmjs.org/esquery/-/esquery-1.7.0.tgz",
      "integrity": "sha512-Ap6G0WQwcU/LHsvLwON1fAQX9Zp0A2Y6Y/cJBl9r/JbW90Zyg4/zbG6zzKa2OTALELarYHmKu0GhpM5EO+7T0g==",
      "dev": true,
      "license": "BSD-3-Clause",
      "dependencies": {
        "estraverse": "^5.1.0"
      },
      "engines": {
        "node": ">=0.10"
      }
    },
    "node_modules/esrecurse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/esrecurse/-/esrecurse-4.3.0.tgz",
      "integrity": "sha512-KmfKL3b6G+RXvP8N1vr3Tq1kL/oCFgn2NYXEtqP8/L3pKapUA4G8cFVaoF3SU323CD4XypR/ffioHmkti6/Tag==",
      "dev": true,
      "license": "BSD-2-Clause",
      "dependencies": {
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/estraverse": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-5.3.0.tgz",
      "integrity": "sha512-MMdARuVEQziNTeJD8DgMqmhwR11BRQ/cBP+pLtYdSTnf3MIO8fFeiINEbX36ZdNlfU/7A9f3gUw49B3oQsvwBA==",
      "dev": true,
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/esutils": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/esutils/-/esutils-2.0.3.tgz",
      "integrity": "sha512-kVscqXk4OCp68SZ0dkgEKVi6/8ij300KBWTJq32P/dYeWTSwK41WyTxalN1eRmA5Z9UU/LX9D7FWSmV9SAYx6g==",
      "dev": true,
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/eventemitter3": {
      "version": "5.0.4",
      "resolved": "https://registry.npmjs.org/eventemitter3/-/eventemitter3-5.0.4.tgz",
      "integrity": "sha512-mlsTRyGaPBjPedk6Bvw+aqbsXDtoAyAzm5MO7JgU+yVRyMQ5O8bD4Kcci7BS85f93veegeCPkL8R4GLClnjLFw==",
      "license": "MIT"
    },
    "node_modules/fast-deep-equal": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-deep-equal/-/fast-deep-equal-3.1.3.tgz",
      "integrity": "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/fast-json-stable-stringify": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/fast-json-stable-stringify/-/fast-json-stable-stringify-2.1.0.tgz",
      "integrity": "sha512-lhd/wF+Lk98HZoTCtlVraHtfh5XYijIjalXck7saUtuanSDyLMxnHhSXEDJqHxD7msR8D0uCmqlkwjCV8xvwHw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/fast-levenshtein": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/fast-levenshtein/-/fast-levenshtein-2.0.6.tgz",
      "integrity": "sha512-DCXu6Ifhqcks7TZKY3Hxp3y6qphY5SJZmrWMDrKcERSOXWQdMhU9Ig/PYrzyw/ul9jOIyh0N4M0tbC5hodg8dw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/file-entry-cache": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/file-entry-cache/-/file-entry-cache-8.0.0.tgz",
      "integrity": "sha512-XXTUwCvisa5oacNGRP9SfNtYBNAMi+RPwBFmblZEF7N7swHYQS6/Zfk7SRwx4D5j3CH211YNRco1DEMNVfZCnQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "flat-cache": "^4.0.0"
      },
      "engines": {
        "node": ">=16.0.0"
      }
    },
    "node_modules/find-root": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/find-root/-/find-root-1.1.0.tgz",
      "integrity": "sha512-NKfW6bec6GfKc0SGx1e07QZY9PE99u0Bft/0rzSD5k3sO/vwkVUpDUKVm5Gpp5Ue3YfShPFTX2070tDs5kB9Ng==",
      "license": "MIT"
    },
    "node_modules/find-up": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-5.0.0.tgz",
      "integrity": "sha512-78/PXT1wlLLDgTzDs7sjq9hzz0vXD+zn+7wypEe4fXQxCmdmqfGsEPQxmiCSQI3ajFV91bVSsvNtrJRiW6nGng==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "locate-path": "^6.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/flat-cache": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/flat-cache/-/flat-cache-4.0.1.tgz",
      "integrity": "sha512-f7ccFPK3SXFHpx15UIGyRJ/FJQctuKZ0zVuN3frBo4HnK3cay9VEW0R6yPYFHC0AgqhukPzKjq22t5DmAyqGyw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "flatted": "^3.2.9",
        "keyv": "^4.5.4"
      },
      "engines": {
        "node": ">=16"
      }
    },
    "node_modules/flatted": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/flatted/-/flatted-3.4.3.tgz",
      "integrity": "sha512-/zipXxyO6rGvuNGDiULY9MvEGSkb2gaG4GGH4ygMi0ZZzyMHdUZBmntJmx5x1G2VuPytCwGN4xsJP6cw+sK+vQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/follow-redirects": {
      "version": "1.16.0",
      "resolved": "https://registry.npmjs.org/follow-redirects/-/follow-redirects-1.16.0.tgz",
      "integrity": "sha512-y5rN/uOsadFT/JfYwhxRS5R7Qce+g3zG97+JrtFZlC9klX/W5hD7iiLzScI4nZqUS7DNUdhPgw4xI8W2LuXlUw==",
      "funding": [
        {
          "type": "individual",
          "url": "https://github.com/sponsors/RubenVerborgh"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=4.0"
      },
      "peerDependenciesMeta": {
        "debug": {
          "optional": true
        }
      }
    },
    "node_modules/form-data": {
      "version": "4.0.6",
      "resolved": "https://registry.npmjs.org/form-data/-/form-data-4.0.6.tgz",
      "integrity": "sha512-vKatAh4SlVfgbv+YtmhiRjhEMJsYpsG1Y2rMQtR+SVSbytsSD1YGzDIcrAJmdFec88u/+VoGmxnl+80gL1tRCQ==",
      "license": "MIT",
      "dependencies": {
        "asynckit": "^0.4.0",
        "combined-stream": "^1.0.8",
        "es-set-tostringtag": "^2.1.0",
        "hasown": "^2.0.4",
        "mime-types": "^2.1.35"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/gensync": {
      "version": "1.0.0-beta.2",
      "resolved": "https://registry.npmjs.org/gensync/-/gensync-1.0.0-beta.2.tgz",
      "integrity": "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/glob-parent": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-6.0.2.tgz",
      "integrity": "sha512-XxwI8EOhVQgWp6iDL+3b0r86f4d6AX6zSU55HfB4ydCEuXLXc5FcYeOu+nnGftS4TEju/11rt4KJPTMgbfmv4A==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.3"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/globals": {
      "version": "17.7.0",
      "resolved": "https://registry.npmjs.org/globals/-/globals-17.7.0.tgz",
      "integrity": "sha512-Czmyns5dUsq4seFBR/Kdydhmo8y9kC79hiSkPn0YcGtNnYWnrgt0vjrSjx9tspoDGWm2CMarffRuLjM4xUz8xg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/goober": {
      "version": "2.1.19",
      "resolved": "https://registry.npmjs.org/goober/-/goober-2.1.19.tgz",
      "integrity": "sha512-U7veizMqxyKlM58+Z5j2ngJBH/r9siDmxpvNxSw0PylF6WQvrASJEZrxh1hidRBJc2jqoBVSyOban5u8m+6Rxg==",
      "license": "MIT",
      "peerDependencies": {
        "csstype": "^3.0.10"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-tostringtag": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-tostringtag/-/has-tostringtag-1.0.2.tgz",
      "integrity": "sha512-NqADB8VjPFLM2V0VvHUewwwsw0ZWBaIdgo+ieHtK3hasLz4qeCRjYcqfB6AQrBggRKppKF8L52/VqdVsO47Dlw==",
      "license": "MIT",
      "dependencies": {
        "has-symbols": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.4.tgz",
      "integrity": "sha512-T2UbfbBEF32wiepXIsMlTW9+dDYC6wMh/t/vYA4tuOMKqWz/n3vr1NFSxQiyP+zk2mXsoMA/i/7qV6LKut1t1A==",
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/hermes-estree": {
      "version": "0.25.1",
      "resolved": "https://registry.npmjs.org/hermes-estree/-/hermes-estree-0.25.1.tgz",
      "integrity": "sha512-0wUoCcLp+5Ev5pDW2OriHC2MJCbwLwuRx+gAqMTOkGKJJiBCLjtrvy4PWUGn6MIVefecRpzoOZ/UV6iGdOr+Cw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/hermes-parser": {
      "version": "0.25.1",
      "resolved": "https://registry.npmjs.org/hermes-parser/-/hermes-parser-0.25.1.tgz",
      "integrity": "sha512-6pEjquH3rqaI6cYAXYPcz9MS4rY6R4ngRgrgfDshRptUZIc3lw0MCIJIGDj9++mfySOuPTHB4nrSW99BCvOPIA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "hermes-estree": "0.25.1"
      }
    },
    "node_modules/hoist-non-react-statics": {
      "version": "3.3.2",
      "resolved": "https://registry.npmjs.org/hoist-non-react-statics/-/hoist-non-react-statics-3.3.2.tgz",
      "integrity": "sha512-/gGivxi8JPKWNm/W0jSmzcMPpfpPLc3dY/6GxhX2hQ9iGj3aDfklV4ET7NjKpSinLpJ5vafa9iiGIEZg10SfBw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "react-is": "^16.7.0"
      }
    },
    "node_modules/hoist-non-react-statics/node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "license": "MIT"
    },
    "node_modules/https-proxy-agent": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/https-proxy-agent/-/https-proxy-agent-5.0.1.tgz",
      "integrity": "sha512-dFcAjpTQFgoLMzC2VwU+C/CbS7uRL0lWmxDITmqm7C+7F0Odmj6s9l6alZc6AELXhrnggM2CeWSXHGOdX2YtwA==",
      "license": "MIT",
      "dependencies": {
        "agent-base": "6",
        "debug": "4"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/ignore": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-5.3.2.tgz",
      "integrity": "sha512-hsBTNUqQTDwkWtcdYI2i06Y/nUBEsNEDJKjWdigLvegy8kDuJAS8uRlpkkcQpyEXL0Z/pjDy5HBmMjRCJ2gq+g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/immer": {
      "version": "11.1.15",
      "resolved": "https://registry.npmjs.org/immer/-/immer-11.1.15.tgz",
      "integrity": "sha512-VrNANlmnWQnh5COXIIOQXM9oOJw7naGKlBT74ZOOR6lpVXc3gFEu9FJLDFcpCJ2j+NWr8TIwtWD//T6ZX6TKiQ==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/immer"
      }
    },
    "node_modules/import-fresh": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/import-fresh/-/import-fresh-3.3.1.tgz",
      "integrity": "sha512-TR3KfrTZTYLPB6jUjfx6MF9WcWrHL9su5TObK4ZkYgBdWKPOFoSoQIdEuTuR82pmtxH2spWG9h6etwfr1pLBqQ==",
      "license": "MIT",
      "dependencies": {
        "parent-module": "^1.0.0",
        "resolve-from": "^4.0.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/imurmurhash": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/imurmurhash/-/imurmurhash-0.1.4.tgz",
      "integrity": "sha512-JmXMZ6wuvDmLiHEml9ykzqO6lwFbof0GG4IkcGaENdCRDDmMVnny7s5HsIgHCbaq0w2MyPhDqkhTUgS2LU2PHA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.8.19"
      }
    },
    "node_modules/internmap": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/internmap/-/internmap-2.0.3.tgz",
      "integrity": "sha512-5Hh7Y1wQbvY5ooGgPbDaL5iYLAPzMTUrjMulskHLH6wnv/A+1q5rgEaiuqEjB+oxGXIVZs1FF+R/KPN3ZSQYYg==",
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/is-arrayish": {
      "version": "0.2.1",
      "resolved": "https://registry.npmjs.org/is-arrayish/-/is-arrayish-0.2.1.tgz",
      "integrity": "sha512-zz06S8t0ozoDXMG+ube26zeCTNXcKIPJZJi8hBrF4idCLms4CG9QtK7qBl1boi5ODzFpjswb5JPmHCbMpjaYzg==",
      "license": "MIT"
    },
    "node_modules/is-core-module": {
      "version": "2.16.2",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.16.2.tgz",
      "integrity": "sha512-evOr8xfXKxE6qSR0hSXL2r3sd7ALj8+7jQEUvPYcm5sgZFdJ+AYzT6yNmJenvIYQBgIGwfwz08sL8zoL7yq2BA==",
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-extglob": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-extglob/-/is-extglob-2.1.1.tgz",
      "integrity": "sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-glob": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/is-glob/-/is-glob-4.0.3.tgz",
      "integrity": "sha512-xelSayHH36ZgE7ZWhli7pW34hNbNl8Ojv5KVmkJD4hBdD3th8Tfk9vYasLM+mXWOZhFkgZfxhLSnrwRr4elSSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-extglob": "^2.1.1"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/js-tokens": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz",
      "integrity": "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==",
      "license": "MIT"
    },
    "node_modules/jsesc": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/jsesc/-/jsesc-3.1.0.tgz",
      "integrity": "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA==",
      "license": "MIT",
      "bin": {
        "jsesc": "bin/jsesc"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/json-buffer": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/json-buffer/-/json-buffer-3.0.1.tgz",
      "integrity": "sha512-4bV5BfR2mqfQTJm+V5tPPdf+ZpuhiIvTuAB5g8kcrXOZpTT/QwwVRWBywX1ozr6lEuPdbHxwaJlm9G6mI2sfSQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/json-parse-even-better-errors": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/json-parse-even-better-errors/-/json-parse-even-better-errors-2.3.1.tgz",
      "integrity": "sha512-xyFwyhro/JEof6Ghe2iz2NcXoj2sloNsWr/XsERDK/oiPCfaNhl5ONfp+jQdAZRQQ0IJWNzH9zIZF7li91kh2w==",
      "license": "MIT"
    },
    "node_modules/json-schema-traverse": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-0.4.1.tgz",
      "integrity": "sha512-xbbCH5dCYU5T8LcEhhuh7HJ88HXuW3qsI3Y0zOZFKfZEHcpWiHU/Jxzk629Brsab/mMiHQti9wMP+845RPe3Vg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/json-stable-stringify-without-jsonify": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/json-stable-stringify-without-jsonify/-/json-stable-stringify-without-jsonify-1.0.1.tgz",
      "integrity": "sha512-Bdboy+l7tA3OGW6FjyFHWkP5LuByj1Tk33Ljyq0axyzdk9//JSi2u3fP1QSmd1KNwq6VOKYGlAu87CisVir6Pw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/json5": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/json5/-/json5-2.2.3.tgz",
      "integrity": "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "json5": "lib/cli.js"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/keyv": {
      "version": "4.5.4",
      "resolved": "https://registry.npmjs.org/keyv/-/keyv-4.5.4.tgz",
      "integrity": "sha512-oxVHkHR/EJf2CNXnWxRLW6mg7JyCCUcG0DtEGmL2ctUo1PNTin1PUil+r/+4r5MpVgC/fn1kjsx7mjSujKqIpw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "json-buffer": "3.0.1"
      }
    },
    "node_modules/levn": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/levn/-/levn-0.4.1.tgz",
      "integrity": "sha512-+bT2uH4E5LGE7h/n3evcS/sQlJXCpIp6ym8OWJ5eV6+67Dsql/LaaT7qJBAt2rzfoa/5QBGBhxDix1dMt2kQKQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "^1.2.1",
        "type-check": "~0.4.0"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/lightningcss": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss/-/lightningcss-1.33.0.tgz",
      "integrity": "sha512-WkUDrojuJs0xkgGf2udWxa3yGBRxPtxUkB79i6aCZLRgc7PM8fZe9TosfPDcvEpQZbuFASnHYmRLBLUbmLOIIA==",
      "dev": true,
      "license": "MPL-2.0",
      "dependencies": {
        "detect-libc": "^2.0.3"
      },
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      },
      "optionalDependencies": {
        "lightningcss-android-arm64": "1.33.0",
        "lightningcss-darwin-arm64": "1.33.0",
        "lightningcss-darwin-x64": "1.33.0",
        "lightningcss-freebsd-x64": "1.33.0",
        "lightningcss-linux-arm-gnueabihf": "1.33.0",
        "lightningcss-linux-arm64-gnu": "1.33.0",
        "lightningcss-linux-arm64-musl": "1.33.0",
        "lightningcss-linux-x64-gnu": "1.33.0",
        "lightningcss-linux-x64-musl": "1.33.0",
        "lightningcss-win32-arm64-msvc": "1.33.0",
        "lightningcss-win32-x64-msvc": "1.33.0"
      }
    },
    "node_modules/lightningcss-android-arm64": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-android-arm64/-/lightningcss-android-arm64-1.33.0.tgz",
      "integrity": "sha512-gEpRTalKdosp4Bb8qWtc2iOgE5SeIHlpS1up9bFq2wAyYhl1UdTObYiHe98zEM9SQvSoqQZ1IQD0JNpg3Ml5pg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-darwin-arm64": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-darwin-arm64/-/lightningcss-darwin-arm64-1.33.0.tgz",
      "integrity": "sha512-Sciaz8eenNTKn9b3t7+xr0ipTp9YxKQY4npwQ3mrRuL0BAVHBLyZxofhaKBAVtzmtRZ/zTyo0/to4B1uWG/Djg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-darwin-x64": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-darwin-x64/-/lightningcss-darwin-x64-1.33.0.tgz",
      "integrity": "sha512-Z5UPAxzrjlWNNyGy6i65cJzzvgJ5D3T6wMvs+gWpY9d7qRhANrxqAp6LhxIgZhWEw18RfJTGcRxjuLIBr+m8XQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-freebsd-x64": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-freebsd-x64/-/lightningcss-freebsd-x64-1.33.0.tgz",
      "integrity": "sha512-QQM/Ti/hQajJwCY+RiWuCZ9sdtI/XQk7nDK5vC8kkdwixezOlDgvDx7+RT+QjK6FcFT4MpsuoBnHIo/O3StRRg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm-gnueabihf": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm-gnueabihf/-/lightningcss-linux-arm-gnueabihf-1.33.0.tgz",
      "integrity": "sha512-N7FVBe6iS24MlM6R/4RBTxGhQheZGs7tiQ9U32UtF75NzP5Q7xWPRqLBCKxlRQRk3rY1jCIPLzx7WzOhuUIRLQ==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm64-gnu": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm64-gnu/-/lightningcss-linux-arm64-gnu-1.33.0.tgz",
      "integrity": "sha512-j2v/itmy4HlNxlc6voKXYgBqNi0Ng2LShg4z7GufpEgs05P+2suBVyi9I6YHq5uoVFx9ETin3eCEhLVyXGQnKg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-arm64-musl": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-arm64-musl/-/lightningcss-linux-arm64-musl-1.33.0.tgz",
      "integrity": "sha512-yiO5ROMuYQgXbC60yjZU5CYSFZGKXL0HFATXt9mHJn1+zW55oCtMI9NfcVhYLMFDL7gV7oBPon/EmMMGg2OvtQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-x64-gnu": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-x64-gnu/-/lightningcss-linux-x64-gnu-1.33.0.tgz",
      "integrity": "sha512-ar+Ju7LmcN0Jo4FpL4hpFybwNG9/3A/Br5KW2n2jyODg3MEZXaDYADdemoNS+BDNfMgKvylJLj4S5tyRActuAg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "libc": [
        "glibc"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-linux-x64-musl": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-linux-x64-musl/-/lightningcss-linux-x64-musl-1.33.0.tgz",
      "integrity": "sha512-RYiYbkokw0trfKqqzfF55lginwEPrD3OJDfTuJzFs1MK6iFnDenaz1fqLLtX4ITG3OktJQXOeTaw1awrBAlZPw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "libc": [
        "musl"
      ],
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-win32-arm64-msvc": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-win32-arm64-msvc/-/lightningcss-win32-arm64-msvc-1.33.0.tgz",
      "integrity": "sha512-1K+MPfLSFVpphzpdbfkhlWk6wBrTObBzS2T6db10PNOZgR9GoVsAWzwNyuhUYYbTp23j+4RrncfujZ4uAzXvwA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lightningcss-win32-x64-msvc": {
      "version": "1.33.0",
      "resolved": "https://registry.npmjs.org/lightningcss-win32-x64-msvc/-/lightningcss-win32-x64-msvc-1.33.0.tgz",
      "integrity": "sha512-OlEICDx/Xl0FqSp4bry8zFnCvGpig3Gl4gCquvYwHuqJKEC1+n9NgDniFvqHGmMv1ZkqDJrDqKKSykTDX+ehuA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MPL-2.0",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">= 12.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/parcel"
      }
    },
    "node_modules/lines-and-columns": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/lines-and-columns/-/lines-and-columns-1.2.4.tgz",
      "integrity": "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg==",
      "license": "MIT"
    },
    "node_modules/locate-path": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-6.0.0.tgz",
      "integrity": "sha512-iPZK6eYjbxRu3uB4/WZ3EsEIMJFMqAoopl3R+zuq0UjcAm/MO6KCweDgPfP3elTztoKP3KtnVHxTn2NHBSDVUw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "p-locate": "^5.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/loose-envify": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz",
      "integrity": "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q==",
      "license": "MIT",
      "dependencies": {
        "js-tokens": "^3.0.0 || ^4.0.0"
      },
      "bin": {
        "loose-envify": "cli.js"
      }
    },
    "node_modules/lru-cache": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-5.1.1.tgz",
      "integrity": "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "yallist": "^3.0.2"
      }
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/mime-db": {
      "version": "1.52.0",
      "resolved": "https://registry.npmjs.org/mime-db/-/mime-db-1.52.0.tgz",
      "integrity": "sha512-sPU4uV7dYlvtWJxwwxHD0PuihVNiE7TyAbQ5SWxDCB9mUYvOgroQOwYQQOKPJ8CIbE+1ETVlOoK1UC2nU3gYvg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mime-types": {
      "version": "2.1.35",
      "resolved": "https://registry.npmjs.org/mime-types/-/mime-types-2.1.35.tgz",
      "integrity": "sha512-ZDY+bPm5zTTF+YpCrAU9nK0UgICYPT0QtT1NZWFv4s++TNkcgVaT0g6+4R2uI4MjQjzysHB1zxuWL50hzaeXiw==",
      "license": "MIT",
      "dependencies": {
        "mime-db": "1.52.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/minimatch": {
      "version": "10.2.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-10.2.5.tgz",
      "integrity": "sha512-MULkVLfKGYDFYejP07QOurDLLQpcjk7Fw+7jXS2R2czRQzR56yHRveU5NDJEOviH+hETZKSkIk5c+T23GjFUMg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "brace-expansion": "^5.0.5"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "license": "MIT"
    },
    "node_modules/nanoid": {
      "version": "3.3.16",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.16.tgz",
      "integrity": "sha512-bzlKTyNJ7+LdGIIwy8ijFpIqEQIvafahV7eYykJ8Cvh42EdJeODoJ6gUJXpQJvej1BddH8OqTXZNE/KfbWAu8Q==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/natural-compare": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/natural-compare/-/natural-compare-1.4.0.tgz",
      "integrity": "sha512-OWND8ei3VtNC9h7V60qff3SVobHr996CTwgxubgyQYEpg290h9J0buyECNNJexkFm5sOajh5G116RYA1c8ZMSw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/node-releases": {
      "version": "2.0.51",
      "resolved": "https://registry.npmjs.org/node-releases/-/node-releases-2.0.51.tgz",
      "integrity": "sha512-wRNIrw4DmVLKQlbgOMdkMx27Wrpzes2hh5Jtbi2bjPd+4wJstWIqP5A+lscnqbm0xxmT5Bpg8Lec5ItEBwx6BQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/optionator": {
      "version": "0.9.4",
      "resolved": "https://registry.npmjs.org/optionator/-/optionator-0.9.4.tgz",
      "integrity": "sha512-6IpQ7mKUxRcZNLIObR0hz7lxsapSSIYNZJwXPGeF0mTVqGKFIXj1DQcMoT22S3ROcLyY/rz0PWaWZ9ayWmad9g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "deep-is": "^0.1.3",
        "fast-levenshtein": "^2.0.6",
        "levn": "^0.4.1",
        "prelude-ls": "^1.2.1",
        "type-check": "^0.4.0",
        "word-wrap": "^1.2.5"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/p-limit": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-3.1.0.tgz",
      "integrity": "sha512-TYOanM3wGwNGsZN2cVTYPArw454xnXj5qmWF1bEoAc4+cU/ol7GVh7odevjp1FNHduHc3KZMcFduxU5Xc6uJRQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "yocto-queue": "^0.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/p-locate": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-5.0.0.tgz",
      "integrity": "sha512-LaNjtRWUBY++zB5nE/NwcaoMylSPk+S+ZHNB1TzdbMJMny6dynpAGt7X/tl/QYq3TIeE6nxHppbo2LGymrG5Pw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "p-limit": "^3.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/parent-module": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/parent-module/-/parent-module-1.0.1.tgz",
      "integrity": "sha512-GQ2EWRpQV8/o+Aw8YqtfZZPfNRWZYkbidE9k5rpl/hC3vtHHBfGm2Ifi6qWV+coDGkrUKZAxE3Lot5kcsRlh+g==",
      "license": "MIT",
      "dependencies": {
        "callsites": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/parse-json": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/parse-json/-/parse-json-5.2.0.tgz",
      "integrity": "sha512-ayCKvm/phCGxOkYRSCM82iDwct8/EonSEgCSxWxD7ve6jHggsFl4fZVQBPRNgQoKiuV/odhFrGzQXZwbifC8Rg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.0.0",
        "error-ex": "^1.3.1",
        "json-parse-even-better-errors": "^2.3.0",
        "lines-and-columns": "^1.1.6"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/path-exists": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-exists/-/path-exists-4.0.0.tgz",
      "integrity": "sha512-ak9Qy5Q7jYb2Wwcey5Fpvg2KoAc/ZIhLSLOSBmRmygPsGwkVVt0fZa0qrtMz+m6tJTAHfZQ8FnmB4MG4LWy7/w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "license": "MIT"
    },
    "node_modules/path-type": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-type/-/path-type-4.0.0.tgz",
      "integrity": "sha512-gDKb8aZMDeD/tZWs9P6+q0J9Mwkdl6xMV8TjnGP3qJVJ06bdMgkbBlLU8IdfOsIsFz2BW1rNVT3XuNEl8zPAvw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "4.0.5",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.5.tgz",
      "integrity": "sha512-RvwwcruNjI1ncT5xRakeyS9Lf8lcItv34KD+aif+VH9kduAyfYBipGh12274xtenIPZ119/R9BdTBa8gAwSh0A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.23",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.23.tgz",
      "integrity": "sha512-g50586zr4bZmwFiTlflMu8E0bDTb5I5gertgwAKmsdUlTQIhZtunzUlD1WSzwcVWPoAVpsrA6vlfCD7oXvRwgg==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.16",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/prelude-ls": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/prelude-ls/-/prelude-ls-1.2.1.tgz",
      "integrity": "sha512-vkcDPrRZo1QZLbn5RLGPpg/WmIQ65qoWWhcGKf/b5eplkkarX0m9z8ppCat4mlOqUsWpyNuYgO3VRyrYHSzX5g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/prop-types": {
      "version": "15.8.1",
      "resolved": "https://registry.npmjs.org/prop-types/-/prop-types-15.8.1.tgz",
      "integrity": "sha512-oj87CgZICdulUohogVAR7AjlC0327U4el4L6eAvOqCeudMDVU0NThNaV+b9Df4dXgSP1gXMTnPdhfe/2qDH5cg==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.4.0",
        "object-assign": "^4.1.1",
        "react-is": "^16.13.1"
      }
    },
    "node_modules/prop-types/node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "license": "MIT"
    },
    "node_modules/proxy-from-env": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/proxy-from-env/-/proxy-from-env-2.1.0.tgz",
      "integrity": "sha512-cJ+oHTW1VAEa8cJslgmUZrc+sjRKgAKl3Zyse6+PV38hZe/V6Z14TbCuXcan9F9ghlz4QrFr2c92TNF82UkYHA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/punycode": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/punycode/-/punycode-2.3.1.tgz",
      "integrity": "sha512-vYt7UD1U9Wg6138shLtLOvdAu+8DsC/ilFtEVHcH+wydcSpNE20AfSOduf6MkRFahL5FY7X1oU7nKVZFtfq8Fg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/react": {
      "version": "19.2.8",
      "resolved": "https://registry.npmjs.org/react/-/react-19.2.8.tgz",
      "integrity": "sha512-PWaYA1L/q9u2u7xYQi+Y3L3Yfnie7XyLeaJICV1MGD6LprsBxcAqGjYyr0eY3p+QdsA+x/Irkt4Qif8D63+Sbw==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-dom": {
      "version": "19.2.8",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-19.2.8.tgz",
      "integrity": "sha512-rVprimfGBG3DR+Tq0IQG2DT5PxKth1WIGDmj5yPmlzr4YBe7uyE+Du4oVqTDXZSHGGGXRtTJEGSSePyQCMBglQ==",
      "license": "MIT",
      "dependencies": {
        "scheduler": "^0.27.0"
      },
      "peerDependencies": {
        "react": "^19.2.8"
      }
    },
    "node_modules/react-hot-toast": {
      "version": "2.6.0",
      "resolved": "https://registry.npmjs.org/react-hot-toast/-/react-hot-toast-2.6.0.tgz",
      "integrity": "sha512-bH+2EBMZ4sdyou/DPrfgIouFpcRLCJ+HoCA32UoAYHn6T3Ur5yfcDCeSr5mwldl6pFOsiocmrXMuoCJ1vV8bWg==",
      "license": "MIT",
      "dependencies": {
        "csstype": "^3.1.3",
        "goober": "^2.1.16"
      },
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "react": ">=16",
        "react-dom": ">=16"
      }
    },
    "node_modules/react-is": {
      "version": "19.2.8",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-19.2.8.tgz",
      "integrity": "sha512-s5un28nYxKJw5gvUHyW5PCC28CvBqLu9r3cWgzHT4Vo/5fqqkFcdRYsGcKf50WMPpjjFZS5d76fn3YCo2njKwQ==",
      "license": "MIT"
    },
    "node_modules/react-redux": {
      "version": "9.3.0",
      "resolved": "https://registry.npmjs.org/react-redux/-/react-redux-9.3.0.tgz",
      "integrity": "sha512-KQopgqFo/p/fgmAs5qz6p5RWaNAzq40WAu7fJIXnQpYxFPbJYtsJPWvGeF2rOBaY/kEuV77AVsX8TsQzKm+A/g==",
      "license": "MIT",
      "dependencies": {
        "@types/use-sync-external-store": "^0.0.6",
        "use-sync-external-store": "^1.4.0"
      },
      "peerDependencies": {
        "@types/react": "^18.2.25 || ^19",
        "react": "^18.0 || ^19",
        "redux": "^5.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        },
        "redux": {
          "optional": true
        }
      }
    },
    "node_modules/react-router": {
      "version": "7.18.1",
      "resolved": "https://registry.npmjs.org/react-router/-/react-router-7.18.1.tgz",
      "integrity": "sha512-GDLgg3i3uM0aeJO3Fm+TCS+sDQ7gu12T6x0qdTEzcwqEfleci7JwugVNIF3U//0FWKnJT7ptG+20B2jfDqnZAg==",
      "license": "MIT",
      "dependencies": {
        "cookie": "^1.0.1",
        "set-cookie-parser": "^2.6.0"
      },
      "engines": {
        "node": ">=20.0.0"
      },
      "peerDependencies": {
        "react": ">=18",
        "react-dom": ">=18"
      },
      "peerDependenciesMeta": {
        "react-dom": {
          "optional": true
        }
      }
    },
    "node_modules/react-router-dom": {
      "version": "7.18.1",
      "resolved": "https://registry.npmjs.org/react-router-dom/-/react-router-dom-7.18.1.tgz",
      "integrity": "sha512-KaZh+X/6UtEp28x51AUYZDMg9NGoz2ja3dNHa+ta/tk40vCzKhQ/RypCWBMLbmDr6//E24Vv5uPsrqXFozdkAg==",
      "license": "MIT",
      "dependencies": {
        "react-router": "7.18.1"
      },
      "engines": {
        "node": ">=20.0.0"
      },
      "peerDependencies": {
        "react": ">=18",
        "react-dom": ">=18"
      }
    },
    "node_modules/react-transition-group": {
      "version": "4.4.5",
      "resolved": "https://registry.npmjs.org/react-transition-group/-/react-transition-group-4.4.5.tgz",
      "integrity": "sha512-pZcd1MCJoiKiBR2NRxeCRg13uCXbydPnmB4EOeRrY7480qNWO8IIgQG6zlDkm6uRMsURXPuKq0GWtiM59a5Q6g==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@babel/runtime": "^7.5.5",
        "dom-helpers": "^5.0.1",
        "loose-envify": "^1.4.0",
        "prop-types": "^15.6.2"
      },
      "peerDependencies": {
        "react": ">=16.6.0",
        "react-dom": ">=16.6.0"
      }
    },
    "node_modules/recharts": {
      "version": "3.10.0",
      "resolved": "https://registry.npmjs.org/recharts/-/recharts-3.10.0.tgz",
      "integrity": "sha512-wulMvfncpIlmu2uFtRU/mE5/+NiVtASXkw2KdwJTdHs3WsASX0WxZlX+rpKgyn5BDbIhkPtCpUKkB9XNK5KE0w==",
      "license": "MIT",
      "workspaces": [
        "www"
      ],
      "dependencies": {
        "@reduxjs/toolkit": "^1.9.0 || 2.x.x",
        "clsx": "^2.1.1",
        "decimal.js-light": "^2.5.1",
        "es-toolkit": "^1.39.3",
        "eventemitter3": "^5.0.1",
        "immer": "^11.1.8",
        "react-redux": "8.x.x || 9.x.x",
        "reselect": "5.2.0",
        "tiny-invariant": "^1.3.3",
        "use-sync-external-store": "^1.2.2",
        "victory-vendor": "^37.0.2"
      },
      "engines": {
        "node": ">=18"
      },
      "peerDependencies": {
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^16.0.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-is": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0"
      }
    },
    "node_modules/redux": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/redux/-/redux-5.0.1.tgz",
      "integrity": "sha512-M9/ELqF6fy8FwmkpnF0S3YKOqMyoWJ4+CS5Efg2ct3oY9daQvd/Pc71FpGZsVsbl3Cpb+IIcjBDUnnyBdQbq4w==",
      "license": "MIT"
    },
    "node_modules/redux-thunk": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/redux-thunk/-/redux-thunk-3.1.0.tgz",
      "integrity": "sha512-NW2r5T6ksUKXCabzhL9z+h206HQw/NJkcLm1GPImRQ8IzfXwRGqjVhKJGauHirT0DAuyy6hjdnMZaRoAcy0Klw==",
      "license": "MIT",
      "peerDependencies": {
        "redux": "^5.0.0"
      }
    },
    "node_modules/reselect": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/reselect/-/reselect-5.2.0.tgz",
      "integrity": "sha512-AgZ3UOZm3YndfrJ4OYjgrT7bmCm/1iqkjvEfH/oYjzh6PD2qw4QuT3jjnXIrpdt4MTpMXclMT3lXbmRY+XRakw==",
      "license": "MIT"
    },
    "node_modules/resolve": {
      "version": "1.22.12",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.12.tgz",
      "integrity": "sha512-TyeJ1zif53BPfHootBGwPRYT1RUt6oGWsaQr8UyZW/eAm9bKoijtvruSDEmZHm92CwS9nj7/fWttqPCgzep8CA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "is-core-module": "^2.16.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/resolve-from": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/resolve-from/-/resolve-from-4.0.0.tgz",
      "integrity": "sha512-pb/MYmXstAkysRFx8piNI1tGFNQIFA3vkE3Gq4EuA1dF6gHp/+vgZqsCGJapvy8N3Q+4o7FwvquPJcnZ7RYy4g==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/rolldown": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/rolldown/-/rolldown-1.1.5.tgz",
      "integrity": "sha512-t9z29cJjXf/vxQ8dyhCSpt6H6aSwHTk8cT5I3iy6SMXuFpk5mB6PL6XfC8PCwrPTx93udwKUm9HRteAlTGBLiA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@oxc-project/types": "=0.139.0",
        "@rolldown/pluginutils": "^1.0.0"
      },
      "bin": {
        "rolldown": "bin/cli.mjs"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      },
      "optionalDependencies": {
        "@rolldown/binding-android-arm64": "1.1.5",
        "@rolldown/binding-darwin-arm64": "1.1.5",
        "@rolldown/binding-darwin-x64": "1.1.5",
        "@rolldown/binding-freebsd-x64": "1.1.5",
        "@rolldown/binding-linux-arm-gnueabihf": "1.1.5",
        "@rolldown/binding-linux-arm64-gnu": "1.1.5",
        "@rolldown/binding-linux-arm64-musl": "1.1.5",
        "@rolldown/binding-linux-ppc64-gnu": "1.1.5",
        "@rolldown/binding-linux-s390x-gnu": "1.1.5",
        "@rolldown/binding-linux-x64-gnu": "1.1.5",
        "@rolldown/binding-linux-x64-musl": "1.1.5",
        "@rolldown/binding-openharmony-arm64": "1.1.5",
        "@rolldown/binding-wasm32-wasi": "1.1.5",
        "@rolldown/binding-win32-arm64-msvc": "1.1.5",
        "@rolldown/binding-win32-x64-msvc": "1.1.5"
      }
    },
    "node_modules/scheduler": {
      "version": "0.27.0",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.27.0.tgz",
      "integrity": "sha512-eNv+WrVbKu1f3vbYJT/xtiF5syA5HPIMtf9IgY/nKg0sWqzAUEvqY/xm7OcZc/qafLx/iO9FgOmeSAp4v5ti/Q==",
      "license": "MIT"
    },
    "node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "dev": true,
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/set-cookie-parser": {
      "version": "2.7.2",
      "resolved": "https://registry.npmjs.org/set-cookie-parser/-/set-cookie-parser-2.7.2.tgz",
      "integrity": "sha512-oeM1lpU/UvhTxw+g3cIfxXHyJRc/uidd3yK1P242gzHds0udQBYzs3y8j4gCCW+ZJ7ad0yctld8RYO+bdurlvw==",
      "license": "MIT"
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/socket.io-client": {
      "version": "4.8.3",
      "resolved": "https://registry.npmjs.org/socket.io-client/-/socket.io-client-4.8.3.tgz",
      "integrity": "sha512-uP0bpjWrjQmUt5DTHq9RuoCBdFJF10cdX9X+a368j/Ft0wmaVgxlrjvK3kjvgCODOMMOz9lcaRzxmso0bTWZ/g==",
      "license": "MIT",
      "dependencies": {
        "@socket.io/component-emitter": "~3.1.0",
        "debug": "~4.4.1",
        "engine.io-client": "~6.6.1",
        "socket.io-parser": "~4.2.4"
      },
      "engines": {
        "node": ">=10.0.0"
      }
    },
    "node_modules/socket.io-parser": {
      "version": "4.2.7",
      "resolved": "https://registry.npmjs.org/socket.io-parser/-/socket.io-parser-4.2.7.tgz",
      "integrity": "sha512-IH/iSeO9T6gz1KkFleGDWkG9N3dl4jXVYUtMhIqH10Md0ttMer8nUNWiP1DKuNrybD2xBrixLJdCC9J6ECoYkg==",
      "license": "MIT",
      "dependencies": {
        "@socket.io/component-emitter": "~3.1.0",
        "debug": "~4.4.1"
      },
      "engines": {
        "node": ">=10.0.0"
      }
    },
    "node_modules/source-map": {
      "version": "0.5.7",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.5.7.tgz",
      "integrity": "sha512-LbrmJOMUSdEVxIKvdcJzQC+nQhe8FUZQTXQy6+I75skNgn3OoQ0DZA8YnFa7gp8tqtL3KPf1kmo0R5DoApeSGQ==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "dev": true,
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/stylis": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/stylis/-/stylis-4.2.0.tgz",
      "integrity": "sha512-Orov6g6BB1sDfYgzWfTHDOxamtX1bE/zo104Dh9e6fqJ3PooipYyfJ0pUmrZO2wAvO8YbEyeFrkV91XTsGMSrw==",
      "license": "MIT"
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/tiny-invariant": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/tiny-invariant/-/tiny-invariant-1.3.3.tgz",
      "integrity": "sha512-+FbBPE1o9QAYvviau/qC5SE3caw21q3xkvWKBtja5vgqOWIHHJ3ioaq1VPfn/Szqctz2bU/oYeKd9/z5BL+PVg==",
      "license": "MIT"
    },
    "node_modules/tinyglobby": {
      "version": "0.2.17",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.17.tgz",
      "integrity": "sha512-wXR/dYpcqKmfWpEdZjiKJOwCNFndD0DMnrW/cYjVGttEkBfVgcLFHoNrlj47mjOVic9yyNu65alsgF4NQyTa2g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.4"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/tslib": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-2.8.1.tgz",
      "integrity": "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w==",
      "dev": true,
      "license": "0BSD",
      "optional": true
    },
    "node_modules/type-check": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/type-check/-/type-check-0.4.0.tgz",
      "integrity": "sha512-XleUoc9uwGXqjWwXaUTZAmzMcFZ5858QA2vvx1Ur5xIcixXIP+8LnFDgRplU30us6teqdlskFfu+ae4K79Ooew==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/update-browserslist-db": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/update-browserslist-db/-/update-browserslist-db-1.2.3.tgz",
      "integrity": "sha512-Js0m9cx+qOgDxo0eMiFGEueWztz+d4+M3rGlmKPT+T4IS/jP4ylw3Nwpu6cpTTP8R1MAC1kF4VbdLt3ARf209w==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "escalade": "^3.2.0",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "update-browserslist-db": "cli.js"
      },
      "peerDependencies": {
        "browserslist": ">= 4.21.0"
      }
    },
    "node_modules/uri-js": {
      "version": "4.4.1",
      "resolved": "https://registry.npmjs.org/uri-js/-/uri-js-4.4.1.tgz",
      "integrity": "sha512-7rKUyy33Q1yc98pQ1DAmLtwX109F7TIfWlW1Ydo8Wl1ii1SeHieeh0HHfPeL2fMXK6z0s8ecKs9frCuLJvndBg==",
      "dev": true,
      "license": "BSD-2-Clause",
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/use-sync-external-store": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/use-sync-external-store/-/use-sync-external-store-1.6.0.tgz",
      "integrity": "sha512-Pp6GSwGP/NrPIrxVFAIkOQeyw8lFenOHijQWkUTrDvrF4ALqylP2C/KCkeS9dpUM3KvYRQhna5vt7IL95+ZQ9w==",
      "license": "MIT",
      "peerDependencies": {
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0"
      }
    },
    "node_modules/victory-vendor": {
      "version": "37.3.6",
      "resolved": "https://registry.npmjs.org/victory-vendor/-/victory-vendor-37.3.6.tgz",
      "integrity": "sha512-SbPDPdDBYp+5MJHhBCAyI7wKM3d5ivekigc2Dk2s7pgbZ9wIgIBYGVw4zGHBml/qTFbexrofXW6Gu4noGxrOwQ==",
      "license": "MIT AND ISC",
      "dependencies": {
        "@types/d3-array": "^3.0.3",
        "@types/d3-ease": "^3.0.0",
        "@types/d3-interpolate": "^3.0.1",
        "@types/d3-scale": "^4.0.2",
        "@types/d3-shape": "^3.1.0",
        "@types/d3-time": "^3.0.0",
        "@types/d3-timer": "^3.0.0",
        "d3-array": "^3.1.6",
        "d3-ease": "^3.0.1",
        "d3-interpolate": "^3.0.1",
        "d3-scale": "^4.0.2",
        "d3-shape": "^3.1.0",
        "d3-time": "^3.0.0",
        "d3-timer": "^3.0.1"
      }
    },
    "node_modules/vite": {
      "version": "8.1.5",
      "resolved": "https://registry.npmjs.org/vite/-/vite-8.1.5.tgz",
      "integrity": "sha512-7ULLwsCdYx/nRyrpiEwvqb5TFHrMVZyBt+rg/OAXT7rgj/z+DtTDyKFeLAdDkubDVDKD8jOsndmy7m55XcfUsw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "lightningcss": "^1.32.0",
        "picomatch": "^4.0.5",
        "postcss": "^8.5.17",
        "rolldown": "~1.1.5",
        "tinyglobby": "^0.2.17"
      },
      "bin": {
        "vite": "bin/vite.js"
      },
      "engines": {
        "node": "^20.19.0 || >=22.12.0"
      },
      "funding": {
        "url": "https://github.com/vitejs/vite?sponsor=1"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.3"
      },
      "peerDependencies": {
        "@types/node": "^20.19.0 || >=22.12.0",
        "@vitejs/devtools": "^0.3.0",
        "esbuild": "^0.27.0 || ^0.28.0",
        "jiti": ">=1.21.0",
        "less": "^4.0.0",
        "sass": "^1.70.0",
        "sass-embedded": "^1.70.0",
        "stylus": ">=0.54.8",
        "sugarss": "^5.0.0",
        "terser": "^5.16.0",
        "tsx": "^4.8.1",
        "yaml": "^2.4.2"
      },
      "peerDependenciesMeta": {
        "@types/node": {
          "optional": true
        },
        "@vitejs/devtools": {
          "optional": true
        },
        "esbuild": {
          "optional": true
        },
        "jiti": {
          "optional": true
        },
        "less": {
          "optional": true
        },
        "sass": {
          "optional": true
        },
        "sass-embedded": {
          "optional": true
        },
        "stylus": {
          "optional": true
        },
        "sugarss": {
          "optional": true
        },
        "terser": {
          "optional": true
        },
        "tsx": {
          "optional": true
        },
        "yaml": {
          "optional": true
        }
      }
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/word-wrap": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/word-wrap/-/word-wrap-1.2.5.tgz",
      "integrity": "sha512-BN22B5eaMMI9UMtjrGd5g5eCYPpCPDUy0FJXbYsaT5zYxjFOckS53SQDE3pWkVoWpHXVb3BrYcEN4Twa55B5cA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/ws": {
      "version": "8.21.1",
      "resolved": "https://registry.npmjs.org/ws/-/ws-8.21.1.tgz",
      "integrity": "sha512-+0NTnW77fFN/DjQi6k/Sq/Yvk4Sgajw7urW8V+asjXnRgDs9gyGkdb7EzgfhA4goXsRIZKE28fzIXBHEzhuiWw==",
      "license": "MIT",
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "bufferutil": "^4.0.1",
        "utf-8-validate": ">=5.0.2"
      },
      "peerDependenciesMeta": {
        "bufferutil": {
          "optional": true
        },
        "utf-8-validate": {
          "optional": true
        }
      }
    },
    "node_modules/xmlhttprequest-ssl": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/xmlhttprequest-ssl/-/xmlhttprequest-ssl-2.1.2.tgz",
      "integrity": "sha512-TEU+nJVUUnA4CYJFLvK5X9AOeH4KvDvhIfm0vV1GaQRtchnG0hgK5p8hw/xjv8cunWYCsiPCSDzObPyhEwq3KQ==",
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/yallist": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/yallist/-/yallist-3.1.1.tgz",
      "integrity": "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/yocto-queue": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/yocto-queue/-/yocto-queue-0.1.0.tgz",
      "integrity": "sha512-rVksvsnNCdJ/ohGc6xgPwyN8eheCxsiLM8mxuE/t/mOVqJewPuO1miLpTHQiRgTKCLexL4MeAFVagts7HmNZ2Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/zod": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/zod/-/zod-4.4.3.tgz",
      "integrity": "sha512-ytENFjIJFl2UwYglde2jchW2Hwm4GJFLDiSXWdTrJQBIN9Fcyp7n4DhxJEiWNAJMV1/BqWfW/kkg71UDcHJyTQ==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/colinhacks"
      }
    },
    "node_modules/zod-validation-error": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/zod-validation-error/-/zod-validation-error-4.0.2.tgz",
      "integrity": "sha512-Q6/nZLe6jxuU80qb/4uJ4t5v2VEZ44lzQjPDhYJNztRQ4wyWc6VF3D3Kb/fAuPetZQnhS3hnajCf9CsWesghLQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18.0.0"
      },
      "peerDependencies": {
        "zod": "^3.25.0 || ^4.0.0"
      }
    }
  }
}
```

## frontend/package.json

**Folder path:** `frontend`

**File path:** `frontend/package.json`

```json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "@emotion/react": "^11.14.0",
    "@emotion/styled": "^11.14.1",
    "@mui/icons-material": "^9.2.0",
    "@mui/lab": "^9.0.0-beta.6",
    "@mui/material": "^9.2.0",
    "axios": "^1.18.1",
    "react": "^19.2.7",
    "react-dom": "^19.2.7",
    "react-hot-toast": "^2.6.0",
    "react-router-dom": "^7.18.1",
    "recharts": "^3.10.0",
    "socket.io-client": "^4.8.3"
  },
  "devDependencies": {
    "@eslint/js": "^10.0.1",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^6.0.3",
    "eslint": "^10.6.0",
    "eslint-plugin-react-hooks": "^7.1.1",
    "eslint-plugin-react-refresh": "^0.5.3",
    "globals": "^17.7.0",
    "vite": "^8.1.1"
  }
}
```

## frontend/README.md

**Folder path:** `frontend`

**File path:** `frontend/README.md`

```markdown
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
```

## frontend/src/api/client.js

**Folder path:** `frontend/src/api`

**File path:** `frontend/src/api/client.js`

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response [${response.config.url}]:`, response.data);
    return response;
  },
  (error) => {
    console.error(`❌ API Error [${error.config?.url}]:`, error.message);
    return Promise.reject(error);
  }
);

// ============================================
// ASSETS
// ============================================
export const getAssets = () => api.get('/assets');
export const getAssetHealth = (assetId) => api.get(`/assets/${assetId}`);

// ============================================
// TELEMETRY
// ============================================
export const getTelemetry = (assetId, limit = 30) =>
  api.get(`/telemetry/${assetId}?limit=${limit}`);

// ============================================
// INCIDENTS
// ============================================
export const getIncidents = () => api.get('/incidents');
export const triggerIncident = (type) =>
  api.post(`/incidents/${encodeURIComponent(type)}`);

// ============================================
// AGENTS
// ============================================
export const getAgents = () => api.get('/agents');
export const getAgentMetrics = () => api.get('/agent-metrics');
export const getAgentActivity = () => api.get('/agent-activity');

// ============================================
// MAINTENANCE
// ============================================
export const getMaintenancePlan = () => api.get('/maintenance');

// ============================================
// PREDICTIONS
// ============================================
export const getPredictions = (assetId, horizon = 14) =>
  api.get(`/predictions/${assetId}?horizon=${horizon}`);

// ============================================
// DASHBOARD
// ============================================
export const getDashboard = () => api.get('/dashboard');

// ============================================
// REPORTS
// ============================================
export const getReports = () => api.get('/reports');

// ============================================
// DIGITAL TWIN
// ============================================
export const getTwinAssets = () => api.get('/twin-assets');

export default api;
```

## frontend/src/App.css

**Folder path:** `frontend/src`

**File path:** `frontend/src/App.css`

```css
.counter {
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 5px;
  color: var(--accent);
  background: var(--accent-bg);
  border: 2px solid transparent;
  transition: border-color 0.3s;
  margin-bottom: 24px;

  &:hover {
    border-color: var(--accent-border);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

.hero {
  position: relative;

  .base,
  .framework,
  .vite {
    inset-inline: 0;
    margin: 0 auto;
  }

  .base {
    width: 170px;
    position: relative;
    z-index: 0;
  }

  .framework,
  .vite {
    position: absolute;
  }

  .framework {
    z-index: 1;
    top: 34px;
    height: 28px;
    transform: perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg)
      scale(1.4);
  }

  .vite {
    z-index: 0;
    top: 107px;
    height: 26px;
    width: auto;
    transform: perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg)
      scale(0.8);
  }
}

#center {
  display: flex;
  flex-direction: column;
  gap: 25px;
  place-content: center;
  place-items: center;
  flex-grow: 1;

  @media (max-width: 1024px) {
    padding: 32px 20px 24px;
    gap: 18px;
  }
}

#next-steps {
  display: flex;
  border-top: 1px solid var(--border);
  text-align: left;

  & > div {
    flex: 1 1 0;
    padding: 32px;
    @media (max-width: 1024px) {
      padding: 24px 20px;
    }
  }

  .icon {
    margin-bottom: 16px;
    width: 22px;
    height: 22px;
  }

  @media (max-width: 1024px) {
    flex-direction: column;
    text-align: center;
  }
}

#docs {
  border-right: 1px solid var(--border);

  @media (max-width: 1024px) {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
}

#next-steps ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 8px;
  margin: 32px 0 0;

  .logo {
    height: 18px;
  }

  a {
    color: var(--text-h);
    font-size: 16px;
    border-radius: 6px;
    background: var(--social-bg);
    display: flex;
    padding: 6px 12px;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    transition: box-shadow 0.3s;

    &:hover {
      box-shadow: var(--shadow);
    }
    .button-icon {
      height: 18px;
      width: 18px;
    }
  }

  @media (max-width: 1024px) {
    margin-top: 20px;
    flex-wrap: wrap;
    justify-content: center;

    li {
      flex: 1 1 calc(50% - 8px);
    }

    a {
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
    }
  }
}

#spacer {
  height: 88px;
  border-top: 1px solid var(--border);
  @media (max-width: 1024px) {
    height: 48px;
  }
}

.ticks {
  position: relative;
  width: 100%;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: -4.5px;
    border: 5px solid transparent;
  }

  &::before {
    left: 0;
    border-left-color: var(--border);
  }
  &::after {
    right: 0;
    border-right-color: var(--border);
  }
}
```

## frontend/src/App.jsx

**Folder path:** `frontend/src`

**File path:** `frontend/src/App.jsx`

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Toaster } from 'react-hot-toast';
import { theme } from './styles/theme';
import { Layout } from './components/Layout/Layout';
import { useWebSocket } from './hooks/useWebSocket';
import { useEffect } from 'react';
import toast from 'react-hot-toast';

// Pages
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import IncidentSimulator from './pages/IncidentSimulator';
import AgentMonitor from './pages/AgentMonitor';
import AIActivity from './pages/AIActivity';
import MaintenancePlanner from './pages/MaintenancePlanner';
import HealthPrediction from './pages/HealthPrediction';
import DigitalTwin from './pages/DigitalTwin';
import Reports from './pages/Reports';

function App() {
  const { data } = useWebSocket();

  // ✅ Show toast notifications when incidents happen
  useEffect(() => {
    if (data?.notifications && data.notifications.length > 0) {
      const latest = data.notifications[0];
      const emoji = {
        critical: '🔴',
        warning: '🟠',
        success: '🟢',
        info: '🔵',
      }[latest.severity] || '🔵';
      
      toast(`${emoji} ${latest.title}`, {
        duration: 4000,
        icon: emoji,
        style: {
          background: '#0d1728',
          color: '#e8f0ff',
          border: '1px solid #55D6FF33',
          borderRadius: '8px',
          padding: '10px 14px',
          maxWidth: '340px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
        },
      });
    }
  }, [data]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#0d1728',
            color: '#e8f0ff',
            border: '1px solid #55D6FF33',
            borderRadius: '8px',
            padding: '10px 14px',
            maxWidth: '340px',
            boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
          },
        }}
      />
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/incident-simulator" element={<IncidentSimulator />} />
            <Route path="/agent-monitor" element={<AgentMonitor />} />
            <Route path="/ai-activity" element={<AIActivity />} />
            <Route path="/maintenance" element={<MaintenancePlanner />} />
            <Route path="/health-prediction" element={<HealthPrediction />} />
            <Route path="/digital-twin" element={<DigitalTwin />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
```

## frontend/src/components/Layout/Header.jsx

**Folder path:** `frontend/src/components/Layout`

**File path:** `frontend/src/components/Layout/Header.jsx`

```jsx
import { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Badge,
  Chip,
} from '@mui/material';
import { Menu, NotificationsOutlined, FiberManualRecord } from '@mui/icons-material';

export function Header({ drawerWidth }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <AppBar
      position="fixed"
      sx={{
        width: { sm: `calc(100% - ${drawerWidth}px)` },
        ml: { sm: `${drawerWidth}px` },
        background: 'rgba(10, 15, 26, 0.92)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid rgba(56, 78, 112, 0.08)',
        boxShadow: 'none',
      }}
    >
      <Toolbar sx={{ minHeight: 56, justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => setMobileOpen(!mobileOpen)}
            sx={{ display: { sm: 'none' }, color: '#8899B4' }}
          >
            <Menu />
          </IconButton>

          <Typography
            variant="h6"
            noWrap
            sx={{
              color: '#E8EDF5',
              fontWeight: 600,
              letterSpacing: '-0.02em',
              fontSize: '1rem',
              display: { xs: 'none', sm: 'block' },
            }}
          >
            RIGOS
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Chip
            icon={<FiberManualRecord sx={{ fontSize: 10, color: '#10B981' }} />}
            label="OPERATIONAL"
            size="small"
            sx={{
              bgcolor: 'rgba(16, 185, 129, 0.08)',
              color: '#10B981',
              border: '1px solid rgba(16, 185, 129, 0.15)',
              fontWeight: 500,
              fontSize: '0.65rem',
              height: 24,
              '& .MuiChip-label': { px: 1.5 },
              display: { xs: 'none', sm: 'flex' },
            }}
          />

          <IconButton color="inherit" sx={{ color: '#8899B4' }}>
            <Badge badgeContent={0} color="error" sx={{ '& .MuiBadge-badge': { bgcolor: '#EF4444', fontSize: 9, height: 16, minWidth: 16 } }}>
              <NotificationsOutlined sx={{ fontSize: 20 }} />
            </Badge>
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
```

## frontend/src/components/Layout/Layout.jsx

**Folder path:** `frontend/src/components/Layout`

**File path:** `frontend/src/components/Layout/Layout.jsx`

```jsx
import { Box } from '@mui/material';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

const drawerWidth = 240;

export function Layout({ children }) {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Header drawerWidth={drawerWidth} />
      <Sidebar drawerWidth={drawerWidth} />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          ml: { sm: `${drawerWidth}px` },
          background: 'radial-gradient(circle at 85% -10%, #182e52 0, #0b1220 34%, #070b13 72%)',
          minHeight: '100vh',
        }}
      >
        {children}
      </Box>
    </Box>
  );
}
```

## frontend/src/components/Layout/Sidebar.jsx

**Folder path:** `frontend/src/components/Layout`

**File path:** `frontend/src/components/Layout/Sidebar.jsx`

```jsx
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
  Toolbar,
} from '@mui/material';
import {
  DashboardOutlined,
  DevicesOutlined,
  WarningOutlined,
  MemoryOutlined,
  TimelineOutlined,
  SettingsOutlined,
  ScienceOutlined,
  SensorsOutlined,
  DescriptionOutlined,
} from '@mui/icons-material';
import { Link, useLocation } from 'react-router-dom';

const menuItems = [
  { text: 'Dashboard', icon: <DashboardOutlined />, path: '/' },
  { text: 'Assets', icon: <DevicesOutlined />, path: '/assets' },
  { text: 'Incident Simulator', icon: <WarningOutlined />, path: '/incident-simulator' },
  { text: 'Agent Monitor', icon: <MemoryOutlined />, path: '/agent-monitor' },
  { text: 'AI Activity', icon: <TimelineOutlined />, path: '/ai-activity' },
  { text: 'Maintenance Planner', icon: <SettingsOutlined />, path: '/maintenance' },
  { text: 'Health Prediction', icon: <ScienceOutlined />, path: '/health-prediction' },
  { text: 'Digital Twin', icon: <SensorsOutlined />, path: '/digital-twin' },
  { text: 'Reports', icon: <DescriptionOutlined />, path: '/reports' },
];


export function Sidebar({ drawerWidth }) {
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        display: { xs: 'none', sm: 'block' },
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          background: 'rgba(10, 15, 26, 0.98)',
          borderRight: '1px solid rgba(56, 78, 112, 0.08)',
        },
      }}
    >
      <Toolbar />
      <Box sx={{ p: 2.5, borderBottom: '1px solid rgba(56, 78, 112, 0.08)' }}>
        <Typography
          variant="h6"
          sx={{
            color: '#E8EDF5',
            fontWeight: 600,
            letterSpacing: '-0.02em',
            fontSize: '1.1rem',
          }}
        >
          RIGOS
        </Typography>
        <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.12em', fontSize: '0.6rem' }}>
          Operations Center
        </Typography>
      </Box>

      <List sx={{ mt: 1, px: 1 }}>
        {menuItems.map((item) => {
          const active = location.pathname === item.path;
          return (
            <ListItem
              component={Link}
              to={item.path}
              key={item.text}
              sx={{
                borderRadius: '6px',
                mb: 0.5,
                py: 1.2,
                px: 2,
                background: active ? 'rgba(59, 130, 246, 0.08)' : 'transparent',
                borderLeft: active ? '2px solid #3B82F6' : '2px solid transparent',
                '&:hover': {
                  background: 'rgba(59, 130, 246, 0.04)',
                },
              }}
            >
              <ListItemIcon
                sx={{
                  color: active ? '#3B82F6' : '#5A6B8A',
                  minWidth: 36,
                  '& svg': { fontSize: 20 },
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                sx={{
                  '& .MuiTypography-root': {
                    color: active ? '#E8EDF5' : '#8899B4',
                    fontWeight: active ? 500 : 400,
                    fontSize: '0.85rem',
                  },
                }}
              />
            </ListItem>
          );
        })}
      </List>

      <Box sx={{ p: 2.5, mt: 'auto', borderTop: '1px solid rgba(56, 78, 112, 0.08)' }}>
        <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', fontSize: '0.65rem' }}>
          RIGOS v2.0
        </Typography>
        <Typography variant="caption" sx={{ color: '#3A4B6A', fontSize: '0.6rem' }}>
          AI Operations Platform
        </Typography>
      </Box>
    </Drawer>
  );
}
```

## frontend/src/hooks/useWebSocket.js

**Folder path:** `frontend/src/hooks`

**File path:** `frontend/src/hooks/useWebSocket.js`

```javascript
import { useEffect, useState, useRef } from 'react';
import { toast } from 'react-hot-toast';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export function useWebSocket() {
  const [connected, setConnected] = useState(false);
  const [data, setData] = useState(null);
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      socketRef.current = new WebSocket(WS_URL);

      socketRef.current.onopen = () => {
        console.log('✅ WebSocket connected');
        setConnected(true);
        toast.success('Connected to RigOS', { duration: 2000 });
      };

      socketRef.current.onclose = () => {
        console.log('❌ WebSocket disconnected');
        setConnected(false);
        // Attempt reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(connect, 3000);
      };

      socketRef.current.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'update') {
            setData(payload.data);
          }
        } catch (e) {
          console.error('WebSocket parse error:', e);
        }
      };
    };

    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  return { connected, data };
}
```

## frontend/src/index.css

**Folder path:** `frontend/src`

**File path:** `frontend/src/index.css`

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: #0b1220;
  color: #e8f0ff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(85, 214, 255, 0.25);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(85, 214, 255, 0.4);
}

/* Toast overrides */
.go3455832932 {
  background: #0d1728 !important;
  color: #e8f0ff !important;
  border: 1px solid rgba(85, 214, 255, 0.15) !important;
  border-radius: 10px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
  backdrop-filter: blur(12px) !important;
}

/* Animated glow for live indicator */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.live-dot {
  animation: pulse 2s ease-in-out infinite;
}

/* Glass morphism */
.glass {
  background: rgba(15, 27, 47, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(129, 172, 226, 0.1);
}

/* Loading shimmer */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

## frontend/src/main.jsx

**Folder path:** `frontend/src`

**File path:** `frontend/src/main.jsx`

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## frontend/src/pages/AgentMonitor.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/AgentMonitor.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  CircularProgress,
  useTheme,
} from '@mui/material';
import {
  Memory,
  CheckCircle,
  Warning,
  Error as ErrorIcon,  // ✅ Rename to avoid conflict
  Circle,
} from '@mui/icons-material';
import { getAgents, getAgentMetrics } from '../api/client';

// ✅ Rest of the code stays the same, but use ErrorIcon instead of Error
const getStatusIcon = (status) => {
  const icons = {
    'Active': <Circle sx={{ fontSize: 10, color: '#10B981' }} />,
    'Ready': <Circle sx={{ fontSize: 10, color: '#3B82F6' }} />,
    'Running': <CircularProgress size={12} sx={{ color: '#F59E0B' }} />,
    'Completed': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
    'Failed': <ErrorIcon sx={{ fontSize: 14, color: '#EF4444' }} />,  // ✅ Use ErrorIcon
    'Queued': <Warning sx={{ fontSize: 14, color: '#8B5CF6' }} />,
  };
  return icons[status] || <Circle sx={{ fontSize: 10, color: '#8899B4' }} />;
};

const AGENT_COLORS = {
  'Active': '#10B981',
  'Ready': '#3B82F6',
  'Running': '#F59E0B',
  'Completed': '#10B981',
  'Failed': '#EF4444',
  'Queued': '#8B5CF6',
};

// ✅ Mock data for when API fails
const MOCK_AGENTS = [
  { name: 'Safety', specialty: 'Risk validation', status: 'Active', confidence: '96%', currentTask: 'Checking assets' },
  { name: 'Diagnostic', specialty: 'Root cause analysis', status: 'Active', confidence: '95%', currentTask: 'Analyzing patterns' },
  { name: 'Knowledge', specialty: 'SOP retrieval', status: 'Ready', confidence: '93%', currentTask: 'Awaiting request' },
  { name: 'Maintenance', specialty: 'Maintenance planning', status: 'Ready', confidence: '94%', currentTask: 'Awaiting task' },
  { name: 'Planning', specialty: 'Recovery planning', status: 'Queued', confidence: '92%', currentTask: 'Preparing plan' },
  { name: 'Prediction', specialty: 'Failure prediction', status: 'Active', confidence: '91%', currentTask: 'Analyzing telemetry' },
  { name: 'Notification', specialty: 'Alerting', status: 'Ready', confidence: '95%', currentTask: 'Monitoring' },
  { name: 'Report', specialty: 'Report generation', status: 'Active', confidence: '94%', currentTask: 'Compiling data' },
];

const MOCK_METRICS = [
  { label: 'Agents online', value: '8 / 8', desc: 'All operational' },
  { label: 'Tasks active', value: '3', desc: 'In progress' },
  { label: 'Avg. confidence', value: '94.2%', desc: 'High accuracy' },
  { label: 'Decisions today', value: '24', desc: '8 per hour' },
];

export default function AgentMonitor() {
  const [agents, setAgents] = useState(MOCK_AGENTS);
  const [metrics, setMetrics] = useState(MOCK_METRICS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      // ✅ Use Promise.race with timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 5000)
      );
      
      const agentsPromise = getAgents();
      const metricsPromise = getAgentMetrics();
      
      const [agentsRes, metricsRes] = await Promise.race([
        Promise.all([agentsPromise, metricsPromise]),
        timeoutPromise.then(() => { throw new Error('Request timeout') })
      ]).catch(() => {
        // ✅ If timeout, use mock data
        console.log('Using mock agent data due to timeout');
        return [null, null];
      });
      
      if (agentsRes?.data) {
        setAgents(agentsRes.data);
      }
      if (metricsRes?.data) {
        setMetrics(metricsRes.data);
      }
    } catch (e) {
      console.error('Failed to load agent data, using mock data:', e);
      // Already using mock data from state
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    return AGENT_COLORS[status] || '#8899B4';
  };

  const getStatusIcon = (status) => {
    const icons = {
      'Active': <Circle sx={{ fontSize: 10, color: '#10B981' }} />,
      'Ready': <Circle sx={{ fontSize: 10, color: '#3B82F6' }} />,
      'Running': <CircularProgress size={12} sx={{ color: '#F59E0B' }} />,
      'Completed': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
      'Failed': <Error sx={{ fontSize: 14, color: '#EF4444' }} />,
      'Queued': <Warning sx={{ fontSize: 14, color: '#8B5CF6' }} />,
    };
    return icons[status] || <Circle sx={{ fontSize: 10, color: '#8899B4' }} />;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading agents...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Agent Monitor
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {agents.length} agents · {agents.filter(a => a.status === 'Active').length} active
          </Typography>
        </Box>
        <Chip
          label="● LIVE"
          sx={{ bgcolor: 'rgba(16,185,129,0.08)', color: '#10B981', border: '1px solid rgba(16,185,129,0.15)' }}
        />
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={6} sm={3} key={index}>
            <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
              <CardContent sx={{ py: 1.5 }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                  {metric.label || 'Metric'}
                </Typography>
                <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                  {metric.value || '0'}
                </Typography>
                <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.6rem' }}>
                  {metric.desc || ''}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Agent</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Specialty</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Confidence</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Current Task</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {agents.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No agents available
                </TableCell>
              </TableRow>
            ) : (
              agents.map((agent) => {
                const statusColor = getStatusColor(agent.status);
                const confidence = parseFloat(agent.confidence) || 0;

                return (
                  <TableRow
                    key={agent.name || Math.random()}
                    sx={{
                      borderBottom: '1px solid rgba(56,78,112,0.05)',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                    }}
                  >
                    <TableCell sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Memory sx={{ fontSize: 16, color: statusColor }} />
                        {agent.name || 'Unknown'}
                      </Box>
                    </TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{agent.specialty || 'N/A'}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getStatusIcon(agent.status)}
                        label={agent.status || 'Unknown'}
                        size="small"
                        sx={{
                          bgcolor: `${statusColor}15`,
                          color: statusColor,
                          border: `1px solid ${statusColor}20`,
                          fontSize: '0.65rem',
                          fontWeight: 500,
                          height: 24,
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={confidence}
                          sx={{
                            width: 60,
                            height: 4,
                            borderRadius: 2,
                            bgcolor: 'rgba(255,255,255,0.05)',
                            '& .MuiLinearProgress-bar': {
                              bgcolor: confidence > 80 ? '#10B981' : confidence > 50 ? '#F59E0B' : '#EF4444',
                            },
                          }}
                        />
                        <Typography sx={{ color: '#8899B4', fontSize: '0.75rem', minWidth: 35 }}>
                          {confidence}%
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell sx={{ color: '#8899B4', fontSize: '0.8rem' }}>
                      {agent.currentTask || 'Idle'}
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
```

## frontend/src/pages/AIActivity.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/AIActivity.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  useTheme,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Circle,
  Refresh,
  Schedule,
} from '@mui/icons-material';
import { getAgentActivity } from '../api/client';

// ✅ Mock data for when API fails
const MOCK_ACTIVITIES = [
  { time: '00:25:30', agent: 'Safety', action: 'Validated operating envelope for Zone A', status: 'Completed', confidence: '96%' },
  { time: '00:24:15', agent: 'Diagnostic', action: 'Analyzed vibration pattern for Pump A-01', status: 'Running', confidence: '95%' },
  { time: '00:23:00', agent: 'Knowledge', action: 'Retrieved SOP for pressure spike response', status: 'Completed', confidence: '93%' },
  { time: '00:22:10', agent: 'Prediction', action: 'Calculated failure probability for Compressor C-12', status: 'Completed', confidence: '91%' },
  { time: '00:21:30', agent: 'Maintenance', action: 'Generated maintenance schedule for critical assets', status: 'Queued', confidence: '94%' },
  { time: '00:20:45', agent: 'Planning', action: 'Created recovery plan for pressure incident', status: 'Completed', confidence: '92%' },
  { time: '00:19:50', agent: 'Notification', action: 'Sent alert for abnormal temperature reading', status: 'Completed', confidence: '96%' },
  { time: '00:18:30', agent: 'Report', action: 'Compiled incident summary report', status: 'In Progress', confidence: '90%' },
];

export default function AIActivity() {
  const [activities, setActivities] = useState(MOCK_ACTIVITIES);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const response = await getAgentActivity();
      const data = response.data;
      
      // ✅ Handle different response formats and filter out nulls
      let activityData = [];
      if (Array.isArray(data)) {
        // ✅ Filter out null/undefined values
        activityData = data.filter(item => item !== null && item !== undefined);
      } else if (data?.data && Array.isArray(data.data)) {
        activityData = data.data.filter(item => item !== null && item !== undefined);
      } else {
        activityData = MOCK_ACTIVITIES;
      }
      
      // ✅ Ensure each item has required fields
      const validActivities = activityData.filter(item => 
        item && typeof item === 'object' && item.status !== undefined
      );
      
      setActivities(validActivities.length > 0 ? validActivities : MOCK_ACTIVITIES);
    } catch (e) {
      console.error('Failed to load activities, using mock data:', e);
      setActivities(MOCK_ACTIVITIES);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    if (!status) return '#8899B4';
    const colors = {
      'Completed': '#10B981',
      'Running': '#F59E0B',
      'Failed': '#EF4444',
      'Queued': '#8B5CF6',
      'Pending': '#3B82F6',
      'In Progress': '#3B82F6',
    };
    return colors[status] || '#8899B4';
  };

  const getStatusDot = (status) => {
    const color = getStatusColor(status);
    return (
      <TimelineDot sx={{ 
        bgcolor: color,
        ...(status === 'Running' || status === 'In Progress' ? {
          animation: 'pulse 2s infinite',
          '@keyframes pulse': {
            '0%, 100%': { opacity: 1, transform: 'scale(1)' },
            '50%': { opacity: 0.4, transform: 'scale(0.8)' },
          }
        } : {})
      }} />
    );
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading activities...</Typography>
      </Box>
    );
  }

  // ✅ Safe filtering with null checks
  const total = activities?.length || 0;
  const completed = activities?.filter(a => a?.status === 'Completed')?.length || 0;
  const running = activities?.filter(a => a?.status === 'Running' || a?.status === 'In Progress')?.length || 0;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            AI Activity
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {total} activities recorded
          </Typography>
        </Box>
        <Chip
          label={`${running} active`}
          sx={{
            bgcolor: 'rgba(245,158,11,0.08)',
            color: '#F59E0B',
            border: '1px solid rgba(245,158,11,0.15)',
          }}
        />
      </Box>

      {/* Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {total}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Completed
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {completed}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                In Progress
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {running}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Queued
              </Typography>
              <Typography variant="h5" sx={{ color: '#8B5CF6', fontWeight: 600 }}>
                {total - completed - running}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Activity List */}
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Activity Timeline
          </Typography>
          <Chip
            label={`${activities?.length || 0} events`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.03)', color: '#5A6B8A' }}
          />
        </Box>

        {!activities || activities.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography sx={{ color: '#5A6B8A' }}>No activities recorded yet</Typography>
          </Box>
        ) : (
          <Box>
            {activities.slice(0, 20).map((activity, index) => {
              if (!activity) return null;
              const color = getStatusColor(activity.status);
              const isLast = index === activities.length - 1 || index === 19;
              
              return (
                <Box key={index}>
                  <Box sx={{ 
                    display: 'flex', 
                    alignItems: 'flex-start', 
                    gap: 2,
                    py: 1.5,
                    px: 1,
                  }}>
                    {/* Time */}
                    <Box sx={{ minWidth: 80, pt: 0.5 }}>
                      <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.7rem' }}>
                        {activity.time || 'N/A'}
                      </Typography>
                    </Box>
                    
                    {/* Dot */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 24 }}>
                      <Box sx={{ 
                        width: 12, 
                        height: 12, 
                        borderRadius: '50%', 
                        bgcolor: color,
                        ...((activity.status === 'Running' || activity.status === 'In Progress') && {
                          animation: 'pulse 2s infinite',
                        })
                      }} />
                      {!isLast && (
                        <Box sx={{ 
                          width: 1, 
                          height: 24, 
                          bgcolor: 'rgba(56,78,112,0.1)',
                          mt: 1,
                        }} />
                      )}
                    </Box>
                    
                    {/* Content */}
                    <Box sx={{ flex: 1, pt: 0.5 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                        <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                          {activity.agent || 'Unknown'}
                        </Typography>
                        <Chip
                          label={activity.status || 'Unknown'}
                          size="small"
                          sx={{
                            bgcolor: `${color}15`,
                            color: color,
                            fontSize: '0.6rem',
                            height: 18,
                            fontWeight: 500,
                          }}
                        />
                      </Box>
                      <Typography variant="caption" sx={{ color: '#8899B4', display: 'block', mt: 0.5 }}>
                        {activity.action || 'No action recorded'}
                      </Typography>
                      {activity.confidence && (
                        <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mt: 0.25 }}>
                          Confidence: {activity.confidence}
                        </Typography>
                      )}
                    </Box>
                  </Box>
                  {!isLast && <Box sx={{ borderBottom: '1px solid rgba(56,78,112,0.05)', mx: 1 }} />}
                </Box>
              );
            })}
          </Box>
        )}
      </Paper>
    </Box>
  );
}
```

## frontend/src/pages/Assets.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/Assets.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  TextField,
  MenuItem,
  LinearProgress,
  IconButton,
  Collapse,
  Card,
  CardContent,
  useTheme,
} from '@mui/material';
import {
  Search,
  ExpandMore,
  ExpandLess,
  Memory,
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  Circle,
} from '@mui/icons-material';
import { getAssets } from '../api/client';

const STATUS_COLORS = {
  'Running': '#10B981',
  'Healthy': '#10B981',
  'Warning': '#F59E0B',
  'Critical': '#EF4444',
  'Offline': '#5A6B8A',
};

export default function Assets() {
  const [assets, setAssets] = useState([]);
  const [filteredAssets, setFilteredAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    loadAssets();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [searchTerm, statusFilter, typeFilter, assets]);

  const loadAssets = async () => {
    try {
      const response = await getAssets();
      setAssets(response.data);
      setFilteredAssets(response.data);
    } catch (e) {
      console.error('Failed to load assets:', e);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = assets;
    
    if (searchTerm) {
      filtered = filtered.filter(a => 
        a.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.type?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.location?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (statusFilter !== 'all') {
      filtered = filtered.filter(a => 
        a.status?.toLowerCase() === statusFilter.toLowerCase()
      );
    }
    
    if (typeFilter !== 'all') {
      filtered = filtered.filter(a => 
        a.type?.toLowerCase() === typeFilter.toLowerCase()
      );
    }
    
    setFilteredAssets(filtered);
  };

  const getHealthColor = (health) => {
    if (health >= 80) return '#10B981';
    if (health >= 50) return '#F59E0B';
    return '#EF4444';
  };

  const getStatusColor = (status) => {
    return STATUS_COLORS[status] || '#8899B4';
  };

  const types = ['all', ...new Set(assets.map(a => a.type))].filter(Boolean);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading assets...</Typography>
      </Box>
    );
  }

  const total = assets.length;
  const online = assets.filter(a => a.status === 'Running').length;
  const warning = assets.filter(a => a.status === 'Warning').length;
  const critical = assets.filter(a => a.status === 'Critical').length;
  const avgHealth = total > 0 
  ? Math.round(assets.reduce((s, a) => s + (a.health || 0), 0) / total)
  : 0;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Asset Registry
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {total} assets monitored · {online} online · {warning} warning · {critical} critical
          </Typography>
        </Box>
        <Chip
          label={`${avgHealth}% Avg Health`}
          sx={{
            bgcolor: parseFloat(avgHealth) >= 80 ? 'rgba(16,185,129,0.08)' : 'rgba(245,158,11,0.08)',
            color: parseFloat(avgHealth) >= 80 ? '#10B981' : '#F59E0B',
          }}
        />
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total Assets
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {total}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Online
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {online}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Warning
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {warning}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Critical
              </Typography>
              <Typography variant="h5" sx={{ color: '#EF4444', fontWeight: 600 }}>
                {critical}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              size="small"
              placeholder="Search assets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              slotProps={{
                input: {
                  startAdornment: <Search sx={{ color: '#5A6B8A', mr: 1, fontSize: 18 }} />,
                  sx: {
                    bgcolor: 'rgba(255,255,255,0.02)',
                    border: '1px solid rgba(56,78,112,0.1)',
                    borderRadius: '6px',
                    '&:hover': { borderColor: 'rgba(56,78,112,0.2)' },
                  }
                }
              }}
            />
          </Grid>
          <Grid item xs={6} md={3}>
            <TextField
              select
              fullWidth
              size="small"
              label="Status"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              sx={{
                '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                '& .MuiSelect-select': { color: '#E8EDF5', fontSize: '0.85rem' },
              }}
            >
              <MenuItem value="all">All Statuses</MenuItem>
              <MenuItem value="Running">Running</MenuItem>
              <MenuItem value="Healthy">Healthy</MenuItem>
              <MenuItem value="Warning">Warning</MenuItem>
              <MenuItem value="Critical">Critical</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={6} md={3}>
            <TextField
              select
              fullWidth
              size="small"
              label="Type"
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              sx={{
                '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                '& .MuiSelect-select': { color: '#E8EDF5', fontSize: '0.85rem' },
              }}
            >
              <MenuItem value="all">All Types</MenuItem>
              {types.filter(t => t !== 'all').map((type) => (
                <MenuItem key={type} value={type}>{type}</MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} md={2}>
            <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
              {filteredAssets.length} assets shown
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Asset
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Type
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Location
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Health
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Status
              </TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontWeight: 600, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                Details
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredAssets.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No assets found matching your filters
                </TableCell>
              </TableRow>
            ) : (
              filteredAssets.map((asset, index) => {
                const health = asset.health || 0;
                const healthColor = getHealthColor(health);
                const statusColor = getStatusColor(asset.status);
                const isExpanded = selectedAsset?.id === asset.id && expanded;

                return (
                  <React.Fragment key={asset.id || index}>
                    <TableRow
                      sx={{
                        '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                        borderBottom: '1px solid rgba(56,78,112,0.05)',
                        cursor: 'pointer',
                      }}
                      onClick={() => {
                        if (selectedAsset?.id === asset.id) {
                          setExpanded(!expanded);
                        } else {
                          setSelectedAsset(asset);
                          setExpanded(true);
                        }
                      }}
                    >
                      <TableCell sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                        {asset.name}
                      </TableCell>
                      <TableCell sx={{ color: '#8899B4' }}>{asset.type || 'Unknown'}</TableCell>
                      <TableCell sx={{ color: '#8899B4' }}>{asset.location || 'Unassigned'}</TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <LinearProgress
                            variant="determinate"
                            value={Math.round(health)}  // ✅ Round the value
                            sx={{
                                width: 80,
                                height: 4,
                                borderRadius: 2,
                                bgcolor: 'rgba(255,255,255,0.05)',
                                '& .MuiLinearProgress-bar': { bgcolor: healthColor },
                            }}
                            />
                            <Typography sx={{ color: healthColor, fontWeight: 500, fontSize: '0.8rem', minWidth: 40 }}>
                            {Math.round(health)}%  
                            </Typography>
                        
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={asset.status || 'Unknown'}
                          size="small"
                          sx={{
                            bgcolor: `${statusColor}15`,
                            color: statusColor,
                            border: `1px solid ${statusColor}20`,
                            fontSize: '0.65rem',
                            fontWeight: 500,
                            height: 24,
                          }}
                        />
                      </TableCell>
                      <TableCell>
                        <IconButton size="small" sx={{ color: '#5A6B8A' }}>
                          {isExpanded ? <ExpandLess sx={{ fontSize: 18 }} /> : <ExpandMore sx={{ fontSize: 18 }} />}
                        </IconButton>
                      </TableCell>
                    </TableRow>

                    <TableRow>
                      <TableCell colSpan={6} sx={{ p: 0, border: 'none' }}>
                        <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                          <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.01)', borderTop: '1px solid rgba(56,78,112,0.05)' }}>
                            <Grid container spacing={2}>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Asset ID
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#8899B4' }}>
                                  {asset.id}
                                </Typography>
                              </Grid>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Health Status
                                </Typography>
                                <Typography variant="body2" sx={{ color: healthColor }}>
                                  {health >= 80 ? 'Excellent' : health >= 50 ? 'Good' : 'Critical'}
                                </Typography>
                              </Grid>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Refinery
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#8899B4' }}>
                                  {asset.refinery_name || 'Unknown'}
                                </Typography>
                              </Grid>
                              <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block' }}>
                                  Last Updated
                                </Typography>
                                <Typography variant="body2" sx={{ color: '#8899B4' }}>
                                  {new Date().toLocaleTimeString()}
                                </Typography>
                              </Grid>
                            </Grid>
                          </Box>
                        </Collapse>
                      </TableCell>
                    </TableRow>
                  </React.Fragment>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
```

## frontend/src/pages/Dashboard.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/Dashboard.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  Devices,
  Warning,
  CheckCircle,
  Speed,
} from '@mui/icons-material';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { getAssets, getTelemetry } from '../api/client';

const COLORS = ['#EF4444', '#EF4444', '#F59E0B', '#3B82F6', '#10B981'];
const HEALTH_RANGES = ['Critical', 'Poor', 'Warning', 'Good', 'Excellent'];

export default function Dashboard() {
  const [assets, setAssets] = useState([]);
  const [telemetry, setTelemetry] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [refreshCount, setRefreshCount] = useState(0);

  // ✅ Load data function
  const loadData = async () => {
    try {
      const assetsRes = await getAssets();
      setAssets(assetsRes.data || []);

      if (assetsRes.data && assetsRes.data.length > 0) {
        const teleRes = await getTelemetry(assetsRes.data[0].id);
        setTelemetry(teleRes.data || []);
      }
    } catch (e) {
      console.error('Failed to load data:', e);
    } finally {
      setLoading(false);
      setLastUpdate(new Date());
      setRefreshCount(prev => prev + 1);
    }
  };

  // ✅ Initial load + auto-refresh every 3 seconds
  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, []);

  const totalAssets = assets.length;
  const healthyCount = assets.filter((a) => a.status === 'Running').length;
  const avgHealth = totalAssets > 0
    ? Math.round(assets.reduce((s, a) => s + (a.health || 0), 0) / totalAssets)
    : 0;
  const criticalCount = assets.filter((a) => a.health < 50).length;
  const warningCount = assets.filter((a) => a.health >= 50 && a.health < 80).length;

  const healthRanges = [
    { name: 'Critical', value: 0, color: '#EF4444' },
    { name: 'Poor', value: 0, color: '#EF4444' },
    { name: 'Warning', value: 0, color: '#F59E0B' },
    { name: 'Good', value: 0, color: '#3B82F6' },
    { name: 'Excellent', value: 0, color: '#10B981' },
  ];
  assets.forEach((a) => {
    const h = a.health || 0;
    if (h <= 20) healthRanges[0].value++;
    else if (h <= 40) healthRanges[1].value++;
    else if (h <= 60) healthRanges[2].value++;
    else if (h <= 80) healthRanges[3].value++;
    else healthRanges[4].value++;
  });

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '50vh', gap: 3 }}>
        <Typography variant="h6" sx={{ color: '#3B82F6' }}>Loading dashboard...</Typography>
        <LinearProgress sx={{ width: 200, height: 3, borderRadius: 2, bgcolor: 'rgba(59,130,246,0.1)' }} />
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Operations Dashboard
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            Real-time monitoring · Last updated {formatTime(lastUpdate)} · Refresh #{refreshCount}
          </Typography>
        </Box>
        <Chip
          label="● LIVE"
          sx={{
            bgcolor: 'rgba(16, 185, 129, 0.08)',
            color: '#10B981',
            border: '1px solid rgba(16, 185, 129, 0.15)',
            fontWeight: 500,
            fontSize: '0.7rem',
          }}
        />
      </Box>

      {/* Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  Fleet Health
                </Typography>
                <Speed sx={{ fontSize: 18, color: avgHealth > 80 ? '#10B981' : '#F59E0B' }} />
              </Box>
              <Typography variant="h3" sx={{ color: avgHealth > 80 ? '#10B981' : '#F59E0B', fontWeight: 600, my: 1 }}>
                {avgHealth}%
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: '#10B981' }} />
                  <Typography variant="caption" sx={{ color: '#8899B4' }}>{healthyCount}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: '#F59E0B' }} />
                  <Typography variant="caption" sx={{ color: '#8899B4' }}>{warningCount}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Box sx={{ width: 6, height: 6, borderRadius: '50%', bgcolor: '#EF4444' }} />
                  <Typography variant="caption" sx={{ color: '#8899B4' }}>{criticalCount}</Typography>
                </Box>
              </Box>
              <LinearProgress
                variant="determinate"
                value={avgHealth}
                sx={{ mt: 1.5, height: 2, borderRadius: 2, bgcolor: 'rgba(255,255,255,0.04)' }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  Total Assets
                </Typography>
                <Devices sx={{ fontSize: 18, color: '#3B82F6' }} />
              </Box>
              <Typography variant="h3" sx={{ color: '#E8EDF5', fontWeight: 600, my: 1 }}>
                {totalAssets}
              </Typography>
              <Typography variant="caption" sx={{ color: '#8899B4' }}>
                {healthyCount} online · {warningCount} warning · {criticalCount} critical
              </Typography>
              <Box sx={{ display: 'flex', gap: 0.5, mt: 1.5 }}>
                <Box sx={{ flex: 1, height: 2, borderRadius: 2, bgcolor: '#10B981', opacity: healthyCount / totalAssets || 0 }} />
                <Box sx={{ flex: 1, height: 2, borderRadius: 2, bgcolor: '#F59E0B', opacity: warningCount / totalAssets || 0 }} />
                <Box sx={{ flex: 1, height: 2, borderRadius: 2, bgcolor: '#EF4444', opacity: criticalCount / totalAssets || 0 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  Telemetry
                </Typography>
                <TrendingUp sx={{ fontSize: 18, color: '#3B82F6' }} />
              </Box>
              <Typography variant="h3" sx={{ color: '#E8EDF5', fontWeight: 600, my: 1 }}>
                {telemetry.length}
              </Typography>
              <Typography variant="caption" sx={{ color: '#8899B4' }}>
                Data points in stream
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>
                  System Status
                </Typography>
                <CheckCircle sx={{ fontSize: 18, color: '#10B981' }} />
              </Box>
              <Typography variant="h3" sx={{ color: '#10B981', fontWeight: 600, my: 1 }}>
                NOMINAL
              </Typography>
              <Typography variant="caption" sx={{ color: '#8899B4' }}>
                All systems operational
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Telemetry Chart */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Telemetry Stream
          </Typography>
          <Chip label={`${telemetry.length} readings`} size="small" sx={{ bgcolor: 'rgba(59,130,246,0.06)', color: '#8899B4', border: '1px solid rgba(56,78,112,0.1)', fontSize: '0.6rem' }} />
        </Box>
        {telemetry.length > 0 ? (
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={telemetry.slice(-30)}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" />
              <XAxis dataKey="timestamp" stroke="#5A6B8A" tick={{ fontSize: 10 }} />
              <YAxis stroke="#5A6B8A" tick={{ fontSize: 10 }} />
              <Tooltip
                contentStyle={{
                  background: '#121C2E',
                  border: '1px solid rgba(56,78,112,0.15)',
                  borderRadius: '6px',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
                }}
                labelStyle={{ color: '#8899B4' }}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#3B82F6"
                strokeWidth={1.5}
                fill="url(#colorValue)"
                name="Sensor Value"
              />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <Box sx={{ textAlign: 'center', py: 6 }}>
            <Typography sx={{ color: '#5A6B8A' }}>No telemetry data available</Typography>
          </Box>
        )}
      </Paper>

      {/* Health Distribution */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
              Asset Health Distribution
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4, flexWrap: 'wrap' }}>
              {/* ✅ Pie Chart */}
              <Box sx={{ width: 200, height: 200 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={healthRanges}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={80}
                      dataKey="value"
                      paddingAngle={2}
                    >
                      {healthRanges.map((entry, i) => (
                        <Cell key={i} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        background: '#121C2E',
                        border: '1px solid rgba(56,78,112,0.15)',
                        borderRadius: '6px',
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
              
              {/* ✅ Legend */}
              <Box>
                {healthRanges.filter(h => h.value > 0).map((item) => (
                  <Box key={item.name} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: item.color }} />
                    <Typography variant="body2" sx={{ color: '#8899B4', fontSize: '0.8rem' }}>
                      {item.name}: <strong style={{ color: '#E8EDF5' }}>{item.value}</strong>
                    </Typography>
                  </Box>
                ))}
                {healthRanges.every(h => h.value === 0) && (
                  <Typography sx={{ color: '#5A6B8A' }}>No asset data available</Typography>
                )}
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
              Asset Health Leaders
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              {assets
                .sort((a, b) => (b.health || 0) - (a.health || 0))
                .slice(0, 5)
                .map((asset, index) => {
                  const health = Math.round(asset.health || 0);
                  const color = health >= 80 ? '#10B981' : health >= 50 ? '#F59E0B' : '#EF4444';
                  return (
                    <Box
                      key={asset.id}
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 2,
                        p: 1.5,
                        borderRadius: 1,
                        bgcolor: 'rgba(255,255,255,0.02)',
                        border: '1px solid rgba(255,255,255,0.03)',
                      }}
                    >
                      <Typography sx={{ color: '#5A6B8A', fontWeight: 500, minWidth: 24, fontSize: '0.75rem' }}>
                        {String(index + 1).padStart(2, '0')}
                      </Typography>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500, fontSize: '0.85rem' }}>
                          {asset.name}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.65rem' }}>
                          {asset.type || 'Unknown'}
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <LinearProgress
                          variant="determinate"
                          value={health}
                          sx={{
                            width: 80,
                            height: 3,
                            borderRadius: 2,
                            bgcolor: 'rgba(255,255,255,0.04)',
                            '& .MuiLinearProgress-bar': {
                              bgcolor: color,
                            },
                          }}
                        />
                        <Typography sx={{ color, fontWeight: 500, minWidth: 40, fontSize: '0.8rem' }}>
                          {health}%
                        </Typography>
                      </Box>
                    </Box>
                  );
                })}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
```

## frontend/src/pages/DigitalTwin.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/DigitalTwin.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  useTheme,
} from '@mui/material';
import {
  Sensors,
  LocationOn,
  CheckCircle,
  Warning,
  Error,
  Circle,
} from '@mui/icons-material';
import { getAssets } from '../api/client';

export default function DigitalTwin() {
  const theme = useTheme();
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await getAssets();
      setAssets(response.data || []);
    } catch (e) {
      console.error('Failed to load assets:', e);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'Running': '#10B981',
      'Healthy': '#10B981',
      'Warning': '#F59E0B',
      'Critical': '#EF4444',
      'Offline': '#5A6B8A',
    };
    return colors[status] || '#8899B4';
  };

  const getHealthColor = (health) => {
    if (health >= 80) return '#10B981';
    if (health >= 50) return '#F59E0B';
    return '#EF4444';
  };

  // Group assets by zone
  const zones = assets.reduce((acc, asset) => {
    const zone = asset.location || 'Unassigned';
    if (!acc[zone]) acc[zone] = [];
    acc[zone].push(asset);
    return acc;
  }, {});

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading digital twin...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Digital Twin
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {assets.length} assets · {Object.keys(zones).length} zones
          </Typography>
        </Box>
        <Chip
          label="● LIVE"
          sx={{ bgcolor: 'rgba(16,185,129,0.08)', color: '#10B981', border: '1px solid rgba(16,185,129,0.15)' }}
        />
      </Box>

      <Grid container spacing={3}>
        {Object.entries(zones).map(([zoneName, zoneAssets]) => {
          const avgHealth = zoneAssets.reduce((s, a) => s + (a.health || 0), 0) / zoneAssets.length;
          const healthColor = getHealthColor(avgHealth);
          const healthyCount = zoneAssets.filter(a => a.status === 'Running').length;

          return (
            <Grid item xs={12} md={6} key={zoneName}>
              <Paper sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LocationOn sx={{ color: '#3B82F6', fontSize: 18 }} />
                    <Typography variant="h6" sx={{ color: '#E8EDF5', fontWeight: 500, fontSize: '1rem' }}>
                      {zoneName}
                    </Typography>
                  </Box>
                  <Chip
                    label={`${healthyCount}/${zoneAssets.length} online`}
                    size="small"
                    sx={{
                      bgcolor: avgHealth >= 80 ? 'rgba(16,185,129,0.08)' : 'rgba(245,158,11,0.08)',
                      color: avgHealth >= 80 ? '#10B981' : '#F59E0B',
                      fontSize: '0.6rem',
                    }}
                  />
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <LinearProgress
                    variant="determinate"
                    value={avgHealth}
                    sx={{
                      flex: 1,
                      height: 6,
                      borderRadius: 3,
                      bgcolor: 'rgba(255,255,255,0.05)',
                      '& .MuiLinearProgress-bar': { bgcolor: healthColor },
                    }}
                  />
                  <Typography sx={{ color: healthColor, fontWeight: 600, minWidth: 45 }}>
                    {Math.round(avgHealth)}%
                  </Typography>
                </Box>

                <Grid container spacing={1}>
                  {zoneAssets.slice(0, 6).map((asset) => {
                    const statusColor = getStatusColor(asset.status);
                    const health = asset.health || 0;
                    return (
                      <Grid item xs={6} key={asset.id}>
                        <Card sx={{ bgcolor: 'rgba(255,255,255,0.02)' }}>
                          <CardContent sx={{ py: 1, px: 1.5 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <Typography variant="caption" sx={{ color: '#E8EDF5', fontWeight: 500, fontSize: '0.7rem' }}>
                                {asset.name}
                              </Typography>
                              <Chip
                                size="small"
                                sx={{
                                  width: 8,
                                  height: 8,
                                  minWidth: 8,
                                  bgcolor: statusColor,
                                  borderRadius: '50%',
                                  '& .MuiChip-label': { display: 'none' },
                                }}
                              />
                            </Box>
                            <Typography variant="caption" sx={{ color: '#5A6B8A', fontSize: '0.6rem' }}>
                              {asset.type || 'Unknown'} · {health}%
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    );
                  })}
                </Grid>
                {zoneAssets.length > 6 && (
                  <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mt: 1 }}>
                    + {zoneAssets.length - 6} more assets
                  </Typography>
                )}
              </Paper>
            </Grid>
          );
        })}
      </Grid>

      {Object.keys(zones).length === 0 && (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography sx={{ color: '#5A6B8A' }}>No assets available for digital twin view</Typography>
        </Paper>
      )}
    </Box>
  );
}
```

## frontend/src/pages/HealthPrediction.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/HealthPrediction.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
  useTheme,
} from '@mui/material';
import {
  Science,
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
  Timeline,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import { getAssets, getPredictions } from '../api/client';

export default function HealthPrediction() {
  const theme = useTheme();
  const [assets, setAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [horizon, setHorizon] = useState(14);

  useEffect(() => {
    loadAssets();
  }, []);

  useEffect(() => {
    if (selectedAsset) {
      loadPrediction();
    }
  }, [selectedAsset, horizon]);

  const loadAssets = async () => {
    try {
      const response = await getAssets();
      setAssets(response.data || []);
      if (response.data?.length > 0) {
        setSelectedAsset(response.data[0].id);
      }
    } catch (e) {
      console.error('Failed to load assets:', e);
    } finally {
      setLoading(false);
    }
  };

  const loadPrediction = async () => {
    try {
      const response = await getPredictions(selectedAsset, horizon);
      setPrediction(response.data);
    } catch (e) {
      console.error('Failed to load prediction:', e);
    }
  };

  const getSelectedAssetName = () => {
    const asset = assets.find(a => a.id === selectedAsset);
    return asset?.name || 'Unknown Asset';
  };

  // Generate mock prediction data if none exists
  const getChartData = () => {
    if (prediction?.historical?.length) {
      return prediction.historical.map((h, i) => ({
        day: i + 1,
        health: h,
      }));
    }
    // Mock data
    const data = [];
    let health = 95;
    for (let i = 0; i < horizon; i++) {
      health -= Math.random() * 2 + 0.5;
      health = Math.max(0, health);
      data.push({
        day: i + 1,
        health: Math.round(health * 10) / 10,
      });
    }
    return data;
  };

  const getHealthStatus = (health) => {
    if (health >= 80) return { label: 'Excellent', color: '#10B981', icon: <CheckCircle /> };
    if (health >= 60) return { label: 'Good', color: '#3B82F6', icon: <CheckCircle /> };
    if (health >= 40) return { label: 'Warning', color: '#F59E0B', icon: <Warning /> };
    return { label: 'Critical', color: '#EF4444', icon: <Warning /> };
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading predictions...</Typography>
      </Box>
    );
  }

  const currentHealth = prediction?.health || 85;
  const status = getHealthStatus(currentHealth);
  const chartData = getChartData();

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Health Prediction
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            AI-powered asset health forecasting
          </Typography>
        </Box>
        <Chip
          label={`${horizon} day forecast`}
          sx={{ bgcolor: 'rgba(59,130,246,0.08)', color: '#3B82F6', border: '1px solid rgba(59,130,246,0.15)' }}
        />
      </Box>

      {/* Asset Selector */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <FormControl fullWidth size="small">
              <InputLabel sx={{ color: '#5A6B8A' }}>Select Asset</InputLabel>
              <Select
                value={selectedAsset}
                onChange={(e) => setSelectedAsset(e.target.value)}
                label="Select Asset"
                sx={{ color: '#E8EDF5' }}
              >
                {assets.map((asset) => (
                  <MenuItem key={asset.id} value={asset.id}>
                    {asset.name} ({asset.type || 'Unknown'})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth size="small">
              <InputLabel sx={{ color: '#5A6B8A' }}>Forecast Horizon</InputLabel>
              <Select
                value={horizon}
                onChange={(e) => setHorizon(e.target.value)}
                label="Forecast Horizon"
                sx={{ color: '#E8EDF5' }}
              >
                <MenuItem value={7}>7 Days</MenuItem>
                <MenuItem value={14}>14 Days</MenuItem>
                <MenuItem value={30}>30 Days</MenuItem>
                <MenuItem value={60}>60 Days</MenuItem>
                <MenuItem value={90}>90 Days</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="body2" sx={{ color: '#5A6B8A', textAlign: 'right' }}>
              Asset: <strong style={{ color: '#E8EDF5' }}>{getSelectedAssetName()}</strong>
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Current Health
              </Typography>
              <Typography variant="h5" sx={{ color: status.color, fontWeight: 600 }}>
                {currentHealth}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Status
              </Typography>
              <Typography variant="h5" sx={{ color: status.color, fontWeight: 600, fontSize: '1rem' }}>
                {status.label}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                RUL
              </Typography>
              <Typography variant="h5" sx={{ color: '#3B82F6', fontWeight: 600, fontSize: '1rem' }}>
                {prediction?.rul || '365 days'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Failure Probability
              </Typography>
              <Typography variant="h5" sx={{ color: prediction?.failureProbability > 50 ? '#EF4444' : '#10B981', fontWeight: 600, fontSize: '1rem' }}>
                {prediction?.failureProbability || '5%'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Prediction Chart */}
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Health Forecast
          </Typography>
          <Chip
            label={`${horizon} days`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.03)', color: '#5A6B8A' }}
          />
        </Box>
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="day" stroke="#5A6B8A" label={{ value: 'Days', position: 'bottom', fill: '#5A6B8A' }} />
            <YAxis stroke="#5A6B8A" domain={[0, 100]} label={{ value: 'Health %', angle: -90, position: 'left', fill: '#5A6B8A' }} />
            <Tooltip
              contentStyle={{
                background: '#121C2E',
                border: '1px solid rgba(56,78,112,0.15)',
                borderRadius: '6px',
              }}
            />
            <Line
              type="monotone"
              dataKey="health"
              stroke="#3B82F6"
              strokeWidth={2}
              dot={{ fill: '#3B82F6', r: 4 }}
              name="Health %"
            />
          </LineChart>
        </ResponsiveContainer>
      </Paper>
    </Box>
  );
}
```

## frontend/src/pages/IncidentSimulator.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/IncidentSimulator.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Button,
  Chip,
  TextField,
  MenuItem,
  Alert,
  List,
  ListItem,
  ListItemText,
  Divider,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  useTheme,
  Fade,
  Grow,
} from '@mui/material';
import { CircularProgress } from '@mui/material';
import {
  Warning,
  PlayArrow,
  History,
  CheckCircle,
  Error,
  Circle,
  Refresh,
  Delete,
  TrendingUp,
  TrendingDown,
  FlashOn,
  Whatshot,
} from '@mui/icons-material';
import { triggerIncident, getIncidents } from '../api/client';

const INCIDENT_TYPES = [
  { value: 'pressure spike', label: 'Pressure Spike', icon: '📈', color: '#EF4444', desc: 'Sudden pressure increase' },
  { value: 'gas leak', label: 'Gas Leak', icon: '💨', color: '#F59E0B', desc: 'Gas concentration detected' },
  { value: 'high temperature', label: 'High Temperature', icon: '🌡️', color: '#F97316', desc: 'Temperature threshold exceeded' },
  { value: 'high vibration', label: 'High Vibration', icon: '📳', color: '#8B5CF6', desc: 'Abnormal vibration detected' },
  { value: 'flow restriction', label: 'Flow Restriction', icon: '🚫', color: '#3B82F6', desc: 'Flow rate below minimum' },
];

const SEVERITY_COLORS = {
  'Low': '#10B981',
  'Medium': '#F59E0B',
  'High': '#F97316',
  'Critical': '#EF4444',
};

export default function IncidentSimulator() {
  const theme = useTheme();
  const [incidentType, setIncidentType] = useState('pressure spike');
  const [severity, setSeverity] = useState('High');
  const [triggering, setTriggering] = useState(false);
  const [incidentHistory, setIncidentHistory] = useState([]);
  const [activeIncidents, setActiveIncidents] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  // Load incidents
  useEffect(() => {
    loadIncidents();
    const interval = setInterval(loadIncidents, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadIncidents = async () => {
    try {
      const response = await getIncidents();
      const incidents = response.data || [];
      setActiveIncidents(incidents);
    } catch (e) {
      console.error('Failed to load incidents:', e);
    }
  };

  const handleTrigger = async () => {
    setTriggering(true);
    setResult(null);
    setLoading(true);
    setShowSuccess(false);

    try {
      const response = await triggerIncident(incidentType);
      setResult({
        success: true,
        message: `Incident triggered successfully`,
        id: response.data?.id || 'unknown',
        type: incidentType,
        severity: severity,
      });
      setShowSuccess(true);

      // Add to history
      setIncidentHistory(prev => [
        {
          id: Date.now(),
          type: incidentType,
          severity: severity,
          timestamp: new Date().toISOString(),
          status: 'Triggered',
          message: response.data?.message || 'Incident triggered',
        },
        ...prev.slice(0, 49),
      ]);

      await loadIncidents();

      setTimeout(() => setShowSuccess(false), 3000);

    } catch (e) {
      console.error('Failed to trigger incident:', e);
      setResult({
        success: false,
        message: `Failed to trigger incident: ${e.message || 'Unknown error'}`,
      });
    } finally {
      setTriggering(false);
      setLoading(false);
      setTimeout(() => setResult(null), 5000);
    }
  };

  const getIncidentIcon = (type) => {
    const found = INCIDENT_TYPES.find(t => t.value === type);
    return found ? found.icon : '⚡';
  };

  const getIncidentColor = (type) => {
    const found = INCIDENT_TYPES.find(t => t.value === type);
    return found ? found.color : '#8899B4';
  };

  const getSeverityColor = (sev) => {
    return SEVERITY_COLORS[sev] || '#8899B4';
  };

  const getSeverityIcon = (sev) => {
    const icons = {
      'Low': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
      'Medium': <Warning sx={{ fontSize: 14, color: '#F59E0B' }} />,
      'High': <Error sx={{ fontSize: 14, color: '#F97316' }} />,
      'Critical': <FlashOn sx={{ fontSize: 14, color: '#EF4444' }} />,
    };
    return icons[sev] || <Circle sx={{ fontSize: 14, color: '#8899B4' }} />;
  };

  const selectedType = INCIDENT_TYPES.find(t => t.value === incidentType);

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Incident Simulator
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            Trigger and test incident response workflows
          </Typography>
        </Box>
        <Chip
          label={`${activeIncidents.length} Active`}
          sx={{
            bgcolor: activeIncidents.length > 0 ? 'rgba(239,68,68,0.08)' : 'rgba(16,185,129,0.08)',
            color: activeIncidents.length > 0 ? '#EF4444' : '#10B981',
            border: `1px solid ${activeIncidents.length > 0 ? 'rgba(239,68,68,0.15)' : 'rgba(16,185,129,0.15)'}`,
            fontWeight: 500,
          }}
        />
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Total Triggered
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {incidentHistory.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Active
              </Typography>
              <Typography variant="h5" sx={{ color: activeIncidents.length > 0 ? '#EF4444' : '#10B981', fontWeight: 600 }}>
                {activeIncidents.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Most Common
              </Typography>
              <Typography variant="h5" sx={{ color: '#3B82F6', fontWeight: 600, fontSize: '1rem' }}>
                {incidentHistory.length > 0 
                  ? Object.entries(
                      incidentHistory.reduce((acc, i) => {
                        acc[i.type] = (acc[i.type] || 0) + 1;
                        return acc;
                      }, {})
                    ).sort((a, b) => b[1] - a[1])[0]?.[0] || 'None'
                  : 'None'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem', letterSpacing: '0.08em' }}>
                Avg Severity
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {incidentHistory.length > 0 
                  ? Object.entries(
                      incidentHistory.reduce((acc, i) => {
                        const sev = i.severity || 'Low';
                        acc[sev] = (acc[sev] || 0) + 1;
                        return acc;
                      }, {})
                    ).sort((a, b) => b[1] - a[1])[0]?.[0] || 'Low'
                  : 'Low'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Trigger Panel - Left */}
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
              Configure Incident
            </Typography>

            {/* Type Preview */}
            {selectedType && (
              <Box 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 2, 
                  p: 2, 
                  mb: 2, 
                  borderRadius: 1,
                  bgcolor: `${selectedType.color}10`,
                  border: `1px solid ${selectedType.color}20`,
                }}
              >
                <Box sx={{ fontSize: 32 }}>{selectedType.icon}</Box>
                <Box>
                  <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                    {selectedType.label}
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
                    {selectedType.desc}
                  </Typography>
                </Box>
              </Box>
            )}

            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  select
                  fullWidth
                  label="Incident Type"
                  value={incidentType}
                  onChange={(e) => setIncidentType(e.target.value)}
                  sx={{
                    '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                    '& .MuiSelect-select': { color: '#E8EDF5' },
                  }}
                  SelectProps={{
                    renderValue: (value) => {
                      const found = INCIDENT_TYPES.find(t => t.value === value);
                      return found ? `${found.icon} ${found.label}` : value;
                    },
                  }}
                >
                  {INCIDENT_TYPES.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.icon} {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  select
                  fullWidth
                  label="Severity"
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                  sx={{
                    '& .MuiInputLabel-root': { color: '#5A6B8A', fontSize: '0.75rem' },
                    '& .MuiSelect-select': { color: '#E8EDF5' },
                  }}
                >
                  {['Low', 'Medium', 'High', 'Critical'].map((option) => (
                    <MenuItem key={option} value={option}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getSeverityIcon(option)}
                        {option}
                      </Box>
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={triggering ? <CircularProgress size={20} color="inherit" /> : <PlayArrow />}
                  onClick={handleTrigger}
                  disabled={triggering}
                  sx={{
                    bgcolor: '#EF4444',
                    '&:hover': { bgcolor: '#DC2626' },
                    py: 1.5,
                    fontWeight: 600,
                    borderRadius: '8px',
                  }}
                >
                  {triggering ? 'Triggering...' : 'Trigger Incident'}
                </Button>
              </Grid>
            </Grid>

            {result && (
              <Fade in={!!result}>
                <Alert
                  severity={result.success ? 'success' : 'error'}
                  sx={{ mt: 2, borderRadius: '8px' }}
                >
                  {result.message}
                  {result.id && (
                    <Typography variant="caption" sx={{ display: 'block', color: 'inherit', opacity: 0.7 }}>
                      ID: {result.id}
                    </Typography>
                  )}
                </Alert>
              </Fade>
            )}

            {/* Quick Presets */}
            <Box sx={{ mt: 2 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mb: 1 }}>
                Quick Presets:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {INCIDENT_TYPES.map((type) => (
                  <Chip
                    key={type.value}
                    label={`${type.icon} ${type.label}`}
                    size="small"
                    onClick={() => setIncidentType(type.value)}
                    sx={{
                      bgcolor: incidentType === type.value ? `${type.color}20` : 'rgba(255,255,255,0.03)',
                      border: incidentType === type.value ? `1px solid ${type.color}40` : '1px solid rgba(56,78,112,0.1)',
                      cursor: 'pointer',
                      color: incidentType === type.value ? '#E8EDF5' : '#8899B4',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.06)' },
                    }}
                  />
                ))}
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Active Incidents - Right */}
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
                Active Incidents
              </Typography>
              <IconButton size="small" onClick={loadIncidents} sx={{ color: '#5A6B8A' }}>
                <Refresh sx={{ fontSize: 16 }} />
              </IconButton>
            </Box>

            {activeIncidents.length === 0 ? (
              <Box sx={{ textAlign: 'center', py: 6 }}>
                <Typography sx={{ color: '#5A6B8A' }}>
                  No active incidents
                </Typography>
                <Typography variant="caption" sx={{ color: '#3A4B6A' }}>
                  Trigger an incident to see it here
                </Typography>
              </Box>
            ) : (
              <Box sx={{ maxHeight: 350, overflow: 'auto' }}>
                {activeIncidents.slice(0, 10).map((incident) => (
                  <Box
                    key={incident.id}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      p: 1.5,
                      mb: 1,
                      borderRadius: 1,
                      bgcolor: 'rgba(255,255,255,0.02)',
                      border: '1px solid rgba(56,78,112,0.05)',
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Box sx={{ fontSize: 24 }}>{getIncidentIcon(incident.name)}</Box>
                      <Box>
                        <Typography variant="body2" sx={{ color: '#E8EDF5', fontWeight: 500 }}>
                          {incident.name || 'Unknown'}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
                          Asset: {incident.asset_id || 'Unknown'}
                        </Typography>
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Chip
                        label="Active"
                        size="small"
                        sx={{
                          bgcolor: 'rgba(239,68,68,0.12)',
                          color: '#EF4444',
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                      <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
                        {incident.timestamp ? new Date(incident.timestamp).toLocaleTimeString() : ''}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            )}

            {activeIncidents.length > 10 && (
              <Typography variant="caption" sx={{ color: '#5A6B8A', display: 'block', mt: 1, textAlign: 'center' }}>
                + {activeIncidents.length - 10} more incidents
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* History Section */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600 }}>
            Incident History
          </Typography>
          <Chip
            label={`${incidentHistory.length} incidents`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.03)', color: '#5A6B8A' }}
          />
        </Box>

        {incidentHistory.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 2 }}>
            <Typography sx={{ color: '#5A6B8A', fontSize: '0.85rem' }}>
              No incidents triggered yet
            </Typography>
          </Box>
        ) : (
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Time</TableCell>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Type</TableCell>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Severity</TableCell>
                  <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {incidentHistory.slice(0, 20).map((incident) => (
                  <TableRow key={incident.id} sx={{ borderBottom: '1px solid rgba(56,78,112,0.03)' }}>
                    <TableCell sx={{ color: '#5A6B8A', fontSize: '0.75rem' }}>
                      {new Date(incident.timestamp).toLocaleTimeString()}
                    </TableCell>
                    <TableCell sx={{ color: '#E8EDF5', fontSize: '0.8rem' }}>
                      {getIncidentIcon(incident.type)} {incident.type}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={incident.severity}
                        size="small"
                        sx={{
                          bgcolor: `${getSeverityColor(incident.severity)}15`,
                          color: getSeverityColor(incident.severity),
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={incident.status}
                        size="small"
                        sx={{
                          bgcolor: 'rgba(16,185,129,0.08)',
                          color: '#10B981',
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Box>
  );
}
```

## frontend/src/pages/MaintenancePlanner.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/MaintenancePlanner.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  useTheme,
  Alert,
} from '@mui/material';
import {
  Build,
  CheckCircle,
  Warning,
  Error,
  Circle,
  Schedule,
  PriorityHigh,
} from '@mui/icons-material';
import { getMaintenancePlan } from '../api/client';

// ✅ Mock data for when API fails
const MOCK_TASKS = [
  { priority: 'P1', asset: 'Heat Exchanger H-03', workOrder: 'Inspect thermal bypass', owner: 'Utilities Crew', state: 'Scheduled' },
  { priority: 'P1', asset: 'Compressor C-12', workOrder: 'Bearing and vibration inspection', owner: 'Rotating Equipment', state: 'In Progress' },
  { priority: 'P2', asset: 'Valve V-09', workOrder: 'Calibrate pressure actuator', owner: 'Instrumentation', state: 'Pending' },
  { priority: 'P2', asset: 'Pump A-01', workOrder: 'Replace seals and gaskets', owner: 'Rotating Equipment', state: 'Scheduled' },
  { priority: 'P3', asset: 'Tank T-04', workOrder: 'Inspect level sensors', owner: 'Instrumentation', state: 'Pending' },
  { priority: 'P3', asset: 'Pipeline P-03', workOrder: 'Corrosion inspection', owner: 'Pipeline Crew', state: 'Completed' },
];

const PRIORITY_COLORS = {
  'P1': '#EF4444',
  'P2': '#F59E0B',
  'P3': '#3B82F6',
  'P4': '#10B981',
};

const PRIORITY_LABELS = {
  'P1': 'Critical',
  'P2': 'High',
  'P3': 'Medium',
  'P4': 'Low',
};

export default function MaintenancePlanner() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const response = await getMaintenancePlan();
      const data = response.data;
      
      // ✅ Handle different response formats
      let taskArray = [];
      if (Array.isArray(data)) {
        taskArray = data;
      } else if (data?.tasks && Array.isArray(data.tasks)) {
        taskArray = data.tasks;
      } else if (data?.data && Array.isArray(data.data)) {
        taskArray = data.data;
      } else {
        taskArray = MOCK_TASKS;
      }
      
      setTasks(taskArray.length > 0 ? taskArray : MOCK_TASKS);
    } catch (e) {
      console.error('Failed to load maintenance plan, using mock data:', e);
      setTasks(MOCK_TASKS);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    return PRIORITY_COLORS[priority] || '#8899B4';
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading maintenance plan...</Typography>
      </Box>
    );
  }

  const totalTasks = tasks.length;
  const criticalTasks = tasks.filter(t => t.priority === 'P1').length;
  const completedTasks = tasks.filter(t => t.state === 'Completed').length;
  const inProgressTasks = tasks.filter(t => t.state === 'In Progress').length;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Maintenance Planner
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {totalTasks} tasks · {criticalTasks} critical
          </Typography>
        </Box>
        <Chip
          label={`${completedTasks}/${totalTasks} completed`}
          sx={{
            bgcolor: 'rgba(16,185,129,0.08)',
            color: '#10B981',
            border: '1px solid rgba(16,185,129,0.15)',
          }}
        />
      </Box>

      {/* Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total Tasks
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {totalTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Critical
              </Typography>
              <Typography variant="h5" sx={{ color: '#EF4444', fontWeight: 600 }}>
                {criticalTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Completed
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {completedTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                In Progress
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {inProgressTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Task Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Priority</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Asset</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Work Order</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Owner</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No maintenance tasks scheduled
                </TableCell>
              </TableRow>
            ) : (
              tasks.map((task, index) => {
                const priorityColor = getPriorityColor(task.priority);
                const isCompleted = task.state === 'Completed';
                const isCritical = task.priority === 'P1';
                const isInProgress = task.state === 'In Progress';
                
                let statusColor = '#5A6B8A';
                if (isCompleted) statusColor = '#10B981';
                else if (isInProgress) statusColor = '#F59E0B';
                else if (isCritical) statusColor = '#EF4444';

                const icon = isCompleted ? 
                  <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} /> : 
                  isCritical ? 
                  <Error sx={{ fontSize: 14, color: '#EF4444' }} /> :
                  <Warning sx={{ fontSize: 14, color: '#F59E0B' }} />;

                return (
                  <TableRow
                    key={index}
                    sx={{
                      borderBottom: '1px solid rgba(56,78,112,0.05)',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                      opacity: isCompleted ? 0.6 : 1,
                    }}
                  >
                    <TableCell>
                      <Chip
                        icon={icon}
                        label={`${task.priority} - ${PRIORITY_LABELS[task.priority] || ''}`}
                        size="small"
                        sx={{
                          bgcolor: `${priorityColor}15`,
                          color: priorityColor,
                          border: `1px solid ${priorityColor}20`,
                          fontSize: '0.65rem',
                          fontWeight: 500,
                          height: 24,
                        }}
                      />
                    </TableCell>
                    <TableCell sx={{ color: '#E8EDF5' }}>{task.asset || 'N/A'}</TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{task.workOrder || task.description || 'N/A'}</TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{task.owner || 'Unassigned'}</TableCell>
                    <TableCell>
                      <Chip
                        label={task.state || 'Pending'}
                        size="small"
                        sx={{
                          bgcolor: `${statusColor}15`,
                          color: statusColor,
                          border: `1px solid ${statusColor}20`,
                          fontSize: '0.6rem',
                          fontWeight: 500,
                          height: 20,
                        }}
                      />
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Summary Alert */}
      {criticalTasks > 0 && (
        <Alert severity="error" sx={{ mt: 2 }}>
          <Typography variant="body2">
            ⚠️ {criticalTasks} critical task(s) require immediate attention!
          </Typography>
        </Alert>
      )}
    </Box>
  );
}
```

## frontend/src/pages/Reports.jsx

**Folder path:** `frontend/src/pages`

**File path:** `frontend/src/pages/Reports.jsx`

```jsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Alert,
} from '@mui/material';
import {
  Description,
  Download,
  CheckCircle,
  Warning,
  Error,
  Circle,
  Refresh,
} from '@mui/icons-material';
import { getReports } from '../api/client';

// ✅ Mock data for when API fails
const MOCK_REPORTS = [
  { id: 'RPT-0001', title: 'Incident Response Report', workflow: 'Pressure Response', status: 'Completed', generated: '2026-07-25 00:25:00', summary: 'Pressure spike resolved successfully', recommendations: ['Inspect relief valve', 'Monitor pressure'] },
  { id: 'RPT-0002', title: 'Maintenance Summary', workflow: 'Maintenance Response', status: 'Pending', generated: '2026-07-25 00:20:00', summary: 'Maintenance tasks scheduled', recommendations: ['Schedule inspection'] },
  { id: 'RPT-0003', title: 'Asset Health Report', workflow: 'Health Check', status: 'Completed', generated: '2026-07-25 00:15:00', summary: 'All assets within parameters', recommendations: ['Continue monitoring'] },
  { id: 'RPT-0004', title: 'Safety Analysis', workflow: 'Safety Check', status: 'Escalated', generated: '2026-07-25 00:10:00', summary: 'Safety concern detected', recommendations: ['Immediate inspection required'] },
  { id: 'RPT-0005', title: 'Prediction Report', workflow: 'Prediction', status: 'In Progress', generated: '2026-07-25 00:05:00', summary: 'Calculating failure probabilities', recommendations: [] },
];

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const response = await getReports();
      // ✅ Ensure reports is always an array
      const data = response.data;
      if (Array.isArray(data)) {
        setReports(data);
      } else if (data && typeof data === 'object') {
        // If it's an object, try to find array property
        const arrayData = data.reports || data.tasks || data.results || data.items;
        if (Array.isArray(arrayData)) {
          setReports(arrayData);
        } else {
          console.warn('Reports data is not an array, using mock data');
          setReports(MOCK_REPORTS);
        }
      } else {
        setReports(MOCK_REPORTS);
      }
    } catch (e) {
      console.error('Failed to load reports, using mock data:', e);
      setReports(MOCK_REPORTS);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'Completed': '#10B981',
      'Pending': '#F59E0B',
      'Escalated': '#EF4444',
      'In Progress': '#3B82F6',
    };
    return colors[status] || '#8899B4';
  };

  const getStatusIcon = (status) => {
    const icons = {
      'Completed': <CheckCircle sx={{ fontSize: 14, color: '#10B981' }} />,
      'Pending': <Warning sx={{ fontSize: 14, color: '#F59E0B' }} />,
      'Escalated': <Error sx={{ fontSize: 14, color: '#EF4444' }} />,
      'In Progress': <Circle sx={{ fontSize: 10, color: '#3B82F6' }} />,
    };
    return icons[status] || <Circle sx={{ fontSize: 10, color: '#8899B4' }} />;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography sx={{ color: '#5A6B8A' }}>Loading reports...</Typography>
      </Box>
    );
  }

  const totalReports = reports.length;
  const completedReports = reports.filter(r => r.status === 'Completed').length;
  const pendingReports = reports.filter(r => r.status === 'Pending').length;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ color: '#E8EDF5', fontWeight: 600, mb: 0.5 }}>
            Reports & Intelligence
          </Typography>
          <Typography variant="body2" sx={{ color: '#8899B4' }}>
            {totalReports} reports generated
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={loadData}
          sx={{
            borderColor: 'rgba(56,78,112,0.2)',
            color: '#8899B4',
            '&:hover': { borderColor: 'rgba(56,78,112,0.4)' },
          }}
        >
          Refresh
        </Button>
      </Box>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Total Reports
              </Typography>
              <Typography variant="h5" sx={{ color: '#E8EDF5', fontWeight: 600 }}>
                {totalReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Completed
              </Typography>
              <Typography variant="h5" sx={{ color: '#10B981', fontWeight: 600 }}>
                {completedReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Pending Review
              </Typography>
              <Typography variant="h5" sx={{ color: '#F59E0B', fontWeight: 600 }}>
                {pendingReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card sx={{ bgcolor: 'rgba(18,28,46,0.6)' }}>
            <CardContent sx={{ py: 1.5 }}>
              <Typography variant="caption" sx={{ color: '#5A6B8A', textTransform: 'uppercase', fontSize: '0.6rem' }}>
                Escalated
              </Typography>
              <Typography variant="h5" sx={{ color: '#EF4444', fontWeight: 600 }}>
                {totalReports - completedReports - pendingReports}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'rgba(255,255,255,0.01)' }}>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Report</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Title</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Workflow</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Status</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Generated</TableCell>
              <TableCell sx={{ color: '#5A6B8A', fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {reports.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ color: '#5A6B8A', py: 4 }}>
                  No reports generated yet
                </TableCell>
              </TableRow>
            ) : (
              reports.map((report, index) => {
                const statusColor = getStatusColor(report.status);
                return (
                  <TableRow
                    key={index}
                    sx={{
                      borderBottom: '1px solid rgba(56,78,112,0.05)',
                      '&:hover': { bgcolor: 'rgba(255,255,255,0.02)' },
                      cursor: 'pointer',
                    }}
                    onClick={() => setSelectedReport(selectedReport === index ? null : index)}
                  >
                    <TableCell sx={{ color: '#3B82F6', fontWeight: 500, fontSize: '0.8rem' }}>
                      {report.id || `RPT-${String(index + 1).padStart(4, '0')}`}
                    </TableCell>
                    <TableCell sx={{ color: '#E8EDF5' }}>{report.title || report.workflow || 'Untitled'}</TableCell>
                    <TableCell sx={{ color: '#8899B4' }}>{report.workflow || 'N/A'}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getStatusIcon(report.status)}
                        label={report.status || 'Unknown'}
                        size="small"
                        sx={{
                          bgcolor: `${statusColor}15`,
                          color: statusColor,
                          border: `1px solid ${statusColor}20`,
                          fontSize: '0.65rem',
                          fontWeight: 500,
                          height: 24,
                        }}
                      />
                    </TableCell>
                    <TableCell sx={{ color: '#5A6B8A', fontSize: '0.75rem' }}>
                      {report.generated || report.timestamp || 'N/A'}
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        startIcon={<Download sx={{ fontSize: 14 }} />}
                        sx={{
                          color: '#3B82F6',
                          fontSize: '0.65rem',
                          textTransform: 'none',
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          // Download logic
                        }}
                      >
                        Export
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {selectedReport !== null && reports[selectedReport] && (
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" sx={{ color: '#8899B4', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem', fontWeight: 600, mb: 2 }}>
            Report Detail
          </Typography>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ color: '#E8EDF5' }}>
              {reports[selectedReport].summary || 'No summary available for this report.'}
            </Typography>
          </Alert>
          <Typography variant="caption" sx={{ color: '#5A6B8A' }}>
            Recommendations: {reports[selectedReport].recommendations?.length || 0}
          </Typography>
        </Paper>
      )}
    </Box>
  );
}
```

## frontend/src/styles/theme.js

**Folder path:** `frontend/src/styles`

**File path:** `frontend/src/styles/theme.js`

```javascript
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#3B82F6',      // Industrial blue
      light: '#60A5FA',
      dark: '#1D4ED8',
    },
    secondary: {
      main: '#10B981',      // Status green
      light: '#34D399',
      dark: '#059669',
    },
    error: {
      main: '#EF4444',      // Alert red
    },
    warning: {
      main: '#F59E0B',      // Warning amber
    },
    info: {
      main: '#3B82F6',
    },
    success: {
      main: '#10B981',
    },
    background: {
      default: '#0A0F1A',
      paper: 'rgba(18, 28, 46, 0.92)',
    },
    text: {
      primary: '#E8EDF5',
      secondary: '#8899B4',
    },
  },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    h1: {
      fontWeight: 600,
      color: '#E8EDF5',
      fontSize: '2.25rem',
      letterSpacing: '-0.02em',
    },
    h4: {
      fontWeight: 600,
      color: '#E8EDF5',
      letterSpacing: '-0.01em',
    },
    h5: {
      fontWeight: 500,
      color: '#E8EDF5',
    },
    h6: {
      fontWeight: 500,
      color: '#8899B4',
      textTransform: 'uppercase',
      letterSpacing: '0.08em',
      fontSize: '0.75rem',
    },
    body1: {
      color: '#E8EDF5',
    },
    body2: {
      color: '#8899B4',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'rgba(18, 28, 46, 0.85)',
          border: '1px solid rgba(56, 78, 112, 0.15)',
          borderRadius: '8px',
          boxShadow: '0 4px 24px rgba(0,0,0,0.3)',
          transition: 'all 0.2s ease',
          '&:hover': {
            borderColor: 'rgba(59, 130, 246, 0.2)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'rgba(18, 28, 46, 0.85)',
          border: '1px solid rgba(56, 78, 112, 0.12)',
          borderRadius: '8px',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: 'rgba(10, 15, 26, 0.98)',
          borderRight: '1px solid rgba(56, 78, 112, 0.1)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'rgba(10, 15, 26, 0.92)',
          backdropFilter: 'blur(12px)',
          borderBottom: '1px solid rgba(56, 78, 112, 0.08)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '6px',
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
  },
});
```

## frontend/vite.config.js

**Folder path:** `frontend`

**File path:** `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
})
```
