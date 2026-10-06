import pytest

from market_microcosm.dcre004_belief_herding import (
    diversified_allocation,
    frozen_opportunities,
    herd_allocation,
    shared_observation_allocation,
)


def test_herding_duplicates_perfect_information_acquisition() -> None:
    report = herd_allocation(frozen_opportunities())
    assert report.assignments == ("A", "A", "A", "A")
    assert report.probe_count == 4
    assert report.unique_opportunities == 1
    assert report.duplicate_probes == 3
    assert report.expected_discovery_value == pytest.approx(8.0)
    assert report.expected_value_per_probe == pytest.approx(2.0)


def test_diversification_uses_same_probe_budget_for_more_expected_discovery() -> None:
    report = diversified_allocation(frozen_opportunities())
    assert report.assignments == ("A", "B", "C", "D")
    assert report.probe_count == 4
    assert report.unique_opportunities == 4
    assert report.duplicate_probes == 0
    assert report.expected_discovery_value == pytest.approx(26.5)
    assert report.expected_value_per_probe == pytest.approx(6.625)


def test_shared_observation_dominates_redundant_herding_on_same_target() -> None:
    herd = herd_allocation(frozen_opportunities())
    shared = shared_observation_allocation(frozen_opportunities())
    assert shared.expected_discovery_value == pytest.approx(herd.expected_discovery_value)
    assert shared.probe_count == 1
    assert herd.probe_count == 4
    assert shared.expected_value_per_probe > herd.expected_value_per_probe


def test_diversification_beats_herding_only_under_frozen_perfect_probe_contract() -> None:
    herd = herd_allocation(frozen_opportunities())
    diverse = diversified_allocation(frozen_opportunities())
    assert diverse.expected_discovery_value > herd.expected_discovery_value
    assert diverse.duplicate_probes < herd.duplicate_probes
