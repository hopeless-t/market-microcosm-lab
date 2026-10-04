from market_microcosm.post_exit_horizon_guard import (
    horizon_authority,
    post_exit_horizon_report_payload,
)


def test_short_horizon_profit_does_not_certify_h1_profit() -> None:
    row = horizon_authority()
    assert row["q1_positive_operating_profit"] is True
    assert row["h1_operating_profit_improvement_jpy_millions"] == 236
    assert row["h1_still_loss_making"] is True
    assert row["durable_profitability_certified"] is False


def test_e092_promotion_contract() -> None:
    payload = post_exit_horizon_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_horizon_rule"] == (
        "one-quarter-profit-sign-flip-does-not-certify-durable-profitability-v1"
    )
