from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OutputEvidence:
    name: str
    scope: str
    period_start: int | None
    period_end: int | None
    metric_kind: str
    raw_series_public: bool
    definition_reproducible: bool
    contains_energy_denominator: bool


@dataclass(frozen=True)
class OutputObservabilityAudit:
    scope_aligned: bool
    period_aligned: bool
    definition_reproducible: bool
    absolute_output_reconstructible: bool
    causal_calibration_admissible: bool
    blocking_reasons: tuple[str, ...]


def google_near_miss_pair() -> tuple[OutputEvidence, OutputEvidence]:
    compute_efficiency = OutputEvidence(
        name="GOOGLE_DC_COMPUTE_PER_ELECTRICITY_RELATIVE_5Y",
        scope="GOOGLE_DATA_CENTER_FLEET",
        period_start=2019,
        period_end=2024,
        metric_kind="RELATIVE_COMPUTE_PER_ELECTRICITY_INDEX",
        raw_series_public=False,
        definition_reproducible=False,
        contains_energy_denominator=True,
    )
    electricity = OutputEvidence(
        name="GOOGLE_DC_ELECTRICITY_SERIES_2020_2024",
        scope="GOOGLE_DATA_CENTER_FLEET",
        period_start=2020,
        period_end=2024,
        metric_kind="ELECTRICITY_CONSUMPTION",
        raw_series_public=True,
        definition_reproducible=True,
        contains_energy_denominator=False,
    )
    return compute_efficiency, electricity


def audit_output_observability(
    compute_efficiency: OutputEvidence,
    electricity: OutputEvidence,
) -> OutputObservabilityAudit:
    scope_aligned = compute_efficiency.scope == electricity.scope
    period_aligned = (
        compute_efficiency.period_start == electricity.period_start
        and compute_efficiency.period_end == electricity.period_end
    )
    definition_reproducible = compute_efficiency.definition_reproducible
    absolute_output_reconstructible = (
        scope_aligned
        and period_aligned
        and definition_reproducible
        and compute_efficiency.raw_series_public
        and electricity.raw_series_public
    )

    reasons: list[str] = []
    if not period_aligned:
        reasons.append("BASELINE_PERIOD_MISMATCH")
    if not definition_reproducible:
        reasons.append("COMPUTE_METRIC_DEFINITION_OPAQUE")
    if not compute_efficiency.raw_series_public:
        reasons.append("NO_PUBLIC_COMPUTE_INDEX_SERIES")

    return OutputObservabilityAudit(
        scope_aligned=scope_aligned,
        period_aligned=period_aligned,
        definition_reproducible=definition_reproducible,
        absolute_output_reconstructible=absolute_output_reconstructible,
        causal_calibration_admissible=False,
        blocking_reasons=tuple(reasons),
    )


def dcre046_output_observability_audit() -> dict:
    pair = google_near_miss_pair()
    audit = audit_output_observability(*pair)
    return {
        "experiment": "DCRE-046",
        "pair": pair,
        "audit": audit,
        "candidate_output_growth": None,
        "candidate_eta": None,
        "partial_identification_candidate": True,
        "authority_effect": "NONE",
    }
