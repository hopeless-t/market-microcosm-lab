from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceMechanismObservation:
    name: str
    observed: bool
    maps_to_market_failure: str


def nwcpud_observed_governance_mechanisms() -> tuple[GovernanceMechanismObservation, ...]:
    return (
        GovernanceMechanismObservation(
            name="separate_cost_assignment_for_large_loads",
            observed=True,
            maps_to_market_failure="cross_subsidy_and_stranded_asset_externality",
        ),
        GovernanceMechanismObservation(
            name="engineering_and_grid_feasibility_studies",
            observed=True,
            maps_to_market_failure="capacity_and_reliability_overcommitment",
        ),
        GovernanceMechanismObservation(
            name="customer_funded_infrastructure_upgrades",
            observed=True,
            maps_to_market_failure="infrastructure_cost_socialization",
        ),
        GovernanceMechanismObservation(
            name="credit_collateral_and_service_deposits",
            observed=True,
            maps_to_market_failure="provider_exit_and_stranded_asset_risk",
        ),
        GovernanceMechanismObservation(
            name="minimum_purchase_and_take_or_pay",
            observed=True,
            maps_to_market_failure="capacity_commitment_and_revenue_risk",
        ),
        GovernanceMechanismObservation(
            name="separate_large_load_power_procurement",
            observed=True,
            maps_to_market_failure="resource_cost_cross_subsidy",
        ),
        GovernanceMechanismObservation(
            name="continuous_service_requirement",
            observed=True,
            maps_to_market_failure="service_reliability_obligation",
        ),
    )


def dcre059_institutional_mechanism_map() -> dict:
    mechanisms = nwcpud_observed_governance_mechanisms()
    return {
        "experiment": "DCRE-059",
        "mechanisms": mechanisms,
        "observed_mechanism_count": sum(int(row.observed) for row in mechanisms),
        "mechanisms_exist": all(row.observed for row in mechanisms),
        "causal_effectiveness_identified": False,
        "counterfactual_without_mechanisms_observed": False,
        "policy_recommendation_authorized": False,
        "authority_effect": "NONE",
    }
