from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import random

from .ecological_evaluation import MarketEvaluation, evaluate_mechanism
from .ecology import MarketWorld, Mechanism


@dataclass(frozen=True)
class PressurePoint:
    level: int
    price_multiplier: float
    platform_cost_multiplier: float
    base_churn_rate: float


@dataclass(frozen=True)
class PressureResult:
    mechanism_name: str
    point: PressurePoint
    evaluation: MarketEvaluation


@dataclass(frozen=True)
class FailureBiopsy:
    mechanism_name: str
    pressure_level: int
    seed: int
    failed: bool
    failure_month: int | None
    trace: tuple[dict, ...]


def pressure_ladder(max_level: int = 10) -> tuple[PressurePoint, ...]:
    points: list[PressurePoint] = []
    for level in range(max_level + 1):
        points.append(
            PressurePoint(
                level=level,
                price_multiplier=max(0.40, 1.0 - 0.06 * level),
                platform_cost_multiplier=1.0 + 0.10 * level,
                base_churn_rate=0.020 + 0.0025 * level,
            )
        )
    return tuple(points)


def world_at_pressure(base: MarketWorld, point: PressurePoint) -> MarketWorld:
    return replace(
        base,
        subscription_price=base.subscription_price * point.price_multiplier,
        platform_monthly_cost=(
            base.platform_monthly_cost * point.platform_cost_multiplier
        ),
        base_churn_rate=point.base_churn_rate,
    )


def scan_pressure(
    *,
    base_world: MarketWorld,
    mechanisms: tuple[Mechanism, ...],
    points: tuple[PressurePoint, ...] | None = None,
    seeds: tuple[int, ...] = tuple(range(7000, 7020)),
    horizon: int = 60,
) -> tuple[PressureResult, ...]:
    points = points or pressure_ladder()
    results: list[PressureResult] = []
    for mechanism in mechanisms:
        for point in points:
            world = world_at_pressure(base_world, point)
            evaluation = evaluate_mechanism(
                world,
                mechanism,
                seeds=seeds,
                horizon=horizon,
            )
            results.append(PressureResult(mechanism.name, point, evaluation))
    return tuple(results)


def pressure_knee(
    results: tuple[PressureResult, ...],
    mechanism_name: str,
    *,
    survival_threshold: float = 0.90,
) -> int | None:
    rows = sorted(
        (x for x in results if x.mechanism_name == mechanism_name),
        key=lambda x: x.point.level,
    )
    for row in rows:
        if row.evaluation.survival_rate < survival_threshold:
            return row.point.level
    return None


def failure_biopsy(
    *,
    base_world: MarketWorld,
    mechanism: Mechanism,
    point: PressurePoint,
    seeds: tuple[int, ...] = tuple(range(8000, 8040)),
    horizon: int = 60,
) -> FailureBiopsy:
    world = world_at_pressure(base_world, point)

    for seed in seeds:
        rng = random.Random(seed)
        state = world.initial_state()
        trace: list[dict] = []

        for _ in range(horizon):
            result = world.step(state, mechanism, rng)
            state = result.state
            metrics = result.metrics
            trace.append(
                {
                    "month": state.month,
                    "user_utility": metrics.user_utility,
                    "diversity": metrics.diversity,
                    "active_developers": metrics.active_developers,
                    "active_publishers": metrics.active_publishers,
                    "total_users": metrics.total_users,
                    "platform_cash": metrics.platform_cash,
                    "health": metrics.health,
                    "entries": state.cumulative_entries,
                    "exits": state.cumulative_exits,
                    "conservation_error": result.audit.conservation_error,
                }
            )
            if not world.viable(state):
                return FailureBiopsy(
                    mechanism_name=mechanism.name,
                    pressure_level=point.level,
                    seed=seed,
                    failed=True,
                    failure_month=state.month,
                    trace=tuple(trace),
                )

    return FailureBiopsy(
        mechanism_name=mechanism.name,
        pressure_level=point.level,
        seed=seeds[-1] if seeds else -1,
        failed=False,
        failure_month=None,
        trace=(),
    )


def pressure_report_payload(
    *,
    results: tuple[PressureResult, ...],
    mechanisms: tuple[Mechanism, ...],
    points: tuple[PressurePoint, ...],
) -> dict:
    knees = {
        mechanism.name: pressure_knee(results, mechanism.name)
        for mechanism in mechanisms
    }
    biopsies: list[dict] = []

    for mechanism in mechanisms:
        knee = knees[mechanism.name]
        biopsy_level = knee if knee is not None else points[-1].level
        point = next(x for x in points if x.level == biopsy_level)
        biopsy = failure_biopsy(
            base_world=MarketWorld(),
            mechanism=mechanism,
            point=point,
        )
        biopsies.append(asdict(biopsy))

    return {
        "experiment": "E011",
        "pressure_definition": [
            asdict(point) for point in points
        ],
        "knees": knees,
        "curves": [
            {
                "mechanism_name": row.mechanism_name,
                "pressure_level": row.point.level,
                "survival_rate": row.evaluation.survival_rate,
                "survival_lcb95": row.evaluation.survival_lcb95,
                "mean_health": row.evaluation.mean_health,
                "mean_user_utility": row.evaluation.mean_user_utility,
                "mean_diversity": row.evaluation.mean_diversity,
                "mean_active_developers": row.evaluation.mean_active_developers,
                "mean_platform_cash": row.evaluation.mean_platform_cash,
                "total_entries": row.evaluation.total_entries,
                "total_exits": row.evaluation.total_exits,
            }
            for row in results
        ],
        "biopsies": biopsies,
    }
