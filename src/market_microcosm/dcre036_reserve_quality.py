from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class ReserveBid:
    name: str
    nominal_units: float
    holding_cost_per_unit: float
    reliability: float

    @property
    def holding_cost(self) -> float:
        return self.nominal_units * self.holding_cost_per_unit

    @property
    def expected_usable_units(self) -> float:
        return self.nominal_units * self.reliability


def frozen_bids() -> tuple[ReserveBid, ...]:
    return (
        ReserveBid("FLAKY_BIG", 20.0, 0.05, 0.40),
        ReserveBid("RELIABLE_A", 10.0, 0.10, 1.00),
        ReserveBid("RELIABLE_B", 10.0, 0.10, 1.00),
    )


def system_expected_cost(
    selected: tuple[ReserveBid, ...],
    *,
    shock_size: float = 20.0,
    shock_probability: float = 0.20,
    shortfall_penalty_per_unit: float = 1.0,
) -> float:
    usable = sum(bid.expected_usable_units for bid in selected)
    holding = sum(bid.holding_cost for bid in selected)
    residual = max(0.0, shock_size - usable)
    return holding + shock_probability * residual * shortfall_penalty_per_unit


def nameplate_cheapest_procurement(
    *, target_nominal: float = 20.0
) -> tuple[ReserveBid, ...]:
    selected: list[ReserveBid] = []
    nominal = 0.0
    for bid in sorted(
        frozen_bids(),
        key=lambda row: (row.holding_cost_per_unit, row.name),
    ):
        if nominal >= target_nominal:
            break
        selected.append(bid)
        nominal += bid.nominal_units
    return tuple(selected)


def reliability_aware_exact() -> tuple[ReserveBid, ...]:
    bids = frozen_bids()
    candidates: list[tuple[ReserveBid, ...]] = []
    for count in range(1, len(bids) + 1):
        candidates.extend(tuple(combo) for combo in combinations(bids, count))
    return min(
        candidates,
        key=lambda selected: (
            system_expected_cost(selected),
            sum(bid.holding_cost for bid in selected),
            tuple(bid.name for bid in selected),
        ),
    )


def frozen_procurement_quality() -> dict:
    nameplate = nameplate_cheapest_procurement()
    exact = reliability_aware_exact()
    return {
        "nameplate": nameplate,
        "nameplate_usable": sum(bid.expected_usable_units for bid in nameplate),
        "nameplate_cost": system_expected_cost(nameplate),
        "exact": exact,
        "exact_usable": sum(bid.expected_usable_units for bid in exact),
        "exact_cost": system_expected_cost(exact),
    }
