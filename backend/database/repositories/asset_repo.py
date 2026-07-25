"""Optimized Asset Repository with batch operations."""

from database.models import AssetDB
from sqlalchemy import text
from typing import List, Optional


class AssetRepository:
    def __init__(self, session):
        self.session = session

    def create(self, asset):
        self.session.add(asset)
        self.session.commit()
        return asset

    def create_batch(self, assets: List[AssetDB]) -> List[AssetDB]:
        """Batch insert for better performance."""
        self.session.add_all(assets)
        self.session.commit()
        return assets

    def get_all(self):
        return self.session.query(AssetDB).all()

    def get(self, asset_id):
        return self.session.query(AssetDB).filter_by(id=asset_id).first()

    def bulk_update_health(self, updates: dict):
        """Bulk update asset health in one query."""
        if not updates:
            return
        
        case_parts = []
        id_list = []
        for asset_id, health in updates.items():
            case_parts.append(f"WHEN '{asset_id}' THEN {health}")
            id_list.append(f"'{asset_id}'")
        
        if not case_parts:
            return
        
        stmt = f"""
            UPDATE assets 
            SET health = CASE id {' '.join(case_parts)} END,
                status = CASE 
                    WHEN health >= 80 THEN 'Running'
                    WHEN health >= 50 THEN 'Warning'
                    ELSE 'Critical'
                END
            WHERE id IN ({','.join(id_list)})
        """
        
        self.session.execute(text(stmt))
        self.session.commit()