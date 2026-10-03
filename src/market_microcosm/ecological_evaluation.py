from __future__ import annotations

from dataclasses import dataclass
import math
import random

from .ecology import MarketWorld, Mechanism


@dataclass(frozen=True)
class MarketEvaluation:
    mechanism_name: str
    scenarios: int
    survived: int
    invariant_violations: int
    mean_health: float
    mean_user_utility: float
    mean_diversity: float
    mean_active_developers: float
    mean_active_publishers: float
    mean_platform_cash: float
    total_entries: int
    total_exits: int

    @property
    def survival_rate(self) -> float:
        return self.survived / self.scenarios if self.scenarios else 0.0

    @property
    def survival_lcb95(self) -> float:
        if not self.scenarios:
            return 0.0
        z = 1.959963984540054
        n = self.scenarios
        p = self.survival_rate
        denom = 1.0 + z * z / n
        centre = p + z * z / (2.0 * n)
        radius = z * math.sqrt((p * (1.0 - p) + z * z / (4.0 * n)) / n)
        return max(0.0, (centre - radius) / denom)


def evaluate_mechanism(
    world: MarketWorld,
    mechanism: Mechanism,
    *,
    seeds: tuple[int, ...],
    horizon: int,
) -> MarketEvaluation:
    survived = 0
    invariant_violations = 0
    health = 0.0
    utility = 0.0
    diversity = 0.0
    active_developers = 0.0
    active_publishers = 0.0
    platform_cash = 0.0
    total_entries = 0
    total_exits = 0

    for seed in seeds:
        rng = random.Random(seed)
        state = world.initial_state()
        scenario_health = 0.0
        scenario_utility = 0.0
        scenario_diversity = 0.0
        scenario_devs = 0.0
        scenario_pubs = 0.0
        scenario_platform = 0.0
        months = 0
        alive = world.viable(state)

        for _ in range(horizon):
            if not alive:
                break
            try:
                result = world.step(state, mechanism, rng)
            except AssertionError:
                invariant_violations += 1
                alive = False
                break

            state = result.state
            metrics = result.metrics
            months += 1
            scenario_health += metrics.health
            scenario_utility += metrics.user_utility
            scenario_diversity += metrics.diversity
            scenario_devs += metrics.active_developers
            scenario_pubs += metrics.active_publishers
            scenario_platform += metrics.platform_cash
            alive = world.viable(state)

        if alive and months == horizon:
            survived += 1

        divisor = max(1, months)
        health += scenario_health / divisor
        utility += scenario_utility / divisor
        diversity += scenario_diversity / divisor
        active_developers += scenario_devs / divisor
        active_publishers += scenario_pubs / divisor
        platform_cash += scenario_platform / divisor
        total_entries += state.cumulative_entries
        total_exits += state.cumulative_exits

    n = max(1, len(seeds))
    return MarketEvaluation(
        mechanism_name=mechanism.name,
        scenarios=len(seeds),
        survived=survived,
        invariant_violations=invariant_violations,
        mean_health=health / n,
        mean_user_utility=utility / n,
        mean_diversity=diversity / n,
        mean_active_developers=active_developers / n,
        mean_active_publishers=active_publishers / n,
        mean_platform_cash=platform_cash / n,
        total_entries=total_entries,
        total_exits=total_exits,
    )
