from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RecordSemantics(str, Enum):
    UTILITY_AGGREGATE_ENERGY = "UTILITY_AGGREGATE_ENERGY"
    PEAK_OR_CONTRACT_CAPACITY = "PEAK_OR_CONTRACT_CAPACITY"
    CUSTOMER_SITE_ANNUAL_ENERGY = "CUSTOMER_SITE_ANNUAL_ENERGY"


@dataclass(frozen=True)
class ExternalInfrastructureRecord:
    source: str
    semantics: RecordSemantics
    observed_value: float | None
    unit: str
    customer_specific: bool
    google_the_dalles_specific: bool


def the_dalles_external_records() -> tuple[ExternalInfrastructureRecord, ...]:
    return (
        ExternalInfrastructureRecord(
            source="Northern Wasco County PUD public system-load history",
            semantics=RecordSemantics.UTILITY_AGGREGATE_ENERGY,
            observed_value=1_000_000_000.0,
            unit="kWh/year lower-bound wording",
            customer_specific=False,
            google_the_dalles_specific=False,
        ),
        ExternalInfrastructureRecord(
            source="Oregon DCAC / NWCPUD large-load service process",
            semantics=RecordSemantics.PEAK_OR_CONTRACT_CAPACITY,
            observed_value=5.0,
            unit="MW agreement threshold",
            customer_specific=False,
            google_the_dalles_specific=False,
        ),
    )


def dcre055_external_site_energy_audit() -> dict:
    records = the_dalles_external_records()
    customer_site_energy = tuple(
        record
        for record in records
        if record.semantics is RecordSemantics.CUSTOMER_SITE_ANNUAL_ENERGY
        and record.customer_specific
        and record.google_the_dalles_specific
    )
    return {
        "experiment": "DCRE-055",
        "records": records,
        "utility_aggregate_energy_observed": any(
            record.semantics is RecordSemantics.UTILITY_AGGREGATE_ENERGY
            for record in records
        ),
        "power_or_contract_capacity_observed": any(
            record.semantics is RecordSemantics.PEAK_OR_CONTRACT_CAPACITY
            for record in records
        ),
        "google_the_dalles_annual_mwh": None,
        "customer_site_energy_record_count": len(customer_site_energy),
        "power_capacity_is_energy_consumption": False,
        "utility_aggregate_is_customer_load": False,
        "site_wue_identified": False,
        "authority_effect": "NONE",
    }
