from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class ReuseCost:
    strategy: str
    uses: int
    preparation_compute: float
    per_use_network: float
    per_use_compute: float
    total_network: float
    total_compute: float
    composite_cost: float


def evaluate_reuse(
    uses: int,
    *,
    strategy: str,
    preparation_compute: float,
    per_use_network: float,
    per_use_compute: float,
    network_weight: float = 1.0,
    compute_weight: float = 1.0,
) -> ReuseCost:
    if uses < 1:
        raise ValueError("uses must be positive")
    if min(
        preparation_compute,
        per_use_network,
        per_use_compute,
        network_weight,
        compute_weight,
    ) < 0.0:
        raise ValueError("costs and weights must be non-negative")
    network = uses * per_use_network
    compute = preparation_compute + uses * per_use_compute
    return ReuseCost(
        strategy=strategy,
        uses=uses,
        preparation_compute=preparation_compute,
        per_use_network=per_use_network,
        per_use_compute=per_use_compute,
        total_network=network,
        total_compute=compute,
        composite_cost=network_weight * network + compute_weight * compute,
    )


def raw_strategy(uses: int) -> ReuseCost:
    return evaluate_reuse(
        uses,
        strategy="RAW_PER_USE",
        preparation_compute=0.0,
        per_use_network=25.0,
        per_use_compute=0.0,
    )


def prepared_compact_strategy(uses: int) -> ReuseCost:
    return evaluate_reuse(
        uses,
        strategy="PREPARED_COMPACT_REUSE",
        preparation_compute=30.0,
        per_use_network=10.0,
        per_use_compute=2.0,
    )


def continuous_break_even_uses() -> float:
    raw_marginal = raw_strategy(1).composite_cost
    compact_one = prepared_compact_strategy(1)
    compact_marginal = compact_one.per_use_network + compact_one.per_use_compute
    if raw_marginal <= compact_marginal:
        raise ValueError("prepared strategy never amortizes")
    return compact_one.preparation_compute / (raw_marginal - compact_marginal)


def integer_break_even_uses() -> int:
    return math.ceil(continuous_break_even_uses())


def frozen_reuse_sweep() -> dict[int, dict[str, ReuseCost]]:
    return {
        uses: {
            "raw": raw_strategy(uses),
            "prepared": prepared_compact_strategy(uses),
        }
        for uses in (1, 2, 3, 4, 8)
    }
