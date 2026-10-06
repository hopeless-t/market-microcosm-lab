import pytest

from market_microcosm.dcre036_reserve_quality import frozen_procurement_quality


def test_nameplate_cheapest_buys_flaky_big_bid() -> None:
    report = frozen_procurement_quality()
    assert tuple(bid.name for bid in report["nameplate"]) == ("FLAKY_BIG",)
    assert report["nameplate_usable"] == pytest.approx(8.0)
    assert report["nameplate_cost"] == pytest.approx(3.4)


def test_reliability_aware_exact_prefers_two_reliable_bids() -> None:
    report = frozen_procurement_quality()
    assert tuple(bid.name for bid in report["exact"]) == ("RELIABLE_A", "RELIABLE_B")
    assert report["exact_usable"] == pytest.approx(20.0)
    assert report["exact_cost"] == pytest.approx(2.0)


def test_nominal_capacity_is_not_usable_resilience() -> None:
    report = frozen_procurement_quality()
    assert sum(bid.nominal_units for bid in report["nameplate"]) == pytest.approx(20.0)
    assert report["nameplate_usable"] < 20.0
    assert report["exact_cost"] < report["nameplate_cost"]
