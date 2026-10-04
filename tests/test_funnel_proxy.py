from market_microcosm.funnel_proxy import (
    attenuation_metrics,
    finite_funnel_proxy_witness,
    funnel_proxy_report_payload,
)


def test_empirical_funnel_attenuation_is_large() -> None:
    rows = attenuation_metrics()

    assert rows[0]["downstream_to_upstream_attainment_ratio"] < 0.15
    assert rows[1]["downstream_to_upstream_attainment_ratio"] < 0.30


def test_upstream_volume_can_reverse_customer_outcome_ranking() -> None:
    row = finite_funnel_proxy_witness()

    assert row["upstream_metric_winner"] == "volume_optimizer"
    assert row["customer_outcome_winner"] == "quality_optimizer"
    assert row["ranking_reversal"] is True


def test_e033_promotion_contract() -> None:
    payload = funnel_proxy_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_funnel_rule"] == (
        "upstream-kpi-cannot-certify-downstream-value-v1"
    )
