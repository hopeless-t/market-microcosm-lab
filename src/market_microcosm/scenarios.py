from __future__ import annotations

from dataclasses import dataclass
import random

from .toy_world import Disturbance, ToyState


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    initial_state: ToyState
    disturbances: tuple[Disturbance, ...]


def generate_scenarios(
    *,
    seeds: tuple[int, ...],
    horizon: int,
    initial_states: tuple[ToyState, ...],
) -> tuple[Scenario, ...]:
    if not initial_states:
        raise ValueError("initial_states must not be empty")

    scenarios: list[Scenario] = []
    ds = tuple(Disturbance)
    for seed in seeds:
        rng = random.Random(seed)
        initial = initial_states[rng.randrange(len(initial_states))]
        disturbances = tuple(ds[rng.randrange(len(ds))] for _ in range(horizon))
        scenarios.append(Scenario(f"seed-{seed}", initial, disturbances))
    return tuple(scenarios)
