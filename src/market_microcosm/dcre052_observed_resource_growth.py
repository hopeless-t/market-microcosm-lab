from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObservedElectricityGrowth:
    start_year: int
    end_year: int
    start_mwh: float
    end_mwh: float
    growth_ratio: float
    cagr: float


@dataclass(frozen=True)
class EfficiencyContext:
    pue_by_year: dict[int, float]
    pue_scope: str
    electricity_scope: str
    scope_identity_certified: bool

    @property
    def pue_non_worsening(self) -> bool:
        years = sorted(self.pue_by_year)
        return self.pue_by_year[years[-1]] <= self.pue_by_year[years[0]]


def google_dc_electricity_2020_2024() -> dict[int, float]:
    return {
        2020: 14_426_600.0,
        2021: 17_659_000.0,
        2022: 20_806_200.0,
        2023: 24_294_900.0,
        2024: 30_825_600.0,
    }


def google_fleet_pue_2020_2024() -> dict[int, float]:
    return {
        2020: 1.10,
        2021: 1.10,
        2022: 1.10,
        2023: 1.10,
        2024: 1.09,
    }


def observed_growth() -> ObservedElectricityGrowth:
    series = google_dc_electricity_2020_2024()
    start_year = min(series)
    end_year = max(series)
    start = series[start_year]
    end = series[end_year]
    years = end_year - start_year
    ratio = end / start
    cagr = ratio ** (1.0 / years) - 1.0
    return ObservedElectricityGrowth(
        start_year=start_year,
        end_year=end_year,
        start_mwh=start,
        end_mwh=end,
        growth_ratio=ratio,
        cagr=cagr,
    )


def dcre052_observed_resource_growth_report() -> dict:
    growth = observed_growth()
    context = EfficiencyContext(
        pue_by_year=google_fleet_pue_2020_2024(),
        pue_scope="GOOGLE_OWNED_AND_OPERATED_DATA_CENTER_CAMPUSES",
        electricity_scope="REPORTED_GOOGLE_DATA_CENTER_ELECTRICITY",
        scope_identity_certified=False,
    )
    return {
        "experiment": "DCRE-052",
        "electricity_series_mwh": google_dc_electricity_2020_2024(),
        "growth": growth,
        "efficiency_context": context,
        "observed_consistency_statement": (
            "TOTAL_DC_ELECTRICITY_MORE_THAN_DOUBLED_WHILE_FLEET_PUE_DID_NOT_WORSEN"
        ),
        "derived_it_energy_series": None,
        "causal_rebound_identified": False,
        "candidate_eta": None,
        "authority_effect": "NONE",
    }
