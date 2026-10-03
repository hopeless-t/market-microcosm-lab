import pytest

from market_microcosm.ecology import MarketWorld, default_mechanisms
from market_microcosm.robust_search import (
    EvaluationDesign,
    evaluate_robust_mechanism,
    run_evaluation_design_meta,
)


def test_robust_score_is_bounded() -> None:
    score = evaluate_robust_mechanism(
        base_world=MarketWorld(),
        mechanism=default_mechanisms()[0],
        pressure_levels=(0, 1),
        seeds=(1, 2, 3),
        horizon=6,
    )
    assert 0.0 <= score.minimum_survival_rate <= 1.0
    assert 0.0 <= score.mean_survival_rate <= 1.0
    assert score.mean_survival_months <= 6


def test_evaluation_meta_rejects_seed_leakage() -> None:
    designs = (
        EvaluationDesign(
            "x",
            pressure_levels=(0,),
            discovery_seeds=(1, 2),
            horizon=4,
        ),
    )
    with pytest.raises(ValueError):
        run_evaluation_design_meta(
            designs=designs,
            meta_pressure_levels=(0,),
            meta_seeds=(2, 3),
            meta_horizon=4,
        )


def test_evaluation_meta_returns_declared_winner() -> None:
    designs = (
        EvaluationDesign(
            "neutral",
            pressure_levels=(0,),
            discovery_seeds=(10, 11),
            horizon=5,
        ),
        EvaluationDesign(
            "stress",
            pressure_levels=(0, 1),
            discovery_seeds=(20, 21),
            horizon=5,
        ),
    )
    result = run_evaluation_design_meta(
        mechanisms=default_mechanisms()[:2],
        designs=designs,
        meta_pressure_levels=(0, 1),
        meta_seeds=(30, 31, 32),
        meta_horizon=6,
    )
    assert result.winner_design in {"neutral", "stress"}
    assert result.winner_mechanism in {m.name for m in default_mechanisms()[:2]}
