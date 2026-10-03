from __future__ import annotations

from dataclasses import dataclass

from .ecological_evaluation import evaluate_mechanism
from .ecology import MarketWorld, Mechanism, default_mechanisms
from .pressure import pressure_ladder, world_at_pressure


@dataclass(frozen=True)
class EvaluationDesign:
    name: str
    pressure_levels: tuple[int, ...]
    discovery_seeds: tuple[int, ...]
    horizon: int


@dataclass(frozen=True)
class RobustMechanismScore:
    mechanism_name: str
    minimum_survival_rate: float
    mean_survival_rate: float
    mean_survival_months: float
    minimum_health: float
    mean_health: float
    mean_user_utility: float
    mean_active_developers: float

    @property
    def rank(self) -> tuple[float, float, float, float, float]:
        return (
            self.minimum_survival_rate,
            self.mean_survival_rate,
            self.mean_survival_months,
            self.minimum_health,
            self.mean_health,
        )


@dataclass(frozen=True)
class DesignResult:
    design_name: str
    selected_mechanism: str
    discovery_score: RobustMechanismScore
    meta_score: RobustMechanismScore
    search_cost: int


@dataclass(frozen=True)
class EvaluationDesignMetaResult:
    winner_design: str
    winner_mechanism: str
    results: tuple[DesignResult, ...]


def _points(levels: tuple[int, ...]):
    ladder = {point.level: point for point in pressure_ladder(max(levels))}
    return tuple(ladder[level] for level in levels)


def evaluate_robust_mechanism(
    *,
    base_world: MarketWorld,
    mechanism: Mechanism,
    pressure_levels: tuple[int, ...],
    seeds: tuple[int, ...],
    horizon: int,
) -> RobustMechanismScore:
    if not pressure_levels:
        raise ValueError("pressure_levels must not be empty")
    evaluations = []
    for point in _points(pressure_levels):
        evaluations.append(
            evaluate_mechanism(
                world_at_pressure(base_world, point),
                mechanism,
                seeds=seeds,
                horizon=horizon,
            )
        )

    n = len(evaluations)
    return RobustMechanismScore(
        mechanism_name=mechanism.name,
        minimum_survival_rate=min(x.survival_rate for x in evaluations),
        mean_survival_rate=sum(x.survival_rate for x in evaluations) / n,
        mean_survival_months=sum(x.mean_survival_months for x in evaluations) / n,
        minimum_health=min(x.mean_health for x in evaluations),
        mean_health=sum(x.mean_health for x in evaluations) / n,
        mean_user_utility=sum(x.mean_user_utility for x in evaluations) / n,
        mean_active_developers=sum(x.mean_active_developers for x in evaluations) / n,
    )


def default_evaluation_designs() -> tuple[EvaluationDesign, ...]:
    return (
        EvaluationDesign(
            "neutral-only",
            pressure_levels=(0,),
            discovery_seeds=tuple(range(9000, 9016)),
            horizon=60,
        ),
        EvaluationDesign(
            "mild-curriculum",
            pressure_levels=(0, 1, 2, 3),
            discovery_seeds=tuple(range(9100, 9116)),
            horizon=60,
        ),
        EvaluationDesign(
            "boundary-curriculum",
            pressure_levels=(1, 2, 3, 4, 5),
            discovery_seeds=tuple(range(9200, 9216)),
            horizon=60,
        ),
    )


def run_evaluation_design_meta(
    *,
    base_world: MarketWorld | None = None,
    mechanisms: tuple[Mechanism, ...] | None = None,
    designs: tuple[EvaluationDesign, ...] | None = None,
    meta_pressure_levels: tuple[int, ...] = (2, 3, 4, 5, 6),
    meta_seeds: tuple[int, ...] = tuple(range(12000, 12030)),
    meta_horizon: int = 72,
) -> EvaluationDesignMetaResult:
    base_world = base_world or MarketWorld()
    mechanisms = mechanisms or default_mechanisms()
    designs = designs or default_evaluation_designs()

    discovery_seed_union = {
        seed for design in designs for seed in design.discovery_seeds
    }
    if discovery_seed_union & set(meta_seeds):
        raise ValueError("meta seeds must be isolated from design discovery seeds")

    results: list[DesignResult] = []
    for design in designs:
        discovery_scores = tuple(
            evaluate_robust_mechanism(
                base_world=base_world,
                mechanism=mechanism,
                pressure_levels=design.pressure_levels,
                seeds=design.discovery_seeds,
                horizon=design.horizon,
            )
            for mechanism in mechanisms
        )
        selected = mechanisms[
            max(
                range(len(mechanisms)),
                key=lambda i: discovery_scores[i].rank,
            )
        ]
        discovery_score = next(
            x for x in discovery_scores if x.mechanism_name == selected.name
        )
        meta_score = evaluate_robust_mechanism(
            base_world=base_world,
            mechanism=selected,
            pressure_levels=meta_pressure_levels,
            seeds=meta_seeds,
            horizon=meta_horizon,
        )
        results.append(
            DesignResult(
                design_name=design.name,
                selected_mechanism=selected.name,
                discovery_score=discovery_score,
                meta_score=meta_score,
                search_cost=(
                    len(design.pressure_levels)
                    * len(design.discovery_seeds)
                    * len(mechanisms)
                    * design.horizon
                ),
            )
        )

    winner = max(
        results,
        key=lambda result: (
            result.meta_score.rank,
            -result.search_cost,
        ),
    )
    return EvaluationDesignMetaResult(
        winner_design=winner.design_name,
        winner_mechanism=winner.selected_mechanism,
        results=tuple(results),
    )
