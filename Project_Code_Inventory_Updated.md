# Project Code Inventory (Updated)

Generated: 2026-07-23 12:30:25 UTC

## Scope

This document contains the complete text source for 181 project files (6592 lines) from the repository root. It includes application code, tests, scripts, configuration, and Markdown documentation. It excludes Git metadata, virtual environments, generated/binary data, generated inventory files, and the secret-bearing `.env` file.

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
│   ├── planning.py
│   └── safety.py
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
│   │   └── knowledge_agent_adapter.py
│   ├── Home.py
│   ├── pages
│   │   ├── 1_Dashboard.py
│   │   ├── 10_Health_Prediction.py
│   │   ├── 11_Maintenance_Planner.py
│   │   ├── 12_AI_Activity.py
│   │   ├── 13_Digital_Twin.py
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
│   ├── base.py
│   ├── bootstrap.py
│   ├── connection.py
│   ├── migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── 0001_operational_records.py
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
│   │   ├── result.py
│   │   └── task.py
│   ├── orchestrator.py
│   ├── tools
│   │   └── tool_registry.py
│   └── workflows
│       ├── flow_workflow.py
│       ├── gas_workflow.py
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
│   ├── parser.py
│   ├── pipeline.py
│   ├── reranker.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vector_store.py
├── README.md
├── requirements.txt
├── run.py
├── scripts
│   ├── benchmark.py
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
│   ├── embedding.py
│   ├── health.py
│   ├── incident_manager.py
│   ├── incident_service.py
│   ├── kernel_factory.py
│   ├── llm.py
│   ├── persistence.py
│   ├── report.py
│   ├── runtime.py
│   ├── sensor.py
│   ├── simulation.py
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
"""
agents/diagnostic.py

Production Diagnostic Agent

Responsibilities
----------------
- Analyze telemetry
- Use Safety Agent findings
- Determine probable root causes
- Publish diagnosis metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class DiagnosticAgent(Agent):

    name = "diagnostic"

    def execute(self, task, context):

        telemetry = self._extract_telemetry(context)

        safety = self._get_safety(context)

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", 0)
        vibration = telemetry.get("vibration", 0)
        flow = telemetry.get("flow_rate", 0)

        diagnosis = []
        evidence = []

        # Pressure
        if pressure >= 150:
            diagnosis.append("Pressure surge")
            evidence.append(
                "Pressure exceeded safe operating threshold."
            )

        # Temperature
        if temperature >= 85:
            diagnosis.append("Equipment overheating")
            evidence.append(
                "Temperature above recommended operating range."
            )

        # Gas
        if gas >= 40:
            diagnosis.append("Possible gas leak")
            evidence.append(
                "Gas concentration indicates potential leak."
            )

        # Vibration
        if vibration >= 8:
            diagnosis.append("Mechanical wear")
            evidence.append(
                "High vibration suggests bearing or shaft wear."
            )

        # Flow
        if flow and flow <= 25:
            diagnosis.append("Flow restriction")
            evidence.append(
                "Low flow rate indicates blockage or valve restriction."
            )

        if not diagnosis:
            diagnosis.append("System operating normally")

        confidence = 0.95 if safety.get("status") != "SAFE" else 0.90

        recommendations = []

        if "Pressure surge" in diagnosis:
            recommendations.append(
                "Inspect pressure relief valve."
            )

        if "Equipment overheating" in diagnosis:
            recommendations.append(
                "Check cooling system."
            )

        if "Possible gas leak" in diagnosis:
            recommendations.append(
                "Inspect pipelines and gas sensors."
            )

        if "Mechanical wear" in diagnosis:
            recommendations.append(
                "Inspect rotating equipment."
            )

        if "Flow restriction" in diagnosis:
            recommendations.append(
                "Inspect valves and pipelines."
            )

        if not recommendations:
            recommendations.append(
                "Continue monitoring."
            )

        metadata = {
            "diagnosis": diagnosis,
            "confidence": confidence,
            "evidence": evidence,
            "source": "DiagnosticAgent",
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=", ".join(diagnosis),
            confidence=confidence,
            evidence=evidence,
            recommendations=recommendations,
            required_action=(
                "Maintenance inspection"
                if diagnosis != ["System operating normally"]
                else "None"
            ),
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

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["diagnosis"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["diagnosis"] = metadata
```

### agents/knowledge.py

**File path:** `agents/knowledge.py`

```python
"""
agents/knowledge.py

