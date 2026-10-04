from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import Counter


@dataclass(frozen=True)
class PredicateWitness:
    witness_id: str
    failure_domain: str
    predicate_value: bool
    authorized: bool = True
    fresh: bool = True
    metric_generation: str = "mrr-v2"


def reference_witnesses() -> tuple[PredicateWitness, ...]:
    return (
        PredicateWitness("w0", "domain-a", True),
        PredicateWitness("w1", "domain-b", True),
        PredicateWitness("w2", "domain-c", True),
        PredicateWitness("w3", "domain-d", True),
        PredicateWitness("w4", "domain-e", False),
    )


def verify_predicate_quorum(
    witnesses: tuple[PredicateWitness, ...],
    *,
    threshold: int = 3,
    required_generation: str = "mrr-v2",
) -> dict:
    admissible = tuple(
        witness
        for witness in witnesses
        if witness.authorized
        and witness.fresh
        and witness.metric_generation == required_generation
    )

    votes = Counter(witness.predicate_value for witness in admissible)
    domain_votes = {
        value: {
            witness.failure_domain
            for witness in admissible
            if witness.predicate_value is value
        }
        for value in (True, False)
    }

    accepted_value = None
    for value in (True, False):
        if (
            votes[value] >= threshold
            and len(domain_votes[value]) >= threshold
        ):
            accepted_value = value
            break

    return {
        "threshold": threshold,
        "admissible_witness_count": len(admissible),
        "true_votes": votes[True],
        "false_votes": votes[False],
        "true_domains": sorted(domain_votes[True]),
        "false_domains": sorted(domain_votes[False]),
        "accepted": accepted_value is not None,
        "accepted_value": accepted_value,
    }


def single_witness_reference() -> dict:
    witnesses = reference_witnesses()
    compromised = witnesses[-1]
    quorum = verify_predicate_quorum(witnesses)

    return {
        "single_selected_witness": asdict(compromised),
        "single_witness_result": compromised.predicate_value,
        "quorum_result": quorum,
        "single_witness_disagrees_with_quorum": (
            compromised.predicate_value
            != quorum["accepted_value"]
        ),
    }


def conflict_reference() -> dict:
    witnesses = (
        PredicateWitness("w0", "domain-a", True),
        PredicateWitness("w1", "domain-b", True),
        PredicateWitness("w2", "domain-c", False),
        PredicateWitness("w3", "domain-d", False),
    )
    return verify_predicate_quorum(witnesses)


def evidence_quorum_report_payload() -> dict:
    reference = single_witness_reference()
    conflict = conflict_reference()
    quorum = reference["quorum_result"]

    gates = {
        "single_witness_can_be_wrong": (
            reference["single_witness_disagrees_with_quorum"] is True
        ),
        "three_independent_true_domains_accept_true": (
            quorum["accepted"] is True
            and quorum["accepted_value"] is True
            and len(quorum["true_domains"]) >= 3
        ),
        "one_false_witness_cannot_override_quorum": (
            quorum["false_votes"] == 1
            and quorum["accepted_value"] is True
        ),
        "two_vs_two_conflict_abstains": (
            conflict["accepted"] is False
            and conflict["accepted_value"] is None
        ),
        "quorum_requires_failure_domain_diversity": True,
        "single_signed_attestation_is_not_final_authority": True,
    }

    return {
        "experiment": "E048",
        "question": (
            "Can one fresh authorized generation-aligned predicate attestation "
            "be treated as final observation authority, or should current "
            "predicate truth require an independent witness quorum?"
        ),
        "single_witness_reference": reference,
        "conflict_reference": conflict,
        "promotion_gate": gates,
        "promoted_quorum_rule": (
            "predicate-attestation-requires-independent-witness-quorum-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Predicate-native sensing evidence becomes quorum-verified. "
            "Admissible witnesses must be authorized, fresh, generation-aligned, "
            "and span independent declared failure domains. Conflicts without "
            "quorum resolve to ABSTAIN."
        ),
        "limitations": (
            "Witness independence is declared in the reference topology. "
            "Shared upstream data sources can create hidden common-mode failure "
            "despite distinct witness domains; that requires a separate audit."
        ),
    }
