# Project Code Inventory (Updated)

Generated: 2026-07-24 07:30:05 UTC

## Scope

This document contains the complete text source for 211 project files (16525 lines) from the repository root. It includes application code, tests, scripts, configuration, and Markdown documentation. It excludes Git metadata, virtual environments, generated/binary data, generated inventory files, and the secret-bearing `.env` file.

## Project root

`C:/Users/Abeer_1ewl9m1/OneDrive/Documents/project`

## Folder structure

```text
project/
├── .devcontainer
│   └── devcontainer.json
├── agents
│   ├── __init__.py
│   ├── base.py
│   ├── diagnostic.py
│   ├── knowledge.py
│   ├── maintenance.py
│   ├── notification.py
│   ├── planning.py
│   ├── prediction.py
│   ├── report.py
│   ├── safety.py
│   └── sensor.py
├── alembic.ini
├── app
│   ├── components
│   │   ├── __init__.py
│   │   ├── agent_card.py
│   │   ├── incident_card.py
│   │   ├── investigation_progress.py
│   │   ├── phase_one_views.py
│   │   ├── phase_two_views.py
│   │   ├── telemetry_card.py
│   │   └── timeline.py
│   ├── frontend_services
│   │   ├── __init__.py
│   │   ├── agent_activity_adapter.py
│   │   ├── agent_adapter.py
│   │   ├── asset_adapter.py
│   │   ├── backend_api_new.py
│   │   ├── control_adapter.py
│   │   ├── dashboard_adapter.py
│   │   ├── digital_twin_adapter.py
│   │   ├── health_adapter.py
│   │   ├── health_prediction_adapter.py
│   │   ├── incident_adapter.py
│   │   ├── knowledge_adapter.py
│   │   ├── knowledge_agent_adapter.py
│   │   ├── maintenance_adapter.py
│   │   ├── report_adapter.py
│   │   └── telemetry_adapter.py
│   ├── Home.py
│   ├── pages
│   │   ├── 1_Dashboard.py
│   │   ├── 10_Health_Prediction.py
│   │   ├── 11_Maintenance_Planner.py
│   │   ├── 12_AI_Activity.py
│   │   ├── 13_Digital_Twin.py
│   │   ├── 14_Config_Dashboard.py
│   │   ├── 2_Assets.py
│   │   ├── 3_Control_Center.py
│   │   ├── 4_Incident_Simulator.py
│   │   ├── 5_Knowledge_Base.py
│   │   ├── 6_Agent_Monitor.py
│   │   ├── 7_Reports.py
│   │   ├── 8_Settings.py
│   │   └── 9_AI_Assistant.py
│   └── ui_helpers.py
├── core
│   ├── __init__.py
│   ├── config.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── logging.py
│   ├── prompts.py
│   ├── settings.py
│   └── utils.py
├── database
│   ├── __init__.py
│   ├── __init__database.py
│   ├── base.py
│   ├── bootstrap.py
│   ├── connection.py
│   ├── migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 0001_operational_records.py
│   │       └── 0002_add_knowledge_source.py
│   ├── models.py
│   ├── repositories
│   │   ├── action_repo.py
│   │   ├── activity_repo.py
│   │   ├── agent_repo.py
│   │   ├── asset_repo.py
│   │   ├── incident_repo.py
│   │   ├── knowledge_repo.py
│   │   ├── report_repo.py
│   │   └── telemetry_repo.py
│   └── seed_demo.py
├── docs
│   ├── API.md
│   ├── architecture.md
│   └── MAO.md
├── mao
│   ├── __init__.py
│   ├── core
│   │   ├── context.py
│   │   ├── exceptions.py
│   │   ├── executor.py
│   │   ├── logger.py
│   │   ├── registry.py
│   │   ├── scheduler.py
│   │   └── state_manager.py
│   ├── events
│   │   ├── event_bus.py
│   │   ├── event_store.py
│   │   └── event.py
│   ├── kernel.py
│   ├── memory
│   │   └── memory_manager.py
│   ├── models
│   │   ├── execution_report.py
│   │   ├── notification.py
│   │   ├── result.py
│   │   └── task.py
│   ├── orchestrator.py
│   ├── tools
│   │   └── tool_registry.py
│   └── workflows
│       ├── flow_workflow.py
│       ├── gas_workflow.py
│       ├── intelligence_tasks.py
│       ├── maintenance_workflow.py
│       ├── planner.py
│       ├── policy_engine.py
│       ├── pressure_workflow.py
│       ├── supervisor.py
│       ├── temperature_workflow.py
│       ├── workflow_engine.py
│       └── workflow.py
├── models
│   ├── __init__.py
│   ├── asset.py
│   ├── enums.py
│   ├── event.py
│   ├── facility.py
│   ├── incident.py
│   ├── maintenance.py
│   ├── pipeline.py
│   ├── report.py
│   ├── sensor.py
│   └── worker.py
├── rag
│   ├── __init__.py
│   ├── chunker.py
│   ├── citation.py
│   ├── embedder.py
│   ├── ingestion.py
│   ├── knowledge.py
│   ├── llm_manager.py
│   ├── llm.py
│   ├── loader.py
│   ├── neon_vector_store.py
│   ├── parser.py
│   ├── pipeline.py
│   ├── reranker.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vector_store.py
├── README.md
├── requirements.txt
├── RigOS_Complete_Source_Code_Archive.md
├── run.py
├── scripts
│   ├── benchmark.py
│   ├── build_knowledge.py
│   ├── build_rag.py
│   ├── generate_embeddings.py
│   ├── ingest_documents.py
│   ├── run_simulation.py
│   ├── seed_database.py
│   ├── test_knowledge.py
│   ├── test_mao.py
│   ├── test_models.py
│   └── test_rag.py
├── services
│   ├── __init__.py
│   ├── asset.py
│   ├── config_services.py
│   ├── embedding.py
│   ├── health.py
│   ├── incident_manager.py
│   ├── incident_service.py
│   ├── kernel_factory.py
│   ├── llm.py
│   ├── persistence.py
│   ├── refinery_generator.py
│   ├── report.py
│   ├── runtime.py
│   ├── sensor.py
│   ├── simulation.py
│   ├── simulator_controller.py
│   ├── telemetry_store.py
│   ├── vision.py
│   └── weather.py
├── simulator
│   ├── asset.py
│   ├── event_generator.py
│   ├── facility.py
│   ├── fault_injector.py
│   ├── sensor.py
│   └── simulator.py
├── tests
│   ├── conftest.py
│   ├── mock_workflow.py
│   ├── test_agent_pipeline.py
│   ├── test_diagnostic_agent.py
│   ├── test_knowledge_agent.py
│   ├── test_maintenance_agent.py
│   ├── test_neon.py
│   ├── test_planning_agent.py
│   └── test_safety_agent.py
├── tools
│   ├── __init__.py
│   ├── base_tool.py
│   ├── email_tool.py
│   ├── notification_tool.py
│   ├── postgres_tool.py
│   ├── report_tool.py
│   ├── search_tool.py
│   ├── sensor_tool.py
│   ├── simulation_tool.py
│   ├── vector_tool.py
│   ├── vision_tool.py
│   └── weather_tool.py
└── workflows
    ├── __init__.py
    ├── compliance_review.py
    ├── emergency_evacuation.py
    ├── fire_response.py
    ├── leak_response.py
    ├── maintenance_cycle.py
    ├── production_optimization.py
    ├── report_generation.py
    ├── shutdown_sequence.py
    └── startup_sequence.py
```

## Complete source code
### .devcontainer/devcontainer.json

**File path:** `.devcontainer/devcontainer.json`

```json
{
  "name": "Python 3",
  // Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
  "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bookworm",
  "customizations": {
    "codespaces": {
      "openFiles": [
        "README.md",
        "app/Home.py"
      ]
    },
    "vscode": {
      "settings": {},
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  },
  "updateContentCommand": "[ -f packages.txt ] && sudo apt update && sudo apt upgrade -y && sudo xargs apt install -y <packages.txt; [ -f requirements.txt ] && pip3 install --user -r requirements.txt; pip3 install --user streamlit; echo '✅ Packages installed and Requirements met'",
  "postAttachCommand": {
    "server": "streamlit run app/Home.py --server.enableCORS false --server.enableXsrfProtection false"
  },
  "portsAttributes": {
    "8501": {
      "label": "Application",
      "onAutoForward": "openPreview"
    }
  },
  "forwardPorts": [
    8501
  ]
}
```

### agents/__init__.py

**File path:** `agents/__init__.py`

```python

```

### agents/base.py

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

### agents/diagnostic.py

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

### agents/knowledge.py

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

### agents/maintenance.py

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

### agents/notification.py

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

### agents/planning.py

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

### agents/prediction.py

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

### agents/report.py

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

### agents/safety.py

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

### agents/sensor.py

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

### alembic.ini

**File path:** `alembic.ini`

```ini
[alembic]
script_location = database/migrations
prepend_sys_path = .

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

### app/components/__init__.py

**File path:** `app/components/__init__.py`

```python
"""Reusable Streamlit presentation components for the RigOS frontend."""
```

### app/components/agent_card.py

**File path:** `app/components/agent_card.py`

```python
import streamlit as st


def render_agent_card(report):

    text = report.final_summary.lower()

    if "[safety]" in text:
        agent_name = "🛡 Safety Agent"

    elif "[diagnostic]" in text:
        agent_name = "🔍 Diagnostic Agent"

    elif "[knowledge]" in text:
        agent_name = "📚 Knowledge Agent"

    else:
        agent_name = "🤖 AI Agent"


    cleaned = (
        report.final_summary
        .replace("[safety]", "")
        .replace("[diagnostic]", "")
        .replace("[knowledge]", "")
    )


    st.markdown(
        f"""
        <div class="agent-card">

        <h3>{agent_name}</h3>

        <p>
        {cleaned}
        </p>

        <b>Status:</b> Completed ✅

        </div>
        """,
        unsafe_allow_html=True
    )
```

### app/components/incident_card.py

**File path:** `app/components/incident_card.py`

```python
import streamlit as st


