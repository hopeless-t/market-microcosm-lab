from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.hidden_common_mode import (
    exact_forge_probability,
    hidden_common_mode_shocks,
    nominal_independent_shocks,
)


@dataclass(frozen=True)
class AuditDecision:
    failure_loss: float
    audit_cost: float
    nominal_risk: float
    hidden_risk: float
    unaudited_expected_cost: float
    audited_expected_cost: float
    decision: str


def audit_knee(*, audit_cost: float = 1.0, shock_probability: float = 0.01) -> float:
    if audit_cost < 0.0:
        raise ValueError("audit_cost must be non-negative")
    nominal = exact_forge_probability(
        nominal_independent_shocks(probability=shock_probability)
    )
    hidden = exact_forge_probability(
        hidden_common_mode_shocks(probability=shock_probability)
    )
    risk_delta = hidden - nominal
    if risk_delta <= 0.0:
        raise ValueError("hidden model must exceed nominal risk")
    return audit_cost / risk_delta


def evaluate_audit(
    failure_loss: float,
    *,
    audit_cost: float = 1.0,
    shock_probability: float = 0.01,
) -> AuditDecision:
    if failure_loss < 0.0:
        raise ValueError("failure_loss must be non-negative")
    if audit_cost < 0.0:
        raise ValueError("audit_cost must be non-negative")

    nominal = exact_forge_probability(
        nominal_independent_shocks(probability=shock_probability)
    )
    hidden = exact_forge_probability(
        hidden_common_mode_shocks(probability=shock_probability)
    )
    unaudited = hidden * failure_loss
    audited = audit_cost + nominal * failure_loss

    tolerance = 1e-12
    if audited < unaudited - tolerance:
        decision = "AUDIT"
    elif unaudited < audited - tolerance:
        decision = "UNAUDITED"
    else:
        decision = "TIE"

    return AuditDecision(
        failure_loss=failure_loss,
        audit_cost=audit_cost,
        nominal_risk=nominal,
        hidden_risk=hidden,
        unaudited_expected_cost=unaudited,
        audited_expected_cost=audited,
        decision=decision,
    )
