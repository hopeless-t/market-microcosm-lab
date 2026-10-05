from market_microcosm.rolling_metric_lag import (
    abrupt_service_end_reference,
    rolling_metric_lag_report_payload,
)


def test_six_month_arr_window_smears_abrupt_end() -> None:
    row = abrupt_service_end_reference()
    month3 = row["three_month_post_shock"]

    assert row["immediate_true_post_shock_arr_equivalent"] == 0.0
    assert month3["reported_arr"] == 60.0
    assert month3["legacy_signal_fraction"] == 0.5


def test_metric_memory_expires_after_full_window() -> None:
    row = abrupt_service_end_reference()
    month6 = row["six_month_post_shock"]

    assert month6["reported_arr"] == 0.0
    assert month6["legacy_signal_fraction"] == 0.0


def test_e039_promotion_contract() -> None:
    payload = rolling_metric_lag_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_observation_rule"] == (
        "rolling-window-metric-lag-must-be-modeled-v1"
    )
