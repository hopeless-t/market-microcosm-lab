from __future__ import annotations

from market_microcosm.censored_evaluation_guard import reference_cases


def full_population_accuracy_interval() -> dict:
    cases = reference_cases()
    observed = [case for case in cases if case.numeric_label_available]
    censored = [case for case in cases if not case.numeric_label_available]
    observed_correct = sum(
        case.prediction == case.numeric_label for case in observed
    )
    total = len(cases)

    lower = observed_correct / total
    upper = (observed_correct + len(censored)) / total

    return {
        "observed_correct": observed_correct,
        "observed_labels": len(observed),
        "censored_labels": len(censored),
        "total_cases": total,
        "accuracy_lower_bound": lower,
        "accuracy_upper_bound": upper,
    }


def threshold_decision(required_accuracy: float) -> dict:
    interval = full_population_accuracy_interval()
    lower = interval["accuracy_lower_bound"]
    upper = interval["accuracy_upper_bound"]

    if lower >= required_accuracy:
        decision = "CERTIFIED_PASS"
    elif upper < required_accuracy:
        decision = "CERTIFIED_FAIL"
    else:
        decision = "ABSTAIN_CENSORED_LABELS"

    return {
        "required_accuracy": required_accuracy,
        "decision": decision,
        "interval": interval,
    }


def censored_accuracy_interval_report_payload() -> dict:
    interval = full_population_accuracy_interval()
    threshold_75 = threshold_decision(0.75)
    threshold_90 = threshold_decision(0.90)

    gates = {
        "full_population_accuracy_lower_bound_is_point_eight": (
            interval["accuracy_lower_bound"] == 0.8
        ),
        "full_population_accuracy_upper_bound_is_one": (
            interval["accuracy_upper_bound"] == 1.0
        ),
        "naive_one_point_zero_point_claim_is_not_identified": (
            interval["accuracy_lower_bound"] != interval["accuracy_upper_bound"]
        ),
        "seventy_five_percent_threshold_is_certified": (
            threshold_75["decision"] == "CERTIFIED_PASS"
        ),
        "ninety_percent_threshold_abstains": (
            threshold_90["decision"] == "ABSTAIN_CENSORED_LABELS"
        ),
        "censored_cases_are_bounded_not_imputed": True,
    }

    return {
        "experiment": "E084",
        "question": (
            "Can informatively censored evaluation still support bounded "
            "performance claims without imputing the hidden labels?"
        ),
        "accuracy_interval": interval,
        "threshold_decisions": {
            "0.75": threshold_75,
            "0.90": threshold_90,
        },
        "promotion_gate": gates,
        "promoted_interval_rule": (
            "censored-evaluation-uses-full-population-performance-intervals-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Partial evaluation is upgraded from a coverage warning to a "
            "sharp finite-population accuracy interval. Decision authority is "
            "predicate-scoped: coarse thresholds can be certified while finer "
            "thresholds that intersect the interval must ABSTAIN."
        ),
        "limitations": (
            "The interval is worst-case over unknown censored labels and does "
            "not use a statistical model for censoring. It is intentionally "
            "conservative but assumption-light."
        ),
    }
