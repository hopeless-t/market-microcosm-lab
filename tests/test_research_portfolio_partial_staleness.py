from market_microcosm.research_portfolio_partial_staleness import rpe008_report_payload


def test_rpe008_partial_staleness_contract() -> None:
    payload = rpe008_report_payload()
    assert payload["experiment"] == "RPE-008"
    assert all(payload["promotion_gate"].values())

    policies = payload["policies"]
    whole = policies["observe_whole_object"]
    oldest = policies["oldest_first"]
    density = policies["mandatory_then_value_density"]
    hazard = policies["hazard_aware_exact_budget"]
    oracle = policies["hidden_staleness_oracle"]

    assert whole["observation_cost"] == 13
    assert whole["budget_feasible"] is False

    assert oldest["observation_cost"] == 6
    assert oldest["restored_decision_value"] == 8
    assert oldest["mandatory_observed"] is False

    assert density["observation_cost"] == 7
    assert density["restored_decision_value"] == 22
    assert density["fresh_observation_waste_cost"] == 2

    assert hazard["selected"] == [
        "authority-contract",
        "cost-model",
        "dependency-map",
    ]
    assert hazard["restored_decision_value"] == 29
    assert hazard["restored_value_coverage"] == 29 / 30
    assert hazard["selected"] == oracle["selected"]
    assert payload["claim_ceiling"].startswith("EXACT_SMALL_SYNTHETIC")
