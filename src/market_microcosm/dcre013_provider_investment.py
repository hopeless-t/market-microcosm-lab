from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre012_capacity_race import demand_after_efficiency


@dataclass(frozen=True)
class InvestmentChoice:
    policy: str
    capacity: float
    demand: float
    served: float
    resource_used: float
    verified_output: float
    profit: float


CAPACITY_GRID = (100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0)


def fixed_resource_cost(resource_used: float, *, unit_price: float = 0.20) -> float:
    if resource_used < 0.0 or unit_price < 0.0:
        raise ValueError("resource and price must be non-negative")
    return unit_price * resource_used


def scarcity_resource_cost(
    resource_used: float,
    *,
    unit_price: float = 0.20,
    soft_threshold: float = 72.0,
    congestion_slope: float = 0.03,
) -> float:
    if min(resource_used, unit_price, soft_threshold, congestion_slope) < 0.0:
        raise ValueError("resource-price parameters must be non-negative")
    excess = max(0.0, resource_used - soft_threshold)
    return unit_price * resource_used + congestion_slope * excess**2


def choose_capacity(
    *,
    policy: str,
    revenue_mode: str,
    dynamic_price: bool,
    efficiency_ratio: float = 0.60,
    demand_elasticity: float = 1.50,
    baseline_capacity: float = 100.0,
    verification_capacity: float = 120.0,
    task_revenue: float = 1.0,
    capacity_cost: float = 0.15,
) -> InvestmentChoice:
    if revenue_mode not in {"VOLUME", "VERIFIED"}:
        raise ValueError(revenue_mode)

    demand = demand_after_efficiency(efficiency_ratio, demand_elasticity)
    rows: list[InvestmentChoice] = []

    for capacity in CAPACITY_GRID:
        served = min(capacity, demand)
        resource_used = efficiency_ratio * served
        verified = min(served, verification_capacity)
        billable = served if revenue_mode == "VOLUME" else verified
        revenue = task_revenue * billable
        resource_cost = (
            scarcity_resource_cost(resource_used)
            if dynamic_price
            else fixed_resource_cost(resource_used)
        )
        capex = capacity_cost * max(0.0, capacity - baseline_capacity)
        rows.append(
            InvestmentChoice(
                policy=policy,
                capacity=capacity,
                demand=demand,
                served=served,
                resource_used=resource_used,
                verified_output=verified,
                profit=revenue - resource_cost - capex,
            )
        )

    return max(rows, key=lambda row: (row.profit, -row.capacity))


def frozen_provider_choices() -> dict[str, InvestmentChoice]:
    return {
        "fixed_volume": choose_capacity(
            policy="FIXED_PRICE_VOLUME_REVENUE",
            revenue_mode="VOLUME",
            dynamic_price=False,
        ),
        "scarcity_volume": choose_capacity(
            policy="SCARCITY_PRICE_VOLUME_REVENUE",
            revenue_mode="VOLUME",
            dynamic_price=True,
        ),
        "scarcity_verified": choose_capacity(
            policy="SCARCITY_PRICE_VERIFIED_REVENUE",
            revenue_mode="VERIFIED",
            dynamic_price=True,
        ),
    }
