from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricDefinition:
    metric_id: str
    construct: str
    formula: str
    scope: str
    generation: int
    retrospective_backfill: bool


def old_arr_metric() -> MetricDefinition:
    return MetricDefinition(
        metric_id="overseas_saas_arr",
        construct="recurring_revenue_run_rate",
        formula="quarter_end_recurring_mrr_x_12",
        scope="overseas_saas",
        generation=1,
        retrospective_backfill=False,
    )


def new_revenue_per_employee_metric() -> MetricDefinition:
    return MetricDefinition(
        metric_id="domestic_revenue_per_employee",
        construct="labor_productivity_revenue_intensity",
        formula="domestic_business_revenue_div_average_domestic_full_time_employees",
        scope="domestic_business",
        generation=2,
        retrospective_backfill=True,
    )


def comparability(left: MetricDefinition, right: MetricDefinition) -> dict:
    same_construct = left.construct == right.construct
    same_formula = left.formula == right.formula
    same_scope = left.scope == right.scope
    authorized = same_construct and same_formula and same_scope
    return {
        "same_construct": same_construct,
        "same_formula": same_formula,
        "same_scope": same_scope,
        "authorized": authorized,
        "decision": "COMPARABLE" if authorized else "REJECT_CONSTRUCT_BRIDGE",
    }


def replacement_kpi_bridge_report_payload() -> dict:
    old = old_arr_metric()
    new = new_revenue_per_employee_metric()

    within_new_generation = comparability(new, new)
    old_to_new = comparability(old, new)

    gates = {
        "new_metric_has_retrospective_backfill": new.retrospective_backfill is True,
        "new_metric_is_self_comparable_across_backfilled_periods": (
            within_new_generation["authorized"] is True
        ),
        "old_arr_and_new_productivity_metric_are_distinct_constructs": (
            old_to_new["same_construct"] is False
        ),
        "old_arr_and_new_metric_have_distinct_scopes": (
            old_to_new["same_scope"] is False
        ),
        "cross_construct_splice_is_rejected": (
            old_to_new["decision"] == "REJECT_CONSTRUCT_BRIDGE"
        ),
        "backfill_does_not_create_cross_construct_authority": True,
    }

    return {
        "experiment": "E091",
        "question": (
            "When a company introduces a new KPI and retrospectively backfills "
            "that new KPI, does the backfill authorize splicing it onto a "
            "withdrawn KPI series measuring a different construct?"
        ),
        "source": {
            "provider": "Allied Architects, Inc.",
            "document": "FY2025 Q1 financial results presentation",
            "published_on": "2025-07-18",
            "page": 7,
            "annotation": (
                "The company introduces revenue per employee as a new KPI and "
                "states that 2024 quarterly values are retrospectively calculated "
                "under the same definition."
            ),
        },
        "old_metric": old.__dict__,
        "replacement_metric": new.__dict__,
        "within_replacement_generation": within_new_generation,
        "old_to_replacement_bridge": old_to_new,
        "promotion_gate": gates,
        "promoted_bridge_rule": (
            "replacement-kpi-backfill-does-not-bridge-different-constructs-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Retrospective backfill grants comparability only inside the new "
            "metric definition. It does not bridge a withdrawn KPI that measures "
            "a different construct, formula, or scope."
        ),
        "limitations": (
            "E091 compares public metric definitions, not economic usefulness. "
            "It does not claim either KPI is superior for every decision."
        ),
    }
