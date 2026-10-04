from __future__ import annotations

from math import sqrt


ROUNDING_UNIT_JPY_MILLIONS = 1.0


def rounded_interval(
    displayed_value: float,
    *,
    rounding_unit: float = ROUNDING_UNIT_JPY_MILLIONS,
) -> tuple[float, float]:
    half = rounding_unit / 2.0
    return displayed_value - half, displayed_value + half


def standard_decay_prediction_interval() -> dict:
    q1_displayed = 266.0
    q3_displayed = 231.0
    q4_displayed = 216.0

    q1_low, q1_high = rounded_interval(q1_displayed)
    q3_low, q3_high = rounded_interval(q3_displayed)
    q4_low, q4_high = rounded_interval(q4_displayed)

    point_prediction = q3_displayed * sqrt(
        q3_displayed / q1_displayed
    )

    prediction_low = q3_low * sqrt(q3_low / q1_high)
    prediction_high = q3_high * sqrt(q3_high / q1_low)

    overlap_low = max(prediction_low, q4_low)
    overlap_high = min(prediction_high, q4_high)
    intervals_overlap = overlap_low < overlap_high

    point_absolute_error = abs(point_prediction - q4_displayed)
    point_relative_error = point_absolute_error / q4_displayed

    return {
        "displayed": {
            "q1": q1_displayed,
            "q3": q3_displayed,
            "q4_holdout": q4_displayed,
            "rounding_unit_jpy_millions": ROUNDING_UNIT_JPY_MILLIONS,
        },
        "input_intervals": {
            "q1": [q1_low, q1_high],
            "q3": [q3_low, q3_high],
        },
        "holdout_interval": [q4_low, q4_high],
        "point_prediction": point_prediction,
        "point_absolute_error": point_absolute_error,
        "point_relative_error": point_relative_error,
        "prediction_interval_from_rounding": [
            prediction_low,
            prediction_high,
        ],
        "intervals_overlap": intervals_overlap,
        "overlap_interval": (
            [overlap_low, overlap_high]
            if intervals_overlap
            else None
        ),
        "point_error_below_one_display_unit": (
            point_absolute_error < ROUNDING_UNIT_JPY_MILLIONS
        ),
    }


def reporting_resolution_report_payload() -> dict:
    row = standard_decay_prediction_interval()

    gates = {
        "e038_point_error_is_sub_display_unit": (
            row["point_error_below_one_display_unit"] is True
        ),
        "input_rounding_materially_widens_prediction": (
            row["prediction_interval_from_rounding"][1]
            - row["prediction_interval_from_rounding"][0]
            > 1.5
        ),
        "prediction_and_holdout_intervals_overlap": (
            row["intervals_overlap"] is True
        ),
        "sub1pct_point_precision_is_not_authoritative": True,
        "interval_consistency_claim_remains_admissible": True,
        "reporting_resolution_is_part_of_empirical_identity": True,
    }

    return {
        "experiment": "E042",
        "question": (
            "Does the rounded reporting resolution of the Informetis ARR "
            "chart support E038's apparent sub-1% point-error precision?"
        ),
        "e038_reassessment": row,
        "legacy_e038_sub1pct_precision_authority": "REVOKED",
        "revised_e038_claim": (
            "The component-decay prediction is consistent with the rounded "
            "Q4 holdout interval, but the displayed million-JPY values do not "
            "support a sub-1% empirical accuracy claim."
        ),
        "promotion_gate": gates,
        "promoted_resolution_rule": (
            "empirical-claim-precision-cannot-exceed-reporting-resolution-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Empirical values carry quantization/rounding intervals. Model "
            "fit and holdout claims must propagate those intervals before "
            "assigning precision authority."
        ),
        "limitations": (
            "The +/-0.5 million JPY interval assumes standard nearest-million "
            "rounding of the chart labels. More precise underlying component "
            "figures, if published, could narrow the interval and permit a "
            "stronger re-evaluation."
        ),
    }
