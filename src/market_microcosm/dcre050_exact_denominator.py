from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DenominatorEvidenceSurface:
    chart_years: tuple[int, ...]
    table_years: tuple[int, ...]
    chart_has_exact_numeric_labels: bool
    exact_2019_data_center_mwh: float | None
    chart_digitization_authorized: bool

    @property
    def exact_2019_denominator_observed(self) -> bool:
        return self.exact_2019_data_center_mwh is not None


def google_2025_dc_denominator_surface() -> DenominatorEvidenceSurface:
    return DenominatorEvidenceSurface(
        chart_years=(2019, 2020, 2021, 2022, 2023, 2024),
        table_years=(2020, 2021, 2022, 2023, 2024),
        chart_has_exact_numeric_labels=False,
        exact_2019_data_center_mwh=None,
        chart_digitization_authorized=False,
    )


def dcre050_exact_denominator_audit() -> dict:
    surface = google_2025_dc_denominator_surface()
    return {
        "experiment": "DCRE-050",
        "surface": surface,
        "known_table_values_mwh": {
            2020: 14_426_600.0,
            2021: 17_659_000.0,
            2022: 20_806_200.0,
            2023: 24_294_900.0,
            2024: 30_825_600.0,
        },
        "exact_2019_dc_denominator_status": "UNOBSERVED",
        "promoted_2019_dc_mwh": None,
        "promoted_dcre047_bound": None,
        "candidate_eta": None,
        "authority_effect": "NONE",
    }
