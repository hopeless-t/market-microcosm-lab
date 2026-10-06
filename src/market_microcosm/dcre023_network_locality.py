from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre022_spatial_resources import evaluate_allocation


@dataclass(frozen=True)
class NetworkAwareAllocation:
    policy: str
    grid_rich_tasks: float
    remote_tasks: float
    network_per_remote_task: float
    total_network: float
    resource_viable: bool
    network_viable: bool

    @property
    def jointly_viable(self) -> bool:
        return self.resource_viable and self.network_viable


def evaluate_network_allocation(
    grid_rich_tasks: float,
    *,
    policy: str,
    network_per_remote_task: float,
    network_ceiling: float = 20.0,
) -> NetworkAwareAllocation:
    resource = evaluate_allocation(grid_rich_tasks, policy=policy)
    remote = resource.water_rich_tasks
    network = remote * network_per_remote_task
    return NetworkAwareAllocation(
        policy=policy,
        grid_rich_tasks=grid_rich_tasks,
        remote_tasks=remote,
        network_per_remote_task=network_per_remote_task,
        total_network=network,
        resource_viable=resource.jointly_viable,
        network_viable=network <= network_ceiling,
    )


def exact_network_grid(
    *,
    network_per_remote_task: float,
    policy: str,
) -> NetworkAwareAllocation | None:
    candidates = tuple(
        evaluate_network_allocation(
            value,
            policy=policy,
            network_per_remote_task=network_per_remote_task,
        )
        for value in (0.0, 25.0, 50.0, 75.0, 100.0)
    )
    viable = tuple(row for row in candidates if row.jointly_viable)
    if not viable:
        return None
    return min(viable, key=lambda row: (row.total_network, -row.grid_rich_tasks))


def frozen_network_locality() -> dict[str, NetworkAwareAllocation | None]:
    resource_only_projection = evaluate_network_allocation(
        50.0,
        policy="RESOURCE_ONLY_PROJECTION",
        network_per_remote_task=0.50,
    )
    return {
        "resource_only_projection": resource_only_projection,
        "raw_network_exact": exact_network_grid(
            network_per_remote_task=0.50,
            policy="RAW_TRANSFER_EXACT",
        ),
        "compact_network_exact": exact_network_grid(
            network_per_remote_task=0.30,
            policy="COMPACT_TRANSFER_EXACT",
        ),
    }
