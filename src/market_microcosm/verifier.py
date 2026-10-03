from __future__ import annotations

from dataclasses import dataclass

from .evaluation import Evaluation


@dataclass(frozen=True)
class PromotionRule:
    minimum_survival_rate: float = 0.95
    maximum_survival_drop: float = 0.0
    minimum_welfare_gain: float = 0.0
    maximum_invariant_violations: int = 0


@dataclass(frozen=True)
class PromotionDecision:
    promoted: bool
    reasons: tuple[str, ...]


def verify_promotion(
    incumbent: Evaluation,
    challenger: Evaluation,
    rule: PromotionRule,
) -> PromotionDecision:
    reasons: list[str] = []

    if challenger.invariant_violations > rule.maximum_invariant_violations:
        reasons.append("challenger violated hard invariants")
    if challenger.survival_rate < rule.minimum_survival_rate:
        reasons.append("challenger survival below absolute floor")
    if challenger.survival_rate + rule.maximum_survival_drop < incumbent.survival_rate:
        reasons.append("challenger degrades protected survival metric")
    welfare_gain = challenger.mean_welfare - incumbent.mean_welfare
    if welfare_gain < rule.minimum_welfare_gain:
        reasons.append("challenger lacks required welfare gain")

    return PromotionDecision(promoted=not reasons, reasons=tuple(reasons))
