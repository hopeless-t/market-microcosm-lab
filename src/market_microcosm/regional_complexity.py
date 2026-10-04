from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import sqrt


REGIONS = ("APAC", "EMEA", "LATAM", "UCAN")
DISCOVERY_QUARTERS = ("Q2-2023", "Q3-2023", "Q4-2023", "Q1-2024")
HOLDOUT_QUARTER = "Q2-2024"


@dataclass(frozen=True)
class RegionalObservation:
    arm_usd: float
    paid_memberships_millions: float


def netflix_regional_arm_history() -> dict[str, dict[str, RegionalObservation]]:
    raw = {
        "Q2-2023": {
            "UCAN": (16.00, 75.57),
            "EMEA": (10.87, 79.81),
            "LATAM": (8.58, 42.47),
            "APAC": (7.66, 40.55),
        },
        "Q3-2023": {
            "UCAN": (16.29, 77.32),
            "EMEA": (10.98, 83.76),
            "LATAM": (8.85, 43.65),
            "APAC": (7.62, 42.43),
        },
        "Q4-2023": {
            "UCAN": (16.64, 80.13),
            "EMEA": (10.75, 88.81),
            "LATAM": (8.60, 46.00),
            "APAC": (7.31, 45.34),
        },
        "Q1-2024": {
            "UCAN": (17.30, 82.66),
            "EMEA": (10.92, 91.73),
            "LATAM": (8.29, 47.72),
            "APAC": (7.35, 47.50),
        },
        "Q2-2024": {
            "UCAN": (17.17, 84.11),
            "EMEA": (10.80, 93.96),
            "LATAM": (8.28, 49.25),
            "APAC": (7.17, 50.32),
        },
    }
    return {
        quarter: {
            region: RegionalObservation(
                arm_usd=values[0],
                paid_memberships_millions=values[1],
            )
            for region, values in rows.items()
        }
        for quarter, rows in raw.items()
    }


def _canonical_partition(
    groups: tuple[tuple[str, ...], ...],
) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted(tuple(sorted(group)) for group in groups))


def _set_partitions(
    items: tuple[str, ...],
) -> tuple[tuple[tuple[str, ...], ...], ...]:
    if not items:
        return ((),)

    first = items[0]
    tails = _set_partitions(items[1:])
    candidates: set[tuple[tuple[str, ...], ...]] = set()

    for partition in tails:
        candidates.add(_canonical_partition(((first,),) + partition))
        for index in range(len(partition)):
            groups = [tuple(group) for group in partition]
            groups[index] = tuple(sorted((first,) + groups[index]))
            candidates.add(_canonical_partition(tuple(groups)))

    return tuple(sorted(candidates))


def _fit_centroids(
    observations: dict[str, RegionalObservation],
    partition: tuple[tuple[str, ...], ...],
) -> dict[str, float]:
    predicted: dict[str, float] = {}

    for group in partition:
        weight = sum(
            observations[region].paid_memberships_millions
            for region in group
        )
        mean = sum(
            observations[region].arm_usd
            * observations[region].paid_memberships_millions
            for region in group
        ) / weight
        for region in group:
            predicted[region] = mean

    return predicted


def _evaluate_predictions(
    observations: dict[str, RegionalObservation],
    predicted: dict[str, float],
) -> dict:
    total_weight = sum(
        row.paid_memberships_millions
        for row in observations.values()
    )
    weighted_squared_error = sum(
        observations[region].paid_memberships_millions
        * (predicted[region] - observations[region].arm_usd) ** 2
        for region in observations
    )
    relative_errors = {
        region: abs(predicted[region] - observations[region].arm_usd)
        / observations[region].arm_usd
        for region in observations
    }

    return {
        "weighted_rmse_usd": sqrt(weighted_squared_error / total_weight),
        "max_relative_error": max(relative_errors.values()),
        "relative_errors": relative_errors,
        "predicted_arm_usd": predicted,
    }


def evaluate_partition(
    observations: dict[str, RegionalObservation],
    partition: tuple[tuple[str, ...], ...],
) -> dict:
    predicted = _fit_centroids(observations, partition)
    return _evaluate_predictions(observations, predicted)


