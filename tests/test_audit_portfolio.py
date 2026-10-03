from market_microcosm.audit_portfolio import (
    AuditItem,
    audit_portfolio_report_payload,
    dp_schedule,
    exhaustive_schedule,
    greedy_schedule,
    greedy_trap_portfolio,
    infeasible_mandatory_portfolio,
)


def test_dp_matches_exhaustive_on_simple_portfolio() -> None:
    items = (
        AuditItem("a", 2, 40),
        AuditItem("b", 3, 55),
        AuditItem("c", 4, 70),
    )
    oracle = exhaustive_schedule(items, budget_units=5)
    dp = dp_schedule(items, budget_units=5)
    assert dp.selected_names == oracle.selected_names
    assert dp.total_restoration_value == oracle.total_restoration_value


def test_greedy_trap_is_real() -> None:
    items = greedy_trap_portfolio()
    oracle = exhaustive_schedule(items, budget_units=50)
    greedy = greedy_schedule(items, budget_units=50)
    assert oracle.total_restoration_value == 220
    assert greedy.total_restoration_value == 160


def test_mandatory_over_budget_fails_closed() -> None:
    items = infeasible_mandatory_portfolio()
    for result in (
        exhaustive_schedule(items, budget_units=10),
        dp_schedule(items, budget_units=10),
        greedy_schedule(items, budget_units=10),
    ):
        assert result.feasible is False
        assert result.fail_closed is True


def test_e018_promotion_contract() -> None:
    payload = audit_portfolio_report_payload()
    assert payload["promoted_scheduler"] == "bounded-dp"
    assert all(payload["promotion_gate"].values())
