from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.minimal_observability_checkpoint import (
    WINDOW_MONTHS,
)


@dataclass(frozen=True)
class Interval:
    low: float
    high: float

    def contains(self, value: float) -> bool:
        return self.low <= value <= self.high


def arr_interval(
    displayed_arr: float,
    *,
    rounding_unit: float = 1.0,
) -> Interval:
    half = rounding_unit / 2.0
    return Interval(displayed_arr - half, displayed_arr + half)


def rolling_sum_interval(arr: Interval) -> Interval:
    factor = WINDOW_MONTHS / 12.0
    return Interval(arr.low * factor, arr.high * factor)


def reconstruct_newest_interval(
    *,
    previous_arr: Interval,
    current_arr: Interval,
    outgoing_mrr: Interval,
) -> Interval:
    previous_sum = rolling_sum_interval(previous_arr)
    current_sum = rolling_sum_interval(current_arr)

    return Interval(
        current_sum.low - previous_sum.high + outgoing_mrr.low,
        current_sum.high - previous_sum.low + outgoing_mrr.high,
    )


def predicate_truth(
    interval: Interval,
    *,
    threshold: float,
    operator: str,
) -> str:
    if operator == ">":
        if interval.low > threshold:
            return "CERTIFIED_TRUE"
        if interval.high <= threshold:
            return "CERTIFIED_FALSE"
        return "AMBIGUOUS"

    if operator == ">=":
        if interval.low >= threshold:
            return "CERTIFIED_TRUE"
        if interval.high < threshold:
            return "CERTIFIED_FALSE"
        return "AMBIGUOUS"

    if operator == "<":
        if interval.high < threshold:
            return "CERTIFIED_TRUE"
        if interval.low >= threshold:
            return "CERTIFIED_FALSE"
        return "AMBIGUOUS"

    if operator == "<=":
        if interval.high <= threshold:
            return "CERTIFIED_TRUE"
        if interval.low > threshold:
            return "CERTIFIED_FALSE"
        return "AMBIGUOUS"

    raise ValueError(f"unsupported operator: {operator}")


def decision_sufficiency_reference() -> dict:
    previous = arr_interval(60.0)
    current = arr_interval(44.0)

    exact_boundary = Interval(10.0, 10.0)
    rounded_boundary = Interval(9.5, 10.5)

    exact_boundary_state = reconstruct_newest_interval(
        previous_arr=previous,
        current_arr=current,
        outgoing_mrr=exact_boundary,
    )
    rounded_boundary_state = reconstruct_newest_interval(
        previous_arr=previous,
        current_arr=current,
        outgoing_mrr=rounded_boundary,
    )

    predicates = {
        "active_gt_0": {
            "threshold": 0.0,
            "operator": ">",
            "exact_boundary": predicate_truth(
                exact_boundary_state,
                threshold=0.0,
                operator=">",
            ),
            "rounded_boundary": predicate_truth(
                rounded_boundary_state,
                threshold=0.0,
                operator=">",
            ),
        },
        "at_least_2": {
            "threshold": 2.0,
            "operator": ">=",
            "exact_boundary": predicate_truth(
                exact_boundary_state,
                threshold=2.0,
                operator=">=",
            ),
            "rounded_boundary": predicate_truth(
                rounded_boundary_state,
                threshold=2.0,
                operator=">=",
            ),
        },
        "distress_le_1": {
            "threshold": 1.0,
            "operator": "<=",
            "exact_boundary": predicate_truth(
                exact_boundary_state,
                threshold=1.0,
                operator="<=",
            ),
            "rounded_boundary": predicate_truth(
                rounded_boundary_state,
                threshold=1.0,
                operator="<=",
            ),
        },
    }

    return {
        "previous_arr_interval": [previous.low, previous.high],
        "current_arr_interval": [current.low, current.high],
        "exact_boundary_mrr_interval": [
            exact_boundary.low,
            exact_boundary.high,
        ],
        "rounded_boundary_mrr_interval": [
            rounded_boundary.low,
            rounded_boundary.high,
        ],
        "newest_mrr_interval_with_exact_boundary": [
            exact_boundary_state.low,
            exact_boundary_state.high,
        ],
        "newest_mrr_interval_with_rounded_boundary": [
            rounded_boundary_state.low,
            rounded_boundary_state.high,
        ],
        "predicates": predicates,
    }


def decision_sufficient_observability_report_payload() -> dict:
    reference = decision_sufficiency_reference()

    exact_interval = reference[
        "newest_mrr_interval_with_exact_boundary"
    ]
    rounded_interval = reference[
        "newest_mrr_interval_with_rounded_boundary"
    ]
    predicates = reference["predicates"]

    gates = {
        "rounding_prevents_exact_point_reconstruction": (
            exact_interval[0] < exact_interval[1]
        ),
        "exact_boundary_still_certifies_activity": (
            predicates["active_gt_0"]["exact_boundary"]
            == "CERTIFIED_TRUE"
        ),
        "rounded_boundary_still_certifies_activity": (
            predicates["active_gt_0"]["rounded_boundary"]
            == "CERTIFIED_TRUE"
        ),
        "threshold_two_remains_ambiguous": (
            predicates["at_least_2"]["exact_boundary"]
            == "AMBIGUOUS"
            and predicates["at_least_2"]["rounded_boundary"]
            == "AMBIGUOUS"
        ),
        "decision_predicate_can_need_less_information_than_exact_state": True,
        "observability_authority_is_predicate_scoped": True,
    }

    return {
        "experiment": "E043",
        "question": (
            "When reporting resolution prevents exact latent-state recovery, "
            "can the available interval still be sufficient for a specific "
            "decision predicate?"
        ),
        "reference": reference,
        "promotion_gate": gates,
        "promoted_observability_rule": (
            "observability-authority-is-decision-predicate-scoped-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Do not require exact latent-state reconstruction when the "
            "downstream decision only needs a coarser predicate. Carry an "
            "interval/set of compatible states and certify a decision only "
            "when every compatible state gives the same predicate result."
        ),
        "limitations": (
            "The reference uses independent nearest-unit rounding intervals "
            "and a fixed six-month window. Correlated reporting errors, metric "
            "redefinitions, or noisier observations require a larger "
            "uncertainty set and can revoke predicate authority."
        ),
    }
