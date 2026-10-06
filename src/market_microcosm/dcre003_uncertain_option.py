from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExplorationOutcome:
    prior_high: float
    safe_value: float
    explore_value: float
    oracle_value: float
    best_no_oracle_policy: str
    best_no_oracle_value: float
    oracle_regret: float


def evaluate_prior(
    prior_high: float,
    *,
    safe_now: float = 4.0,
    safe_future: float = 4.0,
    high_future: float = 12.0,
) -> ExplorationOutcome:
    if not 0.0 <= prior_high <= 1.0:
        raise ValueError("prior_high must be within [0, 1]")
    if min(safe_now, safe_future, high_future) < 0.0:
        raise ValueError("utilities must be non-negative")
    if high_future < safe_future:
        raise ValueError("high_future must be at least safe_future")

    safe_value = safe_now + safe_future
    explore_value = prior_high * high_future + (1.0 - prior_high) * safe_future
    oracle_value = safe_now + prior_high * high_future + (1.0 - prior_high) * safe_future

    tolerance = 1e-12
    if explore_value > safe_value + tolerance:
        policy = "EXPLORE"
        best_value = explore_value
    elif safe_value > explore_value + tolerance:
        policy = "SAFE"
        best_value = safe_value
    else:
        policy = "TIE"
        best_value = safe_value

    return ExplorationOutcome(
        prior_high=prior_high,
        safe_value=safe_value,
        explore_value=explore_value,
        oracle_value=oracle_value,
        best_no_oracle_policy=policy,
        best_no_oracle_value=best_value,
        oracle_regret=oracle_value - best_value,
    )


def prior_grid() -> tuple[ExplorationOutcome, ...]:
    return tuple(evaluate_prior(prior) for prior in (0.0, 0.25, 0.5, 0.75, 1.0))
