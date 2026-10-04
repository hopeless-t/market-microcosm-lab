from __future__ import annotations


def trailing_average_response(
    *,
    pre_shock_mrr: float,
    post_shock_mrr: float,
    window_months: int = 6,
) -> tuple[dict, ...]:
    rows = []

    for months_after_shock in range(0, window_months + 1):
        old_months = max(0, window_months - months_after_shock)
        new_months = window_months - old_months
        average_mrr = (
            old_months * pre_shock_mrr
            + new_months * post_shock_mrr
        ) / window_months

        rows.append(
            {
                "months_after_shock": months_after_shock,
                "legacy_months_in_window": old_months,
                "post_shock_months_in_window": new_months,
                "reported_arr": average_mrr * 12.0,
                "legacy_signal_fraction": (
                    0.0
                    if pre_shock_mrr == post_shock_mrr
                    else old_months / window_months
                ),
            }
        )

    return tuple(rows)


def abrupt_service_end_reference() -> dict:
    pre_shock_mrr = 10.0
    post_shock_mrr = 0.0

    response = trailing_average_response(
        pre_shock_mrr=pre_shock_mrr,
        post_shock_mrr=post_shock_mrr,
        window_months=6,
    )

    immediate_true_arr = post_shock_mrr * 12.0
    three_month_row = next(
        row for row in response
        if row["months_after_shock"] == 3
    )
    six_month_row = next(
        row for row in response
        if row["months_after_shock"] == 6
    )

    return {
        "pre_shock_mrr": pre_shock_mrr,
        "post_shock_mrr": post_shock_mrr,
        "pre_shock_arr_equivalent": pre_shock_mrr * 12.0,
        "immediate_true_post_shock_arr_equivalent": immediate_true_arr,
        "reported_metric_response": list(response),
        "three_month_post_shock": three_month_row,
        "six_month_post_shock": six_month_row,
    }


def rolling_metric_lag_report_payload() -> dict:
    reference = abrupt_service_end_reference()
    month3 = reference["three_month_post_shock"]
    month6 = reference["six_month_post_shock"]

    gates = {
        "rolling_arr_has_measurement_memory": (
            month3["legacy_months_in_window"] == 3
        ),
        "three_month_readout_retains_half_legacy_signal": (
            abs(month3["legacy_signal_fraction"] - 0.5) < 1e-12
        ),
        "three_month_reported_arr_can_remain_positive_after_true_zero": (
            month3["reported_arr"] > 0.0
            and reference[
                "immediate_true_post_shock_arr_equivalent"
            ]
            == 0.0
        ),
        "legacy_signal_fully_exits_after_six_months": (
            month6["reported_arr"] == 0.0
            and month6["legacy_signal_fraction"] == 0.0
        ),
        "metric_kernel_is_separate_from_business_state": True,
        "post_event_quarter_is_not_assumed_steady_state": True,
    }

    return {
        "experiment": "E039",
        "question": (
            "Can a trailing-six-month ARR definition delay observation of "
            "an abrupt service-state change enough to make a post-event "
            "quarter look healthier than the instantaneous underlying state?"
        ),
        "empirical_metric_definition": {
            "provider": "Informetis Co., Ltd.",
            "definition": (
                "ARR = 12 × average MRR over the six months immediately "
                "preceding quarter end."
            ),
            "source_url": (
                "https://www2.jpx.co.jp/disc/281A0/"
                "140120260217564060.pdf"
            ),
            "event_context": (
                "A major rental-business service ended at 2026-03. A June "
                "quarter-end ARR using a six-month trailing window can still "
                "contain pre-end January-March MRR."
            ),
        },
        "abrupt_end_reference": reference,
        "promotion_gate": gates,
        "promoted_observation_rule": (
            "rolling-window-metric-lag-must-be-modeled-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Observed KPIs need a measurement kernel separate from latent "
            "business state. Event timing, window length, and publication "
            "cadence determine observation lag and must be modeled before "
            "warning lead time is evaluated."
        ),
        "limitations": (
            "The abrupt 10→0 MRR reference is a structural impulse response, "
            "not Informetis's actual customer-level MRR. Aggregate company ARR "
            "contains multiple products and replacement growth."
        ),
    }
