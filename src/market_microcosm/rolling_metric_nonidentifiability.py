from __future__ import annotations

from itertools import combinations_with_replacement


WINDOW_MONTHS = 6
MAX_MRR = 10
TARGET_AVERAGE_MRR = 5


def monotone_paths_with_same_rolling_metric() -> tuple[tuple[int, ...], ...]:
    target_sum = TARGET_AVERAGE_MRR * WINDOW_MONTHS
    paths = []

    for ascending in combinations_with_replacement(
        range(MAX_MRR + 1),
        WINDOW_MONTHS,
    ):
        path = tuple(reversed(ascending))
        if sum(path) == target_sum:
            paths.append(path)

    return tuple(paths)


def ambiguity_summary() -> dict:
    paths = monotone_paths_with_same_rolling_metric()
    final_values = sorted({path[-1] for path in paths})

    examples = {
        str(final_value): next(
            path for path in paths
            if path[-1] == final_value
        )
        for final_value in final_values
    }

    return {
        "window_months": WINDOW_MONTHS,
        "target_average_mrr": TARGET_AVERAGE_MRR,
        "reported_arr": TARGET_AVERAGE_MRR * 12,
        "path_count": len(paths),
        "possible_current_mrr_values": final_values,
        "minimum_current_mrr": min(final_values),
        "maximum_current_mrr": max(final_values),
        "examples_by_current_mrr": {
            key: list(value) for key, value in examples.items()
        },
    }


def rolling_metric_nonidentifiability_report_payload() -> dict:
    summary = ambiguity_summary()

    gates = {
        "same_reported_arr_has_many_latent_paths": (
            summary["path_count"] > 100
        ),
        "current_mrr_can_be_zero": (
            summary["minimum_current_mrr"] == 0
        ),
        "current_mrr_can_remain_positive": (
            summary["maximum_current_mrr"] >= 5
        ),
        "same_metric_spans_material_current_state_range": (
            summary["maximum_current_mrr"]
            - summary["minimum_current_mrr"]
            >= 5
        ),
        "rolling_metric_does_not_identify_current_state": True,
        "deconvolution_requires_additional_state_or_assumptions": True,
    }

    return {
        "experiment": "E040",
        "question": (
            "Does one trailing-six-month ARR value uniquely identify the "
            "current MRR state even when the latent path is restricted to "
            "monotone decline?"
        ),
        "metric_context": {
            "window_months": WINDOW_MONTHS,
            "arr_definition": (
                "reported ARR = 12 × average MRR over the trailing window"
            ),
            "informetis_source_url": (
                "https://www2.jpx.co.jp/disc/281A0/"
                "140120260217564060.pdf"
            ),
        },
        "exact_ambiguity": summary,
        "promotion_gate": gates,
        "promoted_identifiability_rule": (
            "rolling-kpi-current-state-nonidentifiable-without-path-state-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "A rolling KPI cannot be inverted into current latent state from "
            "one aggregate value alone. Early-warning models must either "
            "observe additional boundary/path state or explicitly carry a "
            "set/distribution of compatible latent states."
        ),
        "limitations": (
            "The integer monotone path lattice is a finite proof witness, "
            "not a model of actual Informetis monthly MRR. Allowing arbitrary "
            "continuous or non-monotone paths only enlarges ambiguity."
        ),
    }
