from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.audit_portfolio import AuditItem, dp_schedule, exhaustive_schedule


@dataclass(frozen=True)
class BacklogClass:
    name: str
    size: int
    current_value: int
    delayed_value: int
    arrival_order: int

    @property
    def delay_loss(self) -> int:
        return self.current_value - self.delayed_value


def frozen_backlog_classes() -> tuple[BacklogClass, ...]:
    return (
        BacklogClass("BULK", 20, 20, 20, 0),
        BacklogClass("URGENT", 10, 40, 10, 1),
        BacklogClass("FLEX", 10, 20, 18, 2),
    )


def fifo_recovery(
    classes: tuple[BacklogClass, ...], *, capacity: int = 20
) -> tuple[BacklogClass, ...]:
    remaining = capacity
    selected: list[BacklogClass] = []
    for row in sorted(classes, key=lambda item: (item.arrival_order, item.name)):
        if row.size <= remaining:
            selected.append(row)
            remaining -= row.size
    return tuple(selected)


def to_e018_items(classes: tuple[BacklogClass, ...]) -> tuple[AuditItem, ...]:
    return tuple(
        AuditItem(
            name=row.name,
            audit_cost_units=row.size,
            restoration_value=row.delay_loss,
        )
        for row in classes
    )


def preserved_value(
    classes: tuple[BacklogClass, ...], selected_names: tuple[str, ...]
) -> int:
    selected = set(selected_names)
    return sum(
        row.current_value if row.name in selected else row.delayed_value
        for row in classes
    )


def frozen_backlog_portfolio() -> dict:
    classes = frozen_backlog_classes()
    fifo = fifo_recovery(classes)
    items = to_e018_items(classes)
    oracle = exhaustive_schedule(items, budget_units=20)
    dp = dp_schedule(items, budget_units=20)
    return {
        "fifo_names": tuple(row.name for row in fifo),
        "fifo_preserved_value": preserved_value(
            classes, tuple(row.name for row in fifo)
        ),
        "oracle": oracle,
        "dp": dp,
        "dp_preserved_value": preserved_value(classes, dp.selected_names),
        "dp_matches_oracle": (
            dp.selected_names == oracle.selected_names
            and dp.total_restoration_value == oracle.total_restoration_value
            and dp.total_cost_units == oracle.total_cost_units
        ),
    }