Production Knowledge Agent

Responsibilities
----------------
- Query the RAG knowledge base
- Retrieve relevant SOPs and manuals
- Provide contextual recommendations
- Publish knowledge metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult
from rag.retriever import Retriever


class KnowledgeAgent(Agent):

    name = "knowledge"

    def __init__(self,vector_store):

        super().__init__()
        self.retriever = Retriever(vector_store)

    def execute(self, task, context):

        diagnosis = self._get_metadata(
            context,
            "diagnosis",
        )

        planning = self._get_metadata(
            context,
            "planning",
        )

        findings = diagnosis.get(
            "diagnosis",
            [],
        )

        execution_plan = planning.get(
            "execution_plan",
            [],
        )

        query = self._build_query(findings)

        documents = []

        try:
            documents = self.retriever.retrieve(query)

        except Exception:

            documents = []

        references = []
        summaries = []

        for doc in documents:

            references.append(
                doc.metadata.get(
                    "source",
                    "Unknown"
                )
            )

            summaries.append(
                doc.page_content[:300]
            )

        recommendations = list(execution_plan)

        if summaries:

            recommendations.append(
                "Review retrieved operating procedures before execution."
            )

        metadata = {
            "query": query,
            "references": references,
            "documents": summaries,
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=(
                f"{len(documents)} knowledge document(s) retrieved."
            ),
            confidence=0.94,
            evidence=references,
            recommendations=recommendations,
            required_action="Consult retrieved documentation",
            requires_human_approval=False,
            metadata=metadata,
            summary=(
                f"Knowledge retrieval completed with "
                f"{len(documents)} matching document(s)."
            ),
        )

    def _build_query(self, findings):

        if not findings:
            return "general oil and gas operational procedures"

        return " ".join(findings)

    def _get_metadata(self, context, key):

        if isinstance(context, dict):
            return context.get(
                "metadata",
                {},
            ).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["knowledge"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["knowledge"] = metadata
```

### agents/maintenance.py

**File path:** `agents/maintenance.py`

```python
"""
agents/maintenance.py

Production Maintenance Agent

Responsibilities
----------------
- Review diagnostic findings
- Assess maintenance urgency
- Recommend maintenance actions
- Estimate downtime
- Publish maintenance metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class MaintenanceAgent(Agent):

    name = "maintenance"

    def execute(self, task, context):

        diagnosis = self._get_metadata(
            context,
            "diagnosis",
        )

        safety = self._get_metadata(
            context,
            "safety",
        )

        findings = diagnosis.get(
            "diagnosis",
            [],
        )

        work_orders = []
        priority = "LOW"
        downtime = "None"

        if "Pressure surge" in findings:
            work_orders.append(
                "Inspect pressure relief system"
            )
            priority = "HIGH"
            downtime = "2-4 hours"

        if "Equipment overheating" in findings:
            work_orders.append(
                "Inspect cooling system"
            )
            priority = "HIGH"
            downtime = "3-5 hours"

        if "Possible gas leak" in findings:
            work_orders.append(
                "Emergency pipeline inspection"
            )
            priority = "CRITICAL"
            downtime = "Immediate shutdown"

        if "Mechanical wear" in findings:
            work_orders.append(
                "Replace worn bearings"
            )

            if priority != "CRITICAL":
                priority = "MEDIUM"

            downtime = "4-6 hours"

        if "Flow restriction" in findings:
            work_orders.append(
                "Inspect valves and clean pipeline"
            )

            if priority == "LOW":
                priority = "MEDIUM"

            downtime = "2 hours"

        if not work_orders:
            work_orders.append(
                "No maintenance required"
            )

        metadata = {
            "priority": priority,
            "downtime": downtime,
            "work_orders": work_orders,
            "risk_status": safety.get("status", "SAFE"),
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Maintenance Priority: {priority}",
            confidence=0.95,
            evidence=work_orders,
            recommendations=work_orders,
            required_action=priority,
            requires_human_approval=(
                priority in ("HIGH", "CRITICAL")
            ),
            metadata=metadata,
            summary=(
                f"{len(work_orders)} maintenance task(s) "
                f"generated. Priority: {priority}."
            ),
        )

    def _get_metadata(
        self,
        context,
        key,
    ):

        if isinstance(context, dict):
            return context.get(
                "metadata",
                {},
            ).get(key, {})

        if not hasattr(context, "metadata"):
            return {}

        return context.metadata.get(key, {})

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["maintenance"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["maintenance"] = metadata
```

### agents/planning.py

**File path:** `agents/planning.py`

```python
"""
agents/planning.py

Production Planning Agent

Responsibilities
----------------
- Build an operational response plan
- Prioritize maintenance actions
- Recommend execution sequence
- Publish planning metadata
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class PlanningAgent(Agent):

    name = "planning"

    def execute(self, task, context):

        safety = self._get_metadata(context, "safety")
        diagnosis = self._get_metadata(context, "diagnosis")
        maintenance = self._get_metadata(context, "maintenance")

        status = safety.get("status", "SAFE")
        findings = diagnosis.get("diagnosis", [])
        work_orders = maintenance.get("work_orders", [])
        priority = maintenance.get("priority", "LOW")

        execution_plan = []

        if status == "CRITICAL":
            execution_plan.append(
                "Immediately reduce operating load."
            )
            execution_plan.append(
                "Notify control room."
            )

        if "Possible gas leak" in findings:
            execution_plan.append(
                "Isolate affected pipeline section."
            )

        if "Pressure surge" in findings:
            execution_plan.append(
                "Stabilize system pressure."
            )

        if "Equipment overheating" in findings:
            execution_plan.append(
                "Start cooling procedure."
            )

        execution_plan.extend(work_orders)

        if not execution_plan:
            execution_plan.append(
                "Continue normal operation."
            )

        estimated_duration = self._estimate_duration(priority)

        metadata = {
            "priority": priority,
            "execution_plan": execution_plan,
            "estimated_duration": estimated_duration,
            "status": status,
        }

        self._store_metadata(
            context,
            metadata,
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=f"Execution plan created ({priority} priority)",
            confidence=0.96,
            evidence=execution_plan,
            recommendations=execution_plan,
            required_action="Execute plan",
            requires_human_approval=(
                status == "CRITICAL"
            ),
            metadata=metadata,
            summary=(
                f"Operational plan generated with "
                f"{len(execution_plan)} step(s)."
            ),
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

            context.setdefault(
                "metadata",
                {}
            )["planning"] = metadata

            return

        if not hasattr(context, "metadata"):
            context.metadata = {}

        context.metadata["planning"] = metadata
```

### agents/safety.py

**File path:** `agents/safety.py`

```python
"""
agents/safety.py

Production Safety Agent

Responsibilities
----------------
- Analyze incoming telemetry
- Assess operational risk
- Detect safety threshold violations
- Publish safety metadata for downstream agents
"""

from __future__ import annotations

from agents.base import Agent
from mao.models.result import AgentResult


class SafetyAgent(Agent):

    name = "safety"

    PRESSURE_LIMIT = 150
    TEMPERATURE_LIMIT = 85
    GAS_LIMIT = 40
    VIBRATION_LIMIT = 8

    def execute(self, task, context):

        telemetry = self._extract_telemetry(context)

        pressure = telemetry.get("pressure", 0)
        temperature = telemetry.get("temperature", 0)
        gas = telemetry.get("gas_level", 0)
        vibration = telemetry.get("vibration", 0)

        alerts = []

        risk_score = 0

        if pressure >= self.PRESSURE_LIMIT:
            alerts.append(
                f"High pressure detected ({pressure} PSI)"
            )
            risk_score += 30

        if temperature >= self.TEMPERATURE_LIMIT:
            alerts.append(
                f"High temperature detected ({temperature} °C)"
            )
            risk_score += 25

        if gas >= self.GAS_LIMIT:
            alerts.append(
                f"Gas concentration elevated ({gas})"
            )
            risk_score += 35

        if vibration >= self.VIBRATION_LIMIT:
            alerts.append(
                f"Abnormal vibration detected ({vibration})"
            )
            risk_score += 20

        risk_score = min(risk_score, 100)

        if risk_score >= 80:
            status = "CRITICAL"

        elif risk_score >= 40:
            status = "WARNING"

        else:
            status = "SAFE"

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

            recommendations.append(
                "Continue normal operation"
            )

        metadata = {
            "status": status,
            "risk_score": risk_score,
            "alerts": alerts,
            "telemetry": telemetry,
            "confidence": 0.96,
        }

        self._store_metadata(
            context,
            metadata,
        )

        summary = (
            f"Safety assessment completed. "
            f"Status: {status}. "
            f"Risk Score: {risk_score}/100."
        )

        finding = (
            alerts[0]
            if alerts
            else "No safety issues detected."
        )

        return AgentResult(
            agent_name=self.name,
            success=True,
            finding=finding,
            confidence=0.96,
            evidence=alerts,
            recommendations=recommendations,
            required_action=(
                "Immediate intervention"
                if status == "CRITICAL"
                else "Continue monitoring"
            ),
            requires_human_approval=(
                status == "CRITICAL"
            ),
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

    def _store_metadata(
        self,
        context,
        metadata,
    ):

        if isinstance(context, dict):

            context.setdefault(
                "metadata",
                {}
            )["safety"] = metadata

            return

        if not hasattr(context, "metadata"):

            context.metadata = {}

        context.metadata["safety"] = metadata
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
        f"<b>{label}</b>   {status_chip(status)}"
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
            f"<b>{agent['Agent']} Agent</b>   {status_chip(state_tone)}"
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
        f"<div class='panel'><b>{asset['Asset']}</b>   {status_chip(asset['Status'])}"
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

### app/Home.py

**File path:** `app/Home.py`

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

### app/pages/1_Dashboard.py

**File path:** `app/pages/1_Dashboard.py`

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

### app/pages/10_Health_Prediction.py

**File path:** `app/pages/10_Health_Prediction.py`

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

### app/pages/11_Maintenance_Planner.py

**File path:** `app/pages/11_Maintenance_Planner.py`

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
        st.markdown(f"<div class='timeline-row'><span class='muted'>{window}</span><span class='timeline-dot'></span><div class='panel'><b>{asset}</b>   {status_chip('Critical' if priority == 'P1' else 'Warning')}<br><span class='muted'>Assigned engineer: {engineer} · Estimated downtime: {downtime}</span></div></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>AI SCHEDULING RATIONALE</div><div class='panel'><b>Optimized sequence</b><p class='muted'>Prioritizes the thermal-risk work order ahead of compressor inspection, while grouping pipeline work with instrumentation availability.</p><b>Expected impact</b><p class='muted'>Reduces forecasted operational risk by 18% and avoids overlap with peak production windows.</p></div>", unsafe_allow_html=True)

# TODO: Persist maintenance tasks, crew capacity, work-order status, and planning decisions through backend APIs.
```

### app/pages/12_AI_Activity.py

**File path:** `app/pages/12_AI_Activity.py`

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
    st.markdown(f"<div class='timeline-row'><span class='muted'>{event['time']}</span><span class='timeline-dot {'pulse' if event['state'] == 'Running' else ''}'></span><div class='panel'><b>{event['agent']}</b>   {status_chip(state_tone)}<br><span class='muted'>{event['action']} · Confidence {event['confidence']}</span></div></div>", unsafe_allow_html=True)
    st.progress(event["progress"], text=f"{event['progress']}% execution progress")

# TODO: Read immutable agent lifecycle events and audit metadata from the MAO backend/event store.
```

### app/pages/13_Digital_Twin.py

**File path:** `app/pages/13_Digital_Twin.py`

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
    st.markdown("<div class='panel' style='text-align:center; padding:2rem'><b>PROCESS A</b>   ───►   <b>PROCESS B</b>   ───►   <b>TERMINAL</b><br><br><span class='muted'>Utilities support all zones · Pipeline transfer monitored continuously</span></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>SELECTED ASSET DETAIL</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='panel'><b>{selected['Asset']}</b><p>{status_chip(selected['Status'])}</p><span class='muted'>Health: {selected['Health']}%<br>Temperature: {selected['Temperature']}<br>Pressure: {selected['Pressure']}<br>RPM: {selected['RPM']}<br>Failure probability: {selected['Failure']}</span><hr><b>AI recommendation</b><p class='muted'>Continue monitoring. Escalate if the live failure probability exceeds the configured threshold.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>TWIN CONTROLS</div>", unsafe_allow_html=True)
    st.selectbox("Overlay", ["Asset health", "Live telemetry", "Incident severity", "Maintenance schedule"])
    st.toggle("Show process connections", value=True)
    st.toggle("Highlight active incidents", value=True)

# TODO: Bind zones, topology, asset coordinates, and live sensor overlays to a backend digital-twin data source.
```

### app/pages/2_Assets.py

**File path:** `app/pages/2_Assets.py`

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

### app/pages/3_Control_Center.py

**File path:** `app/pages/3_Control_Center.py`

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

### app/pages/4_Incident_Simulator.py

**File path:** `app/pages/4_Incident_Simulator.py`

```python

import sys
from pathlib import Path

import streamlit as st



ROOT_DIR = Path(__file__).resolve().parents[1]
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
    service = IncidentService(simulator)
    simulator_result = service.trigger_incident(incident_type)
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

### app/pages/6_Agent_Monitor.py

**File path:** `app/pages/6_Agent_Monitor.py`

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

### app/pages/7_Reports.py

**File path:** `app/pages/7_Reports.py`

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

### app/pages/8_Settings.py

**File path:** `app/pages/8_Settings.py`

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

### app/pages/9_AI_Assistant.py

**File path:** `app/pages/9_AI_Assistant.py`

```python
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

# TODO: Route chat through an approved MAO chat/workflow endpoint when exposed.
# Never send Gemini keys to Streamlit or create a second MAOKernel here.
```

### app/ui_helpers.py

**File path:** `app/ui_helpers.py`

```python
"""Shared presentation and placeholder-data utilities for the Streamlit UI.

This module deliberately has no backend imports so each page remains runnable while
the Operations Center integration layer is being designed.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from random import Random

import streamlit as st

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
        .agent-card {

            padding:18px;
            border-radius:14px;
            background:rgba(255,255,255,0.05);
            border:1px solid rgba(255,255,255,0.15);
            margin-bottom:15px;

        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
    # TODO: Replace direct agent invocation when the backend exposes an approved
    # MAO chat/workflow endpoint connected to the running orchestration process.


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

### mao/models/result.py

**File path:** `mao/models/result.py`

```python
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class AgentResult:

    agent_name: str

    success: bool

    finding: str = ""

    confidence: float = 0.0

    evidence: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    required_action: str = ""

    requires_human_approval: bool = True

    metadata: Dict = field(default_factory=dict)

    summary: str = ""
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

### mao/workflows/gas_workflow.py

**File path:** `mao/workflows/gas_workflow.py`

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

### mao/workflows/maintenance_workflow.py

**File path:** `mao/workflows/maintenance_workflow.py`

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
"""
rag/embedder.py

Gemini Embedding Manager for RigOS

This module replaces the previous HuggingFace embedding model with
Google's Gemini embedding model (text-embedding-004).

The public API intentionally remains the same:

    embedder = Embedder()
    model = embedder.get_model()

so existing code such as VectorStore and Retriever continues to work.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

logger = logging.getLogger(__name__)

load_dotenv()


class Embedder:
    """
    Singleton wrapper around Google's Gemini embedding model.

    Compatible with:
        - FAISS
        - LangChain VectorStore
        - Retriever
        - Existing RigOS code

    Example
    -------
        embedder = Embedder()
        embeddings = embedder.get_model()
    """

    _model: Optional[GoogleGenerativeAIEmbeddings] = None

    API_KEY_ENVIRONMENTS = (
        "GOOGLE_API_KEY_1",
        "GOOGLE_API_KEY_2",
        "GOOGLE_API_KEY",
        "GEMINI_API_KEY_1",
        "GEMINI_API_KEY_2",
        "GEMINI_API_KEY",
    )

    def __init__(self):
        if Embedder._model is None:
            self._initialize()

    def _initialize(self) -> None:
        """
        Initialize Gemini embeddings once.
        """

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

        logger.info(
            "Initializing Gemini embeddings using %s",
            selected_variable,
        )

        Embedder._model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key,
        )

        logger.info("Gemini embeddings initialized successfully.")

    def get_model(self) -> GoogleGenerativeAIEmbeddings:
        """
        Returns the embedding model.

        This preserves compatibility with the previous implementation.

        Returns
        -------
        GoogleGenerativeAIEmbeddings
        """

        if Embedder._model is None:
            self._initialize()

        return Embedder._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple documents.
        """

        return self.get_model().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """
        Embed a single query.
        """

        return self.get_model().embed_query(text)

    def __repr__(self) -> str:
        return "Embedder(model='models/text-embedding-004')"
```

### rag/ingestion.py

**File path:** `rag/ingestion.py`

```python

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

### rag/reranker.py

**File path:** `rag/reranker.py`

```python

```

### rag/retriever.py

**File path:** `rag/retriever.py`

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

### run.py

**File path:** `run.py`

```python

```

### scripts/benchmark.py

**File path:** `scripts/benchmark.py`

```python

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

### scripts/test_mao.py

**File path:** `scripts/test_mao.py`

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

### scripts/test_models.py

**File path:** `scripts/test_models.py`

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

### scripts/test_rag.py

**File path:** `scripts/test_rag.py`

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

### services/__init__.py

**File path:** `services/__init__.py`

```python

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

Creates and caches the global MAO kernel instance.

The kernel is initialized only once and all production workflows
are registered automatically.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from mao import MAOKernel
from mao.workflows.flow_workflow import FlowWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.temperature_workflow import TemperatureWorkflow

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def create_kernel() -> MAOKernel:
    """
    Create and return the singleton MAO kernel.

    The kernel is cached so the entire application
    shares a single workflow registry.
    """

    logger.info("Initializing MAO Kernel...")

    kernel = MAOKernel()

    workflows = [
        PressureWorkflow(),
        TemperatureWorkflow(),
        GasWorkflow(),
        FlowWorkflow(),
        MaintenanceWorkflow(),
    ]

    for workflow in workflows:
        kernel.register_workflow(workflow)
        logger.info(
            "Registered workflow: %s",
            workflow.__class__.__name__,
        )

    logger.info(
        "MAO Kernel initialized with %d workflows.",
        len(workflows),
    )

    return kernel
```

### services/llm.py

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

### services/sensor.py

**File path:** `services/sensor.py`

```python

```

### services/simulation.py

**File path:** `services/simulation.py`

```python

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
            name="Diagnosis",
            description="Run diagnostics",
            assigned_agent="diagnostic",
            priority=2,
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
