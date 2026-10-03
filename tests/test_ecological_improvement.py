import pytest

from market_microcosm.ecological_evaluation import evaluate_mechanism
from market_microcosm.ecological_improvement import (
    MarketImprovementConfig,
    run_closed_market_improvement,
    run_market_meta_improvement,
)
from market_microcosm.ecology import MarketWorld, default_mechanisms


def test_market_evaluation_reports_bounded_survival_statistics() -> None:
    result = evaluate_mechanism(
        MarketWorld(),
        default_mechanisms()[0],
        seeds=tuple(range(10)),
        horizon=12,
    )
    assert 0.0 <= result.survival_rate <= 1.0
    assert 0.0 <= result.survival_lcb95 <= result.survival_rate
    assert result.invariant_violations == 0


def test_market_seed_splits_fail_closed() -> None:
    with pytest.raises(ValueError):
        MarketImprovementConfig(
            discovery_seeds=(1, 2),
            promotion_seeds=(2, 3),
        )


def test_closed_market_improvement_executes() -> None:
    mechanisms = default_mechanisms()
    result = run_closed_market_improvement(
        world=MarketWorld(),
        incumbent=mechanisms[0],
        config=MarketImprovementConfig(
            discovery_seeds=tuple(range(6)),
            promotion_seeds=tuple(range(100, 112)),
            horizon=18,
            mechanisms=mechanisms[:4],
        ),
        max_generations=3,
    )
    assert result.generations
    assert result.final.name in {m.name for m in mechanisms[:4]}


def test_market_meta_holdout_is_isolated() -> None:
    with pytest.raises(ValueError):
        run_market_meta_improvement(
            world=MarketWorld(),
            incumbent=default_mechanisms()[0],
            meta_seeds=(2000, 4000),
        )
