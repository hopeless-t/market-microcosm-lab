from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubsetBoundCertificate:
    current_target_positive: bool
    historical_superset_positive: bool
    historical_target_subset_of_superset_certified: bool
    current_and_historical_target_same_population: bool
    activity_metric_endpoint_comparable: bool

    @property
    def certified(self) -> bool:
        return all(
            (
                self.current_target_positive,
                self.historical_superset_positive,
                self.historical_target_subset_of_superset_certified,
                self.current_and_historical_target_same_population,
                self.activity_metric_endpoint_comparable,
            )
        )


def conditional_output_growth_lower_bound(
    *,
    current_target_electricity: float,
    historical_superset_electricity: float,
    activity_per_electricity_growth_lower_bound: float,
) -> float:
    if min(
        current_target_electricity,
        historical_superset_electricity,
        activity_per_electricity_growth_lower_bound,
    ) <= 0.0:
        raise ValueError("bound inputs must be positive")
    return (
        activity_per_electricity_growth_lower_bound
        * current_target_electricity
        / historical_superset_electricity
    )


def google_dcre047_certificate() -> SubsetBoundCertificate:
    return SubsetBoundCertificate(
        current_target_positive=True,
        historical_superset_positive=True,
        historical_target_subset_of_superset_certified=False,
        current_and_historical_target_same_population=False,
        activity_metric_endpoint_comparable=False,
    )


def invalid_boundary_counterexample() -> dict:
    reported_historical_superset = 12.0
    true_historical_target = 14.0
    current_target = 30.0
    efficiency_growth = 2.0
    naive_bound = conditional_output_growth_lower_bound(
        current_target_electricity=current_target,
        historical_superset_electricity=reported_historical_superset,
        activity_per_electricity_growth_lower_bound=efficiency_growth,
    )
    true_growth = efficiency_growth * current_target / true_historical_target
    return {
        "reported_historical_superset": reported_historical_superset,
        "true_historical_target": true_historical_target,
        "naive_bound": naive_bound,
        "true_growth": true_growth,
        "bound_invalid": naive_bound > true_growth,
    }


def dcre049_subset_bound_report() -> dict:
    certificate = google_dcre047_certificate()
    conditional_bound = conditional_output_growth_lower_bound(
        current_target_electricity=30_825_600.0,
        historical_superset_electricity=12_237_200.0,
        activity_per_electricity_growth_lower_bound=6.0,
    )
    return {
        "experiment": "DCRE-049",
        "conditional_bound": conditional_bound,
        "certificate": certificate,
        "counterexample": invalid_boundary_counterexample(),
        "promoted_bound": conditional_bound if certificate.certified else None,
        "candidate_eta": None,
        "authority_effect": "NONE",
    }
