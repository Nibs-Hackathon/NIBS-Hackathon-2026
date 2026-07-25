# Folder: backend Code Inventory

Generated: 2026-07-25T06:06:30 UTC

**Folder path:** `backend`

Contains 157 project files.

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
