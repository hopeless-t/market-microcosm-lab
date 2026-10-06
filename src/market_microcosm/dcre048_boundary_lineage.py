from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportVintage:
    name: str
    total_electricity_mwh: dict[int, float]


@dataclass(frozen=True)
class BoundaryLineageAudit:
    compared_years: tuple[int, ...]
    stable_years: tuple[int, ...]
    drift_years: tuple[int, ...]
    maximum_absolute_drift_mwh: float
    recalculation_policy_exists: bool
    energy_metric_recalculations_disclosed: bool
    current_report_restates_2019_total_electricity: bool
    data_center_2019_electricity_disclosed: bool
    compute_metric_definition_public: bool

    @property
    def overlap_values_equal(self) -> bool:
        return not self.drift_years

    @property
    def full_lineage_closed(self) -> bool:
        return all(
            (
                self.overlap_values_equal,
                self.current_report_restates_2019_total_electricity,
                self.data_center_2019_electricity_disclosed,
                self.compute_metric_definition_public,
            )
        )


def google_total_electricity_vintages() -> tuple[ReportVintage, ...]:
    return (
        ReportVintage(
            "GOOGLE_2023_REPORT",
            {
                2019: 12_237_200.0,
                2020: 15_138_500.0,
                2021: 18_287_100.0,
                2022: 21_776_200.0,
            },
        ),
        ReportVintage(
            "GOOGLE_2024_REPORT",
            {
                2019: 12_237_200.0,
                2020: 15_138_500.0,
                2021: 18_287_100.0,
                2022: 21_776_200.0,
                2023: 25_307_000.0,
            },
        ),
        ReportVintage(
            "GOOGLE_2025_REPORT",
            {
                2020: 15_166_800.0,
                2021: 18_287_100.0,
                2022: 21_776_200.0,
                2023: 25_307_000.0,
                2024: 32_179_900.0,
            },
        ),
    )


def audit_visible_overlap(vintages: tuple[ReportVintage, ...]) -> tuple[
    tuple[int, ...], tuple[int, ...], tuple[int, ...], float
]:
    all_years = sorted({year for vintage in vintages for year in vintage.total_electricity_mwh})
    compared: list[int] = []
    stable: list[int] = []
    drift: list[int] = []
    maximum_drift = 0.0
    for year in all_years:
        values = [
            vintage.total_electricity_mwh[year]
            for vintage in vintages
            if year in vintage.total_electricity_mwh
        ]
        if len(values) < 2:
            continue
        compared.append(year)
        spread = max(values) - min(values)
        maximum_drift = max(maximum_drift, spread)
        if spread == 0.0:
            stable.append(year)
        else:
            drift.append(year)
    return tuple(compared), tuple(stable), tuple(drift), maximum_drift


def dcre048_boundary_lineage_audit() -> dict:
    vintages = google_total_electricity_vintages()
    compared, stable, drift, maximum_drift = audit_visible_overlap(vintages)
    audit = BoundaryLineageAudit(
        compared_years=compared,
        stable_years=stable,
        drift_years=drift,
        maximum_absolute_drift_mwh=maximum_drift,
        recalculation_policy_exists=True,
        energy_metric_recalculations_disclosed=True,
        current_report_restates_2019_total_electricity=False,
        data_center_2019_electricity_disclosed=False,
        compute_metric_definition_public=False,
    )
    return {
        "experiment": "DCRE-048",
        "vintages": vintages,
        "audit": audit,
        "visible_total_electricity_lineage_status": "PARTIAL_DRIFT_DETECTED",
        "full_cross_report_lineage_status": "OPEN",
        "promote_dcre047_bound": False,
        "candidate_eta": None,
        "authority_effect": "NONE",
    }
