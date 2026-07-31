# Folder: backend/database/migrations/versions Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/database/migrations/versions`

Contains 3 project file(s) directly in this folder (nested folders have their own inventory files).

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

## backend/database/migrations/versions/0003_incident_outcome_snapshots.py

**Folder path:** `backend/database/migrations/versions`

**File path:** `backend/database/migrations/versions/0003_incident_outcome_snapshots.py`

```python
"""Persist health and timing snapshots needed by the incident audit trail.

Revision ID: 0003_incident_outcome_snapshots
Revises: 0002_add_knowledge_source
Create Date: 2026-07-25
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_incident_outcome_snapshots"
down_revision = "0002_add_knowledge_source"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("incidents", sa.Column("health_before", sa.Float(), nullable=True))
    op.add_column("incidents", sa.Column("health_after", sa.Float(), nullable=True))
    op.add_column("incidents", sa.Column("resolution_seconds", sa.Float(), nullable=True))
    op.add_column("incidents", sa.Column("resolved_at", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("incidents", "resolved_at")
    op.drop_column("incidents", "resolution_seconds")
    op.drop_column("incidents", "health_after")
    op.drop_column("incidents", "health_before")
```
