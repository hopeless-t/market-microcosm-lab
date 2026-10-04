from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations


@dataclass(frozen=True)
class DependencyShock:
    name: str
    affected_witnesses: tuple[int, ...]
    probability: float


@dataclass(frozen=True)
class ShockSubsetOutcome:
    active_shocks: tuple[str, ...]
    affected_witnesses: tuple[int, ...]
    forge_possible: bool
    probability: float


def nominal_independent_shocks(
    *,
    witness_count: int = 5,
    probability: float = 0.01,
) -> tuple[DependencyShock, ...]:
    return tuple(
        DependencyShock(
            name=f"domain-{index}",
            affected_witnesses=(index,),
            probability=probability,
        )
        for index in range(witness_count)
    )


def hidden_common_mode_shocks(
    *,
    probability: float = 0.01,
) -> tuple[DependencyShock, ...]:
    return nominal_independent_shocks(probability=probability) + (
        DependencyShock(
            name="hidden-shared-kms",
            affected_witnesses=(0, 1, 2),
            probability=probability,
        ),
    )


def enumerate_shock_subsets(
    shocks: tuple[DependencyShock, ...],
    *,
    quorum_threshold: int = 3,
) -> tuple[ShockSubsetOutcome, ...]:
    outcomes: list[ShockSubsetOutcome] = []
    shock_count = len(shocks)

    for size in range(shock_count + 1):
        for indexes in combinations(range(shock_count), size):
            active = set(indexes)
            affected: set[int] = set()
            probability = 1.0

            for index, shock in enumerate(shocks):
                if not 0.0 <= shock.probability <= 1.0:
                    raise ValueError(
                        f"invalid probability for {shock.name}"
                    )
                if index in active:
                    probability *= shock.probability
                    affected.update(shock.affected_witnesses)
                else:
                    probability *= 1.0 - shock.probability

            outcomes.append(
                ShockSubsetOutcome(
                    active_shocks=tuple(
                        shocks[index].name for index in indexes
                    ),
                    affected_witnesses=tuple(sorted(affected)),
                    forge_possible=len(affected) >= quorum_threshold,
                    probability=probability,
                )
            )
    return tuple(outcomes)


def exact_forge_probability(
    shocks: tuple[DependencyShock, ...],
    *,
    quorum_threshold: int = 3,
) -> float:
    return sum(
        row.probability
        for row in enumerate_shock_subsets(
            shocks,
            quorum_threshold=quorum_threshold,
        )
        if row.forge_possible
    )


def minimum_shocks_to_forge(
    shocks: tuple[DependencyShock, ...],
    *,
    quorum_threshold: int = 3,
) -> int:
    values = [
        len(row.active_shocks)
        for row in enumerate_shock_subsets(
            shocks,
            quorum_threshold=quorum_threshold,
        )
        if row.forge_possible
    ]
    if not values:
        raise ValueError("no shock subset can reach quorum")
    return min(values)


def minimal_forge_witnesses(
    shocks: tuple[DependencyShock, ...],
    *,
    quorum_threshold: int = 3,
) -> tuple[dict, ...]:
    outcomes = enumerate_shock_subsets(
        shocks,
        quorum_threshold=quorum_threshold,
    )
    minimum = min(
        len(row.active_shocks)
        for row in outcomes
        if row.forge_possible
    )
    return tuple(
        asdict(row)
        for row in outcomes
        if row.forge_possible
        and len(row.active_shocks) == minimum
    )


def hidden_common_mode_report_payload() -> dict:
    probability = 0.01
    threshold = 3

    nominal = nominal_independent_shocks(
        probability=probability,
    )
    hidden = hidden_common_mode_shocks(
        probability=probability,
    )

    nominal_probability = exact_forge_probability(
        nominal,
        quorum_threshold=threshold,
    )
    hidden_probability = exact_forge_probability(
        hidden,
        quorum_threshold=threshold,
    )

    nominal_minimum = minimum_shocks_to_forge(
        nominal,
        quorum_threshold=threshold,
    )
    hidden_minimum = minimum_shocks_to_forge(
        hidden,
        quorum_threshold=threshold,
    )

    inflation_ratio = hidden_probability / nominal_probability
    probability_increase = hidden_probability - nominal_probability

    hidden_minimal = minimal_forge_witnesses(
        hidden,
        quorum_threshold=threshold,
    )

    gates = {
        "nominal_model_requires_three_shocks": nominal_minimum == 3,
        "hidden_common_mode_collapses_to_one_shock": hidden_minimum == 1,
        "hidden_single_shock_hits_quorum": any(
            row["active_shocks"] == ("hidden-shared-kms",)
            and len(row["affected_witnesses"]) >= threshold
            for row in hidden_minimal
        ),
        "hidden_dependency_inflates_modeled_forge_probability_over_100x": (
            inflation_ratio > 100.0
        ),
        "hidden_model_probability_exceeds_one_percent": (
            hidden_probability > 0.01
        ),
        "exact_subset_enumeration_complete": (
            len(enumerate_shock_subsets(nominal)) == 2 ** len(nominal)
            and len(enumerate_shock_subsets(hidden)) == 2 ** len(hidden)
        ),
    }

    return {
        "experiment": "E023",
        "question": (
            "Can a nominally independent 3-of-5 witness topology still "
            "collapse under an undeclared shared dependency?"
        ),
        "quorum_threshold": threshold,
        "synthetic_shock_probability": probability,
        "nominal_model": {
            "shock_count": len(nominal),
            "minimum_shocks_to_forge": nominal_minimum,
            "forge_probability": nominal_probability,
            "shocks": [asdict(row) for row in nominal],
        },
        "hidden_common_mode_model": {
            "shock_count": len(hidden),
            "minimum_shocks_to_forge": hidden_minimum,
            "forge_probability": hidden_probability,
            "shocks": [asdict(row) for row in hidden],
            "minimal_forge_subsets": hidden_minimal,
        },
        "comparison": {
            "forge_probability_increase": probability_increase,
            "forge_probability_inflation_ratio": inflation_ratio,
        },
        "promotion_gate": gates,
        "promoted_dependency_rule": (
            "declared-domain-independence-requires-hidden-dependency-audit-v1"
            if all(gates.values())
            else None
        ),
        "limitation": (
            "The hidden shared-KMS dependency and homogeneous 1% shock rates "
            "are synthetic. The experiment demonstrates sensitivity to "
            "undeclared common modes; it does not estimate real infrastructure "
            "failure probabilities."
        ),
    }
