import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load local .env if available
load_dotenv(PROJECT_ROOT / ".env")


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Add it to .env locally or Streamlit Secrets."
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session():
    return SessionLocal()