from market_microcosm.disclosure_selection_bias import (
    complete_case_benchmark,
    disclosure_selection_bias_report_payload,
    event_aware_benchmark,
)


def test_complete_case_filter_hides_deterioration_events() -> None:
    row = complete_case_benchmark()
    assert row["selected_count"] == 8
    assert row["excluded_count"] == 2
    assert row["observed_deterioration_rate"] == 0.0


def test_event_aware_population_retains_withdrawals_without_imputation() -> None:
    row = event_aware_benchmark()
    assert row["record_count"] == 10
    assert row["deterioration_event_rate"] == 0.2
    assert row["withdrawal_event_count"] == 2
    assert row["hidden_withdrawn_values_inferred"] is False


def test_e081_promotion_contract() -> None:
    payload = disclosure_selection_bias_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_selection_rule"] == (
        "benchmark-selection-must-retain-informative-kpi-withdrawal-events-v1"
    )
