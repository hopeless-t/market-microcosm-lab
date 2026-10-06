from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoolingTechnology:
    name: str
    energy_per_task: float
    water_per_task: float

    def __post_init__(self) -> None:
        if min(self.energy_per_task, self.water_per_task) < 0.0:
            raise ValueError("resource intensities must be non-negative")


@dataclass(frozen=True)
class CoolingChoice:
    policy: str
    technology: CoolingTechnology
    throughput: float
    total_energy: float
    total_water: float
    energy_viable: bool
    water_viable: bool

    @property
    def jointly_viable(self) -> bool:
        return self.energy_viable and self.water_viable


def frozen_technologies() -> tuple[CoolingTechnology, ...]:
    return (
        CoolingTechnology("DRY", energy_per_task=1.00, water_per_task=0.05),
        CoolingTechnology("WET", energy_per_task=0.70, water_per_task=0.50),
        CoolingTechnology("HYBRID", energy_per_task=0.82, water_per_task=0.20),
    )


def evaluate(
    technology: CoolingTechnology,
    *,
    policy: str,
    throughput: float = 120.0,
    energy_ceiling: float = 100.0,
    water_ceiling: float = 30.0,
) -> CoolingChoice:
    if min(throughput, energy_ceiling, water_ceiling) <= 0.0:
        raise ValueError("throughput and ceilings must be positive")
    energy = technology.energy_per_task * throughput
    water = technology.water_per_task * throughput
    return CoolingChoice(
        policy=policy,
        technology=technology,
        throughput=throughput,
        total_energy=energy,
        total_water=water,
        energy_viable=energy <= energy_ceiling,
        water_viable=water <= water_ceiling,
    )


def choose_energy_only() -> CoolingChoice:
    technology = min(frozen_technologies(), key=lambda row: (row.energy_per_task, row.name))
    return evaluate(technology, policy="ENERGY_ONLY")


def choose_water_only() -> CoolingChoice:
    technology = min(frozen_technologies(), key=lambda row: (row.water_per_task, row.name))
    return evaluate(technology, policy="WATER_ONLY")


def choose_joint_viability() -> CoolingChoice:
    candidates = [evaluate(row, policy="JOINT_VIABILITY") for row in frozen_technologies()]
    viable = [row for row in candidates if row.jointly_viable]
    if not viable:
        raise ValueError("no jointly viable technology")
    return min(
        viable,
        key=lambda row: (
            row.total_energy / 100.0 + row.total_water / 30.0,
            row.technology.name,
        ),
    )


def frozen_resource_substitution() -> dict[str, CoolingChoice]:
    return {
        "energy_only": choose_energy_only(),
        "water_only": choose_water_only(),
        "joint": choose_joint_viability(),
    }
