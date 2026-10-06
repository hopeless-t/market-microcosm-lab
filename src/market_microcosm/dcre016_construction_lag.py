from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapacityPeriod:
    period: int
    demand: float
    capacity: float
    unmet_demand: float
    idle_capacity: float
    next_adjustment: float


@dataclass(frozen=True)
class CapacityTrace:
    policy: str
    periods: tuple[CapacityPeriod, ...]
    total_mismatch: float
    total_unmet: float
    total_idle: float
    capacity_movement: float


def frozen_demand_trace() -> tuple[float, ...]:
    return (100.0, 180.0, 100.0, 180.0, 100.0, 180.0)


def simulate_capacity_response(
    *,
    policy: str,
    adjustment_fraction: float,
    initial_capacity: float = 100.0,
    demand_trace: tuple[float, ...] | None = None,
) -> CapacityTrace:
    if not 0.0 <= adjustment_fraction <= 1.0:
        raise ValueError("adjustment_fraction must be within [0, 1]")
    if initial_capacity <= 0.0:
        raise ValueError("initial_capacity must be positive")

    demand_trace = demand_trace or frozen_demand_trace()
    capacity = initial_capacity
    pending_adjustment = 0.0
    rows: list[CapacityPeriod] = []

    for period, demand in enumerate(demand_trace):
        capacity = max(0.0, capacity + pending_adjustment)
        gap = demand - capacity
        unmet = max(0.0, gap)
        idle = max(0.0, -gap)
        pending_adjustment = adjustment_fraction * gap
        rows.append(
            CapacityPeriod(
                period=period,
                demand=demand,
                capacity=capacity,
                unmet_demand=unmet,
                idle_capacity=idle,
                next_adjustment=pending_adjustment,
            )
        )

    movement = sum(
        abs(rows[index].capacity - rows[index - 1].capacity)
        for index in range(1, len(rows))
    )
    total_unmet = sum(row.unmet_demand for row in rows)
    total_idle = sum(row.idle_capacity for row in rows)
    return CapacityTrace(
        policy=policy,
        periods=tuple(rows),
        total_mismatch=total_unmet + total_idle,
        total_unmet=total_unmet,
        total_idle=total_idle,
        capacity_movement=movement,
    )


def frozen_construction_lag() -> dict[str, CapacityTrace]:
    return {
        "full_reactive": simulate_capacity_response(
            policy="FULL_REACTIVE_ONE_PERIOD_LAG",
            adjustment_fraction=1.0,
        ),
        "damped_half": simulate_capacity_response(
            policy="DAMPED_HALF_RESPONSE",
            adjustment_fraction=0.5,
        ),
    }
