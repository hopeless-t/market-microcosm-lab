from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations


@dataclass(frozen=True)
class WitnessTopology:
    name: str
    witness_domains: tuple[str, ...]
    quorum_threshold: int = 3

    @property
    def witness_count(self) -> int:
        return len(self.witness_domains)

    @property
    def domains(self) -> tuple[str, ...]:
        return tuple(sorted(set(self.witness_domains)))

    @property
    def domain_count(self) -> int:
        return len(self.domains)

    @property
    def domain_sizes(self) -> dict[str, int]:
        return {
            domain: self.witness_domains.count(domain)
            for domain in self.domains
        }


@dataclass(frozen=True)
class DomainSubsetOutcome:
    compromised_domains: tuple[str, ...]
    compromised_witnesses: int
    forged_quorum_possible: bool
    available_witnesses: int
    quorum_available_after_outage: bool


def reference_topologies() -> tuple[WitnessTopology, ...]:
    return (
        WitnessTopology(
            name="concentrated-3-1-1",
            witness_domains=("a", "a", "a", "b", "c"),
        ),
        WitnessTopology(
            name="balanced-2-2-1",
            witness_domains=("a", "a", "b", "b", "c"),
        ),
        WitnessTopology(
            name="independent-1-1-1-1-1",
            witness_domains=("a", "b", "c", "d", "e"),
        ),
    )


def enumerate_domain_subsets(
    topology: WitnessTopology,
) -> tuple[DomainSubsetOutcome, ...]:
    outcomes: list[DomainSubsetOutcome] = []
    domains = topology.domains
    sizes = topology.domain_sizes

    for size in range(len(domains) + 1):
        for subset in combinations(domains, size):
            compromised_witnesses = sum(
                sizes[domain] for domain in subset
            )
            available_witnesses = (
                topology.witness_count - compromised_witnesses
            )
            outcomes.append(
                DomainSubsetOutcome(
                    compromised_domains=tuple(subset),
                    compromised_witnesses=compromised_witnesses,
                    forged_quorum_possible=(
                        compromised_witnesses
                        >= topology.quorum_threshold
                    ),
                    available_witnesses=available_witnesses,
                    quorum_available_after_outage=(
                        available_witnesses
                        >= topology.quorum_threshold
                    ),
                )
            )
    return tuple(outcomes)


def minimum_domains_to_forge(topology: WitnessTopology) -> int:
    forged = [
        len(row.compromised_domains)
        for row in enumerate_domain_subsets(topology)
        if row.forged_quorum_possible
    ]
    if not forged:
        raise ValueError("quorum cannot be reached")
    return min(forged)


def minimum_domains_to_break_availability(
    topology: WitnessTopology,
) -> int:
    broken = [
        len(row.compromised_domains)
        for row in enumerate_domain_subsets(topology)
        if not row.quorum_available_after_outage
    ]
    if not broken:
        raise ValueError("quorum cannot be made unavailable")
    return min(broken)


def exact_domain_event_probability(
    topology: WitnessTopology,
    *,
    domain_event_probability: float,
    event: str,
) -> float:
    if not 0.0 <= domain_event_probability <= 1.0:
        raise ValueError("domain_event_probability must be in [0, 1]")
    if event not in {"forge", "availability-loss"}:
        raise ValueError(event)

    probability = 0.0
    domain_count = topology.domain_count
    for row in enumerate_domain_subsets(topology):
        event_count = len(row.compromised_domains)
        subset_probability = (
            domain_event_probability**event_count
            * (1.0 - domain_event_probability)
            ** (domain_count - event_count)
        )
        triggered = (
            row.forged_quorum_possible
            if event == "forge"
            else not row.quorum_available_after_outage
        )
        if triggered:
            probability += subset_probability
    return probability


def topology_metrics(
    topology: WitnessTopology,
    *,
    domain_compromise_probability: float,
    domain_outage_probability: float,
) -> dict:
    sizes = topology.domain_sizes
    outcomes = enumerate_domain_subsets(topology)
    return {
        "name": topology.name,
        "witness_count": topology.witness_count,
        "quorum_threshold": topology.quorum_threshold,
        "domain_count": topology.domain_count,
        "domain_sizes": sizes,
        "maximum_domain_witnesses": max(sizes.values()),
        "maximum_domain_share": max(sizes.values()) / topology.witness_count,
        "minimum_domains_to_forge": minimum_domains_to_forge(topology),
        "minimum_domains_to_break_availability": (
            minimum_domains_to_break_availability(topology)
        ),
        "forge_probability": exact_domain_event_probability(
            topology,
            domain_event_probability=domain_compromise_probability,
            event="forge",
        ),
        "availability_loss_probability": exact_domain_event_probability(
            topology,
            domain_event_probability=domain_outage_probability,
            event="availability-loss",
        ),
        "enumerated_domain_subsets": len(outcomes),
    }


