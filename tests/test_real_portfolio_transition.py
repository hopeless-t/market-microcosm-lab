from market_microcosm.real_portfolio_transition import (
    churn_direction_naive_predictor,
    portfolio_transition_report_payload,
    quarterly_transitions,
)


def test_same_churn_improvement_sign_has_opposite_arr_outcomes() -> None:
    rows = [
        row for row in quarterly_transitions()
        if row["churn_direction"] == "down"
    ]

    assert {row["arr_direction"] for row in rows} == {"up", "down"}


def test_q4_churn_improves_while_arr_and_arpa_decline() -> None:
    q4 = quarterly_transitions()[-1]

    assert q4["churn_direction"] == "down"
    assert q4["arr_direction"] == "down"
    assert q4["arpa_direction"] == "down"
    assert q4["contract_direction"] == "down"


def test_naive_churn_sign_predictor_fails_two_of_three() -> None:
    row = churn_direction_naive_predictor()

    assert row["correct_count"] == 1
    assert row["transition_count"] == 3
    assert row["accuracy"] == 1 / 3


def test_e063_promotion_contract() -> None:
    payload = portfolio_transition_report_payload()

    assert all(payload["promotion_gate"].values())
    assert payload["promoted_transition_rule"] == (
        "portfolio-transition-kpi-direction-requires-event-semantics-v1"
    )
