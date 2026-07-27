"""Development-only schema bootstrap. Production uses Alembic migrations."""

from sqlalchemy import text

from database.base import Base
from database.connection import engine
from database import models  # noqa: F401


def _ensure_vector_extension() -> bool:
    """Return True when pgvector is available for the knowledge table."""
    if engine is None:
        return False
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        return True
    except Exception as exc:
        print(f"WARNING: pgvector unavailable ({exc.__class__.__name__}). Skipping knowledge table.")
        return False


def create_schema():
    if engine is None:
        print("WARNING: Skipping schema bootstrap; DATABASE_URL is not configured.")
        return

    has_vector = _ensure_vector_extension()
    tables = list(Base.metadata.sorted_tables)
    if not has_vector:
        tables = [table for table in tables if table.name != "knowledge"]

    Base.metadata.create_all(engine, tables=tables)
