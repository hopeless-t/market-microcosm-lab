from market_microcosm.ecology import MarketWorld, default_mechanisms
from market_microcosm.pressure import (
    pressure_knee,
    pressure_ladder,
    scan_pressure,
    world_at_pressure,
)


def test_pressure_ladder_increases_declared_stress() -> None:
    base = MarketWorld()
    points = pressure_ladder(3)
    worlds = [world_at_pressure(base, point) for point in points]
    assert worlds[0].subscription_price > worlds[-1].subscription_price
    assert worlds[0].platform_monthly_cost < worlds[-1].platform_monthly_cost
    assert worlds[0].base_churn_rate < worlds[-1].base_churn_rate


def test_small_pressure_scan_is_well_formed() -> None:
    mechanisms = default_mechanisms()[:2]
    points = pressure_ladder(2)
    results = scan_pressure(
        base_world=MarketWorld(),
        mechanisms=mechanisms,
        points=points,
        seeds=(1, 2, 3),
        horizon=6,
    )
    assert len(results) == len(mechanisms) * len(points)
    assert all(0.0 <= x.evaluation.survival_rate <= 1.0 for x in results)
    assert all(x.evaluation.invariant_violations == 0 for x in results)


def test_knee_returns_none_or_declared_level() -> None:
    mechanisms = default_mechanisms()[:1]
    points = pressure_ladder(2)
    results = scan_pressure(
        base_world=MarketWorld(),
        mechanisms=mechanisms,
        points=points,
        seeds=(4, 5, 6),
        horizon=6,
    )
    knee = pressure_knee(results, mechanisms[0].name)
    assert knee is None or knee in {0, 1, 2}
