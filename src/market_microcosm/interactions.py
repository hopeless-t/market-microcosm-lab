from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import random

from .ecological_evaluation import MarketEvaluation, evaluate_mechanism
from .ecology import MarketWorld, Mechanism
from .sensitivity import (
    SUPPORTED_AXES,
    AxisPoint,
    axis_ladder,
    world_at_axis,
)


PAIR_AXES = (
    ("subscription_price_multiplier", "platform_cost_multiplier"),
    ("subscription_price_multiplier", "base_churn_rate"),
    ("platform_cost_multiplier", "base_churn_rate"),
)


@dataclass(frozen=True)
class InteractionPoint:
    axis_a: str
    axis_b: str
    level_a: int
    level_b: int
    value_a: float
    value_b: float


@dataclass(frozen=True)
class InteractionResult:
    mechanism_name: str
    point: InteractionPoint
    evaluation: MarketEvaluation
    single_a_survival: float
    single_b_survival: float
    survival_loss_excess_over_max_single: float
    survival_loss_excess_over_additive: float
    interaction_only: bool


@dataclass(frozen=True)
class InteractionBiopsy:
    mechanism_name: str
    axis_a: str
    axis_b: str
    level_a: int
    level_b: int
    value_a: float
    value_b: float
    seed: int
    failed: bool
    failure_month: int | None
    failure_reasons: tuple[str, ...]
    trace: tuple[dict, ...]


def _axis_point(axis: str, level: int) -> AxisPoint:
    return axis_ladder(axis, max_level=level)[level]


def world_at_interaction(base: MarketWorld, point: InteractionPoint) -> MarketWorld:
    world = world_at_axis(
        base,
        AxisPoint(point.axis_a, point.level_a, point.value_a),
    )
    return world_at_axis(
        world,
        AxisPoint(point.axis_b, point.level_b, point.value_b),
    )


def interaction_grid(
    axis_a: str,
    axis_b: str,
    *,
    max_level: int = 6,
) -> tuple[InteractionPoint, ...]:
    if axis_a not in SUPPORTED_AXES or axis_b not in SUPPORTED_AXES:
        raise ValueError("unsupported interaction axis")
    if axis_a == axis_b:
        raise ValueError("interaction axes must differ")

    points: list[InteractionPoint] = []
    ladder_a = axis_ladder(axis_a, max_level=max_level)
    ladder_b = axis_ladder(axis_b, max_level=max_level)

    for point_a in ladder_a:
        for point_b in ladder_b:
            points.append(
                InteractionPoint(
                    axis_a=axis_a,
                    axis_b=axis_b,
                    level_a=point_a.level,
                    level_b=point_b.level,
                    value_a=point_a.value,
                    value_b=point_b.value,
                )
            )
    return tuple(points)


def _survival_loss(evaluation: MarketEvaluation) -> float:
    return 1.0 - evaluation.survival_rate


def scan_interaction_pair(
    *,
    base_world: MarketWorld,
    mechanisms: tuple[Mechanism, ...],
    axis_a: str,
    axis_b: str,
    max_level: int = 6,
    seeds: tuple[int, ...] = tuple(range(15000, 15012)),
    horizon: int = 60,
) -> tuple[InteractionResult, ...]:
    points = interaction_grid(axis_a, axis_b, max_level=max_level)

    single_a: dict[tuple[str, int], MarketEvaluation] = {}
    single_b: dict[tuple[str, int], MarketEvaluation] = {}

    for mechanism in mechanisms:
        for level in range(max_level + 1):
            point_a = _axis_point(axis_a, level)
            point_b = _axis_point(axis_b, level)
            single_a[(mechanism.name, level)] = evaluate_mechanism(
                world_at_axis(base_world, point_a),
                mechanism,
                seeds=seeds,
                horizon=horizon,
            )
            single_b[(mechanism.name, level)] = evaluate_mechanism(
                world_at_axis(base_world, point_b),
                mechanism,
                seeds=seeds,
                horizon=horizon,
            )

    results: list[InteractionResult] = []
    for mechanism in mechanisms:
        for point in points:
            pair_eval = evaluate_mechanism(
                world_at_interaction(base_world, point),
                mechanism,
                seeds=seeds,
                horizon=horizon,
            )
            eval_a = single_a[(mechanism.name, point.level_a)]
            eval_b = single_b[(mechanism.name, point.level_b)]

            pair_loss = _survival_loss(pair_eval)
            loss_a = _survival_loss(eval_a)
            loss_b = _survival_loss(eval_b)
            excess_max = pair_loss - max(loss_a, loss_b)
            excess_additive = pair_loss - min(1.0, loss_a + loss_b)

            results.append(
                InteractionResult(
                    mechanism_name=mechanism.name,
                    point=point,
                    evaluation=pair_eval,
                    single_a_survival=eval_a.survival_rate,
                    single_b_survival=eval_b.survival_rate,
                    survival_loss_excess_over_max_single=excess_max,
                    survival_loss_excess_over_additive=excess_additive,
                    interaction_only=(
                        pair_eval.survival_rate < 0.90
                        and eval_a.survival_rate >= 0.90
                        and eval_b.survival_rate >= 0.90
                    ),
                )
            )

    return tuple(results)


