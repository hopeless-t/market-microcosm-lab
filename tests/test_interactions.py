from market_microcosm.ecology import MarketWorld, default_mechanisms
from market_microcosm.interactions import (
    interaction_grid,
    scan_interaction_pair,
    world_at_interaction,
)


def test_interaction_grid_has_expected_size() -> None:
    points = interaction_grid(
        "subscription_price_multiplier",
        "platform_cost_multiplier",
        max_level=2,
    )
    assert len(points) == 9
    assert {(p.level_a, p.level_b) for p in points} == {
        (a, b) for a in range(3) for b in range(3)
    }


def test_world_at_interaction_changes_only_declared_axes() -> None:
    base = MarketWorld()
    point = interaction_grid(
        "subscription_price_multiplier",
        "platform_cost_multiplier",
        max_level=1,
    )[-1]
    world = world_at_interaction(base, point)
    assert world.subscription_price != base.subscription_price
    assert world.platform_monthly_cost != base.platform_monthly_cost
    assert world.base_churn_rate == base.base_churn_rate


def test_small_interaction_scan_is_well_formed() -> None:
    results = scan_interaction_pair(
        base_world=MarketWorld(),
        mechanisms=default_mechanisms()[:2],
        axis_a="subscription_price_multiplier",
        axis_b="base_churn_rate",
        max_level=1,
        seeds=(1, 2, 3),
        horizon=6,
    )
    assert len(results) == 2 * 4
    assert all(0.0 <= row.evaluation.survival_rate <= 1.0 for row in results)
    assert all(row.evaluation.invariant_violations == 0 for row in results)
