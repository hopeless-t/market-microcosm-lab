import pytest

from market_microcosm.dcre025_reuse_knee import (
    continuous_break_even_uses,
    frozen_reuse_sweep,
    integer_break_even_uses,
)


def test_continuous_reuse_knee_is_between_two_and_three_uses() -> None:
    assert continuous_break_even_uses() == pytest.approx(30.0 / 13.0)
    assert integer_break_even_uses() == 3


def test_raw_is_cheaper_for_one_and_two_uses() -> None:
    sweep = frozen_reuse_sweep()
    for uses in (1, 2):
        assert sweep[uses]["raw"].composite_cost < sweep[uses]["prepared"].composite_cost


def test_prepared_compact_wins_from_third_use_on_frozen_surface() -> None:
    sweep = frozen_reuse_sweep()
    assert sweep[3]["raw"].composite_cost == pytest.approx(75.0)
    assert sweep[3]["prepared"].composite_cost == pytest.approx(66.0)
    for uses in (3, 4, 8):
        assert sweep[uses]["prepared"].composite_cost < sweep[uses]["raw"].composite_cost


def test_reuse_changes_cost_ranking_without_changing_per_use_payload_contract() -> None:
    sweep = frozen_reuse_sweep()
    one = sweep[1]["prepared"]
    eight = sweep[8]["prepared"]
    assert one.per_use_network == eight.per_use_network == 10.0
    assert one.per_use_compute == eight.per_use_compute == 2.0
    assert one.preparation_compute == eight.preparation_compute == 30.0
