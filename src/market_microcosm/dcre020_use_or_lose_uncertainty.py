from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DemandState:
    name: str
    probability: float
    demand: float


@dataclass(frozen=True)
class ObligationOutcome:
    policy: str
    expected_activation_resource: float
    expected_idle_capacity: float
    expected_unmet_demand: float
    expected_served_demand: float


def frozen_demand_states() -> tuple[DemandState, ...]:
    return (
        DemandState("LOW", 0.5, 100.0),
        DemandState("HIGH", 0.5, 160.0),
    )


def evaluate_policy(
    *,
    policy: str,
    force_full_deployment: bool,
    baseline_capacity: float = 100.0,
    capacity_right: float = 60.0,
    activation_resource_per_capacity: float = 0.5,
) -> ObligationOutcome:
    activation = 0.0
    idle = 0.0
    unmet = 0.0
    served = 0.0

    for state in frozen_demand_states():
        residual_demand = max(0.0, state.demand - baseline_capacity)
        deploy = (
            capacity_right
            if force_full_deployment
            else min(capacity_right, residual_demand)
        )
        total_capacity = baseline_capacity + deploy
        state_served = min(state.demand, total_capacity)
        activation += state.probability * deploy * activation_resource_per_capacity
        idle += state.probability * max(0.0, total_capacity - state.demand)
        unmet += state.probability * max(0.0, state.demand - total_capacity)
        served += state.probability * state_served

    return ObligationOutcome(
        policy=policy,
        expected_activation_resource=activation,
        expected_idle_capacity=idle,
        expected_unmet_demand=unmet,
        expected_served_demand=served,
    )


def frozen_use_or_lose_uncertainty() -> dict[str, ObligationOutcome]:
    return {
        "flexible": evaluate_policy(
            policy="DEMAND_CONTINGENT_DEPLOYMENT",
            force_full_deployment=False,
        ),
        "use_or_lose": evaluate_policy(
            policy="RIGID_USE_OR_LOSE",
            force_full_deployment=True,
        ),
    }
