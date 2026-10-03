from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Iterable


class Action(str, Enum):
    BALANCED = "balanced"
    SUPPORT_A = "support_a"
    SUPPORT_B = "support_b"
    CONSERVE = "conserve"


class Disturbance(str, Enum):
    NONE = "none"
    SHOCK_A = "shock_a"
    SHOCK_B = "shock_b"


PAYOUTS: dict[Action, tuple[int, int]] = {
    Action.BALANCED: (1, 1),
    Action.SUPPORT_A: (2, 1),
    Action.SUPPORT_B: (1, 2),
    Action.CONSERVE: (0, 0),
}


@dataclass(frozen=True, order=True)
class ToyState:
    platform: int
    developer_a: int
    developer_b: int

    @property
    def minimum_reserve(self) -> int:
        return min(self.platform, self.developer_a, self.developer_b)

    @property
    def welfare(self) -> int:
        return self.platform + self.developer_a + self.developer_b


@dataclass(frozen=True)
class ToyObservation:
    platform: int
    developer_a: int
    developer_b: int


@dataclass(frozen=True)
class ToyWorld:
    cap: int = 4
    subscription_revenue: int = 4
    platform_burn: int = 1
    developer_burn: int = 1

    @property
    def actions(self) -> tuple[Action, ...]:
        return tuple(Action)

    @property
    def disturbances(self) -> tuple[Disturbance, ...]:
        return tuple(Disturbance)

    def states(self) -> Iterable[ToyState]:
        rng = range(self.cap + 1)
        for p, a, b in product(rng, repeat=3):
            yield ToyState(p, a, b)

    def viable(self, state: ToyState) -> bool:
        return state.platform >= 1 and state.developer_a >= 1 and state.developer_b >= 1

    def feasible(self, state: ToyState, action: Action) -> bool:
        pa, pb = PAYOUTS[action]
        available = state.platform + self.subscription_revenue - self.platform_burn
        return available >= pa + pb

    def step(self, state: ToyState, action: Action, disturbance: Disturbance) -> ToyState:
        if not self.feasible(state, action):
            raise ValueError("infeasible action")

        pa, pb = PAYOUTS[action]
        shock_a = int(disturbance is Disturbance.SHOCK_A)
        shock_b = int(disturbance is Disturbance.SHOCK_B)

        platform = state.platform + self.subscription_revenue - self.platform_burn - pa - pb
        dev_a = state.developer_a + pa - self.developer_burn - shock_a
        dev_b = state.developer_b + pb - self.developer_burn - shock_b

        return ToyState(
            platform=max(0, min(self.cap, platform)),
            developer_a=max(0, min(self.cap, dev_a)),
            developer_b=max(0, min(self.cap, dev_b)),
        )


def observe(state: ToyState, mode: str = "full") -> ToyObservation:
    if mode == "full":
        return ToyObservation(state.platform, state.developer_a, state.developer_b)
    if mode == "coarse":
        def bucket(x: int) -> int:
            return 0 if x == 0 else (1 if x == 1 else 2)
        return ToyObservation(bucket(state.platform), bucket(state.developer_a), bucket(state.developer_b))
    raise ValueError(f"unknown observation mode: {mode}")
