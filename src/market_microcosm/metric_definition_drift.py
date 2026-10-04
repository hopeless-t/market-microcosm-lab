from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MetricObservation:
    observation_id: str
    observed_on: str
    value_millions: float
    value_semantics: str
    metric_label: str
    definition_version: str
    source_id: str


@dataclass(frozen=True)
class MetricDefinitionEvent:
    event_id: str
    effective_on: str
    description: str
    source_id: str


def gamepass_membership_history() -> tuple[MetricObservation, ...]:
    return (
        MetricObservation(
            observation_id="gamepass-2022-25m-plus",
            observed_on="2022-01-18",
            value_millions=25.0,
            value_semantics="lower_bound_exclusive",
            metric_label="Game Pass subscribers",
            definition_version="pre-core-public-headline-v1",
            source_id="gamepass-2022-members-lower-bound",
        ),
        MetricObservation(
            observation_id="gamepass-2024-34m",
            observed_on="2024-02-15",
            value_millions=34.0,
            value_semantics="rounded_point",
            metric_label="Game Pass members",
            definition_version="post-core-public-headline-v2",
            source_id="gamepass-2024-members-rounded",
        ),
    )


def gamepass_definition_events() -> tuple[MetricDefinitionEvent, ...]:
    return (
        MetricDefinitionEvent(
            event_id="xbox-live-gold-to-game-pass-core",
            effective_on="2023-09-14",
            description=(
                "Xbox Live Gold members automatically became Game Pass "
                "Core members."
            ),
            source_id="gamepass-core-2023-definition-event",
        ),
    )


def naive_headline_growth() -> dict:
    earlier, later = gamepass_membership_history()
    ratio = later.value_millions / earlier.value_millions
    return {
        "earlier_millions_used_as_if_exact": earlier.value_millions,
        "later_millions_used_as_if_exact": later.value_millions,
        "naive_ratio": ratio,
        "naive_growth_fraction": ratio - 1.0,
        "authority": "illustrative_only",
        "invalidating_reasons": (
            "earlier observation is a strict lower bound rather than a point estimate",
            "later observation is a rounded public headline",
            "metric definition generation changes across the Core conversion",
        ),
    }


def growth_authority_check(
    earlier: MetricObservation,
    later: MetricObservation,
) -> dict:
    exact_semantics = {"exact_point"}
    same_definition = (
        earlier.definition_version == later.definition_version
    )
    exact_points = (
        earlier.value_semantics in exact_semantics
        and later.value_semantics in exact_semantics
    )
    chronological = earlier.observed_on < later.observed_on

    authorized = chronological and same_definition and exact_points

    reasons: list[str] = []
    if not chronological:
        reasons.append("non_chronological_observations")
    if not same_definition:
        reasons.append("definition_generation_mismatch")
    if not exact_points:
        reasons.append("non_exact_value_semantics")

    return {
        "authorized": authorized,
        "same_definition": same_definition,
        "exact_points": exact_points,
        "chronological": chronological,
        "rejection_reasons": reasons,
    }


def metric_definition_drift_report_payload() -> dict:
    observations = gamepass_membership_history()
    events = gamepass_definition_events()
    authority = growth_authority_check(
        observations[0],
        observations[1],
    )
    naive = naive_headline_growth()

    event_is_between_observations = (
        observations[0].observed_on
        < events[0].effective_on
        < observations[1].observed_on
    )

    gates = {
        "public_values_are_retained_with_value_semantics": (
            observations[0].value_semantics == "lower_bound_exclusive"
            and observations[1].value_semantics == "rounded_point"
        ),
        "definition_event_occurs_between_headlines": (
            event_is_between_observations
        ),
        "definition_versions_do_not_silently_match": (
            observations[0].definition_version
            != observations[1].definition_version
        ),
        "growth_rate_is_not_authorized": (
            authority["authorized"] is False
        ),
        "naive_36_percent_is_quarantined": (
            abs(naive["naive_growth_fraction"] - 0.36) < 1e-12
            and naive["authority"] == "illustrative_only"
        ),
        "metric_identity_includes_semantics_and_definition": True,
    }

    return {
        "experiment": "E027",
        "question": (
            "Can two public Game Pass membership headlines be treated as "
            "one comparable time series across a membership-definition event?"
        ),
        "observations": [asdict(row) for row in observations],
        "definition_events": [asdict(row) for row in events],
        "naive_headline_growth": naive,
        "growth_authority": authority,
        "promotion_gate": gates,
        "promoted_metric_rule": (
            "metric-definition-version-required-for-time-series-growth-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "Store empirical metrics as typed observations. A value, unit, "
            "date, bound/rounding semantic, and metric-definition generation "
            "must all match the estimator contract before a time-series "
            "growth calculation gains authority."
        ),
        "limitations": (
            "E027 does not estimate Game Pass growth. It demonstrates why "
            "the 2022 >25M subscriber headline and 2024 34M member headline "
            "cannot by themselves authorize a precise growth rate."
        ),
    }
