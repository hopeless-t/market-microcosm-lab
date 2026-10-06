from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InvalidationCost:
    uses: int
    invalidation_probability: float
    raw_expected_cost: float
    prepared_expected_cost: float
    expected_rebuilds: float

    @property
    def prepared_wins(self) -> bool:
        return self.prepared_expected_cost < self.raw_expected_cost


def expected_costs(
    uses: int,
    invalidation_probability: float,
    *,
    raw_per_use: float = 25.0,
    preparation_cost: float = 30.0,
    prepared_per_use: float = 12.0,
) -> InvalidationCost:
    if uses < 1:
        raise ValueError("uses must be positive")
    if not 0.0 <= invalidation_probability <= 1.0:
        raise ValueError("invalidation_probability must be within [0, 1]")
    if min(raw_per_use, preparation_cost, prepared_per_use) < 0.0:
        raise ValueError("costs must be non-negative")
    expected_rebuilds = invalidation_probability * max(0, uses - 1)
    raw = raw_per_use * uses
    prepared = (
        preparation_cost
        + prepared_per_use * uses
        + preparation_cost * expected_rebuilds
    )
    return InvalidationCost(
        uses=uses,
        invalidation_probability=invalidation_probability,
        raw_expected_cost=raw,
        prepared_expected_cost=prepared,
        expected_rebuilds=expected_rebuilds,
    )


def break_even_invalidation_probability(
    uses: int,
    *,
    raw_per_use: float = 25.0,
    preparation_cost: float = 30.0,
    prepared_per_use: float = 12.0,
) -> float | None:
    if uses <= 1:
        return None
    numerator = (
        raw_per_use * uses
        - preparation_cost
        - prepared_per_use * uses
    )
    denominator = preparation_cost * (uses - 1)
    if numerator <= 0.0:
        return None
    return numerator / denominator


def frozen_invalidation_sweep() -> dict[str, InvalidationCost | float | None]:
    return {
        "uses_3_q_010": expected_costs(3, 0.10),
        "uses_3_q_020": expected_costs(3, 0.20),
        "uses_8_q_030": expected_costs(8, 0.30),
        "uses_8_q_040": expected_costs(8, 0.40),
        "knee_3": break_even_invalidation_probability(3),
        "knee_8": break_even_invalidation_probability(8),
    }
