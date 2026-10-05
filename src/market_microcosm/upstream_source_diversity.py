from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import Counter


@dataclass(frozen=True)
class SourcedWitness:
    witness_id: str
    failure_domain: str
    upstream_source: str
    predicate_value: bool


def verify_quorum(
    witnesses: tuple[SourcedWitness, ...],
    *,
    threshold: int = 3,
    require_source_diversity: bool,
) -> dict:
    votes = Counter(w.predicate_value for w in witnesses)

    accepted_value = None
    accepted_domains: list[str] = []
    accepted_sources: list[str] = []

    for value in (True, False):
        matching = [w for w in witnesses if w.predicate_value is value]
        domains = sorted({w.failure_domain for w in matching})
        sources = sorted({w.upstream_source for w in matching})

        enough_votes = votes[value] >= threshold
        enough_domains = len(domains) >= threshold
        enough_sources = (
            len(sources) >= threshold
            if require_source_diversity
            else True
        )

        if enough_votes and enough_domains and enough_sources:
            accepted_value = value
            accepted_domains = domains
            accepted_sources = sources
            break

    return {
        "threshold": threshold,
        "require_source_diversity": require_source_diversity,
        "true_votes": votes[True],
        "false_votes": votes[False],
        "accepted": accepted_value is not None,
        "accepted_value": accepted_value,
        "accepted_domains": accepted_domains,
        "accepted_sources": accepted_sources,
    }


def hidden_common_source_reference() -> dict:
    witnesses = (
        SourcedWitness("w0", "domain-a", "shared-feed", False),
        SourcedWitness("w1", "domain-b", "shared-feed", False),
        SourcedWitness("w2", "domain-c", "shared-feed", False),
        SourcedWitness("w3", "domain-d", "independent-d", True),
        SourcedWitness("w4", "domain-e", "independent-e", True),
    )

    domain_only = verify_quorum(
        witnesses,
        require_source_diversity=False,
    )
    source_aware = verify_quorum(
        witnesses,
        require_source_diversity=True,
    )

    return {
        "witnesses": [asdict(w) for w in witnesses],
        "ground_truth_reference": True,
        "domain_only_quorum": domain_only,
        "source_aware_quorum": source_aware,
    }


def diversified_repair_reference() -> dict:
    witnesses = (
        SourcedWitness("w0", "domain-a", "source-a", True),
        SourcedWitness("w1", "domain-b", "source-b", True),
        SourcedWitness("w2", "domain-c", "source-c", True),
        SourcedWitness("w3", "domain-d", "shared-bad-feed", False),
        SourcedWitness("w4", "domain-e", "shared-bad-feed", False),
    )

    return verify_quorum(
        witnesses,
        require_source_diversity=True,
    )


def upstream_source_diversity_report_payload() -> dict:
    hidden = hidden_common_source_reference()
    repair = diversified_repair_reference()

    gates = {
        "domain_only_quorum_can_accept_false_common_mode": (
            hidden["domain_only_quorum"]["accepted"] is True
            and hidden["domain_only_quorum"]["accepted_value"] is False
        ),
        "false_quorum_spans_three_domains_but_one_source": (
            len(hidden["domain_only_quorum"]["accepted_domains"]) >= 3
            and len(hidden["domain_only_quorum"]["accepted_sources"]) == 1
        ),
        "source_diversity_revokes_false_quorum": (
            hidden["source_aware_quorum"]["accepted"] is False
        ),
        "diversified_repair_accepts_true": (
            repair["accepted"] is True
            and repair["accepted_value"] is True
            and len(repair["accepted_sources"]) >= 3
        ),
        "witness_identity_and_domain_diversity_are_not_source_independence": True,
        "common_upstream_sources_are_audited_explicitly": True,
    }

    return {
        "experiment": "E049",
        "question": (
            "Can a predicate quorum spanning independent witness domains still "
            "accept a false result when enough witnesses share one corrupted "
            "upstream evidence source?"
        ),
        "hidden_common_source_reference": hidden,
        "diversified_repair_reference": repair,
        "promotion_gate": gates,
        "promoted_source_rule": (
            "predicate-quorum-must-diversify-upstream-evidence-sources-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Predicate attestation quorum now tracks both witness failure "
            "domains and upstream evidence-source dependencies. Distinct "
            "attesters do not count as independent evidence when their data "
            "lineage collapses onto one shared source."
        ),
        "limitations": (
            "The source graph is declared in the reference. Undiscovered "
            "common-mode dependencies can still invalidate the diversity claim "
            "and require the same revoke/re-audit lifecycle as E023."
        ),
    }
