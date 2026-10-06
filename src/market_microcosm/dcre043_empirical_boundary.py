from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmpiricalAnchor:
    key: str
    evidence_class: str
    period: str
    values: tuple[float, ...]
    unit: str
    scope: str
    source_url: str
    note: str


OBSERVED = "OBSERVED_COMPANY_REPORTED"
FORECAST = "AUTHORITATIVE_FORECAST"
UNKNOWN = "UNKNOWN_STRUCTURAL_PARAMETER"


def empirical_anchors() -> tuple[EmpiricalAnchor, ...]:
    return (
        EmpiricalAnchor(
            key="google_dc_electricity_growth_2024_yoy",
            evidence_class=OBSERVED,
            period="2024",
            values=(27.0,),
            unit="percent_yoy",
            scope="Google data centers",
            source_url="https://sustainability.google/commitments/water/",
            note="Company reports data-center electricity consumption increased 27% year over year in 2024.",
        ),
        EmpiricalAnchor(
            key="google_compute_per_electricity_5y_lower_bound",
            evidence_class=OBSERVED,
            period="five-year comparison reported in 2026",
            values=(6.0,),
            unit="times_lower_bound",
            scope="Google data centers",
            source_url="https://sustainability.google/commitments/water/",
            note="Company reports more than six times the computing power per unit of electricity versus five years earlier; 6x is stored only as a lower bound.",
        ),
        EmpiricalAnchor(
            key="google_water_replenishment_2025",
            evidence_class=OBSERVED,
            period="2025",
            values=(7.7, 78.0),
            unit="billion_gallons_and_percent_of_freshwater_consumption",
            scope="Google operations water stewardship portfolio",
            source_url="https://sustainability.google/google-2026-environmental-report/",
            note="Company reports roughly 7.7 billion gallons replenished, about 78% of 2025 total freshwater consumption; replenishment is not treated as reduced consumption.",
        ),
        EmpiricalAnchor(
            key="lbl_us_data_center_electricity_share_2030",
            evidence_class=FORECAST,
            period="2030",
            values=(9.5, 11.8, 15.3),
            unit="percent_of_us_electricity_low_central_high",
            scope="United States data centers",
            source_url="https://bies.lbl.gov/publications/united-states-data-center-energy-2025",
            note="LBNL 2025 Update published June 2026; bottom-up scenario range with 11.8% central estimate.",
        ),
        EmpiricalAnchor(
            key="iea_us_demand_growth_data_center_share_to_2030",
            evidence_class=FORECAST,
            period="2026-2030",
            values=(50.0,),
            unit="percent_approx_of_us_electricity_demand_growth",
            scope="United States electricity demand growth",
            source_url="https://www.iea.org/reports/electricity-2026/executive-summary",
            note="IEA projects around half of U.S. electricity-demand growth through 2030 to be driven by data-center expansion.",
        ),
        EmpiricalAnchor(
            key="iea_global_data_center_electricity_2030",
            evidence_class=FORECAST,
            period="2030",
            values=(945.0,),
            unit="TWh_approx",
            scope="Global data centers",
            source_url="https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai",
            note="IEA Energy and AI Base Case projects global data-center electricity consumption around 945 TWh in 2030.",
        ),
    )


def unknown_structural_parameters() -> tuple[str, ...]:
    return (
        "causal_demand_elasticity_eta",
        "causal_rebound_coefficient",
        "verified_utility_per_compute",
        "site_level_energy_water_substitution",
        "provider_recovery_response_curve",
        "shock_probability_and_cross_region_correlation",
    )


def calibration_contract() -> dict:
    return {
        "anchors": empirical_anchors(),
        "allowed_uses": (
            "qualitative_consistency_checks",
            "scenario_envelope_stress_tests",
            "scope_and_order_of_magnitude_checks",
        ),
        "forbidden_uses": (
            "infer_causal_elasticity_from_company_efficiency_and_growth",
            "treat_forecast_as_observation",
            "derive_site_water_intensity_from_global_replenishment",
            "map_compute_efficiency_directly_to_verified_utility",
        ),
        "unknown_structural_parameters": unknown_structural_parameters(),
        "automatic_synthetic_parameter_writes": (),
    }
