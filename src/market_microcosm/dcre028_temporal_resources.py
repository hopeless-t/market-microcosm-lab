from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TemporalAllocation:
    flexible_peak_tasks: float
    peak_tasks: float
    offpeak_tasks: float
    peak_energy: float
    peak_water: float
    offpeak_energy: float
    offpeak_water: float
    jointly_viable: bool


def evaluate_temporal_allocation(
    flexible_peak_tasks: float,
    *,
    flexible_total: float = 40.0,
    peak_base: float = 70.0,
    offpeak_base: float = 20.0,
    energy_per_task: float = 0.8,
    peak_water_per_task: float = 0.2,
    offpeak_water_per_task: float = 0.4,
    peak_energy_ceiling: float = 70.0,
    peak_water_ceiling: float = 30.0,
    offpeak_energy_ceiling: float = 100.0,
    offpeak_water_ceiling: float = 20.0,
) -> TemporalAllocation:
    if not 0.0 <= flexible_peak_tasks <= flexible_total:
        raise ValueError("flexible allocation must be within workload")
    peak_tasks = peak_base + flexible_peak_tasks
    offpeak_tasks = offpeak_base + flexible_total - flexible_peak_tasks
    peak_energy = peak_tasks * energy_per_task
    peak_water = peak_tasks * peak_water_per_task
    offpeak_energy = offpeak_tasks * energy_per_task
    offpeak_water = offpeak_tasks * offpeak_water_per_task
    viable = (
        peak_energy <= peak_energy_ceiling
        and peak_water <= peak_water_ceiling
        and offpeak_energy <= offpeak_energy_ceiling
        and offpeak_water <= offpeak_water_ceiling
    )
    return TemporalAllocation(
        flexible_peak_tasks=flexible_peak_tasks,
        peak_tasks=peak_tasks,
        offpeak_tasks=offpeak_tasks,
        peak_energy=peak_energy,
        peak_water=peak_water,
        offpeak_energy=offpeak_energy,
        offpeak_water=offpeak_water,
        jointly_viable=viable,
    )


def energy_shift_greedy() -> TemporalAllocation:
    return evaluate_temporal_allocation(0.0)


def water_shift_greedy() -> TemporalAllocation:
    return evaluate_temporal_allocation(40.0)


def exact_temporal_grid() -> TemporalAllocation:
    candidates = tuple(
        evaluate_temporal_allocation(value)
        for value in (0.0, 10.0, 20.0, 30.0, 40.0)
    )
    viable = tuple(row for row in candidates if row.jointly_viable)
    if not viable:
        raise ValueError("no jointly viable temporal allocation")
    return min(
        viable,
        key=lambda row: (
            max(row.peak_energy / 70.0, row.offpeak_water / 20.0),
            row.flexible_peak_tasks,
        ),
    )


def frozen_temporal_market() -> dict[str, TemporalAllocation]:
    return {
        "energy_greedy": energy_shift_greedy(),
        "water_greedy": water_shift_greedy(),
        "joint": exact_temporal_grid(),
    }
