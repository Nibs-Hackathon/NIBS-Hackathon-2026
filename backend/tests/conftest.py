import os
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

# Production validates its database configuration during module import. Tests
# replace persistence before constructing the kernel, but SQLAlchemy still
# needs a syntactically valid URL while those modules load. This unreachable
# local URL prevents tests from depending on developer or hosted credentials.
os.environ["DATABASE_URL"] = (
    "postgresql+psycopg2://test:test@127.0.0.1:1/rigos_test"
)
