from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScopeAlignmentCandidate:
    key: str
    source_url: str
    signal_a: str
    signal_b: str
    scope_relation: str
    time_relation: str
    grain_relation: str
    causal_elasticity_ready: bool
    blocker: str


def scope_alignment_candidates() -> tuple[ScopeAlignmentCandidate, ...]:
    return (
        ScopeAlignmentCandidate(
            key="google_efficiency_vs_electricity_growth",
            source_url="https://sustainability.google/commitments/water/",
            signal_a="more-than-6x compute per unit electricity versus five years earlier",
            signal_b="27% year-over-year data-center electricity growth in 2024",
            scope_relation="same company / data-center context but metric coverage is not published here as a matched panel",
            time_relation="five-year comparison versus one-year growth",
            grain_relation="efficiency ratio versus total electricity growth",
            causal_elasticity_ready=False,
            blocker="period and workload/capacity numerator are not scope-aligned for causal demand elasticity",
        ),
        ScopeAlignmentCandidate(
            key="lbl_accelerator_shipments_vs_total_electricity",
            source_url="https://escholarship.org/uc/item/33m6w3x0",
            signal_a="2024 accelerator shipments just over 7 million units; 2030 forecast 19 million",
            signal_b="2024 U.S. data-center electricity estimate 192 TWh; 2030 Reference 649 TWh",
            scope_relation="United States data-center model",
            time_relation="historical estimate plus forecast",
            grain_relation="accelerator shipment flow versus total electricity across servers, storage, networking, and infrastructure",
            causal_elasticity_ready=False,
            blocker="shipments are not installed compute stock and total electricity includes non-accelerator loads",
        ),
        ScopeAlignmentCandidate(
            key="microsoft_pue_wue_without_workload_volume",
            source_url="https://datacenters.microsoft.com/sustainability/efficiency/",
            signal_a="global PUE FY24 1.16 and FY25 1.17; global WUE FY24 .30 and FY25 .27 L/kWh",
            signal_b="owned-and-controlled datacenter operational scope",
            scope_relation="matched Microsoft owned-and-controlled fleet eligibility definition by fiscal year",
            time_relation="FY24 versus FY25",
            grain_relation="facility efficiency intensities without a matched total workload/capacity volume series",
            causal_elasticity_ready=False,
            blocker="intensity metrics constrain overhead/water efficiency but do not identify workload-volume elasticity",
        ),
    )


def causal_elasticity_ready_candidates() -> tuple[ScopeAlignmentCandidate, ...]:
    return tuple(row for row in scope_alignment_candidates() if row.causal_elasticity_ready)


def promotion_requirements() -> tuple[str, ...]:
    return (
        "matched_scope",
        "matched_period_or_explicit_lag_model",
        "stock_or_throughput_volume_not_unmatched_shipment_flow",
        "total_resource_boundary_documented",
        "metric_semantics_and_denominators_documented",
        "causal_confounders_or_identification_strategy_explicit",
    )


def scope_alignment_report() -> dict:
    candidates = scope_alignment_candidates()
    return {
        "candidate_count": len(candidates),
        "causal_elasticity_ready_count": len(causal_elasticity_ready_candidates()),
        "candidates": candidates,
        "promotion_requirements": promotion_requirements(),
        "eta_status": "UNKNOWN",
        "automatic_eta_write": None,
    }
