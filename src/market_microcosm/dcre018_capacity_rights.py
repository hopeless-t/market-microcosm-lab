from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapacityRightsOutcome:
    policy: str
    investments: tuple[float, ...]
    initial_capacity: float
    actual_demand: float
    future_capacity: float
    idle_capacity: float
    unmet_demand: float
    construction_resource: float
    investment_hhi: float


def _outcome(
    *,
    policy: str,
    investments: tuple[float, ...],
    initial_capacity: float = 100.0,
    actual_demand: float = 160.0,
    construction_resource_per_capacity: float = 0.5,
) -> CapacityRightsOutcome:
    total_investment = sum(investments)
    future = initial_capacity + total_investment
    if total_investment > 0.0:
        shares = tuple(value / total_investment for value in investments)
        hhi = sum(share**2 for share in shares)
    else:
        hhi = 0.0
    return CapacityRightsOutcome(
        policy=policy,
        investments=investments,
        initial_capacity=initial_capacity,
        actual_demand=actual_demand,
        future_capacity=future,
        idle_capacity=max(0.0, future - actual_demand),
        unmet_demand=max(0.0, actual_demand - future),
        construction_resource=total_investment * construction_resource_per_capacity,
        investment_hhi=hhi,
    )


def no_capacity_rights() -> CapacityRightsOutcome:
    return _outcome(
        policy="NO_CAPACITY_RIGHTS",
        investments=(60.0, 60.0),
    )


def winner_take_all_rights() -> CapacityRightsOutcome:
    return _outcome(
        policy="WINNER_TAKE_ALL_RIGHTS",
        investments=(60.0, 0.0),
    )


def split_capacity_rights() -> CapacityRightsOutcome:
    return _outcome(
        policy="SPLIT_CAPACITY_RIGHTS",
        investments=(30.0, 30.0),
    )


def frozen_capacity_rights() -> dict[str, CapacityRightsOutcome]:
    return {
        "none": no_capacity_rights(),
        "winner_take_all": winner_take_all_rights(),
        "split": split_capacity_rights(),
    }
