from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastInvestmentOutcome:
    policy: str
    provider_investments: tuple[float, ...]
    initial_market_capacity: float
    forecast_demand: float
    actual_demand: float
    future_capacity: float
    idle_capacity: float
    unmet_demand: float
    construction_resource: float


def shared_forecast_uncoordinated(
    *,
    provider_count: int = 2,
    initial_market_capacity: float = 100.0,
    forecast_demand: float = 160.0,
    actual_demand: float = 160.0,
    construction_resource_per_capacity: float = 0.5,
) -> ForecastInvestmentOutcome:
    if provider_count < 1:
        raise ValueError("provider_count must be positive")
    gap = max(0.0, forecast_demand - initial_market_capacity)
    investments = tuple(gap for _ in range(provider_count))
    future = initial_market_capacity + sum(investments)
    return ForecastInvestmentOutcome(
        policy="UNCOORDINATED_SHARED_FORECAST",
        provider_investments=investments,
        initial_market_capacity=initial_market_capacity,
        forecast_demand=forecast_demand,
        actual_demand=actual_demand,
        future_capacity=future,
        idle_capacity=max(0.0, future - actual_demand),
        unmet_demand=max(0.0, actual_demand - future),
        construction_resource=sum(investments) * construction_resource_per_capacity,
    )


def shared_forecast_coordinated(
    *,
    provider_count: int = 2,
    initial_market_capacity: float = 100.0,
    forecast_demand: float = 160.0,
    actual_demand: float = 160.0,
    construction_resource_per_capacity: float = 0.5,
) -> ForecastInvestmentOutcome:
    if provider_count < 1:
        raise ValueError("provider_count must be positive")
    gap = max(0.0, forecast_demand - initial_market_capacity)
    per_provider = gap / provider_count
    investments = tuple(per_provider for _ in range(provider_count))
    future = initial_market_capacity + sum(investments)
    return ForecastInvestmentOutcome(
        policy="COORDINATED_RESIDUAL_SPLIT",
        provider_investments=investments,
        initial_market_capacity=initial_market_capacity,
        forecast_demand=forecast_demand,
        actual_demand=actual_demand,
        future_capacity=future,
        idle_capacity=max(0.0, future - actual_demand),
        unmet_demand=max(0.0, actual_demand - future),
        construction_resource=sum(investments) * construction_resource_per_capacity,
    )


def frozen_shared_forecast() -> dict[str, ForecastInvestmentOutcome]:
    return {
        "uncoordinated": shared_forecast_uncoordinated(),
        "coordinated": shared_forecast_coordinated(),
    }
