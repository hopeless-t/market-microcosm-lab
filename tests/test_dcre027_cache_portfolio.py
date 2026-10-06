import pytest

from market_microcosm.dcre027_cache_portfolio import frozen_cache_portfolio


def test_frequency_greedy_spends_budget_on_hot_big_object() -> None:
    report = frozen_cache_portfolio()
    assert report["frequency_greedy_names"] == ("HOT_BIG",)
    assert report["frequency_greedy_relief"] == pytest.approx(6.0)


def test_e018_dp_reuse_matches_exact_cache_portfolio_oracle() -> None:
    report = frozen_cache_portfolio()
    assert report["dp_matches_oracle"] is True
    assert report["oracle"].selected_names == ("WARM_A", "WARM_B")
    assert report["dp"].selected_names == ("WARM_A", "WARM_B")
    assert report["dp"].total_cost_units == 10
    assert report["dp"].total_restoration_value == 26


def test_frequency_is_not_resident_value_in_frozen_world() -> None:
    report = frozen_cache_portfolio()
    assert report["dp"].total_restoration_value > report["frequency_greedy_relief"]