def discovery_complexity_frontier() -> dict[int, dict]:
    history = netflix_regional_arm_history()
    partitions = _set_partitions(REGIONS)
    frontier: dict[int, dict] = {}

    for group_count in range(1, len(REGIONS) + 1):
        candidates: list[tuple[tuple, dict]] = []

        for partition in partitions:
            if len(partition) != group_count:
                continue

            quarter_metrics = {
                quarter: evaluate_partition(history[quarter], partition)
                for quarter in DISCOVERY_QUARTERS
            }
            worst_max_relative_error = max(
                row["max_relative_error"]
                for row in quarter_metrics.values()
            )
            mean_weighted_rmse = sum(
                row["weighted_rmse_usd"]
                for row in quarter_metrics.values()
            ) / len(quarter_metrics)
            score = (
                worst_max_relative_error,
                mean_weighted_rmse,
                partition,
            )
            candidates.append(
                (
                    score,
                    {
                        "group_count": group_count,
                        "partition": [list(group) for group in partition],
                        "worst_max_relative_error": worst_max_relative_error,
                        "mean_weighted_rmse_usd": mean_weighted_rmse,
                        "quarter_metrics": quarter_metrics,
                    },
                )
            )

        if not candidates:
            raise ValueError(f"no partition for group count {group_count}")

        _, best = min(candidates, key=lambda row: row[0])
        frontier[group_count] = best

    return frontier


def minimum_admissible_complexity(
    *,
    max_relative_error_tolerance: float = 0.10,
) -> dict:
    frontier = discovery_complexity_frontier()

    for group_count in sorted(frontier):
        row = frontier[group_count]
        if row["worst_max_relative_error"] <= max_relative_error_tolerance:
            return {
                "tolerance": max_relative_error_tolerance,
                "minimum_group_count": group_count,
                "selected": row,
                "frontier": frontier,
            }

    raise ValueError("no regional partition meets tolerance")


def one_quarter_forward_holdout(
    partition: tuple[tuple[str, ...], ...],
) -> dict:
    history = netflix_regional_arm_history()
    calibration = history["Q1-2024"]
    holdout = history[HOLDOUT_QUARTER]
    predicted = _fit_centroids(calibration, partition)
    metrics = _evaluate_predictions(holdout, predicted)

    return {
        "calibration_quarter": "Q1-2024",
        "holdout_quarter": HOLDOUT_QUARTER,
        "partition": [list(group) for group in partition],
        "fixed_calibration_centroids_usd": predicted,
        **metrics,
    }


def regional_complexity_report_payload() -> dict:
    tolerance = 0.10
    selection = minimum_admissible_complexity(
        max_relative_error_tolerance=tolerance
    )
    selected_partition = tuple(
        tuple(group)
        for group in selection["selected"]["partition"]
    )
    holdout = one_quarter_forward_holdout(selected_partition)
    expected_partition = (
        ("APAC", "LATAM"),
        ("EMEA",),
        ("UCAN",),
    )

    frontier = selection["frontier"]
    gates = {
        "discovery_excludes_holdout_quarter": (
            HOLDOUT_QUARTER not in DISCOVERY_QUARTERS
        ),
        "one_group_is_rejected": (
            frontier[1]["worst_max_relative_error"] > tolerance
        ),
        "two_groups_are_rejected": (
            frontier[2]["worst_max_relative_error"] > tolerance
        ),
        "three_groups_meet_tolerance": (
            frontier[3]["worst_max_relative_error"] <= tolerance
        ),
        "minimum_complexity_is_three": (
            selection["minimum_group_count"] == 3
        ),
        "stable_three_group_topology": (
            selected_partition == expected_partition
        ),
        "one_quarter_forward_holdout_meets_tolerance": (
            holdout["max_relative_error"] <= tolerance
        ),
    }

    return {
        "experiment": "E025",
        "question": (
            "What is the smallest regional ARM model that preserves the "
            "observed Netflix cross-sectional structure to a declared error "
            "tolerance, and does that structure survive a one-quarter holdout?"
        ),
        "source_id": "netflix-q2-2024-regional",
        "metric_definition": (
            "ARM is average revenue per membership as defined by Netflix; "
            "it is not a posted subscription price."
        ),
        "discovery_quarters": list(DISCOVERY_QUARTERS),
        "holdout_quarter": HOLDOUT_QUARTER,
        "max_relative_error_tolerance": tolerance,
        "complexity_selection": selection,
        "forward_holdout": holdout,
        "promotion_gate": gates,
        "promoted_regional_rule": (
            "regional-arm-complexity-knee-k3-v1"
            if all(gates.values())
            else None
        ),
        "model_update": (
            "For this five-quarter aggregate ARM window, replace one global "
            "empirical revenue-per-membership parameter with at least three "
            "regional groups: UCAN, EMEA, and LATAM+APAC. This is a compression "
            "result, not a causal segmentation claim."
        ),
        "limitations": (
            "The source contains only four broad Netflix reporting regions and "
            "five quarters. Group centroids are descriptive compression "
            "parameters. They do not identify plan prices, willingness to pay, "
            "or causal regional effects."
        ),
    }
