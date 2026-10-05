from market_microcosm.strategic_exit import (
    ExitDecisionState,
    preferred_action,
    strategic_exit_report_payload,
)


def test_positive_cash_can_still_have_strategic_exit() -> None:
    state = ExitDecisionState(
        cash=100.0,
        expected_monthly_net=-10.0,
        horizon_months=12,
        redeployment_value=50.0,
        sunset_cost=10.0,
    )

    assert state.cash > 0
    assert preferred_action(state) == "strategic_exit"


def test_profitable_continuation_can_beat_exit() -> None:
    state = ExitDecisionState(
        cash=10.0,
        expected_monthly_net=10.0,
        horizon_months=12,
        redeployment_value=0.0,
        sunset_cost=10.0,
    )

    assert preferred_action(state) == "continue"


def test_e029_promotion_contract() -> None:
    payload = strategic_exit_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_exit_rule"] == (
        "separate-strategic-exit-from-insolvency-v1"
    )
    assert (
        payload["finite_decision_grid"][
            "positive_cash_strategic_exit_count"
        ]
        > 0
    )
