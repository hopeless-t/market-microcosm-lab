from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ThresholdActor:
    name: str
    threshold: float
    flexible_tasks: float = 10.0


@dataclass(frozen=True)
class ShockOutcome:
    price_gap: float
    active_responders: tuple[str, ...]
    flexible_a: float
    load_a: float
    load_b: float
    peak_load: float


def frozen_actors() -> tuple[ThresholdActor, ...]:
    return (
        ThresholdActor("T05", 5.0),
        ThresholdActor("T10", 10.0),
        ThresholdActor("T15", 15.0),
        ThresholdActor("T20", 20.0),
    )


def evaluate_common_shock(price_gap: float) -> ShockOutcome:
    if price_gap < 0.0:
        raise ValueError("price_gap must be non-negative")
    actors = frozen_actors()
    active = tuple(actor for actor in actors if price_gap > actor.threshold)
    active_names = tuple(actor.name for actor in active)

    # Balanced baseline: every actor initially places half of its flexible work in A.
    flexible_a = 20.0
    for actor in active:
        flexible_a -= actor.flexible_tasks / 2.0

    load_a = 40.0 + flexible_a
    load_b = 40.0 + 40.0 - flexible_a
    return ShockOutcome(
        price_gap=price_gap,
        active_responders=active_names,
        flexible_a=flexible_a,
        load_a=load_a,
        load_b=load_b,
        peak_load=max(load_a, load_b),
    )


def frozen_shock_comparison() -> dict[str, ShockOutcome]:
    return {
        "moderate": evaluate_common_shock(12.0),
        "large": evaluate_common_shock(25.0),
    }
