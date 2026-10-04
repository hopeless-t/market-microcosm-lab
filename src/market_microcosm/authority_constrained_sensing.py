from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SensingCandidate:
    name: str
    cost: int
    resolves_predicate: bool
    authorized: bool
    privacy_class: str
    evidence_form: str


def sensing_candidates() -> tuple[SensingCandidate, ...]:
    return (
        SensingCandidate(
            name="raw_customer_ledger_boolean",
            cost=1,
            resolves_predicate=True,
            authorized=False,
            privacy_class="raw_customer_data",
            evidence_form="predicate_native_raw_query",
        ),
        SensingCandidate(
            name="cheap_partial_refinement",
            cost=1,
            resolves_predicate=False,
            authorized=True,
            privacy_class="aggregate",
            evidence_form="partial_numeric_refinement",
        ),
        SensingCandidate(
            name="signed_predicate_attestation",
            cost=3,
            resolves_predicate=True,
            authorized=True,
            privacy_class="predicate_only",
            evidence_form="signed_boolean_attestation",
        ),
        SensingCandidate(
            name="authorized_exact_current_mrr",
            cost=5,
            resolves_predicate=True,
            authorized=True,
            privacy_class="aggregate_exact",
            evidence_form="exact_state_query",
        ),
    )


def select_authority_constrained_candidate() -> dict:
    rows = [asdict(row) for row in sensing_candidates()]

    naive_resolving = [
        row for row in rows if row["resolves_predicate"]
    ]
    naive_selected = min(
        naive_resolving,
        key=lambda row: (row["cost"], row["name"]),
    )

    admissible = [
        row
        for row in rows
        if row["authorized"] and row["resolves_predicate"]
    ]
    if not admissible:
        raise ValueError("no authorized resolving candidate")

    authorized_selected = min(
        admissible,
        key=lambda row: (row["cost"], row["name"]),
    )

    return {
        "candidates": rows,
        "naive_cost_only_selection": naive_selected,
        "authorized_selection": authorized_selected,
        "unauthorized_candidate_would_win_naive_search": (
            naive_selected["authorized"] is False
        ),
        "authorized_resolving_candidate_count": len(admissible),
    }


def authority_constrained_active_sensing_report_payload() -> dict:
    selection = select_authority_constrained_candidate()
    selected = selection["authorized_selection"]

    gates = {
        "naive_cost_search_selects_unauthorized_evidence": (
            selection[
                "unauthorized_candidate_would_win_naive_search"
            ]
            is True
        ),
        "authority_filter_changes_selected_observation": (
            selection["naive_cost_only_selection"]["name"]
            != selected["name"]
        ),
        "selected_observation_is_authorized": (
            selected["authorized"] is True
        ),
        "selected_observation_resolves_predicate": (
            selected["resolves_predicate"] is True
        ),
        "selected_observation_avoids_raw_customer_data": (
            selected["privacy_class"] != "raw_customer_data"
        ),
        "authority_is_a_hard_constraint_not_a_soft_cost": True,
    }

    return {
        "experiment": "E046",
        "question": (
            "Can minimum-cost active sensing select inadmissible evidence "
            "unless authorization/privacy constraints are applied before "
            "cost optimization?"
        ),
        "candidate_search": selection,
        "promotion_gate": gates,
        "promoted_authority_rule": (
            "active-sensing-optimizes-only-within-authorized-evidence-set-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Observation selection becomes lexicographic: first filter by "
            "authorization and predicate resolution, then minimize declared "
            "collection cost. Unauthorized evidence cannot be purchased by "
            "assigning it a larger soft penalty."
        ),
        "limitations": (
            "Authorization and privacy classes are synthetic labels in this "
            "reference. Production policy must come from the actual evidence "
            "provider, user consent, organizational policy, and applicable "
            "access controls."
        ),
    }
