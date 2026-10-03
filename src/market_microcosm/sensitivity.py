from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import random

from .ecological_evaluation import MarketEvaluation, evaluate_mechanism
from .ecology import MarketWorld, Mechanism


@dataclass(frozen=True)
class AxisPoint:
    axis: str
    level: int
    value: float


@dataclass(frozen=True)
class AxisResult:
    mechanism_name: str
    point: AxisPoint
    evaluation: MarketEvaluation


@dataclass(frozen=True)
class AxisFailureBiopsy:
    axis: str
    mechanism_name: str
    level: int
    value: float
    seed: int
    failed: bool
    failure_month: int | None
    failure_reasons: tuple[str, ...]
    trace: tuple[dict, ...]


SUPPORTED_AXES = (
    "subscription_price_multiplier",
    "platform_cost_multiplier",
    "base_churn_rate",
)


def axis_ladder(axis: str, max_level: int = 10) -> tuple[AxisPoint, ...]:
    if axis not in SUPPORTED_AXES:
        raise ValueError(f"unsupported axis: {axis}")

    points: list[AxisPoint] = []
    for level in range(max_level + 1):
        if axis == "subscription_price_multiplier":
            value = max(0.40, 1.0 - 0.06 * level)
        elif axis == "platform_cost_multiplier":
            value = 1.0 + 0.10 * level
        else:
            value = 0.020 + 0.0025 * level

        points.append(AxisPoint(axis=axis, level=level, value=value))
    return tuple(points)


def world_at_axis(base: MarketWorld, point: AxisPoint) -> MarketWorld:
    if point.axis == "subscription_price_multiplier":
        return replace(
            base,
            subscription_price=base.subscription_price * point.value,
        )
    if point.axis == "platform_cost_multiplier":
        return replace(
            base,
            platform_monthly_cost=base.platform_monthly_cost * point.value,
        )
    if point.axis == "base_churn_rate":
        return replace(base, base_churn_rate=point.value)
    raise ValueError(f"unsupported axis: {point.axis}")


def scan_axis(
    *,
    base_world: MarketWorld,
    mechanisms: tuple[Mechanism, ...],
    axis: str,
    points: tuple[AxisPoint, ...] | None = None,
    seeds: tuple[int, ...] = tuple(range(13000, 13020)),
    horizon: int = 60,
) -> tuple[AxisResult, ...]:
    points = points or axis_ladder(axis)
    results: list[AxisResult] = []
    for mechanism in mechanisms:
        for point in points:
            evaluation = evaluate_mechanism(
                world_at_axis(base_world, point),
                mechanism,
                seeds=seeds,
                horizon=horizon,
            )
            results.append(AxisResult(mechanism.name, point, evaluation))
    return tuple(results)


def axis_knee(
    results: tuple[AxisResult, ...],
    mechanism_name: str,
    axis: str,
    *,
    survival_threshold: float = 0.90,
) -> int | None:
    rows = sorted(
        (
            row
            for row in results
            if row.mechanism_name == mechanism_name and row.point.axis == axis
        ),
        key=lambda row: row.point.level,
    )
    for row in rows:
        if row.evaluation.survival_rate < survival_threshold:
            return row.point.level
    return None


def axis_auc(
    results: tuple[AxisResult, ...],
    mechanism_name: str,
    axis: str,
) -> float:
    rows = [
        row
        for row in results
        if row.mechanism_name == mechanism_name and row.point.axis == axis
    ]
    if not rows:
        return 0.0
    return sum(row.evaluation.survival_rate for row in rows) / len(rows)


def axis_failure_biopsy(
    *,
    base_world: MarketWorld,
    mechanism: Mechanism,
    point: AxisPoint,
    seeds: tuple[int, ...] = tuple(range(14000, 14040)),
    horizon: int = 60,
) -> AxisFailureBiopsy:
    world = world_at_axis(base_world, point)

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
                return AxisFailureBiopsy(
                    axis=point.axis,
                    mechanism_name=mechanism.name,
                    level=point.level,
                    value=point.value,
                    seed=seed,
                    failed=True,
                    failure_month=state.month,
                    failure_reasons=world.viability_failures(state),
                    trace=tuple(trace),
                )

    return AxisFailureBiopsy(
        axis=point.axis,
        mechanism_name=mechanism.name,
        level=point.level,
        value=point.value,
        seed=seeds[-1] if seeds else -1,
        failed=False,
        failure_month=None,
        failure_reasons=(),
        trace=(),
    )


def decomposition_report_payload(
    *,
    base_world: MarketWorld,
    mechanisms: tuple[Mechanism, ...],
    axes: tuple[str, ...] = SUPPORTED_AXES,
    seeds: tuple[int, ...] = tuple(range(13000, 13020)),
    biopsy_seeds: tuple[int, ...] = tuple(range(14000, 14040)),
    horizon: int = 60,
) -> dict:
    all_results: list[AxisResult] = []
    ladders: dict[str, tuple[AxisPoint, ...]] = {}

    for axis in axes:
        points = axis_ladder(axis)
        ladders[axis] = points
        all_results.extend(
            scan_axis(
                base_world=base_world,
                mechanisms=mechanisms,
                axis=axis,
                points=points,
                seeds=seeds,
                horizon=horizon,
            )
        )

    results = tuple(all_results)
    knees: dict[str, dict[str, int | None]] = {}
    resilience_auc: dict[str, dict[str, float]] = {}
    biopsies: list[dict] = []

    for axis in axes:
        knees[axis] = {
            mechanism.name: axis_knee(results, mechanism.name, axis)
            for mechanism in mechanisms
        }
        resilience_auc[axis] = {
            mechanism.name: axis_auc(results, mechanism.name, axis)
            for mechanism in mechanisms
        }

        for mechanism in mechanisms:
            knee = knees[axis][mechanism.name]
            level = knee if knee is not None else ladders[axis][-1].level
            point = next(p for p in ladders[axis] if p.level == level)
            biopsy = axis_failure_biopsy(
                base_world=base_world,
                mechanism=mechanism,
                point=point,
                seeds=biopsy_seeds,
                horizon=horizon,
            )
            biopsies.append(asdict(biopsy))

    return {
        "experiment": "E013",
        "question": "Which individual E011 pressure component causes which collapse mode?",
        "axes": {
            axis: [asdict(point) for point in ladders[axis]]
            for axis in axes
        },
        "knees": knees,
        "resilience_auc": resilience_auc,
        "curves": [
            {
                "axis": row.point.axis,
                "level": row.point.level,
                "value": row.point.value,
                "mechanism_name": row.mechanism_name,
                "survival_rate": row.evaluation.survival_rate,
                "survival_lcb95": row.evaluation.survival_lcb95,
                "mean_health": row.evaluation.mean_health,
                "mean_user_utility": row.evaluation.mean_user_utility,
                "mean_diversity": row.evaluation.mean_diversity,
                "mean_active_developers": row.evaluation.mean_active_developers,
                "mean_active_publishers": row.evaluation.mean_active_publishers,
                "mean_platform_cash": row.evaluation.mean_platform_cash,
                "mean_survival_months": row.evaluation.mean_survival_months,
                "total_entries": row.evaluation.total_entries,
                "total_exits": row.evaluation.total_exits,
            }
            for row in results
        ],
        "biopsies": biopsies,
    }
