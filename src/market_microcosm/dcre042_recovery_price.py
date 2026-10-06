from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecoveryProvider:
    name: str
    max_build: float
    recovery_cost_per_unit: float

    def independent_build(self, payment_per_unit: float, perceived_gap: float) -> float:
        if payment_per_unit < 0.0 or perceived_gap < 0.0:
            raise ValueError("payment and gap must be non-negative")
        if payment_per_unit <= self.recovery_cost_per_unit:
            return 0.0
        return min(self.max_build, perceived_gap)


def frozen_providers() -> tuple[RecoveryProvider, RecoveryProvider]:
    return (
        RecoveryProvider("P1", max_build=40.0, recovery_cost_per_unit=1.0),
        RecoveryProvider("P2", max_build=40.0, recovery_cost_per_unit=1.0),
    )


def independent_recovery_market(
    payment_per_unit: float,
    *,
    shocked_capacity: float = 60.0,
    target_capacity: float = 100.0,
) -> dict:
    gap = max(0.0, target_capacity - shocked_capacity)
    builds = tuple(
        provider.independent_build(payment_per_unit, gap)
        for provider in frozen_providers()
    )
    final_capacity = shocked_capacity + sum(builds)
    return {
        "payment_per_unit": payment_per_unit,
        "perceived_gap": gap,
        "builds": builds,
        "final_capacity": final_capacity,
        "shortfall": max(0.0, target_capacity - final_capacity),
        "overshoot": max(0.0, final_capacity - target_capacity),
    }


def coordinated_recovery(
    *,
    payment_per_unit: float = 1.1,
    shocked_capacity: float = 60.0,
    target_capacity: float = 100.0,
) -> dict:
    providers = frozen_providers()
    gap = max(0.0, target_capacity - shocked_capacity)
    if payment_per_unit <= providers[0].recovery_cost_per_unit:
        builds = tuple(0.0 for _ in providers)
    else:
        share = gap / len(providers)
        builds = tuple(min(provider.max_build, share) for provider in providers)
    final_capacity = shocked_capacity + sum(builds)
    return {
        "builds": builds,
        "final_capacity": final_capacity,
        "shortfall": max(0.0, target_capacity - final_capacity),
        "overshoot": max(0.0, final_capacity - target_capacity),
    }


def frozen_recovery_price_market() -> dict:
    return {
        "low_payment": independent_recovery_market(0.9),
        "high_payment": independent_recovery_market(1.1),
        "coordinated": coordinated_recovery(payment_per_unit=1.1),
    }
