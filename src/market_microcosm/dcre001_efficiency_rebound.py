from __future__ import annotations

from dataclasses import dataclass
from itertools import product


EFFICIENCY_RATIOS = (1.0, 0.8, 0.6, 0.4)
DEMAND_ELASTICITIES = (0.0, 0.5, 1.0, 1.5, 2.0)
CAPACITY_RESPONSES = (0.0, 0.5, 1.0)


@dataclass(frozen=True)
class DCRECell:
    efficiency_ratio: float
    demand_elasticity: float
    capacity_response: float
    demand: float
    capacity: float
    served_open: float
    resource_open: float
    verified_open: float
    served_verified_gate: float
    resource_verified_gate: float
    verified_gate: float
    rebound_class: str
    verification_starved: bool


def evaluate_cell(
    efficiency_ratio: float,
    demand_elasticity: float,
    capacity_response: float,
    *,
    baseline_demand: float = 100.0,
    baseline_capacity: float = 100.0,
    verification_capacity: float = 120.0,
) -> DCRECell:
    if not 0.0 < efficiency_ratio <= 1.0:
        raise ValueError("efficiency_ratio must be within (0, 1]")
    if demand_elasticity < 0.0:
        raise ValueError("demand_elasticity must be non-negative")
    if not 0.0 <= capacity_response <= 1.0:
        raise ValueError("capacity_response must be within [0, 1]")
    if baseline_demand <= 0 or baseline_capacity <= 0 or verification_capacity <= 0:
        raise ValueError("capacities and baseline demand must be positive")

    demand = baseline_demand * (1.0 / efficiency_ratio) ** demand_elasticity
    capacity = baseline_capacity * (
        1.0 + capacity_response * (demand / baseline_demand - 1.0)
    )
    served_open = min(demand, capacity)
    resource_open = efficiency_ratio * served_open
    verified_open = min(served_open, verification_capacity)

    served_verified_gate = min(served_open, verification_capacity)
    resource_verified_gate = efficiency_ratio * served_verified_gate
    verified_gate = served_verified_gate

    baseline_resource = baseline_demand
    tolerance = 1e-9
    if resource_open < baseline_resource - tolerance:
        rebound_class = "CONSERVATION"
    elif resource_open > baseline_resource + tolerance:
        rebound_class = "BACKFIRE"
    else:
        rebound_class = "FULL_REBOUND"

    return DCRECell(
        efficiency_ratio=efficiency_ratio,
        demand_elasticity=demand_elasticity,
        capacity_response=capacity_response,
        demand=demand,
        capacity=capacity,
        served_open=served_open,
        resource_open=resource_open,
        verified_open=verified_open,
        served_verified_gate=served_verified_gate,
        resource_verified_gate=resource_verified_gate,
        verified_gate=verified_gate,
        rebound_class=rebound_class,
        verification_starved=served_open > verification_capacity + tolerance,
    )


def exact_grid() -> tuple[DCRECell, ...]:
    return tuple(
        evaluate_cell(efficiency, elasticity, response)
        for efficiency, elasticity, response in product(
            EFFICIENCY_RATIOS,
            DEMAND_ELASTICITIES,
            CAPACITY_RESPONSES,
        )
    )


def grid_summary(cells: tuple[DCRECell, ...] | None = None) -> dict[str, float | int]:
    cells = exact_grid() if cells is None else cells
    if not cells:
        raise ValueError("cells must be non-empty")

    class_counts = {
        name: sum(cell.rebound_class == name for cell in cells)
        for name in ("CONSERVATION", "FULL_REBOUND", "BACKFIRE")
    }
    resource_open = sum(cell.resource_open for cell in cells)
    resource_gate = sum(cell.resource_verified_gate for cell in cells)
    verified_open = sum(cell.verified_open for cell in cells)
    verified_gate = sum(cell.verified_gate for cell in cells)

    return {
        "cell_count": len(cells),
        "conservation_cells": class_counts["CONSERVATION"],
        "full_rebound_cells": class_counts["FULL_REBOUND"],
        "backfire_cells": class_counts["BACKFIRE"],
        "verification_starved_cells": sum(cell.verification_starved for cell in cells),
        "aggregate_resource_open": resource_open,
        "aggregate_resource_verified_gate": resource_gate,
        "aggregate_verified_open": verified_open,
        "aggregate_verified_gate": verified_gate,
        "verified_gate_resource_reduction_fraction": (resource_open - resource_gate)
        / resource_open,
    }
