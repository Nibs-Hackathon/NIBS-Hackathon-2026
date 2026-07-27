"""Asset note persistence helpers."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4


def list_asset_notes(asset_id: str) -> list[dict]:
    from database.connection import get_session
    from database.models import AssetNoteDB

    session = get_session()
    try:
        rows = (
            session.query(AssetNoteDB)
            .filter(AssetNoteDB.asset_id == asset_id)
            .order_by(AssetNoteDB.updated_at.desc())
            .limit(50)
            .all()
        )
        return [
            {
                "id": row.id,
                "asset_id": row.asset_id,
                "note": row.note,
                "operator": row.operator,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
            }
            for row in rows
        ]
    finally:
        session.close()


def upsert_asset_note(asset_id: str, note: str, operator: str = "Control operator") -> dict:
    """Replace the latest note for an asset (single active note per asset for UI)."""
    from database.connection import get_session
    from database.models import AssetNoteDB

    text = str(note or "").strip()
    session = get_session()
    try:
        existing = (
            session.query(AssetNoteDB)
            .filter(AssetNoteDB.asset_id == asset_id)
            .order_by(AssetNoteDB.updated_at.desc())
            .first()
        )
        if existing:
            existing.note = text
            existing.operator = operator
            existing.updated_at = datetime.utcnow()
            session.add(existing)
            session.commit()
            row = existing
        else:
            row = AssetNoteDB(
                id=str(uuid4()),
                asset_id=asset_id,
                note=text,
                operator=operator,
            )
            session.add(row)
            session.commit()
        return {
            "id": row.id,
            "asset_id": row.asset_id,
            "note": row.note,
            "operator": row.operator,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }
    finally:
        session.close()
