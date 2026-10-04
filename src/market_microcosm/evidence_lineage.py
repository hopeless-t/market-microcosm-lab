from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import Counter


@dataclass(frozen=True)
class LineageWitness:
    witness_id: str
    failure_domain: str
    source_id: str
    root_lineage: str
    predicate_value: bool


def verify_lineage_quorum(
    witnesses: tuple[LineageWitness, ...],
    *,
    threshold: int = 3,
    require_distinct_sources: bool,
    require_distinct_roots: bool,
) -> dict:
    votes = Counter(w.predicate_value for w in witnesses)

    accepted_value = None
    accepted_domains: list[str] = []
    accepted_sources: list[str] = []
    accepted_roots: list[str] = []

    for value in (True, False):
        matching = [w for w in witnesses if w.predicate_value is value]
        domains = sorted({w.failure_domain for w in matching})
        sources = sorted({w.source_id for w in matching})
        roots = sorted({w.root_lineage for w in matching})

        if votes[value] < threshold:
            continue
        if len(domains) < threshold:
            continue
        if require_distinct_sources and len(sources) < threshold:
            continue
        if require_distinct_roots and len(roots) < threshold:
            continue

        accepted_value = value
        accepted_domains = domains
        accepted_sources = sources
        accepted_roots = roots
        break

    return {
        "threshold": threshold,
        "require_distinct_sources": require_distinct_sources,
        "require_distinct_roots": require_distinct_roots,
        "accepted": accepted_value is not None,
        "accepted_value": accepted_value,
        "accepted_domains": accepted_domains,
        "accepted_sources": accepted_sources,
        "accepted_roots": accepted_roots,
        "true_votes": votes[True],
        "false_votes": votes[False],
    }


def hidden_root_reference() -> dict:
    witnesses = (
        LineageWitness(
            "w0", "domain-a", "source-a", "master-warehouse", False
        ),
        LineageWitness(
            "w1", "domain-b", "source-b", "master-warehouse", False
        ),
        LineageWitness(
            "w2", "domain-c", "source-c", "master-warehouse", False
        ),
        LineageWitness(
            "w3", "domain-d", "source-d", "independent-root-d", True
        ),
        LineageWitness(
            "w4", "domain-e", "source-e", "independent-root-e", True
        ),
    )

    source_aware = verify_lineage_quorum(
        witnesses,
        require_distinct_sources=True,
        require_distinct_roots=False,
    )
    root_aware = verify_lineage_quorum(
        witnesses,
        require_distinct_sources=True,
        require_distinct_roots=True,
    )

    return {
        "witnesses": [asdict(w) for w in witnesses],
        "ground_truth_reference": True,
        "source_aware_quorum": source_aware,
        "root_aware_quorum": root_aware,
    }


def lineage_diversified_repair() -> dict:
    witnesses = (
        LineageWitness("w0", "domain-a", "source-a", "root-a", True),
        LineageWitness("w1", "domain-b", "source-b", "root-b", True),
        LineageWitness("w2", "domain-c", "source-c", "root-c", True),
        LineageWitness(
            "w3", "domain-d", "bad-source-d", "shared-bad-root", False
        ),
        LineageWitness(
            "w4", "domain-e", "bad-source-e", "shared-bad-root", False
        ),
    )

    return verify_lineage_quorum(
        witnesses,
        require_distinct_sources=True,
        require_distinct_roots=True,
    )


def evidence_lineage_report_payload() -> dict:
    hidden = hidden_root_reference()
    repair = lineage_diversified_repair()

    source_aware = hidden["source_aware_quorum"]
    root_aware = hidden["root_aware_quorum"]

    gates = {
        "distinct_immediate_sources_can_share_one_root": (
            source_aware["accepted"] is True
            and source_aware["accepted_value"] is False
            and len(source_aware["accepted_sources"]) >= 3
            and len(source_aware["accepted_roots"]) == 1
        ),
        "root_lineage_audit_revokes_false_quorum": (
            root_aware["accepted"] is False
        ),
        "diversified_roots_restore_true_quorum": (
            repair["accepted"] is True
            and repair["accepted_value"] is True
            and len(repair["accepted_roots"]) >= 3
        ),
        "source_labels_are_not_independence_proof": True,
        "lineage_graph_is_part_of_evidence_identity": True,
        "hidden_root_discovery_revokes_prior_source_diversity_authority": True,
    }

    return {
        "experiment": "E050",
        "question": (
            "Can three distinct upstream source labels still form one hidden "
            "common-mode failure when all three ultimately derive from the "
            "same root dataset or warehouse?"
        ),
        "hidden_root_reference": hidden,
        "lineage_diversified_repair": repair,
        "promotion_gate": gates,
        "promoted_lineage_rule": (
            "predicate-quorum-must-audit-upstream-lineage-roots-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Evidence independence is represented as a lineage graph, not a "
            "flat list of source labels. Quorum authority depends on the "
            "minimum independent upstream roots supporting the accepted view."
        ),
        "limitations": (
            "The lineage graph is declared in this reference. Real systems can "
            "contain undiscovered vendor, ETL, warehouse, identity, or network "
            "common modes that require active dependency discovery."
        ),
    }
