from types import SimpleNamespace

from api.adapters.knowledge_agent_adapter import _financial_context_answer, _live_context
from services import runtime as runtime_module


def _asset(asset_id, name, location="RigOS Alpha Refinery"):
    return SimpleNamespace(
        id=asset_id,
        name=name,
        location=location,
        health=100.0,
        status="Running",
        asset_type=SimpleNamespace(value="Valve"),
    )


def _install_runtime(monkeypatch):
    valve = _asset("valve-003", "Valve V-003")
    pump = _asset("pump-a01", "Pump A-01")
    assets = [valve, pump]
    kernel = SimpleNamespace(
        asset_service=SimpleNamespace(
            all_assets=lambda: assets,
            get=lambda asset_id: next(
                (asset for asset in assets if asset.id == asset_id),
                None,
            ),
        ),
        event_store=SimpleNamespace(all=lambda: []),
    )
    monkeypatch.setattr(
        runtime_module,
        "runtime",
        SimpleNamespace(
            kernel=kernel,
            active_simulator=SimpleNamespace(active_incidents={}),
        ),
    )
    return valve


def test_stale_selected_asset_does_not_scope_a_new_portfolio_question(monkeypatch):
    valve = _install_runtime(monkeypatch)

    lines = _live_context(
        "Are there any gas leaks?",
        valve.id,
        None,
        "Enterprise view",
        history=[{"text": "Earlier we inspected Valve V-003."}],
    )

    assert not any(line.startswith("Resolved asset:") for line in lines)
    assert "Active incidents in scope: none" in lines


def test_current_question_can_explicitly_resolve_selected_asset(monkeypatch):
    valve = _install_runtime(monkeypatch)

    lines = _live_context(
        "Is there a gas leak on Valve V-003?",
        valve.id,
        None,
        "Enterprise view",
    )

    assert any(line.startswith("Resolved asset: Valve V-003") for line in lines)
    assert any(
        line.startswith("Assertion check: no active GasLeak is recorded on Valve V-003")
        for line in lines
    )


def test_contextual_pronoun_can_use_selected_asset(monkeypatch):
    valve = _install_runtime(monkeypatch)

    lines = _live_context(
        "What is the condition of this asset?",
        valve.id,
        None,
        "Enterprise view",
    )

    assert any(line.startswith("Resolved asset: Valve V-003") for line in lines)


def test_live_context_includes_calculated_fleet_health(monkeypatch):
    _install_runtime(monkeypatch)

    lines = _live_context(
        "What is fleet health right now?",
        None,
        None,
        "Enterprise view",
    )

    assert any(
        line.startswith("Fleet health (average of published asset health): 100.0/100")
        for line in lines
    )
    assert "Assets in scope: 2" in lines


def test_portfolio_financial_question_aggregates_persisted_reports(monkeypatch):
    _install_runtime(monkeypatch)
    from api.adapters import operations_adapter

    monkeypatch.setattr(
        operations_adapter,
        "get_execution_reports",
        lambda limit=500: [
            {
                "incident_type": "GasLeak",
                "financial_impact": 1250,
                "maintenance_cost": 300,
                "production_impact": 8,
                "facility": "RigOS Alpha Refinery",
            },
            {
                "incident_type": "PressureSpike",
                "financial_impact": 750,
                "maintenance_cost": 100,
                "production_impact": 4,
                "facility": "RigOS Alpha Refinery",
            },
        ],
    )

    lines = _live_context(
        "What has impacted revenue and by how much?",
        None,
        None,
        "Enterprise view",
    )
    answer = _financial_context_answer(lines)

    assert any(
        line.startswith("Modeled portfolio report exposure: $2,000.00")
        for line in lines
    )
    assert any("GasLeak $1,250.00 across 1 incident(s)" in line for line in lines)
    assert "Modeled maintenance estimate total: $400.00." in lines
    assert answer is not None
    assert "$2,000.00 across 2 persisted incident report(s)" in answer


def test_specific_asset_exposure_takes_priority_over_portfolio_totals():
    answer = _financial_context_answer([
        "Resolved asset: Pump A-01 (pump-a01)",
        "Active incident on resolved asset: PressureSpike",
        "Modeled incident exposure (estimate, not booked loss): $425.00 over 2 hours.",
        "Modeled portfolio report exposure: $9,999.00 across 10 persisted incident report(s).",
    ])

    assert "$425.00 over 2 hours" in answer
    assert "$9,999.00" not in answer
