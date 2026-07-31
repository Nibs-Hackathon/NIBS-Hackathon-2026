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