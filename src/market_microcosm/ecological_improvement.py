from __future__ import annotations

from dataclasses import dataclass, replace

from .ecological_evaluation import MarketEvaluation, evaluate_mechanism
from .ecology import MarketWorld, Mechanism, default_mechanisms


@dataclass(frozen=True)
class MarketPromotionRule:
    minimum_survival_lcb95: float = 0.80
    maximum_user_utility_drop: float = 0.01
    maximum_active_developer_drop: float = 0.05
    minimum_health_gain: float = 0.002
    maximum_invariant_violations: int = 0


@dataclass(frozen=True)
class MarketPromotionDecision:
    promoted: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class MarketImprovementConfig:
    discovery_seeds: tuple[int, ...] = tuple(range(2000, 2020))
    promotion_seeds: tuple[int, ...] = tuple(range(3000, 3040))
    horizon: int = 48
    mechanisms: tuple[Mechanism, ...] = default_mechanisms()

    def __post_init__(self) -> None:
        if set(self.discovery_seeds) & set(self.promotion_seeds):
            raise ValueError("discovery and promotion seeds must be disjoint")
        if not self.mechanisms:
            raise ValueError("at least one mechanism is required")


@dataclass(frozen=True)
class MarketImprovementResult:
    incumbent: Mechanism
    challenger: Mechanism
    discovery_scores: tuple[MarketEvaluation, ...]
    incumbent_holdout: MarketEvaluation
    challenger_holdout: MarketEvaluation
    decision: MarketPromotionDecision


@dataclass(frozen=True)
class ClosedMarketImprovement:
    initial: Mechanism
    final: Mechanism
    generations: tuple[MarketImprovementResult, ...]
    converged: bool


def verify_market_promotion(
    incumbent: MarketEvaluation,
    challenger: MarketEvaluation,
    rule: MarketPromotionRule,
) -> MarketPromotionDecision:
    reasons: list[str] = []
    if incumbent.mechanism_name == challenger.mechanism_name:
        reasons.append("challenger is identical to incumbent")
    if challenger.invariant_violations > rule.maximum_invariant_violations:
        reasons.append("hard accounting invariant violated")
    if challenger.survival_lcb95 < rule.minimum_survival_lcb95:
        reasons.append("survival confidence bound below required floor")
    if challenger.survived < incumbent.survived:
        reasons.append("protected survival count degraded")
    if (
        challenger.mean_user_utility
        < incumbent.mean_user_utility - rule.maximum_user_utility_drop
    ):
        reasons.append("user utility degraded beyond tolerance")
    if (
        challenger.mean_active_developers
        < incumbent.mean_active_developers - rule.maximum_active_developer_drop
    ):
        reasons.append("developer viability degraded beyond tolerance")
    if challenger.mean_health < incumbent.mean_health + rule.minimum_health_gain:
        reasons.append("insufficient ecosystem-health improvement")
    return MarketPromotionDecision(not reasons, tuple(reasons))


def _rank(evaluation: MarketEvaluation) -> tuple[float, float, float, float, float]:
    return (
        evaluation.survival_rate,
        evaluation.mean_health,
        evaluation.mean_user_utility,
        evaluation.mean_diversity,
        evaluation.mean_active_developers,
    )


def run_market_improvement(
    *,
    world: MarketWorld,
    incumbent: Mechanism,
    config: MarketImprovementConfig,
    rule: MarketPromotionRule | None = None,
) -> MarketImprovementResult:
    rule = rule or MarketPromotionRule()
    discovery_scores = tuple(
        evaluate_mechanism(
            world,
            mechanism,
            seeds=config.discovery_seeds,
            horizon=config.horizon,
        )
        for mechanism in config.mechanisms
    )
    challenger = config.mechanisms[
        max(range(len(config.mechanisms)), key=lambda i: _rank(discovery_scores[i]))
    ]

    incumbent_holdout = evaluate_mechanism(
        world,
        incumbent,
        seeds=config.promotion_seeds,
        horizon=config.horizon,
    )
    challenger_holdout = evaluate_mechanism(
        world,
        challenger,
        seeds=config.promotion_seeds,
        horizon=config.horizon,
    )
    decision = verify_market_promotion(
        incumbent_holdout,
        challenger_holdout,
        rule,
    )
    return MarketImprovementResult(
        incumbent=incumbent,
        challenger=challenger,
        discovery_scores=discovery_scores,
        incumbent_holdout=incumbent_holdout,
        challenger_holdout=challenger_holdout,
        decision=decision,
    )


