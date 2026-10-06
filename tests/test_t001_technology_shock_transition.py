import pytest

from market_microcosm.t001_technology_shock_transition import t001_report


def test_same_shock_collapses_legacy_occupation_and_expands_output() -> None:
    report = t001_report()
    baseline = report["baseline"]
    fast = report["fast_reallocation"]
    frictional = report["frictional_transition"]

    assert report["same_technology_shock"] is True
    assert fast.legacy_workers_after == 12
    assert frictional.legacy_workers_after == 12
    assert fast.legacy_headcount_reduction == pytest.approx(0.80)
    assert frictional.legacy_headcount_reduction == pytest.approx(0.80)
    assert fast.output == pytest.approx(178.0)
    assert frictional.output == pytest.approx(150.0)
    assert fast.output > baseline.output
    assert frictional.output > baseline.output
    assert report["legacy_occupation_collapses_in_both"] is True
    assert report["aggregate_expansion_in_both_shock_worlds"] is True


def test_transition_capacity_changes_human_viability_without_changing_shock() -> None:
    report = t001_report()
    fast = report["fast_reallocation"]
    frictional = report["frictional_transition"]

    assert fast.transitioned_workers == 48
    assert fast.unemployed_workers == 0
    assert fast.employment_rate == pytest.approx(1.0)
    assert fast.household_income == pytest.approx(100.0)
    assert fast.viable is True

    assert frictional.transitioned_workers == 20
    assert frictional.unemployed_workers == 28
    assert frictional.employment_rate == pytest.approx(0.72)
    assert frictional.household_income == pytest.approx(72.0)
    assert frictional.viable is False
    assert report["human_viability_diverges"] is True


def test_t001_does_not_upgrade_real_world_authority() -> None:
    assert t001_report()["authority_effect"] == "NONE"
