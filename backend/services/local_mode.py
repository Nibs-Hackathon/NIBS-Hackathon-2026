"""Shared switch for running RigOS without external providers."""

import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_ROOT / ".env")
load_dotenv(BACKEND_ROOT / ".env.local", override=True)


def local_demo_mode() -> bool:
    """Return whether the isolated, in-memory demo runtime is enabled."""
    return os.getenv("LOCAL_DEMO_MODE", "").strip().lower() in {"1", "true", "yes", "on"}
