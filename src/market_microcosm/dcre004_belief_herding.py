from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    prior_high: float
    high_state_value: float = 10.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.prior_high <= 1.0:
            raise ValueError("prior_high must be within [0, 1]")
        if self.high_state_value < 0.0:
            raise ValueError("high_state_value must be non-negative")


@dataclass(frozen=True)
class ProbeReport:
    assignments: tuple[str, ...]
    probe_count: int
    unique_opportunities: int
    duplicate_probes: int
    expected_discovery_value: float
    expected_value_per_probe: float


def frozen_opportunities() -> tuple[Opportunity, ...]:
    return (
        Opportunity("A", 0.80),
        Opportunity("B", 0.70),
        Opportunity("C", 0.60),
        Opportunity("D", 0.55),
    )


def summarize(
    opportunities: tuple[Opportunity, ...], assignments: tuple[str, ...]
) -> ProbeReport:
    by_id = {item.opportunity_id: item for item in opportunities}
    if len(by_id) != len(opportunities):
        raise ValueError("opportunity ids must be unique")
    if any(item_id not in by_id for item_id in assignments):
        raise ValueError("assignment references unknown opportunity")

    unique_ids = tuple(dict.fromkeys(assignments))
    expected = sum(
        by_id[item_id].prior_high * by_id[item_id].high_state_value
        for item_id in unique_ids
    )
    probe_count = len(assignments)
    return ProbeReport(
        assignments=assignments,
        probe_count=probe_count,
        unique_opportunities=len(unique_ids),
        duplicate_probes=probe_count - len(unique_ids),
        expected_discovery_value=expected,
        expected_value_per_probe=(expected / probe_count if probe_count else 0.0),
    )


def herd_allocation(
    opportunities: tuple[Opportunity, ...], *, actor_count: int = 4
) -> ProbeReport:
    if actor_count < 1:
        raise ValueError("actor_count must be positive")
    best = max(opportunities, key=lambda item: (item.prior_high, item.opportunity_id))
    return summarize(opportunities, tuple(best.opportunity_id for _ in range(actor_count)))


def diversified_allocation(
    opportunities: tuple[Opportunity, ...], *, probe_budget: int = 4
) -> ProbeReport:
    if probe_budget < 1:
        raise ValueError("probe_budget must be positive")
    ranked = sorted(
        opportunities,
        key=lambda item: (-item.prior_high, item.opportunity_id),
    )
    assignments = tuple(item.opportunity_id for item in ranked[:probe_budget])
    return summarize(opportunities, assignments)


def shared_observation_allocation(
    opportunities: tuple[Opportunity, ...]
) -> ProbeReport:
    best = max(opportunities, key=lambda item: (item.prior_high, item.opportunity_id))
    return summarize(opportunities, (best.opportunity_id,))
