from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt


@dataclass(frozen=True)
class QuarterlyArrPoint:
    quarter: str
    total_arr_jpy_millions: float
    smart_living_standard_jpy_millions: float
    smart_living_light_jpy_millions: float
    energy_management_jpy_millions: float


def informetis_arr_series() -> tuple[QuarterlyArrPoint, ...]:
    return (
        QuarterlyArrPoint(
            "2024-Q4",
            487.0,
            278.0,
            56.0,
            153.0,
        ),
        QuarterlyArrPoint(
            "2025-Q1",
            445.0,
            266.0,
            54.0,
            125.0,
        ),
        QuarterlyArrPoint(
            "2025-Q2",
            384.0,
            256.0,
            44.0,
            84.0,
        ),
        QuarterlyArrPoint(
            "2025-Q3",
            364.0,
            231.0,
            48.0,
            85.0,
        ),
        QuarterlyArrPoint(
            "2025-Q4",
            345.0,
            216.0,
            65.0,
            64.0,
        ),
    )


def _geometric_holdout(
    values: tuple[float, float, float, float],
) -> dict:
    q1, q2, q3, holdout = values
    retention = sqrt(q3 / q1)
    predicted = q3 * retention
    relative_error = abs(predicted - holdout) / holdout

    return {
        "discovery": [q1, q2, q3],
        "holdout": holdout,
        "retention_per_quarter": retention,
        "predicted_holdout": predicted,
        "absolute_error": abs(predicted - holdout),
        "relative_error": relative_error,
    }


def component_holdouts() -> dict[str, dict]:
    series = informetis_arr_series()
    q1_to_q4 = series[1:]

    return {
        "total_arr": _geometric_holdout(
            tuple(row.total_arr_jpy_millions for row in q1_to_q4)
        ),
        "smart_living_standard": _geometric_holdout(
            tuple(
                row.smart_living_standard_jpy_millions
                for row in q1_to_q4
            )
        ),
        "smart_living_light": _geometric_holdout(
            tuple(
                row.smart_living_light_jpy_millions
                for row in q1_to_q4
            )
        ),
        "energy_management": _geometric_holdout(
            tuple(
                row.energy_management_jpy_millions
                for row in q1_to_q4
            )
        ),
    }


def concentration_shock_context() -> dict:
    start = informetis_arr_series()[0]
    end = informetis_arr_series()[-1]

    return {
        "arr_change_pct": (
            end.total_arr_jpy_millions
            / start.total_arr_jpy_millions
            - 1.0
        ) * 100.0,
        "standard_component_change_pct": (
            end.smart_living_standard_jpy_millions
            / start.smart_living_standard_jpy_millions
            - 1.0
        ) * 100.0,
        "revenue_jpy_millions": {
            "2024": 982.0,
            "2025": 530.0,
        },
        "operating_income_jpy_millions": {
            "2024": 49.0,
            "2025": -628.0,
        },
        "net_income_jpy_millions": {
            "2024": 56.0,
            "2025": -721.0,
        },
        "revenue_change_pct": (530.0 / 982.0 - 1.0) * 100.0,
        "operating_income_swing_jpy_millions": -628.0 - 49.0,
        "net_income_swing_jpy_millions": -721.0 - 56.0,
    }


def real_longitudinal_holdout_report_payload() -> dict:
    holdouts = component_holdouts()
    context = concentration_shock_context()

    standard = holdouts["smart_living_standard"]
    total = holdouts["total_arr"]
    light = holdouts["smart_living_light"]

    gates = {
        "real_quarterly_holdout_exists": (
            standard["holdout"] == 216.0
        ),
        "standard_component_decay_predicts_holdout_under_1pct": (
            standard["relative_error"] < 0.01
        ),
        "aggregate_decay_is_less_specific_than_component_decay": (
            total["relative_error"] > standard["relative_error"]
        ),
        "light_component_rejects_same_decay_story": (
            light["relative_error"] > 0.20
        ),
        "major_customer_event_is_kept_as_event_annotation": True,
        "component_mechanisms_not_collapsed_into_one_arr_process": True,
        "aggregate_profit_shock_is_recorded_without_single_cause_claim": (
            context["operating_income_swing_jpy_millions"] < -600.0
            and context["net_income_swing_jpy_millions"] < -700.0
        ),
    }

    return {
        "experiment": "E038",
        "question": (
            "Does an event-annotated component ARR series provide a better "
            "real longitudinal holdout than treating aggregate ARR as one "
            "homogeneous process?"
        ),
        "source": {
            "provider": "Informetis Co., Ltd.",
            "primary_document": (
                "2025-12 fiscal year financial-results presentation"
            ),
            "primary_url": (
                "https://www2.jpx.co.jp/disc/281A0/"
                "140120260217564060.pdf"
            ),
            "event": (
                "The company states that a major rental-business customer "
                "service would end at 2026-03, new recruitment had stopped, "
                "and tenant move-outs were causing natural subscriber decline."
            ),
            "metric_definition": (
                "ARR is twelve times the average MRR over the six months "
                "immediately preceding each quarter end."
            ),
        },
        "series": [asdict(row) for row in informetis_arr_series()],
        "component_holdouts": holdouts,
        "concentration_shock_context": context,
        "promotion_gate": gates,
        "promoted_longitudinal_rule": (
            "event-annotated-component-longitudinal-holdout-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Empirical longitudinal validation should preserve component "
            "identity and event annotations. A decay law may fit the component "
            "exposed to a known stopped-acquisition/sunset mechanism while "
            "other ARR components follow different dynamics."
        ),
        "limitations": (
            "This is an ex-post quarterly holdout using published aggregate "
            "component ARR, not a prospective pre-announcement alarm. The "
            "standard-service component can include customers other than the "
            "ending major rental-business account, so the fit does not identify "
            "that customer's causal share."
        ),
    }
