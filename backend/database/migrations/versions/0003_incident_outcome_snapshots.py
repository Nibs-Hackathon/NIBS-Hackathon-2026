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
