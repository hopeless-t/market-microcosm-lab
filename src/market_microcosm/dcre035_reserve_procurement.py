from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre034_reserve_capacity import evaluate_reserve


@dataclass(frozen=True)
class ReserveProvider:
    name: str
    reserve_units: float = 10.0
    holding_cost_per_unit: float = 0.1

    def private_net(self, payment_per_unit: float) -> float:
        if payment_per_unit < 0.0:
            raise ValueError("payment must be non-negative")
        return self.reserve_units * (
            payment_per_unit - self.holding_cost_per_unit
        )


def frozen_providers() -> tuple[ReserveProvider, ReserveProvider]:
    return (ReserveProvider("P1"), ReserveProvider("P2"))


def privately_supplied_reserve(payment_per_unit: float) -> tuple[ReserveProvider, ...]:
    # Strictly positive private net is required; zero-profit tie does not enter.
    return tuple(
        provider
        for provider in frozen_providers()
        if provider.private_net(payment_per_unit) > 0.0
    )


def reserve_market_outcome(
    payment_per_unit: float,
    *,
    shock_probability: float = 0.20,
) -> dict:
    selected = privately_supplied_reserve(payment_per_unit)
    aggregate_reserve = sum(provider.reserve_units for provider in selected)
    system = evaluate_reserve(
        aggregate_reserve,
        shock_probability,
        holding_cost_per_unit=0.1,
        shortfall_penalty_per_unit=1.0,
    )
    return {
        "payment_per_unit": payment_per_unit,
        "selected_names": tuple(provider.name for provider in selected),
        "aggregate_reserve": aggregate_reserve,
        "system_expected_cost": system.expected_total_cost,
        "total_capacity_payment": payment_per_unit * aggregate_reserve,
    }


def private_payment_knee() -> float:
    return frozen_providers()[0].holding_cost_per_unit


def frozen_reserve_procurement() -> dict:
    return {
        "no_payment": reserve_market_outcome(0.0),
        "at_knee": reserve_market_outcome(0.10),
        "above_knee": reserve_market_outcome(0.11),
        "payment_knee": private_payment_knee(),
    }