def sweep_probabilities(
    topology: WitnessTopology,
    *,
    probabilities: tuple[float, ...],
) -> tuple[dict, ...]:
    return tuple(
        {
            "domain_probability": probability,
            "forge_probability": exact_domain_event_probability(
                topology,
                domain_event_probability=probability,
                event="forge",
            ),
            "availability_loss_probability": exact_domain_event_probability(
                topology,
                domain_event_probability=probability,
                event="availability-loss",
            ),
        }
        for probability in probabilities
    )


def failure_domain_report_payload() -> dict:
    topologies = reference_topologies()
    compromise_probability = 0.10
    outage_probability = 0.10
    sweep = (0.01, 0.05, 0.10, 0.20)

    metrics = {
        topology.name: topology_metrics(
            topology,
            domain_compromise_probability=compromise_probability,
            domain_outage_probability=outage_probability,
        )
        for topology in topologies
    }
    sweeps = {
        topology.name: sweep_probabilities(
            topology,
            probabilities=sweep,
        )
        for topology in topologies
    }

    concentrated = metrics["concentrated-3-1-1"]
    balanced = metrics["balanced-2-2-1"]
    independent = metrics["independent-1-1-1-1-1"]

    forge_reduction_vs_concentrated = (
        1.0
        - independent["forge_probability"]
        / concentrated["forge_probability"]
    )
    balanced_reduction_vs_concentrated = (
        1.0
        - balanced["forge_probability"]
        / concentrated["forge_probability"]
    )

    gates = {
        "concentrated_topology_collapses_to_one_domain_forge": (
            concentrated["minimum_domains_to_forge"] == 1
        ),
        "balanced_topology_requires_two_domains": (
            balanced["minimum_domains_to_forge"] == 2
        ),
        "independent_topology_requires_three_domains": (
            independent["minimum_domains_to_forge"] == 3
        ),
        "independent_domain_model_forge_probability_below_one_percent_at_10pct": (
            independent["forge_probability"] < 0.01
        ),
        "independent_topology_reduces_forge_probability_over_90_percent": (
            forge_reduction_vs_concentrated > 0.90
        ),
        "availability_failure_boundary_matches_quorum_loss_geometry": all(
            row["minimum_domains_to_break_availability"]
            == row["minimum_domains_to_forge"]
            for row in metrics.values()
        ),
        "exact_subset_enumeration_complete": all(
            row["enumerated_domain_subsets"]
            == 2 ** row["domain_count"]
            for row in metrics.values()
        ),
    }

    return {
        "experiment": "E022",
        "question": (
            "How much of a nominal 3-of-5 witness quorum survives after "
            "correlated witness failures are represented at the failure-domain level?"
        ),
        "domain_model": {
            "domain_compromise_probability": compromise_probability,
            "domain_outage_probability": outage_probability,
            "assumption": (
                "domains fail independently; witnesses inside one domain "
                "fail or are compromised together"
            ),
        },
        "topologies": metrics,
        "probability_sweeps": sweeps,
        "comparison": {
            "balanced_forge_reduction_vs_concentrated": (
                balanced_reduction_vs_concentrated
            ),
            "independent_forge_reduction_vs_concentrated": (
                forge_reduction_vs_concentrated
            ),
            "concentrated_forge_probability": (
                concentrated["forge_probability"]
            ),
            "balanced_forge_probability": balanced["forge_probability"],
            "independent_forge_probability": independent["forge_probability"],
        },
        "promotion_gate": gates,
        "promoted_failure_domain_rule": (
            "quorum-witnesses-must-span-at-least-three-independent-domains-v1"
            if all(gates.values())
            else None
        ),
        "limitation": (
            "Domain independence and homogeneous event probabilities are "
            "synthetic assumptions. Real correlated risks require empirical "
            "dependency models and must not be inferred from nominal provider "
            "or region labels alone."
        ),
    }
