from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TemporalEvidenceCandidate:
    name: str
    cost: int
    authorized: bool
    resolves_predicate: bool
    observed_period: int
    metric_generation: str
    evidence_form: str


DECISION_PERIOD = 3
MAX_AGE_PERIODS = 1
REQUIRED_METRIC_GENERATION = "mrr-v2"


def temporal_candidates() -> tuple[TemporalEvidenceCandidate, ...]:
    return (
        TemporalEvidenceCandidate(
            name="stale_signed_predicate_attestation",
            cost=3,
            authorized=True,
            resolves_predicate=True,
            observed_period=0,
            metric_generation="mrr-v2",
            evidence_form="signed_boolean_attestation",
        ),
        TemporalEvidenceCandidate(
            name="fresh_old_generation_attestation",
            cost=2,
            authorized=True,
            resolves_predicate=True,
            observed_period=3,
            metric_generation="mrr-v1",
            evidence_form="signed_boolean_attestation",
        ),
        TemporalEvidenceCandidate(
            name="fresh_current_generation_attestation",
            cost=4,
            authorized=True,
            resolves_predicate=True,
            observed_period=3,
            metric_generation="mrr-v2",
            evidence_form="signed_boolean_attestation",
        ),
        TemporalEvidenceCandidate(
            name="fresh_exact_current_mrr",
            cost=5,
            authorized=True,
            resolves_predicate=True,
            observed_period=3,
            metric_generation="mrr-v2",
            evidence_form="exact_state_query",
        ),
    )


def evaluate_temporal_candidate(
    candidate: TemporalEvidenceCandidate,
) -> dict:
    age = DECISION_PERIOD - candidate.observed_period
    fresh = 0 <= age <= MAX_AGE_PERIODS
    generation_matches = (
        candidate.metric_generation
        == REQUIRED_METRIC_GENERATION
    )
    admissible = (
        candidate.authorized
        and candidate.resolves_predicate
        and fresh
        and generation_matches
    )

    return {
        **asdict(candidate),
        "age_periods": age,
        "fresh": fresh,
        "generation_matches": generation_matches,
        "admissible": admissible,
    }


def select_fresh_generation_aligned_evidence() -> dict:
    rows = [
        evaluate_temporal_candidate(candidate)
        for candidate in temporal_candidates()
    ]

    authority_only = [
        row
        for row in rows
        if row["authorized"] and row["resolves_predicate"]
    ]
    authority_only_selected = min(
        authority_only,
        key=lambda row: (row["cost"], row["name"]),
    )

    admissible = [
        row for row in rows if row["admissible"]
    ]
    if not admissible:
        raise ValueError("no temporally admissible evidence")

    selected = min(
        admissible,
        key=lambda row: (row["cost"], row["name"]),
    )

    return {
        "decision_period": DECISION_PERIOD,
        "max_age_periods": MAX_AGE_PERIODS,
        "required_metric_generation": REQUIRED_METRIC_GENERATION,
        "candidates": rows,
        "authority_only_selection": authority_only_selected,
        "temporal_generation_selection": selected,
    }


def temporal_evidence_report_payload() -> dict:
    selection = select_fresh_generation_aligned_evidence()
    authority_only = selection["authority_only_selection"]
    selected = selection["temporal_generation_selection"]

    gates = {
        "authority_only_search_is_insufficient": (
            authority_only["admissible"] is False
        ),
        "cheapest_authorized_candidate_has_wrong_generation": (
            authority_only["name"]
            == "fresh_old_generation_attestation"
            and authority_only["generation_matches"] is False
        ),
        "stale_current_generation_evidence_is_rejected": any(
            row["name"] == "stale_signed_predicate_attestation"
            and row["fresh"] is False
            and row["admissible"] is False
            for row in selection["candidates"]
        ),
        "selected_evidence_is_fresh": selected["fresh"] is True,
        "selected_evidence_matches_generation": (
            selected["generation_matches"] is True
        ),
        "selected_evidence_resolves_and_is_authorized": (
            selected["authorized"] is True
            and selected["resolves_predicate"] is True
        ),
    }

    return {
        "experiment": "E047",
        "question": (
            "Is authorized predicate-resolving evidence sufficient for a "
            "current decision if the evidence is stale or belongs to an "
            "older metric-definition generation?"
        ),
        "candidate_search": selection,
        "promotion_gate": gates,
        "promoted_temporal_rule": (
            "active-sensing-evidence-must-be-fresh-and-generation-aligned-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Active sensing admission now requires authorization, predicate "
            "resolution, decision-time freshness, and metric-generation "
            "alignment before cost optimization."
        ),
        "limitations": (
            "Periods and the one-period freshness budget are synthetic policy "
            "parameters. Production freshness must depend on the decision "
            "hazard rate, publication cadence, and metric update semantics."
        ),
    }