def first_interaction_frontier(
    results: tuple[InteractionResult, ...],
    *,
    mechanism_name: str,
    axis_a: str,
    axis_b: str,
    survival_threshold: float = 0.90,
) -> InteractionResult | None:
    failing = [
        row
        for row in results
        if row.mechanism_name == mechanism_name
        and row.point.axis_a == axis_a
        and row.point.axis_b == axis_b
        and row.evaluation.survival_rate < survival_threshold
    ]
    if not failing:
        return None
    return min(
        failing,
        key=lambda row: (
            row.point.level_a + row.point.level_b,
            max(row.point.level_a, row.point.level_b),
            abs(row.point.level_a - row.point.level_b),
            row.point.level_a,
            row.point.level_b,
        ),
    )


def interaction_biopsy(
    *,
    base_world: MarketWorld,
    mechanism: Mechanism,
    point: InteractionPoint,
    seeds: tuple[int, ...] = tuple(range(16000, 16040)),
    horizon: int = 60,
) -> InteractionBiopsy:
    world = world_at_interaction(base_world, point)

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
                return InteractionBiopsy(
                    mechanism_name=mechanism.name,
                    axis_a=point.axis_a,
                    axis_b=point.axis_b,
                    level_a=point.level_a,
                    level_b=point.level_b,
                    value_a=point.value_a,
                    value_b=point.value_b,
                    seed=seed,
                    failed=True,
                    failure_month=state.month,
                    failure_reasons=world.viability_failures(state),
                    trace=tuple(trace),
                )

    return InteractionBiopsy(
        mechanism_name=mechanism.name,
        axis_a=point.axis_a,
        axis_b=point.axis_b,
        level_a=point.level_a,
        level_b=point.level_b,
        value_a=point.value_a,
        value_b=point.value_b,
        seed=seeds[-1] if seeds else -1,
        failed=False,
        failure_month=None,
        failure_reasons=(),
        trace=(),
    )


def interaction_report_payload(
    *,
    base_world: MarketWorld,
    mechanisms: tuple[Mechanism, ...],
    pairs: tuple[tuple[str, str], ...] = PAIR_AXES,
    max_level: int = 6,
    seeds: tuple[int, ...] = tuple(range(15000, 15012)),
    biopsy_seeds: tuple[int, ...] = tuple(range(16000, 16040)),
    horizon: int = 60,
) -> dict:
    all_results: list[InteractionResult] = []

    for axis_a, axis_b in pairs:
        all_results.extend(
            scan_interaction_pair(
                base_world=base_world,
                mechanisms=mechanisms,
                axis_a=axis_a,
                axis_b=axis_b,
                max_level=max_level,
                seeds=seeds,
                horizon=horizon,
            )
        )

    results = tuple(all_results)
    summaries: dict[str, dict[str, dict]] = {}
    biopsies: list[dict] = []

    for axis_a, axis_b in pairs:
        pair_key = f"{axis_a}__{axis_b}"
        summaries[pair_key] = {}

        for mechanism in mechanisms:
            rows = [
                row
                for row in results
                if row.mechanism_name == mechanism.name
                and row.point.axis_a == axis_a
                and row.point.axis_b == axis_b
            ]
            frontier = first_interaction_frontier(
                results,
                mechanism_name=mechanism.name,
                axis_a=axis_a,
                axis_b=axis_b,
            )
            interaction_only = [row for row in rows if row.interaction_only]
            max_excess = max(
                (row.survival_loss_excess_over_additive for row in rows),
                default=0.0,
            )
            max_excess_over_single = max(
                (row.survival_loss_excess_over_max_single for row in rows),
                default=0.0,
            )

            summaries[pair_key][mechanism.name] = {
                "frontier": (
                    {
                        "level_a": frontier.point.level_a,
                        "level_b": frontier.point.level_b,
                        "level_sum": frontier.point.level_a + frontier.point.level_b,
                        "survival_rate": frontier.evaluation.survival_rate,
                        "single_a_survival": frontier.single_a_survival,
                        "single_b_survival": frontier.single_b_survival,
                        "interaction_only": frontier.interaction_only,
                    }
                    if frontier
                    else None
                ),
                "interaction_only_cells": len(interaction_only),
                "max_survival_loss_excess_over_max_single": max_excess_over_single,
                "max_survival_loss_excess_over_additive": max_excess,
            }

            if frontier is not None:
                biopsy = interaction_biopsy(
                    base_world=base_world,
                    mechanism=mechanism,
                    point=frontier.point,
                    seeds=biopsy_seeds,
                    horizon=horizon,
                )
                biopsies.append(asdict(biopsy))

    return {
        "experiment": "E014",
        "question": "Where do pairwise pressure interactions advance collapse beyond single-axis stress?",
        "grid_max_level": max_level,
        "pairs": [list(pair) for pair in pairs],
        "summaries": summaries,
        "cells": [
            {
                "mechanism_name": row.mechanism_name,
                "axis_a": row.point.axis_a,
                "axis_b": row.point.axis_b,
                "level_a": row.point.level_a,
                "level_b": row.point.level_b,
                "value_a": row.point.value_a,
                "value_b": row.point.value_b,
                "survival_rate": row.evaluation.survival_rate,
                "survival_lcb95": row.evaluation.survival_lcb95,
                "mean_survival_months": row.evaluation.mean_survival_months,
                "mean_health": row.evaluation.mean_health,
                "single_a_survival": row.single_a_survival,
                "single_b_survival": row.single_b_survival,
                "survival_loss_excess_over_max_single": (
                    row.survival_loss_excess_over_max_single
                ),
                "survival_loss_excess_over_additive": (
                    row.survival_loss_excess_over_additive
                ),
                "interaction_only": row.interaction_only,
            }
            for row in results
        ],
        "biopsies": biopsies,
    }
