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