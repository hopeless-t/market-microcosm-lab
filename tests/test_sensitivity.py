from market_microcosm.ecology import MarketWorld, default_mechanisms
from market_microcosm.sensitivity import (
    SUPPORTED_AXES,
    axis_knee,
    axis_ladder,
    scan_axis,
    world_at_axis,
)


def test_axis_ladders_change_only_declared_parameter() -> None:
    base = MarketWorld()

    price = world_at_axis(base, axis_ladder("subscription_price_multiplier", 1)[1])
    assert price.subscription_price != base.subscription_price
    assert price.platform_monthly_cost == base.platform_monthly_cost
    assert price.base_churn_rate == base.base_churn_rate

    cost = world_at_axis(base, axis_ladder("platform_cost_multiplier", 1)[1])
    assert cost.subscription_price == base.subscription_price
    assert cost.platform_monthly_cost != base.platform_monthly_cost
    assert cost.base_churn_rate == base.base_churn_rate

    churn = world_at_axis(base, axis_ladder("base_churn_rate", 1)[1])
    assert churn.subscription_price == base.subscription_price
    assert churn.platform_monthly_cost == base.platform_monthly_cost
    assert churn.base_churn_rate != base.base_churn_rate


def test_small_axis_scans_are_well_formed() -> None:
    mechanisms = default_mechanisms()[:2]
    for axis in SUPPORTED_AXES:
        points = axis_ladder(axis, 2)
        results = scan_axis(
            base_world=MarketWorld(),
            mechanisms=mechanisms,
            axis=axis,
            points=points,
            seeds=(1, 2, 3),
            horizon=6,
        )
        assert len(results) == len(mechanisms) * len(points)
        assert all(0.0 <= row.evaluation.survival_rate <= 1.0 for row in results)
        assert all(row.evaluation.invariant_violations == 0 for row in results)


def test_axis_knee_is_none_or_declared_level() -> None:
    mechanism = default_mechanisms()[0]
    points = axis_ladder("base_churn_rate", 2)
    results = scan_axis(
        base_world=MarketWorld(),
        mechanisms=(mechanism,),
        axis="base_churn_rate",
        points=points,
        seeds=(4, 5, 6),
        horizon=6,
    )
    knee = axis_knee(results, mechanism.name, "base_churn_rate")
    assert knee is None or knee in {0, 1, 2}
