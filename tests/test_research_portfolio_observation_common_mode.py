from market_microcosm.research_portfolio_observation_common_mode import rpe010_report_payload


def test_rpe010_observation_common_mode_contract() -> None:
    payload = rpe010_report_payload()
    assert payload["experiment"] == "RPE-010"
    assert all(payload["promotion_gate"].values())

    nominal = payload["policies"]["nominal_value_first"]
    hidden = payload["policies"]["hidden_common_mode_value_first"]
    aware = payload["policies"]["hidden_topology_dependency_aware"]

    assert nominal["effective_failure_domain_count"] == 2
    assert nominal["minimum_domain_shocks_to_forge_healthy"] == 2
    assert nominal["exact_forge_probability"] == 0.0001

    assert hidden["effective_failure_domain_count"] == 1
    assert hidden["minimum_domain_shocks_to_forge_healthy"] == 1
    assert hidden["exact_forge_probability"] == 0.01

    assert aware["effective_failure_domain_count"] == 2
    assert aware["minimum_domain_shocks_to_forge_healthy"] == 2
    assert aware["exact_forge_probability"] == 0.0001

    assert payload["comparison"]["forge_probability_inflation_factor"] == 100.0
    assert payload["fixture"]["hidden_common_mode_value_at_risk"] == 17
    assert payload["claim_ceiling"].startswith("EXACT_SYNTHETIC")
