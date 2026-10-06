from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Provider:
    name: str
    capacity: float
    energy_per_task: float
    water_per_task: float
    fixed_cost: float
    service_credit: float = 0.0

    def __post_init__(self) -> None:
        if min(
            self.capacity,
            self.energy_per_task,
            self.water_per_task,
            self.fixed_cost,
            self.service_credit,
        ) < 0.0:
            raise ValueError("provider values must be non-negative")


@dataclass(frozen=True)
class EntryOutcome:
    policy: str
    active_providers: tuple[str, ...]
    total_capacity: float
    total_energy: float
    total_water: float
    service_viable: bool
    energy_viable: bool
    water_viable: bool
    public_credit_cost: float

    @property
    def jointly_viable(self) -> bool:
        return self.service_viable and self.energy_viable and self.water_viable


def frozen_providers(*, local_credit: float = 0.0) -> tuple[Provider, ...]:
    return (
        Provider("SCALE", 70.0, 0.75, 0.15, 15.0),
        Provider("LOCAL", 35.0, 0.90, 0.08, 20.0, local_credit),
        Provider("WET", 60.0, 0.65, 0.50, 10.0),
    )


def provider_profit(
    provider: Provider,
    *,
    task_revenue: float,
    energy_price: float,
    water_price: float,
) -> float:
    margin_per_task = (
        task_revenue
        - energy_price * provider.energy_per_task
        - water_price * provider.water_per_task
    )
    return (
        margin_per_task * provider.capacity
        - provider.fixed_cost
        + provider.service_credit
    )


def evaluate_market(
    *,
    policy: str,
    energy_price: float,
    water_price: float,
    local_credit: float = 0.0,
    task_revenue: float = 1.0,
    service_floor: float = 100.0,
    energy_ceiling: float = 100.0,
    water_ceiling: float = 25.0,
) -> EntryOutcome:
    providers = frozen_providers(local_credit=local_credit)
    active = tuple(
        provider
        for provider in providers
        if provider_profit(
            provider,
            task_revenue=task_revenue,
            energy_price=energy_price,
            water_price=water_price,
        ) >= 0.0
    )
    capacity = sum(provider.capacity for provider in active)
    energy = sum(provider.capacity * provider.energy_per_task for provider in active)
    water = sum(provider.capacity * provider.water_per_task for provider in active)
    return EntryOutcome(
        policy=policy,
        active_providers=tuple(provider.name for provider in active),
        total_capacity=capacity,
        total_energy=energy,
        total_water=water,
        service_viable=capacity >= service_floor,
        energy_viable=energy <= energy_ceiling,
        water_viable=water <= water_ceiling,
        public_credit_cost=sum(provider.service_credit for provider in providers),
    )


def frozen_entry_exit() -> dict[str, EntryOutcome]:
    return {
        "low_price": evaluate_market(
            policy="LOW_RESOURCE_PRICE",
            energy_price=0.10,
            water_price=0.10,
        ),
        "scarcity_price": evaluate_market(
            policy="JOINT_SCARCITY_PRICE",
            energy_price=0.40,
            water_price=1.20,
        ),
        "scarcity_plus_service_credit": evaluate_market(
            policy="JOINT_PRICE_PLUS_LOCAL_SERVICE_CREDIT",
            energy_price=0.40,
            water_price=1.20,
            local_credit=3.0,
        ),
    }
