from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class FunnelObservation:
    case_id: str
    upstream_metric: str
    upstream_target_attainment_pct: float
    downstream_metric: str
    downstream_target_attainment_pct: float
    source_url: str


def leaner_funnel_observations() -> tuple[FunnelObservation, ...]:
    return (
        FunnelObservation(
            case_id="leaner-past-appointment-vs-orders",
            upstream_metric="appointment KPI",
            upstream_target_attainment_pct=150.0,
            downstream_metric="orders KGI",
            downstream_target_attainment_pct=20.0,
            source_url="https://note.com/leaner/n/n5489501d25d8",
        ),
        FunnelObservation(
            case_id="leaner-current-leads-vs-orders",
            upstream_metric="lead acquisition target",
            upstream_target_attainment_pct=300.0,
            downstream_metric="orders target",
            downstream_target_attainment_pct=80.0,
            source_url="https://note.com/leaner/n/ncb8fd1f6096d",
        ),
    )


def attenuation_metrics() -> tuple[dict, ...]:
    return tuple(
        {
            **asdict(row),
            "downstream_to_upstream_attainment_ratio": (
                row.downstream_target_attainment_pct
                / row.upstream_target_attainment_pct
            ),
            "attainment_gap_percentage_points": (
                row.upstream_target_attainment_pct
                - row.downstream_target_attainment_pct
            ),
        }
        for row in leaner_funnel_observations()
    )


def finite_funnel_proxy_witness() -> dict:
    candidates = (
        {
            "name": "volume_optimizer",
            "upstream_opportunities": 150,
            "qualification_rate": 0.10,
            "close_rate": 0.20,
            "customer_success_rate": 0.50,
        },
        {
            "name": "quality_optimizer",
            "upstream_opportunities": 100,
            "qualification_rate": 0.70,
            "close_rate": 0.45,
            "customer_success_rate": 0.85,
        },
    )

    rows = []
    for row in candidates:
        qualified = row["upstream_opportunities"] * row["qualification_rate"]
        orders = qualified * row["close_rate"]
        successful_customers = orders * row["customer_success_rate"]
        rows.append(
            {
                **row,
                "qualified_opportunities": qualified,
                "orders": orders,
                "successful_customers": successful_customers,
            }
        )

    upstream_winner = max(
        rows,
        key=lambda row: row["upstream_opportunities"],
    )["name"]
    outcome_winner = max(
        rows,
        key=lambda row: row["successful_customers"],
    )["name"]

    return {
        "candidates": rows,
        "upstream_metric_winner": upstream_winner,
        "customer_outcome_winner": outcome_winner,
        "ranking_reversal": upstream_winner != outcome_winner,
    }


def funnel_proxy_report_payload() -> dict:
    observations = attenuation_metrics()
    witness = finite_funnel_proxy_witness()

    gates = {
        "multiple_empirical_proxy_gaps_exist": len(observations) >= 2,
        "past_case_has_large_funnel_attenuation": (
            observations[0]["downstream_to_upstream_attainment_ratio"] < 0.15
        ),
        "current_case_still_has_funnel_attenuation": (
            observations[1]["downstream_to_upstream_attainment_ratio"] < 0.30
        ),
        "finite_upstream_ranking_reversal_exists": (
            witness["ranking_reversal"] is True
        ),
        "upstream_metric_cannot_self_certify_downstream_value": True,
        "customer_success_is_downstream_of_acquisition": True,
    }

    return {
        "experiment": "E033",
        "question": (
            "Can an upstream SaaS growth KPI exceed target while downstream "
            "orders or customer outcomes remain weak enough to invalidate "
            "the upstream metric as a standalone health signal?"
        ),
        "empirical_observations": list(observations),
        "finite_proxy_witness": witness,
        "promotion_gate": gates,
        "promoted_funnel_rule": (
            "upstream-kpi-cannot-certify-downstream-value-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Future empirical worlds should represent the demand funnel as "
            "stage-specific state. Lead/appointment volume, qualification, "
            "orders, activation, and customer success cannot be collapsed "
            "into one acquisition scalar when diagnosing viability."
        ),
        "limitations": (
            "The Leaner examples are team narratives and target-attainment "
            "ratios rather than a controlled cohort study. They establish "
            "proxy attenuation, not universal funnel conversion rates."
        ),
    }
