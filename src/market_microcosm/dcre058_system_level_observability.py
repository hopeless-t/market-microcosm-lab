from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UtilityLoadGrowthObservation:
    start_year: int
    end_year: int
    start_mw: float
    end_mw: float
    data_centers_reported_as_substantial_driver: bool
    exact_data_center_share: float | None

    @property
    def growth_ratio(self) -> float:
        return self.end_mw / self.start_mw


def nwcpud_2016_2026_load_growth() -> UtilityLoadGrowthObservation:
    return UtilityLoadGrowthObservation(
        start_year=2016,
        end_year=2026,
        start_mw=90.0,
        end_mw=277.0,
        data_centers_reported_as_substantial_driver=True,
        exact_data_center_share=None,
    )


def dcre058_system_level_observability_report() -> dict:
    observation = nwcpud_2016_2026_load_growth()
    return {
        "experiment": "DCRE-058",
        "observation": observation,
        "utility_load_more_than_tripled": observation.growth_ratio > 3.0,
        "source_attribution_level": "QUALITATIVE_SUBSTANTIAL_DRIVER",
        "exact_data_center_share": observation.exact_data_center_share,
        "customer_specific_causality_identified": False,
        "system_level_planning_pressure_observed": True,
        "authority_effect": "NONE",
    }
