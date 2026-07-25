"""FastAPI backend for RigOS."""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sys
from pathlib import Path
import asyncio
from datetime import datetime
from uuid import uuid4
import time
import os
from dotenv import load_dotenv
DATABASE_URL = os.getenv("DATABASE_URL")

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


class AssistantQuery(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class OperatorActionRequest(BaseModel):
    """Human decision recorded against an incident or AI recommendation."""

    incident_id: str | None = None
    asset_id: str | None = None
    action_type: str = Field(min_length=2, max_length=80)
    decision: str = Field(pattern="^(approved|rejected|escalated|evidence_requested)$")
    operator: str = Field(default="Chief Operator", min_length=2, max_length=120)
    risk_level: str = Field(default="MEDIUM", max_length=30)
    note: str | None = Field(default=None, max_length=2000)

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


@app.get(
    "/api/metadata",
    tags=["Platform metadata"],
    summary="Describe the live RigOS capability contract",
)
async def platform_metadata():
    """Small, UI-consumable documentation payload for environments and demos."""
    return {
        "product": "RigOS",
        "api_version": "1.1.0",
        "capabilities": {
            "multi_agent_investigation": True,
            "rag_assistant": True,
            "websocket_updates": True,
            "persistent_operator_actions": True,
            "modelled_production_value": True,
        },
        "contracts": {
            "operations_live": "/api/operations/live",
            "assistant": "/api/assistant/query",
            "operator_action": "/api/operator-actions",
            "database_health": "/api/health/database",
        },
        "notes": {
            "revenue_projection": "Modelled production value based on current asset availability and health; not booked revenue.",
            "operator_actions": "Decisions are persisted to the existing actions table when PostgreSQL is available.",
        },
    }


@app.post(
    "/api/operator-actions",
    tags=["Operator decisions"],
    summary="Persist an operator approval, rejection, escalation, or evidence request",
)
async def record_operator_action(payload: OperatorActionRequest):
    """Use the existing ActionDB audit table; never execute industrial equipment here."""
    try:
        from database.connection import get_session
        from database.models import ActionDB

        session = get_session()
        try:
            status = "approved" if payload.decision == "approved" else payload.decision
            action = ActionDB(
                id=str(uuid4()),
                incident_id=payload.incident_id,
                asset_id=payload.asset_id,
                action_type=payload.action_type,
                payload={"decision": payload.decision, "note": payload.note},
                risk_level=payload.risk_level.upper(),
                status=status,
                requires_human_approval=False,
                requested_by="MAO",
                approved_by=payload.operator if payload.decision == "approved" else None,
                executed_at=datetime.utcnow() if payload.decision == "approved" else None,
            )
            session.add(action)
            session.commit()
            return {
                "id": action.id,
                "status": action.status,
                "decision": payload.decision,
                "recorded_at": action.created_at.isoformat() if action.created_at else None,
                "message": "Operator decision recorded. No industrial command was executed.",
            }
        finally:
            session.close()
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "OPERATOR_ACTION_STORAGE_UNAVAILABLE",
                "message": "The operator decision could not be persisted. Check PostgreSQL connectivity.",
                "error_type": type(error).__name__,
            },
        ) from error

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


@app.get("/api/operations/live")
async def get_operations_live():
    """Aggregated Operations Center snapshot; existing page APIs remain unchanged."""
    try:
        from api.adapters.operations_adapter import get_operations_live as operations_live
        return operations_live()
    except Exception as e:
        print(f"⚠️ Error fetching operations snapshot: {e}")
        return {"generated_at": datetime.now().isoformat(), "dashboard": {}, "assets": []}


@app.get("/api/incidents/audit")
async def get_incident_audit(limit: int = 100):
    try:
        from api.adapters.operations_adapter import get_incident_audit as incident_audit
        return incident_audit(limit=max(1, min(limit, 500)))
    except Exception as e:
        print(f"⚠️ Error fetching incident audit: {e}")
        return []


@app.get("/api/incidents/audit/{incident_id}")
async def get_incident_audit_detail(incident_id: str):
    from fastapi import HTTPException
    try:
        from api.adapters.operations_adapter import get_incident_audit_detail as incident_detail
        audit = incident_detail(incident_id)
        if audit is None:
            raise HTTPException(status_code=404, detail="Incident audit record not found")
        return audit
    except HTTPException:
        raise
    except Exception as e:
        print(f"⚠️ Error fetching incident audit detail: {e}")
        raise HTTPException(status_code=500, detail="Unable to load incident audit record") from e


@app.post("/api/assistant/query")
async def query_assistant(payload: AssistantQuery):
    """Route the global assistant through the existing Knowledge Agent/RAG path."""
    try:
        from api.adapters.knowledge_agent_adapter import ask_knowledge_agent
        answer = await run_in_threadpool(ask_knowledge_agent, payload.question)
        return {"answer": answer}
    except Exception as e:
        print(f"⚠️ Assistant query failed: {e}")
        return {"answer": "RigOS Assistant is temporarily unavailable. Please try again shortly.", "degraded": True}


@app.get("/api/health/database")
async def database_health():
    """Diagnose database reachability without exposing the configured DSN."""
    try:
        from sqlalchemy import text
        from database.connection import engine

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "unavailable",
            "error_type": type(error).__name__,
            "message": str(error).split("\n", 1)[0][:300],
        }

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
                from api.adapters.operations_adapter import get_operations_live as operations_live
                snapshot = await run_in_threadpool(operations_live)
                
                await websocket.send_json({
                    "type": "update",
                    "data": snapshot
                })
                
            except (WebSocketDisconnect, RuntimeError):
                break
            except Exception as e:
                print(f"⚠️ WebSocket update error: {e}")
            
            await asyncio.sleep(2)
            
    except Exception as e:
        print(f"⚠️ WebSocket disconnected: {e}")
        manager.disconnect(websocket)
    finally:
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
        from api.adapters.operations_adapter import get_execution_reports
        return get_execution_reports()
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
