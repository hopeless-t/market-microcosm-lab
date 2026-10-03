from __future__ import annotations

from dataclasses import dataclass

from .toy_world import Action, ToyObservation


@dataclass(frozen=True)
class PolicySpec:
    name: str
    correction_threshold: int = 1
    platform_floor: int = 1

    def act(self, observation: ToyObservation) -> Action:
        if observation.platform <= self.platform_floor:
            return Action.BALANCED

        gap = observation.developer_a - observation.developer_b
        if gap <= -self.correction_threshold:
            return Action.SUPPORT_A
        if gap >= self.correction_threshold:
            return Action.SUPPORT_B
        return Action.BALANCED


def candidate_family(thresholds: tuple[int, ...] = (1, 2, 3)) -> tuple[PolicySpec, ...]:
    return tuple(
        PolicySpec(name=f"reserve-balancer-t{t}", correction_threshold=t)
        for t in thresholds
    )
