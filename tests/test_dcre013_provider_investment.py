import pytest

from market_microcosm.dcre013_provider_investment import frozen_provider_choices


def test_fixed_resource_price_allows_backfire_capacity_race() -> None:
    choices = frozen_provider_choices()
    fixed = choices["fixed_volume"]
    assert fixed.capacity == 220.0
    assert fixed.resource_used == pytest.approx(129.09944487358055)
    assert fixed.resource_used > 100.0
    assert fixed.verified_output == 120.0


def test_scarcity_price_suppresses_but_does_not_eliminate_overbuild() -> None:
    choices = frozen_provider_choices()
    scarce = choices["scarcity_volume"]
    assert scarce.capacity == 160.0
    assert scarce.resource_used == pytest.approx(96.0)
    assert scarce.verified_output == 120.0
    assert scarce.capacity > scarce.verified_output


def test_verified_revenue_aligns_capacity_with_other_scarcity() -> None:
    choices = frozen_provider_choices()
    verified = choices["scarcity_verified"]
    assert verified.capacity == 120.0
    assert verified.resource_used == pytest.approx(72.0)
    assert verified.verified_output == pytest.approx(120.0)


def test_dynamic_price_alone_is_not_full_alignment() -> None:
    choices = frozen_provider_choices()
    fixed = choices["fixed_volume"]
    scarce = choices["scarcity_volume"]
    verified = choices["scarcity_verified"]
    assert fixed.resource_used > scarce.resource_used > verified.resource_used
    assert scarce.verified_output == verified.verified_output == 120.0
