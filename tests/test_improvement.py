import pytest

from market_microcosm.improvement import ImprovementConfig, run_improvement_loop
from market_microcosm.meta_improvement import run_meta_improvement_loop
from market_microcosm.policies import PolicySpec
from market_microcosm.toy_world import ToyWorld


def test_inner_loop_rejects_leaky_seed_split() -> None:
    with pytest.raises(ValueError):
        ImprovementConfig(
            discovery_seeds=(1, 2, 3),
            promotion_seeds=(3, 4, 5),
            horizon=5,
        )


def test_inner_loop_runs_with_independent_holdout() -> None:
    world = ToyWorld()
    incumbent = PolicySpec("incumbent", correction_threshold=99)
    result = run_improvement_loop(
        world=world,
        incumbent=incumbent,
        config=ImprovementConfig(
            discovery_seeds=tuple(range(6)),
            promotion_seeds=tuple(range(100, 112)),
            horizon=8,
        ),
    )
    assert result.discovery_scores
    assert result.incumbent_holdout.scenarios == 12
    assert result.challenger_holdout.scenarios == 12
    assert result.viability.kernel


def test_meta_loop_selects_a_declared_candidate() -> None:
    result = run_meta_improvement_loop(
        world=ToyWorld(),
        incumbent=PolicySpec("incumbent", correction_threshold=99),
    )
    assert result.winner.name in {s.candidate_name for s in result.scores}
    assert len(result.scores) == 3
