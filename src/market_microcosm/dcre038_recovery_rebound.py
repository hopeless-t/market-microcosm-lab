from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecoveryEpoch:
    epoch: int
    capacity: float
    recovery_increment: float
    demand: float
    service_shortfall: float
    recovery_resource: float


@dataclass(frozen=True)
class RecoveryResult:
    name: str
    epochs: tuple[RecoveryEpoch, ...]

    @property
    def total_shortfall(self) -> float:
        return sum(row.service_shortfall for row in self.epochs)

    @property
    def peak_recovery_resource(self) -> float:
        return max(row.recovery_resource for row in self.epochs)

    @property
    def total_recovery_resource(self) -> float:
        return sum(row.recovery_resource for row in self.epochs)


def simulate_recovery(
    name: str,
    increments: tuple[float, ...],
    *,
    shocked_capacity: float = 60.0,
    baseline_demand: float = 100.0,
    rebound_per_restored_unit: float = 0.5,
    recovery_resource_per_unit: float = 1.5,
) -> RecoveryResult:
    if min(shocked_capacity, baseline_demand, rebound_per_restored_unit, recovery_resource_per_unit) < 0.0:
        raise ValueError("model parameters must be non-negative")
    if any(value < 0.0 for value in increments):
        raise ValueError("recovery increments must be non-negative")

    rows = [
        RecoveryEpoch(
            epoch=0,
            capacity=shocked_capacity,
            recovery_increment=0.0,
            demand=baseline_demand,
            service_shortfall=max(0.0, baseline_demand - shocked_capacity),
            recovery_resource=0.0,
        )
    ]
    capacity = shocked_capacity
    for index, increment in enumerate(increments, start=1):
        capacity += increment
        demand = baseline_demand + rebound_per_restored_unit * increment
        rows.append(
            RecoveryEpoch(
                epoch=index,
                capacity=capacity,
                recovery_increment=increment,
                demand=demand,
                service_shortfall=max(0.0, demand - capacity),
                recovery_resource=increment * recovery_resource_per_unit,
            )
        )

    # One calm epoch exposes whether a second-wave shortfall persists after rebuilding stops.
    rows.append(
        RecoveryEpoch(
            epoch=len(increments) + 1,
            capacity=capacity,
            recovery_increment=0.0,
            demand=baseline_demand,
            service_shortfall=max(0.0, baseline_demand - capacity),
            recovery_resource=0.0,
        )
    )
    return RecoveryResult(name=name, epochs=tuple(rows))


def frozen_recovery_plans() -> dict[str, RecoveryResult]:
    return {
        "aggressive": simulate_recovery("AGGRESSIVE", (40.0,)),
        "damped": simulate_recovery("DAMPED", (20.0, 20.0)),
    }


def scalarized_loss(result: RecoveryResult, peak_resource_weight: float) -> float:
    if peak_resource_weight < 0.0:
        raise ValueError("peak resource weight must be non-negative")
    return result.total_shortfall + peak_resource_weight * result.peak_recovery_resource


def peak_weight_knee() -> float:
    aggressive = frozen_recovery_plans()["aggressive"]
    damped = frozen_recovery_plans()["damped"]
    shortfall_advantage = damped.total_shortfall - aggressive.total_shortfall
    peak_penalty = aggressive.peak_recovery_resource - damped.peak_recovery_resource
    if peak_penalty <= 0.0:
        raise ValueError("no recovery-peak tradeoff")
    return shortfall_advantage / peak_penalty
