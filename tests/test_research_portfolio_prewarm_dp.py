from market_microcosm.research_portfolio_prewarm_dp import rpe006_report_payload


def test_rpe006_bounded_dp_contract() -> None:
    payload = rpe006_report_payload()
    assert payload["experiment"] == "RPE-006"
    assert all(payload["promotion_gate"].values())

    suite = payload["suite"]
    assert suite["portfolio_count"] == 32
    assert suite["jobs_per_portfolio"] == 10
    assert suite["exact_value_match_rate"] == 1.0
    assert suite["exact_selection_match_rate"] == 1.0
    assert suite["oracle_work_units"] == 32768
    assert suite["dp_work_units"] == 11744
    assert suite["aggregate_work_reduction_fraction"] == 0.6416015625
    assert suite["minimum_per_portfolio_work_reduction_fraction"] == 0.515625
    assert payload["candidate_scheduler"] == "bounded-slot-mask-dp"
    assert payload["claim_ceiling"].startswith("DETERMINISTIC_GENERATED_SMALL_WORLDS")
