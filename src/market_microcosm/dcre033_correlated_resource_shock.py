from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegionalShockResult:
    capacity_a: float
    capacity_b: float
    total_workload: float
    selected_a: float | None
    selected_b: float | None

    @property
    def feasible(self) -> bool:
        return self.selected_a is not None and self.selected_b is not None

    @property
    def aggregate_capacity(self) -> float:
        return self.capacity_a + self.capacity_b


def exact_reallocation(
    capacity_a: float,
    capacity_b: float,
    *,
    total_workload: float = 100.0,
) -> RegionalShockResult:
    if min(capacity_a, capacity_b, total_workload) < 0.0:
        raise ValueError("capacities and workload must be non-negative")
    candidates: list[tuple[float, float]] = []
    for tasks_a in (0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0):
        tasks_b = total_workload - tasks_a
        if tasks_a <= capacity_a and tasks_b <= capacity_b:
            candidates.append((tasks_a, tasks_b))
    if not candidates:
        return RegionalShockResult(
            capacity_a=capacity_a,
            capacity_b=capacity_b,
            total_workload=total_workload,
            selected_a=None,
            selected_b=None,
        )
    selected_a, selected_b = min(
        candidates,
        key=lambda pair: (abs(pair[0] - pair[1]), pair[0]),
    )
    return RegionalShockResult(
        capacity_a=capacity_a,
        capacity_b=capacity_b,
        total_workload=total_workload,
        selected_a=selected_a,
        selected_b=selected_b,
    )


def frozen_resource_shocks() -> dict[str, RegionalShockResult]:
    return {
        "baseline": exact_reallocation(60.0, 60.0),
        "independent_shock": exact_reallocation(40.0, 60.0),
        "common_shock": exact_reallocation(40.0, 40.0),
    }
