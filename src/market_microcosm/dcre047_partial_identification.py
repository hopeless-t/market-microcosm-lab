from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConditionalBound:
    compute_efficiency_lower_bound: float
    data_center_electricity_2024_mwh: float
    total_electricity_2019_mwh: float
    electricity_ratio_lower_bound: float
    compute_growth_lower_bound: float
    endpoint_year_alignment: bool
    denominator_scope_equivalence_verified: bool
    reporting_boundary_compatibility_verified: bool
    compute_metric_stability_verified: bool

    @property
    def assumptions_verified(self) -> bool:
        return all(
            (
                self.endpoint_year_alignment,
                self.denominator_scope_equivalence_verified,
                self.reporting_boundary_compatibility_verified,
                self.compute_metric_stability_verified,
            )
        )


def conditional_google_compute_growth_bound() -> ConditionalBound:
    compute_efficiency_lower_bound = 6.0
    data_center_electricity_2024_mwh = 30_825_600.0
    total_electricity_2019_mwh = 12_237_200.0
    electricity_ratio_lower_bound = (
        data_center_electricity_2024_mwh / total_electricity_2019_mwh
    )
    compute_growth_lower_bound = (
        compute_efficiency_lower_bound * electricity_ratio_lower_bound
    )
    return ConditionalBound(
        compute_efficiency_lower_bound=compute_efficiency_lower_bound,
        data_center_electricity_2024_mwh=data_center_electricity_2024_mwh,
        total_electricity_2019_mwh=total_electricity_2019_mwh,
        electricity_ratio_lower_bound=electricity_ratio_lower_bound,
        compute_growth_lower_bound=compute_growth_lower_bound,
        endpoint_year_alignment=True,
        denominator_scope_equivalence_verified=False,
        reporting_boundary_compatibility_verified=False,
        compute_metric_stability_verified=False,
    )


def dcre047_partial_identification_report() -> dict:
    bound = conditional_google_compute_growth_bound()
    blockers = tuple(
        name
        for name, verified in (
            ("DENOMINATOR_SCOPE_EQUIVALENCE", bound.denominator_scope_equivalence_verified),
            ("REPORTING_BOUNDARY_COMPATIBILITY", bound.reporting_boundary_compatibility_verified),
            ("COMPUTE_METRIC_STABILITY", bound.compute_metric_stability_verified),
        )
        if not verified
    )
    return {
        "experiment": "DCRE-047",
        "conditional_bound": bound,
        "strict_conditional_statement": (
            f"compute_2024/compute_2019 > {bound.compute_growth_lower_bound:.6f}"
        ),
        "promoted_compute_growth_lower_bound": None,
        "candidate_eta": None,
        "blocking_assumptions": blockers,
        "authority_effect": "NONE",
    }
