from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalSeries:
    name: str
    geography: str
    equipment_scope: str
    period_start: int
    period_end: int
    semantic_kind: str
    provenance_class: str
    independent_observation: bool
    demand_quantity: bool
    complete_public_numeric_series: bool


@dataclass(frozen=True)
class CalibrationAudit:
    same_geography: bool
    same_equipment_scope: bool
    overlapping_period: bool
    provenance_independent: bool
    demand_semantics_aligned: bool
    complete_pairwise_numeric_series: bool
    causal_calibration_admissible: bool
    blocking_reasons: tuple[str, ...]


def lbnl_historical_pair() -> tuple[HistoricalSeries, HistoricalSeries]:
    installed_base = HistoricalSeries(
        name="LBNL_SERVER_INSTALLED_BASE_2014_2023",
        geography="US_DATA_CENTERS",
        equipment_scope="SERVERS",
        period_start=2014,
        period_end=2023,
        semantic_kind="EQUIPMENT_STOCK_PROXY",
        provenance_class="MODEL_DERIVED_FROM_SHIPMENTS_AND_LIFETIME",
        independent_observation=False,
        demand_quantity=False,
        complete_public_numeric_series=False,
    )
    server_electricity = HistoricalSeries(
        name="LBNL_SERVER_ELECTRICITY_2014_2023",
        geography="US_DATA_CENTERS",
        equipment_scope="SERVERS",
        period_start=2014,
        period_end=2023,
        semantic_kind="MODELED_ENERGY_OUTCOME",
        provenance_class="MODEL_DERIVED_FROM_INSTALLED_BASE_POWER_AND_UTILIZATION",
        independent_observation=False,
        demand_quantity=False,
        complete_public_numeric_series=False,
    )
    return installed_base, server_electricity


def audit_causal_calibration(
    left: HistoricalSeries,
    right: HistoricalSeries,
) -> CalibrationAudit:
    same_geography = left.geography == right.geography
    same_equipment_scope = left.equipment_scope == right.equipment_scope
    overlapping_period = not (
        left.period_end < right.period_start or right.period_end < left.period_start
    )
    provenance_independent = left.independent_observation and right.independent_observation
    demand_semantics_aligned = left.demand_quantity or right.demand_quantity
    complete_pairwise_numeric_series = (
        left.complete_public_numeric_series and right.complete_public_numeric_series
    )

    reasons: list[str] = []
    if not provenance_independent:
        reasons.append("MODEL_FAMILY_DEPENDENCE")
    if not demand_semantics_aligned:
        reasons.append("NO_SERVICE_OR_COMPUTE_DEMAND_QUANTITY")
    if not complete_pairwise_numeric_series:
        reasons.append("NO_COMPLETE_PUBLIC_PAIRED_NUMERIC_SERIES")

    admissible = (
        same_geography
        and same_equipment_scope
        and overlapping_period
        and provenance_independent
        and demand_semantics_aligned
        and complete_pairwise_numeric_series
    )
    return CalibrationAudit(
        same_geography=same_geography,
        same_equipment_scope=same_equipment_scope,
        overlapping_period=overlapping_period,
        provenance_independent=provenance_independent,
        demand_semantics_aligned=demand_semantics_aligned,
        complete_pairwise_numeric_series=complete_pairwise_numeric_series,
        causal_calibration_admissible=admissible,
        blocking_reasons=tuple(reasons),
    )


def dcre045_scope_aligned_history_audit() -> dict:
    installed_base, server_electricity = lbnl_historical_pair()
    audit = audit_causal_calibration(installed_base, server_electricity)
    return {
        "experiment": "DCRE-045",
        "pair": (installed_base, server_electricity),
        "audit": audit,
        "candidate_eta": None,
        "chart_digitization_authorized": False,
        "authority_effect": "NONE",
    }
