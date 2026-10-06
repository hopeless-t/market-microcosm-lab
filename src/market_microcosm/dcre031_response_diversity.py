from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre030_price_oscillation import (
    oscillation_metrics,
    simulate_lagged_price_response,
)


@dataclass(frozen=True)
class CadenceActor:
    name: str
    update_phase: int
    flexible_tasks: float = 10.0


@dataclass(frozen=True)
class CadenceEpoch:
    epoch: int
    signal_a: float
    signal_b: float
    flexible_a: float
    load_a: float
    load_b: float


def frozen_actors() -> tuple[CadenceActor, ...]:
    return (
        CadenceActor("A0", 0),
        CadenceActor("A1", 0),
        CadenceActor("B0", 1),
        CadenceActor("B1", 1),
    )


def simulate_staggered_cadence(
    *,
    epochs: int = 6,
    initial_signal_a: float = 60.0,
    initial_signal_b: float = 40.0,
) -> tuple[CadenceEpoch, ...]:
    actors = frozen_actors()
    allocations = {actor.name: actor.flexible_tasks / 2.0 for actor in actors}
    signal_a = initial_signal_a
    signal_b = initial_signal_b
    rows: list[CadenceEpoch] = []

    for epoch in range(epochs):
        for actor in actors:
            if epoch % 2 != actor.update_phase:
                continue
            if signal_a < signal_b:
                allocations[actor.name] = actor.flexible_tasks
            elif signal_b < signal_a:
                allocations[actor.name] = 0.0
            else:
                allocations[actor.name] = actor.flexible_tasks / 2.0

        flexible_a = sum(allocations.values())
        load_a = 40.0 + flexible_a
        load_b = 40.0 + 40.0 - flexible_a
        rows.append(
            CadenceEpoch(
                epoch=epoch,
                signal_a=signal_a,
                signal_b=signal_b,
                flexible_a=flexible_a,
                load_a=load_a,
                load_b=load_b,
            )
        )
        signal_a = load_a
        signal_b = load_b

    return tuple(rows)


def cadence_metrics(rows: tuple[CadenceEpoch, ...]) -> dict[str, float]:
    peak = max(max(row.load_a, row.load_b) for row in rows)
    movement = sum(
        abs(rows[index].flexible_a - rows[index - 1].flexible_a)
        for index in range(1, len(rows))
    )
    return {"peak_load": peak, "flexible_movement": movement}


def frozen_cadence_comparison() -> dict:
    synchronized = simulate_lagged_price_response(responsive_fraction=1.0)
    staggered = simulate_staggered_cadence()
    return {
        "synchronized": synchronized,
        "staggered": staggered,
        "synchronized_metrics": oscillation_metrics(synchronized),
        "staggered_metrics": cadence_metrics(staggered),
    }
