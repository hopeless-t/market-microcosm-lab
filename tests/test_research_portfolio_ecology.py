from market_microcosm.research_portfolio_ecology import (
    canonical_exact_budget,
    canonical_on_demand,
    direct_fanout,
    hard_one_projection_per_spark,
    rpe001_report_payload,
)


def test_rpe001_on_demand_preserves_demand_with_less_work() -> None:
    direct = direct_fanout()
    on_demand = canonical_on_demand()

    assert direct["demand_edge_coverage"] == 1.0
    assert on_demand["demand_edge_coverage"] == 1.0
    assert on_demand["review_cost"] < direct["review_cost"]
    assert direct["duplicate_materializations"] > 0
    assert on_demand["duplicate_materializations"] == 0


def test_rpe001_hard_cap_can_suppress_decision_relevant_work() -> None:
    hard_cap = hard_one_projection_per_spark()
    assert hard_cap["demand_edge_coverage"] < 1.0


def test_rpe001_budgeted_policy_is_bounded_and_keeps_canonical_option_value() -> None:
    budgeted = canonical_exact_budget(review_budget=30)
    assert budgeted["review_cost"] <= 30
    assert budgeted["canonical_meanings_retained"] == 7
    assert budgeted["canonical_dormant_meanings_retained"] == 1
    assert budgeted["decision_value_coverage"] > 0.70


def test_rpe001_promotion_contract() -> None:
    payload = rpe001_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["claim_ceiling"].startswith("DETERMINISTIC_SYNTHETIC_FIXTURE_ONLY")