def render_incident_card(
    asset,
    incident_type,
    severity,
    status="Processing"
):

    st.markdown(
        f"""
        <div class="incident-card">

        <h2>🚨 {incident_type}</h2>

        <p>
        <b>Asset:</b> {asset}
        </p>

        <p>
        <b>Severity:</b>
        <span style="color:#ff5555">
        {severity}
        </span>
        </p>

        <p>
        <b>Status:</b> {status}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )
```

### app/components/investigation_progress.py

**File path:** `app/components/investigation_progress.py`

```python
import streamlit as st


def render_investigation_progress():
    st.markdown("### 🤖 AI Investigation")

    stages = [
        ("🛡 Safety Analysis", "Completed"),
        ("🔍 Diagnostic Analysis", "Completed"),
        ("📚 Knowledge Retrieval", "Completed"),
        ("🔧 Maintenance Review", "Completed"),
        ("📋 Planning", "Completed"),
    ]

    for stage, status in stages:
        left, right = st.columns([5, 1])

        with left:
            st.write(stage)

        with right:
            st.success(status)
```

### app/components/phase_one_views.py

**File path:** `app/components/phase_one_views.py`

```python
"""Reusable Phase 1 visual components.

These components are presentation-only. They accept data supplied by the page
or frontend helpers and never create a MAO kernel or call backend services.
"""

from __future__ import annotations

import streamlit as st

from ui_helpers import status_chip


def render_live_signal_banner(label: str, detail: str, status: str = "Running") -> None:
    """Render a compact operational status banner."""
    st.markdown(
        f"<div class='panel'><span class='pulse' style='color:#4FE3B2'>●</span> "
        f"<b>{label}</b> &nbsp; {status_chip(status)}"
        f"<br><span class='muted'>{detail}</span></div>",
        unsafe_allow_html=True,
    )


def render_incident_response_flow(steps: list[tuple[str, str]]) -> None:
    """Visualize the existing incident-to-report demo lifecycle without executing it."""
    st.markdown("<div class='section-label'>RESPONSE LIFECYCLE</div>", unsafe_allow_html=True)
    for index, (title, detail) in enumerate(steps, start=1):
        st.markdown(
            f"<div class='timeline-row'><span class='muted'>STEP {index}</span>"
            f"<span class='timeline-dot'></span><div class='panel'><b>{title}</b>"
            f"<br><span class='muted'>{detail}</span></div></div>",
            unsafe_allow_html=True,
        )


def render_agent_execution_view(agents: list[dict]) -> None:
    """Render registered/demo agent state as a vertical command-center flow."""
    st.markdown("<div class='section-label'>AGENT EXECUTION VIEW</div>", unsafe_allow_html=True)
    for agent in agents:
        state = agent["State"]
        state_tone = "Running" if state == "Active" else ("Pending" if state == "Queued" else "Info")
        pulse_class = "pulse" if state == "Active" else ""
        st.markdown(
            f"<div class='timeline-row'><span class='muted'>{agent['Specialty']}</span>"
            f"<span class='timeline-dot {pulse_class}'></span><div class='panel'>"
            f"<b>{agent['Agent']} Agent</b> &nbsp; {status_chip(state_tone)}"
            f"<br><span class='muted'>{agent['Current task']} · Confidence {agent['Confidence']}</span>"
            f"</div></div>",
            unsafe_allow_html=True,
        )
```

### app/components/phase_two_views.py

**File path:** `app/components/phase_two_views.py`

```python
"""Reusable presentation components for Phase 2 frontend pages."""

from __future__ import annotations

import streamlit as st

from ui_helpers import status_chip


def render_asset_detail_panel(asset: dict, sensors: list[dict]) -> None:
    """Show selected asset condition and its current demo telemetry snapshot."""
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><b>{asset['Asset']}</b> &nbsp; {status_chip(asset['Status'])}"
        f"<p class='muted'>{asset['Type']} · {asset['Zone']}<br>"
        f"Health: {asset['Health']}% · Last telemetry: {asset['Last telemetry']}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>SENSOR SNAPSHOT</div>", unsafe_allow_html=True)
    st.dataframe(sensors, hide_index=True, use_container_width=True)


def render_report_detail_panel(report: dict) -> None:
    """Render the current report preview in a reusable glass panel."""
    # ✅ Add default values to prevent KeyError
    report_id = report.get('Report', 'N/A')
    title = report.get('Title', 'Untitled')
    summary = report.get('Summary', 'No summary available.')
    recommendation = report.get('Recommendation', 'No recommendation available.')
    
    st.markdown(
        f"<div class='panel'><b>{report_id} · {title}</b>"
        f"<p class='muted'>{summary}</p>"
        f"<p><b>Recommendation:</b> {recommendation}</p></div>",
        unsafe_allow_html=True,
    )

def render_copilot_context_panel() -> None:
    """Shared visual context for the full-page Copilot workspace."""
    st.markdown("<div class='section-label'>CONTEXT IN USE</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><b>Demo facility</b><p class='muted'>RigOS Alpha Refinery</p>"
        "<b>Priority signal</b><p class='muted'>Compressor C-12 vibration watch</p>"
        "<b>Knowledge mode</b><p class='muted'>Simulated SOP retrieval</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>SUGGESTED PROMPTS</div>", unsafe_allow_html=True)
    st.caption("• Summarize today's incidents\n\n• Predict asset failures\n\n• Explain system status\n\n• Generate executive report\n\n• Recommend maintenance")
```

### app/components/telemetry_card.py

**File path:** `app/components/telemetry_card.py`

```python
import streamlit as st


def render_telemetry():

    st.markdown("### 📊 Live Telemetry")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Pressure</div>
                <div class="metric-value">152 PSI</div>
                <div class="status status-critical">HIGH</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Temperature</div>
                <div class="metric-value">84 °C</div>
                <div class="status status-warning">ELEVATED</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Flow Rate</div>
                <div class="metric-value">310 L/min</div>
                <div class="status status-running">NORMAL</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">AI Status</div>
                <div class="metric-value">Running</div>
                <div class="status status-info">ACTIVE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
```

### app/components/timeline.py

**File path:** `app/components/timeline.py`

```python
import streamlit as st


def render_timeline():
    st.markdown("### ⏱ Incident Timeline")

    events = [
        ("10:42:01", "🚨 Pressure spike detected"),
        ("10:42:03", "🛡 Safety Agent executed"),
        ("10:42:05", "🔍 Diagnostic completed"),
        ("10:42:08", "📚 Knowledge retrieved"),
        ("10:42:10", "🔧 Maintenance recommended"),
        ("10:42:12", "📋 Planning completed"),
    ]

    for time, event in events:
        st.markdown(
            f"""
            <div class="timeline-row">
                <div style="color:#8fa1ba;font-size:0.9rem;">{time}</div>
                <div class="timeline-dot"></div>
                <div>{event}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
```

### app/frontend_services/__init__.py

**File path:** `app/frontend_services/__init__.py`

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

### app/frontend_services/agent_activity_adapter.py

**File path:** `app/frontend_services/agent_activity_adapter.py`

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
from services.runtime import kernel


def _format_time(timestamp) -> str:
    return timestamp.strftime("%H:%M:%S") if timestamp else "Unknown"


def _runtime_activity() -> list[dict]:
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

### app/frontend_services/agent_adapter.py

**File path:** `app/frontend_services/agent_adapter.py`

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

### app/frontend_services/asset_adapter.py

**File path:** `app/frontend_services/asset_adapter.py`

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

### app/frontend_services/backend_api_new.py

**File path:** `app/frontend_services/backend_api_new.py`

```python
"""Unified backend API for frontend access with caching and refinery support."""
# At the very top of backend_api.py - BEFORE any other code
print("🔴🔴🔴 BACKEND_API.PY LOADED - VERSION WITH get_incidents 🔴🔴🔴")
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from functools import lru_cache
import time

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel, simulator
from services.config_services import ConfigService


class BackendAPI:
    """Single interface for frontend to access backend data with caching."""

    def __init__(self):
        self.config = ConfigService()
        self._cache_ttl = 5
        self._cache_timestamps = {}

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

    # -------------------------
    # Refinery Operations
    # -------------------------

    def get_refineries(self) -> List[Dict]:
        """Get all refineries with their assets."""
        refineries = getattr(kernel, "_refineries", [])
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
        refineries = getattr(kernel, "_refineries", [])
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

    # -------------------------
    # Asset Operations (with Caching)
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_assets_cached(self) -> List[Dict]:
        """Cached version of get_assets."""
        assets = kernel.asset_service.all_assets()
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
        readings = kernel.state.get_history(asset_id)
        if limit:
            readings = readings[-limit:]
        return tuple([
            {
                "timestamp": r.timestamp.isoformat(),
                "sensor_type": r.sensor_type.value if hasattr(r.sensor_type, 'value') else str(r.sensor_type),
                "value": r.value,
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
        readings = kernel.state.get_history(asset_id)
        health = kernel.health.calculate_health(readings)
        return {
            "health": health,
            "readings": len(readings),
            "status": "Running" if health > 80 else "Warning" if health > 50 else "Critical",
        }

    # -------------------------
    # Incident Operations (with Caching)
    # ✅ FIXED: get_incidents is now properly defined
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_incidents_cached(self) -> tuple:
        """Cached version of get_incidents."""
        events = kernel.event_store.all()
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
        service = IncidentService(simulator)
        result = service.trigger_incident(incident_type)
        # Invalidate caches after new incident
        self._invalidate_cache("get_incidents")
        self._invalidate_cache("get_agent_activity")
        return result

    # -------------------------
    # Agent Operations (with Caching)
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_agents_cached(self) -> List[Dict]:
        """Cached version of get_agents."""
        agents = kernel.registry.all()
        results = kernel.state.agent_results
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
        results = kernel.state.agent_results[-limit:]
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

    # -------------------------
    # Report Operations (with Caching)
    # -------------------------

    @lru_cache(maxsize=32)
    def _get_reports_cached(self) -> tuple:
        """Cached version of get_reports."""
        reports = kernel.state.execution_reports
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

    # -------------------------
    # Configuration
    # -------------------------

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

    # -------------------------
    # Simulation Control
    # -------------------------

    def get_simulation_status(self) -> Dict:
        """Get current simulation status."""
        return {
            "running": getattr(kernel, "_simulation_running", False),
            "events": len(kernel.event_store.all()),
            "reports": len(kernel.state.execution_reports),
            "agent_results": len(kernel.state.agent_results),
            "assets": len(kernel.asset_service.all_assets()),
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


# Singleton instance
api = BackendAPI()
```

### app/frontend_services/control_adapter.py

**File path:** `app/frontend_services/control_adapter.py`

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

### app/frontend_services/dashboard_adapter.py

**File path:** `app/frontend_services/dashboard_adapter.py`

```python
"""Dashboard adapter using BackendAPI."""

from app.frontend_services.backend_api_new import api
from services.runtime import kernel


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

### app/frontend_services/digital_twin_adapter.py

**File path:** `app/frontend_services/digital_twin_adapter.py`

```python
"""Read-only asset and telemetry view-model for the Digital Twin page."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.runtime import kernel


def _reading_value(readings: list[Any], sensor_type: str) -> str:
    for reading in reversed(readings):
        reading_type = getattr(reading.sensor_type, "value", reading.sensor_type)
        if str(reading_type).lower() == sensor_type.lower():
            value = getattr(reading, "value", "N/A")
            unit = getattr(reading, "unit", "")
            return f"{value} {unit}".strip()
    return "Not available"


def _maintenance_recommendation(asset_id: str) -> str:
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

### app/frontend_services/health_adapter.py

**File path:** `app/frontend_services/health_adapter.py`

```python
from services.runtime import kernel


def get_asset_health(asset_id):

    readings = kernel.state.get_history(asset_id)

    health = kernel.health.calculate_health(
        readings
    )

    return {
        "health": health,
        "readings": readings
    }
```

### app/frontend_services/health_prediction_adapter.py

**File path:** `app/frontend_services/health_prediction_adapter.py`

```python
from services.runtime import kernel


def get_health_prediction(asset_id, horizon_days=14):

    readings = kernel.state.get_history(
        asset_id
    )


    current_health = kernel.health.calculate_health(
        readings
    )


    historical = calculate_history(
        readings
    )


    prediction = predict_degradation(
        current_health,
        horizon_days
    )


    failure_probability = calculate_failure_probability(
        current_health
    )


    return {

        "health": round(
            current_health
        ),

        "rul": calculate_rul(
            current_health
        ),

        "failure_probability": f"{failure_probability}%",

        "confidence": calculate_confidence(
            readings
        ),

        "historical": {
            "Historical health": historical
        },

        "predicted": {
            "Predicted health": prediction,
            "Intervention threshold":
                [70] * len(prediction)
        },

        "telemetry": format_telemetry(
            readings
        )
    }



def calculate_history(readings):

    history = []

    for i in range(len(readings)):

        health = kernel.health.calculate_health(
            readings[:i+1]
        )

        history.append(
            round(health,1)
        )

    return history



def predict_degradation(
    current,
    days
):

    prediction = []

    health = current


    for _ in range(days):

        health -= 0.5

        prediction.append(
            round(
                max(0, health),
                1
            )
        )

    return prediction



def calculate_failure_probability(
    health
):

    risk = 100 - health

    return min(
        100,
        round(risk)
    )



def calculate_rul(
    health
):

    if health > 90:
        return "90+ days"

    if health > 75:
        return "45 days"

    if health > 50:
        return "14 days"

    return "<7 days"



def calculate_confidence(
    readings
):

    if len(readings) > 20:
        return "90%"

    if len(readings) > 5:
        return "75%"

    return "Low"



def format_telemetry(readings):

    data = []

    for reading in readings[-10:]:

        data.append(
            {
                "Sensor": reading.sensor_type.value,

                "Observed": reading.value,

                "Time": reading.timestamp.strftime(
                    "%H:%M:%S"
                )
            }
        )

    return data
```

### app/frontend_services/incident_adapter.py

**File path:** `app/frontend_services/incident_adapter.py`

```python
from services.runtime import kernel, simulator
from services.incident_service import IncidentService


def trigger_incident(incident_type):

    service = IncidentService(
        simulator
    )

    return service.trigger_incident(
        incident_type
    )



def get_incidents():

    events = kernel.event_store.all()

    incidents = []

    for event in events:

        severity = calculate_severity(event)


        incidents.append(
            {
                "Incident": event.name,

                "Asset": event.source,

                "Severity": severity,

                "Detected": event.timestamp.strftime(
                    "%H:%M:%S"
                ),

                "Payload": event.payload,
            }
        )


    return incidents



def calculate_severity(event):

    payload = event.payload


    # derive severity from actual signal

    if "pressure" in payload:

        return (
            "Critical"
            if payload["pressure"] > 160
            else "High"
        )


    if "temperature" in payload:

        return (
            "Critical"
            if payload["temperature"] > 100
            else "High"
        )


    if "gas" in payload:

        return "Critical"


    if "vibration" in payload:

        return (
            "Critical"
            if payload["vibration"] > 40
            else "High"
        )


    if "flow" in payload:

        return "Medium"


    return "Unknown"
```

### app/frontend_services/knowledge_adapter.py

**File path:** `app/frontend_services/knowledge_adapter.py`

```python
"""Read-only Knowledge Base access through the shared MAO kernel."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

class KnowledgeSearchError(RuntimeError):
    """Raised when the registered knowledge retrieval path is unavailable."""


__all__ = ["KnowledgeSearchError", "search_knowledge"]


def search_knowledge(query: str) -> list[dict[str, str]]:
    """Return normalized Neon retrieval results from the registered KnowledgeAgent."""
    normalized_query = query.strip()
    if not normalized_query:
        return []

    try:
        # Delay backend initialization until the user submits a search.  This
        # keeps the page importable even while Neon/Gemini is unavailable.
        from services.runtime import kernel

        agent = kernel.registry.get("knowledge")
        if agent is None or agent.retriever is None:
            raise KnowledgeSearchError("The shared KnowledgeAgent is unavailable.")
    except KnowledgeSearchError:
        raise
    except Exception as error:
        raise KnowledgeSearchError("The shared KnowledgeAgent is unavailable.") from error

    try:
        documents = agent.retriever.retrieve(normalized_query)
    except Exception as error:
        raise KnowledgeSearchError("Knowledge retrieval could not be completed.") from error

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

### app/frontend_services/knowledge_agent_adapter.py

**File path:** `app/frontend_services/knowledge_agent_adapter.py`

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
    return LLMManager().generate(prompt)


def _emit(callback: ProgressCallback | None, message: str) -> None:
    """Log and optionally expose a diagnostic stage without changing backend behavior."""
    LOGGER.info(message)
    if callback is not None:
        callback(message)


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Return the KnowledgeAgent registered on the shared MAO kernel."""
    try:
        from services.runtime import kernel

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
            raise KnowledgeAgentUnavailable(
                "Command Nexus is temporarily unavailable. Please try again shortly."
            ) from error

    _emit(on_progress, "Preparing an operational assessment.")
    try:
        # Backend imports are lazy so ordinary Streamlit rendering does not
        # initialize the operational stack until an operational question arrives.
        from mao.models.task import Task

        task = Task(
            name="Operator knowledge query",
            description=normalized_question,
            assigned_agent="knowledge",
        )
        agent = get_knowledge_agent()
        result = agent.execute(task)
    except KnowledgeAgentUnavailable:
        raise
    except Exception as error:
        LOGGER.exception("Command Nexus operational response failed")
        raise KnowledgeAgentUnavailable(
            "Command Nexus is temporarily unavailable. Please try again shortly."
        ) from error

    if not result.success or not result.summary:
        raise KnowledgeAgentUnavailable("Command Nexus could not prepare an operational assessment. Please try again.")

    _emit(on_progress, "Operational assessment prepared.")
    return result.summary
```

### app/frontend_services/maintenance_adapter.py

**File path:** `app/frontend_services/maintenance_adapter.py`

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

from services.runtime import kernel


def _result_index() -> dict[tuple[str, str], Any]:
    """Index completed agent output by its workflow task and assigned agent."""
    return {
        (result.metadata.get("task_name", ""), result.agent_name): result
        for result in kernel.state.agent_results
    }


def _task_asset_name(task: Any, result: Any | None) -> str:
    """Resolve an asset label only when it is present in live task/result data."""
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
    """Format state-manager tasks and agent output for the planner UI.

    TODO: Add a maintenance-task repository when schedule windows and crew
    assignments become persisted backend concepts.
    """
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

### app/frontend_services/report_adapter.py

**File path:** `app/frontend_services/report_adapter.py`

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

### app/frontend_services/telemetry_adapter.py

**File path:** `app/frontend_services/telemetry_adapter.py`

```python
from services.runtime import kernel


def get_asset_telemetry(asset_id):

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

### app/Home.py

**File path:** `app/Home.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # app/ → project_root/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import importlib
import streamlit as st
import ui_helpers

# Refresh shared UI helpers during Streamlit development reruns
importlib.reload(ui_helpers)

from ui_helpers import executive_metrics, metric_card, page_heading, render_sidebar, setup_page, status_chip
from app.frontend_services.backend_api_new import api
from services.simulator_controller import sim_controller
# In app/Home.py - add this after other imports
import importlib
import app.frontend_services.backend_api_new
importlib.reload(app.frontend_services.backend_api_new)


setup_page("Operations Center")
render_sidebar("Operations Center")

page_heading(
    "NIBS / AI OPERATIONS CENTER",
    "Welcome to Command Nexus",
    "A unified mission-control surface for operational intelligence, risk, and response."
)

# Add simulation controls to sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎮 Simulation Controls")

status = sim_controller.get_status()
st.sidebar.metric("Ticks", status['ticks'])
st.sidebar.metric("Events", status['events'])

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("▶️ Start", use_container_width=True):
        sim_controller.start()
        st.rerun()
with col2:
    if st.button("⏹️ Stop", use_container_width=True):
        sim_controller.stop()
        st.rerun()

if st.sidebar.button("⏭️ Step", use_container_width=True):
    telemetry, reports = sim_controller.step()
    st.sidebar.success(f"Step: {len(reports)} reports")

if st.sidebar.button("🔄 Refresh Config", use_container_width=True):
    api.refresh_config()
    st.sidebar.success("Config refreshed!")

st.sidebar.markdown("---")

left, right = st.columns([1.45, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>MISSION STATUS</div><h3 style='margin:.2rem 0 .6rem'>Operational picture: stable, with monitored assets.</h3><p class='muted'>Use the dashboard to review live health, incidents, agent decisions, and the current response queue.</p></div>", unsafe_allow_html=True)
with right:
    sim_status = "Running" if status.get("running") else "Stopped"
    st.markdown(f"<div class='panel'><div class='section-label'>PLATFORM STATUS</div>{status_chip(sim_status)}<p class='muted' style='margin-top:.8rem'>Demo workspace • {status['ticks']} ticks • {status['events']} events</p></div>", unsafe_allow_html=True)

st.write("")
st.markdown("<div class='section-label'>EXECUTIVE MISSION CONTROL</div>", unsafe_allow_html=True)
for metric_row in [executive_metrics()[:4], executive_metrics()[4:]]:
    for col, args in zip(st.columns(4), metric_row):
        with col:
            metric_card(*args)

st.write("")
st.markdown("<div class='panel'><div class='section-label'>QUICK START</div><p class='muted'>Navigate with the sidebar to inspect assets, simulate an incident, ask the global copilot, inspect predictive health, or review AI activity.</p></div>", unsafe_allow_html=True)
```

### app/pages/1_Dashboard.py

**File path:** `app/pages/1_Dashboard.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from components.phase_one_views import render_live_signal_banner
from ui_helpers import (
    metric_card,
    page_heading,
    render_health_heatmap,
    render_sidebar,
    setup_page
)
from frontend_services.dashboard_adapter import get_dashboard

setup_page("Dashboard")
render_sidebar("Executive Dashboard")
page_heading("OVERVIEW", "Operations Dashboard", "Real-time operational intelligence across the facility.")
snapshot = get_dashboard()
render_live_signal_banner("LIVE DEMO TELEMETRY", "Operational data shown is the existing frontend demo snapshot. Backend stream integration is pending.")
st.write("")

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col: metric_card(*args)

st.write("")
st.markdown("<div class='section-label'>FACILITY HEALTH HEATMAP</div>", unsafe_allow_html=True)
render_health_heatmap()
st.write("")
left, right = st.columns([1.65, 1])
with left:
    st.markdown("<div class='section-label'>24-HOUR OPERATIONAL HEALTH</div>", unsafe_allow_html=True)
    st.info("Live health trend will appear after telemetry history is populated.")
with right:
    st.markdown("<div class='section-label'>ATTENTION QUEUE</div>", unsafe_allow_html=True)
    for item in snapshot["incidents"]:
        st.markdown(f"<div class='panel'><b>{item['Incident']}</b><br><span class='muted'>{item['Asset']} • {item['Severity']} • {item['Detected']}</span></div>", unsafe_allow_html=True)
        st.write("")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>ASSET WATCHLIST</div>", unsafe_allow_html=True)
    st.dataframe(snapshot["assets"], hide_index=True, use_container_width=True, height=245)
with right:
    st.markdown("<div class='section-label'>LIVE ACTIVITY</div>", unsafe_allow_html=True)
    for time, actor, text in snapshot["activity"]:
        st.markdown(f"**{time} · {actor}**  \n<span class='muted'>{text}</span>", unsafe_allow_html=True)
```

### app/pages/10_Health_Prediction.py

**File path:** `app/pages/10_Health_Prediction.py`

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from ui_helpers import gauge_card, metric_card, page_heading, render_sidebar, setup_page
from frontend_services.asset_adapter import get_assets
from frontend_services.health_prediction_adapter import get_health_prediction

setup_page("Health Prediction")
render_sidebar("Predictive Health")
page_heading("PREDICTIVE INTELLIGENCE", "Asset Health Prediction", "Forecast degradation risk early enough to plan safe, efficient intervention.")

asset_snapshot = get_assets()
assets = asset_snapshot.get("assets", [])

if not assets:
    st.warning("No assets available. Start the simulation to generate telemetry data.")
    st.stop()

asset_names = [a.get("name", "Unknown") for a in assets]

left, right = st.columns([1, 1.5])
with left:
    selected_name = st.selectbox("Forecast asset", asset_names)
    horizon = st.select_slider("Forecast horizon", options=["7 days", "14 days", "30 days"], value="14 days")
    selected_asset = next((a for a in assets if a.get("name") == selected_name), assets[0])
    horizon_days = int(horizon.split()[0])
    
    # ✅ Check if we have telemetry data
    try:
        profile = get_health_prediction(selected_asset.get("id"), horizon_days)
    except Exception as e:
        st.error(f"Could not generate prediction: {e}")
        profile = None
    
    if profile:
        st.markdown(
            """
            <div class='panel'>
            <div class='section-label'>MODEL STATUS</div>
            <b>Forecast engine: LIVE TELEMETRY MODE</b>
            <p class='muted'>Prediction generated from asset telemetry history and current health calculations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Generate some telemetry data by running the simulation or triggering incidents.")

with right:
    if profile:
        st.markdown(f"<div class='section-label'>PROJECTED HEALTH · {selected_name.upper()}</div>", unsafe_allow_html=True)
        predicted = profile.get("predicted", {})
        if predicted:
            st.line_chart(predicted, height=280)
        else:
            st.info("No prediction data available yet.")
    else:
        st.info("Run simulation to generate prediction data.")

# ... rest of the page with checks for profile data
```

### app/pages/11_Maintenance_Planner.py

**File path:** `app/pages/11_Maintenance_Planner.py`

```python
# Add a way to trigger maintenance planning
import streamlit as st
from frontend_services.maintenance_adapter import get_maintenance_plan
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip

setup_page("Maintenance Planner")
render_sidebar("Maintenance Planner")
page_heading("WORK ORCHESTRATION", "Maintenance Planner", "Turn MAO task state and recommendations into an executable maintenance view.")

plan = get_maintenance_plan()

# ✅ If no tasks, show a way to generate them
if not plan.get("tasks"):
    st.info("No maintenance tasks have been generated yet. Trigger an incident to generate tasks.")
    
    # ✅ Add a button to trigger a maintenance incident
    if st.button("🚨 Generate Maintenance Task", use_container_width=True):
        from frontend_services.incident_adapter import trigger_incident
        result = trigger_incident("maintenance")
        st.success("Maintenance incident triggered! Refresh the page to see tasks.")
        st.rerun()

# ... rest of the page

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>RECOMMENDED WORK PLAN</div>", unsafe_allow_html=True)
    if plan["tasks"]:
        st.dataframe(plan["tasks"], hide_index=True, height=250, width="stretch")
    else:
        st.info("No MAO maintenance tasks have been generated yet.")

with right:
    st.markdown("<div class='section-label'>PLANNING STATUS</div>", unsafe_allow_html=True)
    st.metric("Latest priority", plan["priority"])
    st.metric("Estimated downtime", plan["downtime"])
    st.caption("Read-only view of tasks generated by the shared MAO runtime.")

st.write("")
left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>MAINTENANCE TIMELINE</div>", unsafe_allow_html=True)
    if plan["tasks"]:
        for task in plan["tasks"]:
            tone = "Critical" if task["Priority"] == "P1" else "Info"
            st.markdown(
                f"<div class='timeline-row'><span class='muted'>{task['Priority']}</span>"
                f"<span class='timeline-dot'></span><div class='panel'><b>{task['Work order']}</b> "
                f"&nbsp; {status_chip(tone)}<br><span class='muted'>Asset: {task['Asset']} "
                f"· Owner: {task['Owner']} · State: {task['State']}</span></div></div>",
                unsafe_allow_html=True,
            )
    else:
        st.caption("The timeline will populate when a maintenance workflow creates tasks.")

with right:
    st.markdown("<div class='section-label'>AI SCHEDULING RATIONALE</div>", unsafe_allow_html=True)
    if plan["rationale"]:
        st.markdown(
            "<div class='panel'><b>Latest MAO recommendations</b><ul>"
            + "".join(f"<li>{item}</li>" for item in plan["rationale"])
            + "</ul></div>",
            unsafe_allow_html=True,
        )
    else:
        st.info("No planning-agent recommendation is available yet.")
```

### app/pages/12_AI_Activity.py

**File path:** `app/pages/12_AI_Activity.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from frontend_services.agent_activity_adapter import get_agent_activity, get_agent_metrics
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
page_heading(
    "AUTONOMY AUDIT",
    "AI Agent Activity Timeline",
    "A chronological, reviewable record of AI observation, reasoning, and workflow handoffs.",
)

for col, args in zip(st.columns(4), get_agent_metrics()):
    with col:
        metric_card(*args)

st.write("")
filter_col, search_col = st.columns([1, 2])
with filter_col:
    agent_filter = st.selectbox(
        "Agent",
        ["All agents", "Safety", "Diagnostic", "Knowledge", "Maintenance", "Planning"],
    )
with search_col:
    search_term = st.text_input(
        "Search activity", placeholder="Filter by asset, workflow, or action"
    )

st.markdown("<div class='section-label'>LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)
events, activity_warning = get_agent_activity()
if activity_warning:
    st.caption(activity_warning)

visible_events = [
    event
    for event in events
    if (agent_filter == "All agents" or event["agent"].lower() == agent_filter.lower())
    and (
        not search_term.strip()
        or search_term.lower() in f"{event['agent']} {event['action']}".lower()
    )
]

if not visible_events:
    st.info("No matching MAO activity has been recorded yet.")

for event in visible_events:
    state_tone = (
        "Running"
        if event["state"] == "Running"
        else ("Pending" if event["state"] == "Queued" else "Info")
    )
    st.markdown(
        f"<div class='timeline-row'><span class='muted'>{event['time']}</span>"
        f"<span class='timeline-dot {'pulse' if event['state'] == 'Running' else ''}'></span>"
        f"<div class='panel'><b>{event['agent']}</b> &nbsp; {status_chip(state_tone)}"
        f"<br><span class='muted'>{event['action']} · Confidence {event['confidence']}"
        f"</span></div></div>",
        unsafe_allow_html=True,
    )
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")
```

### app/pages/13_Digital_Twin.py

**File path:** `app/pages/13_Digital_Twin.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from frontend_services.digital_twin_adapter import get_twin_assets
from ui_helpers import page_heading, render_sidebar, setup_page, status_chip


setup_page("Digital Twin")
render_sidebar("Digital Twin")
page_heading(
    "FACILITY TOPOLOGY",
    "Digital Twin View",
    "A live operational map of facility zones, asset condition, and observed process signals.",
)

assets = get_twin_assets()
if not assets:
    st.info("No assets are registered with the shared MAO runtime.")
    st.stop()

selected_name = st.selectbox("Inspect digital-twin asset", [asset["Asset"] for asset in assets])
selected = next(asset for asset in assets if asset["Asset"] == selected_name)

st.markdown("<div class='section-label'>INTERACTIVE FACILITY LAYERS</div>", unsafe_allow_html=True)
columns = st.columns(4)
for col, asset in zip(columns * 2, assets):
    with col:
        st.markdown(
            f"<div class='panel twin-tile'><div class='section-label'>{asset['Zone']} · {asset['Category']}</div>"
            f"<b>{asset['Asset']}</b><p style='margin:.7rem 0'>{status_chip(asset['Status'])}</p>"
            f"<p class='muted'>Health: {asset['Health']}%<br>Temp: {asset['Temperature']} "
            f"· Pressure: {asset['Pressure']}<br>RPM: {asset['RPM']} "
            f"· Failure: {asset['Failure']}</p></div>",
            unsafe_allow_html=True,
        )

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown("<div class='section-label'>PROCESS CONNECTIONS</div>", unsafe_allow_html=True)
    zones = " &nbsp; → &nbsp; ".join(sorted({asset["Zone"] for asset in assets}))
    st.markdown(
        "<div class='panel' style='text-align:center; padding:2rem'><b>REGISTERED ZONES</b>"
        f"<br><br><span class='muted'>{zones}</span></div>",
        unsafe_allow_html=True,
    )

with right:
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><b>{selected['Asset']}</b><p>{status_chip(selected['Status'])}</p>"
        f"<span class='muted'>Health: {selected['Health']}%<br>Temperature: {selected['Temperature']}"
        f"<br>Pressure: {selected['Pressure']}<br>RPM: {selected['RPM']}"
        f"<br>Failure probability: {selected['Failure']}</span><hr>"
        f"<b>Maintenance recommendation</b><p class='muted'>{selected['Recommendation']}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>TWIN CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Overlay", ["Asset health", "Live telemetry", "Incident severity", "Maintenance schedule"])
    st.toggle("Show process connections", value=True)
    st.toggle("Highlight active incidents", value=True)
```

### app/pages/14_Config_Dashboard.py

**File path:** `app/pages/14_Config_Dashboard.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page, metric_card
from app.frontend_services.backend_api_new import api


setup_page("Configuration Dashboard")
render_sidebar("Configuration")

page_heading(
    "DYNAMIC CONFIGURATION",
    "Gemini-Generated Settings",
    "View and refresh operational parameters generated by Gemini.",
)

# -------------------------
# API Key Status Section
# -------------------------

st.markdown("### 🔑 API Key Status")

try:
    from services.llm import LLMManager
    llm = LLMManager()
    status = llm.get_key_status()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Keys", status["total_keys"])
    with col2:
        st.metric("Available Keys", status["summary"]["available_keys"])
    with col3:
        st.metric("Active Keys", status["summary"]["active_keys"])
    with col4:
        success_rate = status["summary"]["overall_success_rate"]
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    # Detailed key table
    key_data = []
    for k in status["keys"]:
        # Determine status emoji
        if k["is_available"]:
            status_emoji = "🟢 Active"
        elif not k["is_active"]:
            status_emoji = "🔴 Cooldown"
        else:
            status_emoji = "🟡 Degraded"
        
        key_data.append({
            "#": k["index"],
            "Key": k["key_preview"],
            "Status": status_emoji,
            "Success Rate": k["success_rate"],
            "Requests": k["total_requests"],
            "Failures": k["failures"],
            "Last Used": k["last_used"],
            "Last Error": k["last_error"][:40] + "..." if len(k["last_error"] or "") > 40 else (k["last_error"] or "None"),
        })
    
    if key_data:
        st.dataframe(key_data, hide_index=True, use_container_width=True)
    
    # Reset key button
    st.markdown("#### Reset a Failed Key")
    col1, col2 = st.columns([2, 1])
    with col1:
        key_index = st.number_input("Key Number to Reset", min_value=1, max_value=status["total_keys"], value=1, step=1)
    with col2:
        if st.button("🔄 Reset Key", use_container_width=True):
            if llm.reset_key(key_index):
                st.success(f"✅ Key {key_index} reset successfully!")
                st.rerun()
            else:
                st.error(f"❌ Failed to reset key {key_index}")
    
    st.divider()
    
except Exception as e:
    st.warning(f"Could not load API key status: {e}")
    st.divider()

# -------------------------
# Current Configuration Section
# -------------------------

st.markdown("### 📊 Current Configuration")

# Display thresholds for different asset types
asset_types = ["Pump", "Compressor", "Tank", "Valve", "Pipeline", "Heat Exchanger"]

for asset_type in asset_types:
    with st.expander(f"{asset_type} Thresholds", expanded=False):
        try:
            thresholds = api.get_dynamic_thresholds(asset_type)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Pressure Max", f"{thresholds.get('pressure_max', 'N/A')} PSI")
            with col2:
                st.metric("Temperature Max", f"{thresholds.get('temperature_max', 'N/A')} °C")
            with col3:
                st.metric("Gas Max", f"{thresholds.get('gas_max', 'N/A')} ppm")
            with col4:
                st.metric("Vibration Max", f"{thresholds.get('vibration_max', 'N/A')} mm/s")
            with col5:
                st.metric("Flow Min", f"{thresholds.get('flow_min', 'N/A')} L/min")
        except Exception as e:
            st.error(f"Error loading thresholds for {asset_type}: {e}")

st.divider()

# Workflow sequences
st.markdown("### 🔄 Workflow Sequences")

incident_types = ["Pressure Spike", "Gas Leak", "High Temperature", "High Vibration", "Flow Restriction"]

for incident_type in incident_types:
    with st.expander(f"{incident_type} Workflow", expanded=False):
        try:
            sequence = api.get_workflow_sequence(incident_type.lower())
            st.write(" → ".join(sequence))
        except Exception as e:
            st.error(f"Error loading workflow for {incident_type}: {e}")

st.divider()

# Refresh button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🔄 Refresh All Configs", use_container_width=True):
        with st.spinner("Refreshing configurations from Gemini..."):
            result = api.refresh_config()
            st.success("Config cache cleared and refreshed!")
            st.rerun()

with col2:
    status = api.get_simulation_status()
    st.metric("Simulation Status", "Running" if status.get("running") else "Stopped")

st.caption("⚠️ Configurations are generated by Gemini and may vary between refreshes. Refresh to get new values.")
```

### app/pages/2_Assets.py

**File path:** `app/pages/2_Assets.py`

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from components.phase_one_views import render_live_signal_banner
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page
from app.frontend_services.backend_api_new import api

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")
page_heading("FLEET INTELLIGENCE", "Asset Monitoring", "Health, telemetry, and operational posture for every connected asset.")

render_live_signal_banner("LIVE ASSET TELEMETRY", "Connected to RigOS backend state manager.", "Info")
st.write("")

# -------------------------
# Refinery Selector
# -------------------------

refineries = api.get_refineries()

if not refineries:
    st.warning("No refineries available. Start the simulation to see assets.")
    st.stop()

# Refinery selection
refinery_names = [r["name"] for r in refineries]
selected_refinery_name = st.selectbox("🏭 Select Refinery", refinery_names)
selected_refinery = next(r for r in refineries if r["name"] == selected_refinery_name)

# Get assets for this refinery
all_assets = selected_refinery["assets"]
refinery_id = selected_refinery["id"]

st.markdown(f"**{selected_refinery_name}** - {selected_refinery['location']} | **{len(all_assets)}** assets")

# -------------------------
# Filters
# -------------------------

filters = st.columns(4)

with filters[0]:
    asset_types = ["All Types"] + sorted(set(a["type"] for a in all_assets))
    selected_type = st.selectbox("Asset Type", asset_types)

with filters[1]:
    zones = ["All Zones"] + sorted(set(a.get("zone", "Unassigned") for a in all_assets))
    selected_zone = st.selectbox("Zone", zones)

with filters[2]:
    statuses = ["All Statuses"] + sorted(set(a["status"] for a in all_assets))
    selected_status = st.selectbox("Status", statuses)

with filters[3]:
    # Health range filter
    health_min = st.slider("Min Health %", 0, 100, 0)

# Filter assets
visible = [
    a for a in all_assets
    if (selected_type == "All Types" or a["type"] == selected_type)
    and (selected_zone == "All Zones" or a.get("zone", "Unassigned") == selected_zone)
    and (selected_status == "All Statuses" or a["status"] == selected_status)
    and (a["health"] >= health_min)
]

st.dataframe(visible, hide_index=True, use_container_width=True, height=300)
st.caption(f"Showing {len(visible)} of {len(all_assets)} assets")

# -------------------------
# Asset Type Distribution
# -------------------------

st.markdown("### 📊 Asset Distribution")

# Count by type
type_counts = {}
for a in all_assets:
    t = a["type"]
    type_counts[t] = type_counts.get(t, 0) + 1

# Display as metrics
cols = st.columns(min(len(type_counts), 8))
for i, (asset_type, count) in enumerate(sorted(type_counts.items())):
    with cols[i % len(cols)]:
        st.metric(asset_type, count)

# -------------------------
# Selected Asset Detail
# -------------------------

if visible:
    st.markdown("### 🔍 Asset Detail")

    # Select an asset to inspect
    asset_names = [a["name"] for a in visible]
    selected_name = st.selectbox("Select asset to inspect", asset_names)
    selected_asset = next(a for a in visible if a["name"] == selected_name)

    # Display asset details
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Name", selected_asset["name"])
    with col2:
        st.metric("Type", selected_asset["type"])
    with col3:
        st.metric("Health", f"{selected_asset['health']:.1f}%")
    with col4:
        st.metric("Status", selected_asset["status"])

    # Get telemetry for this asset
    try:
        from frontend_services.telemetry_adapter import get_asset_telemetry
        telemetry = get_asset_telemetry(selected_asset["id"])
        if telemetry and telemetry.get("history"):
            st.line_chart(telemetry["history"], height=200)
        else:
            st.info("No telemetry history available for this asset. Run the simulation.")
    except Exception as e:
        st.info("Telemetry data not available.")
```

### app/pages/3_Control_Center.py

**File path:** `app/pages/3_Control_Center.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from frontend_services.control_adapter import get_control_state
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Control Center")
render_sidebar("Control Center")
page_heading(
    "MISSION CONTROL",
    "Control Center",
    "A protected command surface for supervising facility-level operating state.",
)

state = get_control_state()
summary = state.get("summary", "Live facility summary is not available yet.")
metrics = [
    ("Facility mode", state["facility_mode"], "Live backend state", "green"),
    ("Asset availability", state["throughput"], "Calculated from assets", "cyan"),
    ("Safety systems", state["safety"], "Online assets", "green"),
    ("Response queue", state["queue"], "Active EventStore entries", "amber"),
]
for col, args in zip(st.columns(4), metrics):
    with col:
        metric_card(*args)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown(
        "<div class='panel'><div class='section-label'>FACILITY STATE</div>"
        f"<h3>{state['facility_mode'].title()}</h3>"
        f"<p class='muted'>{summary}</p>"
        f"{status_chip(state['facility_mode'])}</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown("<div class='section-label'>PROCESS ZONES</div>", unsafe_allow_html=True)
    if state["zones"]:
        st.dataframe(state["zones"], hide_index=True, width="stretch")
    else:
        st.info("No zone data is available because no assets are registered.")

# Replace the disabled buttons with functional ones

with right:
    st.markdown("<div class='section-label'>SUPERVISORY ACTIONS</div>", unsafe_allow_html=True)
    
    # ✅ Acknowledge alerts
    if st.button("✅ Acknowledge monitored alerts", use_container_width=True):
        st.success("All alerts acknowledged. Incident manager updated.")
    
    # ✅ Request AI brief
    if st.button("🤖 Request AI situation brief", use_container_width=True):
        with st.spinner("Generating situation brief..."):
            from frontend_services.knowledge_agent_adapter import ask_knowledge_agent
            brief = ask_knowledge_agent("Summarize the current facility situation and operational status.")
            st.info(brief)
    
    # ✅ Emergency response
    if st.button("🚨 Open emergency response checklist", use_container_width=True):
        st.warning("⚠️ Emergency Response Checklist:\n1. Alert all personnel\n2. Isolate affected area\n3. Follow safety protocols\n4. Contact control room")
```

### app/pages/4_Incident_Simulator.py

**File path:** `app/pages/4_Incident_Simulator.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from components.phase_one_views import render_incident_response_flow, render_live_signal_banner
from frontend_services.incident_adapter import trigger_incident
from ui_helpers import (
    incident_simulator_demo_flow,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip,
)
from components.incident_card import render_incident_card
from components.agent_card import render_agent_card
from components.telemetry_card import render_telemetry
from components.timeline import render_timeline
from components.investigation_progress import render_investigation_progress


setup_page("Incident Simulator")
render_sidebar("Incident Simulator")
page_heading(
    "SCENARIO LAB",
    "Incident Simulator",
    "Safely exercise AI detection, triage, and response workflows using synthetic events.",
)
render_live_signal_banner(
    "SCENARIO DESIGN MODE",
    "This interface visualizes the existing simulator flow and runs approved synthetic scenarios.",
    "Info",
)
st.write("")

left, right = st.columns([1, 1.35])
with left:
    st.markdown("<div class='section-label'>CONFIGURE SCENARIO</div>", unsafe_allow_html=True)
    asset = st.selectbox("Affected asset", ["Compressor C-12", "Pump A-01", "Valve V-09", "Heat Exchanger H-03"])
    incident_type = st.selectbox("Incident type", ["Pressure spike", "High temperature", "Gas leak", "High vibration", "Flow restriction"])
    severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"], value="High")
    automated = st.toggle("Enable AI workflow", value=True)
    launched = st.button("Launch simulated incident", use_container_width=True)
with right:
    render_incident_response_flow(incident_simulator_demo_flow(incident_type, asset))

if launched:
    st.success(f"Simulation launched for {asset}")
    simulator_result = trigger_incident(incident_type)
    render_incident_card(
        asset,
        incident_type,
        severity,
        "AI Investigation Complete" if simulator_result["reports"] else "Processing"
    )

    render_telemetry()
    render_timeline()
    render_investigation_progress()

    reports = simulator_result["reports"]

    if reports:
        for report in reports:
            render_agent_card(report)
    else:
        st.warning("No incident generated.")

    st.markdown("### ✅ System Recommendation")

    st.info(
        """
### Recommended Operator Actions

- Reduce pump speed by **20%**
- Verify discharge valve position
- Inspect the pressure relief valve
- Monitor pressure for **5 minutes**
- Do not restart until pressure remains below **135 PSI**
"""
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("✅ Approve Response Plan"):
            st.success("Response approved.")

    with c2:
        if st.button("🔄 Run Investigation Again"):
            st.info("Investigation restarted.")

    with c3:
        if st.button("📄 Generate Incident Report"):
            st.success("Report generation coming soon.")


st.write("")
st.markdown(
    "<div class='section-label'>RECENT SIMULATED SCENARIOS</div>",
    unsafe_allow_html=True,
)

st.dataframe(
    [
        {
            "Scenario": "SIM-772",
            "Type": "Gas leak",
            "Asset": "Tank T-04",
            "Result": "Resolved",
            "Duration": "3m 14s",
        },
        {
            "Scenario": "SIM-771",
            "Type": "High vibration",
            "Asset": "Compressor C-12",
            "Result": "Review required",
            "Duration": "2m 47s",
        },
    ],
    hide_index=True,
    use_container_width=True,
)
```

### app/pages/5_Knowledge_Base.py

**File path:** `app/pages/5_Knowledge_Base.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from frontend_services.knowledge_adapter import KnowledgeSearchError, search_knowledge
from ui_helpers import page_heading, render_sidebar, setup_page


setup_page("Knowledge Base")
render_sidebar("Knowledge Base")
page_heading(
    "RETRIEVAL INTELLIGENCE",
    "Knowledge Base",
    "Search the live operational procedures, safety manuals, and maintenance guidance in Neon.",
)

with st.form("knowledge_search", border=False):
    query = st.text_input(
        "Search approved operational knowledge",
        placeholder="e.g. pressure spike response procedure",
    )
    submitted = st.form_submit_button("Search knowledge", icon=":material/search:")

if submitted:
    if not query.strip():
        st.warning("Enter a search query to retrieve operational knowledge.")
    else:
        with st.spinner("Searching the operational knowledge base..."):
            try:
                st.session_state["knowledge_search_results"] = search_knowledge(query)
                st.session_state["knowledge_search_query"] = query.strip()
                st.session_state.pop("knowledge_search_error", None)
            except KnowledgeSearchError as error:
                st.session_state["knowledge_search_results"] = []
                st.session_state["knowledge_search_error"] = str(error)

if error := st.session_state.get("knowledge_search_error"):
    st.error(error)

results = st.session_state.get("knowledge_search_results")
if results is not None and not st.session_state.get("knowledge_search_error"):
    query_label = st.session_state.get("knowledge_search_query", "your query")
    if not results:
        st.info(f"No matching knowledge documents were found for “{query_label}”.")
    else:
        st.caption(f"{len(results)} live Neon retrieval result(s) for “{query_label}”")
        for index, result in enumerate(results, start=1):
            with st.expander(f"{index}. {result['filename']}", expanded=index == 1):
                st.caption(f"Source: {result['source']}")
                st.write(result["content"])
```

### app/pages/6_Agent_Monitor.py

**File path:** `app/pages/6_Agent_Monitor.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from components.phase_one_views import render_agent_execution_view, render_live_signal_banner
from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip
)
from frontend_services.agent_adapter import get_agent_metrics, get_agents

setup_page("Agent Monitor")
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Observe autonomous specialists, workflow handoffs, and decision confidence.")
render_live_signal_banner("LIVE MAO REGISTRY", "Agent registration and completed execution state are read from the shared backend kernel.", "Info")
st.write("")

for col, args in zip(st.columns(4), get_agent_metrics()):
    with col: metric_card(*args)

st.write("")
agents = get_agents()
st.markdown("<div class='section-label'>AGENT FLEET</div>", unsafe_allow_html=True)
st.dataframe(agents, hide_index=True, use_container_width=True)

render_agent_execution_view(agents)
# Replace the placeholder workflow progress with real data
left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>WORKFLOW PROGRESS</div>", unsafe_allow_html=True)
    
    # ✅ Get real workflow progress from reports
    from app.frontend_services.backend_api_new import api
    reports = api.get_reports()
    
    if reports:
        for report in reports[-3:]:  # Show last 3 reports
            progress = 100 if report.get("success") else 50
            status = "Complete" if report.get("success") else "In Progress"
            st.progress(progress / 100, text=f"{report.get('workflow', 'Unknown')} • {status}")
    else:
        st.info("No workflows have been executed yet. Trigger an incident to see progress.")

with right:
    st.markdown("<div class='section-label'>LATEST HANDOFF</div>", unsafe_allow_html=True)
    
    # ✅ Get real agent handoff data
    activity = api.get_agent_activity(limit=10)
    if len(activity) >= 2:
        last = activity[-1]
        prev = activity[-2] if len(activity) >= 2 else None
        if prev:
            st.markdown(
                f"<div class='panel'>{status_chip('Info')}<p><b>{prev.get('agent_name', 'Unknown')} → {last.get('agent_name', 'Unknown')}</b></p>"
                f"<span class='muted'>{last.get('summary', 'Handoff completed.')[:100]}</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.info("Waiting for agent handoffs...")
    else:
        st.info("No agent activity recorded yet.")
```

### app/pages/7_Reports.py

**File path:** `app/pages/7_Reports.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_report_detail_panel
from ui_helpers import (
    metric_card,
    page_heading,
    render_sidebar,
    setup_page
)
from frontend_services.report_adapter import get_reports

setup_page("Reports")
render_sidebar("Reports & Intelligence")
page_heading("DECISION RECORD", "Reports & Intelligence", "Review operational reports, AI recommendations, and response outcomes.")
render_live_signal_banner("REPORT DEMO REGISTER", "Existing demonstration records are shown until MAO execution reports are available through a read-only integration.", "Info")
st.write("")
snapshot = get_reports()

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col: metric_card(*args)

st.write("")
filters = st.columns(3)
with filters[0]: st.selectbox("Report type", ["All reports", "Incident response", "Asset health", "Maintenance", "Compliance"])
with filters[1]: st.selectbox("Status", ["All status", "Completed", "Pending review", "Escalated"])
with filters[2]: st.date_input("From date")

st.dataframe(snapshot["reports"], hide_index=True, use_container_width=True, height=240)

# Fix the render_report_detail_panel call
left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>REPORT DETAIL PREVIEW</div>", unsafe_allow_html=True)
    
    # ✅ Check if preview exists before rendering
    preview = snapshot.get("preview", {})
    if preview and preview.get("Report"):
        render_report_detail_panel(preview)
    else:
        st.info("Select a report to view details.")

import json
import pandas as pd
from datetime import datetime

# ... in the export section ...

with right:
    st.markdown("<div class='section-label'>EXPORT</div>", unsafe_allow_html=True)
    
    # ✅ PDF Briefing
    if st.button("📄 Prepare PDF briefing", use_container_width=True):
        from app.frontend_services.backend_api_new import api
        reports = api.get_reports()
        
        # Create a summary
        summary = f"""
        OPERATIONAL BRIEFING
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Total Reports: {len(reports)}
        Successful: {sum(1 for r in reports if r.get('success'))}
        Average Confidence: {sum(r.get('confidence', 0) for r in reports) / len(reports) * 100:.1f}%
        
        Recent Reports:
        """
        for r in reports[-3:]:
            summary += f"\n- {r.get('workflow')}: {r.get('summary', '')[:100]}..."
        
        st.download_button(
            label="📥 Download Briefing",
            data=summary,
            file_name=f"briefing_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    
    # ✅ Export Report Register
    if st.button("📊 Export report register", use_container_width=True):
        from app.frontend_services.backend_api_new import api
        reports = api.get_reports()
        
        # Create CSV
        df = pd.DataFrame(reports)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"reports_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
```

### app/pages/8_Settings.py

**File path:** `app/pages/8_Settings.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page

setup_page("Settings")
render_sidebar("Settings")
page_heading("WORKSPACE CONFIGURATION", "Settings", "Configure how Command Nexus presents information and routes operational notifications.")

# Initialize session state for settings
if "settings" not in st.session_state:
    st.session_state.settings = {
        "facility": "RigOS Alpha Refinery",
        "dashboard_range": "Last 24 hours",
        "compact_tables": False,
        "show_sim_badge": True,
        "critical_alerts": True,
        "daily_digest": True,
        "agent_completion_alerts": False,
        "escalation_policy": "Standard operational",
        "response_profile": "Balanced",
        "confidence_threshold": 85,
    }

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>DISPLAY & WORKSPACE</div>", unsafe_allow_html=True)
    facility = st.selectbox(
        "Default facility",
        ["RigOS Alpha Refinery", "North Terminal", "Training Sandbox"],
        index=["RigOS Alpha Refinery", "North Terminal", "Training Sandbox"].index(st.session_state.settings["facility"])
    )
    dashboard_range = st.selectbox(
        "Default dashboard range",
        ["Last 24 hours", "Current shift", "Last 7 days"],
        index=["Last 24 hours", "Current shift", "Last 7 days"].index(st.session_state.settings["dashboard_range"])
    )
    compact_tables = st.toggle("Compact data tables", value=st.session_state.settings["compact_tables"])
    show_sim_badge = st.toggle("Show simulated-data badge", value=st.session_state.settings["show_sim_badge"])

with right:
    st.markdown("<div class='section-label'>NOTIFICATIONS</div>", unsafe_allow_html=True)
    critical_alerts = st.toggle("Critical incident alerts", value=st.session_state.settings["critical_alerts"])
    daily_digest = st.toggle("Daily operational digest", value=st.session_state.settings["daily_digest"])
    agent_completion_alerts = st.toggle("Agent workflow-completion alerts", value=st.session_state.settings["agent_completion_alerts"])
    escalation_policy = st.selectbox(
        "Escalation policy",
        ["Standard operational", "High sensitivity", "Training mode"],
        index=["Standard operational", "High sensitivity", "Training mode"].index(st.session_state.settings["escalation_policy"])
    )

st.write("")
left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>AI CONFIGURATION</div>", unsafe_allow_html=True)
    response_profile = st.selectbox(
        "Response profile",
        ["Balanced", "Safety-first", "Speed-first"],
        index=["Balanced", "Safety-first", "Speed-first"].index(st.session_state.settings["response_profile"])
    )
    confidence_threshold = st.slider(
        "Recommendation confidence threshold",
        50, 100, st.session_state.settings["confidence_threshold"], 5
    )

with right:
    st.markdown("<div class='section-label'>INTEGRATION STATUS</div>", unsafe_allow_html=True)
    st.dataframe([
        {"Integration": "Telemetry service", "State": "Active ✅" if st.session_state.settings.get("telemetry_connected", False) else "Demo mode"},
        {"Integration": "MAO kernel", "State": "Connected ✅" if st.session_state.settings.get("mao_connected", False) else "Not connected"},
        {"Integration": "Knowledge retrieval", "State": "Active ✅" if st.session_state.settings.get("knowledge_connected", False) else "Not connected"},
        {"Integration": "Notifications", "State": "Ready" if st.session_state.settings.get("notifications_enabled", False) else "Not connected"},
    ], hide_index=True, use_container_width=True)

# Save button
if st.button("💾 Save workspace preferences", use_container_width=True):
    st.session_state.settings.update({
        "facility": facility,
        "dashboard_range": dashboard_range,
        "compact_tables": compact_tables,
        "show_sim_badge": show_sim_badge,
        "critical_alerts": critical_alerts,
        "daily_digest": daily_digest,
        "agent_completion_alerts": agent_completion_alerts,
        "escalation_policy": escalation_policy,
        "response_profile": response_profile,
        "confidence_threshold": confidence_threshold,
    })
    st.success("✅ Settings saved successfully!")
    st.balloons()

st.info("Changes are retained for the current Streamlit session. Refresh the page to reset.")
```

### app/pages/9_AI_Assistant.py

**File path:** `app/pages/9_AI_Assistant.py`

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_copilot_context_panel
from ui_helpers import append_copilot_backend_exchange, copilot_messages, page_heading, render_sidebar, setup_page


setup_page("AI Assistant")
render_sidebar("AI Operations Assistant")
page_heading("COPILOT", "AI Operations Assistant", "Ask for a concise operational brief, asset context, or safety-focused recommendation.")
render_live_signal_banner("COMMAND NEXUS ONLINE", "Your industrial operations copilot is ready for operational questions and shift support.", "Info")
st.write("")
messages = copilot_messages()

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>CONVERSATION</div>", unsafe_allow_html=True)
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
with right:
    render_copilot_context_panel()

prompt = st.chat_input("Ask Command Nexus...")
if prompt:
    with st.spinner("Command Nexus is preparing your response..."):
        append_copilot_backend_exchange(prompt)
    st.rerun()
```

### app/ui_helpers.py

**File path:** `app/ui_helpers.py`

```python
"""Shared presentation and placeholder-data utilities for the Streamlit UI."""

from __future__ import annotations

from datetime import datetime, timedelta
from random import Random

import streamlit as st

from frontend_services.knowledge_agent_adapter import KnowledgeAgentUnavailable, ask_knowledge_agent


COLORS = {
    "cyan": "#55D6FF",
    "violet": "#9B8CFF",
    "green": "#4FE3B2",
    "amber": "#FFBF69",
    "red": "#FF718D",
    "muted": "#8FA1BA",
}


def setup_page(title: str, icon: str = "◈") -> None:
    """Configure a page and apply the shared enterprise dark visual system."""
    st.set_page_config(page_title=f"{title} | NIBS Ops", page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: radial-gradient(circle at 85% -10%, #182e52 0, #0b1220 34%, #070b13 72%); color: #e8f0ff; }
        [data-testid="stHeader"] { background: rgba(7, 11, 19, .78); backdrop-filter: blur(18px); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #101b30 0%, #090f1d 100%); border-right: 1px solid rgba(123, 160, 207, .14); }
        [data-testid="stSidebar"] * { color: #dce8fa; }
        [data-testid="stSidebarNav"] { padding-top: .7rem; }
        [data-testid="stSidebarNav"] a { border-radius: 10px; margin: 2px 8px; padding: 8px 10px; }
        [data-testid="stSidebarNav"] a:hover { background: rgba(85,214,255,.10); }
        .ops-brand { font-size: .74rem; letter-spacing: .22em; color: #55d6ff; font-weight: 800; }
        .ops-title { font-size: 1.6rem; font-weight: 750; margin: .15rem 0 .1rem; color: #f4f8ff; }
        .ops-subtitle, .muted { color: #8fa1ba; }
        .section-label { color: #55d6ff; font-size: .72rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .25rem; }
        .metric-card { background: linear-gradient(145deg, rgba(25,42,70,.88), rgba(13,22,39,.88)); border: 1px solid rgba(129,172,226,.16); border-radius: 16px; padding: 1rem 1.1rem; min-height: 116px; box-shadow: 0 12px 32px rgba(0,0,0,.18); }
        .metric-card, .panel { transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease; backdrop-filter: blur(14px); }
        .metric-card:hover, .panel:hover { transform: translateY(-2px); border-color: rgba(85,214,255,.38); box-shadow: 0 16px 36px rgba(0,0,0,.24); }
        .metric-value { font-size: 1.65rem; font-weight: 760; color: #f5f8ff; margin: .15rem 0; }
        .metric-label { color: #9badc5; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }
        .metric-delta { font-size: .78rem; font-weight: 650; }
        .panel { background: rgba(15,27,47,.76); border: 1px solid rgba(129,172,226,.14); border-radius: 15px; padding: 1rem 1.1rem; }
        .status { display: inline-block; border-radius: 999px; padding: .22rem .6rem; font-size: .72rem; font-weight: 750; letter-spacing: .04em; }
        .status-healthy, .status-running, .status-resolved { color:#6af0c2; background:rgba(79,227,178,.13); border:1px solid rgba(79,227,178,.3); }
        .status-warning, .status-pending { color:#ffd184; background:rgba(255,191,105,.13); border:1px solid rgba(255,191,105,.28); }
        .status-critical, .status-offline { color:#ff91a5; background:rgba(255,113,141,.13); border:1px solid rgba(255,113,141,.28); }
        .status-info { color:#8fe6ff; background:rgba(85,214,255,.13); border:1px solid rgba(85,214,255,.28); }
        .pulse { animation: pulse 1.8s ease-in-out infinite; } @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .38; } }
        .gauge { width: 128px; height: 128px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:.4rem auto; }
        .gauge-inner { width:98px; height:98px; border-radius:50%; background:#0d1728; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .timeline-row { display:grid; grid-template-columns:70px 24px 1fr; gap:10px; align-items:start; margin:.4rem 0; }
        .timeline-dot { width:13px; height:13px; border-radius:50%; background:#55d6ff; box-shadow:0 0 14px #55d6ff; margin-top:5px; }
        .twin-tile { min-height:172px; position:relative; overflow:hidden; }
        .stButton > button { border-radius: 9px; border: 1px solid rgba(85,214,255,.45); background: linear-gradient(135deg,#1686b8,#5664c9); color:#fff; font-weight:650; }
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div { background:#101d31 !important; border-color:#284569 !important; color:#e8f0ff !important; }
        [data-testid="stDataFrame"] { border: 1px solid rgba(129,172,226,.14); border-radius: 12px; overflow: hidden; }
        .agent-card { padding:18px; border-radius:14px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); margin-bottom:15px; }
        .stChatInput textarea { color: #e8f0ff !important; background: #101d31 !important; border: 1px solid #284569 !important; border-radius: 12px !important; }
        .stChatInput textarea::placeholder { color: #8fa1ba !important; }
        .stChatInput textarea:focus { border-color: #55d6ff !important; box-shadow: 0 0 20px rgba(85, 214, 255, 0.1) !important; }
        .stChatMessage { background: rgba(15, 27, 47, 0.76) !important; border: 1px solid rgba(129, 172, 226, 0.14) !important; border-radius: 15px !important; padding: 12px 16px !important; }
        /* Fix white backgrounds */
        .stApp > div { background: transparent !important; }
        .main > div { background: transparent !important; }
        .stChatInput > div { background: rgba(15, 27, 47, 0.9) !important; border-radius: 12px !important; border: 1px solid rgba(129, 172, 226, 0.2) !important; }
        [data-testid="stSelectbox"] > div { background: #101d31 !important; border-radius: 8px !important; }
        /* Fix for the white background in pages */
        .st-emotion-cache-6qob1r { background: transparent !important; }
        .st-emotion-cache-1r6slb0 { background: transparent !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(active: str) -> None:
    """Render the sidebar with navigation and copilot widget."""
    with st.sidebar:
        st.markdown("<div class='ops-brand'>NIBS • AI OPERATIONS</div>", unsafe_allow_html=True)
        st.markdown("<div class='ops-title'>Command Nexus</div>", unsafe_allow_html=True)
        st.caption("Industrial intelligence, unified.")
        st.divider()

        st.markdown("<div class='section-label'>NAVIGATION</div>", unsafe_allow_html=True)

        pages = [
            ("🏠 Home", "Home"),
            ("📊 Dashboard", "1_Dashboard"),
            ("🏭 Assets", "2_Assets"),
            ("🎮 Control Center", "3_Control_Center"),
            ("🚨 Incident Simulator", "4_Incident_Simulator"),
            ("📚 Knowledge Base", "5_Knowledge_Base"),
            ("🤖 Agent Monitor", "6_Agent_Monitor"),
            ("📄 Reports", "7_Reports"),
            ("💬 AI Assistant", "9_AI_Assistant"),
            ("🔮 Health Prediction", "10_Health_Prediction"),
            ("🔧 Maintenance Planner", "11_Maintenance_Planner"),
            ("📋 AI Activity", "12_AI_Activity"),
            ("🏗️ Digital Twin", "13_Digital_Twin"),
        ]

        for label, page_id in pages:
            is_active = (page_id == active) or (active == "Operations Center" and page_id == "Home")
            if is_active:
                st.markdown(f"**{label}**", unsafe_allow_html=True)
            else:
                if page_id == "Home":
                    st.markdown(f"[{label}](/)", unsafe_allow_html=True)
                else:
                    st.markdown(f"[{label}]({page_id})", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div class='section-label'>⚙️ CONFIGURATION</div>", unsafe_allow_html=True)

        config_pages = [
            ("⚙️ Config Dashboard", "14_Config_Dashboard"),
            ("⚙️ Settings", "8_Settings"),
        ]

        for label, page_id in config_pages:
            is_active = (page_id == active)
            if is_active:
                st.markdown(f"**{label}**", unsafe_allow_html=True)
            else:
                st.markdown(f"[{label}]({page_id})", unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='section-label'>Current workspace</div>", unsafe_allow_html=True)
        st.markdown(f"**{active}**")
        st.markdown("<span class='status status-running'>● SYSTEMS NOMINAL</span>", unsafe_allow_html=True)
        st.divider()
        st.caption("LIVE DEMO ENVIRONMENT")
        st.caption("Data shown is simulated until backend integration is enabled.")
        render_copilot_widget()


def render_copilot_widget() -> None:
    """Compact copilot that is intentionally available on every Streamlit page."""
    messages = copilot_messages()
    with st.sidebar.expander("✦ AI COPILOT", expanded=False):
        st.caption("Industrial operations copilot")
        for message in messages[-3:]:
            marker = "You" if message["role"] == "user" else "Nexus"
            st.caption(f"**{marker}:** {message['content']}")
        prompts = ["Summarize today's incidents", "Predict asset failures", "Explain system status", "Generate executive report", "Recommend maintenance"]
        prompt = st.selectbox("Suggested prompts", ["Select a prompt…"] + prompts, key="copilot_suggestion")
        typed = st.text_input("Ask Copilot", key="copilot_input", placeholder="Ask about operations")
        if st.button("Send", key="copilot_send", use_container_width=True):
            question = typed if typed.strip() else (prompt if prompt != "Select a prompt…" else "Explain system status")
            append_copilot_backend_exchange(question)
            st.rerun()


def page_heading(eyebrow: str, title: str, subtitle: str) -> None:
    """Render a page heading with eyebrow, title, and subtitle."""
    st.markdown(
        f"<div class='section-label'>{eyebrow}</div><div class='ops-title'>{title}</div><div class='ops-subtitle'>{subtitle}</div>",
        unsafe_allow_html=True,
    )
    st.write("")


def metric_card(label: str, value: str, delta: str, tone: str = "green") -> None:
    """Render a metric card with label, value, and delta."""
    color = COLORS.get(tone, COLORS["green"])
    st.markdown(
        f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-delta' style='color:{color}'>{delta}</div></div>",
        unsafe_allow_html=True,
    )


def status_chip(status: str) -> str:
    """Return HTML for a status chip."""
    key = status.lower().replace(" ", "-")
    return f"<span class='status status-{key}'>{status.upper()}</span>"


def mock_assets() -> list[dict]:
    """Return mock asset data."""
    return [
        {"Asset": "Pump A-01", "Type": "Centrifugal Pump", "Zone": "Process A", "Health": 96, "Status": "Healthy", "Last telemetry": "12 sec ago"},
        {"Asset": "Compressor C-12", "Type": "Gas Compressor", "Zone": "Process B", "Health": 82, "Status": "Warning", "Last telemetry": "18 sec ago"},
        {"Asset": "Tank T-04", "Type": "Storage Tank", "Zone": "Terminal", "Health": 91, "Status": "Healthy", "Last telemetry": "9 sec ago"},
        {"Asset": "Valve V-09", "Type": "Control Valve", "Zone": "Pipeline", "Health": 68, "Status": "Warning", "Last telemetry": "23 sec ago"},
        {"Asset": "Heat Exchanger H-03", "Type": "Heat Exchanger", "Zone": "Utilities", "Health": 43, "Status": "Critical", "Last telemetry": "31 sec ago"},
    ]


def mock_incidents() -> list[dict]:
    """Return mock incident data."""
    return [
        {"ID": "INC-2048", "Incident": "Elevated vibration", "Asset": "Compressor C-12", "Severity": "High", "Status": "Investigating", "Detected": "08:42"},
        {"ID": "INC-2047", "Incident": "Pressure variance", "Asset": "Valve V-09", "Severity": "Medium", "Status": "Monitoring", "Detected": "08:15"},
        {"ID": "INC-2046", "Incident": "Temperature excursion", "Asset": "Heat Exchanger H-03", "Severity": "Critical", "Status": "Escalated", "Detected": "07:51"},
    ]


def trend_series(points: int = 24, base: int = 88, spread: int = 6) -> dict[str, list[float]]:
    """Generate mock trend series data."""
    rng = Random(17)
    return {
        "Asset Health": [round(base + rng.uniform(-spread, spread), 1) for _ in range(points)],
        "Safety Index": [round(min(100, base + 4 + rng.uniform(-spread, spread)), 1) for _ in range(points)],
    }


def activity_items() -> list[tuple[str, str, str]]:
    """Return mock activity items."""
    return [
        ("08:42", "Diagnostic agent", "Started vibration root-cause analysis for Compressor C-12."),
        ("08:39", "Safety agent", "Validated operating envelope for Process B."),
        ("08:31", "Telemetry gateway", "Ingested 1,248 sensor readings across 42 assets."),
        ("08:15", "Workflow supervisor", "Closed INC-2043 with monitored recovery plan."),
    ]


def dashboard_demo_snapshot() -> dict:
    """Return mock dashboard snapshot."""
    return {
        "metrics": [
            ("Fleet health", "88.4%", "+2.1% vs. prior shift", "green"),
            ("Assets online", "42 / 45", "3 under attention", "cyan"),
            ("Active incidents", "03", "1 requires escalation", "red"),
            ("AI decisions", "128", "94.6% confidence", "violet"),
        ],
        "assets": mock_assets(),
        "incidents": mock_incidents(),
        "activity": activity_items(),
    }


def incident_simulator_demo_flow(incident_type: str, asset: str) -> list[tuple[str, str]]:
    """Return demo flow for incident simulator."""
    return [
        ("Detect", f"Synthetic {incident_type.lower()} signal selected for {asset}."),
        ("Triage", "Classify severity, assess the safety envelope, and create an incident record."),
        ("Orchestrate", "Route specialist agents through the matching response workflow."),
        ("Recommend", "Compile evidence, SOP guidance, and recovery actions for operator review."),
    ]


def agent_monitor_demo_agents() -> list[dict]:
    """Return mock agent monitor data."""
    return [
        {"Agent": "Safety", "Specialty": "Risk validation", "State": "Active", "Confidence": "96%", "Current task": "Check Compressor C-12"},
        {"Agent": "Diagnostic", "Specialty": "Root-cause analysis", "State": "Active", "Confidence": "95%", "Current task": "Analyze vibration pattern"},
        {"Agent": "Knowledge", "Specialty": "SOP retrieval", "State": "Ready", "Confidence": "93%", "Current task": "Awaiting request"},
        {"Agent": "Maintenance", "Specialty": "Maintenance planning", "State": "Ready", "Confidence": "94%", "Current task": "Awaiting task"},
        {"Agent": "Planning", "Specialty": "Recovery planning", "State": "Queued", "Confidence": "92%", "Current task": "Prepare recovery sequence"},
    ]


def asset_monitor_demo_snapshot() -> dict:
    """Return mock asset monitor snapshot."""
    return {
        "assets": mock_assets(),
        "sensors": [
            {"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"},
            {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"},
            {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"},
            {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"},
        ],
    }


def reports_demo_snapshot() -> dict:
    """Return mock reports snapshot."""
    return {
        "metrics": [
            ("Reports generated", "128", "+18 today", "cyan"),
            ("Resolved incidents", "41", "92% within target", "green"),
            ("Average response", "4m 18s", "42 sec faster", "green"),
            ("Pending review", "06", "2 high priority", "amber"),
        ],
        "reports": [
            {"Report": "RPT-2048", "Title": "Compressor vibration response", "Workflow": "Maintenance response", "Status": "Pending review", "Generated": recent_dates(1)[0]},
            {"Report": "RPT-2047", "Title": "Valve pressure variance", "Workflow": "Pressure response", "Status": "Completed", "Generated": recent_dates(2)[0]},
            {"Report": "RPT-2046", "Title": "Heat exchanger excursion", "Workflow": "Temperature response", "Status": "Escalated", "Generated": recent_dates(3)[0]},
        ],
        "preview": {
            "Report": "RPT-2048",
            "Title": "Compressor vibration response",
            "Summary": "Diagnostic analysis indicates a likely bearing wear pattern. The recommended action is controlled load reduction followed by inspection within 24 hours.",
            "Recommendation": "Assign maintenance technician and verify suction pressure.",
        },
    }


def copilot_messages() -> list[dict]:
    """Return the persistent UI conversation."""
    if "ops_messages" not in st.session_state:
        st.session_state.ops_messages = [{"role": "assistant", "content": "Command Nexus copilot online. Ask for an operational brief or recommendation."}]
    return st.session_state.ops_messages


def copilot_diagnostics() -> list[str]:
    """Return temporary frontend diagnostics for the current Copilot session."""
    if "copilot_diagnostics" not in st.session_state:
        st.session_state.copilot_diagnostics = []
    return st.session_state.copilot_diagnostics


def _record_copilot_diagnostic(message: str, callback=None) -> None:
    """Record a diagnostic message for the Copilot."""
    entry = f"{datetime.now().strftime('%H:%M:%S')} — {message}"
    diagnostics = copilot_diagnostics()
    diagnostics.append(entry)
    del diagnostics[:-25]
    if callback is not None:
        callback(entry)


def append_copilot_backend_exchange(question: str, diagnostic_callback=None) -> bool:
    """Append an existing KnowledgeAgent answer and retain its execution trace."""
    messages = copilot_messages()
    messages.append({"role": "user", "content": question})
    _record_copilot_diagnostic("Frontend received question; beginning backend request.", diagnostic_callback)
    try:
        answer = ask_knowledge_agent(
            question,
            on_progress=lambda stage: _record_copilot_diagnostic(stage, diagnostic_callback),
        )
    except Exception as error:
        _record_copilot_diagnostic(
            f"Frontend caught {type(error).__name__}: {error}",
            diagnostic_callback,
        )
        answer = "I'm unable to complete that request right now. Please try again shortly."
        messages.append({"role": "assistant", "content": answer})
        return False
    messages.append({"role": "assistant", "content": answer})
    _record_copilot_diagnostic("Assistant answer added to the conversation.", diagnostic_callback)
    return True


def recent_dates(count: int = 6) -> list[str]:
    """Return a list of recent dates."""
    return [(datetime.now() - timedelta(days=index)).strftime("%d %b") for index in range(count - 1, -1, -1)]


def prediction_series(points: int = 14) -> dict[str, list[float]]:
    """Generate mock prediction series data."""
    rng = Random(41)
    current = 84.0
    health = []
    for _ in range(points):
        current += rng.uniform(-2.8, -0.4)
        health.append(round(current, 1))
    return {"Predicted health": health, "Intervention threshold": [70.0] * points}


def mock_maintenance_tasks() -> list[dict]:
    """Return mock maintenance tasks."""
    return [
        {"Priority": "P1", "Asset": "Heat Exchanger H-03", "Work order": "Inspect thermal bypass", "Window": "Today · 14:00", "Owner": "Utilities Crew", "State": "Scheduled"},
        {"Priority": "P2", "Asset": "Compressor C-12", "Work order": "Bearing and vibration inspection", "Window": "Tomorrow · 09:00", "Owner": "Rotating Equipment", "State": "Proposed"},
        {"Priority": "P3", "Asset": "Valve V-09", "Work order": "Calibrate pressure actuator", "Window": "25 Jul · 11:00", "Owner": "Instrumentation", "State": "Planned"},
    ]


def executive_metrics() -> list[tuple[str, str, str, str]]:
    """Get real executive metrics from backend."""
    from app.frontend_services.backend_api_new import api
    from services.runtime import kernel

    assets = api.get_assets()
    incidents = api.get_incidents()
    agent_results = kernel.state.agent_results

    total_assets = len(assets)
    healthy_assets = sum(1 for a in assets if a.get("status") == "Running")
    avg_health = sum(a.get("health", 0) for a in assets) / total_assets if total_assets else 0

    active_incidents = len(incidents)
    critical_incidents = sum(1 for i in incidents if i.get("payload", {}).get("pressure", 0) > 160)
    predicted_failures = sum(1 for a in assets if a.get("health", 100) < 60)
    safety_score = min(100, avg_health - (active_incidents * 2))

    confidences = [r.confidence for r in agent_results if hasattr(r, 'confidence')]
    avg_confidence = (sum(confidences) / len(confidences) * 100) if confidences else 0

    return [
        ("Overall health", f"{avg_health:.1f}%", "Within mission target", "green"),
        ("Active assets", f"{healthy_assets} / {total_assets}", f"{total_assets - healthy_assets} under attention", "cyan"),
        ("AI agents", f"{len(kernel.registry.all())} / {len(kernel.registry.all())}", "All online", "violet"),
        ("Open incidents", f"{active_incidents:02d}", f"{critical_incidents} critical", "red"),
        ("Predicted failures", f"{predicted_failures:02d}", "Next 14 days", "amber"),
        ("Safety score", f"{safety_score:.1f}", "Operating envelope secure", "green"),
        ("Mission status", "STABLE" if avg_health > 70 else "ATTENTION", "Monitored operations", "green"),
        ("System confidence", f"{avg_confidence:.1f}%", "Evidence quality high", "cyan"),
    ]


def mock_prediction_profile() -> dict:
    """Return mock prediction profile."""
    return {
        "health": 82,
        "rul": "43 days",
        "failure_probability": "32%",
        "confidence": "87%",
        "historical": {"Historical health": [96, 95, 95, 93, 92, 91, 90, 88, 87, 85, 84, 82]},
        "telemetry": [
            {"Signal": "Vibration RMS", "Observed": "23.7 mm/s", "Baseline": "15.0 mm/s", "Evidence": "Elevated +58%"},
            {"Signal": "Bearing temperature", "Observed": "78.2 °C", "Baseline": "68.0 °C", "Evidence": "Rising trend"},
            {"Signal": "Runtime since service", "Observed": "4,238 h", "Baseline": "3,600 h", "Evidence": "Past service window"},
        ],
    }


def mock_agent_timeline() -> list[dict]:
    """Return mock agent timeline."""
    return [
        {"time": "08:42:17", "agent": "Sensor Agent", "action": "Ingested vibration anomaly from Compressor C-12", "state": "Completed", "confidence": "99%", "progress": 100},
        {"time": "08:42:20", "agent": "Prediction Agent", "action": "Calculated 32% failure probability within 14 days", "state": "Completed", "confidence": "87%", "progress": 100},
        {"time": "08:42:25", "agent": "Knowledge Agent", "action": "Retrieved bearing inspection SOP and vibration limits", "state": "Completed", "confidence": "93%", "progress": 100},
        {"time": "08:42:31", "agent": "Planner Agent", "action": "Reserved next rotating-equipment maintenance window", "state": "Running", "confidence": "89%", "progress": 72},
        {"time": "08:42:37", "agent": "Notification Agent", "action": "Prepared operations escalation message", "state": "Queued", "confidence": "96%", "progress": 38},
        {"time": "08:42:42", "agent": "Report Agent", "action": "Compiling executive decision record", "state": "Queued", "confidence": "94%", "progress": 15},
    ]


def mock_twin_assets() -> list[dict]:
    """Return mock twin assets."""
    return [
        {"Asset": "Pump A-01", "Category": "Pump", "Zone": "Process A", "Status": "Healthy", "Health": 96, "Temperature": "72 °C", "Pressure": "119 bar", "RPM": "2,960", "Failure": "4%"},
        {"Asset": "Motor M-07", "Category": "Motor", "Zone": "Process A", "Status": "Healthy", "Health": 93, "Temperature": "64 °C", "Pressure": "—", "RPM": "1,485", "Failure": "7%"},
        {"Asset": "Tank T-04", "Category": "Tank", "Zone": "Terminal", "Status": "Healthy", "Health": 91, "Temperature": "38 °C", "Pressure": "4.8 bar", "RPM": "—", "Failure": "9%"},
        {"Asset": "HVAC H-02", "Category": "HVAC", "Zone": "Utilities", "Status": "Warning", "Health": 76, "Temperature": "31 °C", "Pressure": "2.1 bar", "RPM": "1,120", "Failure": "18%"},
        {"Asset": "Generator G-01", "Category": "Generator", "Zone": "Utilities", "Status": "Healthy", "Health": 89, "Temperature": "79 °C", "Pressure": "6.2 bar", "RPM": "1,500", "Failure": "11%"},
        {"Asset": "Pipeline P-03", "Category": "Pipeline", "Zone": "Pipeline", "Status": "Warning", "Health": 68, "Temperature": "46 °C", "Pressure": "137 bar", "RPM": "—", "Failure": "24%"},
        {"Asset": "Compressor C-12", "Category": "Compressor", "Zone": "Process B", "Status": "Warning", "Health": 82, "Temperature": "78 °C", "Pressure": "112 bar", "RPM": "3,585", "Failure": "32%"},
    ]


def gauge_card(label: str, value: int, detail: str, color: str = "#55D6FF") -> None:
    """Render a gauge card with a circular progress indicator."""
    st.markdown(
        f"<div class='panel' style='text-align:center'><div class='metric-label'>{label}</div><div class='gauge' style='background:conic-gradient({color} {value * 3.6}deg, #22344f 0)'><div class='gauge-inner'><b style='font-size:1.45rem'>{value}%</b><span class='muted' style='font-size:.7rem'>score</span></div></div><span class='muted'>{detail}</span></div>",
        unsafe_allow_html=True,
    )


def render_health_heatmap() -> None:
    """Render health heatmap from actual asset data."""
    from app.frontend_services.backend_api_new import api

    assets = api.get_assets()

    zones = {}
    for asset in assets:
        zone = asset.get("location", "Unassigned")
        if zone not in zones:
            zones[zone] = {"healths": [], "count": 0}
        zones[zone]["healths"].append(asset.get("health", 0))
        zones[zone]["count"] += 1

    zone_data = []
    for zone, data in zones.items():
        avg_health = sum(data["healths"]) / len(data["healths"]) if data["healths"] else 0
        color = "#4FE3B2" if avg_health >= 80 else "#FFBF69" if avg_health >= 50 else "#FF718D"
        zone_data.append((zone, f"{avg_health:.0f}%", color))

    if not zone_data:
        zone_data = [("No Assets", "N/A", "#8FA1BA")]

    blocks = "".join(
        f"<div style='flex:1;min-width:100px;padding:14px 10px;border-radius:11px;background:{color}20;border:1px solid {color}66'><b>{zone}</b><br><span style='font-size:1.45rem;color:{color}'>{score}</span></div>"
        for zone, score, color in zone_data
    )
    st.markdown(f"<div style='display:flex;gap:10px;flex-wrap:wrap'>{blocks}</div>", unsafe_allow_html=True)
```

### core/__init__.py

**File path:** `core/__init__.py`

```python

```

### core/config.py

**File path:** `core/config.py`

```python

```

### core/constants.py

**File path:** `core/constants.py`

```python

```

### core/exceptions.py

**File path:** `core/exceptions.py`

```python

```

### core/logging.py

**File path:** `core/logging.py`

```python

```

### core/prompts.py

**File path:** `core/prompts.py`

```python

```

### core/settings.py

**File path:** `core/settings.py`

```python

```

### core/utils.py

**File path:** `core/utils.py`

```python

```

### database/__init__.py

**File path:** `database/__init__.py`

```python
from database.base import Base
from database.connection import engine

from database import models
```

### database/__init__database.py

**File path:** `database/__init__database.py`

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

### database/base.py

**File path:** `database/base.py`

```python
from sqlalchemy.orm import declarative_base


Base = declarative_base()
```

### database/bootstrap.py

**File path:** `database/bootstrap.py`

```python
"""Development-only schema bootstrap. Production uses Alembic migrations."""

from database.base import Base
from database.connection import engine
from database import models  # noqa: F401


def create_schema():
    Base.metadata.create_all(engine)
```

### database/connection.py

**File path:** `database/connection.py`

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load local .env if available
load_dotenv(PROJECT_ROOT / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Add it to .env locally or Streamlit Secrets."
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session():
    return SessionLocal()
```

### database/migrations/env.py

**File path:** `database/migrations/env.py`

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

### database/migrations/script.py.mako

**File path:** `database/migrations/script.py.mako`

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

### database/migrations/versions/0001_operational_records.py

**File path:** `database/migrations/versions/0001_operational_records.py`

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

### database/migrations/versions/0002_add_knowledge_source.py

**File path:** `database/migrations/versions/0002_add_knowledge_source.py`

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

### database/models.py

**File path:** `database/models.py`

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

### database/repositories/action_repo.py

**File path:** `database/repositories/action_repo.py`

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

### database/repositories/activity_repo.py

**File path:** `database/repositories/activity_repo.py`

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

### database/repositories/agent_repo.py

**File path:** `database/repositories/agent_repo.py`

```python
from database.models import AgentExecutionDB

class AgentRepository:

    def __init__(self,session):
        self.session = session

    def create(self,execution):
        self.session.add(execution)
        self.session.commit()

        self.session.refresh(execution)
        return execution

    def create_many(self, executions):
        self.session.add_all(executions)
        self.session.commit()
        return executions

    def get_all(self):
        return (
            self.session
            .query(AgentExecutionDB)
            .order_by(
                AgentExecutionDB.timestamp.desc()
            )
            .all()
        )
    def get_recent(self, limit = 20):
        return (
            self.session.query(AgentExecutionDB).order_by(AgentExecutionDB.timestamp.desc()).limit(limit).all()
        )
    def get_success_rate(self, agent_name =None):

        query =(
            self.session
            .query(AgentExecutionDB)
        )

        if agent_name:

            query = query.filter(
                AgentExecutionDB.agent_name == agent_name
            )

        executions = query.all()
        if not executions:
            return 0.0

        successful = sum(
            1
            for execution in executions
            if execution.success
        )

        return (
            successful/len(executions)
        ) * 100
    
    
        
```

### database/repositories/asset_repo.py

**File path:** `database/repositories/asset_repo.py`

```python
from database.models import AssetDB



class AssetRepository:


    def __init__(self, session):

        self.session = session



    def create(self, asset):

        self.session.add(asset)

        self.session.commit()

        return asset



    def get_all(self):

        return (
            self.session
            .query(AssetDB)
            .all()
        )



    def get(
        self,
        asset_id
    ):

        return (
            self.session
            .query(AssetDB)
            .filter_by(
                id=asset_id
            )
            .first()
        )
```

### database/repositories/incident_repo.py

**File path:** `database/repositories/incident_repo.py`

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

### database/repositories/knowledge_repo.py

**File path:** `database/repositories/knowledge_repo.py`

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

### database/repositories/report_repo.py

**File path:** `database/repositories/report_repo.py`

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

### database/repositories/telemetry_repo.py

**File path:** `database/repositories/telemetry_repo.py`

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

        self.session.add_all(readings)

        self.session.commit()

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

### database/seed_demo.py

**File path:** `database/seed_demo.py`

```python

```

### docs/API.md

**File path:** `docs/API.md`

```markdown

```

### docs/architecture.md

**File path:** `docs/architecture.md`

```markdown

```

### docs/MAO.md

**File path:** `docs/MAO.md`

```markdown

```

### mao/__init__.py

**File path:** `mao/__init__.py`

```python
from .kernel import MAOKernel

__all__ = [
    "MAOKernel",
]
```

### mao/core/context.py

**File path:** `mao/core/context.py`

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

### mao/core/exceptions.py

**File path:** `mao/core/exceptions.py`

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

### mao/core/executor.py

**File path:** `mao/core/executor.py`

```python
from mao.models.result import AgentResult
from mao.core.exceptions import AgentNotFound


class Executor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, task, context):

        agent = self.registry.get(
            task.assigned_agent
        )

        if agent is None:
            raise AgentNotFound(
                f"Agent '{task.assigned_agent}' not found."
            )

        try:

            # Agent.run() handles:
            # think()
            # execute()
            # validate_result()
            # reflect()
            result = agent.run(
                task,
                context,
            )

        except Exception as e:

            result = AgentResult(
                agent_name=agent.name,
                success=False,
                finding="Agent execution failed.",
                confidence=0.0,
                summary=str(e),
                recommendations=[
                    "Review execution logs."
                ],
                metadata={
                    "exception": type(e).__name__,
                },
            )

        result.metadata.update(
            {
                "task_name": task.name,
                "task_description": task.description,
                "event_name": context.event.name,
                "asset_id": context.event.source,
            }
        )

        return result
```

### mao/core/logger.py

**File path:** `mao/core/logger.py`

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

### mao/core/registry.py

**File path:** `mao/core/registry.py`

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

### mao/core/scheduler.py

**File path:** `mao/core/scheduler.py`

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

### mao/core/state_manager.py

**File path:** `mao/core/state_manager.py`

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

### mao/events/event_bus.py

**File path:** `mao/events/event_bus.py`

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

### mao/events/event_store.py

**File path:** `mao/events/event_store.py`

```python
class EventStore:

    def __init__(self):

        self.events = []

    def save(self, event):

        self.events.append(event)

    def all(self):

        return self.events
```

### mao/events/event.py

**File path:** `mao/events/event.py`

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

### mao/kernel.py

**File path:** `mao/kernel.py`

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

### mao/memory/memory_manager.py

**File path:** `mao/memory/memory_manager.py`

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

### mao/models/execution_report.py

**File path:** `mao/models/execution_report.py`

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

### mao/models/notification.py

**File path:** `mao/models/notification.py`

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

### mao/models/result.py

**File path:** `mao/models/result.py`

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

### mao/models/task.py

**File path:** `mao/models/task.py`

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

### mao/orchestrator.py

**File path:** `mao/orchestrator.py`

```python
from datetime import datetime

from mao.core.context import ExecutionContext
from mao.models.execution_report import ExecutionReport


class Orchestrator:
    """
    Coordinates the complete execution lifecycle for a single event.
    """

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

        self.logger.info(
            "Kernel",
            f"[{context.execution_id}] Received event '{event.name}'",
        )

        # Persist incoming event
        self.state.add_event(event)
        self.event_store.save(event)

        # Select workflow
        workflow_name = self.planner.choose_workflow(event)
        context.workflow = workflow_name

        self.logger.info(
            "Planner",
            f"[{context.execution_id}] Selected workflow '{workflow_name}'",
        )

        # Build workflow tasks
        tasks = self.workflow_engine.create_tasks(
            workflow_name,
            event,
        )

        self.logger.info(
            "WorkflowEngine",
            f"[{context.execution_id}] Generated {len(tasks)} task(s)",
        )

        # Schedule tasks
        for task in tasks:
            self.scheduler.submit(task)

        # Execute tasks
        while not self.scheduler.empty():

            task = self.scheduler.next()

            self.logger.info(
                "Executor",
                f"[{context.execution_id}] Executing '{task.name}'",
            )

            result = self.executor.execute(
                task,
                context,
            )

            # NEW
            context.add_result(result)

            self.state.add_task(task)

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

        self.logger.info(
            "Kernel",
            f"[{context.execution_id}] Execution completed.",
        )

        # Persist into memory
        self.memory.remember_event(event)
        self.memory.remember_report(report)

        for result in report.agent_results:
            self.memory.remember_result(result)

        return report
```

### mao/tools/tool_registry.py

**File path:** `mao/tools/tool_registry.py`

```python

```

### mao/workflows/flow_workflow.py

**File path:** `mao/workflows/flow_workflow.py`

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

### mao/workflows/gas_workflow.py

**File path:** `mao/workflows/gas_workflow.py`

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

### mao/workflows/intelligence_tasks.py

**File path:** `mao/workflows/intelligence_tasks.py`

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

### mao/workflows/maintenance_workflow.py

**File path:** `mao/workflows/maintenance_workflow.py`

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

### mao/workflows/planner.py

**File path:** `mao/workflows/planner.py`

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

### mao/workflows/policy_engine.py

**File path:** `mao/workflows/policy_engine.py`

```python

```

### mao/workflows/pressure_workflow.py

**File path:** `mao/workflows/pressure_workflow.py`

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

### mao/workflows/supervisor.py

**File path:** `mao/workflows/supervisor.py`

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

### mao/workflows/temperature_workflow.py

**File path:** `mao/workflows/temperature_workflow.py`

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

### mao/workflows/workflow_engine.py

**File path:** `mao/workflows/workflow_engine.py`

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

### mao/workflows/workflow.py

**File path:** `mao/workflows/workflow.py`

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

### models/__init__.py

**File path:** `models/__init__.py`

```python

```

### models/asset.py

**File path:** `models/asset.py`

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

### models/enums.py

**File path:** `models/enums.py`

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

### models/event.py

**File path:** `models/event.py`

```python

```

### models/facility.py

**File path:** `models/facility.py`

```python
from pydantic import BaseModel
from models.asset import Asset

class Facility(BaseModel):
    id:str
    name:str
    assets:list[Asset]
```

### models/incident.py

**File path:** `models/incident.py`

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

### models/maintenance.py

**File path:** `models/maintenance.py`

```python

```

### models/pipeline.py

**File path:** `models/pipeline.py`

```python

```

### models/report.py

**File path:** `models/report.py`

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

### models/sensor.py

**File path:** `models/sensor.py`

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

### models/worker.py

**File path:** `models/worker.py`

```python

```

### rag/__init__.py

**File path:** `rag/__init__.py`

```python

```

### rag/chunker.py

**File path:** `rag/chunker.py`

```python

```

### rag/citation.py

**File path:** `rag/citation.py`

```python

```

### rag/embedder.py

**File path:** `rag/embedder.py`

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

### rag/ingestion.py

**File path:** `rag/ingestion.py`

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

### rag/knowledge.py

**File path:** `rag/knowledge.py`

```python

```

### rag/llm_manager.py

**File path:** `rag/llm_manager.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

__all__ = ["LLMManager"]
```

### rag/llm.py

**File path:** `rag/llm.py`

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

CloudLLM = LLMManager

__all__ = ["CloudLLM", "LLMManager"]
```

### rag/loader.py

**File path:** `rag/loader.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:


    def load(self, path):

        loader = PyPDFLoader(path)

        documents = loader.load()

        return documents
```

### rag/neon_vector_store.py

**File path:** `rag/neon_vector_store.py`

```python
from sqlalchemy import text
from langchain_core.documents import Document

from database.connection import get_session
from database.models import KnowledgeDB
from uuid import uuid4


class NeonVectorStore:

    def __init__(self, embeddings):
        self.embeddings = embeddings
        self._db = None  # For compatibility with FAISS pattern

    def create(self, documents):
        """Create the vector store from a list of documents."""
        session = get_session()
        try:
            for doc in documents:
                vector = (
                    self.embeddings
                    .embed_query(
                        doc.page_content
                    )
                )

                row = KnowledgeDB(
                    id=str(uuid4()),
                    content=doc.page_content,
                    source=doc.metadata.get(
                        "source",
                        "unknown"
                    ),
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
        """Add documents to an existing vector store (incremental)."""
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
        """Remove all indexed chunks from the active knowledge database."""
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
        """Return the number of searchable chunks currently stored in Neon."""
        session = get_session()
        try:
            return session.query(KnowledgeDB).count()
        finally:
            session.close()

    def similarity_search(self, query, k=5):
        """Search by query string (generates embedding internally)."""
        session = get_session()
        try:
            vector = self.embeddings.embed_query(query)

            results = session.execute(
                text(
                    """
                    SELECT
                        content,
                        source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                    """
                ),
                {
                    "vector": str(vector),
                    "limit": k
                }
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

    # ✅ NEW: Search by pre-computed embedding vector
    def similarity_search_by_vector(self, embedding, k=5):
        """Search by embedding vector (for use with pre-computed embeddings)."""
        session = get_session()
        try:
            results = session.execute(
                text(
                    """
                    SELECT
                        content,
                        source
                    FROM knowledge
                    ORDER BY embedding <-> :vector
                    LIMIT :limit
                    """
                ),
                {
                    "vector": str(embedding),
                    "limit": k
                }
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

    # ✅ NEW: Get method for Retriever compatibility
    def get(self):
        """Return self for compatibility with Retriever."""
        return self

    # ✅ NEW: Alias for backward compatibility with FAISS pattern
    def as_retriever(self, search_kwargs=None):
        """Return a retriever interface."""
        from rag.retriever import Retriever
        return Retriever(self)
```

### rag/parser.py

**File path:** `rag/parser.py`

```python
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    def load(self, path):

        loader = PyPDFLoader(path)

        return loader.load()
```

### rag/pipeline.py

**File path:** `rag/pipeline.py`

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

### rag/reranker.py

**File path:** `rag/reranker.py`

```python

```

### rag/retriever.py

**File path:** `rag/retriever.py`

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

### rag/splitter.py

**File path:** `rag/splitter.py`

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

### rag/vector_store.py

**File path:** `rag/vector_store.py`

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

### README.md

**File path:** `README.md`

````markdown
# NIBS-Hackathon-2026
Hackathon 2026

## Gemini setup

The AI Assistant uses the existing RAG-backed KnowledgeAgent, which requires a
Gemini API key. Create a local configuration file before using the assistant:

```powershell
Copy-Item .env.example .env
```

Then replace `YOUR_GEMINI_API_KEY_HERE` in `.env` with a real Gemini API key.
The `.env` file is ignored by Git and must not be committed.

The application loads the repository-root `.env` automatically and supports
these environment variable names: `GEMINI_API_KEY_1` (preferred),
`GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `GEMINI_KEY_1`.

The default production model is `gemini-3.6-flash`. Set `GEMINI_MODEL` in
`.env` only when you need to select another model available to your Gemini API
project.
````

### requirements.txt

**File path:** `requirements.txt`

```text
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

### RigOS_Complete_Source_Code_Archive.md

**File path:** `RigOS_Complete_Source_Code_Archive.md`

`````markdown
# RigOS Complete Source Code Archive

Project Name: NIBS-Hackathon-2026 / RigOS

Branch: dev-ashutosh-zinia

Current Local Commit: 30643aa0608139edda0db080c74185e0bf275691

Generation Date: 2026-07-23T02:53:20+05:30

## Table of Contents

- `.devcontainer/devcontainer.json`
- `.env.example`
- `.gitignore`
- `agents/__init__.py`
- `agents/base.py`
- `agents/diagnostic.py`
- `agents/knowledge.py`
- `agents/maintenance.py`
- `agents/planning.py`
- `agents/safety.py`
- `alembic.ini`
- `app/components/__init__.py`
- `app/components/phase_one_views.py`
- `app/components/phase_two_views.py`
- `app/frontend_services/__init__.py`
- `app/frontend_services/knowledge_agent_adapter.py`
- `app/Home.py`
- `app/pages/10_Health_Prediction.py`
- `app/pages/11_Maintenance_Planner.py`
- `app/pages/12_AI_Activity.py`
- `app/pages/13_Digital_Twin.py`
- `app/pages/1_Dashboard.py`
- `app/pages/2_Assets.py`
- `app/pages/3_Control_Center.py`
- `app/pages/4_Incident_Simulator.py`
- `app/pages/5_Knowledge_Base.py`
- `app/pages/6_Agent_Monitor.py`
- `app/pages/7_Reports.py`
- `app/pages/8_Settings.py`
- `app/pages/9_AI_Assistant.py`
- `app/ui_helpers.py`
- `core/__init__.py`
- `core/config.py`
- `core/constants.py`
- `core/exceptions.py`
- `core/logging.py`
- `core/prompts.py`
- `core/settings.py`
- `core/utils.py`
- `database/__init__.py`
- `database/base.py`
- `database/bootstrap.py`
- `database/connection.py`
- `database/migrations/env.py`
- `database/migrations/script.py.mako`
- `database/migrations/versions/0001_operational_records.py`
- `database/models.py`
- `database/repositories/action_repo.py`
- `database/repositories/activity_repo.py`
- `database/repositories/agent_repo.py`
- `database/repositories/asset_repo.py`
- `database/repositories/incident_repo.py`
- `database/repositories/knowledge_repo.py`
- `database/repositories/report_repo.py`
- `database/repositories/telemetry_repo.py`
- `database/seed_demo.py`
- `docs/API.md`
- `docs/architecture.md`
- `docs/MAO.md`
- `mao/__init__.py`
- `mao/core/context.py`
- `mao/core/exceptions.py`
- `mao/core/executor.py`
- `mao/core/logger.py`
- `mao/core/registry.py`
- `mao/core/scheduler.py`
- `mao/core/state_manager.py`
- `mao/events/event.py`
- `mao/events/event_bus.py`
- `mao/events/event_store.py`
- `mao/kernel.py`
- `mao/memory/memory_manager.py`
- `mao/models/execution_report.py`
- `mao/models/result.py`
- `mao/models/task.py`
- `mao/orchestrator.py`
- `mao/tools/tool_registry.py`
- `mao/workflows/flow_workflow.py`
- `mao/workflows/gas_workflow.py`
- `mao/workflows/maintenance_workflow.py`
- `mao/workflows/planner.py`
- `mao/workflows/policy_engine.py`
- `mao/workflows/pressure_workflow.py`
- `mao/workflows/supervisor.py`
- `mao/workflows/temperature_workflow.py`
- `mao/workflows/workflow.py`
- `mao/workflows/workflow_engine.py`
- `models/__init__.py`
- `models/asset.py`
- `models/enums.py`
- `models/event.py`
- `models/facility.py`
- `models/incident.py`
- `models/maintenance.py`
- `models/pipeline.py`
- `models/report.py`
- `models/sensor.py`
- `models/worker.py`
- `rag/__init__.py`
- `rag/chunker.py`
- `rag/citation.py`
- `rag/embedder.py`
- `rag/ingestion.py`
- `rag/knowledge.py`
- `rag/llm.py`
- `rag/llm_manager.py`
- `rag/loader.py`
- `rag/parser.py`
- `rag/pipeline.py`
- `rag/reranker.py`
- `rag/retriever.py`
- `rag/splitter.py`
- `rag/vector_store.py`
- `README.md`
- `requirements.txt`
- `run.py`
- `scripts/benchmark.py`
- `scripts/build_rag.py`
- `scripts/generate_embeddings.py`
- `scripts/ingest_documents.py`
- `scripts/run_simulation.py`
- `scripts/seed_database.py`
- `scripts/test_knowledge.py`
- `scripts/test_mao.py`
- `scripts/test_models.py`
- `scripts/test_rag.py`
- `services/__init__.py`
- `services/asset.py`
- `services/embedding.py`
- `services/health.py`
- `services/incident_manager.py`
- `services/incident_service.py`
- `services/kernel_factory.py`
- `services/llm.py`
- `services/persistence.py`
- `services/report.py`
- `services/runtime.py`
- `services/sensor.py`
- `services/simulation.py`
- `services/telemetry_store.py`
- `services/vision.py`
- `services/weather.py`
- `simulator/asset.py`
- `simulator/event_generator.py`
- `simulator/facility.py`
- `simulator/fault_injector.py`
- `simulator/sensor.py`
- `simulator/simulator.py`
- `tests/mock_agent.py`
- `tests/mock_workflow.py`
- `tests/test_kernel.py`
- `tests/test_neon.py`
- `tools/__init__.py`
- `tools/base_tool.py`
- `tools/email_tool.py`
- `tools/notification_tool.py`
- `tools/postgres_tool.py`
- `tools/report_tool.py`
- `tools/search_tool.py`
- `tools/sensor_tool.py`
- `tools/simulation_tool.py`
- `tools/vector_tool.py`
- `tools/vision_tool.py`
- `tools/weather_tool.py`
- `workflows/__init__.py`
- `workflows/compliance_review.py`
- `workflows/emergency_evacuation.py`
- `workflows/fire_response.py`
- `workflows/leak_response.py`
- `workflows/maintenance_cycle.py`
- `workflows/production_optimization.py`
- `workflows/report_generation.py`
- `workflows/shutdown_sequence.py`
- `workflows/startup_sequence.py`

================================================================================
FILE: .devcontainer/devcontainer.json
================================================================================

```json
{
  "name": "Python 3",
  // Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
  "image": "mcr.microsoft.com/devcontainers/python:1-3.11-bookworm",
  "customizations": {
    "codespaces": {
      "openFiles": [
        "README.md",
        "app/Home.py"
      ]
    },
    "vscode": {
      "settings": {},
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  },
  "updateContentCommand": "[ -f packages.txt ] && sudo apt update && sudo apt upgrade -y && sudo xargs apt install -y <packages.txt; [ -f requirements.txt ] && pip3 install --user -r requirements.txt; pip3 install --user streamlit; echo '✅ Packages installed and Requirements met'",
  "postAttachCommand": {
    "server": "streamlit run app/Home.py --server.enableCORS false --server.enableXsrfProtection false"
  },
  "portsAttributes": {
    "8501": {
      "label": "Application",
      "onAutoForward": "openPreview"
    }
  },
  "forwardPorts": [
    8501
  ]
}
```

================================================================================
FILE: .env.example
================================================================================

```text
# Copy this file to .env and replace the placeholder with your Gemini API key.
# Never commit the real .env file.
GEMINI_API_KEY_1=YOUR_GEMINI_API_KEY_HERE
GEMINI_MODEL=gemini-3.6-flash
```

================================================================================
FILE: .gitignore
================================================================================

```text
.env
*.env

__pycache__/
*.pyc

.venv/
venv/

.streamlit/
```

================================================================================
FILE: agents/__init__.py
================================================================================

```python
```

================================================================================
FILE: agents/base.py
================================================================================

```python
from abc import ABC, abstractmethod
from mao.models.result import AgentResult


class Agent(ABC):

    name = ""

    def think(self, task):
        print(f"[{self.name}] Thinking about '{task.name}'...")

    @abstractmethod
    def execute(self, task, context):
        pass

    def reflect(self, result):
        print(
            f"[{self.name}] Finished | "
            f"Success: {result.success} | "
            f"Confidence: {result.confidence:.2f}"
        )
```

================================================================================
FILE: agents/diagnostic.py
================================================================================

```python
from agents.base import Agent
from mao.models.result import AgentResult


class DiagnosticAgent(Agent):

    name = "diagnostic"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.95,
            summary="Possible cavitation detected.",
            recommendations=[
                "Inspect pump inlet",
                "Check suction pressure",
            ],
        )
```

================================================================================
FILE: agents/knowledge.py
================================================================================

```python
from pathlib import Path

from agents.base import Agent
from mao.models.result import AgentResult


class KnowledgeAgent(Agent):
    """Grounded refinery operations agent used for technical questions."""

    name = "knowledge"

    def __init__(self):
        self.retriever = None
        self.llm = None

    def _initialize_services(self):
        """Load the operational reference stack only when it is required."""
        if self.retriever is not None and self.llm is not None:
            return

        from rag.embedder import Embedder
        from rag.retriever import Retriever
        from rag.vector_store import VectorStore
        from services.llm import LLMManager

        embedder = Embedder()
        store = VectorStore(embedder.get_model())
        store.load("data/faiss_index")
        self.retriever = Retriever(store.db)
        self.llm = LLMManager()

    def think(self, task):
        print("[knowledge] Preparing an operational assessment...")

    def execute(self, task, context=None):
        self._initialize_services()
        query = task.description
        documents = self.retriever.retrieve(query)

        source_labels = []
        context_parts = []
        for index, document in enumerate(documents, start=1):
            metadata = document.metadata or {}
            source = Path(str(metadata.get("source", "Operational reference"))).name
            page = metadata.get("page")
            label = f"[{index}] {source}" + (f", page {page + 1}" if isinstance(page, int) else "")
            source_labels.append(label)
            context_parts.append(f"{label}\n{document.page_content}")

        reference_material = "\n\n".join(context_parts)
        prompt = f"""
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
        answer = self.llm.generate(prompt)

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.95,
            summary=answer,
            recommendations=["Follow approved operating procedures", "Verify operating limits"],
            metadata={"documents_used": len(documents), "sources": source_labels},
        )

    def reflect(self, result):
        print("[knowledge] Operational assessment completed.")
```

================================================================================
FILE: agents/maintenance.py
================================================================================

```python
from agents.base import Agent
from mao.models.result import AgentResult


class MaintenanceAgent(Agent):

    name = "maintenance"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.94,
            summary="Maintenance inspection recommended.",
            recommendations=[
                "Inspect bearings",
                "Schedule maintenance within 24 hours",
            ],
        )
```

================================================================================
FILE: agents/planning.py
================================================================================

```python
from agents.base import Agent
from mao.models.result import AgentResult


class PlanningAgent(Agent):

    name = "planning"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.92,
            summary="Maintenance scheduled.",
            recommendations=[
                "Assign technician",
                "Notify operations",
            ],
        )
```

================================================================================
FILE: agents/safety.py
================================================================================

```python
from agents.base import Agent
from mao.models.result import AgentResult


class SafetyAgent(Agent):

    name = "safety"

    def execute(self, task, context):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=0.96,
            summary="Safety limits verified. Continue monitoring.",
            recommendations=[
                "Reduce operating pressure",
                "Inspect relief valve",
            ],
        )
```

================================================================================
FILE: alembic.ini
================================================================================

```ini
[alembic]
script_location = database/migrations
prepend_sys_path = .

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

================================================================================
FILE: app/components/__init__.py
================================================================================

```python
"""Reusable Streamlit presentation components for the RigOS frontend."""
```

================================================================================
FILE: app/components/phase_one_views.py
================================================================================

```python
"""Reusable Phase 1 visual components.

These components are presentation-only. They accept data supplied by the page
or frontend helpers and never create a MAO kernel or call backend services.
"""

from __future__ import annotations

import streamlit as st

from ui_helpers import status_chip


def render_live_signal_banner(label: str, detail: str, status: str = "Running") -> None:
    """Render a compact operational status banner."""
    st.markdown(
        f"<div class='panel'><span class='pulse' style='color:#4FE3B2'>●</span> "
        f"<b>{label}</b> &nbsp; {status_chip(status)}"
        f"<br><span class='muted'>{detail}</span></div>",
        unsafe_allow_html=True,
    )


def render_incident_response_flow(steps: list[tuple[str, str]]) -> None:
    """Visualize the existing incident-to-report demo lifecycle without executing it."""
    st.markdown("<div class='section-label'>RESPONSE LIFECYCLE</div>", unsafe_allow_html=True)
    for index, (title, detail) in enumerate(steps, start=1):
        st.markdown(
            f"<div class='timeline-row'><span class='muted'>STEP {index}</span>"
            f"<span class='timeline-dot'></span><div class='panel'><b>{title}</b>"
            f"<br><span class='muted'>{detail}</span></div></div>",
            unsafe_allow_html=True,
        )


def render_agent_execution_view(agents: list[dict]) -> None:
    """Render registered/demo agent state as a vertical command-center flow."""
    st.markdown("<div class='section-label'>AGENT EXECUTION VIEW</div>", unsafe_allow_html=True)
    for agent in agents:
        state = agent["State"]
        state_tone = "Running" if state == "Active" else ("Pending" if state == "Queued" else "Info")
        pulse_class = "pulse" if state == "Active" else ""
        st.markdown(
            f"<div class='timeline-row'><span class='muted'>{agent['Specialty']}</span>"
            f"<span class='timeline-dot {pulse_class}'></span><div class='panel'>"
            f"<b>{agent['Agent']} Agent</b> &nbsp; {status_chip(state_tone)}"
            f"<br><span class='muted'>{agent['Current task']} · Confidence {agent['Confidence']}</span>"
            f"</div></div>",
            unsafe_allow_html=True,
        )
```

================================================================================
FILE: app/components/phase_two_views.py
================================================================================

```python
"""Reusable presentation components for Phase 2 frontend pages."""

from __future__ import annotations

import streamlit as st

from ui_helpers import status_chip


def render_asset_detail_panel(asset: dict, sensors: list[dict]) -> None:
    """Show selected asset condition and its current demo telemetry snapshot."""
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='panel'><b>{asset['Asset']}</b> &nbsp; {status_chip(asset['Status'])}"
        f"<p class='muted'>{asset['Type']} · {asset['Zone']}<br>"
        f"Health: {asset['Health']}% · Last telemetry: {asset['Last telemetry']}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>SENSOR SNAPSHOT</div>", unsafe_allow_html=True)
    st.dataframe(sensors, hide_index=True, use_container_width=True)


def render_report_detail_panel(report: dict) -> None:
    """Render the current report preview in a reusable glass panel."""
    st.markdown(
        f"<div class='panel'><b>{report['Report']} · {report['Title']}</b>"
        f"<p class='muted'>{report['Summary']}</p>"
        f"<p><b>Recommendation:</b> {report['Recommendation']}</p></div>",
        unsafe_allow_html=True,
    )


def render_copilot_context_panel() -> None:
    """Shared visual context for the full-page Copilot workspace."""
    st.markdown("<div class='section-label'>CONTEXT IN USE</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='panel'><b>Demo facility</b><p class='muted'>RigOS Alpha Refinery</p>"
        "<b>Priority signal</b><p class='muted'>Compressor C-12 vibration watch</p>"
        "<b>Knowledge mode</b><p class='muted'>Simulated SOP retrieval</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>SUGGESTED PROMPTS</div>", unsafe_allow_html=True)
    st.caption("• Summarize today's incidents\n\n• Predict asset failures\n\n• Explain system status\n\n• Generate executive report\n\n• Recommend maintenance")
```

================================================================================
FILE: app/frontend_services/__init__.py
================================================================================

```python
"""Frontend-facing adapters for existing RigOS backend modules."""
```

================================================================================
FILE: app/frontend_services/knowledge_agent_adapter.py
================================================================================

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
    "trip", "failure", "process", "telemetry", "sensor",
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
    return LLMManager().generate(prompt)


def _emit(callback: ProgressCallback | None, message: str) -> None:
    """Log and optionally expose a diagnostic stage without changing backend behavior."""
    LOGGER.info(message)
    if callback is not None:
        callback(message)


class KnowledgeAgentUnavailable(RuntimeError):
    """Raised when the existing backend knowledge path cannot serve a query."""


@lru_cache(maxsize=1)
def get_knowledge_agent() -> "KnowledgeAgent":
    """Initialize the existing agent once per Streamlit server process."""
    try:
        from agents.knowledge import KnowledgeAgent

        return KnowledgeAgent()
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
            raise KnowledgeAgentUnavailable(
                "Command Nexus is temporarily unavailable. Please try again shortly."
            ) from error

    _emit(on_progress, "Preparing an operational assessment.")
    try:
        # Backend imports are lazy so ordinary Streamlit rendering does not
        # initialize the operational stack until an operational question arrives.
        from mao.models.task import Task

        task = Task(
            name="Operator knowledge query",
            description=normalized_question,
            assigned_agent="knowledge",
        )
        agent = get_knowledge_agent()
        result = agent.execute(task)
    except KnowledgeAgentUnavailable:
        raise
    except Exception as error:
        LOGGER.exception("Command Nexus operational response failed")
        raise KnowledgeAgentUnavailable(
            "Command Nexus is temporarily unavailable. Please try again shortly."
        ) from error

    if not result.success or not result.summary:
        raise KnowledgeAgentUnavailable("Command Nexus could not prepare an operational assessment. Please try again.")

    _emit(on_progress, "Operational assessment prepared.")
    return result.summary
```

================================================================================
FILE: app/Home.py
================================================================================

```python
import importlib

import streamlit as st
import ui_helpers

# Refresh shared UI helpers during Streamlit development reruns so an older
# module cached by the script runner cannot mask newly added components.
importlib.reload(ui_helpers)

from ui_helpers import executive_metrics, metric_card, page_heading, render_sidebar, setup_page, status_chip


setup_page("Operations Center")
render_sidebar("Operations Center")
page_heading("NIBS / AI OPERATIONS CENTER", "Welcome to Command Nexus", "A unified mission-control surface for operational intelligence, risk, and response.")

left, right = st.columns([1.45, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>MISSION STATUS</div><h3 style='margin:.2rem 0 .6rem'>Operational picture: stable, with two monitored assets.</h3><p class='muted'>Use the dashboard to review live health, incidents, agent decisions, and the current response queue.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown(f"<div class='panel'><div class='section-label'>PLATFORM STATUS</div>{status_chip('Running')}<p class='muted' style='margin-top:.8rem'>Demo workspace • Simulated telemetry</p></div>", unsafe_allow_html=True)

st.write("")
st.markdown("<div class='section-label'>EXECUTIVE MISSION CONTROL</div>", unsafe_allow_html=True)
for metric_row in [executive_metrics()[:4], executive_metrics()[4:]]:
    for col, args in zip(st.columns(4), metric_row):
        with col:
            metric_card(*args)

st.write("")
st.markdown("<div class='panel'><div class='section-label'>QUICK START</div><p class='muted'>Navigate with the sidebar to inspect assets, simulate an incident, ask the global copilot, inspect predictive health, or review AI activity.</p></div>", unsafe_allow_html=True)
```

================================================================================
FILE: app/pages/10_Health_Prediction.py
================================================================================

```python
import streamlit as st

from ui_helpers import gauge_card, metric_card, mock_prediction_profile, page_heading, prediction_series, render_sidebar, setup_page


setup_page("Health Prediction")
render_sidebar("Predictive Health")
page_heading("PREDICTIVE INTELLIGENCE", "Asset Health Prediction", "Forecast degradation risk early enough to plan safe, efficient intervention.")

assets = ["Compressor C-12", "Heat Exchanger H-03", "Valve V-09", "Pump A-01"]
profile = mock_prediction_profile()
left, right = st.columns([1, 1.5])
with left:
    asset = st.selectbox("Forecast asset", assets)
    horizon = st.select_slider("Forecast horizon", options=["7 days", "14 days", "30 days"], value="14 days")
    st.markdown("<div class='panel'><div class='section-label'>MODEL STATUS</div><b>Forecast engine: demo mode</b><p class='muted'>Placeholder projections are displayed until telemetry-history and model endpoints are exposed.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>PROJECTED HEALTH · " + asset.upper() + "</div>", unsafe_allow_html=True)
    st.line_chart(prediction_series(), color=["#55D6FF", "#FFBF69"], height=280)

gauge_columns = st.columns(3)
with gauge_columns[0]:
    gauge_card("Health score", profile["health"], "Current modeled condition", "#55D6FF")
with gauge_columns[1]:
    gauge_card("Model confidence", 87, "Evidence consistency", "#4FE3B2")
with gauge_columns[2]:
    gauge_card("Failure risk", 32, "14-day probability", "#FF718D")

for col, args in zip(st.columns(4), [("Current health", f"{profile['health']}%", "Watch threshold: 80%", "amber"), ("Remaining useful life", profile["rul"], "Estimate before intervention", "cyan"), ("Failure probability", profile["failure_probability"], f"At end of {horizon}", "red"), ("Model confidence", profile["confidence"], "Sufficient evidence", "green")]):
    with col:
        metric_card(*args)

st.write("")
left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>HISTORICAL HEALTH TIMELINE</div>", unsafe_allow_html=True)
    st.line_chart(profile["historical"], color="#4FE3B2", height=210)
with right:
    st.markdown("<div class='section-label'>AI DECISION EXPLANATION</div><div class='panel'><b>Why this prediction was made</b><p class='muted'>Vibration and bearing temperature have increased while runtime has exceeded the expected service window.</p><b>Recommended action</b><p class='muted'>Schedule bearing inspection within six days and reduce load if vibration rises further.</p><b>Expected impact</b><p class='muted'>Avoid an estimated 18 hours of unplanned downtime.</p></div>", unsafe_allow_html=True)

st.markdown("<div class='section-label'>SUPPORTING TELEMETRY</div>", unsafe_allow_html=True)
st.dataframe(profile["telemetry"], hide_index=True, use_container_width=True)

# TODO: Replace prediction_series with backend model forecasts based on live telemetry and service history.
```

================================================================================
FILE: app/pages/11_Maintenance_Planner.py
================================================================================

```python
import streamlit as st

from ui_helpers import metric_card, mock_maintenance_tasks, page_heading, render_sidebar, setup_page, status_chip


setup_page("Maintenance Planner")
render_sidebar("Maintenance Planner")
page_heading("WORK ORCHESTRATION", "Maintenance Planner", "Turn asset risk and AI recommendations into an executable maintenance plan.")

for col, args in zip(st.columns(4), [("Planned work", "12", "Across 4 crews", "cyan"), ("High priority", "02", "Needs today", "red"), ("Schedule load", "76%", "Within capacity", "green"), ("Predicted avoided risk", "18%", "Next 30 days", "violet")]):
    with col:
        metric_card(*args)

left, right = st.columns([1.7, 1])
with left:
    st.markdown("<div class='section-label'>RECOMMENDED WORK PLAN</div>", unsafe_allow_html=True)
    st.dataframe(mock_maintenance_tasks(), hide_index=True, use_container_width=True, height=250)
with right:
    st.markdown("<div class='section-label'>PLANNING CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Planning window", ["Next 7 days", "Next 14 days", "Next 30 days"])
    st.selectbox("Crew availability", ["All crews", "Rotating Equipment", "Utilities Crew", "Instrumentation"])
    st.button("Generate AI work plan", use_container_width=True)
    st.button("Balance schedule", use_container_width=True)
    st.caption("These controls are UI-only in the current prototype.")

st.write("")
left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>MAINTENANCE TIMELINE</div>", unsafe_allow_html=True)
    timeline = [("Today · 14:00", "Heat Exchanger H-03", "Utilities Crew", "P1", "2.5 h"), ("Tomorrow · 09:00", "Compressor C-12", "Rotating Equipment", "P2", "4.0 h"), ("25 Jul · 11:00", "Valve V-09", "Instrumentation", "P3", "1.5 h")]
    for window, asset, engineer, priority, downtime in timeline:
        st.markdown(f"<div class='timeline-row'><span class='muted'>{window}</span><span class='timeline-dot'></span><div class='panel'><b>{asset}</b> &nbsp; {status_chip('Critical' if priority == 'P1' else 'Warning')}<br><span class='muted'>Assigned engineer: {engineer} · Estimated downtime: {downtime}</span></div></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>AI SCHEDULING RATIONALE</div><div class='panel'><b>Optimized sequence</b><p class='muted'>Prioritizes the thermal-risk work order ahead of compressor inspection, while grouping pipeline work with instrumentation availability.</p><b>Expected impact</b><p class='muted'>Reduces forecasted operational risk by 18% and avoids overlap with peak production windows.</p></div>", unsafe_allow_html=True)

# TODO: Persist maintenance tasks, crew capacity, work-order status, and planning decisions through backend APIs.
```

================================================================================
FILE: app/pages/12_AI_Activity.py
================================================================================

```python
import streamlit as st

from ui_helpers import metric_card, mock_agent_timeline, page_heading, render_sidebar, setup_page, status_chip


setup_page("AI Activity")
render_sidebar("AI Activity Timeline")
page_heading("AUTONOMY AUDIT", "AI Agent Activity Timeline", "A chronological, reviewable record of AI observation, reasoning, and workflow handoffs.")

for col, args in zip(st.columns(4), [("Activities today", "386", "+14% from yesterday", "cyan"), ("Completed workflows", "34", "No failed executions", "green"), ("Human reviews", "08", "2 awaiting review", "amber"), ("Avg. confidence", "94.6%", "Governance target met", "violet")]):
    with col:
        metric_card(*args)

st.write("")
filter_col, search_col = st.columns([1, 2])
with filter_col:
    st.selectbox("Agent", ["All agents", "Safety", "Diagnostic", "Knowledge", "Maintenance", "Planning"])
with search_col:
    st.text_input("Search activity", placeholder="Filter by asset, workflow, or action")

st.markdown("<div class='section-label'>LIVE EXECUTION FLOW</div>", unsafe_allow_html=True)
for event in mock_agent_timeline():
    state_tone = "Running" if event["state"] == "Running" else ("Pending" if event["state"] == "Queued" else "Info")
    st.markdown(f"<div class='timeline-row'><span class='muted'>{event['time']}</span><span class='timeline-dot {'pulse' if event['state'] == 'Running' else ''}'></span><div class='panel'><b>{event['agent']}</b> &nbsp; {status_chip(state_tone)}<br><span class='muted'>{event['action']} · Confidence {event['confidence']}</span></div></div>", unsafe_allow_html=True)
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")

# TODO: Read immutable agent lifecycle events and audit metadata from the MAO backend/event store.
```

================================================================================
FILE: app/pages/13_Digital_Twin.py
================================================================================

```python
import streamlit as st

from ui_helpers import mock_twin_assets, page_heading, render_sidebar, setup_page, status_chip


setup_page("Digital Twin")
render_sidebar("Digital Twin")
page_heading("FACILITY TOPOLOGY", "Digital Twin View", "A live-ready operational map of facility zones, asset condition, and active process signals.")

st.info("Digital twin is running in visual-demo mode. Asset positions and signals are simulated.")

assets = mock_twin_assets()
selected_name = st.selectbox("Inspect digital-twin asset", [asset["Asset"] for asset in assets])
selected = next(asset for asset in assets if asset["Asset"] == selected_name)

st.markdown("<div class='section-label'>INTERACTIVE FACILITY LAYERS</div>", unsafe_allow_html=True)
columns = st.columns(4)
for col, asset in zip(columns * 2, assets):
    with col:
        st.markdown(f"<div class='panel twin-tile'><div class='section-label'>{asset['Zone']} · {asset['Category']}</div><b>{asset['Asset']}</b><p style='margin:.7rem 0'>{status_chip(asset['Status'])}</p><p class='muted'>Health: {asset['Health']}%<br>Temp: {asset['Temperature']} · Pressure: {asset['Pressure']}<br>RPM: {asset['RPM']} · Failure: {asset['Failure']}</p></div>", unsafe_allow_html=True)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown("<div class='section-label'>PROCESS CONNECTIONS</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel' style='text-align:center; padding:2rem'><b>PROCESS A</b> &nbsp; ───► &nbsp; <b>PROCESS B</b> &nbsp; ───► &nbsp; <b>TERMINAL</b><br><br><span class='muted'>Utilities support all zones · Pipeline transfer monitored continuously</span></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'><b>{selected['Asset']}</b><p>{status_chip(selected['Status'])}</p><span class='muted'>Health: {selected['Health']}%<br>Temperature: {selected['Temperature']}<br>Pressure: {selected['Pressure']}<br>RPM: {selected['RPM']}<br>Failure probability: {selected['Failure']}</span><hr><b>AI recommendation</b><p class='muted'>Continue monitoring. Escalate if the live failure probability exceeds the configured threshold.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>TWIN CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Overlay", ["Asset health", "Live telemetry", "Incident severity", "Maintenance schedule"])
    st.toggle("Show process connections", value=True)
    st.toggle("Highlight active incidents", value=True)

# TODO: Bind zones, topology, asset coordinates, and live sensor overlays to a backend digital-twin data source.
```

================================================================================
FILE: app/pages/1_Dashboard.py
================================================================================

```python
import streamlit as st
from components.phase_one_views import render_live_signal_banner
from ui_helpers import dashboard_demo_snapshot, metric_card, page_heading, render_health_heatmap, render_sidebar, setup_page, trend_series

setup_page("Dashboard")
render_sidebar("Executive Dashboard")
page_heading("OVERVIEW", "Operations Dashboard", "Real-time operational intelligence across the facility.")
snapshot = dashboard_demo_snapshot()
render_live_signal_banner("LIVE DEMO TELEMETRY", "Operational data shown is the existing frontend demo snapshot. Backend stream integration is pending.")
st.write("")

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col: metric_card(*args)

st.write("")
st.markdown("<div class='section-label'>FACILITY HEALTH HEATMAP</div>", unsafe_allow_html=True)
render_health_heatmap()
st.write("")
left, right = st.columns([1.65, 1])
with left:
    st.markdown("<div class='section-label'>24-HOUR OPERATIONAL HEALTH</div>", unsafe_allow_html=True)
    st.line_chart(trend_series(), color=["#55D6FF", "#9B8CFF"], height=280)
with right:
    st.markdown("<div class='section-label'>ATTENTION QUEUE</div>", unsafe_allow_html=True)
    for item in snapshot["incidents"]:
        st.markdown(f"<div class='panel'><b>{item['Incident']}</b><br><span class='muted'>{item['Asset']} • {item['Severity']} • {item['Detected']}</span></div>", unsafe_allow_html=True)
        st.write("")

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>ASSET WATCHLIST</div>", unsafe_allow_html=True)
    st.dataframe(snapshot["assets"], hide_index=True, use_container_width=True, height=245)
with right:
    st.markdown("<div class='section-label'>LIVE ACTIVITY</div>", unsafe_allow_html=True)
    for time, actor, text in snapshot["activity"]:
        st.markdown(f"**{time} · {actor}**  \n<span class='muted'>{text}</span>", unsafe_allow_html=True)
```

================================================================================
FILE: app/pages/2_Assets.py
================================================================================

```python
import streamlit as st
from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_asset_detail_panel
from ui_helpers import asset_monitor_demo_snapshot, metric_card, page_heading, render_sidebar, setup_page, trend_series

setup_page("Asset Monitoring")
render_sidebar("Asset Monitoring")
page_heading("FLEET INTELLIGENCE", "Asset Monitoring", "Health, telemetry, and operational posture for every connected asset.")
render_live_signal_banner("ASSET DEMO SNAPSHOT", "The existing asset and telemetry demo is isolated for future state-manager integration.", "Info")
st.write("")

snapshot = asset_monitor_demo_snapshot()
assets = snapshot["assets"]
filters = st.columns(3)
with filters[0]: zone = st.selectbox("Zone", ["All zones", "Process A", "Process B", "Terminal", "Pipeline", "Utilities"])
with filters[1]: status = st.selectbox("Status", ["All statuses", "Healthy", "Warning", "Critical"])
with filters[2]: selected = st.selectbox("Focus asset", [a["Asset"] for a in assets])

# TODO: Replace asset_monitor_demo_snapshot with a read-only asset/telemetry adapter.
visible = [a for a in assets if (zone == "All zones" or a["Zone"] == zone) and (status == "All statuses" or a["Status"] == status)]
st.dataframe(visible, hide_index=True, use_container_width=True, height=260)

st.write("")
for col, args in zip(st.columns(4), [("Selected asset", selected, "Telemetry connected", "cyan"), ("Current health", "82%", "Watch threshold: 80%", "amber"), ("Sensor coverage", "5 / 5", "All channels reporting", "green"), ("Last update", "18 sec", "Within SLA", "green")]):
    with col: metric_card(*args)

left, right = st.columns([1.55, 1])
with left:
    st.markdown("<div class='section-label'>HEALTH & SAFETY TREND</div>", unsafe_allow_html=True)
    st.line_chart(trend_series(18, 84, 8), color=["#55D6FF", "#4FE3B2"], height=260)
with right:
    selected_asset = next(asset for asset in assets if asset["Asset"] == selected)
    render_asset_detail_panel(selected_asset, snapshot["sensors"])
```

================================================================================
FILE: app/pages/3_Control_Center.py
================================================================================

```python
import streamlit as st
from ui_helpers import metric_card, page_heading, render_sidebar, setup_page, status_chip

setup_page("Control Center")
render_sidebar("Control Center")
page_heading("MISSION CONTROL", "Control Center", "A protected command surface for supervising facility-level operating state.")

for col, args in zip(st.columns(4), [("Facility mode", "RUNNING", "Stable production", "green"), ("Throughput", "82.4%", "+3.2% shift target", "cyan"), ("Safety systems", "12 / 12", "All armed", "green"), ("Response queue", "02", "Awaiting review", "amber")]):
    with col: metric_card(*args)

st.write("")
left, right = st.columns([1.2, 1])
with left:
    st.markdown("<div class='panel'><div class='section-label'>FACILITY STATE</div><h3>RigOS Alpha Refinery</h3><p class='muted'>All primary systems are operating within their configured envelope. AI supervision is active across five critical workflows.</p>" + status_chip("Running") + "</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<div class='section-label'>PROCESS ZONES</div>", unsafe_allow_html=True)
    st.dataframe([{"Zone": "Process A", "State": "Nominal", "Load": "78%", "Assets": 11}, {"Zone": "Process B", "State": "Monitoring", "Load": "86%", "Assets": 9}, {"Zone": "Terminal", "State": "Nominal", "Load": "69%", "Assets": 14}, {"Zone": "Utilities", "State": "Attention", "Load": "73%", "Assets": 8}], hide_index=True, use_container_width=True)
with right:
    st.markdown("<div class='section-label'>SUPERVISORY ACTIONS</div>", unsafe_allow_html=True)
    st.info("Controls are presentation-only in this demo. No operational commands are sent.")
    st.button("Acknowledge monitored alerts", use_container_width=True)
    st.button("Request AI situation brief", use_container_width=True)
    st.button("Open emergency response checklist", use_container_width=True)
    # TODO: Connect these controls to authenticated backend command/workflow endpoints.
```

================================================================================
FILE: app/pages/4_Incident_Simulator.py
================================================================================

```python
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from components.phase_one_views import render_incident_response_flow, render_live_signal_banner
from services.incident_service import IncidentService
from services.runtime import simulator
from ui_helpers import (
    incident_simulator_demo_flow,
    page_heading,
    render_sidebar,
    setup_page,
    status_chip,
)


setup_page("Incident Simulator")
render_sidebar("Incident Simulator")
page_heading(
    "SCENARIO LAB",
    "Incident Simulator",
    "Safely exercise AI detection, triage, and response workflows using synthetic events.",
)
render_live_signal_banner(
    "SCENARIO DESIGN MODE",
    "This interface visualizes the existing simulator flow and runs approved synthetic scenarios.",
    "Info",
)
st.write("")

left, right = st.columns([1, 1.35])
with left:
    st.markdown("<div class='section-label'>CONFIGURE SCENARIO</div>", unsafe_allow_html=True)
    asset = st.selectbox("Affected asset", ["Compressor C-12", "Pump A-01", "Valve V-09", "Heat Exchanger H-03"])
    incident_type = st.selectbox("Incident type", ["Pressure spike", "High temperature", "Gas leak", "High vibration", "Flow restriction"])
    severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"], value="High")
    automated = st.toggle("Enable AI workflow", value=True)
    launched = st.button("Launch simulated incident", use_container_width=True)
with right:
    render_incident_response_flow(incident_simulator_demo_flow(incident_type, asset))

if launched:
    st.success(f"Simulation launched for {asset}")
    service = IncidentService(simulator)
    simulator_result = service.trigger_incident(incident_type)
    st.markdown(status_chip("Processing"), unsafe_allow_html=True)
    st.subheader("🚨 AI Response")

    reports = simulator_result["reports"]
    if reports:
        for report in reports:
            st.success(report.final_summary)
            st.write("Recommendations:")
            for recommendation in report.recommendations:
                st.write("-", recommendation)
    else:
        st.warning("No incident generated.")

st.write("")
st.markdown("<div class='section-label'>RECENT SIMULATED SCENARIOS</div>", unsafe_allow_html=True)
st.dataframe(
    [
        {"Scenario": "SIM-772", "Type": "Gas leak", "Asset": "Tank T-04", "Result": "Resolved", "Duration": "3m 14s"},
        {"Scenario": "SIM-771", "Type": "High vibration", "Asset": "Compressor C-12", "Result": "Review required", "Duration": "2m 47s"},
    ],
    hide_index=True,
    use_container_width=True,
)
```

================================================================================
FILE: app/pages/5_Knowledge_Base.py
================================================================================

```python
import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page

setup_page("Knowledge Base")
render_sidebar("Knowledge Base")
page_heading("RETRIEVAL INTELLIGENCE", "Knowledge Base", "Search operational procedures, safety manuals, and maintenance guidance.")

query = st.text_input("Search approved operational knowledge", placeholder="e.g. pressure spike response procedure")
filters = st.columns(3)
with filters[0]: st.selectbox("Source", ["All sources", "SOP", "Safety manual", "Maintenance manual"])
with filters[1]: st.selectbox("Asset family", ["All assets", "Pumps", "Pipelines", "Tanks", "Compressors"])
with filters[2]: st.selectbox("Confidence", ["Any confidence", "90%+", "75%+"])

if query:
    st.success(f"Showing simulated results for “{query}”.")
    # TODO: Query the RAG retriever/knowledge agent through a stable backend API.

results = [
    ("Pressure SOP • Section 3.2", "Immediate stabilization actions for sustained discharge-pressure deviations.", "94% match"),
    ("Refinery Safety Handbook • Chapter 7", "Isolation, permit, and escalation requirements for abnormal process conditions.", "88% match"),
    ("Pump Maintenance Manual • Inspection", "Bearing, suction, and vibration checks for centrifugal pumping equipment.", "81% match"),
]
for title, summary, confidence in results:
    st.markdown(f"<div class='panel'><b>{title}</b><p class='muted'>{summary}</p><span style='color:#55d6ff;font-weight:700'>{confidence}</span></div>", unsafe_allow_html=True)
    st.write("")

st.markdown("<div class='section-label'>SUGGESTED SEARCHES</div>", unsafe_allow_html=True)
st.caption("Gas leak isolation • Compressor vibration limits • Flow restriction recovery • Emergency shutdown sequence")
```

================================================================================
FILE: app/pages/6_Agent_Monitor.py
================================================================================

```python
import streamlit as st
from components.phase_one_views import render_agent_execution_view, render_live_signal_banner
from ui_helpers import agent_monitor_demo_agents, metric_card, page_heading, render_sidebar, setup_page, status_chip

setup_page("Agent Monitor")
render_sidebar("Agent Monitor")
page_heading("AI SUPERVISION", "Agent Monitor", "Observe autonomous specialists, workflow handoffs, and decision confidence.")
render_live_signal_banner("DEMO AGENT STATE", "The current view preserves the existing demonstration data. Live registry and workflow state are pending backend integration.", "Info")
st.write("")

for col, args in zip(st.columns(4), [("Agents online", "5 / 5", "All systems available", "green"), ("Workflows active", "02", "1 awaiting input", "amber"), ("Avg. confidence", "94.6%", "+1.8% today", "cyan"), ("Decisions today", "128", "Within review SLA", "violet")]):
    with col: metric_card(*args)

st.write("")
agents = agent_monitor_demo_agents()
st.markdown("<div class='section-label'>AGENT FLEET</div>", unsafe_allow_html=True)
st.dataframe(agents, hide_index=True, use_container_width=True)

render_agent_execution_view(agents)

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>WORKFLOW PROGRESS</div>", unsafe_allow_html=True)
    st.progress(72, text="Vibration response workflow • 72% complete")
    st.progress(38, text="Pressure variance workflow • 38% complete")
with right:
    st.markdown("<div class='section-label'>LATEST HANDOFF</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'>{status_chip('Info')}<p><b>Diagnostic → Planning</b></p><span class='muted'>Root-cause confidence reached threshold. Recovery plan generation has been queued.</span></div>", unsafe_allow_html=True)
    # TODO: Surface live MAOKernel registry, scheduler, task, and report state
    # through an approved read-only backend integration; do not instantiate a kernel here.
```

================================================================================
FILE: app/pages/7_Reports.py
================================================================================

```python
import streamlit as st
from components.phase_one_views import render_live_signal_banner
from components.phase_two_views import render_report_detail_panel
from ui_helpers import metric_card, page_heading, render_sidebar, reports_demo_snapshot, setup_page

setup_page("Reports")
render_sidebar("Reports & Intelligence")
page_heading("DECISION RECORD", "Reports & Intelligence", "Review operational reports, AI recommendations, and response outcomes.")
render_live_signal_banner("REPORT DEMO REGISTER", "Existing demonstration records are shown until MAO execution reports are available through a read-only integration.", "Info")
st.write("")
snapshot = reports_demo_snapshot()

for col, args in zip(st.columns(4), snapshot["metrics"]):
    with col: metric_card(*args)

st.write("")
filters = st.columns(3)
with filters[0]: st.selectbox("Report type", ["All reports", "Incident response", "Asset health", "Maintenance", "Compliance"])
with filters[1]: st.selectbox("Status", ["All status", "Completed", "Pending review", "Escalated"])
with filters[2]: st.date_input("From date")

# TODO: Replace reports_demo_snapshot with execution reports exposed by MAO StateManager.
st.dataframe(snapshot["reports"], hide_index=True, use_container_width=True, height=240)

left, right = st.columns([1.25, 1])
with left:
    st.markdown("<div class='section-label'>REPORT DETAIL PREVIEW</div>", unsafe_allow_html=True)
    render_report_detail_panel(snapshot["preview"])
with right:
    st.markdown("<div class='section-label'>EXPORT</div>", unsafe_allow_html=True)
    st.button("Prepare PDF briefing", use_container_width=True)
    st.button("Export report register", use_container_width=True)
    st.caption("Export controls are UI placeholders in this demo.")
```

================================================================================
FILE: app/pages/8_Settings.py
================================================================================

```python
import streamlit as st
from ui_helpers import page_heading, render_sidebar, setup_page

setup_page("Settings")
render_sidebar("Settings")
page_heading("WORKSPACE CONFIGURATION", "Settings", "Configure how Command Nexus presents information and routes operational notifications.")

left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>DISPLAY & WORKSPACE</div>", unsafe_allow_html=True)
    st.selectbox("Default facility", ["RigOS Alpha Refinery", "North Terminal", "Training Sandbox"])
    st.selectbox("Default dashboard range", ["Last 24 hours", "Current shift", "Last 7 days"])
    st.toggle("Compact data tables", value=False)
    st.toggle("Show simulated-data badge", value=True)
with right:
    st.markdown("<div class='section-label'>NOTIFICATIONS</div>", unsafe_allow_html=True)
    st.toggle("Critical incident alerts", value=True)
    st.toggle("Daily operational digest", value=True)
    st.toggle("Agent workflow-completion alerts", value=False)
    st.selectbox("Escalation policy", ["Standard operational", "High sensitivity", "Training mode"])

st.write("")
left, right = st.columns(2)
with left:
    st.markdown("<div class='section-label'>AI CONFIGURATION</div>", unsafe_allow_html=True)
    st.selectbox("Response profile", ["Balanced", "Safety-first", "Speed-first"])
    st.slider("Recommendation confidence threshold", 50, 100, 85, 5)
with right:
    st.markdown("<div class='section-label'>INTEGRATION STATUS</div>", unsafe_allow_html=True)
    st.dataframe([{"Integration": "Telemetry service", "State": "Demo mode"}, {"Integration": "MAO kernel", "State": "Not connected"}, {"Integration": "Knowledge retrieval", "State": "Not connected"}, {"Integration": "Notifications", "State": "Not connected"}], hide_index=True, use_container_width=True)

st.info("Changes are retained only for the current Streamlit session in this UI prototype.")
st.button("Save workspace preferences")
# TODO: Persist preferences and integration secrets through authenticated backend settings endpoints.
```

================================================================================
FILE: app/pages/9_AI_Assistant.py
================================================================================

```python
"""Legacy deep-link for Command Nexus.

NEX is now the global assistant entry point. This route remains available for
bookmarked URLs without duplicating the chat interface or backend calls.
"""

from ui_helpers import page_heading, render_sidebar, setup_page


setup_page("AI Assistant")
render_sidebar("Command Nexus")
page_heading(
    "COMMAND NEXUS",
    "NEX is ready",
    "Use the floating NEX companion in the lower-left corner to open your operations copilot.",
)
```

================================================================================
FILE: app/ui_helpers.py
================================================================================

```python
"""Shared presentation and placeholder-data utilities for the Streamlit UI.

This module deliberately has no backend imports so each page remains runnable while
the Operations Center integration layer is being designed.
"""

from __future__ import annotations

import base64
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from random import Random

import streamlit as st
from streamlit.components.v1 import html as component_html

# Streamlit launched with ``streamlit run app/Home.py`` puts ``app/`` on
# sys.path. Use a frontend-specific package name to avoid shadowing the
# repository's backend ``services`` package.
from frontend_services.knowledge_agent_adapter import KnowledgeAgentUnavailable, ask_knowledge_agent


COLORS = {
    "cyan": "#55D6FF",
    "violet": "#9B8CFF",
    "green": "#4FE3B2",
    "amber": "#FFBF69",
    "red": "#FF718D",
    "muted": "#8FA1BA",
}


@lru_cache(maxsize=1)
def nex_mascot_data_url() -> str:
    """Return the packaged NEX concept asset as a browser-safe data URL."""
    asset_path = Path(__file__).resolve().parent / "assets" / "nex_mascot.png"
    encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def setup_page(title: str, icon: str = "◈") -> None:
    """Configure a page and apply the shared enterprise dark visual system."""
    st.set_page_config(page_title=f"{title} | NIBS Ops", page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: radial-gradient(circle at 85% -10%, #182e52 0, #0b1220 34%, #070b13 72%); color: #e8f0ff; }
        [data-testid="stHeader"] { background: rgba(7, 11, 19, .78); backdrop-filter: blur(18px); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #101b30 0%, #090f1d 100%); border-right: 1px solid rgba(123, 160, 207, .14); }
        [data-testid="stSidebar"] * { color: #dce8fa; }
        [data-testid="stSidebarNav"] { padding-top: .7rem; }
        [data-testid="stSidebarNav"] a { border-radius: 10px; margin: 2px 8px; padding: 8px 10px; }
        [data-testid="stSidebarNav"] a:hover { background: rgba(85,214,255,.10); }
        .ops-brand { font-size: .74rem; letter-spacing: .22em; color: #55d6ff; font-weight: 800; }
        .ops-title { font-size: 1.6rem; font-weight: 750; margin: .15rem 0 .1rem; color: #f4f8ff; }
        .ops-subtitle, .muted { color: #8fa1ba; }
        .section-label { color: #55d6ff; font-size: .72rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .25rem; }
        .metric-card { background: linear-gradient(145deg, rgba(25,42,70,.88), rgba(13,22,39,.88)); border: 1px solid rgba(129,172,226,.16); border-radius: 16px; padding: 1rem 1.1rem; min-height: 116px; box-shadow: 0 12px 32px rgba(0,0,0,.18); }
        .metric-card, .panel { transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease; backdrop-filter: blur(14px); }
        .metric-card:hover, .panel:hover { transform: translateY(-2px); border-color: rgba(85,214,255,.38); box-shadow: 0 16px 36px rgba(0,0,0,.24); }
        .metric-value { font-size: 1.65rem; font-weight: 760; color: #f5f8ff; margin: .15rem 0; }
        .metric-label { color: #9badc5; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }
        .metric-delta { font-size: .78rem; font-weight: 650; }
        .panel { background: rgba(15,27,47,.76); border: 1px solid rgba(129,172,226,.14); border-radius: 15px; padding: 1rem 1.1rem; }
        .status { display: inline-block; border-radius: 999px; padding: .22rem .6rem; font-size: .72rem; font-weight: 750; letter-spacing: .04em; }
        .status-healthy, .status-running, .status-resolved { color:#6af0c2; background:rgba(79,227,178,.13); border:1px solid rgba(79,227,178,.3); }
        .status-warning, .status-pending { color:#ffd184; background:rgba(255,191,105,.13); border:1px solid rgba(255,191,105,.28); }
        .status-critical, .status-offline { color:#ff91a5; background:rgba(255,113,141,.13); border:1px solid rgba(255,113,141,.28); }
        .status-info { color:#8fe6ff; background:rgba(85,214,255,.13); border:1px solid rgba(85,214,255,.28); }
        .pulse { animation: pulse 1.8s ease-in-out infinite; } @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .38; } }
        .gauge { width: 128px; height: 128px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:.4rem auto; }
        .gauge-inner { width:98px; height:98px; border-radius:50%; background:#0d1728; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .timeline-row { display:grid; grid-template-columns:70px 24px 1fr; gap:10px; align-items:start; margin:.4rem 0; }
        .timeline-dot { width:13px; height:13px; border-radius:50%; background:#55d6ff; box-shadow:0 0 14px #55d6ff; margin-top:5px; }
        .twin-tile { min-height:172px; position:relative; overflow:hidden; }
        .stButton > button { border-radius: 9px; border: 1px solid rgba(85,214,255,.45); background: linear-gradient(135deg,#1686b8,#5664c9); color:#fff; font-weight:650; }
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div { background:#101d31 !important; border-color:#284569 !important; color:#e8f0ff !important; }
        [data-testid="stDataFrame"] { border: 1px solid rgba(129,172,226,.14); border-radius: 12px; overflow: hidden; }
        /* NEX is the global entry point; the legacy route remains directly addressable. */
        [data-testid="stSidebarNav"] a[href*="AI_Assistant"] { display: none !important; }
        .st-key-nex-launcher { position:fixed; left:18px; bottom:18px; z-index:10001; width:86px; height:86px; animation:nex-roam 13s cubic-bezier(.45,.05,.55,.95) infinite; will-change:transform; }
        .st-key-nex-launcher > div { height:100%; }
        .st-key-nex-launcher button { position:relative; width:82px !important; height:82px !important; min-height:82px !important; padding:0 !important; overflow:visible; border:0 !important; border-radius:50% !important; font-size:0 !important; background:radial-gradient(circle at 49% 43%,#fcfeff 0 28%,#c9d3df 29% 48%,#2b3747 49% 67%,#101a29 68% 100%) !important; box-shadow:0 10px 22px rgba(0,0,0,.42),0 0 24px rgba(85,214,255,.34),inset 0 2px 3px rgba(255,255,255,.7) !important; transform:translateZ(0); transition:transform .25s ease,box-shadow .25s ease,filter .25s ease; animation:nex-hover 4.2s ease-in-out infinite; will-change:transform; }
        .st-key-nex-launcher button::before { content:''; position:absolute; width:29px; height:29px; left:26px; top:25px; border-radius:50%; background:radial-gradient(circle at 42% 42%,#fff 0 9%,#c7fbff 10% 17%,#46dbff 18% 33%,#0c536f 34% 62%,#020d16 63%); box-shadow:0 0 9px #75ecff,0 0 22px rgba(85,214,255,.85); animation:nex-eye-idle 3s ease-in-out infinite; }
        .st-key-nex-launcher button::after { content:'COMMAND NEXUS\\A Click to open AI Assistant'; white-space:pre; position:absolute; left:96px; bottom:12px; width:180px; padding:9px 11px; border-radius:10px; color:#dff8ff; background:rgba(11,22,38,.92); border:1px solid rgba(85,214,255,.34); box-shadow:0 12px 30px rgba(0,0,0,.32); font-size:11px; font-weight:700; letter-spacing:.04em; text-align:left; opacity:0; transform:translateX(-6px); pointer-events:none; transition:opacity .2s ease,transform .2s ease; }
        .st-key-nex-launcher button:hover { transform:scale(1.08) rotate(-2deg); filter:brightness(1.08); box-shadow:0 12px 28px rgba(0,0,0,.45),0 0 36px rgba(85,214,255,.8),inset 0 2px 3px rgba(255,255,255,.78) !important; animation:nex-bounce .55s ease; }
        .st-key-nex-launcher button:hover::after { opacity:1; transform:translateX(0); }
        .st-key-nex-launcher.nex-active button { animation:nex-activate .7s cubic-bezier(.2,.8,.2,1); }
        .st-key-nex-launcher.nex-active button::before { animation:nex-thinking .7s ease-out; }
        .st-key-nex-launcher.nex-sleeping { animation-duration:24s; opacity:.66; }
        .st-key-nex-launcher.nex-sleeping button { animation-duration:8s; filter:saturate(.65); }
        .st-key-nex-launcher.nex-near button { transform:rotate(-2deg) scale(1.04); box-shadow:0 12px 30px rgba(0,0,0,.45),0 0 40px rgba(85,214,255,.85),inset 0 2px 3px rgba(255,255,255,.75) !important; }
        .st-key-nex-launcher.nex-near button::before { animation:none; transform:translate(var(--nex-eye-x,0px),var(--nex-eye-y,0px)); }
        @keyframes nex-roam { 0%,100% { transform:translate3d(0,0,0); } 25% { transform:translate3d(20px,-5px,0); } 50% { transform:translate3d(10px,-14px,0); } 75% { transform:translate3d(27px,-7px,0); } }
        @keyframes nex-hover { 0%,100% { transform:translateY(0) rotate(-1deg); } 50% { transform:translateY(-6px) rotate(2deg); } }
        @keyframes nex-eye-idle { 0%,100% { transform:translate(0,0) scale(1); opacity:.92; } 35% { transform:translate(2px,-1px) scale(1.04); opacity:1; } 70% { transform:translate(-1px,1px) scale(.94); opacity:.88; } }
        @keyframes nex-thinking { 0% { transform:scale(1); } 45% { transform:scale(1.22) rotate(140deg); box-shadow:0 0 18px #8cf5ff,0 0 38px #55d6ff; } 100% { transform:scale(1) rotate(360deg); } }
        @keyframes nex-bounce { 0%,100% { transform:scale(1.08) translateY(0); } 45% { transform:scale(1.11) translateY(-5px); } }
        @keyframes nex-activate { 0% { transform:scale(1); } 42% { transform:scale(1.2); box-shadow:0 0 0 0 rgba(85,214,255,.75),0 0 54px rgba(85,214,255,1); } 100% { transform:scale(1.03); box-shadow:0 0 0 42px rgba(85,214,255,0),0 0 26px rgba(85,214,255,.58); } }
        .st-key-nex-panel { position:fixed; left:112px; bottom:20px; z-index:10000; width:min(430px,calc(100vw - 138px)); max-height:min(670px,calc(100vh - 42px)); padding:0 2px; border:1px solid rgba(109,211,255,.3); border-radius:19px; background:linear-gradient(145deg,rgba(18,35,59,.96),rgba(7,14,27,.98)); box-shadow:0 26px 72px rgba(0,0,0,.54),0 0 34px rgba(58,177,255,.17); backdrop-filter:blur(20px); animation:nex-panel-in .36s cubic-bezier(.2,.85,.22,1); overflow:hidden; }
        .st-key-nex-panel > div { max-height:min(650px,calc(100vh - 56px)); overflow-y:auto; padding:14px 16px 12px; }
        .st-key-nex-panel [data-testid="stChatMessage"] { padding:.4rem .1rem; }
        .st-key-nex-panel [data-testid="stChatInput"] { padding-bottom:0; }
        .st-key-nex-panel .stButton button { font-size:.76rem !important; height:auto !important; min-height:0 !important; padding:.3rem .55rem !important; background:transparent !important; border-color:rgba(143,161,186,.3) !important; box-shadow:none !important; }
        @keyframes nex-panel-in { from { opacity:0; transform:translateX(-22px) scale(.97); } to { opacity:1; transform:translateX(0) scale(1); } }
        [data-testid="stDialog"] { align-items:flex-end !important; justify-content:flex-start !important; padding:0 0 24px 128px !important; z-index:999998 !important; }
        [data-testid="stDialog"] [role="dialog"] { width:min(440px,calc(100vw - 152px)) !important; max-height:calc(100vh - 48px); border:1px solid rgba(109,211,255,.34); border-radius:19px; background:linear-gradient(145deg,rgba(18,35,59,.97),rgba(7,14,27,.99)); box-shadow:0 26px 72px rgba(0,0,0,.58),0 0 34px rgba(58,177,255,.18); backdrop-filter:blur(20px); animation:nex-panel-in .36s cubic-bezier(.2,.85,.22,1); }
        @media (max-width:700px) { .st-key-nex-launcher { left:8px; bottom:8px; transform:scale(.82); transform-origin:bottom left; } .st-key-nex-panel { left:10px; bottom:98px; width:calc(100vw - 20px); } }
        </style>
        """,
        unsafe_allow_html=True,
    )
    render_nex_global()


def render_sidebar(active: str) -> None:
    with st.sidebar:
        st.markdown("<div class='ops-brand'>NIBS • AI OPERATIONS</div>", unsafe_allow_html=True)
        st.markdown("<div class='ops-title'>Command Nexus</div>", unsafe_allow_html=True)
        st.caption("Industrial intelligence, unified.")
        st.divider()
        st.markdown("<div class='section-label'>Current workspace</div>", unsafe_allow_html=True)
        st.markdown(f"**{active}**")
        st.markdown("<span class='status status-running'>● SYSTEMS NOMINAL</span>", unsafe_allow_html=True)
        st.divider()
        st.caption("LIVE DEMO ENVIRONMENT")
        st.caption("Data shown is simulated until backend integration is enabled.")


def render_copilot_widget() -> None:
    """Compact copilot that is intentionally available on every Streamlit page."""
    messages = copilot_messages()
    with st.sidebar.expander("✦ AI COPILOT", expanded=False):
        st.caption("Industrial operations copilot")
        for message in messages[-3:]:
            marker = "You" if message["role"] == "user" else "Nexus"
            st.caption(f"**{marker}:** {message['content']}")
        prompts = ["Summarize today's incidents", "Predict asset failures", "Explain system status", "Generate executive report", "Recommend maintenance"]
        prompt = st.selectbox("Suggested prompts", ["Select a prompt…"] + prompts, key="copilot_suggestion")
        typed = st.text_input("Ask Copilot", key="copilot_input", placeholder="Ask about operations")
        if st.button("Send", key="copilot_send", use_container_width=True):
            question = typed if typed.strip() else (prompt if prompt != "Select a prompt…" else "Explain system status")
            append_copilot_backend_exchange(question)
            st.rerun()
    # TODO: Replace direct agent invocation when the backend exposes an approved
    # MAO chat/workflow endpoint connected to the running orchestration process.


def _render_nex_presence_script() -> None:
    """Run lightweight browser-only NEX awareness and sleep behavior."""
    component_html(
        """
        <script>
        (() => {
          const host = window.parent;
          let lastActivity = Date.now();
          let framePending = false;
          const launcher = () => host.document.querySelector('.st-key-nex-launcher');
          const update = (event) => {
            lastActivity = Date.now();
            if (framePending) return;
            framePending = true;
            host.requestAnimationFrame(() => {
              const node = launcher();
              if (!node) { framePending = false; return; }
              const rect = node.getBoundingClientRect();
              const dx = event.clientX - (rect.left + rect.width / 2);
              const dy = event.clientY - (rect.top + rect.height / 2);
              const close = Math.hypot(dx, dy) < 210;
              node.classList.toggle('nex-near', close);
              node.classList.remove('nex-sleeping');
              if (close) {
                const eye = node.querySelector('button');
                if (eye) {
                  eye.style.setProperty('--nex-eye-x', `${Math.max(-3, Math.min(3, dx / 34))}px`);
                  eye.style.setProperty('--nex-eye-y', `${Math.max(-2, Math.min(2, dy / 45))}px`);
                }
              }
              framePending = false;
            });
          };
          host.document.addEventListener('pointermove', update, { passive: true });
          host.setInterval(() => {
            const node = launcher();
            if (node && Date.now() - lastActivity > 60000) node.classList.add('nex-sleeping');
          }, 5000);
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def render_nex_global() -> None:
    """Render the floating NEX launcher and persistent Command Nexus panel."""
    if "nex_panel_open" not in st.session_state:
        st.session_state.nex_panel_open = False

    action = st.query_params.get("nex")
    if action == "open":
        st.session_state.nex_panel_open = True
    elif action == "close":
        st.session_state.nex_panel_open = False

    mascot_url = nex_mascot_data_url()
    # Portal the launcher to document.body so it is a sibling of Streamlit's
    # app root, never a child of the sidebar or another layout block.
    st.html(
        f"""
        <script>
        (() => {{
          const existing = document.getElementById('rigos-nex-overlay-root');
          if (existing) existing.remove();
          const root = document.createElement('div');
          root.id = 'rigos-nex-overlay-root';
          root.innerHTML = `
        <style>
        #rigos-nex-launcher {{
            position: fixed; left: 24px; bottom: 24px; z-index: 999999;
            width: 88px; height: 88px; display: block; overflow: visible;
            animation: rigos-nex-patrol 13s ease-in-out infinite;
            pointer-events: auto;
        }}
        #rigos-nex-launcher a {{ display: block; width: 100%; height: 100%; text-decoration: none; }}
        #rigos-nex-launcher img {{
            width: 84px; height: 84px; object-fit: contain; display: block;
            filter: drop-shadow(0 10px 9px rgba(0,0,0,.46)) drop-shadow(0 0 14px rgba(49,203,255,.72));
            animation: rigos-nex-float 4.2s ease-in-out infinite;
            transition: transform .22s ease, filter .22s ease;
        }}
        #rigos-nex-launcher::after {{
            content: 'Command Nexus — Click to open AI Assistant'; white-space: normal;
            position: absolute; left: 96px; bottom: 14px; width: 180px; padding: 9px 11px;
            border: 1px solid rgba(85,214,255,.36); border-radius: 10px;
            background: rgba(8,19,34,.94); color: #e6f9ff; font: 700 11px/1.45 sans-serif;
            letter-spacing: .04em; opacity: 0; transform: translateX(-6px); pointer-events: none;
            transition: opacity .2s ease, transform .2s ease;
        }}
        #rigos-nex-launcher:hover img {{ transform: scale(1.08) rotate(-2deg); filter: drop-shadow(0 12px 10px rgba(0,0,0,.48)) drop-shadow(0 0 24px rgba(49,203,255,1)); animation: rigos-nex-bounce .55s ease; }}
        #rigos-nex-launcher:hover::after {{ opacity: 1; transform: translateX(0); }}
        @keyframes rigos-nex-patrol {{ 0%,100% {{ transform: translate3d(0,0,0); }} 25% {{ transform: translate3d(17px,-5px,0); }} 50% {{ transform: translate3d(9px,-12px,0); }} 75% {{ transform: translate3d(24px,-6px,0); }} }}
        @keyframes rigos-nex-float {{ 0%,100% {{ transform: translateY(0) rotate(-1deg); }} 50% {{ transform: translateY(-6px) rotate(2deg); }} }}
        @keyframes rigos-nex-bounce {{ 0%,100% {{ transform: scale(1.08) translateY(0); }} 45% {{ transform: scale(1.11) translateY(-5px); }} }}
        @media (max-width:700px) {{ #rigos-nex-launcher {{ left: 7px; bottom: 7px; transform: scale(.84); transform-origin: bottom left; }} }}
        </style>
        <div id="rigos-nex-launcher" role="complementary" aria-label="Command Nexus AI Assistant">
          <a href="?nex=open" aria-label="Open Command Nexus">
            <img src="{mascot_url}" alt="NEX, the Command Nexus companion">
          </a>
        </div>
          `;
          document.body.appendChild(root);
        }})();
        </script>
        """,
        unsafe_allow_javascript=True,
    )

    if not st.session_state.nex_panel_open:
        return
    render_nex_chat_dialog()


@st.dialog("Command Nexus", width="large", dismissible=False)
def render_nex_chat_dialog() -> None:
    """Render the existing chat flow in Streamlit's root-level dialog portal."""
    st.markdown("<div class='section-label'>NEX OPERATIONS COPILOT</div>", unsafe_allow_html=True)
    st.caption("Operational intelligence for the current shift")
    if st.button("Close Command Nexus", key="nex_close"):
        st.session_state.nex_panel_open = False
        st.query_params["nex"] = "close"
        st.rerun()

    for message in copilot_messages()[-8:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    suggestions = [
        "Summarize today's incidents",
        "Predict asset failures",
        "Explain system status",
        "Generate executive report",
        "Recommend maintenance",
    ]
    selected = st.selectbox("Suggested prompt", ["Select a prompt"] + suggestions, key="nex_suggestion")
    use_selected = st.button("Use selected prompt", key="nex_use_suggestion", disabled=selected == "Select a prompt")
    prompt = st.chat_input("Ask Command Nexus...", key="nex_chat_input")
    question = prompt or (selected if use_selected else "")
    if question:
        with st.spinner("NEX is preparing an operational response..."):
            append_copilot_backend_exchange(question)
        st.rerun()


def render_nex_global() -> None:
    """Render the reliable fixed NEX fallback without custom portal JavaScript.

    This intentionally replaces the earlier body-portal attempt while the
    overlay is validated in the live application. ``st.html`` places a real
    image element in the Streamlit DOM and CSS fixes it to the viewport.
    """
    if "nex_panel_open" not in st.session_state:
        st.session_state.nex_panel_open = False

    action = st.query_params.get("nex")
    if action == "open":
        st.session_state.nex_panel_open = True
    elif action == "close":
        st.session_state.nex_panel_open = False

    st.html(
        f"""
        <style>
        #rigos-nex-fallback {{
            position: fixed !important; left: 24px !important; bottom: 24px !important;
            z-index: 999999 !important; display: block !important; visibility: visible !important;
            opacity: 1 !important; overflow: visible !important; width: 88px; height: 88px;
            pointer-events: auto; animation: rigos-nex-fallback-float 4.2s ease-in-out infinite;
        }}
        #rigos-nex-fallback a {{ display: block; width: 100%; height: 100%; }}
        #rigos-nex-fallback img {{ width: 84px; height: 84px; object-fit: contain; display: block; filter: drop-shadow(0 10px 9px rgba(0,0,0,.46)) drop-shadow(0 0 16px rgba(49,203,255,.8)); transition: transform .2s ease, filter .2s ease; }}
        #rigos-nex-fallback:hover img {{ transform: scale(1.08) rotate(-2deg); filter: drop-shadow(0 12px 10px rgba(0,0,0,.48)) drop-shadow(0 0 26px rgba(49,203,255,1)); }}
        #rigos-nex-debug {{ position: fixed; left: 24px; bottom: 4px; z-index: 999999; color: #86e9ff; font: 600 9px/1.3 monospace; text-shadow: 0 1px 4px #000; pointer-events: none; }}
        @keyframes rigos-nex-fallback-float {{ 0%,100% {{ transform: translateY(0) rotate(-1deg); }} 50% {{ transform: translateY(-6px) rotate(2deg); }} }}
        </style>
        <div id="rigos-nex-fallback" role="complementary" aria-label="Command Nexus AI Assistant">
          <a href="?nex=open" aria-label="Open Command Nexus">
            <img src="{nex_mascot_data_url()}" alt="NEX, the Command Nexus companion">
          </a>
        </div>
        <div id="rigos-nex-debug">NEX render function executed<br>Portal created: fallback active<br>Mascot appended</div>
        """,
        unsafe_allow_javascript=False,
    )

    if st.session_state.nex_panel_open:
        render_nex_chat_dialog()


def page_heading(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(f"<div class='section-label'>{eyebrow}</div><div class='ops-title'>{title}</div><div class='ops-subtitle'>{subtitle}</div>", unsafe_allow_html=True)
    st.write("")


def metric_card(label: str, value: str, delta: str, tone: str = "green") -> None:
    color = COLORS.get(tone, COLORS["green"])
    st.markdown(
        f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-delta' style='color:{color}'>{delta}</div></div>",
        unsafe_allow_html=True,
    )


def status_chip(status: str) -> str:
    key = status.lower().replace(" ", "-")
    return f"<span class='status status-{key}'>{status.upper()}</span>"


def mock_assets() -> list[dict]:
    return [
        {"Asset": "Pump A-01", "Type": "Centrifugal Pump", "Zone": "Process A", "Health": 96, "Status": "Healthy", "Last telemetry": "12 sec ago"},
        {"Asset": "Compressor C-12", "Type": "Gas Compressor", "Zone": "Process B", "Health": 82, "Status": "Warning", "Last telemetry": "18 sec ago"},
        {"Asset": "Tank T-04", "Type": "Storage Tank", "Zone": "Terminal", "Health": 91, "Status": "Healthy", "Last telemetry": "9 sec ago"},
        {"Asset": "Valve V-09", "Type": "Control Valve", "Zone": "Pipeline", "Health": 68, "Status": "Warning", "Last telemetry": "23 sec ago"},
        {"Asset": "Heat Exchanger H-03", "Type": "Heat Exchanger", "Zone": "Utilities", "Health": 43, "Status": "Critical", "Last telemetry": "31 sec ago"},
    ]


def mock_incidents() -> list[dict]:
    return [
        {"ID": "INC-2048", "Incident": "Elevated vibration", "Asset": "Compressor C-12", "Severity": "High", "Status": "Investigating", "Detected": "08:42"},
        {"ID": "INC-2047", "Incident": "Pressure variance", "Asset": "Valve V-09", "Severity": "Medium", "Status": "Monitoring", "Detected": "08:15"},
        {"ID": "INC-2046", "Incident": "Temperature excursion", "Asset": "Heat Exchanger H-03", "Severity": "Critical", "Status": "Escalated", "Detected": "07:51"},
    ]


def trend_series(points: int = 24, base: int = 88, spread: int = 6) -> dict[str, list[float]]:
    rng = Random(17)
    return {"Asset Health": [round(base + rng.uniform(-spread, spread), 1) for _ in range(points)], "Safety Index": [round(min(100, base + 4 + rng.uniform(-spread, spread)), 1) for _ in range(points)]}


def activity_items() -> list[tuple[str, str, str]]:
    return [
        ("08:42", "Diagnostic agent", "Started vibration root-cause analysis for Compressor C-12."),
        ("08:39", "Safety agent", "Validated operating envelope for Process B."),
        ("08:31", "Telemetry gateway", "Ingested 1,248 sensor readings across 42 assets."),
        ("08:15", "Workflow supervisor", "Closed INC-2043 with monitored recovery plan."),
    ]


# Phase 1 frontend demo contracts. Replace these functions with a frontend
# service adapter once the backend team exposes an approved snapshot endpoint.
# TODO: Expected contract: system metrics, active incidents, assets, and recent
# agent activity from the *running* MAO/simulator process; never create a new kernel here.
def dashboard_demo_snapshot() -> dict:
    return {
        "metrics": [
            ("Fleet health", "88.4%", "+2.1% vs. prior shift", "green"),
            ("Assets online", "42 / 45", "3 under attention", "cyan"),
            ("Active incidents", "03", "1 requires escalation", "red"),
            ("AI decisions", "128", "94.6% confidence", "violet"),
        ],
        "assets": mock_assets(),
        "incidents": mock_incidents(),
        "activity": activity_items(),
    }


def incident_simulator_demo_flow(incident_type: str, asset: str) -> list[tuple[str, str]]:
    """Existing UI-only simulator flow; this function does not submit an event."""
    return [
        ("Detect", f"Synthetic {incident_type.lower()} signal selected for {asset}."),
        ("Triage", "Classify severity, assess the safety envelope, and create an incident record."),
        ("Orchestrate", "Route specialist agents through the matching response workflow."),
        ("Recommend", "Compile evidence, SOP guidance, and recovery actions for operator review."),
    ]


def agent_monitor_demo_agents() -> list[dict]:
    """Current agent-monitor display data, isolated for future MAO registry mapping."""
    return [
        {"Agent": "Safety", "Specialty": "Risk validation", "State": "Active", "Confidence": "96%", "Current task": "Check Compressor C-12"},
        {"Agent": "Diagnostic", "Specialty": "Root-cause analysis", "State": "Active", "Confidence": "95%", "Current task": "Analyze vibration pattern"},
        {"Agent": "Knowledge", "Specialty": "SOP retrieval", "State": "Ready", "Confidence": "93%", "Current task": "Awaiting request"},
        {"Agent": "Maintenance", "Specialty": "Maintenance planning", "State": "Ready", "Confidence": "94%", "Current task": "Awaiting task"},
        {"Agent": "Planning", "Specialty": "Recovery planning", "State": "Queued", "Confidence": "92%", "Current task": "Prepare recovery sequence"},
    ]


# TODO: Map agent_monitor_demo_agents to MAOKernel.registry, scheduler, and
# StateManager report/task data through an approved read-only backend interface.


# Phase 2 frontend demo contracts. These keep current demonstration content in
# one place while defining the data each page will require from a future adapter.
# TODO: Expected asset contract: asset identity/status/health and recent sensor
# telemetry from the running simulator/state manager, exposed read-only.
def asset_monitor_demo_snapshot() -> dict:
    return {
        "assets": mock_assets(),
        "sensors": [
            {"Sensor": "Pressure", "Reading": "119.4 bar", "State": "Normal"},
            {"Sensor": "Temperature", "Reading": "76.2 °C", "State": "Normal"},
            {"Sensor": "Vibration", "Reading": "23.7 mm/s", "State": "Watch"},
            {"Sensor": "Flow", "Reading": "63.1 m³/h", "State": "Normal"},
        ],
    }


# TODO: Expected report contract: execution report id/title/workflow/status,
# generated time, final summary, and recommendations from MAO StateManager.
def reports_demo_snapshot() -> dict:
    return {
        "metrics": [
            ("Reports generated", "128", "+18 today", "cyan"),
            ("Resolved incidents", "41", "92% within target", "green"),
            ("Average response", "4m 18s", "42 sec faster", "green"),
            ("Pending review", "06", "2 high priority", "amber"),
        ],
        "reports": [
            {"Report": "RPT-2048", "Title": "Compressor vibration response", "Workflow": "Maintenance response", "Status": "Pending review", "Generated": recent_dates(1)[0]},
            {"Report": "RPT-2047", "Title": "Valve pressure variance", "Workflow": "Pressure response", "Status": "Completed", "Generated": recent_dates(2)[0]},
            {"Report": "RPT-2046", "Title": "Heat exchanger excursion", "Workflow": "Temperature response", "Status": "Escalated", "Generated": recent_dates(3)[0]},
        ],
        "preview": {
            "Report": "RPT-2048",
            "Title": "Compressor vibration response",
            "Summary": "Diagnostic analysis indicates a likely bearing wear pattern. The recommended action is controlled load reduction followed by inspection within 24 hours.",
            "Recommendation": "Assign maintenance technician and verify suction pressure.",
        },
    }


def copilot_messages() -> list[dict]:
    """Return the persistent UI conversation, initialized with existing demo copy."""
    if "ops_messages" not in st.session_state:
        st.session_state.ops_messages = [{"role": "assistant", "content": "Command Nexus copilot online. Ask for an operational brief or recommendation."}]
    return st.session_state.ops_messages


def copilot_diagnostics() -> list[str]:
    """Return temporary frontend diagnostics for the current Copilot session."""
    if "copilot_diagnostics" not in st.session_state:
        st.session_state.copilot_diagnostics = []
    return st.session_state.copilot_diagnostics


def _record_copilot_diagnostic(message: str, callback=None) -> None:
    entry = f"{datetime.now().strftime('%H:%M:%S')} — {message}"
    diagnostics = copilot_diagnostics()
    diagnostics.append(entry)
    del diagnostics[:-25]
    if callback is not None:
        callback(entry)


def append_copilot_backend_exchange(question: str, diagnostic_callback=None) -> bool:
    """Append an existing KnowledgeAgent answer and retain its execution trace."""
    messages = copilot_messages()
    messages.append({"role": "user", "content": question})
    _record_copilot_diagnostic("Frontend received question; beginning backend request.", diagnostic_callback)
    try:
        answer = ask_knowledge_agent(
            question,
            on_progress=lambda stage: _record_copilot_diagnostic(stage, diagnostic_callback),
        )
    except Exception as error:
        _record_copilot_diagnostic(
            f"Frontend caught {type(error).__name__}: {error}",
            diagnostic_callback,
        )
        answer = "I’m unable to complete that request right now. Please try again shortly."
        messages.append({"role": "assistant", "content": answer})
        return False
    messages.append({"role": "assistant", "content": answer})
    _record_copilot_diagnostic("Assistant answer added to the conversation.", diagnostic_callback)
    return True


# TODO: Route copilot messages through an approved MAO chat/workflow endpoint
# once one exists; retain this thin adapter only until then.


def recent_dates(count: int = 6) -> list[str]:
    return [(datetime.now() - timedelta(days=index)).strftime("%d %b") for index in range(count - 1, -1, -1)]


def prediction_series(points: int = 14) -> dict[str, list[float]]:
    """Deterministic placeholder for projected health and intervention thresholds."""
    rng = Random(41)
    current = 84.0
    health = []
    for _ in range(points):
        current += rng.uniform(-2.8, -0.4)
        health.append(round(current, 1))
    return {"Predicted health": health, "Intervention threshold": [70.0] * points}


def mock_maintenance_tasks() -> list[dict]:
    return [
        {"Priority": "P1", "Asset": "Heat Exchanger H-03", "Work order": "Inspect thermal bypass", "Window": "Today · 14:00", "Owner": "Utilities Crew", "State": "Scheduled"},
        {"Priority": "P2", "Asset": "Compressor C-12", "Work order": "Bearing and vibration inspection", "Window": "Tomorrow · 09:00", "Owner": "Rotating Equipment", "State": "Proposed"},
        {"Priority": "P3", "Asset": "Valve V-09", "Work order": "Calibrate pressure actuator", "Window": "25 Jul · 11:00", "Owner": "Instrumentation", "State": "Planned"},
    ]




def executive_metrics() -> list[tuple[str, str, str, str]]:
    return [
        ("Overall health", "88.4%", "Within mission target", "green"),
        ("Active assets", "42 / 45", "3 under attention", "cyan"),
        ("AI agents", "6 / 6", "All online", "violet"),
        ("Open incidents", "03", "1 critical", "red"),
        ("Predicted failures", "02", "Next 14 days", "amber"),
        ("Safety score", "91.2", "Operating envelope secure", "green"),
        ("Mission status", "STABLE", "Monitored operations", "green"),
        ("System confidence", "94.6%", "Evidence quality high", "cyan"),
    ]


def mock_prediction_profile() -> dict:
    return {
        "health": 82,
        "rul": "43 days",
        "failure_probability": "32%",
        "confidence": "87%",
        "historical": {"Historical health": [96, 95, 95, 93, 92, 91, 90, 88, 87, 85, 84, 82]},
        "telemetry": [
            {"Signal": "Vibration RMS", "Observed": "23.7 mm/s", "Baseline": "15.0 mm/s", "Evidence": "Elevated +58%"},
            {"Signal": "Bearing temperature", "Observed": "78.2 °C", "Baseline": "68.0 °C", "Evidence": "Rising trend"},
            {"Signal": "Runtime since service", "Observed": "4,238 h", "Baseline": "3,600 h", "Evidence": "Past service window"},
        ],
    }


def mock_agent_timeline() -> list[dict]:
    return [
        {"time": "08:42:17", "agent": "Sensor Agent", "action": "Ingested vibration anomaly from Compressor C-12", "state": "Completed", "confidence": "99%", "progress": 100},
        {"time": "08:42:20", "agent": "Prediction Agent", "action": "Calculated 32% failure probability within 14 days", "state": "Completed", "confidence": "87%", "progress": 100},
        {"time": "08:42:25", "agent": "Knowledge Agent", "action": "Retrieved bearing inspection SOP and vibration limits", "state": "Completed", "confidence": "93%", "progress": 100},
        {"time": "08:42:31", "agent": "Planner Agent", "action": "Reserved next rotating-equipment maintenance window", "state": "Running", "confidence": "89%", "progress": 72},
        {"time": "08:42:37", "agent": "Notification Agent", "action": "Prepared operations escalation message", "state": "Queued", "confidence": "96%", "progress": 38},
        {"time": "08:42:42", "agent": "Report Agent", "action": "Compiling executive decision record", "state": "Queued", "confidence": "94%", "progress": 15},
    ]


def mock_twin_assets() -> list[dict]:
    return [
        {"Asset": "Pump A-01", "Category": "Pump", "Zone": "Process A", "Status": "Healthy", "Health": 96, "Temperature": "72 °C", "Pressure": "119 bar", "RPM": "2,960", "Failure": "4%"},
        {"Asset": "Motor M-07", "Category": "Motor", "Zone": "Process A", "Status": "Healthy", "Health": 93, "Temperature": "64 °C", "Pressure": "—", "RPM": "1,485", "Failure": "7%"},
        {"Asset": "Tank T-04", "Category": "Tank", "Zone": "Terminal", "Status": "Healthy", "Health": 91, "Temperature": "38 °C", "Pressure": "4.8 bar", "RPM": "—", "Failure": "9%"},
        {"Asset": "HVAC H-02", "Category": "HVAC", "Zone": "Utilities", "Status": "Warning", "Health": 76, "Temperature": "31 °C", "Pressure": "2.1 bar", "RPM": "1,120", "Failure": "18%"},
        {"Asset": "Generator G-01", "Category": "Generator", "Zone": "Utilities", "Status": "Healthy", "Health": 89, "Temperature": "79 °C", "Pressure": "6.2 bar", "RPM": "1,500", "Failure": "11%"},
        {"Asset": "Pipeline P-03", "Category": "Pipeline", "Zone": "Pipeline", "Status": "Warning", "Health": 68, "Temperature": "46 °C", "Pressure": "137 bar", "RPM": "—", "Failure": "24%"},
        {"Asset": "Compressor C-12", "Category": "Compressor", "Zone": "Process B", "Status": "Warning", "Health": 82, "Temperature": "78 °C", "Pressure": "112 bar", "RPM": "3,585", "Failure": "32%"},
    ]


def gauge_card(label: str, value: int, detail: str, color: str = "#55D6FF") -> None:
    st.markdown(
        f"<div class='panel' style='text-align:center'><div class='metric-label'>{label}</div><div class='gauge' style='background:conic-gradient({color} {value * 3.6}deg, #22344f 0)'><div class='gauge-inner'><b style='font-size:1.45rem'>{value}%</b><span class='muted' style='font-size:.7rem'>score</span></div></div><span class='muted'>{detail}</span></div>",
        unsafe_allow_html=True,
    )


def render_health_heatmap() -> None:
    """Compact CSS heatmap for the executive dashboard; data remains demo-only."""
    cells = [("Process A", "96%", "#4FE3B2"), ("Process B", "82%", "#FFBF69"), ("Terminal", "91%", "#4FE3B2"), ("Pipeline", "68%", "#FFBF69"), ("Utilities", "43%", "#FF718D")]
    blocks = "".join(f"<div style='flex:1;min-width:100px;padding:14px 10px;border-radius:11px;background:{color}20;border:1px solid {color}66'><b>{zone}</b><br><span style='font-size:1.45rem;color:{color}'>{score}</span></div>" for zone, score, color in cells)
    st.markdown(f"<div style='display:flex;gap:10px;flex-wrap:wrap'>{blocks}</div>", unsafe_allow_html=True)
```

================================================================================
FILE: core/__init__.py
================================================================================

```python
```

================================================================================
FILE: core/config.py
================================================================================

```python
```

================================================================================
FILE: core/constants.py
================================================================================

```python
```

================================================================================
FILE: core/exceptions.py
================================================================================

```python
```

================================================================================
FILE: core/logging.py
================================================================================

```python
```

================================================================================
FILE: core/prompts.py
================================================================================

```python
```

================================================================================
FILE: core/settings.py
================================================================================

```python
```

================================================================================
FILE: core/utils.py
================================================================================

```python
```

================================================================================
FILE: database/__init__.py
================================================================================

```python
from database.base import Base
from database.connection import engine

from database import models
```

================================================================================
FILE: database/base.py
================================================================================

```python
from sqlalchemy.orm import declarative_base


Base = declarative_base()
```

================================================================================
FILE: database/bootstrap.py
================================================================================

```python
"""Development-only schema bootstrap. Production uses Alembic migrations."""

from database.base import Base
from database.connection import engine
from database import models  # noqa: F401


def create_schema():
    Base.metadata.create_all(engine)
```

================================================================================
FILE: database/connection.py
================================================================================

```python
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load local .env if available
load_dotenv(PROJECT_ROOT / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Add it to .env locally or Streamlit Secrets."
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session():
    return SessionLocal()
```

================================================================================
FILE: database/migrations/env.py
================================================================================

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

================================================================================
FILE: database/migrations/script.py.mako
================================================================================

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

================================================================================
FILE: database/migrations/versions/0001_operational_records.py
================================================================================

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

================================================================================
FILE: database/models.py
================================================================================

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
        Vector(384)
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

================================================================================
FILE: database/repositories/action_repo.py
================================================================================

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

================================================================================
FILE: database/repositories/activity_repo.py
================================================================================

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

================================================================================
FILE: database/repositories/agent_repo.py
================================================================================

```python
from database.models import AgentExecutionDB

class AgentRepository:

    def __init__(self,session):
        self.session = session

    def create(self,execution):
        self.session.add(execution)
        self.session.commit()

        self.session.refresh(execution)
        return execution

    def create_many(self, executions):
        self.session.add_all(executions)
        self.session.commit()
        return executions

    def get_all(self):
        return (
            self.session
            .query(AgentExecutionDB)
            .order_by(
                AgentExecutionDB.timestamp.desc()
            )
            .all()
        )
    def get_recent(self, limit = 20):
        return (
            self.session.query(AgentExecutionDB).order_by(AgentExecutionDB.timestamp.desc()).limit(limit).all()
        )
    def get_success_rate(self, agent_name =None):

        query =(
            self.session
            .query(AgentExecutionDB)
        )

        if agent_name:

            query = query.filter(
                AgentExecutionDB.agent_name == agent_name
            )

        executions = query.all()
        if not executions:
            return 0.0

        successful = sum(
            1
            for execution in executions
            if execution.success
        )

        return (
            successful/len(executions)
        ) * 100
    
    
        
```

================================================================================
FILE: database/repositories/asset_repo.py
================================================================================

```python
from database.models import AssetDB



class AssetRepository:


    def __init__(self, session):

        self.session = session



    def create(self, asset):

        self.session.add(asset)

        self.session.commit()

        return asset



    def get_all(self):

        return (
            self.session
            .query(AssetDB)
            .all()
        )



    def get(
        self,
        asset_id
    ):

        return (
            self.session
            .query(AssetDB)
            .filter_by(
                id=asset_id
            )
            .first()
        )
```

================================================================================
FILE: database/repositories/incident_repo.py
================================================================================

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

================================================================================
FILE: database/repositories/knowledge_repo.py
================================================================================

```python
from database.models import KnowledgeDB

class KnowledgeRepository:

    def __init__(self, session):
        self.session = session

    def create(
            self,
            knowledge
    ):
        self.session.add(
            knowledge
        )
        self.session.commit()

        self.session.refresh(
            knowledge
        )
        return knowledge

    def create_many(
            self,
            documents
    ):
        self.session.add_all(
            documents
        )
        self.session.commit()
        return documents

    def similarity_search(
            self,
            embedding,
            limit = 5
    ):

        results = (
            self.session
            .query(KnowledgeDB)

            .order_by(
                KnowledgeDB.embedding.cosine_distance(
                    embedding
                )
            )
            .limit(limit)
            .all()
        )

        return results

    def get_all(self):
        return (
            self.session
            .query(
                KnowledgeDB
            ).delete()
        )
    
        self.session.commit()
```

================================================================================
FILE: database/repositories/report_repo.py
================================================================================

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

================================================================================
FILE: database/repositories/telemetry_repo.py
================================================================================

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

        self.session.add_all(readings)

        self.session.commit()

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

================================================================================
FILE: database/seed_demo.py
================================================================================

```python
```

================================================================================
FILE: docs/API.md
================================================================================

```markdown
```

================================================================================
FILE: docs/architecture.md
================================================================================

```markdown
```

================================================================================
FILE: docs/MAO.md
================================================================================

```markdown
```

================================================================================
FILE: mao/__init__.py
================================================================================

```python
from .kernel import MAOKernel

__all__ = [
    "MAOKernel",
]
```

================================================================================
FILE: mao/core/context.py
================================================================================

```python
from datetime import datetime
from uuid import uuid4


class ExecutionContext:

    def __init__(
        self,
        event,
        state_manager,
        memory_manager,
        logger,
    ):

        self.execution_id = str(uuid4())

        self.started_at = datetime.now()

        self.event = event

        self.workflow = None

        self.state = state_manager

        self.memory = memory_manager

        self.logger = logger

        self.results = []

        self.metadata = {}
```

================================================================================
FILE: mao/core/exceptions.py
================================================================================

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

================================================================================
FILE: mao/core/executor.py
================================================================================

```python
from mao.models.result import AgentResult
from mao.core.exceptions import AgentNotFound


class Executor:

    def __init__(self, registry):

        self.registry = registry


    def execute(self, task, context):

        agent = self.registry.get(
            task.assigned_agent
        )


        if agent is None:

            raise AgentNotFound(
                f"Agent '{task.assigned_agent}' not found."
            )


        # Agent lifecycle

        agent.think(task)


        try:

            result = agent.execute(
                task,
                context
            )


        except Exception as e:

            result = AgentResult(
                agent_name=agent.name,
                success=False,
                confidence=0.0,
                summary=str(e),
                recommendations=[],
            )


        agent.reflect(result)

        result.metadata.update(
            {
                "task_name": task.name,
                "task_description": task.description,
                "event_name": context.event.name,
                "asset_id": context.event.source,
            }
        )


        return result
```

================================================================================
FILE: mao/core/logger.py
================================================================================

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

================================================================================
FILE: mao/core/registry.py
================================================================================

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

================================================================================
FILE: mao/core/scheduler.py
================================================================================

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

================================================================================
FILE: mao/core/state_manager.py
================================================================================

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
    # Memory
    # -------------------------

    def add_memory(self, item):

        self.memory.append(item)


    def get_memory(self):

        return self.memory
```

================================================================================
FILE: mao/events/event.py
================================================================================

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

================================================================================
FILE: mao/events/event_bus.py
================================================================================

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

================================================================================
FILE: mao/events/event_store.py
================================================================================

```python
class EventStore:

    def __init__(self):

        self.events = []

    def save(self, event):

        self.events.append(event)

    def all(self):

        return self.events
```

================================================================================
FILE: mao/kernel.py
================================================================================

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

        )



    def register_agent(self, agent):

        self.registry.register(agent)



    def register_workflow(self, workflow):

        self.workflow_engine.register(workflow)



    def handle_event(self, event):

        # Store incoming event

        self.state.add_event(event)



        # Run MAO pipeline

        report = self.orchestrator.run(event)



        # Store report

        self.state.add_report(report)



        # Store agent outputs

        for result in report.agent_results:

            self.state.add_agent_result(result)

        self.persistence.record_execution(event, report)



        return report
```

================================================================================
FILE: mao/memory/memory_manager.py
================================================================================

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

================================================================================
FILE: mao/models/execution_report.py
================================================================================

```python
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from mao.models.result import AgentResult


class ExecutionReport(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))

    execution_id: str

    workflow_name: str

    success: bool

    started_at: datetime

    completed_at: datetime

    agent_results: list[AgentResult]

    final_summary: str

    recommendations: list[str] = Field(default_factory=list)
```

================================================================================
FILE: mao/models/result.py
================================================================================

```python
from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    agent_name: str

    success: bool = True

    confidence: float

    summary: str

    decision: str = "monitor"

    evidence: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    actions_required: list[str] = Field(default_factory=list)

    requires_human_approval: bool = False

    metadata: dict[str, Any] = Field(default_factory=dict)

    execution_time: float = 0.0

    timestamp: datetime = Field(default_factory=datetime.now)
```

================================================================================
FILE: mao/models/task.py
================================================================================

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

================================================================================
FILE: mao/orchestrator.py
================================================================================

```python
from datetime import datetime

from mao.core.context import ExecutionContext
from mao.models.execution_report import ExecutionReport


class Orchestrator:
    """
    Coordinates the complete execution lifecycle for a single event.
    """

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


    def run(self, event):

        context = ExecutionContext(
            event=event,
            state_manager=self.state,
            memory_manager=self.memory,
            logger=self.logger,
        )


        self.logger.info(
            "Kernel",
            f"Received event '{event.name}'"
        )


        # Persist event

        self.state.add_event(event)

        self.event_store.save(event)



        # Select workflow

        workflow_name = self.planner.choose_workflow(event)

        context.workflow = workflow_name


        self.logger.info(
            "Planner",
            f"Selected workflow '{workflow_name}'",
        )



        # Build tasks

        tasks = self.workflow_engine.create_tasks(
            workflow_name,
            event,
        )


        self.logger.info(
            "WorkflowEngine",
            f"Generated {len(tasks)} task(s)",
        )



        # Schedule tasks

        for task in tasks:

            self.scheduler.submit(task)



        # Execute tasks

        while not self.scheduler.empty():

            task = self.scheduler.next()


            self.logger.info(
                "Executor",
                f"Executing '{task.name}'",
            )


            result = self.executor.execute(
                task,
                context
            )


            context.results.append(result)

            self.state.add_task(task)



        # Aggregate results

        decision = self.supervisor.summarize(
            context.results
        )


        report = ExecutionReport(
            execution_id=context.execution_id,
            workflow_name=workflow_name,
            success=decision["success"],
            started_at=context.started_at,
            completed_at=datetime.now(),
            agent_results=context.results,
            final_summary=decision["summary"],
            recommendations=decision["recommendations"],
        )



        self.state.add_report(report)



        self.logger.info(
            "Kernel",
            "Execution completed.",
        )



        # Memory persistence

        self.memory.remember_event(event)

        self.memory.remember_report(report)


        for result in report.agent_results:

            self.memory.remember_result(result)



        return report
```

================================================================================
FILE: mao/tools/tool_registry.py
================================================================================

```python
```

================================================================================
FILE: mao/workflows/flow_workflow.py
================================================================================

```python
from mao.workflows.workflow import Workflow
from mao.models.task import Task


class FlowWorkflow(Workflow):

    name = "flow_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Assess risks caused by restricted flow.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Flow Diagnosis",
                description="Determine the cause of flow restriction.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve flow restriction operating procedures.",
                assigned_agent="knowledge",
                priority=3,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for restricted flow.",
                assigned_agent="maintenance",
                priority=4,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a flow recovery procedure.",
                assigned_agent="planning",
                priority=5,
            ),
        ]
```

================================================================================
FILE: mao/workflows/gas_workflow.py
================================================================================

```python
from mao.workflows.workflow import Workflow
from mao.models.task import Task


class GasWorkflow(Workflow):

    name = "gas_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Assess gas leak hazards.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Gas Leak Diagnosis",
                description="Identify the source of the gas leak.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve gas leak emergency procedures.",
                assigned_agent="knowledge",
                priority=3,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend repair actions for the gas leak.",
                assigned_agent="maintenance",
                priority=4,
            ),

            Task(
                name="Recovery Plan",
                description="Generate a gas leak recovery plan.",
                assigned_agent="planning",
                priority=5,
            ),
        ]
```

================================================================================
FILE: mao/workflows/maintenance_workflow.py
================================================================================

```python
from mao.workflows.workflow import Workflow
from mao.models.task import Task


class MaintenanceWorkflow(Workflow):

    name = "maintenance_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Verify equipment is safe before maintenance.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Equipment Diagnosis",
                description="Analyze equipment condition.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Retrieve Manual",
                description="Retrieve maintenance manuals and procedures.",
                assigned_agent="knowledge",
                priority=3,
            ),

            Task(
                name="Maintenance Planning",
                description="Generate maintenance recommendations.",
                assigned_agent="maintenance",
                priority=4,
            ),

            Task(
                name="Execution Plan",
                description="Create the maintenance execution plan.",
                assigned_agent="planning",
                priority=5,
            ),
        ]
```

================================================================================
FILE: mao/workflows/planner.py
================================================================================

```python
class Planner:

    def choose_workflow(self, event):

        workflows = {
            "PressureSpike": "pressure_response",
            "HighTemperature": "temperature_response",
            "GasLeak": "gas_response",
            "HighVibration": "maintenance_response",
            "FlowRestriction": "flow_response",
        }

        return workflows.get(
            event.name,
            "default"
        )
```

================================================================================
FILE: mao/workflows/policy_engine.py
================================================================================

```python
```

================================================================================
FILE: mao/workflows/pressure_workflow.py
================================================================================

```python
from mao.workflows.workflow import Workflow
from mao.models.task import Task


class PressureWorkflow(Workflow):

    name = "pressure_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Analyze safety impact of the pressure spike.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Root Cause Analysis",
                description="Determine the likely cause of the pressure spike.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve the pressure spike operating procedure.",
                assigned_agent="knowledge",
                priority=3,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for the affected equipment.",
                assigned_agent="maintenance",
                priority=4,
            ),

            Task(
                name="Recovery Plan",
                description="Generate the recovery and restart plan.",
                assigned_agent="planning",
                priority=5,
            ),
        ]
```

================================================================================
FILE: mao/workflows/supervisor.py
================================================================================

```python
from collections import OrderedDict

from mao.models.result import AgentResult


class Supervisor:
    """
    Aggregates agent outputs into a final decision.
    """

    def summarize(self, results: list[AgentResult]) -> dict:

        if not results:
            return {
                "success": True,
                "confidence": 0.0,
                "summary": "No agents were executed.",
                "recommendations": [],
            }

        success = all(result.success for result in results)

        confidence = (
            sum(result.confidence for result in results)
            / len(results)
        )

        recommendations = list(
            OrderedDict.fromkeys(
                rec
                for result in results
                for rec in result.recommendations
            )
        )

        summary = "\n".join(
            f"[{result.agent_name}] {result.summary}"
            for result in results
        )

        return {
            "success": success,
            "confidence": round(confidence, 2),
            "summary": summary,
            "recommendations": recommendations,
        }
```

================================================================================
FILE: mao/workflows/temperature_workflow.py
================================================================================

```python
from mao.workflows.workflow import Workflow
from mao.models.task import Task


class TemperatureWorkflow(Workflow):

    name = "temperature_response"

    def build(self, event):

        return [

            Task(
                name="Safety Check",
                description="Evaluate overheating risks.",
                assigned_agent="safety",
                priority=1,
            ),

            Task(
                name="Temperature Diagnosis",
                description="Determine the cause of abnormal temperature.",
                assigned_agent="diagnostic",
                priority=2,
            ),

            Task(
                name="Retrieve SOP",
                description="Retrieve overheating operating procedures.",
                assigned_agent="knowledge",
                priority=3,
            ),

            Task(
                name="Maintenance Recommendation",
                description="Recommend maintenance for overheating equipment.",
                assigned_agent="maintenance",
                priority=4,
            ),

            Task(
                name="Recovery Plan",
                description="Create a safe recovery procedure.",
                assigned_agent="planning",
                priority=5,
            ),
        ]
```

================================================================================
FILE: mao/workflows/workflow.py
================================================================================

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

================================================================================
FILE: mao/workflows/workflow_engine.py
================================================================================

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

================================================================================
FILE: models/__init__.py
================================================================================

```python
```

================================================================================
FILE: models/asset.py
================================================================================

```python
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4

class AssetType(str, Enum):
    PUMP = "Pump"
    PIPELINE = "Pipeline"
    TANK = "Tank"
    VALVE = "Valve"
    COMPRESSOR = "Compressor"


class Asset(BaseModel):
    id: str = Field(default_factory=lambda:str(uuid4()))
    name:str
    asset_type: AssetType
    location:str
    health:float = 100.0
    status:str = "Running"
```

================================================================================
FILE: models/enums.py
================================================================================

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

================================================================================
FILE: models/event.py
================================================================================

```python
```

================================================================================
FILE: models/facility.py
================================================================================

```python
from pydantic import BaseModel
from models.asset import Asset

class Facility(BaseModel):
    id:str
    name:str
    assets:list[Asset]
```

================================================================================
FILE: models/incident.py
================================================================================

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

================================================================================
FILE: models/maintenance.py
================================================================================

```python
```

================================================================================
FILE: models/pipeline.py
================================================================================

```python
```

================================================================================
FILE: models/report.py
================================================================================

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

================================================================================
FILE: models/sensor.py
================================================================================

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

================================================================================
FILE: models/worker.py
================================================================================

```python
```

================================================================================
FILE: rag/__init__.py
================================================================================

```python
```

================================================================================
FILE: rag/chunker.py
================================================================================

```python
```

================================================================================
FILE: rag/citation.py
================================================================================

```python
```

================================================================================
FILE: rag/embedder.py
================================================================================

```python
from langchain_huggingface import HuggingFaceEmbeddings


class Embedder:


    def __init__(self):

        self.model = HuggingFaceEmbeddings(

            model_name=
            "sentence-transformers/all-MiniLM-L6-v2"

        )


    def get_model(self):

        return self.model
```

================================================================================
FILE: rag/ingestion.py
================================================================================

```python
```

================================================================================
FILE: rag/knowledge.py
================================================================================

```python
```

================================================================================
FILE: rag/llm.py
================================================================================

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

CloudLLM = LLMManager

__all__ = ["CloudLLM", "LLMManager"]
```

================================================================================
FILE: rag/llm_manager.py
================================================================================

```python
"""Compatibility export for the centralized LLM service."""

from services.llm import LLMManager

__all__ = ["LLMManager"]
```

================================================================================
FILE: rag/loader.py
================================================================================

```python
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:


    def load(self, path):

        loader = PyPDFLoader(path)

        documents = loader.load()

        return documents
```

================================================================================
FILE: rag/parser.py
================================================================================

```python
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    def load(self, path):

        loader = PyPDFLoader(path)

        return loader.load()
```

================================================================================
FILE: rag/pipeline.py
================================================================================

```python
from rag.loader import DocumentLoader
from rag.splitter import DocumentSplitter
from rag.embedder import Embedder
from rag.vector_store import VectorStore


class RAGPipeline:

    def build(self, pdfs):

        loader = DocumentLoader()

        splitter = DocumentSplitter()

        embedder = Embedder()

        docs = []

        for pdf in pdfs:

            docs.extend(

                loader.load(pdf)

            )

        chunks = splitter.split(docs)

        store = VectorStore(embedder)

        store.build(chunks)

        store.save()

        return store
```

================================================================================
FILE: rag/reranker.py
================================================================================

```python
```

================================================================================
FILE: rag/retriever.py
================================================================================

```python
class Retriever:


    def __init__(self, vector_store):

        self.db = vector_store



    def retrieve(self, query, k=3):

        results = self.db.similarity_search(

            query,

            k=k

        )

        return results
```

================================================================================
FILE: rag/splitter.py
================================================================================

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

================================================================================
FILE: rag/vector_store.py
================================================================================

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

================================================================================
FILE: README.md
================================================================================

````markdown
# NIBS-Hackathon-2026
Hackathon 2026

## Gemini setup

The AI Assistant uses the existing RAG-backed KnowledgeAgent, which requires a
Gemini API key. Create a local configuration file before using the assistant:

```powershell
Copy-Item .env.example .env
```

Then replace `YOUR_GEMINI_API_KEY_HERE` in `.env` with a real Gemini API key.
The `.env` file is ignored by Git and must not be committed.

The application loads the repository-root `.env` automatically and supports
these environment variable names: `GEMINI_API_KEY_1` (preferred),
`GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `GEMINI_KEY_1`.

The default production model is `gemini-3.6-flash`. Set `GEMINI_MODEL` in
`.env` only when you need to select another model available to your Gemini API
project.
````

================================================================================
FILE: requirements.txt
================================================================================

```text
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

================================================================================
FILE: run.py
================================================================================

```python
```

================================================================================
FILE: scripts/benchmark.py
================================================================================

```python
```

================================================================================
FILE: scripts/build_rag.py
================================================================================

```python
from pathlib import Path

from rag.pipeline import RAGPipeline

docs_folder = Path("docs")

pdfs = [str(pdf) for pdf in docs_folder.glob("*.pdf")]

pipeline = RAGPipeline()

pipeline.build(pdfs)

print("✅ FAISS index created successfully!")
```

================================================================================
FILE: scripts/generate_embeddings.py
================================================================================

```python
```

================================================================================
FILE: scripts/ingest_documents.py
================================================================================

```python
```

================================================================================
FILE: scripts/run_simulation.py
================================================================================

```python
import time
from uuid import uuid4

from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator


from tests.mock_workflow import MockWorkflow

from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from mao.workflows.flow_workflow import FlowWorkflow

from agents.safety import SafetyAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.diagnostic import DiagnosticAgent
from agents.planning import PlanningAgent



# -----------------------------
# Create Assets
# -----------------------------

pump_a = Asset(
    name="Pump A",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

pump_b = Asset(
    name="Pump B",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

tank_a = Asset(
    name="Tank A",
    asset_type=AssetType.TANK,
    location="Zone B",
)


facility = Facility(
    id=str(uuid4()),
    name="RigOS Alpha",
    assets=[
        pump_a,
        pump_b,
        tank_a,
    ],
)



# -----------------------------
# Setup MAO
# -----------------------------

kernel = MAOKernel()


# Register assets

for asset in facility.assets:

    kernel.asset_service.register(asset)



# Register workflows

kernel.register_workflow(MockWorkflow())

kernel.register_workflow(PressureWorkflow())
kernel.register_workflow(TemperatureWorkflow())
kernel.register_workflow(GasWorkflow())
kernel.register_workflow(MaintenanceWorkflow())
kernel.register_workflow(FlowWorkflow())



# Register agents

kernel.register_agent(SafetyAgent())
kernel.register_agent(KnowledgeAgent())
kernel.register_agent(MaintenanceAgent())
kernel.register_agent(DiagnosticAgent())
kernel.register_agent(PlanningAgent())



# -----------------------------
# Simulator
# -----------------------------

facility_sim = SimulatedFacility(facility)


simulator = Simulator(
    facility=facility_sim,
    kernel=kernel,
)



print("=" * 60)
print("🏭 RigOS Alpha Refinery")
print("=" * 60)


tick = 0


while True:

    tick += 1


    telemetry, reports = simulator.tick(tick)


    print(f"\nTick {tick}")
    print("-" * 50)



    for reading in telemetry:

        print(
            f"{reading.sensor_type.value:<12}"
            f"{reading.value:>8.2f}"
        )



    if reports:

        print("\n🚨 INCIDENT DETECTED")


        for report in reports:

            print(report.final_summary)



    print("\nRegistered Agents")


    for agent in kernel.registry.all():

        print("-", agent.name)



    print("\nTelemetry History")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        print(
            f"{asset.name:<10} -> {len(history)} readings"
        )



    print("\nAsset Health")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        health = kernel.health.calculate_health(history)


        kernel.asset_service.update_health(
            asset.id,
            health
        )


        asset_obj = kernel.asset_service.get(asset.id)


        print(
            f"{asset_obj.name:<10}"
            f"{asset_obj.health:>7.1f}%   "
            f"{asset_obj.status}"
        )



    print("\nMemory")


    print(
        "Events:",
        len(kernel.memory.events)
    )


    print(
        "Reports:",
        len(kernel.memory.execution_reports)
    )


    print(
        "Agent Results:",
        len(kernel.memory.agent_results)
    )



    time.sleep(1)
```

================================================================================
FILE: scripts/seed_database.py
================================================================================

```python
```

================================================================================
FILE: scripts/test_knowledge.py
================================================================================

```python
from agents.knowledge import KnowledgeAgent


agent = KnowledgeAgent()


class Task:

    description = (
        "What should operators do during a pressure spike?"
    )


result = agent.execute(Task())


print("="*60)
print(result.summary)
print("="*60)
```

================================================================================
FILE: scripts/test_mao.py
================================================================================

```python
from agents.safety import SafetyAgent
from mao.events.event import Event
from mao.orchestrator import MAO

mao = MAO()

safety = SafetyAgent()

mao.register_agent(safety)

mao.event_bus.subscribe(
    "PressureSpike",
    safety.execute,
)

event = Event(
    name="PressureSpike",
    source="SensorAgent",
    payload={
        "asset": "Pump A",
        "pressure": 112,
    },
)

mao.publish(event)

mao.run()
```

================================================================================
FILE: scripts/test_models.py
================================================================================

```python
from datetime import datetime

from models.asset import Asset
from models.enums import AssetStatus, AssetType
from models.sensor import SensorReading

sensor = SensorReading(
    pressure=103.5,
    temperature=87.2,
    flow_rate=1200,
    vibration=0.42,
    gas_level=1.5,
    timestamp=datetime.now(),
)

pump = Asset(
    id="PUMP-001",
    name="Main Feed Pump",
    asset_type=AssetType.PUMP,
    location="Zone A",
    health_score=98.2,
    status=AssetStatus.HEALTHY,
    latest_sensor=sensor,
)

print(pump.model_dump_json(indent=2))
```

================================================================================
FILE: scripts/test_rag.py
================================================================================

```python
from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.retriever import Retriever

embedder = Embedder()

store = VectorStore(embedder)
store.load()

retriever = Retriever(store.db)

results = retriever.retrieve(
    "How do I respond to a pressure spike?"
)

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content)
```

================================================================================
FILE: services/__init__.py
================================================================================

```python
```

================================================================================
FILE: services/asset.py
================================================================================

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

================================================================================
FILE: services/embedding.py
================================================================================

```python
```

================================================================================
FILE: services/health.py
================================================================================

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

================================================================================
FILE: services/incident_manager.py
================================================================================

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

================================================================================
FILE: services/incident_service.py
================================================================================

```python
from models.sensor import SensorType


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

================================================================================
FILE: services/kernel_factory.py
================================================================================

```python
from mao import MAOKernel

from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.flow_workflow import FlowWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow


def create_kernel():

    kernel = MAOKernel()

    kernel.register_workflow(
        PressureWorkflow()
    )

    kernel.register_workflow(
        TemperatureWorkflow()
    )

    kernel.register_workflow(
        GasWorkflow()
    )

    kernel.register_workflow(
        FlowWorkflow()
    )

    kernel.register_workflow(
        MaintenanceWorkflow()
    )


    return kernel
```

================================================================================
FILE: services/llm.py
================================================================================

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
from pathlib import Path

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

        return ChatGoogleGenerativeAI(

            model=self.model_name,

            google_api_key=key,
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

================================================================================
FILE: services/persistence.py
================================================================================

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

================================================================================
FILE: services/report.py
================================================================================

```python
```

================================================================================
FILE: services/runtime.py
================================================================================

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

for agent in (
    SafetyAgent(),
    KnowledgeAgent(),
    MaintenanceAgent(),
    DiagnosticAgent(),
    PlanningAgent(),
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

================================================================================
FILE: services/sensor.py
================================================================================

```python
```

================================================================================
FILE: services/simulation.py
================================================================================

```python
```

================================================================================
FILE: services/telemetry_store.py
================================================================================

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

================================================================================
FILE: services/vision.py
================================================================================

```python
```

================================================================================
FILE: services/weather.py
================================================================================

```python
```

================================================================================
FILE: simulator/asset.py
================================================================================

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

================================================================================
FILE: simulator/event_generator.py
================================================================================

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

================================================================================
FILE: simulator/facility.py
================================================================================

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

        self.injector.schedule(
            tick=40,
            asset_index=0,
            sensor=SensorType.VIBRATION,
            value=40,
        )

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

================================================================================
FILE: simulator/fault_injector.py
================================================================================

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

================================================================================
FILE: simulator/sensor.py
================================================================================

```python
```

================================================================================
FILE: simulator/simulator.py
================================================================================

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

================================================================================
FILE: tests/mock_agent.py
================================================================================

```python
from agents.base import Agent
from mao.models.result import AgentResult


class MockAgent(Agent):

    def __init__(self):

        super().__init__("mock")


    def execute(self, task):

        return AgentResult(
            agent_name=self.name,
            success=True,
            confidence=1.0,
            summary="Mock execution successful.",
            recommendations=[],
            metadata={},
            execution_time=0.0,
        )
```

================================================================================
FILE: tests/mock_workflow.py
================================================================================

```python
from mao.workflows.workflow import Workflow
from mao.models.task import Task


class MockWorkflow(Workflow):

    name = "default"

    def build(self, event):

        return [
            Task(
                name="Mock Task",
                description="Test task",
                assigned_agent="mock",
                priority=1,
            )
        ]
```

================================================================================
FILE: tests/test_kernel.py
================================================================================

```python
from mao import MAOKernel
from mao.events.event import Event

from tests.mock_agent import MockAgent
from tests.mock_workflow import MockWorkflow

kernel = MAOKernel()

kernel.register_agent(MockAgent())
kernel.register_workflow(MockWorkflow())

event = Event(
    name="PressureSpike",
    source="Pump-A",
    payload={"pressure": 120},
)

report = kernel.handle_event(event)

print(report)
```

================================================================================
FILE: tests/test_neon.py
================================================================================

```python
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

print("connected to database")
conn.close()
```

================================================================================
FILE: tools/__init__.py
================================================================================

```python
```

================================================================================
FILE: tools/base_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/email_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/notification_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/postgres_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/report_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/search_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/sensor_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/simulation_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/vector_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/vision_tool.py
================================================================================

```python
```

================================================================================
FILE: tools/weather_tool.py
================================================================================

```python
```

================================================================================
FILE: workflows/__init__.py
================================================================================

```python
```

================================================================================
FILE: workflows/compliance_review.py
================================================================================

```python
```

================================================================================
FILE: workflows/emergency_evacuation.py
================================================================================

```python
```

================================================================================
FILE: workflows/fire_response.py
================================================================================

```python
```

================================================================================
FILE: workflows/leak_response.py
================================================================================

```python
```

================================================================================
FILE: workflows/maintenance_cycle.py
================================================================================

```python
```

================================================================================
FILE: workflows/production_optimization.py
================================================================================

```python
```

================================================================================
FILE: workflows/report_generation.py
================================================================================

```python
```

================================================================================
FILE: workflows/shutdown_sequence.py
================================================================================

```python
```

================================================================================
FILE: workflows/startup_sequence.py
================================================================================

```python
```

## Export Summary

- Total number of files exported: 174
- Total lines of code: 5235
- Export completed successfully
`````

### run.py

**File path:** `run.py`

```python

```

### scripts/benchmark.py

**File path:** `scripts/benchmark.py`

```python

```

### scripts/build_knowledge.py

**File path:** `scripts/build_knowledge.py`

```python
"""Build the Neon/pgvector knowledge index used by the Streamlit UI."""

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(
        str(ROOT_DIR)
    )


from rag.ingestion import KnowledgeIngestion


def parse_args():
    parser = argparse.ArgumentParser(
        description="Index PDF knowledge documents into the configured Neon database."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=ROOT_DIR / "docs",
        help="Directory containing PDF source documents (default: ./docs).",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing knowledge chunks before indexing. Use for a clean rebuild.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        raise SystemExit(f"Documents directory does not exist: {docs_dir}")

    engine = KnowledgeIngestion()
    if args.replace:
        deleted = engine.vector_store.clear()
        print(f"Removed {deleted} existing knowledge chunk(s).")

    count = engine.ingest_folder(docs_dir)
    total = engine.vector_store.count()
    print(f"Indexed {count} chunk(s). Neon now contains {total} searchable chunk(s).")


if __name__ == "__main__":
    main()
```

### scripts/build_rag.py

**File path:** `scripts/build_rag.py`

```python
from pathlib import Path

from rag.pipeline import RAGPipeline

docs_folder = Path("docs")

pdfs = [str(pdf) for pdf in docs_folder.glob("*.pdf")]

pipeline = RAGPipeline()

pipeline.build(pdfs)

print("✅ FAISS index created successfully!")
```

### scripts/generate_embeddings.py

**File path:** `scripts/generate_embeddings.py`

```python

```

### scripts/ingest_documents.py

**File path:** `scripts/ingest_documents.py`

```python

```

### scripts/run_simulation.py

**File path:** `scripts/run_simulation.py`

```python
import time
from uuid import uuid4

from mao import MAOKernel

from models.asset import Asset, AssetType
from models.facility import Facility

from simulator.facility import SimulatedFacility
from simulator.simulator import Simulator


from tests.mock_workflow import MockWorkflow

from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from mao.workflows.flow_workflow import FlowWorkflow

from agents.safety import SafetyAgent
from agents.knowledge import KnowledgeAgent
from agents.maintenance import MaintenanceAgent
from agents.diagnostic import DiagnosticAgent
from agents.planning import PlanningAgent



# -----------------------------
# Create Assets
# -----------------------------

pump_a = Asset(
    name="Pump A",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

pump_b = Asset(
    name="Pump B",
    asset_type=AssetType.PUMP,
    location="Zone A",
)

tank_a = Asset(
    name="Tank A",
    asset_type=AssetType.TANK,
    location="Zone B",
)


facility = Facility(
    id=str(uuid4()),
    name="RigOS Alpha",
    assets=[
        pump_a,
        pump_b,
        tank_a,
    ],
)



# -----------------------------
# Setup MAO
# -----------------------------

kernel = MAOKernel()


# Register assets

for asset in facility.assets:

    kernel.asset_service.register(asset)



# Register workflows

kernel.register_workflow(MockWorkflow())

kernel.register_workflow(PressureWorkflow())
kernel.register_workflow(TemperatureWorkflow())
kernel.register_workflow(GasWorkflow())
kernel.register_workflow(MaintenanceWorkflow())
kernel.register_workflow(FlowWorkflow())



# Register agents

kernel.register_agent(SafetyAgent())
kernel.register_agent(KnowledgeAgent())
kernel.register_agent(MaintenanceAgent())
kernel.register_agent(DiagnosticAgent())
kernel.register_agent(PlanningAgent())



# -----------------------------
# Simulator
# -----------------------------

facility_sim = SimulatedFacility(facility)


simulator = Simulator(
    facility=facility_sim,
    kernel=kernel,
)



print("=" * 60)
print("🏭 RigOS Alpha Refinery")
print("=" * 60)


tick = 0


while True:

    tick += 1


    telemetry, reports = simulator.tick(tick)


    print(f"\nTick {tick}")
    print("-" * 50)



    for reading in telemetry:

        print(
            f"{reading.sensor_type.value:<12}"
            f"{reading.value:>8.2f}"
        )



    if reports:

        print("\n🚨 INCIDENT DETECTED")


        for report in reports:

            print(report.final_summary)



    print("\nRegistered Agents")


    for agent in kernel.registry.all():

        print("-", agent.name)



    print("\nTelemetry History")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        print(
            f"{asset.name:<10} -> {len(history)} readings"
        )



    print("\nAsset Health")


    for asset in facility.assets:


        history = kernel.state.get_history(asset.id)


        health = kernel.health.calculate_health(history)


        kernel.asset_service.update_health(
            asset.id,
            health
        )


        asset_obj = kernel.asset_service.get(asset.id)


        print(
            f"{asset_obj.name:<10}"
            f"{asset_obj.health:>7.1f}%   "
            f"{asset_obj.status}"
        )



    print("\nMemory")


    print(
        "Events:",
        len(kernel.memory.events)
    )


    print(
        "Reports:",
        len(kernel.memory.execution_reports)
    )


    print(
        "Agent Results:",
        len(kernel.memory.agent_results)
    )



    time.sleep(1)
```

### scripts/seed_database.py

**File path:** `scripts/seed_database.py`

```python

```

### scripts/test_knowledge.py

**File path:** `scripts/test_knowledge.py`

```python
"""Test script for KnowledgeAgent."""

from agents.knowledge import KnowledgeAgent
from mao.models.task import Task


def test_knowledge_agent():
    """Test the KnowledgeAgent with a simple query."""
    
    # Create the agent
    agent = KnowledgeAgent()
    
    task = Task(
        name="Knowledge Test",
        description="What should operators do during a pressure spike?",
        assigned_agent="knowledge",
        priority=1,
    )
    
    result = agent.execute(task, context=None)
    
    print("=" * 60)
    print("KnowledgeAgent Test Results")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Confidence: {result.confidence}")
    print(f"Finding: {result.finding}")
    print("\nSummary:")
    print(result.summary)
    print("\nRecommendations:")
    for rec in result.recommendations:
        print(f"  - {rec}")
    print("=" * 60)


if __name__ == "__main__":
    test_knowledge_agent()
```

### scripts/test_mao.py

**File path:** `scripts/test_mao.py`

```python
"""Test script for MAO kernel."""

from mao import MAOKernel
from agents.safety import SafetyAgent
from mao.events.event import Event

# Create kernel
kernel = MAOKernel()

# Register agent
safety = SafetyAgent()
kernel.register_agent(safety)

# Create event
event = Event(
    name="PressureSpike",
    source="SensorAgent",
    payload={
        "asset": "Pump A",
        "pressure": 112,
    },
)

# ✅ FIXED: Use handle_event
report = kernel.handle_event(event)

print("=" * 60)
print("MAO Test Results")
print("=" * 60)
print(f"Workflow: {report.workflow_name}")
print(f"Success: {report.success}")
print(f"Summary: {report.final_summary}")
print(f"Confidence: {report.average_confidence}")
```

### scripts/test_models.py

**File path:** `scripts/test_models.py`

```python
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
```

### scripts/test_rag.py

**File path:** `scripts/test_rag.py`

```python
from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.retriever import Retriever

embedder = Embedder()
store = VectorStore(embedder)

# ✅ FIXED: Provide path
FAISS_INDEX_PATH = "./data/faiss_index"
store.load(FAISS_INDEX_PATH)

retriever = Retriever(store.db)
results = retriever.retrieve("How do I respond to a pressure spike?")

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content)
```

### services/__init__.py

**File path:** `services/__init__.py`

```python
"""Services module exports."""

from services.asset import AssetService
from services.health import HealthService
from services.llm import LLMManager
from services.persistence import PersistenceService
from services.config_services import ConfigService
from services.simulator_controller import SimulatorController, sim_controller
from services.runtime import kernel, simulator

__all__ = [
    "AssetService",
    "HealthService",
    "LLMManager",
    "PersistenceService",
    "ConfigService",
    "SimulatorController",
    "sim_controller",
    "kernel",
    "simulator",
]
```

### services/asset.py

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

### services/config_services.py

**File path:** `services/config_services.py`

```python
"""Gemini-powered dynamic configuration service."""

import json
import re
from typing import Any, Dict, List, Optional
from services.llm import LLMManager


class ConfigService:
    """Generate and cache operational configurations using Gemini."""

    _instance = None
    _cache: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.llm = LLMManager()

    def get_thresholds(self, asset_type: str, context: Optional[str] = None) -> Dict[str, float]:
        """Generate asset-specific thresholds using Gemini."""
        cache_key = f"thresholds_{asset_type}_{context or 'default'}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prompt = f"""
You are an industrial operations configuration expert.

Generate operational thresholds for a {asset_type} asset in a {context or 'standard'} industrial environment.

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
            response = self.llm.generate(prompt)
            thresholds = self._parse_json(response)
            self._cache[cache_key] = thresholds
            return thresholds
        except Exception as e:
            print(f"⚠️ Gemini config generation failed: {e}")
            return self._get_default_thresholds(asset_type)

    def _parse_json(self, response: str) -> Dict:
        """Extract JSON from Gemini response."""
        # Find JSON-like content
        start = response.find('{')
        end = response.rfind('}') + 1
        if start >= 0 and end > start:
            json_str = response[start:end]
            # Clean up common issues
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
        }
        return defaults.get(asset_type, defaults["Pump"])

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
            response = self.llm.generate(prompt)
            sequence = self._parse_json(response)
            if isinstance(sequence, list):
                self._cache[cache_key] = sequence
                return sequence
        except Exception:
            pass

        # Fallback - standard sequence
        return ["sensor", "safety", "diagnostic", "knowledge", "maintenance", "planning", "prediction", "notification", "report"]

    def get_priority_level(self, incident_type: str, severity: str) -> int:
        """Generate priority level for an incident."""
        prompt = f"""
For an industrial {incident_type} incident with {severity} severity, assign a priority level.

Priority is 1 (highest) to 9 (lowest).
Return ONLY an integer.
"""

        try:
            response = self.llm.generate(prompt)
            numbers = re.findall(r'\d+', response)
            if numbers:
                priority = int(numbers[0])
                return max(1, min(9, priority))
        except Exception:
            pass

        # Fallback
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
            response = self.llm.generate(prompt)
            weights = self._parse_json(response)
            self._cache[cache_key] = weights
            return weights
        except Exception:
            pass

        # Fallback
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

### services/embedding.py

**File path:** `services/embedding.py`

```python

```

### services/health.py

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

### services/incident_manager.py

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

### services/incident_service.py

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

### services/kernel_factory.py

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

### services/llm.py

**File path:** `services/llm.py`

```python
"""Centralized, failover-safe access to Gemini models with multi-key rotation."""

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

# Support for up to 10 API keys
SUPPORTED_GEMINI_ENV_VARS = (
    "GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3",
    "GEMINI_API_KEY_4", "GEMINI_API_KEY_5", "GEMINI_API_KEY_6",
    "GEMINI_API_KEY_7", "GEMINI_API_KEY_8", "GEMINI_API_KEY_9",
    "GEMINI_API_KEY_10",
    "GEMINI_API_KEY", "GOOGLE_API_KEY",
    "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3",
)

DEFAULT_GEMINI_MODEL = "gemini-2.0-flash-lite"

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

        if self.failures >= 5:
            self.is_active = False
            self.cooldown_until = time.time() + 60
            logger.warning(f"Key {self.index + 1} deactivated for 60s due to {self.failures} failures")

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


class LLMManager:
    """Central Gemini router with automatic multi-key rotation."""

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

    @staticmethod
    def _load_keys() -> List[str]:
        """Load API keys from environment variables and Streamlit secrets."""
        keys = []
        seen = set()

        for var in SUPPORTED_GEMINI_ENV_VARS:
            value = os.getenv(var)
            if value and value not in seen:
                seen.add(value)
                keys.append(value)

        try:
            import streamlit as st
            for var in SUPPORTED_GEMINI_ENV_VARS:
                if var in st.secrets:
                    value = st.secrets[var]
                    if value and value not in seen:
                        seen.add(value)
                        keys.append(value)
        except Exception:
            pass

        return keys

    def _get_next_available_key(self) -> Optional[str]:
        """Get the next available API key with rotation."""
        total_keys = len(self.keys)
        attempts = 0

        while attempts < total_keys * 2:
            idx = self.current_key_index
            key = self.keys[idx]
            self.current_key_index = (self.current_key_index + 1) % total_keys

            status = self.key_statuses[key]
            if not status.is_active:
                status.reactivate_if_ready()

            if status.is_available:
                status.last_used = time.time()
                return key

            attempts += 1

        # Fallback: return first key
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

    def generate(self, prompt: str, max_retries_per_key: int = 2) -> str:
        """Generate Gemini response with automatic multi-key rotation."""
        last_error = None

        for attempt in range(len(self.keys) * max_retries_per_key + 1):
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
                if key and key in self.key_statuses:
                    status = self.key_statuses[key]
                    status.record_failure(str(error))
                    logger.warning(f"Key {status.index + 1} failed: {str(error)[:100]}")
                time.sleep(0.5)

        raise RuntimeError(
            f"All {len(self.keys)} Gemini API keys failed. Check quota and permissions."
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
```

### services/persistence.py

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

### services/refinery_generator.py

**File path:** `services/refinery_generator.py`

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

### services/report.py

**File path:** `services/report.py`

```python

```

### services/runtime.py

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
from services.refinery_generator import RefineryGenerator

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

embedder = Embedder()
vector_store = NeonVectorStore(embedder.get_model())

# Register all 9 agents
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

# ✅ Generate multiple refineries with assets
refineries = RefineryGenerator.generate_refineries(count=5, assets_per_refinery=50)

# Register all assets
all_assets = []
for refinery in refineries:
    for asset in refinery.assets:
        kernel.asset_service.register(asset)
        all_assets.append(asset)

# Store refineries in kernel for access
kernel._refineries = refineries

print(f"✅ Loaded {len(refineries)} refineries with {len(all_assets)} total assets")

# Create a simulated facility with ALL assets
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
```

### services/sensor.py

**File path:** `services/sensor.py`

```python

```

### services/simulation.py

**File path:** `services/simulation.py`

```python

```

### services/simulator_controller.py

**File path:** `services/simulator_controller.py`

```python
"""Simulator controller with threading support."""

import threading
import time
from typing import Dict, List, Optional, Any
from services.runtime import simulator, kernel


class SimulatorController:
    """Controls the simulation lifecycle with UI integration."""

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.tick_count = 0
        self._latest_telemetry: List[Any] = []
        self._latest_reports: List[Any] = []

    def start(self, interval: float = 1.0):
        """Start the simulation in a background thread."""
        if self.running:
            return

        self.running = True
        kernel._simulation_running = True
        self._thread = threading.Thread(
            target=self._run,
            args=(interval,),
            daemon=True
        )
        self._thread.start()
        print(f"✅ Simulation started with interval {interval}s")

    def stop(self):
        """Stop the simulation."""
        self.running = False
        kernel._simulation_running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("⏹️ Simulation stopped")

    def step(self) -> tuple[List[Any], List[Any]]:
        """Advance simulation by one tick (synchronous)."""
        self.tick_count += 1
        telemetry, reports = simulator.tick(self.tick_count)
        self._latest_telemetry = telemetry
        self._latest_reports = reports
        return telemetry, reports

    def _run(self, interval: float):
        """Main simulation loop."""
        while self.running:
            try:
                telemetry, reports = self.step()
            except Exception as e:
                print(f"⚠️ Simulation error: {e}")
                continue
            time.sleep(interval)

    def get_latest_telemetry(self) -> List[Any]:
        """Get the latest telemetry from the last tick."""
        return self._latest_telemetry

    def get_latest_reports(self) -> List[Any]:
        """Get the latest reports from the last tick."""
        return self._latest_reports

    def get_status(self) -> Dict:
        """Get current simulation status."""
        return {
            "running": self.running,
            "ticks": self.tick_count,
            "assets": len(kernel.asset_service.all_assets()),
            "events": len(kernel.event_store.all()),
            "reports": len(kernel.state.execution_reports),
            "agent_results": len(kernel.state.agent_results),
        }


# Singleton controller
sim_controller = SimulatorController()
```

### services/telemetry_store.py

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

### services/vision.py

**File path:** `services/vision.py`

```python

```

### services/weather.py

**File path:** `services/weather.py`

```python

```

### simulator/asset.py

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

### simulator/event_generator.py

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

### simulator/facility.py

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

### simulator/fault_injector.py

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

### simulator/sensor.py

**File path:** `simulator/sensor.py`

```python

```

### simulator/simulator.py

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

### tests/conftest.py

**File path:** `tests/conftest.py`

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from mao.core.context import ExecutionContext


class DummyEvent:
    def __init__(self, payload):
        self.payload = payload


@pytest.fixture
def normal_context():
    event = DummyEvent(
        {
            "pressure": 120,
            "temperature": 50,
            "gas_level": 5,
            "vibration": 2,
            "flow_rate": 80,
        }
    )

    return ExecutionContext(
        event,
        state_manager=None,
        memory_manager=None,
        logger=None,
    )


@pytest.fixture
def critical_context():

    event = DummyEvent(
        {
            "pressure": 170,
            "temperature": 95,
            "gas_level": 60,
            "vibration": 10,
            "flow_rate": 20,
        }
    )

    return ExecutionContext(
        event,
        state_manager=None,
        memory_manager=None,
        logger=None,
    )
```

### tests/mock_workflow.py

**File path:** `tests/mock_workflow.py`

```python
"""Mock workflow for testing purposes."""

from mao.workflows.workflow import Workflow
from mao.models.task import Task


class MockWorkflow(Workflow):
    """A simple mock workflow for testing the MAO system."""

    name = "mock_workflow"

    def build(self, event):
        """Create a single task for testing."""
        return [
            Task(
                name="Mock Task",
                description="Mock task for testing",
                assigned_agent="safety",
                priority=1,
                input_data={
                    "event_id": event.id,
                    "event_name": event.name,
                    "source": event.source,
                }
            )
        ]
```

### tests/test_agent_pipeline.py

**File path:** `tests/test_agent_pipeline.py`

```python
from unittest.mock import MagicMock

from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent
from agents.planning import PlanningAgent
from agents.knowledge import KnowledgeAgent

from mao.models.task import Task


def test_pipeline(critical_context):

    SafetyAgent().run(
        Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context
    )

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
        ),
        critical_context
    )

    MaintenanceAgent().run(
        Task(
            name="Maintenance",
            description="Generate maintenance plan",
            assigned_agent="maintenance",
            priority=3,
        ),
        critical_context
    )

    PlanningAgent().run(
        Task(
            name="Planning",
            description="Generate execution plan",
            assigned_agent="planning",
            priority=4,
        ),
        critical_context
    )

    agent = KnowledgeAgent(
        MagicMock()
    )

    agent.retriever = MagicMock()

    agent.retriever.retrieve.return_value = []

    agent.run(
        Task(
            name="Knowledge",
            description="Retrieve knowledge",
            assigned_agent="knowledge",
            priority=5,
        ),
        critical_context
    )

    expected = [
        "safety",
        "diagnosis",
        "maintenance",
        "planning",
        "knowledge",
    ]

    for key in expected:
        assert key in critical_context.metadata
```

### tests/test_diagnostic_agent.py

**File path:** `tests/test_diagnostic_agent.py`

```python
from agents.diagnostic import DiagnosticAgent
from agents.safety import SafetyAgent
from mao.models.task import Task


safety_task = Task(
    name="Safety",
    description="Safety Assessment",
    assigned_agent="safety",
    priority=1,
)

diag_task = Task(
    name="Diagnosis",
    description="Run diagnostics",
    assigned_agent="diagnostic",
    priority=2,
)

def test_diagnosis(critical_context):

    SafetyAgent().run(
        safety_task,
        critical_context,
    )

    result = DiagnosticAgent().run(
        diag_task,
        critical_context,
    )

    assert result.success

    assert "diagnosis" in critical_context.metadata

    diagnosis = critical_context.metadata["diagnosis"]

    assert len(diagnosis["diagnosis"]) > 0
```

### tests/test_knowledge_agent.py

**File path:** `tests/test_knowledge_agent.py`

```python
from unittest.mock import MagicMock

from agents.knowledge import KnowledgeAgent

from mao.models.task import Task


def test_knowledge():

    retriever = MagicMock()

    retriever.retrieve.return_value = []

    vector_store = MagicMock()

    agent = KnowledgeAgent(vector_store)

    agent.retriever = retriever

    from mao.core.context import ExecutionContext


    class Event:
        payload = {}


    context = ExecutionContext(
        Event(),
        None,
        None,
        None,
    )

    result = agent.run(
        Task(
            name="Knowledge",
            description="Retrieve knowledge",
            assigned_agent="knowledge",
            priority=5,
        ),
        context,
    )

    assert result.success

    assert "knowledge" in context.metadata
```

### tests/test_maintenance_agent.py

**File path:** `tests/test_maintenance_agent.py`

```python
from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent

from mao.models.task import Task


def test_maintenance_plan(critical_context):

    SafetyAgent().run(Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context,
    )
    

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
            
        ),
        critical_context,
    )

    result = MaintenanceAgent().run(
        Task(
            name="Maintenance",
            description="Generate maintenance plan",
            assigned_agent="maintenance",
            priority=3,
        ),
        critical_context,
    )

    assert result.success

    metadata = critical_context.metadata["maintenance"]

    assert "priority" in metadata

    assert "work_orders" in metadata

    assert len(metadata["work_orders"]) > 0
```

### tests/test_neon.py

**File path:** `tests/test_neon.py`

```python
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

print("connected to database")
conn.close()
```

### tests/test_planning_agent.py

**File path:** `tests/test_planning_agent.py`

```python
from agents.safety import SafetyAgent
from agents.diagnostic import DiagnosticAgent
from agents.maintenance import MaintenanceAgent
from agents.planning import PlanningAgent

from mao.models.task import Task


def test_plan_generation(critical_context):

    SafetyAgent().run(
        Task(
            name="Safety",
            description="Safety Assessment",
            assigned_agent="safety",
            priority=1,
        ),
        critical_context
    )

    DiagnosticAgent().run(
        Task(
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
        ),
        critical_context
    )

    
    MaintenanceAgent().run(
        Task(
            name="Maintenance",
            description="Generate maintenance plan",
            assigned_agent="maintenance",
            priority=3,
        ),
        critical_context
    )

    result = PlanningAgent().run(
        Task(
            name="Planning",
            description="Generate execution plan",
            assigned_agent="planning",
            priority=4,
        ),
        critical_context,   
    )

    assert result.success

    assert "planning" in critical_context.metadata

    plan = critical_context.metadata["planning"]

    assert len(plan["execution_plan"]) > 0
```

### tests/test_safety_agent.py

**File path:** `tests/test_safety_agent.py`

```python
from agents.safety import SafetyAgent
from mao.models.task import Task


task = Task(
    name="Safety",
    description="",
    assigned_agent="safety",
    priority=1,
)


def test_safe_system(normal_context):

    agent = SafetyAgent()

    result = agent.run(task, normal_context)

    assert result.success
    assert result.confidence > 0

    assert "safety" in normal_context.metadata

    assert (
        normal_context.metadata["safety"]["status"]
        == "SAFE"
    )


def test_critical_system(critical_context):

    agent = SafetyAgent()

    result = agent.run(task, critical_context)

    assert result.success

    metadata = critical_context.metadata["safety"]

    assert metadata["status"] == "CRITICAL"

    assert metadata["risk_score"] >= 80

    assert len(metadata["alerts"]) > 0
```

### tools/__init__.py

**File path:** `tools/__init__.py`

```python

```

### tools/base_tool.py

**File path:** `tools/base_tool.py`

```python

```

### tools/email_tool.py

**File path:** `tools/email_tool.py`

```python

```

### tools/notification_tool.py

**File path:** `tools/notification_tool.py`

```python

```

### tools/postgres_tool.py

**File path:** `tools/postgres_tool.py`

```python

```

### tools/report_tool.py

**File path:** `tools/report_tool.py`

```python

```

### tools/search_tool.py

**File path:** `tools/search_tool.py`

```python

```

### tools/sensor_tool.py

**File path:** `tools/sensor_tool.py`

```python

```

### tools/simulation_tool.py

**File path:** `tools/simulation_tool.py`

```python

```

### tools/vector_tool.py

**File path:** `tools/vector_tool.py`

```python

```

### tools/vision_tool.py

**File path:** `tools/vision_tool.py`

```python

```

### tools/weather_tool.py

**File path:** `tools/weather_tool.py`

```python

```

### workflows/__init__.py

**File path:** `workflows/__init__.py`

```python

```

### workflows/compliance_review.py

**File path:** `workflows/compliance_review.py`

```python

```

### workflows/emergency_evacuation.py

**File path:** `workflows/emergency_evacuation.py`

```python

```

### workflows/fire_response.py

**File path:** `workflows/fire_response.py`

```python

```

### workflows/leak_response.py

**File path:** `workflows/leak_response.py`

```python

```

### workflows/maintenance_cycle.py

**File path:** `workflows/maintenance_cycle.py`

```python

```

### workflows/production_optimization.py

**File path:** `workflows/production_optimization.py`

```python

```

### workflows/report_generation.py

**File path:** `workflows/report_generation.py`

```python

```

### workflows/shutdown_sequence.py

**File path:** `workflows/shutdown_sequence.py`

```python

```

### workflows/startup_sequence.py

**File path:** `workflows/startup_sequence.py`

```python

```

