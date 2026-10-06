from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IndependentRateObservation:
    year: int
    utility_residential_cents_per_kwh: float
    state_residential_cents_per_kwh: float
    source: str

    @property
    def utility_to_state_ratio(self) -> float:
        return (
            self.utility_residential_cents_per_kwh
            / self.state_residential_cents_per_kwh
        )

    @property
    def percent_below_state(self) -> float:
        return 1.0 - self.utility_to_state_ratio


def eia_2024_nwcpud_rate_observation() -> IndependentRateObservation:
    return IndependentRateObservation(
        year=2024,
        utility_residential_cents_per_kwh=7.72,
        state_residential_cents_per_kwh=14.70,
        source="US_EIA_2024_ANNUAL_RETAIL_PRICE_TABLES",
    )


def dcre061_independent_rate_crosscheck_report() -> dict:
    observation = eia_2024_nwcpud_rate_observation()
    return {
        "experiment": "DCRE-061",
        "observation": observation,
        "utility_rate_below_state_average": (
            observation.utility_residential_cents_per_kwh
            < observation.state_residential_cents_per_kwh
        ),
        "independent_low_rate_outcome_verified": True,
        "mechanism_caused_low_rate": None,
        "causal_effectiveness_identified": False,
        "authority_effect": "NONE",
    }
