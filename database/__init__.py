from database.base import Base
from database.connection import engine

from database import models


print("Creating tables...")


Base.metadata.create_all(
    engine
)


print("Done")