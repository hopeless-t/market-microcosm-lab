import pytest

from market_microcosm.dcre037_reserve_domains import frozen_reserve_domains


def test_concentrated_reserve_can_fail_on_one_domain_outage() -> None:
    report = frozen_reserve_domains()
    assert report["concentrated"].domain_count == 2
    assert report["concentrated_min_domains_to_break"] == 1
    assert report["concentrated_loss_probability"] == pytest.approx(0.10)


def test_independent_reserve_requires_two_domain_outages() -> None:
    report = frozen_reserve_domains()
    assert report["independent"].domain_count == 3
    assert report["independent_min_domains_to_break"] == 2
    assert report["independent_loss_probability"] == pytest.approx(0.028)


def test_nominal_three_modules_do_not_imply_three_independent_domains() -> None:
    report = frozen_reserve_domains()
    assert report["concentrated"].witness_count == 3
    assert report["independent"].witness_count == 3
    assert report["concentrated"].domain_count < report["independent"].domain_count
