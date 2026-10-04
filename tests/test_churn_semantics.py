from market_microcosm.churn_semantics import (
    churn_semantics_report_payload,
    endpoint_change,
)


def test_bbd_endpoint_is_churn_sign_counterexample() -> None:
    row = endpoint_change()

    assert row["churn_relative_change_pct"] > 100
    assert row["contracts_change_pct"] < -5
    assert row["arr_change_pct"] > 0
    assert row["arpa_change_pct"] > 5


def test_e030_promotion_contract() -> None:
    payload = churn_semantics_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_churn_rule"] == (
        "churn-must-be-layer-and-cause-typed-v1"
    )
    assert all(payload["sign_counterexample"].values())
