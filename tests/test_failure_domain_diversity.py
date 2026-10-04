from market_microcosm.failure_domain_diversity import (
    exact_domain_event_probability,
    failure_domain_report_payload,
    minimum_domains_to_forge,
    reference_topologies,
)


def test_minimum_domain_compromise_boundary() -> None:
    topologies = {row.name: row for row in reference_topologies()}

    assert minimum_domains_to_forge(
        topologies["concentrated-3-1-1"]
    ) == 1
    assert minimum_domains_to_forge(
        topologies["balanced-2-2-1"]
    ) == 2
    assert minimum_domains_to_forge(
        topologies["independent-1-1-1-1-1"]
    ) == 3


def test_exact_probability_at_ten_percent() -> None:
    topologies = {row.name: row for row in reference_topologies()}

    concentrated = exact_domain_event_probability(
        topologies["concentrated-3-1-1"],
        domain_event_probability=0.10,
        event="forge",
    )
    balanced = exact_domain_event_probability(
        topologies["balanced-2-2-1"],
        domain_event_probability=0.10,
        event="forge",
    )
    independent = exact_domain_event_probability(
        topologies["independent-1-1-1-1-1"],
        domain_event_probability=0.10,
        event="forge",
    )

    assert abs(concentrated - 0.10) < 1e-12
    assert abs(balanced - 0.028) < 1e-12
    assert abs(independent - 0.00856) < 1e-12


def test_e022_promotion_contract() -> None:
    payload = failure_domain_report_payload()
    assert all(payload["promotion_gate"].values())
    independent = payload["topologies"]["independent-1-1-1-1-1"]
    assert independent["minimum_domains_to_forge"] == 3
    assert (
        payload["promoted_failure_domain_rule"]
        == "quorum-witnesses-must-span-at-least-three-independent-domains-v1"
    )
