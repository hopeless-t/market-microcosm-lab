from market_microcosm.metric_definition_drift import (
    gamepass_membership_history,
    growth_authority_check,
    metric_definition_drift_report_payload,
    naive_headline_growth,
)


def test_naive_headline_ratio_is_quarantined() -> None:
    row = naive_headline_growth()

    assert abs(row["naive_growth_fraction"] - 0.36) < 1e-12
    assert row["authority"] == "illustrative_only"


def test_gamepass_headlines_are_not_growth_authorized() -> None:
    earlier, later = gamepass_membership_history()
    row = growth_authority_check(earlier, later)

    assert row["authorized"] is False
    assert row["same_definition"] is False
    assert row["exact_points"] is False
    assert "definition_generation_mismatch" in row["rejection_reasons"]
    assert "non_exact_value_semantics" in row["rejection_reasons"]


def test_e027_promotion_contract() -> None:
    payload = metric_definition_drift_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_metric_rule"] == (
        "metric-definition-version-required-for-time-series-growth-v1"
    )
