from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre007_imperfect_audit import evaluate_imperfect_audit
from market_microcosm.hidden_common_mode import (
    exact_forge_probability,
    nominal_independent_shocks,
)


@dataclass(frozen=True)
class DynamicWaitDecision:
    failure_loss: float
    act_now_cost: float
    wait_cost: float
    abandon_cost: float
    decision: str


def evaluate_wait(
    failure_loss: float,
    *,
    information_arrival_probability: float = 0.6,
    delay_cost: float = 0.25,
    unresolved_deadline_penalty: float = 0.2,
    abstention_cost: float = 5.0,
    hidden_prior: float = 0.5,
    mitigation_cost: float = 0.5,
    shock_probability: float = 0.01,
) -> DynamicWaitDecision:
    if failure_loss < 0.0:
        raise ValueError("failure_loss must be non-negative")
    if not 0.0 <= information_arrival_probability <= 1.0:
        raise ValueError("information_arrival_probability must be within [0, 1]")
    if not 0.0 <= hidden_prior <= 1.0:
        raise ValueError("hidden_prior must be within [0, 1]")
    if min(delay_cost, unresolved_deadline_penalty, abstention_cost, mitigation_cost) < 0.0:
        raise ValueError("costs must be non-negative")

    immediate = evaluate_imperfect_audit(
        failure_loss,
        hidden_prior=hidden_prior,
        mitigation_cost=mitigation_cost,
        abstention_cost=abstention_cost,
        shock_probability=shock_probability,
    )
    act_now_cost = min(immediate.unaudited_cost, immediate.audit_cost)

    nominal_risk = exact_forge_probability(
        nominal_independent_shocks(probability=shock_probability)
    )
    perfect_information_action_cost = hidden_prior * mitigation_cost + nominal_risk * failure_loss

    q = information_arrival_probability
    wait_cost = (
        delay_cost
        + q * perfect_information_action_cost
        + (1.0 - q) * (act_now_cost + unresolved_deadline_penalty)
    )

    costs = {
        "ACT_NOW": act_now_cost,
        "WAIT": wait_cost,
        "ABANDON": abstention_cost,
    }
    decision = min(costs, key=lambda name: (costs[name], name))
    return DynamicWaitDecision(
        failure_loss=failure_loss,
        act_now_cost=act_now_cost,
        wait_cost=wait_cost,
        abandon_cost=abstention_cost,
        decision=decision,
    )
