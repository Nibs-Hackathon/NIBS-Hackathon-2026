# Folder: backend/database Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `backend/database`

Contains 7 project file(s) directly in this folder (nested folders have their own inventory files).

## backend/database/__init__.py

**Folder path:** `backend/database`

**File path:** `backend/database/__init__.py`

```python
from database.base import Base
from database.connection import engine

from database import models
```

## backend/database/__init__database.py

**Folder path:** `backend/database`

**File path:** `backend/database/__init__database.py`

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

## backend/database/base.py

**Folder path:** `backend/database`

**File path:** `backend/database/base.py`

```python
from sqlalchemy.orm import declarative_base


Base = declarative_base()
```

## backend/database/bootstrap.py

**Folder path:** `backend/database`

**File path:** `backend/database/bootstrap.py`

```python
"""Development-only schema bootstrap. Production uses Alembic migrations."""

from database.base import Base
from database.connection import engine
from database import models  # noqa: F401


def create_schema():
    Base.metadata.create_all(engine)
```

## backend/database/connection.py

**Folder path:** `backend/database`

**File path:** `backend/database/connection.py`

```python
"""Optimized database connection with pooling and query caching."""

import os
from pathlib import Path
from functools import lru_cache
from contextlib import contextmanager
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

# Some hosted PostgreSQL providers still publish the legacy postgres:// scheme.
# SQLAlchemy 2 requires the explicit psycopg2 dialect for those URLs.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Add it to .env locally or Streamlit Secrets.")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=15,
    # Keep control-room reads responsive when a local/remote database is offline.
    # Durable queries use an in-memory runtime fallback during transient outages.
    connect_args={"connect_timeout": 2},
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Scoped session for thread safety
db_session = scoped_session(SessionLocal)


@contextmanager
def get_session_context():
    """Context manager for database sessions with automatic cleanup."""
    session = db_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ✅ SIMPLE SESSION FUNCTION (returns a session, NOT a context manager)
def get_session():
    """Return a database session."""
    return db_session()


# ✅ Cache for frequently accessed data
_cache_data = {}
_cache_timestamps = {}
_CACHE_TTL = 5


def cached_query(key: str, func, *args, **kwargs):
    """Get cached data or compute it."""
    now = time.time()
    if key in _cache_data and now - _cache_timestamps.get(key, 0) < _CACHE_TTL:
        return _cache_data[key]
    
    result = func(*args, **kwargs)
    _cache_data[key] = result
    _cache_timestamps[key] = now
    return result


def invalidate_cache(key: str = None):
    """Invalidate cache for a key or all keys."""
    if key:
        _cache_data.pop(key, None)
        _cache_timestamps.pop(key, None)
    else:
        _cache_data.clear()
        _cache_timestamps.clear()


@lru_cache(maxsize=128)
def get_all_assets_cached():
    """Cache all assets for 5 seconds."""
    session = get_session()
    try:
        from database.models import AssetDB
        return session.query(AssetDB).all()
    finally:
        session.close()


def invalidate_asset_cache():
    """Invalidate the asset cache when new assets are added."""
    get_all_assets_cached.cache_clear()
```

## backend/database/models.py

**Folder path:** `backend/database`

**File path:** `backend/database/models.py`

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
    health_before = Column(Float)
    health_after = Column(Float)
    resolution_seconds = Column(Float)
    resolved_at = Column(DateTime)
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

## backend/database/seed_demo.py

**Folder path:** `backend/database`

**File path:** `backend/database/seed_demo.py`

```python

```
