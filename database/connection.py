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

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Add it to .env locally or Streamlit Secrets.")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
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