from __future__ import annotations

from market_microcosm.failure_domain_diversity import (
    WitnessTopology,
    exact_domain_event_probability,
    minimum_domains_to_break_availability,
)


def reserve_topologies() -> tuple[WitnessTopology, WitnessTopology]:
    return (
        WitnessTopology(
            name="reserve-concentrated-2-1",
            witness_domains=("grid-x", "grid-x", "grid-y"),
            quorum_threshold=2,
        ),
        WitnessTopology(
            name="reserve-independent-1-1-1",
            witness_domains=("grid-a", "grid-b", "grid-c"),
            quorum_threshold=2,
        ),
    )


def frozen_reserve_domains() -> dict:
    concentrated, independent = reserve_topologies()
    q = 0.10
    return {
        "concentrated": concentrated,
        "independent": independent,
        "concentrated_min_domains_to_break": minimum_domains_to_break_availability(concentrated),
        "independent_min_domains_to_break": minimum_domains_to_break_availability(independent),
        "concentrated_loss_probability": exact_domain_event_probability(
            concentrated,
            domain_event_probability=q,
            event="availability-loss",
        ),
        "independent_loss_probability": exact_domain_event_probability(
            independent,
            domain_event_probability=q,
            event="availability-loss",
        ),
    }
