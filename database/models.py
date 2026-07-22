from sqlalchemy import Column, String, Float, Text, DateTime, Boolean
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
    report = Column(Text)

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
        Vector(384)
    )

class AgentExecutionDB(Base):

    __tablename__ = "agent_execution"


    id = Column(
        String,
        primary_key=True
    )

    agent_name = Column(String)

    task = Column(String)

    success = Column(Boolean)

    confidence = Column(Float)

    summary = Column(Text)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )