from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Actor:
    actor_id: str
    kind: str
    cash: float
    burn: float = 0.0


@dataclass(frozen=True)
class Transfer:
    src: str
    dst: str
    amount: float

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("transfer amount must be non-negative")


@dataclass(frozen=True)
class EcosystemState:
    t: int
    actors: tuple[Actor, ...]
    user_utility: float
    service_quality: float

    @property
    def total_cash(self) -> float:
        return sum(a.cash for a in self.actors)


def apply_internal_transfers(
    state: EcosystemState, transfers: Iterable[Transfer]
) -> EcosystemState:
    balances = {a.actor_id: a.cash for a in state.actors}

    for tx in transfers:
        if tx.src not in balances or tx.dst not in balances:
            raise KeyError("internal transfer references unknown actor")
        if balances[tx.src] < tx.amount:
            raise ValueError("internal transfer would overdraw source")
        balances[tx.src] -= tx.amount
        balances[tx.dst] += tx.amount

    actors = tuple(
        Actor(a.actor_id, a.kind, balances[a.actor_id], a.burn)
        for a in state.actors
    )
    result = EcosystemState(
        t=state.t,
        actors=actors,
        user_utility=state.user_utility,
        service_quality=state.service_quality,
    )
    assert_cash_conservation(state, result)
    return result


def assert_cash_conservation(before: EcosystemState, after: EcosystemState) -> None:
    if abs(before.total_cash - after.total_cash) > 1e-9:
        raise AssertionError(
            f"internal ledger violated conservation: "
            f"{before.total_cash=} {after.total_cash=}"
        )


def viability_margin(state: EcosystemState) -> float:
    margins = []
    for actor in state.actors:
        if actor.burn > 0:
            margins.append(actor.cash / actor.burn)
    if not margins:
        return float("inf")
    return min(margins)
