from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriceEpoch:
    epoch: int
    signal_a: float
    signal_b: float
    flexible_a: float
    load_a: float
    load_b: float


def simulate_lagged_price_response(
    *,
    epochs: int = 6,
    responsive_fraction: float = 1.0,
    base_load_each: float = 40.0,
    flexible_total: float = 40.0,
    initial_signal_a: float = 60.0,
    initial_signal_b: float = 40.0,
) -> tuple[PriceEpoch, ...]:
    if epochs < 1:
        raise ValueError("epochs must be positive")
    if not 0.0 <= responsive_fraction <= 1.0:
        raise ValueError("responsive_fraction must be within [0, 1]")

    signal_a = initial_signal_a
    signal_b = initial_signal_b
    rows: list[PriceEpoch] = []

    anchored = flexible_total * (1.0 - responsive_fraction)
    anchored_each = anchored / 2.0
    responsive = flexible_total * responsive_fraction

    for epoch in range(epochs):
        if signal_a < signal_b:
            responsive_a = responsive
        elif signal_b < signal_a:
            responsive_a = 0.0
        else:
            responsive_a = responsive / 2.0

        flexible_a = anchored_each + responsive_a
        flexible_b = flexible_total - flexible_a
        load_a = base_load_each + flexible_a
        load_b = base_load_each + flexible_b
        rows.append(
            PriceEpoch(
                epoch=epoch,
                signal_a=signal_a,
                signal_b=signal_b,
                flexible_a=flexible_a,
                load_a=load_a,
                load_b=load_b,
            )
        )

        # One-step-lag congestion price: next signal equals current load.
        signal_a = load_a
        signal_b = load_b

    return tuple(rows)


def oscillation_metrics(rows: tuple[PriceEpoch, ...]) -> dict[str, float]:
    if not rows:
        raise ValueError("rows must not be empty")
    peak = max(max(row.load_a, row.load_b) for row in rows)
    movement = sum(
        abs(rows[index].flexible_a - rows[index - 1].flexible_a)
        for index in range(1, len(rows))
    )
    return {
        "peak_load": peak,
        "flexible_movement": movement,
    }


def frozen_price_response() -> dict:
    full = simulate_lagged_price_response(responsive_fraction=1.0)
    damped = simulate_lagged_price_response(responsive_fraction=0.5)
    return {
        "full": full,
        "damped": damped,
        "full_metrics": oscillation_metrics(full),
        "damped_metrics": oscillation_metrics(damped),
    }
