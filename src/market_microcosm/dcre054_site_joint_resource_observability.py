from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SiteResourceSurface:
    location: str
    water_consumption_million_gallons_2024: float
    pue_observed: bool
    site_electricity_mwh_2024: float | None

    @property
    def site_wue_identified(self) -> bool:
        return (
            self.pue_observed
            and self.site_electricity_mwh_2024 is not None
            and self.site_electricity_mwh_2024 > 0.0
        )


def matched_official_surfaces() -> tuple[SiteResourceSurface, ...]:
    return (
        SiteResourceSurface(
            location="Dublin, Ireland",
            water_consumption_million_gallons_2024=0.1,
            pue_observed=True,
            site_electricity_mwh_2024=None,
        ),
        SiteResourceSurface(
            location="Eemshaven, Netherlands",
            water_consumption_million_gallons_2024=330.0,
            pue_observed=True,
            site_electricity_mwh_2024=None,
        ),
        SiteResourceSurface(
            location="Hamina, Finland",
            water_consumption_million_gallons_2024=0.3,
            pue_observed=True,
            site_electricity_mwh_2024=None,
        ),
        SiteResourceSurface(
            location="St. Ghislain, Belgium",
            water_consumption_million_gallons_2024=393.3,
            pue_observed=True,
            site_electricity_mwh_2024=None,
        ),
    )


def dcre054_site_joint_resource_report() -> dict:
    surfaces = matched_official_surfaces()
    return {
        "experiment": "DCRE-054",
        "surfaces": surfaces,
        "water_location_series_observed": True,
        "campus_pue_series_observed": True,
        "site_absolute_electricity_series_observed": False,
        "matched_site_count": len(surfaces),
        "identified_site_wue_count": sum(
            int(surface.site_wue_identified) for surface in surfaces
        ),
        "site_energy_water_substitution_identified": False,
        "missing_variable": "SITE_ABSOLUTE_ELECTRICITY_MWH",
        "authority_effect": "NONE",
    }
