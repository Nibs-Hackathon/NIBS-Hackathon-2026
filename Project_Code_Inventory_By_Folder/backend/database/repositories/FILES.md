# Folder: backend/database/repositories Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/database/repositories`

Contains 8 project file(s) directly in this folder (nested folders have their own inventory files).

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
