from __future__ import annotations


WINDOW_MONTHS = 6


def newest_mrr_interval_from_rounded_arr(
    *,
    previous_arr_displayed: float,
    current_arr_displayed: float,
    outgoing_oldest_mrr: float,
    arr_rounding_unit: float = 1.0,
) -> tuple[float, float]:
    half = arr_rounding_unit / 2.0

    previous_arr_low = previous_arr_displayed - half
    previous_arr_high = previous_arr_displayed + half
    current_arr_low = current_arr_displayed - half
    current_arr_high = current_arr_displayed + half

    scale = WINDOW_MONTHS / 12.0

    previous_sum_low = previous_arr_low * scale
    previous_sum_high = previous_arr_high * scale
    current_sum_low = current_arr_low * scale
    current_sum_high = current_arr_high * scale

    newest_low = (
        current_sum_low
        - previous_sum_high
        + outgoing_oldest_mrr
    )
    newest_high = (
        current_sum_high
        - previous_sum_low
        + outgoing_oldest_mrr
    )

    return newest_low, newest_high


def classify_threshold_from_interval(
    *,
    interval: tuple[float, float],
    threshold: float,
) -> str:
    low, high = interval

    if low >= threshold:
        return "CERTAIN_TRUE"
    if high < threshold:
        return "CERTAIN_FALSE"
    return "UNKNOWN"


def decision_relative_reference() -> dict:
    interval = newest_mrr_interval_from_rounded_arr(
        previous_arr_displayed=60.0,
        current_arr_displayed=44.0,
        outgoing_oldest_mrr=10.0,
        arr_rounding_unit=1.0,
    )

    predicates = {
        "mrr_positive": {
            "threshold": 0.0,
            "classification": classify_threshold_from_interval(
                interval=interval,
                threshold=0.0,
            ),
        },
        "mrr_at_least_2": {
            "threshold": 2.0,
            "classification": classify_threshold_from_interval(
                interval=interval,
                threshold=2.0,
            ),
        },
        "mrr_at_least_3": {
            "threshold": 3.0,
            "classification": classify_threshold_from_interval(
                interval=interval,
                threshold=3.0,
            ),
        },
    }

    return {
        "displayed_previous_arr": 60.0,
        "displayed_current_arr": 44.0,
        "outgoing_boundary_mrr": 10.0,
        "arr_rounding_unit": 1.0,
        "newest_mrr_interval": list(interval),
        "interval_width": interval[1] - interval[0],
        "predicates": predicates,
    }


def decision_relative_observability_report_payload() -> dict:
    reference = decision_relative_reference()

    gates = {
        "rounded_inputs_destroy_exact_point_reconstruction": (
            reference["interval_width"] > 0.0
        ),
        "positive_activity_predicate_is_still_identifiable": (
            reference["predicates"]["mrr_positive"]["classification"]
            == "CERTAIN_TRUE"
        ),
        "threshold_2_predicate_is_ambiguous": (
            reference["predicates"]["mrr_at_least_2"]["classification"]
            == "UNKNOWN"
        ),
        "threshold_3_predicate_is_identifiably_false": (
            reference["predicates"]["mrr_at_least_3"]["classification"]
            == "CERTAIN_FALSE"
        ),
        "observability_is_defined_relative_to_decision_predicate": True,
        "unknown_threshold_crossings_fail_closed": True,
    }

    return {
        "experiment": "E043",
        "question": (
            "When reporting quantization prevents exact state recovery, can "
            "the same interval still be sufficient for some decisions but "
            "not others?"
        ),
        "reference": reference,
        "e041_exact_point_authority_under_rounded_arr": "REVOKED",
        "promotion_gate": gates,
        "promoted_observability_rule": (
            "observability-is-decision-relative-with-interval-fail-closed-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "The evidence plane need not reconstruct an exact latent scalar "
            "when the downstream decision only requires a predicate. Carry "
            "an uncertainty interval and certify a decision only when the "
            "entire interval lies on one side of its threshold; otherwise "
            "return UNKNOWN."
        ),
        "limitations": (
            "The interval assumes exact knowledge of the outgoing boundary "
            "MRR and nearest-one-unit ARR rounding. Additional boundary noise "
            "would widen the interval."
        ),
    }
