from __future__ import annotations

from dataclasses import dataclass

from market_microcosm.dcre020_use_or_lose_uncertainty import frozen_demand_states


@dataclass(frozen=True)
class TelemetryOutcome:
    policy: str
    telemetry_accuracy: float | None
    expected_activation_resource: float
    expected_idle_capacity: float
    expected_unmet_demand: float
    expected_loss: float


def always_on(
    *,
    capacity_right: float = 60.0,
    activation_resource_per_capacity: float = 0.5,
    unmet_penalty: float = 2.0,
) -> TelemetryOutcome:
    activation = capacity_right * activation_resource_per_capacity
    expected_idle = sum(
        state.probability * max(0.0, 100.0 + capacity_right - state.demand)
        for state in frozen_demand_states()
    )
    return TelemetryOutcome(
        policy="ALWAYS_ON",
        telemetry_accuracy=None,
        expected_activation_resource=activation,
        expected_idle_capacity=expected_idle,
        expected_unmet_demand=0.0,
        expected_loss=activation,
    )


def telemetry_gated(
    accuracy: float,
    *,
    capacity_right: float = 60.0,
    activation_resource_per_capacity: float = 0.5,
    unmet_penalty: float = 2.0,
) -> TelemetryOutcome:
    if not 0.0 <= accuracy <= 1.0:
        raise ValueError("accuracy must be within [0, 1]")

    activation = 0.0
    idle = 0.0
    unmet = 0.0

    for state in frozen_demand_states():
        true_high = state.name == "HIGH"
        for signal_high, signal_probability in (
            (true_high, accuracy),
            (not true_high, 1.0 - accuracy),
        ):
            weight = state.probability * signal_probability
            deploy = capacity_right if signal_high else 0.0
            total_capacity = 100.0 + deploy
            activation += weight * deploy * activation_resource_per_capacity
            idle += weight * max(0.0, total_capacity - state.demand)
            unmet += weight * max(0.0, state.demand - total_capacity)

    return TelemetryOutcome(
        policy="TELEMETRY_GATED",
        telemetry_accuracy=accuracy,
        expected_activation_resource=activation,
        expected_idle_capacity=idle,
        expected_unmet_demand=unmet,
        expected_loss=activation + unmet_penalty * unmet,
    )


def telemetry_break_even_accuracy(
    *,
    capacity_right: float = 60.0,
    activation_resource_per_capacity: float = 0.5,
    unmet_penalty: float = 2.0,
) -> float:
    always = always_on(
        capacity_right=capacity_right,
        activation_resource_per_capacity=activation_resource_per_capacity,
        unmet_penalty=unmet_penalty,
    ).expected_loss
    # Symmetric two-state world:
    # gated loss = 0.5*C*activation_cost + 0.5*(1-q)*C*unmet_penalty.
    activation = 0.5 * capacity_right * activation_resource_per_capacity
    risk_scale = 0.5 * capacity_right * unmet_penalty
    return 1.0 - (always - activation) / risk_scale


def frozen_telemetry_value() -> dict[str, TelemetryOutcome | float]:
    return {
        "always_on": always_on(),
        "telemetry_060": telemetry_gated(0.60),
        "telemetry_080": telemetry_gated(0.80),
        "break_even_accuracy": telemetry_break_even_accuracy(),
    }
