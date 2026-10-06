import pytest

from market_microcosm.dcre008_dynamic_wait import evaluate_wait


def test_low_loss_prefers_action_now() -> None:
    assert evaluate_wait(100.0).decision == "ACT_NOW"


def test_intermediate_loss_prefers_waiting_for_information() -> None:
    assert evaluate_wait(200.0).decision == "WAIT"
    assert evaluate_wait(20_000.0).decision == "WAIT"


def test_extreme_loss_prefers_abandonment() -> None:
    result = evaluate_wait(30_000.0)
    assert result.decision == "ABANDON"
    assert result.abandon_cost < result.wait_cost
    assert result.abandon_cost < result.act_now_cost


def test_dynamic_wait_creates_three_regimes() -> None:
    decisions = {
        evaluate_wait(loss).decision
        for loss in (100.0, 200.0, 30_000.0)
    }
    assert decisions == {"ACT_NOW", "WAIT", "ABANDON"}


def test_invalid_information_probability_fails_closed() -> None:
    with pytest.raises(ValueError):
        evaluate_wait(100.0, information_arrival_probability=1.1)
