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
