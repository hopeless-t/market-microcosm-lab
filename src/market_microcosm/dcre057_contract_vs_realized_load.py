from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContractObservability:
    minimum_purchase_commitment_exists: bool
    minimum_purchase_commitment_mw: float | None
    take_or_pay_exists: bool
    continuous_delivery_hours_per_year: int
    customer_interval_meter_series_observed: bool
    realized_load_factor: float | None


def nwcpud_large_load_contract_surface() -> ContractObservability:
    return ContractObservability(
        minimum_purchase_commitment_exists=True,
        minimum_purchase_commitment_mw=None,
        take_or_pay_exists=True,
        continuous_delivery_hours_per_year=8760,
        customer_interval_meter_series_observed=False,
        realized_load_factor=None,
    )


def dcre057_contract_vs_realized_load_report() -> dict:
    surface = nwcpud_large_load_contract_surface()
    return {
        "experiment": "DCRE-057",
        "surface": surface,
        "contracted_minimum_is_realized_load": False,
        "delivery_availability_is_energy_used": False,
        "realized_load_factor_identified": False,
        "google_the_dalles_annual_mwh": None,
        "authority_effect": "NONE",
    }
