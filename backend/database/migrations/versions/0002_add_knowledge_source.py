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
