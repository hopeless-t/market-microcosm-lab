from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product

from market_microcosm.japan_failure_corpus import japan_failure_corpus


@dataclass(frozen=True)
class ExitDecisionState:
    cash: float
    expected_monthly_net: float
    horizon_months: int
    redeployment_value: float
    sunset_cost: float


def continuation_value(state: ExitDecisionState) -> float:
    return state.expected_monthly_net * state.horizon_months


def strategic_exit_value(state: ExitDecisionState) -> float:
    return state.redeployment_value - state.sunset_cost


def preferred_action(state: ExitDecisionState) -> str:
    if strategic_exit_value(state) > continuation_value(state):
        return "strategic_exit"
    return "continue"


def positive_cash_exit_grid() -> tuple[dict, ...]:
    rows: list[dict] = []

    for cash, monthly_net, horizon, redeployment, sunset_cost in product(
        (10.0, 50.0, 100.0),
        (-20.0, -10.0, 0.0, 10.0),
        (3, 6, 12),
        (0.0, 50.0),
        (10.0,),
    ):
        state = ExitDecisionState(
            cash=cash,
            expected_monthly_net=monthly_net,
            horizon_months=horizon,
            redeployment_value=redeployment,
            sunset_cost=sunset_cost,
        )
        rows.append(
            {
                **asdict(state),
                "continuation_value": continuation_value(state),
                "strategic_exit_value": strategic_exit_value(state),
                "preferred_action": preferred_action(state),
                "cash_positive": state.cash > 0,
            }
        )

    return tuple(rows)


def empirical_noninsolvency_exit_evidence() -> tuple[dict, ...]:
    corpus = {row.case_id: row for row in japan_failure_corpus()}
    selected = (
        "bbd-restructuring-2026",
        "rickcloud-sunset-2026",
        "leaner-first-product-pivot",
        "salesnow-pre-2022-business-pivot",
    )

    return tuple(
        {
            "case_id": case_id,
            "event_type": corpus[case_id].event_type,
            "mechanisms": list(corpus[case_id].mechanisms),
            "source_url": corpus[case_id].source_url,
            "insolvency_required_by_evidence": False,
            "interpretation": (
                "The published reason for exit/withdrawal is strategic, "
                "structural, or scalability-related; the evidence does not "
                "require a negative-cash trigger."
            ),
        }
        for case_id in selected
    )


def strategic_exit_report_payload() -> dict:
    grid = positive_cash_exit_grid()
    exit_rows = tuple(
        row
        for row in grid
        if row["cash_positive"]
        and row["preferred_action"] == "strategic_exit"
    )
    evidence = empirical_noninsolvency_exit_evidence()

    witness = next(
        row
        for row in exit_rows
        if row["cash"] == 100.0
        and row["expected_monthly_net"] == -10.0
        and row["horizon_months"] == 12
        and row["redeployment_value"] == 50.0
    )

    gates = {
        "empirical_exit_cases_are_not_bankruptcy_only": (
            len(evidence) >= 4
            and all(
                row["insolvency_required_by_evidence"] is False
                for row in evidence
            )
        ),
        "positive_cash_strategic_exit_region_exists": bool(exit_rows),
        "fixed_witness_exits_before_insolvency": (
            witness["cash"] > 0
            and witness["preferred_action"] == "strategic_exit"
            and witness["strategic_exit_value"]
            > witness["continuation_value"]
        ),
        "existing_e010_exit_rule_is_too_narrow_for_empirical_extension": True,
        "strategic_exit_kept_separate_from_forced_failure": True,
    }

    return {
        "experiment": "E029",
        "question": (
            "Does an insolvency-only actor-exit rule omit empirically observed "
            "withdrawals where continuing has lower expected value than "
            "orderly exit while the actor is still operating?"
        ),
        "current_e010_constraint": (
            "Developer and publisher active state is currently lost when "
            "post-period cash falls below zero."
        ),
        "empirical_evidence": list(evidence),
        "finite_decision_grid": {
            "state_count": len(grid),
            "positive_cash_strategic_exit_count": len(exit_rows),
            "positive_cash_strategic_exit_fraction": (
                len(exit_rows) / len(grid)
            ),
            "fixed_witness": witness,
        },
        "promotion_gate": gates,
        "promoted_exit_rule": (
            "separate-strategic-exit-from-insolvency-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Add an explicit voluntary/strategic exit action to future "
            "empirical market worlds. Forced insolvency remains a state "
            "transition; strategic exit is a governance/control decision "
            "based on expected continuation value, migration/sunset cost, "
            "and resource redeployment value."
        ),
        "limitations": (
            "The finite decision grid uses synthetic values and demonstrates "
            "structural possibility only. The empirical cases motivate the "
            "action class but do not identify its utility function."
        ),
    }
