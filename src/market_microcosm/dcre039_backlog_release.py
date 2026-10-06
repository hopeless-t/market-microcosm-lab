from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BacklogEpoch:
    epoch: int
    starting_backlog: float
    attempted_release: float
    demand: float
    served: float
    new_shortfall: float
    ending_backlog: float


@dataclass(frozen=True)
class BacklogResult:
    policy: str
    epochs: tuple[BacklogEpoch, ...]

    @property
    def peak_demand(self) -> float:
        return max(row.demand for row in self.epochs)

    @property
    def total_new_shortfall(self) -> float:
        return sum(row.new_shortfall for row in self.epochs)

    @property
    def ending_backlog(self) -> float:
        return self.epochs[-1].ending_backlog


def simulate_backlog_release(
    policy: str,
    *,
    initial_backlog: float = 40.0,
    baseline_demand: float = 100.0,
    recovered_capacity: float = 120.0,
    max_epochs: int = 4,
) -> BacklogResult:
    if min(initial_backlog, baseline_demand, recovered_capacity) < 0.0:
        raise ValueError("workload parameters must be non-negative")
    if max_epochs < 1:
        raise ValueError("max_epochs must be positive")
    if policy not in {"RELEASE_ALL", "CAPACITY_AWARE"}:
        raise ValueError(policy)

    backlog = initial_backlog
    rows: list[BacklogEpoch] = []
    for epoch in range(max_epochs):
        if backlog <= 0.0:
            break
        if policy == "RELEASE_ALL":
            attempted = backlog
        else:
            spare = max(0.0, recovered_capacity - baseline_demand)
            attempted = min(backlog, spare)

        demand = baseline_demand + attempted
        served = min(demand, recovered_capacity)
        served_backlog = max(0.0, served - baseline_demand)
        new_shortfall = max(0.0, attempted - served_backlog)
        ending = backlog - served_backlog
        rows.append(
            BacklogEpoch(
                epoch=epoch,
                starting_backlog=backlog,
                attempted_release=attempted,
                demand=demand,
                served=served,
                new_shortfall=new_shortfall,
                ending_backlog=ending,
            )
        )
        backlog = ending

    return BacklogResult(policy=policy, epochs=tuple(rows))


def frozen_backlog_recovery() -> dict[str, BacklogResult]:
    return {
        "release_all": simulate_backlog_release("RELEASE_ALL"),
        "capacity_aware": simulate_backlog_release("CAPACITY_AWARE"),
    }
