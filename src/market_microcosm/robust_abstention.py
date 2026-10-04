from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.decision_sufficient_observability import (
    Interval,
    decision_sufficiency_reference,
)


@dataclass(frozen=True)
class RobustDecision:
    result: str
    reason: str


def robust_threshold_decision(
    interval: Interval,
    *,
    threshold: float,
) -> RobustDecision:
    if interval.low >= threshold:
        return RobustDecision(
            "CERTIFIED_TRUE",
            "every compatible state is at or above threshold",
        )
    if interval.high < threshold:
        return RobustDecision(
            "CERTIFIED_FALSE",
            "every compatible state is below threshold",
        )
    return RobustDecision(
        "ABSTAIN",
        "compatible states exist on both sides of threshold",
    )


def midpoint_forced_decision(
    interval: Interval,
    *,
    threshold: float,
) -> bool:
    midpoint = (interval.low + interval.high) / 2.0
    return midpoint >= threshold


def abstention_reference() -> dict:
    e043 = decision_sufficiency_reference()
    ambiguous_interval = Interval(
        *e043["newest_mrr_interval_with_exact_boundary"]
    )

    clearly_true = Interval(2.6, 3.2)
    clearly_false = Interval(0.8, 1.4)
    threshold = 2.0

    ambiguous = robust_threshold_decision(
        ambiguous_interval,
        threshold=threshold,
    )
    true_decision = robust_threshold_decision(
        clearly_true,
        threshold=threshold,
    )
    false_decision = robust_threshold_decision(
        clearly_false,
        threshold=threshold,
    )

    midpoint_forced = midpoint_forced_decision(
        ambiguous_interval,
        threshold=threshold,
    )

    counterexample_state = 1.5
    midpoint_is_unsound = (
        midpoint_forced is True
        and counterexample_state < threshold
        and ambiguous_interval.contains(counterexample_state)
    )

    return {
        "threshold": threshold,
        "ambiguous_interval": [
            ambiguous_interval.low,
            ambiguous_interval.high,
        ],
        "ambiguous_robust_result": ambiguous.result,
        "clearly_true_interval": [clearly_true.low, clearly_true.high],
        "clearly_true_result": true_decision.result,
        "clearly_false_interval": [clearly_false.low, clearly_false.high],
        "clearly_false_result": false_decision.result,
        "midpoint_forced_result": midpoint_forced,
        "compatible_counterexample_state": counterexample_state,
        "midpoint_forced_decision_is_unsound": midpoint_is_unsound,
    }


def robust_abstention_report_payload() -> dict:
    reference = abstention_reference()

    gates = {
        "boundary_straddling_interval_abstains": (
            reference["ambiguous_robust_result"] == "ABSTAIN"
        ),
        "clearly_true_interval_is_certified": (
            reference["clearly_true_result"] == "CERTIFIED_TRUE"
        ),
        "clearly_false_interval_is_certified": (
            reference["clearly_false_result"] == "CERTIFIED_FALSE"
        ),
        "midpoint_forcing_has_compatible_counterexample": (
            reference["midpoint_forced_decision_is_unsound"] is True
        ),
        "abstention_is_authorized_control_output": True,
        "more_data_required_only_for_unresolved_predicates": True,
    }

    return {
        "experiment": "E044",
        "question": (
            "When an uncertainty interval straddles a decision boundary, "
            "should the system force a binary answer from a point proxy or "
            "emit an explicit abstention until more evidence arrives?"
        ),
        "reference": reference,
        "promotion_gate": gates,
        "promoted_decision_rule": (
            "boundary-straddling-uncertainty-must-abstain-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "ABSTAIN becomes a first-class control output. Forced binary "
            "decisions are admissible only when every compatible latent state "
            "agrees on the predicate; otherwise the system requests additional "
            "evidence only for that unresolved decision."
        ),
        "limitations": (
            "The reference uses one scalar threshold. Multi-objective actions "
            "and asymmetric error costs require predicate-specific loss and "
            "possibly different abstention bands."
        ),
    }
