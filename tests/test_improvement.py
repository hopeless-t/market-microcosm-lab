import pytest

from market_microcosm.improvement import (
    ImprovementConfig,
    run_closed_improvement_loop,
    run_improvement_loop,
)
from market_microcosm.meta_improvement import (
    run_closed_meta_loop,
    run_meta_improvement_loop,
)
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
    assert result.discovery_manifest.run_id != result.promotion_manifest.run_id


def test_closed_inner_loop_reaches_a_fixed_point() -> None:
    result = run_closed_improvement_loop(
        world=ToyWorld(),
        incumbent=PolicySpec("incumbent", correction_threshold=99),
        config=ImprovementConfig(),
        max_generations=4,
    )
    assert result.generations
    assert result.converged
    assert result.final_policy.name != "incumbent"


def test_meta_loop_rejects_seed_leakage() -> None:
    with pytest.raises(ValueError):
        run_meta_improvement_loop(
            world=ToyWorld(),
            incumbent=PolicySpec("incumbent", correction_threshold=99),
            meta_seeds=(0, 1, 2),
        )


def test_meta_loop_selects_on_separate_meta_holdout() -> None:
    result = run_meta_improvement_loop(
        world=ToyWorld(),
        incumbent=PolicySpec("incumbent", correction_threshold=99),
    )
    assert result.winner.name in {s.candidate_name for s in result.scores}
    assert len(result.scores) == 3
    assert all(x.startswith("seed-10") for x in result.meta_scenario_ids)


def test_closed_meta_loop_runs_multiple_generations() -> None:
    result = run_closed_meta_loop(
        world=ToyWorld(),
        incumbent=PolicySpec("incumbent", correction_threshold=1),
        max_generations=3,
    )
    assert result.generations
    assert 1 <= len(result.generations) <= 3
    assert result.final_winner.name
