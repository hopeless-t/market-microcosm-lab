from market_microcosm.cash_conversion_lag import (
    CashLagScenario,
    cash_conversion_lag_report_payload,
    minimum_initial_cash_for_survival,
    simulate_cash_lag,
)


def test_positive_booked_margin_can_fail_on_cash_timing() -> None:
    row = simulate_cash_lag(
        CashLagScenario(
            initial_cash=100.0,
            monthly_booked_revenue=100.0,
            monthly_cash_cost=80.0,
            collection_lag_months=2,
            horizon_months=6,
        )
    )

    assert row["booked_margin_positive"] is True
    assert row["failure_month"] == 2
    assert row["trace"][1]["cumulative_booked_profit"] == 40.0
    assert row["trace"][1]["cash"] == -60.0


def test_exact_minimum_liquidity_buffer() -> None:
    value = minimum_initial_cash_for_survival(
        monthly_booked_revenue=100.0,
        monthly_cash_cost=80.0,
        collection_lag_months=2,
        horizon_months=6,
    )
    assert value == 160


def test_e032_promotion_contract() -> None:
    payload = cash_conversion_lag_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_liquidity_rule"] == (
        "separate-booked-revenue-from-cash-arrival-v1"
    )
