from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WaitActor:
    actor_id: str
    arrival_order: int
    budget: float
    private_wait_benefit: float
    system_wait_value: float
    essential: bool = False

    def __post_init__(self) -> None:
        if self.arrival_order < 0:
            raise ValueError("arrival_order must be non-negative")
        if min(self.budget, self.private_wait_benefit, self.system_wait_value) < 0.0:
            raise ValueError("economic values must be non-negative")


def frozen_actors() -> tuple[WaitActor, ...]:
    return (
        WaitActor("PREMIUM", 0, 0.20, 0.08, 0.08, False),
        WaitActor("ESSENTIAL", 1, 0.03, 0.02, 0.50, True),
        WaitActor("ROUTINE", 2, 0.10, 0.06, 0.06, False),
        WaitActor("BATCH", 3, 0.08, 0.05, 0.05, False),
    )


def fifo_allocate(actors: tuple[WaitActor, ...], *, capacity: int = 1) -> tuple[WaitActor, ...]:
    if capacity < 1:
        raise ValueError("capacity must be positive")
    return tuple(sorted(actors, key=lambda actor: (actor.arrival_order, actor.actor_id))[:capacity])


def posted_price_allocate(
    actors: tuple[WaitActor, ...], *, price: float = 0.05, capacity: int = 1
) -> tuple[WaitActor, ...]:
    if price < 0.0 or capacity < 1:
        raise ValueError("price must be non-negative and capacity positive")
    eligible = [actor for actor in actors if actor.budget >= price]
    eligible.sort(key=lambda actor: (-actor.private_wait_benefit, actor.actor_id))
    return tuple(eligible[:capacity])


def system_value_allocate(
    actors: tuple[WaitActor, ...], *, capacity: int = 1
) -> tuple[WaitActor, ...]:
    if capacity < 1:
        raise ValueError("capacity must be positive")
    ranked = sorted(
        actors,
        key=lambda actor: (-actor.system_wait_value, -int(actor.essential), actor.actor_id),
    )
    return tuple(ranked[:capacity])


def allocation_value(selected: tuple[WaitActor, ...]) -> float:
    return sum(actor.system_wait_value for actor in selected)
