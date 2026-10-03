from __future__ import annotations

from dataclasses import dataclass

from .improvement import ImprovementConfig, ImprovementResult, run_improvement_loop
from .policies import PolicySpec
from .toy_world import ToyWorld


@dataclass(frozen=True)
class MetaCandidate:
    name: str
    config: ImprovementConfig


@dataclass(frozen=True)
class MetaScore:
    candidate_name: str
    selected_policy: str
    promoted: bool
    holdout_survival: float
    holdout_welfare: float
    oracle_disagreement_rate: float
    search_cost: int

    @property
    def rank(self) -> tuple[float, float, float, int]:
        return (
            self.holdout_survival,
            self.holdout_welfare,
            -self.oracle_disagreement_rate,
            -self.search_cost,
        )


@dataclass(frozen=True)
class MetaImprovementResult:
    winner: MetaCandidate
    scores: tuple[MetaScore, ...]
    inner_results: tuple[ImprovementResult, ...]


def default_meta_candidates() -> tuple[MetaCandidate, ...]:
    return (
        MetaCandidate(
            "narrow-full",
            ImprovementConfig(
                observation_mode="full",
                thresholds=(1, 2),
                discovery_seeds=tuple(range(12)),
                promotion_seeds=tuple(range(100, 130)),
                horizon=20,
            ),
        ),
        MetaCandidate(
            "wide-full",
            ImprovementConfig(
                observation_mode="full",
                thresholds=(1, 2, 3),
                discovery_seeds=tuple(range(20)),
                promotion_seeds=tuple(range(100, 130)),
                horizon=20,
            ),
        ),
        MetaCandidate(
            "wide-coarse",
            ImprovementConfig(
                observation_mode="coarse",
                thresholds=(1, 2, 3),
                discovery_seeds=tuple(range(20)),
                promotion_seeds=tuple(range(100, 130)),
                horizon=20,
            ),
        ),
    )


def run_meta_improvement_loop(
    *,
    world: ToyWorld,
    incumbent: PolicySpec,
    candidates: tuple[MetaCandidate, ...] | None = None,
) -> MetaImprovementResult:
    candidates = candidates or default_meta_candidates()
    if not candidates:
        raise ValueError("meta candidate set must not be empty")

    inner_results: list[ImprovementResult] = []
    scores: list[MetaScore] = []

    for candidate in candidates:
        result = run_improvement_loop(
            world=world,
            incumbent=incumbent,
            config=candidate.config,
        )
        inner_results.append(result)
        chosen = result.challenger if result.decision.promoted else result.incumbent
        chosen_eval = result.challenger_holdout if result.decision.promoted else result.incumbent_holdout
        scores.append(
            MetaScore(
                candidate_name=candidate.name,
                selected_policy=chosen.name,
                promoted=result.decision.promoted,
                holdout_survival=chosen_eval.survival_rate,
                holdout_welfare=chosen_eval.mean_welfare,
                oracle_disagreement_rate=chosen_eval.oracle_disagreement_rate,
                search_cost=len(candidate.config.thresholds) * len(candidate.config.discovery_seeds),
            )
        )

    winner_index = max(range(len(candidates)), key=lambda i: scores[i].rank)
    return MetaImprovementResult(
        winner=candidates[winner_index],
        scores=tuple(scores),
        inner_results=tuple(inner_results),
    )
