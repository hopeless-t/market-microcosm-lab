from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre008_dynamic_wait import evaluate_wait


@dataclass(frozen=True)
class QueueAllocation:
    actor_count: int
    waiter_count: int
    act_now_count: int
    total_cost: float
    per_waiter_cost: float
    base_wait_cost: float
    act_now_cost: float


def evaluate_queue_allocation(
    waiter_count: int,
    *,
    actor_count: int = 4,
    failure_loss: float = 200.0,
    congestion_penalty_per_other_waiter: float = 0.05,
) -> QueueAllocation:
    if actor_count < 1:
        raise ValueError("actor_count must be positive")
    if not 0 <= waiter_count <= actor_count:
        raise ValueError("waiter_count must be within [0, actor_count]")
    if congestion_penalty_per_other_waiter < 0.0:
        raise ValueError("congestion penalty must be non-negative")

    base = evaluate_wait(failure_loss)
    per_waiter_cost = base.wait_cost + congestion_penalty_per_other_waiter * max(
        0, waiter_count - 1
    )
    act_now_count = actor_count - waiter_count
    total_cost = waiter_count * per_waiter_cost + act_now_count * base.act_now_cost
    return QueueAllocation(
        actor_count=actor_count,
        waiter_count=waiter_count,
        act_now_count=act_now_count,
        total_cost=total_cost,
        per_waiter_cost=per_waiter_cost,
        base_wait_cost=base.wait_cost,
        act_now_cost=base.act_now_cost,
    )


def exact_queue_optimum(
    *,
    actor_count: int = 4,
    failure_loss: float = 200.0,
    congestion_penalty_per_other_waiter: float = 0.05,
) -> QueueAllocation:
    candidates = tuple(
        evaluate_queue_allocation(
            waiter_count,
            actor_count=actor_count,
            failure_loss=failure_loss,
            congestion_penalty_per_other_waiter=congestion_penalty_per_other_waiter,
        )
        for waiter_count in range(actor_count + 1)
    )
    return min(candidates, key=lambda row: (row.total_cost, row.waiter_count))
