from market_microcosm.research_portfolio_signal_guard import rpe004_report_payload


def test_rpe004_signal_guard_contract() -> None:
    payload = rpe004_report_payload()
    assert payload["experiment"] == "RPE-004"
    assert all(payload["promotion_gate"].values())

    policies = payload["policies"]
    naive = policies["naive_any_signal"]
    filtered = policies["confidence_filtered"]
    always_warm = policies["always_warm_rare"]
    hybrid = policies["certified_hybrid"]

    assert naive["aggregate_resource_cost"] == 604.0
    assert naive["aggregate_captured_value"] == 1149

    assert filtered["aggregate_resource_cost"] == 596.0
    assert filtered["aggregate_captured_value"] == 1149

    assert always_warm["aggregate_resource_cost"] == 685.0
    assert always_warm["aggregate_value_coverage"] == 1.0

    assert hybrid["aggregate_resource_cost"] == 593.0
    assert hybrid["aggregate_captured_value"] == 1185
    assert hybrid["aggregate_value_coverage"] == 1.0

    assert payload["comparison"]["naive_value_loss_pct"] > 0.0
    assert payload["comparison"]["hybrid_cost_reduction_vs_always_warm_pct"] > 10.0
    assert payload["claim_ceiling"].startswith("DETERMINISTIC_SYNTHETIC")
