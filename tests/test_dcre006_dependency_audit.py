import pytest

from market_microcosm.dcre006_dependency_audit import audit_knee, evaluate_audit


def test_hidden_common_mode_audit_knee_is_near_100() -> None:
    assert audit_knee() == pytest.approx(100.00098506970352)


def test_low_failure_loss_does_not_justify_audit_in_frozen_model() -> None:
    result = evaluate_audit(50.0)
    assert result.decision == "UNAUDITED"
    assert result.unaudited_expected_cost < result.audited_expected_cost


def test_high_failure_loss_justifies_audit_in_frozen_model() -> None:
    result = evaluate_audit(200.0)
    assert result.decision == "AUDIT"
    assert result.audited_expected_cost < result.unaudited_expected_cost


def test_knee_flips_between_100_and_101() -> None:
    assert evaluate_audit(100.0).decision == "UNAUDITED"
    assert evaluate_audit(101.0).decision == "AUDIT"


def test_invalid_costs_fail_closed() -> None:
    with pytest.raises(ValueError):
        audit_knee(audit_cost=-1.0)
    with pytest.raises(ValueError):
        evaluate_audit(-1.0)
