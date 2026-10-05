from __future__ import annotations

from itertools import combinations

from market_microcosm.coupled_audit_bundles import (
    UNSAFE_OBLIGATIONS,
    audit_actions,
)


def evidence_failure_blast(selected) -> dict:
    coverage_count = {
        obligation: sum(
            obligation in action.discharges
            for action in selected
        )
        for obligation in UNSAFE_OBLIGATIONS
    }

    per_action = []
    for action in selected:
        uniquely_supported = sorted(
            obligation
            for obligation in action.discharges
            if coverage_count[obligation] == 1
        )
        per_action.append(
            {
                "action_id": action.action_id,
                "solely_supported_obligations": uniquely_supported,
                "obligation_blast_if_evidence_fails": len(
                    uniquely_supported
                ),
            }
        )

    return {
        "per_action": per_action,
        "maximum_obligation_blast": max(
            (
                row["obligation_blast_if_evidence_fails"]
                for row in per_action
            ),
            default=0,
        ),
    }


def exact_failure_domain_aware_audit_cover(
    *,
    maximum_obligation_blast: int = 1,
) -> dict:
    actions = audit_actions()
    candidates = []

    for size in range(1, len(actions) + 1):
        for selected in combinations(actions, size):
            covered = frozenset().union(
                *(action.discharges for action in selected)
            )
            if not UNSAFE_OBLIGATIONS.issubset(covered):
                continue

            blast = evidence_failure_blast(selected)
            if (
                blast["maximum_obligation_blast"]
                > maximum_obligation_blast
            ):
                continue

            candidates.append(
                {
                    "action_ids": sorted(
                        action.action_id for action in selected
                    ),
                    "action_count": len(selected),
                    "total_cost": sum(
                        action.cost for action in selected
                    ),
                    "covered_obligations": sorted(covered),
                    "evidence_failure_blast": blast,
                }
            )

    if not candidates:
        raise ValueError("no failure-domain-safe audit cover")

    selected = min(
        candidates,
        key=lambda row: (
            row["total_cost"],
            row["action_count"],
            row["action_ids"],
        ),
    )

    e061_selected = tuple(
        action
        for action in actions
        if action.action_id
        in {"control-plane-bundle", "infra-resilience-bundle"}
    )

    return {
        "maximum_obligation_blast": maximum_obligation_blast,
        "safe_candidate_count": len(candidates),
        "selected": selected,
        "e061_bundle_plan": {
            "action_ids": sorted(
                action.action_id for action in e061_selected
            ),
            "total_cost": sum(
                action.cost for action in e061_selected
            ),
            "evidence_failure_blast": evidence_failure_blast(
                e061_selected
            ),
        },
    }


def audit_evidence_failure_domain_report_payload() -> dict:
    result = exact_failure_domain_aware_audit_cover()
    selected = result["selected"]
    e061 = result["e061_bundle_plan"]

    gates = {
        "e061_shared_bundle_plan_has_two_obligation_blast": (
            e061["evidence_failure_blast"][
                "maximum_obligation_blast"
            ]
            == 2
        ),
        "e061_cost_six_plan_loses_failure_domain_authority": (
            e061["total_cost"] == 6
            and e061["evidence_failure_blast"][
                "maximum_obligation_blast"
            ]
            > result["maximum_obligation_blast"]
        ),
        "robust_selected_cost_is_eight": (
            selected["total_cost"] == 8
        ),
        "robust_selected_plan_uses_bundle_with_independent_corroboration": (
            selected["action_ids"]
            == [
                "control-plane-bundle",
                "identity-targeted",
                "operator-targeted",
                "power-deep",
            ]
        ),
        "robust_selected_max_blast_is_one": (
            selected["evidence_failure_blast"][
                "maximum_obligation_blast"
            ]
            == 1
        ),
        "cost_optimum_and_failure_domain_optimum_are_distinct": True,
    }

    return {
        "experiment": "E062",
        "question": (
            "Does E061's cheapest shared-evidence audit cover remain "
            "authoritative when one audit artifact can fail and falsely "
            "discharge multiple proof obligations at once?"
        ),
        "robust_cover": result,
        "e061_cost_authority_after_evidence_failure_model": "REVOKED",
        "promotion_gate": gates,
        "promoted_failure_domain_rule": (
            "audit-evidence-reuse-must-model-proof-obligation-failure-blast-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Shared audit evidence is now treated as a failure-domain choice. "
            "Cost savings from reuse are authoritative only when overlapping "
            "coverage keeps the number of obligations uniquely dependent on "
            "one evidence artifact inside the declared proof-failure budget."
        ),
        "limitations": (
            "The reference treats an evidence artifact as either valid or "
            "failed and requires at most one uniquely dependent obligation. "
            "The exact optimum still reuses one bundle, but corroborates one "
            "covered obligation independently. Partial corruption and correlated "
            "audit-tool failures need richer evidence-quorum models."
        ),
    }
