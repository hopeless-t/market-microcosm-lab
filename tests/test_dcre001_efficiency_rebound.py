import pytest

from market_microcosm.dcre001_efficiency_rebound import (
    evaluate_cell,
    exact_grid,
    grid_summary,
)


def test_full_capacity_elasticity_knee() -> None:
    for efficiency in (0.8, 0.6, 0.4):
        assert evaluate_cell(efficiency, 0.5, 1.0).rebound_class == "CONSERVATION"
        assert evaluate_cell(efficiency, 1.0, 1.0).rebound_class == "FULL_REBOUND"
        assert evaluate_cell(efficiency, 1.5, 1.0).rebound_class == "BACKFIRE"


def test_exact_grid_contract() -> None:
    summary = grid_summary(exact_grid())
    assert summary["cell_count"] == 60
    assert summary["conservation_cells"] == 33
    assert summary["full_rebound_cells"] == 18
    assert summary["backfire_cells"] == 9
    assert summary["verification_starved_cells"] == 19


def test_verified_gate_preserves_verified_output_on_frozen_grid() -> None:
    summary = grid_summary(exact_grid())
    assert summary["aggregate_verified_gate"] == pytest.approx(
        summary["aggregate_verified_open"]
    )
    assert summary["aggregate_resource_verified_gate"] < summary["aggregate_resource_open"]
    assert summary["verified_gate_resource_reduction_fraction"] == pytest.approx(
        0.16248803098944806
    )


def test_backfire_cells_are_not_misreported_as_efficiency_success() -> None:
    cells = [cell for cell in exact_grid() if cell.rebound_class == "BACKFIRE"]
    assert cells
    assert all(cell.resource_open > 100.0 for cell in cells)
    assert all(cell.verification_starved for cell in cells)


def test_invalid_parameters_fail_closed() -> None:
    with pytest.raises(ValueError):
        evaluate_cell(0.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        evaluate_cell(0.8, -0.1, 1.0)
    with pytest.raises(ValueError):
        evaluate_cell(0.8, 1.0, 1.1)
