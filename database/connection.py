import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

sessionlocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind = engine
)

def get_session():
    return sessionlocal()
