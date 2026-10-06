from __future__ import annotations

from dataclasses import dataclass


GALLON_TO_LITER = 3.785411784


@dataclass(frozen=True)
class JointResourceObservation:
    year: int
    data_center_electricity_mwh: float
    data_center_water_consumption_million_gallons: float
    electricity_third_party_assured: bool
    water_third_party_assured: bool
    metric_scope_identity_certified: bool

    @property
    def conditional_gallons_per_kwh(self) -> float:
        gallons = self.data_center_water_consumption_million_gallons * 1_000_000.0
        kwh = self.data_center_electricity_mwh * 1_000.0
        return gallons / kwh

    @property
    def conditional_liters_per_kwh(self) -> float:
        return self.conditional_gallons_per_kwh * GALLON_TO_LITER


def google_2024_joint_resource_observation() -> JointResourceObservation:
    return JointResourceObservation(
        year=2024,
        data_center_electricity_mwh=30_825_600.0,
        data_center_water_consumption_million_gallons=7_787.0,
        electricity_third_party_assured=True,
        water_third_party_assured=True,
        metric_scope_identity_certified=False,
    )


def dcre053_joint_resource_observability_report() -> dict:
    observation = google_2024_joint_resource_observation()
    return {
        "experiment": "DCRE-053",
        "observation": observation,
        "conditional_aggregate_gallons_per_kwh": (
            observation.conditional_gallons_per_kwh
        ),
        "conditional_aggregate_liters_per_kwh": (
            observation.conditional_liters_per_kwh
        ),
        "derived_ratio_status": "CONDITIONAL_DESCRIPTIVE_RATIO_ONLY",
        "promoted_wue_liters_per_kwh": None,
        "candidate_energy_water_substitution_coefficient": None,
        "causal_cooling_tradeoff_identified": False,
        "authority_effect": "NONE",
    }
