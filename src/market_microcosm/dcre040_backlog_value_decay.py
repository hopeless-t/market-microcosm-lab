from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BacklogValueChoice:
    strategy: str
    decay_fraction: float
    completed_now: float
    completed_later: float
    gross_completed_value: float
    burst_cost: float
    net_value: float


def pace_backlog(
    decay_fraction: float,
    *,
    backlog: float = 40.0,
    normal_spare: float = 20.0,
) -> BacklogValueChoice:
    if not 0.0 <= decay_fraction <= 1.0:
        raise ValueError("decay_fraction must be within [0, 1]")
    now = min(backlog, normal_spare)
    later = backlog - now
    gross = now + later * (1.0 - decay_fraction)
    return BacklogValueChoice(
        strategy="PACE",
        decay_fraction=decay_fraction,
        completed_now=now,
        completed_later=later,
        gross_completed_value=gross,
        burst_cost=0.0,
        net_value=gross,
    )


def burst_backlog(
    decay_fraction: float,
    *,
    backlog: float = 40.0,
    burst_cost: float = 4.0,
) -> BacklogValueChoice:
    if not 0.0 <= decay_fraction <= 1.0:
        raise ValueError("decay_fraction must be within [0, 1]")
    if burst_cost < 0.0:
        raise ValueError("burst_cost must be non-negative")
    gross = backlog
    return BacklogValueChoice(
        strategy="BURST",
        decay_fraction=decay_fraction,
        completed_now=backlog,
        completed_later=0.0,
        gross_completed_value=gross,
        burst_cost=burst_cost,
        net_value=gross - burst_cost,
    )


def decay_knee(
    *,
    delayed_backlog: float = 20.0,
    burst_cost: float = 4.0,
) -> float:
    if delayed_backlog <= 0.0:
        raise ValueError("delayed_backlog must be positive")
    if burst_cost < 0.0:
        raise ValueError("burst_cost must be non-negative")
    return burst_cost / delayed_backlog


def frozen_backlog_value_market() -> dict:
    return {
        "low_decay_pace": pace_backlog(0.10),
        "low_decay_burst": burst_backlog(0.10),
        "high_decay_pace": pace_backlog(0.30),
        "high_decay_burst": burst_backlog(0.30),
        "decay_knee": decay_knee(),
    }
