from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReserveChoice:
    reserve_units: float
    shock_probability: float
    holding_cost: float
    expected_shortfall_cost: float
    expected_total_cost: float


def evaluate_reserve(
    reserve_units: float,
    shock_probability: float,
    *,
    shock_size: float = 20.0,
    holding_cost_per_unit: float = 0.1,
    shortfall_penalty_per_unit: float = 1.0,
) -> ReserveChoice:
    if reserve_units < 0.0 or shock_size < 0.0:
        raise ValueError("reserve and shock size must be non-negative")
    if not 0.0 <= shock_probability <= 1.0:
        raise ValueError("shock probability must be within [0, 1]")
    if min(holding_cost_per_unit, shortfall_penalty_per_unit) < 0.0:
        raise ValueError("costs must be non-negative")
    holding = reserve_units * holding_cost_per_unit
    shortfall = max(0.0, shock_size - reserve_units)
    expected_shortfall = (
        shock_probability * shortfall * shortfall_penalty_per_unit
    )
    return ReserveChoice(
        reserve_units=reserve_units,
        shock_probability=shock_probability,
        holding_cost=holding,
        expected_shortfall_cost=expected_shortfall,
        expected_total_cost=holding + expected_shortfall,
    )


def exact_reserve_grid(shock_probability: float) -> ReserveChoice:
    candidates = tuple(
        evaluate_reserve(reserve, shock_probability)
        for reserve in (0.0, 10.0, 20.0, 30.0)
    )
    return min(
        candidates,
        key=lambda row: (row.expected_total_cost, row.reserve_units),
    )


def marginal_probability_knee(
    *,
    holding_cost_per_unit: float = 0.1,
    shortfall_penalty_per_unit: float = 1.0,
) -> float:
    if shortfall_penalty_per_unit <= 0.0:
        raise ValueError("shortfall penalty must be positive")
    return holding_cost_per_unit / shortfall_penalty_per_unit


def frozen_reserve_market() -> dict:
    return {
        "low_risk": exact_reserve_grid(0.05),
        "high_risk": exact_reserve_grid(0.20),
        "probability_knee": marginal_probability_knee(),
    }
