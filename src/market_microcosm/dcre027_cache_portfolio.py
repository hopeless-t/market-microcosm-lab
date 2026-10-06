from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.audit_portfolio import AuditItem, dp_schedule, exhaustive_schedule


@dataclass(frozen=True)
class CacheCandidate:
    name: str
    storage_units: int
    request_count: int
    network_relief_per_valid_hit: float
    invalidation_probability: float

    def __post_init__(self) -> None:
        if self.storage_units <= 0 or self.request_count < 0:
            raise ValueError("storage must be positive and requests non-negative")
        if self.network_relief_per_valid_hit < 0.0:
            raise ValueError("network relief must be non-negative")
        if not 0.0 <= self.invalidation_probability <= 1.0:
            raise ValueError("invalidation probability must be within [0, 1]")

    @property
    def expected_network_relief(self) -> float:
        return (
            self.request_count
            * (1.0 - self.invalidation_probability)
            * self.network_relief_per_valid_hit
        )


def frozen_candidates() -> tuple[CacheCandidate, ...]:
    return (
        CacheCandidate("HOT_BIG", 8, 10, 1.0, 0.40),
        CacheCandidate("WARM_A", 5, 7, 2.0, 0.00),
        CacheCandidate("WARM_B", 5, 6, 2.0, 0.00),
    )


def frequency_greedy(
    candidates: tuple[CacheCandidate, ...], *, storage_budget: int = 10
) -> tuple[CacheCandidate, ...]:
    if storage_budget < 0:
        raise ValueError("storage budget must be non-negative")
    remaining = storage_budget
    selected: list[CacheCandidate] = []
    for candidate in sorted(
        candidates,
        key=lambda item: (-item.request_count, item.storage_units, item.name),
    ):
        if candidate.storage_units <= remaining:
            selected.append(candidate)
            remaining -= candidate.storage_units
    return tuple(selected)


def to_e018_items(candidates: tuple[CacheCandidate, ...]) -> tuple[AuditItem, ...]:
    items = []
    for candidate in candidates:
        value = candidate.expected_network_relief
        if not float(value).is_integer():
            raise ValueError("frozen projection requires integer expected relief")
        items.append(
            AuditItem(
                candidate.name,
                audit_cost_units=candidate.storage_units,
                restoration_value=int(value),
            )
        )
    return tuple(items)


def frozen_cache_portfolio() -> dict:
    candidates = frozen_candidates()
    greedy = frequency_greedy(candidates)
    items = to_e018_items(candidates)
    oracle = exhaustive_schedule(items, budget_units=10)
    dp = dp_schedule(items, budget_units=10)
    return {
        "frequency_greedy_names": tuple(item.name for item in greedy),
        "frequency_greedy_relief": sum(
            item.expected_network_relief for item in greedy
        ),
        "oracle": oracle,
        "dp": dp,
        "dp_matches_oracle": (
            dp.selected_names == oracle.selected_names
            and dp.total_restoration_value == oracle.total_restoration_value
            and dp.total_cost_units == oracle.total_cost_units
        ),
    }
