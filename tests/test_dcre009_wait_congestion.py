import pytest

from market_microcosm.dcre009_wait_congestion import (
    evaluate_queue_allocation,
    exact_queue_optimum,
)


def test_wait_is_individually_better_before_congestion() -> None:
    one_waiter = evaluate_queue_allocation(1)
    assert one_waiter.base_wait_cost < one_waiter.act_now_cost


def test_all_waiting_is_collectively_worse_than_all_acting() -> None:
    all_act = evaluate_queue_allocation(0)
    all_wait = evaluate_queue_allocation(4)
    assert all_wait.total_cost > all_act.total_cost
    assert all_wait.per_waiter_cost > all_wait.act_now_cost


def test_exact_queue_optimum_uses_one_waiter() -> None:
    optimum = exact_queue_optimum()
    assert optimum.waiter_count == 1
    assert optimum.total_cost == pytest.approx(3.3353771307959996)


def test_queue_externality_breaks_independent_best_response() -> None:
    one_waiter = evaluate_queue_allocation(1)
    four_waiters = evaluate_queue_allocation(4)
    assert one_waiter.base_wait_cost < one_waiter.act_now_cost
    assert four_waiters.total_cost > evaluate_queue_allocation(0).total_cost


def test_invalid_waiter_count_fails_closed() -> None:
    with pytest.raises(ValueError):
        evaluate_queue_allocation(5)
