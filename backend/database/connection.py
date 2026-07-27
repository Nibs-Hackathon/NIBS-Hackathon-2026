"""Optimized database connection with pooling and query caching."""

import os
from pathlib import Path
from contextlib import contextmanager
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Prefer committed-local secrets file first, then optional overrides.
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / ".env.local", override=True)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
LOCAL_DEMO_MODE = os.getenv("LOCAL_DEMO_MODE", "").strip().lower() in {"1", "true", "yes", "on"}

# Keep database imports valid in isolated demo mode without contacting a real
# provider. Persistence and database-backed reads are disabled elsewhere.
if LOCAL_DEMO_MODE:
    DATABASE_URL = "postgresql+psycopg2://demo:demo@127.0.0.1:1/rigos_demo"

# Some hosted PostgreSQL providers still publish the legacy postgres:// scheme.
# SQLAlchemy 2 requires the explicit psycopg2 dialect for those URLs.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = None
SessionLocal = None
db_session = None

if DATABASE_URL:
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
        bind=engine,
    )
    db_session = scoped_session(SessionLocal)
else:
    print(
        "WARNING: DATABASE_URL is missing. Add it to backend/.env "
        "(copy from .env.example). Runtime will use in-memory fallbacks."
    )


def is_database_configured() -> bool:
    """True when DATABASE_URL was provided and a session factory exists."""
    return db_session is not None


def _require_session_factory():
    if db_session is None:
        raise RuntimeError(
            "DATABASE_URL is missing. Add it to backend/.env locally "
            "(see backend/.env.example) or set it in deployment secrets."
        )
    return db_session


@contextmanager
def get_session_context():
    """Context manager for database sessions with automatic cleanup."""
    session = _require_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session():
    """Return a database session."""
    return _require_session_factory()()


# ✅ Cache for frequently accessed data
_cache_data = {}
_cache_timestamps = {}
_CACHE_TTL = 5


def cached_query(key: str, func, *args, **kwargs):
    """Get cached data or compute it."""
    now = time.time()
    if key in _cache_data and (now - _cache_timestamps.get(key, 0)) < _CACHE_TTL:
        return _cache_data[key]
    result = func(*args, **kwargs)
    _cache_data[key] = result
    _cache_timestamps[key] = now
    return result


def clear_cache(key: str | None = None):
    """Clear one cache entry or the entire cache."""
    if key is None:
        _cache_data.clear()
        _cache_timestamps.clear()
        return
    _cache_data.pop(key, None)
    _cache_timestamps.pop(key, None)


def healthcheck() -> bool:
    """Return True when the database accepts a trivial query."""
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
