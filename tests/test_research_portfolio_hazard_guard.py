from market_microcosm.research_portfolio_hazard_guard import rpe009_report_payload


def test_rpe009_hazard_channel_contract() -> None:
    payload = rpe009_report_payload()
    assert payload["experiment"] == "RPE-009"
    assert all(payload["promotion_gate"].values())

    naive = payload["policies"]["hazard_only"]
    guarded = payload["policies"]["health_guarded_hazard"]
    naive_by_name = {row["scenario"]: row for row in naive["scenario_results"]}
    guarded_by_name = {row["scenario"]: row for row in guarded["scenario_results"]}

    assert naive_by_name["healthy"]["restored_decision_value"] == 29
    assert naive_by_name["false-positive-workflow"]["restored_decision_value"] == 22
    assert naive_by_name["false-negative-dependency"]["restored_decision_value"] == 20
    assert naive_by_name["combined"]["restored_decision_value"] == 19

    assert guarded["aggregate_restored_decision_value"] == 116
    assert guarded["aggregate_possible_stale_value"] == 120
    assert guarded["aggregate_fresh_waste_cost"] == 0
    assert all(row["restored_decision_value"] == 29 for row in guarded["scenario_results"])
    assert "dependency-map" in guarded_by_name["combined"]["selected"]
    assert "workflow-shape" not in guarded_by_name["combined"]["selected"]
    assert payload["claim_ceiling"].startswith("DETERMINISTIC_SYNTHETIC")
