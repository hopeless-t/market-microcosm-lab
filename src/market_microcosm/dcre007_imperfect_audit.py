from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.hidden_common_mode import (
    exact_forge_probability,
    hidden_common_mode_shocks,
    nominal_independent_shocks,
)


@dataclass(frozen=True)
class ImperfectAuditDecision:
    failure_loss: float
    unaudited_cost: float
    audit_cost: float
    abstain_cost: float
    decision: str


def evaluate_imperfect_audit(
    failure_loss: float,
    *,
    hidden_prior: float = 0.5,
    sensitivity: float = 0.9,
    false_positive_rate: float = 0.05,
    audit_fixed_cost: float = 0.5,
    mitigation_cost: float = 0.5,
    abstention_cost: float = 5.0,
    shock_probability: float = 0.01,
) -> ImperfectAuditDecision:
    if failure_loss < 0.0:
        raise ValueError("failure_loss must be non-negative")
    for name, value in (
        ("hidden_prior", hidden_prior),
        ("sensitivity", sensitivity),
        ("false_positive_rate", false_positive_rate),
    ):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be within [0, 1]")
    if min(audit_fixed_cost, mitigation_cost, abstention_cost) < 0.0:
        raise ValueError("costs must be non-negative")

    nominal_risk = exact_forge_probability(
        nominal_independent_shocks(probability=shock_probability)
    )
    hidden_risk = exact_forge_probability(
        hidden_common_mode_shocks(probability=shock_probability)
    )

    unaudited = (
        hidden_prior * hidden_risk
        + (1.0 - hidden_prior) * nominal_risk
    ) * failure_loss

    hidden_branch = sensitivity * (
        mitigation_cost + nominal_risk * failure_loss
    ) + (1.0 - sensitivity) * hidden_risk * failure_loss
    nominal_branch = false_positive_rate * (
        mitigation_cost + nominal_risk * failure_loss
    ) + (1.0 - false_positive_rate) * nominal_risk * failure_loss
    audited = (
        audit_fixed_cost
        + hidden_prior * hidden_branch
        + (1.0 - hidden_prior) * nominal_branch
    )

    costs = {
        "UNAUDITED": unaudited,
        "AUDIT": audited,
        "ABSTAIN": abstention_cost,
    }
    decision = min(costs, key=lambda name: (costs[name], name))
    return ImperfectAuditDecision(
        failure_loss=failure_loss,
        unaudited_cost=unaudited,
        audit_cost=audited,
        abstain_cost=abstention_cost,
        decision=decision,
    )
