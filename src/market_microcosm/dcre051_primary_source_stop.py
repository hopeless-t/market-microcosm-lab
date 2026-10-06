from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssuranceEndpoint:
    year: int
    total_electricity_mwh: float
    data_center_electricity_mwh: float | None
    third_party_assured: bool
    boundary_label: str


@dataclass(frozen=True)
class PrimarySourceAudit:
    checked_surfaces: tuple[str, ...]
    historical_total_assured: bool
    current_data_center_value_assured: bool
    historical_data_center_exact_observed: bool
    boundary_wording_identical: bool
    cross_boundary_subset_certified: bool
    stop_condition_met: bool


def assured_endpoints() -> tuple[AssuranceEndpoint, AssuranceEndpoint]:
    historical = AssuranceEndpoint(
        year=2019,
        total_electricity_mwh=12_237_198.0,
        data_center_electricity_mwh=None,
        third_party_assured=True,
        boundary_label=(
            "ALPHABET_2019_GLOBAL_FACILITIES_OPERATIONAL_CONTROL_"
            "DATA_CENTERS_OFFICES_NETWORKING_INFRASTRUCTURE_"
            "EXCL_CALICO_SIDEWALK"
        ),
    )
    current = AssuranceEndpoint(
        year=2024,
        total_electricity_mwh=32_179_900.0,
        data_center_electricity_mwh=30_825_600.0,
        third_party_assured=True,
        boundary_label=(
            "ALPHABET_2024_GLOBAL_OPERATIONAL_CONTROL_"
            "OWNED_LEASED_DATA_CENTERS_OFFICES_OTHER_ASSETS"
        ),
    )
    return historical, current


def dcre051_primary_source_stop_audit() -> dict:
    historical, current = assured_endpoints()
    checked_surfaces = (
        "ALPHABET_FY2019_ENVIRONMENTAL_INDICATORS_ASSURANCE_LETTER",
        "ALPHABET_FY2024_ENVIRONMENTAL_INDICATORS_ASSURANCE_LETTER",
        "GOOGLE_2025_ENVIRONMENTAL_REPORT_FIGURE_2",
        "GOOGLE_2025_ENVIRONMENTAL_REPORT_DATA_TABLE",
    )
    audit = PrimarySourceAudit(
        checked_surfaces=checked_surfaces,
        historical_total_assured=(
            historical.third_party_assured
            and historical.total_electricity_mwh == 12_237_198.0
        ),
        current_data_center_value_assured=(
            current.third_party_assured
            and current.data_center_electricity_mwh == 30_825_600.0
        ),
        historical_data_center_exact_observed=(
            historical.data_center_electricity_mwh is not None
        ),
        boundary_wording_identical=(
            historical.boundary_label == current.boundary_label
        ),
        cross_boundary_subset_certified=False,
        stop_condition_met=True,
    )
    return {
        "experiment": "DCRE-051",
        "historical_endpoint": historical,
        "current_endpoint": current,
        "audit": audit,
        "exact_2019_dc_denominator_status": (
            "PUBLICLY_UNOBSERVED_IN_CHECKED_PRIMARY_SOURCES"
        ),
        "promoted_2019_dc_mwh": None,
        "promoted_dcre047_bound": None,
        "candidate_eta": None,
        "next_action": "PIVOT_FROM_DENOMINATOR_SEARCH",
        "authority_effect": "NONE",
    }
