from __future__ import annotations

from dataclasses import dataclass

from .evaluation import Evaluation, evaluate_policy
from .policies import PolicySpec, candidate_family
from .scenarios import generate_scenarios
from .toy_world import ToyWorld
from .verifier import PromotionDecision, PromotionRule, verify_promotion
from .viability import ViabilityResult, exact_robust_viability_kernel, oracle_action


@dataclass(frozen=True)
class ImprovementConfig:
    observation_mode: str = "full"
    thresholds: tuple[int, ...] = (1, 2, 3)
    discovery_seeds: tuple[int, ...] = tuple(range(20))
    promotion_seeds: tuple[int, ...] = tuple(range(100, 140))
    horizon: int = 20

    def __post_init__(self) -> None:
        if set(self.discovery_seeds) & set(self.promotion_seeds):
            raise ValueError("discovery and promotion seeds must be disjoint")


@dataclass(frozen=True)
class ImprovementResult:
    incumbent: PolicySpec
    challenger: PolicySpec
    discovery_scores: tuple[Evaluation, ...]
    incumbent_holdout: Evaluation
    challenger_holdout: Evaluation
    decision: PromotionDecision
    viability: ViabilityResult


def _rank(e: Evaluation) -> tuple[float, float, float]:
    return (e.survival_rate, e.mean_minimum_reserve, e.mean_welfare)


def run_improvement_loop(
    *,
    world: ToyWorld,
    incumbent: PolicySpec,
    config: ImprovementConfig,
    rule: PromotionRule | None = None,
) -> ImprovementResult:
    rule = rule or PromotionRule()
    viability = exact_robust_viability_kernel(world)
    starts = tuple(sorted(viability.kernel))
    if not starts:
        raise RuntimeError("toy world has empty robust viability kernel")

    oracle = lambda s: oracle_action(world, viability, s)

    discovery = generate_scenarios(
        seeds=config.discovery_seeds,
        horizon=config.horizon,
        initial_states=starts,
    )
    candidates = candidate_family(config.thresholds)
    scores = tuple(
        evaluate_policy(world, p, discovery, observation_mode=config.observation_mode, oracle=oracle)
        for p in candidates
    )
    challenger = candidates[max(range(len(candidates)), key=lambda i: _rank(scores[i]))]

    holdout = generate_scenarios(
        seeds=config.promotion_seeds,
        horizon=config.horizon,
        initial_states=starts,
    )
    incumbent_eval = evaluate_policy(
        world, incumbent, holdout, observation_mode=config.observation_mode, oracle=oracle
    )
    challenger_eval = evaluate_policy(
        world, challenger, holdout, observation_mode=config.observation_mode, oracle=oracle
    )
    decision = verify_promotion(incumbent_eval, challenger_eval, rule)

    return ImprovementResult(
        incumbent=incumbent,
        challenger=challenger,
        discovery_scores=scores,
        incumbent_holdout=incumbent_eval,
        challenger_holdout=challenger_eval,
        decision=decision,
        viability=viability,
    )
