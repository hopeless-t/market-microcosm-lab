from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class WorkItem:
    item_id: str
    resource_cost: int
    verification_cost: int
    verified_utility: int
    option_value: int
    mandatory: bool
    requires_verification: bool


@dataclass(frozen=True)
class PortfolioResult:
    selected_ids: tuple[str, ...]
    resource_used: int
    verification_used: int
    verified_utility: int
    option_value: int
    mandatory_complete: bool

    @property
    def total_value(self) -> int:
        return self.verified_utility + self.option_value


def frozen_items() -> tuple[WorkItem, ...]:
    return (
        WorkItem("E1", 3, 4, 12, 0, True, True),
        WorkItem("E2", 3, 4, 12, 0, True, True),
        WorkItem("R1", 1, 1, 2, 0, False, True),
        WorkItem("R2", 1, 1, 2, 0, False, True),
        WorkItem("R3", 1, 1, 2, 0, False, True),
        WorkItem("R4", 1, 1, 2, 0, False, True),
        WorkItem("P1", 2, 0, 0, 6, False, False),
        WorkItem("P2", 2, 0, 0, 6, False, False),
    )


def summarize(items: tuple[WorkItem, ...], selected: tuple[WorkItem, ...]) -> PortfolioResult:
    selected_ids = tuple(item.item_id for item in selected)
    mandatory_ids = {item.item_id for item in items if item.mandatory}
    return PortfolioResult(
        selected_ids=selected_ids,
        resource_used=sum(item.resource_cost for item in selected),
        verification_used=sum(item.verification_cost for item in selected),
        verified_utility=sum(item.verified_utility for item in selected),
        option_value=sum(item.option_value for item in selected),
        mandatory_complete=mandatory_ids.issubset(selected_ids),
    )


def verified_count_gate(
    items: tuple[WorkItem, ...], *, resource_budget: int = 12, verification_budget: int = 8
) -> PortfolioResult:
    candidates = sorted(
        (item for item in items if item.requires_verification),
        key=lambda item: (item.verification_cost, item.resource_cost, item.item_id),
    )
    selected: list[WorkItem] = []
    resource_used = 0
    verification_used = 0
    for item in candidates:
        if resource_used + item.resource_cost > resource_budget:
            continue
        if verification_used + item.verification_cost > verification_budget:
            continue
        selected.append(item)
        resource_used += item.resource_cost
        verification_used += item.verification_cost
    return summarize(items, tuple(selected))


def verified_utility_gate(
    items: tuple[WorkItem, ...], *, resource_budget: int = 12, verification_budget: int = 8
) -> PortfolioResult:
    candidates = sorted(
        (item for item in items if item.requires_verification),
        key=lambda item: (
            -(item.verified_utility / item.verification_cost),
            -item.verified_utility,
            item.item_id,
        ),
    )
    selected: list[WorkItem] = []
    resource_used = 0
    verification_used = 0
    for item in candidates:
        if resource_used + item.resource_cost > resource_budget:
            continue
        if verification_used + item.verification_cost > verification_budget:
            continue
        selected.append(item)
        resource_used += item.resource_cost
        verification_used += item.verification_cost
    return summarize(items, tuple(selected))


def option_preserving_exact(
    items: tuple[WorkItem, ...], *, resource_budget: int = 12, verification_budget: int = 8
) -> PortfolioResult:
    if resource_budget <= 0 or verification_budget < 0:
        raise ValueError("budgets must be non-negative and resource_budget positive")

    best: PortfolioResult | None = None
    for count in range(len(items) + 1):
        for subset in combinations(items, count):
            result = summarize(items, subset)
            if result.resource_used > resource_budget:
                continue
            if result.verification_used > verification_budget:
                continue
            if not result.mandatory_complete:
                continue
            if best is None:
                best = result
                continue
            candidate_key = (
                result.total_value,
                result.verified_utility,
                -result.resource_used,
                tuple(reversed(result.selected_ids)),
            )
            best_key = (
                best.total_value,
                best.verified_utility,
                -best.resource_used,
                tuple(reversed(best.selected_ids)),
            )
            if candidate_key > best_key:
                best = result

    if best is None:
        raise ValueError("no mandatory-complete feasible portfolio")
    return best
