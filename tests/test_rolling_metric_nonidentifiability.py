from market_microcosm.rolling_metric_nonidentifiability import (
    ambiguity_summary,
    rolling_metric_nonidentifiability_report_payload,
)


def test_same_arr_has_many_monotone_latent_paths() -> None:
    row = ambiguity_summary()

    assert row["reported_arr"] == 60
    assert row["path_count"] == 338
    assert row["possible_current_mrr_values"] == [0, 1, 2, 3, 4, 5]


def test_same_metric_can_mean_dead_or_still_active() -> None:
    row = ambiguity_summary()

    assert row["minimum_current_mrr"] == 0
    assert row["maximum_current_mrr"] == 5


def test_e040_promotion_contract() -> None:
    payload = rolling_metric_nonidentifiability_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_identifiability_rule"] == (
        "rolling-kpi-current-state-nonidentifiable-without-path-state-v1"
    )
