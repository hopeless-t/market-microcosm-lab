from market_microcosm.research_portfolio_residency import rpe003_report_payload


def test_rpe003_residency_contract() -> None:
    payload = rpe003_report_payload()
    assert payload["experiment"] == "RPE-003"
    assert all(payload["promotion_gate"].values())

    policies = payload["policies"]
    always_hot = policies["always_hot"]
    all_dormant = policies["all_dormant"]
    static = policies["static_tiering"]
    recency = policies["recency_only"]
    signal = policies["signal_aware_prewarm"]

    assert always_hot["captured_value"] == 237
    assert always_hot["value_coverage"] == 1.0
    assert always_hot["total_resource_cost"] == 288.0

    assert all_dormant["captured_value"] == 0
    assert all_dormant["missed_events"] > 0

    assert static["captured_value"] == 213
    assert static["total_resource_cost"] == 123.0

    assert signal["captured_value"] == 237
    assert signal["missed_events"] == 0
    assert signal["total_resource_cost"] == 117.0

    assert recency["captured_value"] < signal["captured_value"]
    assert payload["comparison"]["signal_cost_reduction_vs_always_hot_pct"] > 50.0
    assert payload["claim_ceiling"].startswith("DETERMINISTIC_SYNTHETIC")
