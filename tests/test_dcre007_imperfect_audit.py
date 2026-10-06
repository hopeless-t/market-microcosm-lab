import pytest

from market_microcosm.dcre007_imperfect_audit import evaluate_imperfect_audit


def test_low_loss_prefers_unaudited() -> None:
    assert evaluate_imperfect_audit(100.0).decision == "UNAUDITED"


def test_midrange_loss_prefers_audit() -> None:
    assert evaluate_imperfect_audit(200.0).decision == "AUDIT"
    assert evaluate_imperfect_audit(8_000.0).decision == "AUDIT"


def test_extreme_loss_prefers_abstention() -> None:
    result = evaluate_imperfect_audit(10_000.0)
    assert result.decision == "ABSTAIN"
    assert result.abstain_cost < result.audit_cost
    assert result.abstain_cost < result.unaudited_cost


def test_imperfect_audit_creates_three_policy_regimes() -> None:
    decisions = {
        evaluate_imperfect_audit(loss).decision
        for loss in (100.0, 200.0, 10_000.0)
    }
    assert decisions == {"UNAUDITED", "AUDIT", "ABSTAIN"}


def test_invalid_probabilities_fail_closed() -> None:
    with pytest.raises(ValueError):
        evaluate_imperfect_audit(100.0, sensitivity=1.1)
