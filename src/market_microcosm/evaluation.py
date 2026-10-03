from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .policies import PolicySpec
from .scenarios import Scenario
from .toy_world import Action, ToyState, ToyWorld, observe


@dataclass(frozen=True)
class Evaluation:
    policy_name: str
    scenarios: int
    survived: int
    invariant_violations: int
    total_welfare: float
    total_minimum_reserve: float
    oracle_disagreements: int
    decisions: int

    @property
    def survival_rate(self) -> float:
        return self.survived / self.scenarios if self.scenarios else 0.0

    @property
    def mean_welfare(self) -> float:
        return self.total_welfare / self.scenarios if self.scenarios else 0.0

    @property
    def mean_minimum_reserve(self) -> float:
        return self.total_minimum_reserve / self.scenarios if self.scenarios else 0.0

    @property
    def oracle_disagreement_rate(self) -> float:
        return self.oracle_disagreements / self.decisions if self.decisions else 0.0


def evaluate_policy(
    world: ToyWorld,
    policy: PolicySpec,
    scenarios: tuple[Scenario, ...],
    *,
    observation_mode: str,
    oracle: Callable[[ToyState], Action] | None = None,
) -> Evaluation:
    survived = 0
    invariant_violations = 0
    total_welfare = 0.0
    total_minimum_reserve = 0.0
    disagreements = 0
    decisions = 0

    for scenario in scenarios:
        state = scenario.initial_state
        scenario_welfare = 0.0
        scenario_minimum = float("inf")
        alive = world.viable(state)

        for disturbance in scenario.disturbances:
            if not alive:
                break
            action = policy.act(observe(state, observation_mode))
            if not world.feasible(state, action):
                invariant_violations += 1
                alive = False
                break
            if oracle is not None:
                try:
                    oracle_choice = oracle(state)
                except ValueError:
                    oracle_choice = None
                if oracle_choice is not None and oracle_choice != action:
                    disagreements += 1
                decisions += 1
            state = world.step(state, action, disturbance)
            scenario_welfare += state.welfare
            scenario_minimum = min(scenario_minimum, state.minimum_reserve)
            alive = world.viable(state)

        if alive:
            survived += 1
        total_welfare += scenario_welfare
        if scenario_minimum != float("inf"):
            total_minimum_reserve += scenario_minimum

    return Evaluation(
        policy_name=policy.name,
        scenarios=len(scenarios),
        survived=survived,
        invariant_violations=invariant_violations,
        total_welfare=total_welfare,
        total_minimum_reserve=total_minimum_reserve,
        oracle_disagreements=disagreements,
        decisions=decisions,
    )
