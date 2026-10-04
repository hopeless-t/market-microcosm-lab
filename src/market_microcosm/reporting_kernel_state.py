from __future__ import annotations

from dataclasses import dataclass


RICH_KPIS = frozenset(
    {
        "revenue",
        "operating_profit",
        "stock_revenue",
        "stock_revenue_ratio",
        "arr",
        "churn_rate",
        "customer_count",
        "average_unit_price",
    }
)

DEGRADED_KPIS = frozenset({"revenue", "operating_profit"})


@dataclass(frozen=True)
class ObservationKernel:
    kernel_id: str
    generation: int
    visible_metrics: frozenset[str]
    comparability_bridge_from_previous: bool


def rich_kernel() -> ObservationKernel:
    return ObservationKernel(
        kernel_id="OVERSEAS_SAAS_RICH_KPI_KERNEL",
        generation=1,
        visible_metrics=RICH_KPIS,
        comparability_bridge_from_previous=True,
    )


def degraded_kernel() -> ObservationKernel:
    return ObservationKernel(
        kernel_id="OVERSEAS_SAAS_REVENUE_PROFIT_ONLY_KERNEL",
        generation=2,
        visible_metrics=DEGRADED_KPIS,
        comparability_bridge_from_previous=False,
    )


def observe(latent_state: dict[str, float], kernel: ObservationKernel) -> dict:
    return {
        metric: latent_state[metric]
        for metric in sorted(kernel.visible_metrics)
        if metric in latent_state
    }


def metric_status(metric: str, kernel: ObservationKernel) -> str:
    if metric in kernel.visible_metrics:
        return "OBSERVED_UNDER_ACTIVE_KERNEL"
    return "NOT_OBSERVED_UNDER_ACTIVE_KERNEL"


def cross_kernel_estimator_authority(required_metrics: set[str]) -> dict:
    old = rich_kernel()
    new = degraded_kernel()
    old_visible = required_metrics.issubset(old.visible_metrics)
    new_visible = required_metrics.issubset(new.visible_metrics)
    bridged = new.comparability_bridge_from_previous

    authorized = old_visible and new_visible and bridged
    return {
        "required_metrics": sorted(required_metrics),
        "old_kernel_visible": old_visible,
        "new_kernel_visible": new_visible,
        "comparability_bridge": bridged,
        "authorized": authorized,
        "decision": "AUTHORIZED" if authorized else "ABSTAIN_KERNEL_BREAK",
    }


def reporting_kernel_report_payload() -> dict:
    latent = {
        "revenue": 196.0,
        "operating_profit": -1.0,
        "stock_revenue": 150.0,
        "stock_revenue_ratio": 0.76,
        "arr": 600.0,
        "churn_rate": 0.12,
        "customer_count": 40.0,
        "average_unit_price": 5.0,
    }

    before = observe(latent, rich_kernel())
    after = observe(latent, degraded_kernel())
    arr_trend = cross_kernel_estimator_authority({"arr"})
    revenue_trend = cross_kernel_estimator_authority({"revenue"})

    gates = {
        "same_latent_state_has_different_observations": before != after,
        "arr_is_visible_before_and_hidden_after": (
            metric_status("arr", rich_kernel()) == "OBSERVED_UNDER_ACTIVE_KERNEL"
            and metric_status("arr", degraded_kernel())
            == "NOT_OBSERVED_UNDER_ACTIVE_KERNEL"
        ),
        "hidden_metric_is_not_encoded_as_zero": "arr" not in after,
        "arr_cross_kernel_estimator_abstains": (
            arr_trend["decision"] == "ABSTAIN_KERNEL_BREAK"
        ),
        "revenue_without_bridge_still_abstains_for_cross_kernel_estimator": (
            revenue_trend["decision"] == "ABSTAIN_KERNEL_BREAK"
        ),
        "new_kpi_set_requires_new_kernel_generation": (
            degraded_kernel().generation == rich_kernel().generation + 1
        ),
    }

    return {
        "experiment": "E080",
        "question": (
            "Should a KPI disclosure withdrawal be modeled as missing values "
            "inside one observation process, or as a change in the observation "
            "kernel itself?"
        ),
        "reference_latent_state": latent,
        "before_kernel": {
            "kernel_id": rich_kernel().kernel_id,
            "generation": rich_kernel().generation,
            "visible_metrics": sorted(rich_kernel().visible_metrics),
            "observation": before,
        },
        "after_kernel": {
            "kernel_id": degraded_kernel().kernel_id,
            "generation": degraded_kernel().generation,
            "visible_metrics": sorted(degraded_kernel().visible_metrics),
            "observation": after,
        },
        "arr_cross_kernel_authority": arr_trend,
        "revenue_cross_kernel_authority": revenue_trend,
        "promotion_gate": gates,
        "promoted_kernel_rule": (
            "reporting-policy-change-creates-new-observation-kernel-generation-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Reporting policy is part of the measurement model. A disclosure "
            "withdrawal changes the observation operator and creates a new "
            "kernel generation. Missing metrics are not zeros, and cross-kernel "
            "estimators fail closed until an explicit comparability bridge exists."
        ),
        "limitations": (
            "The latent numeric state is synthetic and exists only to prove "
            "the observation-kernel distinction. E080 does not infer Allied "
            "Architects' undisclosed ARR, churn, customer count, or unit price."
        ),
    }
