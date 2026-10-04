from market_microcosm.warning_monte_carlo import (
    generate_warning_states,
    monte_carlo_warning_report_payload,
    select_thresholds,
)


def test_threshold_search_is_deterministic() -> None:
    discovery = generate_warning_states(seed=32035, count=500)
    row = select_thresholds(discovery)

    assert row["candidate_count"] >= 300
    assert row["selected_thresholds"] == {
        "cash_coverage_ratio": 1.0,
        "fully_loaded_margin": 0.05,
        "market_headroom": 0.15,
        "downstream_success_ratio": 0.1,
        "strategic_exit_value_gap": 0.0,
    }


def test_e036_holdout_generalization_contract() -> None:
    payload = monte_carlo_warning_report_payload()
    multi = payload["holdout_scores"]["multi_signal"]

    assert multi["recall"] > 0.98
    assert multi["precision"] > 0.98
    assert multi["f1"] > 0.98
    assert payload["holdout_scores"]["revenue_only"]["recall"] < 0.25
    assert payload["holdout_scores"]["churn_only"]["recall"] < 0.30
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_warning_search_rule"] == (
        "discovery-tuned-multi-signal-warning-with-holdout-v1"
    )
