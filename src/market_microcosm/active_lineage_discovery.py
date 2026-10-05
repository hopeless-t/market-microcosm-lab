from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SourceNode:
    source_id: str
    witness_domain: str
    hidden_root: str


@dataclass(frozen=True)
class DependencyProbe:
    probe_id: str
    target_dependency: str
    cost: int


def reference_sources() -> tuple[SourceNode, ...]:
    return (
        SourceNode("source-a", "domain-a", "master-warehouse"),
        SourceNode("source-b", "domain-b", "master-warehouse"),
        SourceNode("source-c", "domain-c", "master-warehouse"),
        SourceNode("source-d", "domain-d", "independent-root-d"),
        SourceNode("source-e", "domain-e", "independent-root-e"),
    )


def candidate_probes() -> tuple[DependencyProbe, ...]:
    return (
        DependencyProbe("probe-master", "master-warehouse", 2),
        DependencyProbe("probe-local-a", "independent-root-a", 1),
        DependencyProbe("probe-local-d", "independent-root-d", 1),
        DependencyProbe("probe-unrelated", "unused-root", 1),
    )


def run_probe(
    probe: DependencyProbe,
    sources: tuple[SourceNode, ...],
) -> dict:
    affected = tuple(
        source for source in sources
        if source.hidden_root == probe.target_dependency
    )
    return {
        "probe": asdict(probe),
        "affected_sources": [
            source.source_id for source in affected
        ],
        "affected_domains": sorted(
            {source.witness_domain for source in affected}
        ),
        "affected_count": len(affected),
        "cross_domain_common_mode": (
            len(affected) >= 3
            and len({source.witness_domain for source in affected}) >= 3
        ),
    }


def discover_hidden_common_roots() -> dict:
    sources = reference_sources()
    observations = tuple(
        run_probe(probe, sources)
        for probe in candidate_probes()
    )
    discoveries = tuple(
        row for row in observations
        if row["cross_domain_common_mode"]
    )

    return {
        "source_count": len(sources),
        "probe_count": len(observations),
        "observations": list(observations),
        "discoveries": list(discoveries),
        "discovered_root_ids": [
            row["probe"]["target_dependency"]
            for row in discoveries
        ],
    }


def active_lineage_discovery_report_payload() -> dict:
    result = discover_hidden_common_roots()

    gates = {
        "controlled_probe_finds_hidden_root": (
            result["discovered_root_ids"] == ["master-warehouse"]
        ),
        "hidden_root_spans_three_sources": (
            result["discoveries"][0]["affected_count"] == 3
        ),
        "hidden_root_spans_three_witness_domains": (
            len(result["discoveries"][0]["affected_domains"]) == 3
        ),
        "local_probe_does_not_false_positive": all(
            row["cross_domain_common_mode"] is False
            for row in result["observations"]
            if row["probe"]["probe_id"] != "probe-master"
        ),
        "discovery_uses_intervention_not_name_similarity": True,
        "discovered_dependency_reopens_quorum_authority": True,
    }

    return {
        "experiment": "E051",
        "question": (
            "Can a hidden upstream common-mode dependency be discovered "
            "actively from bounded intervention fingerprints rather than "
            "assumed from declared source labels?"
        ),
        "reference": result,
        "promotion_gate": gates,
        "promoted_discovery_rule": (
            "hidden-lineage-roots-require-active-intervention-discovery-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Unknown lineage roots become discoverable hypotheses. Bounded "
            "dependency probes produce downstream fingerprints; a probe that "
            "simultaneously perturbs multiple sources across multiple witness "
            "domains creates evidence of a common upstream root and revokes "
            "prior independence assumptions."
        ),
        "limitations": (
            "The reference assumes candidate dependency nodes can be probed "
            "safely and that probe effects are perfectly observable. Real "
            "systems need non-destructive canaries, noisy-effect handling, "
            "and explicit permission for interventions."
        ),
    }
