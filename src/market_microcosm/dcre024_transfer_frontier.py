from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TransferMode:
    name: str
    network_per_remote_task: float
    encode_compute_per_remote_task: float
    semantic_fidelity: float

    def __post_init__(self) -> None:
        if min(self.network_per_remote_task, self.encode_compute_per_remote_task) < 0.0:
            raise ValueError("resource costs must be non-negative")
        if not 0.0 <= self.semantic_fidelity <= 1.0:
            raise ValueError("semantic_fidelity must be within [0, 1]")


@dataclass(frozen=True)
class TransferOutcome:
    mode: TransferMode
    remote_tasks: float
    total_network: float
    total_encode_compute: float
    preserved_semantic_tasks: float
    network_viable: bool
    compute_viable: bool
    semantic_viable: bool

    @property
    def jointly_viable(self) -> bool:
        return self.network_viable and self.compute_viable and self.semantic_viable


def frozen_modes() -> tuple[TransferMode, ...]:
    return (
        TransferMode("RAW", 0.50, 0.00, 1.00),
        TransferMode("COMPACT_BALANCED", 0.30, 0.20, 0.95),
        TransferMode("OVERCOMPRESSED", 0.15, 0.40, 0.80),
        TransferMode("HEAVY_LOSSLESS", 0.25, 0.50, 1.00),
    )


def evaluate_mode(
    mode: TransferMode,
    *,
    remote_tasks: float = 50.0,
    network_ceiling: float = 20.0,
    encode_compute_ceiling: float = 20.0,
    semantic_floor: float = 45.0,
) -> TransferOutcome:
    if min(remote_tasks, network_ceiling, encode_compute_ceiling, semantic_floor) < 0.0:
        raise ValueError("constraints must be non-negative")
    network = remote_tasks * mode.network_per_remote_task
    compute = remote_tasks * mode.encode_compute_per_remote_task
    semantic = remote_tasks * mode.semantic_fidelity
    return TransferOutcome(
        mode=mode,
        remote_tasks=remote_tasks,
        total_network=network,
        total_encode_compute=compute,
        preserved_semantic_tasks=semantic,
        network_viable=network <= network_ceiling,
        compute_viable=compute <= encode_compute_ceiling,
        semantic_viable=semantic >= semantic_floor,
    )


def frozen_transfer_frontier() -> dict[str, TransferOutcome]:
    return {mode.name: evaluate_mode(mode) for mode in frozen_modes()}


def jointly_viable_modes() -> tuple[str, ...]:
    return tuple(
        name
        for name, outcome in frozen_transfer_frontier().items()
        if outcome.jointly_viable
    )
