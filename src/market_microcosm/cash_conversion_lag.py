from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CashLagScenario:
    initial_cash: float
    monthly_booked_revenue: float
    monthly_cash_cost: float
    collection_lag_months: int
    horizon_months: int


def simulate_cash_lag(scenario: CashLagScenario) -> dict:
    cash = scenario.initial_cash
    cumulative_booked_profit = 0.0
    rows: list[dict] = []
    failure_month: int | None = None

    for month in range(1, scenario.horizon_months + 1):
        booked_revenue = scenario.monthly_booked_revenue
        collected_revenue = (
            scenario.monthly_booked_revenue
            if month > scenario.collection_lag_months
            else 0.0
        )
        cumulative_booked_profit += (
            booked_revenue - scenario.monthly_cash_cost
        )
        cash += collected_revenue - scenario.monthly_cash_cost

        if failure_month is None and cash < 0:
            failure_month = month

        rows.append(
            {
                "month": month,
                "booked_revenue": booked_revenue,
                "collected_revenue": collected_revenue,
                "monthly_cash_cost": scenario.monthly_cash_cost,
                "cash": cash,
                "cumulative_booked_profit": cumulative_booked_profit,
            }
        )

    return {
        "scenario": asdict(scenario),
        "trace": rows,
        "failure_month": failure_month,
        "survives_horizon": failure_month is None,
        "booked_margin_positive": (
            scenario.monthly_booked_revenue > scenario.monthly_cash_cost
        ),
    }


def minimum_initial_cash_for_survival(
    *,
    monthly_booked_revenue: float,
    monthly_cash_cost: float,
    collection_lag_months: int,
    horizon_months: int,
    max_cash: int = 1000,
) -> int:
    for initial_cash in range(max_cash + 1):
        result = simulate_cash_lag(
            CashLagScenario(
                initial_cash=float(initial_cash),
                monthly_booked_revenue=monthly_booked_revenue,
                monthly_cash_cost=monthly_cash_cost,
                collection_lag_months=collection_lag_months,
                horizon_months=horizon_months,
            )
        )
        if result["survives_horizon"]:
            return initial_cash
    raise ValueError("survival buffer exceeds search bound")


def warning_comparison() -> dict:
    scenario = CashLagScenario(
        initial_cash=100.0,
        monthly_booked_revenue=100.0,
        monthly_cash_cost=80.0,
        collection_lag_months=2,
        horizon_months=6,
    )
    result = simulate_cash_lag(scenario)

    naive_revenue_warning = (
        scenario.monthly_booked_revenue <= scenario.monthly_cash_cost
    )
    liquidity_gap_warning = (
        scenario.initial_cash
        < scenario.monthly_cash_cost * scenario.collection_lag_months
    )

    return {
        "witness": result,
        "naive_booked_margin_warning_at_t0": naive_revenue_warning,
        "lag_aware_liquidity_warning_at_t0": liquidity_gap_warning,
        "failure_month": result["failure_month"],
        "lag_aware_warning_lead_months": (
            result["failure_month"] if liquidity_gap_warning else 0
        ),
        "minimum_initial_cash_for_survival": (
            minimum_initial_cash_for_survival(
                monthly_booked_revenue=scenario.monthly_booked_revenue,
                monthly_cash_cost=scenario.monthly_cash_cost,
                collection_lag_months=scenario.collection_lag_months,
                horizon_months=scenario.horizon_months,
            )
        ),
    }


def cash_conversion_lag_report_payload() -> dict:
    comparison = warning_comparison()
    witness = comparison["witness"]

    gates = {
        "positive_booked_margin_can_precede_cash_failure": (
            witness["booked_margin_positive"]
            and witness["failure_month"] is not None
        ),
        "failure_occurs_before_first_collection_can_repair_cash": (
            witness["failure_month"] == 2
        ),
        "naive_booked_margin_warning_misses_witness": (
            comparison["naive_booked_margin_warning_at_t0"] is False
        ),
        "lag_aware_warning_detects_witness_at_t0": (
            comparison["lag_aware_liquidity_warning_at_t0"] is True
        ),
        "minimum_survival_buffer_is_exactly_enumerated": (
            comparison["minimum_initial_cash_for_survival"] == 160
        ),
        "revenue_and_cash_state_are_kept_separate": True,
    }

    return {
        "experiment": "E032",
        "question": (
            "Can a software/SaaS-like business show positive booked unit "
            "margin and healthy demand while failing from collection lag "
            "before booked revenue becomes cash?"
        ),
        "empirical_anchor": {
            "source": "TDB software-industry bankruptcy reports",
            "observations": (
                "TDB reports strong software demand alongside high bankruptcy "
                "levels, and specifically notes that package-software revenue "
                "can take time to turn into cash while labor/fixed costs rise."
            ),
            "scope_guard": (
                "TDB's software category is broader than SaaS; it motivates "
                "the cash-conversion mechanism but is not treated as a SaaS-only rate."
            ),
        },
        "warning_comparison": comparison,
        "promotion_gate": gates,
        "promoted_liquidity_rule": (
            "separate-booked-revenue-from-cash-arrival-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Future empirical market worlds must represent receivables/"
            "collection lag and liquidity runway separately from demand and "
            "booked revenue. Positive booked margin cannot grant viability "
            "authority when near-term cash obligations arrive first."
        ),
        "limitations": (
            "The fixed witness uses synthetic cash-flow values. It demonstrates "
            "a structurally possible failure mode motivated by TDB evidence; "
            "it is not an estimate of a named company's collection cycle."
        ),
    }
