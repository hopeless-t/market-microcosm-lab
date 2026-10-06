from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UtilitySalesStructure:
    year: int
    total_mwh: float
    industrial_mwh: float
    commercial_mwh: float
    residential_mwh: float
    industrial_customers: int

    @property
    def industrial_share(self) -> float:
        return self.industrial_mwh / self.total_mwh

    @property
    def commercial_share(self) -> float:
        return self.commercial_mwh / self.total_mwh

    @property
    def residential_share(self) -> float:
        return self.residential_mwh / self.total_mwh


def eia_2024_nwcpud_sales_structure() -> UtilitySalesStructure:
    return UtilitySalesStructure(
        year=2024,
        total_mwh=1_530_602.0,
        industrial_mwh=1_263_389.0,
        commercial_mwh=121_887.0,
        residential_mwh=145_326.0,
        industrial_customers=190,
    )


def dcre062_utility_energy_structure_report() -> dict:
    structure = eia_2024_nwcpud_sales_structure()
    return {
        "experiment": "DCRE-062",
        "structure": structure,
        "sector_sum_matches_total": (
            structure.industrial_mwh
            + structure.commercial_mwh
            + structure.residential_mwh
            == structure.total_mwh
        ),
        "industrial_share": structure.industrial_share,
        "industrial_majority_of_sales": structure.industrial_share > 0.5,
        "utility_total_exceeds_one_twh": structure.total_mwh > 1_000_000.0,
        "independent_system_energy_crosscheck": True,
        "industrial_equals_data_center": False,
        "exact_data_center_share": None,
        "customer_specific_causality_identified": False,
        "authority_effect": "NONE",
    }
