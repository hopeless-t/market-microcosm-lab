from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OutcomeClaim:
    name: str
    source_reported: bool
    independently_verified_here: bool
    counterfactual_observed: bool


def nwcpud_public_outcome_claims() -> tuple[OutcomeClaim, ...]:
    return (
        OutcomeClaim(
            name="residential_rates_remain_low",
            source_reported=True,
            independently_verified_here=False,
            counterfactual_observed=False,
        ),
        OutcomeClaim(
            name="other_industries_not_crowded_out",
            source_reported=True,
            independently_verified_here=False,
            counterfactual_observed=False,
        ),
        OutcomeClaim(
            name="large_load_costs_not_shifted_to_base_customers",
            source_reported=True,
            independently_verified_here=False,
            counterfactual_observed=False,
        ),
    )


def dcre060_mechanism_outcome_cooccurrence_report() -> dict:
    claims = nwcpud_public_outcome_claims()
    return {
        "experiment": "DCRE-060",
        "mechanism_bundle_observed": True,
        "outcome_claims": claims,
        "favorable_outcome_claims_coexist": all(
            claim.source_reported for claim in claims
        ),
        "all_outcomes_independently_verified": all(
            claim.independently_verified_here for claim in claims
        ),
        "counterfactual_observed": any(
            claim.counterfactual_observed for claim in claims
        ),
        "mechanism_caused_favorable_outcomes": None,
        "causal_effectiveness_identified": False,
        "authority_effect": "NONE",
    }
