from types import SimpleNamespace

from api.adapters import maintenance_adapter


class _AssetService:
    @staticmethod
    def get(asset_id):
        return SimpleNamespace(
            id=asset_id,
            name="Pump A-01",
            location="North Terminal Refinery",
            asset_type=SimpleNamespace(value="Pump"),
        )


def test_local_demo_work_order_lifecycle(monkeypatch):
    monkeypatch.setattr(maintenance_adapter, "local_demo_mode", lambda: True)
    monkeypatch.setattr(
        maintenance_adapter,
        "runtime",
        SimpleNamespace(kernel=SimpleNamespace(asset_service=_AssetService())),
    )
    maintenance_adapter._DEMO_WORK_ORDERS.clear()

    created = maintenance_adapter.create_work_order(
        asset_id="asset-1",
        incident_id="incident-1",
        title="Inspect Pump A-01",
        priority="P1",
        owner="Control operator",
    )

    assert created["status"] == "pending_approval"
    rows = maintenance_adapter._persisted_work_orders()
    assert len(rows) == 1
    assert rows[0]["id"] == created["id"]
    assert rows[0]["State"] == "Ready"
    assert rows[0]["Asset"] == "Pump A-01"

    approved = maintenance_adapter.approve_work_order(
        created["id"],
        operator="Maintenance lead",
        note="Approved for the next shift.",
    )

    assert approved["status"] == "approved"
    rows = maintenance_adapter._persisted_work_orders()
    assert rows[0]["State"] == "Scheduled"
    assert rows[0]["approved_by"] == "Maintenance lead"
    assert rows[0]["approval_note"] == "Approved for the next shift."
