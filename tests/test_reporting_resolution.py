from market_microcosm.reporting_resolution import (
    reporting_resolution_report_payload,
    standard_decay_prediction_interval,
)


def test_e038_point_error_is_below_chart_resolution() -> None:
    row = standard_decay_prediction_interval()

    assert row["point_absolute_error"] < 1.0
    assert row["point_relative_error"] < 0.01


def test_rounding_intervals_overlap() -> None:
    row = standard_decay_prediction_interval()

    assert row["intervals_overlap"] is True
    lo, hi = row["prediction_interval_from_rounding"]
    assert lo < 215.0
    assert hi > 216.0


def test_e042_revokes_overprecise_e038_interpretation() -> None:
    payload = reporting_resolution_report_payload()

    assert payload["legacy_e038_sub1pct_precision_authority"] == "REVOKED"
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_resolution_rule"] == (
        "empirical-claim-precision-cannot-exceed-reporting-resolution-v1"
    )
