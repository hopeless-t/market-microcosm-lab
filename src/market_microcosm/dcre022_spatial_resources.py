from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    name: str
    energy_ceiling: float
    water_ceiling: float


@dataclass(frozen=True)
class RegionalAllocation:
    policy: str
    grid_rich_tasks: float
    water_rich_tasks: float
    grid_rich_energy: float
    grid_rich_water: float
    water_rich_energy: float
    water_rich_water: float
    jointly_viable: bool


def frozen_regions() -> tuple[Region, Region]:
    return (
        Region("GRID_RICH", energy_ceiling=100.0, water_ceiling=20.0),
        Region("WATER_RICH", energy_ceiling=50.0, water_ceiling=100.0),
    )


def evaluate_allocation(
    grid_rich_tasks: float,
    *,
    total_tasks: float = 100.0,
    energy_per_task: float = 0.8,
    water_per_task: float = 0.3,
    policy: str = "CUSTOM",
) -> RegionalAllocation:
    if not 0.0 <= grid_rich_tasks <= total_tasks:
        raise ValueError("allocation must be within total tasks")
    grid, water = frozen_regions()
    water_rich_tasks = total_tasks - grid_rich_tasks
    ge = grid_rich_tasks * energy_per_task
    gw = grid_rich_tasks * water_per_task
    we = water_rich_tasks * energy_per_task
    ww = water_rich_tasks * water_per_task
    viable = (
        ge <= grid.energy_ceiling
        and gw <= grid.water_ceiling
        and we <= water.energy_ceiling
        and ww <= water.water_ceiling
    )
    return RegionalAllocation(
        policy=policy,
        grid_rich_tasks=grid_rich_tasks,
        water_rich_tasks=water_rich_tasks,
        grid_rich_energy=ge,
        grid_rich_water=gw,
        water_rich_energy=we,
        water_rich_water=ww,
        jointly_viable=viable,
    )


def energy_headroom_greedy() -> RegionalAllocation:
    return evaluate_allocation(100.0, policy="ENERGY_HEADROOM_GREEDY")


def water_headroom_greedy() -> RegionalAllocation:
    return evaluate_allocation(0.0, policy="WATER_HEADROOM_GREEDY")


def exact_joint_grid() -> RegionalAllocation:
    candidates = tuple(
        evaluate_allocation(value, policy="EXACT_JOINT_GRID")
        for value in (0.0, 25.0, 50.0, 75.0, 100.0)
    )
    viable = tuple(row for row in candidates if row.jointly_viable)
    if not viable:
        raise ValueError("no jointly viable allocation on frozen grid")
    return min(
        viable,
        key=lambda row: (
            max(
                row.grid_rich_energy / 100.0,
                row.grid_rich_water / 20.0,
                row.water_rich_energy / 50.0,
                row.water_rich_water / 100.0,
            ),
            row.grid_rich_tasks,
        ),
    )


def frozen_spatial_allocation() -> dict[str, RegionalAllocation]:
    return {
        "energy_greedy": energy_headroom_greedy(),
        "water_greedy": water_headroom_greedy(),
        "joint": exact_joint_grid(),
    }
