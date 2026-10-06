import pytest

from market_microcosm.dcre003_uncertain_option import evaluate_prior, prior_grid


def test_exploration_knee_is_one_half_in_frozen_world() -> None:
    assert evaluate_prior(0.25).best_no_oracle_policy == "SAFE"
    assert evaluate_prior(0.5).best_no_oracle_policy == "TIE"
    assert evaluate_prior(0.75).best_no_oracle_policy == "EXPLORE"


def test_frozen_values() -> None:
    low = evaluate_prior(0.25)
    mid = evaluate_prior(0.5)
    high = evaluate_prior(0.75)

    assert low.safe_value == pytest.approx(8.0)
    assert low.explore_value == pytest.approx(6.0)
    assert mid.safe_value == pytest.approx(8.0)
    assert mid.explore_value == pytest.approx(8.0)
    assert high.explore_value == pytest.approx(10.0)
    assert high.oracle_value == pytest.approx(14.0)


def test_exploration_has_both_over_and_under_use_failure_modes() -> None:
    low = evaluate_prior(0.25)
    high = evaluate_prior(0.75)
    assert low.explore_value < low.safe_value
    assert high.explore_value > high.safe_value


def test_oracle_advantage_never_disappears_when_information_matters() -> None:
    for outcome in prior_grid()[1:]:
        assert outcome.oracle_value >= outcome.best_no_oracle_value
        assert outcome.oracle_regret >= 0.0


def test_invalid_prior_fails_closed() -> None:
    with pytest.raises(ValueError):
        evaluate_prior(-0.1)
    with pytest.raises(ValueError):
        evaluate_prior(1.1)
