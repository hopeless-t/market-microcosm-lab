from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre028_temporal_resources import evaluate_temporal_allocation


@dataclass(frozen=True)
class ShiftActor:
    name: str
    flexible_tasks: float = 20.0


def frozen_actors() -> tuple[ShiftActor, ShiftActor]:
    return (ShiftActor("A"), ShiftActor("B"))


def actor_independent_shift(actor: ShiftActor) -> float:
    # Each actor evaluates the destination against the frozen baseline and
    # does not account for the other actor making the same move.
    assumed_total_flexible = actor.flexible_tasks
    assumed_offpeak_tasks = 20.0 + assumed_total_flexible
    assumed_offpeak_water = assumed_offpeak_tasks * 0.4
    if assumed_offpeak_water <= 20.0:
        return actor.flexible_tasks
    return 0.0


def aggregate_outcome(offpeak_shifts: tuple[float, ...]):
    total_flexible = sum(actor.flexible_tasks for actor in frozen_actors())
    total_offpeak_shift = sum(offpeak_shifts)
    flexible_peak = total_flexible - total_offpeak_shift
    return evaluate_temporal_allocation(
        flexible_peak,
        flexible_total=total_flexible,
    )


def independent_herd_outcome():
    actors = frozen_actors()
    shifts = tuple(actor_independent_shift(actor) for actor in actors)
    return shifts, aggregate_outcome(shifts)


def coordinated_symmetric_outcome():
    shifts = (15.0, 15.0)
    return shifts, aggregate_outcome(shifts)