def run_closed_market_improvement(
    *,
    world: MarketWorld,
    incumbent: Mechanism,
    config: MarketImprovementConfig,
    max_generations: int = 6,
) -> ClosedMarketImprovement:
    if max_generations < 1:
        raise ValueError("max_generations must be positive")
    initial = incumbent
    history: list[MarketImprovementResult] = []
    converged = False

    for _ in range(max_generations):
        result = run_market_improvement(
            world=world,
            incumbent=incumbent,
            config=config,
        )
        history.append(result)
        if not result.decision.promoted:
            converged = True
            break
        incumbent = result.challenger

    return ClosedMarketImprovement(
        initial=initial,
        final=incumbent,
        generations=tuple(history),
        converged=converged,
    )


@dataclass(frozen=True)
class MarketMetaCandidate:
    name: str
    config: MarketImprovementConfig


@dataclass(frozen=True)
class MarketMetaScore:
    candidate_name: str
    selected_mechanism: str
    meta_survival_rate: float
    meta_survival_lcb95: float
    meta_health: float
    meta_user_utility: float
    meta_diversity: float
    search_cost: int

    @property
    def rank(self) -> tuple[float, float, float, float, int]:
        return (
            self.meta_survival_lcb95,
            self.meta_health,
            self.meta_user_utility,
            self.meta_diversity,
            -self.search_cost,
        )


@dataclass(frozen=True)
class MarketMetaResult:
    winner: MarketMetaCandidate
    scores: tuple[MarketMetaScore, ...]


def default_market_meta_candidates() -> tuple[MarketMetaCandidate, ...]:
    mechanisms = default_mechanisms()
    return (
        MarketMetaCandidate(
            "short-wide",
            MarketImprovementConfig(
                discovery_seeds=tuple(range(2000, 2016)),
                promotion_seeds=tuple(range(3000, 3030)),
                horizon=36,
                mechanisms=mechanisms,
            ),
        ),
        MarketMetaCandidate(
            "long-wide",
            MarketImprovementConfig(
                discovery_seeds=tuple(range(2100, 2120)),
                promotion_seeds=tuple(range(3100, 3140)),
                horizon=60,
                mechanisms=mechanisms,
            ),
        ),
        MarketMetaCandidate(
            "long-compact",
            MarketImprovementConfig(
                discovery_seeds=tuple(range(2200, 2212)),
                promotion_seeds=tuple(range(3200, 3230)),
                horizon=60,
                mechanisms=mechanisms[:4],
            ),
        ),
    )


def run_market_meta_improvement(
    *,
    world: MarketWorld,
    incumbent: Mechanism,
    candidates: tuple[MarketMetaCandidate, ...] | None = None,
    meta_seeds: tuple[int, ...] = tuple(range(4000, 4040)),
) -> MarketMetaResult:
    candidates = candidates or default_market_meta_candidates()
    used = {
        seed
        for candidate in candidates
        for seed in candidate.config.discovery_seeds
        + candidate.config.promotion_seeds
    }
    if used & set(meta_seeds):
        raise ValueError("meta seeds must be isolated from inner-loop seeds")

    scores: list[MarketMetaScore] = []
    for candidate in candidates:
        result = run_closed_market_improvement(
            world=world,
            incumbent=incumbent,
            config=candidate.config,
        )
        meta_eval = evaluate_mechanism(
            world,
            result.final,
            seeds=meta_seeds,
            horizon=candidate.config.horizon,
        )
        scores.append(
            MarketMetaScore(
                candidate_name=candidate.name,
                selected_mechanism=result.final.name,
                meta_survival_rate=meta_eval.survival_rate,
                meta_survival_lcb95=meta_eval.survival_lcb95,
                meta_health=meta_eval.mean_health,
                meta_user_utility=meta_eval.mean_user_utility,
                meta_diversity=meta_eval.mean_diversity,
                search_cost=(
                    len(candidate.config.discovery_seeds)
                    * len(candidate.config.mechanisms)
                    * candidate.config.horizon
                ),
            )
        )

    winner_index = max(range(len(candidates)), key=lambda i: scores[i].rank)
    return MarketMetaResult(candidates[winner_index], tuple(scores))
