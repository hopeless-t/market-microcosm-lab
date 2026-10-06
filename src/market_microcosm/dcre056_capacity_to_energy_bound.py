from __future__ import annotations

from dataclasses import dataclass


HOURS_PER_YEAR = 8760.0


@dataclass(frozen=True)
class CapacityBoundCertificate:
    capacity_positive: bool
    capacity_customer_specific: bool
    capacity_site_specific: bool
    capacity_population_matches_target: bool
    capacity_is_peak_power_not_energy: bool

    @property
    def certified(self) -> bool:
        return all(
            (
                self.capacity_positive,
                self.capacity_customer_specific,
                self.capacity_site_specific,
                self.capacity_population_matches_target,
                self.capacity_is_peak_power_not_energy,
            )
        )


def annual_energy_upper_bound_mwh(*, capacity_mw: float) -> float:
    if capacity_mw <= 0.0:
        raise ValueError("capacity_mw must be positive")
    return capacity_mw * HOURS_PER_YEAR


def nwcpud_2026_google_site_certificate() -> CapacityBoundCertificate:
    return CapacityBoundCertificate(
        capacity_positive=True,
        capacity_customer_specific=False,
        capacity_site_specific=False,
        capacity_population_matches_target=False,
        capacity_is_peak_power_not_energy=True,
    )


def dcre056_capacity_to_energy_bound_report() -> dict:
    observed_utility_load_mw = 277.0
    certificate = nwcpud_2026_google_site_certificate()
    mathematical_bound = annual_energy_upper_bound_mwh(
        capacity_mw=observed_utility_load_mw
    )
    return {
        "experiment": "DCRE-056",
        "observed_utility_load_mw": observed_utility_load_mw,
        "mathematical_annual_energy_upper_bound_mwh": mathematical_bound,
        "certificate": certificate,
        "promoted_google_site_annual_energy_upper_bound_mwh": (
            mathematical_bound if certificate.certified else None
        ),
        "google_site_capacity_mw": None,
        "google_site_annual_energy_mwh": None,
        "authority_effect": "NONE",
    }
