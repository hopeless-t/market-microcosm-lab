from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TechnologyShock:
    task_cost_ratio_after_shock: float = 0.10
    legacy_human_substitution_rate: float = 0.80
    automated_legacy_output: float = 90.0
    potential_new_human_roles: int = 50


@dataclass(frozen=True)
class TransitionOutcome:
    name: str
    total_workers: int
    legacy_workers_before: int
    legacy_workers_after: int
    incumbent_complement_workers: int
    transitioned_workers: int
    unemployed_workers: int
    output: float
    household_income: float
    employment_rate: float
    legacy_headcount_reduction: float
    viable: bool


TOTAL_WORKERS = 100
BASELINE_LEGACY_WORKERS = 60
BASELINE_COMPLEMENT_WORKERS = 40
BASELINE_OUTPUT = 100.0
BASELINE_HOUSEHOLD_INCOME = 100.0
EMPLOYMENT_FLOOR = 0.90
INCOME_FLOOR = 90.0


def baseline_outcome() -> TransitionOutcome:
    return TransitionOutcome(
        name="BASELINE",
        total_workers=TOTAL_WORKERS,
        legacy_workers_before=BASELINE_LEGACY_WORKERS,
        legacy_workers_after=BASELINE_LEGACY_WORKERS,
        incumbent_complement_workers=BASELINE_COMPLEMENT_WORKERS,
        transitioned_workers=0,
        unemployed_workers=0,
        output=BASELINE_OUTPUT,
        household_income=BASELINE_HOUSEHOLD_INCOME,
        employment_rate=1.0,
        legacy_headcount_reduction=0.0,
        viable=True,
    )


def simulate_transition(
    *,
    name: str,
    transition_capacity: int,
    shock: TechnologyShock = TechnologyShock(),
) -> TransitionOutcome:
    if not 0 <= shock.legacy_human_substitution_rate <= 1:
        raise ValueError("substitution rate must be in [0, 1]")
    if transition_capacity < 0:
        raise ValueError("transition_capacity must be non-negative")

    legacy_after = int(
        round(
            BASELINE_LEGACY_WORKERS
            * (1.0 - shock.legacy_human_substitution_rate)
        )
    )
    displaced = BASELINE_LEGACY_WORKERS - legacy_after
    transitioned = min(
        displaced,
        transition_capacity,
        shock.potential_new_human_roles,
    )
    unemployed = displaced - transitioned
    employed = (
        legacy_after
        + BASELINE_COMPLEMENT_WORKERS
        + transitioned
    )

    # Synthetic output units: the transformed legacy task bundle produces
    # automated_legacy_output; incumbent and newly rebundled human roles each
    # contribute one output unit. This is a frozen exact world, not calibration.
    output = (
        shock.automated_legacy_output
        + BASELINE_COMPLEMENT_WORKERS
        + transitioned
    )
    income = float(employed)
    employment_rate = employed / TOTAL_WORKERS
    legacy_reduction = 1.0 - legacy_after / BASELINE_LEGACY_WORKERS
    viable = (
        employment_rate >= EMPLOYMENT_FLOOR
        and income >= INCOME_FLOOR
    )

    return TransitionOutcome(
        name=name,
        total_workers=TOTAL_WORKERS,
        legacy_workers_before=BASELINE_LEGACY_WORKERS,
        legacy_workers_after=legacy_after,
        incumbent_complement_workers=BASELINE_COMPLEMENT_WORKERS,
        transitioned_workers=transitioned,
        unemployed_workers=unemployed,
        output=output,
        household_income=income,
        employment_rate=employment_rate,
        legacy_headcount_reduction=legacy_reduction,
        viable=viable,
    )


def t001_report() -> dict:
    shock = TechnologyShock()
    baseline = baseline_outcome()
    fast = simulate_transition(
        name="FAST_REALLOCATION",
        transition_capacity=48,
        shock=shock,
    )
    frictional = simulate_transition(
        name="FRICTIONAL_TRANSITION",
        transition_capacity=20,
        shock=shock,
    )
    return {
        "experiment": "T001",
        "shock": shock,
        "baseline": baseline,
        "fast_reallocation": fast,
        "frictional_transition": frictional,
        "same_technology_shock": True,
        "occupation_collapse_threshold": 0.75,
        "aggregate_expansion_in_both_shock_worlds": (
            fast.output > baseline.output
            and frictional.output > baseline.output
        ),
        "legacy_occupation_collapses_in_both": (
            fast.legacy_headcount_reduction >= 0.75
            and frictional.legacy_headcount_reduction >= 0.75
        ),
        "human_viability_diverges": fast.viable and not frictional.viable,
        "authority_effect": "NONE",
    }
