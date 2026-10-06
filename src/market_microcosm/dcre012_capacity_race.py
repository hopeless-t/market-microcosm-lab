from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapacityRaceState:
    demand: float
    capacity: float
    served: float
    resource_used: float
    verified_output: float


def demand_after_efficiency(
    efficiency_ratio: float,
    demand_elasticity: float,
    *,
    baseline_demand: float = 100.0,
) -> float:
    if not 0.0 < efficiency_ratio <= 1.0:
        raise ValueError("efficiency_ratio must be within (0, 1]")
    if demand_elasticity < 0.0 or baseline_demand <= 0.0:
        raise ValueError("elasticity must be non-negative and demand positive")
    return baseline_demand * (1.0 / efficiency_ratio) ** demand_elasticity


def state_for_capacity(
    capacity: float,
    *,
    efficiency_ratio: float = 0.6,
    demand_elasticity: float = 1.5,
    baseline_demand: float = 100.0,
    verification_capacity: float = 120.0,
) -> CapacityRaceState:
    if capacity <= 0.0 or verification_capacity <= 0.0:
        raise ValueError("capacities must be positive")
    demand = demand_after_efficiency(
        efficiency_ratio,
        demand_elasticity,
        baseline_demand=baseline_demand,
    )
    served = min(demand, capacity)
    return CapacityRaceState(
        demand=demand,
        capacity=capacity,
        served=served,
        resource_used=efficiency_ratio * served,
        verified_output=min(served, verification_capacity),
    )


def frozen_capacity_race() -> dict[str, CapacityRaceState | float]:
    efficiency_ratio = 0.6
    baseline_capacity = 100.0
    resource_ceiling = 100.0
    verification_capacity = 120.0
    demand_elasticity = 1.5

    no_reinvestment = state_for_capacity(
        baseline_capacity,
        efficiency_ratio=efficiency_ratio,
        demand_elasticity=demand_elasticity,
        verification_capacity=verification_capacity,
    )

    resource_ceiling_capacity = resource_ceiling / efficiency_ratio
    resource_reinvestment = state_for_capacity(
        resource_ceiling_capacity,
        efficiency_ratio=efficiency_ratio,
        demand_elasticity=demand_elasticity,
        verification_capacity=verification_capacity,
    )

    verification_aware_capacity = min(
        verification_capacity,
        resource_ceiling_capacity,
        no_reinvestment.demand,
    )
    verification_aware = state_for_capacity(
        verification_aware_capacity,
        efficiency_ratio=efficiency_ratio,
        demand_elasticity=demand_elasticity,
        verification_capacity=verification_capacity,
    )

    return {
        "no_reinvestment": no_reinvestment,
        "resource_reinvestment": resource_reinvestment,
        "verification_aware": verification_aware,
        "resource_waste_vs_verification_aware": (
            resource_reinvestment.resource_used - verification_aware.resource_used
        ),
        "resource_waste_fraction": (
            resource_reinvestment.resource_used - verification_aware.resource_used
        ) / resource_reinvestment.resource_used,
    }
