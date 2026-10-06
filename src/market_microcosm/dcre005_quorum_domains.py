from __future__ import annotations

from itertools import product

from market_microcosm.failure_domain_diversity import WitnessTopology


def quorum_accuracy(
    topology: WitnessTopology,
    *,
    domain_accuracy: float = 0.8,
) -> float:
    if not 0.0 <= domain_accuracy <= 1.0:
        raise ValueError("domain_accuracy must be within [0, 1]")
    if topology.quorum_threshold < 1:
        raise ValueError("quorum threshold must be positive")

    domains = topology.domains
    total = 0.0
    for states in product((False, True), repeat=len(domains)):
        state_by_domain = dict(zip(domains, states, strict=True))
        probability = 1.0
        for correct in states:
            probability *= domain_accuracy if correct else (1.0 - domain_accuracy)
        correct_votes = sum(
            state_by_domain[domain] for domain in topology.witness_domains
        )
        if correct_votes >= topology.quorum_threshold:
            total += probability
    return total


def frozen_topologies() -> tuple[WitnessTopology, ...]:
    return (
        WitnessTopology(
            name="same-domain-3",
            witness_domains=("a", "a", "a"),
            quorum_threshold=2,
        ),
        WitnessTopology(
            name="correlated-pair-2-1",
            witness_domains=("a", "a", "b"),
            quorum_threshold=2,
        ),
        WitnessTopology(
            name="independent-1-1-1",
            witness_domains=("a", "b", "c"),
            quorum_threshold=2,
        ),
    )


def frozen_quorum_report() -> dict[str, dict[str, float | int]]:
    return {
        topology.name: {
            "nominal_witnesses": topology.witness_count,
            "independent_domains": topology.domain_count,
            "majority_accuracy": quorum_accuracy(topology),
        }
        for topology in frozen_topologies()
    }
