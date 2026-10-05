from market_microcosm.post_exit_profitability import (
    allied_q1_comparison,
    post_exit_profitability_report_payload,
    scalar_evaluations,
)


def test_revenue_down_while_operating_profit_flips_positive() -> None:
    row = allied_q1_comparison()
    assert row["revenue_delta_jpy_millions"] == -18
    assert row["operating_profit_delta_jpy_millions"] == 245
    assert row["operating_profit_sign_flip"] is True


def test_scalar_health_rankings_conflict() -> None:
    row = scalar_evaluations()
    assert row["revenue_only"] == "WORSE"
    assert row["operating_profit_only"] == "BETTER"
    assert row["sign_conflict"] is True


def test_e090_promotion_contract() -> None:
    payload = post_exit_profitability_report_payload()
    assert all(payload["promotion_gate"].values())
    assert payload["promoted_exit_rule"] == (
        "strategic-exit-can-lower-revenue-while-improving-operating-profit-v1"
    )
