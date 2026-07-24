# Folder: agents Code Inventory

Generated: 2026-07-24 12:23:53 UTC

Contains 11 project files.

## agents/__init__.py

**File path:** `agents/__init__.py`

```python

```

## agents/base.py

**File path:** `agents/base.py`

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

## agents/diagnostic.py

**File path:** `agents/diagnostic.py`

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

## agents/knowledge.py

**File path:** `agents/knowledge.py`

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

## agents/maintenance.py

**File path:** `agents/maintenance.py`

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

## agents/notification.py

**File path:** `agents/notification.py`

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

## agents/planning.py

**File path:** `agents/planning.py`

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

## agents/prediction.py

**File path:** `agents/prediction.py`

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

## agents/report.py

**File path:** `agents/report.py`

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

## agents/safety.py

**File path:** `agents/safety.py`

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

## agents/sensor.py

**File path:** `agents/sensor.py`

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
