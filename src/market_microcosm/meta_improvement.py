from __future__ import annotations

from dataclasses import dataclass, replace

from .evaluation import evaluate_policy
from .improvement import ImprovementConfig, ImprovementResult, run_improvement_loop
from .policies import PolicySpec
from .scenarios import generate_scenarios
from .toy_world import ToyWorld
from .viability import exact_robust_viability_kernel, oracle_action


@dataclass(frozen=True)
class MetaCandidate:
    name: str
    config: ImprovementConfig


@dataclass(frozen=True)
class MetaScore:
    candidate_name: str
    selected_policy: str
    promoted: bool
    meta_survival: float
    meta_welfare: float
    meta_minimum_reserve: float
    oracle_disagreement_rate: float
    search_cost: int

    @property
    def rank(self) -> tuple[float, float, float, float, int]:
        return (
            self.meta_survival,
            self.meta_minimum_reserve,
            self.meta_welfare,
            -self.oracle_disagreement_rate,
            -self.search_cost,
        )


@dataclass(frozen=True)
class MetaImprovementResult:
    winner: MetaCandidate
    scores: tuple[MetaScore, ...]
    inner_results: tuple[ImprovementResult, ...]
    meta_scenario_ids: tuple[str, ...]


@dataclass(frozen=True)
class ClosedMetaRun:
    initial_candidates: tuple[MetaCandidate, ...]
    final_winner: MetaCandidate
    generations: tuple[MetaImprovementResult, ...]
    converged: bool


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
    meta_seeds: tuple[int, ...] = tuple(range(1000, 1040)),
) -> MetaImprovementResult:
    candidates = candidates or default_meta_candidates()
    if not candidates:
        raise ValueError("meta candidate set must not be empty")

    used_inner_seeds = {
        seed
        for candidate in candidates
        for seed in candidate.config.discovery_seeds + candidate.config.promotion_seeds
    }
    if used_inner_seeds & set(meta_seeds):
        raise ValueError("meta seeds must be isolated from all inner-loop seeds")

    viability = exact_robust_viability_kernel(world)
    starts = tuple(sorted(viability.kernel))
    oracle = lambda s: oracle_action(world, viability, s)
    meta_scenarios = generate_scenarios(
        seeds=meta_seeds,
        horizon=max(c.config.horizon for c in candidates),
        initial_states=starts,
    )

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
        meta_eval = evaluate_policy(
            world,
            chosen,
            meta_scenarios,
            observation_mode=candidate.config.observation_mode,
            oracle=oracle,
        )
        scores.append(
            MetaScore(
                candidate_name=candidate.name,
                selected_policy=chosen.name,
                promoted=result.decision.promoted,
                meta_survival=meta_eval.survival_rate,
                meta_welfare=meta_eval.mean_welfare,
                meta_minimum_reserve=meta_eval.mean_minimum_reserve,
                oracle_disagreement_rate=meta_eval.oracle_disagreement_rate,
                search_cost=len(candidate.config.thresholds) * len(candidate.config.discovery_seeds),
            )
        )

    winner_index = max(range(len(candidates)), key=lambda i: scores[i].rank)
    return MetaImprovementResult(
        winner=candidates[winner_index],
        scores=tuple(scores),
        inner_results=tuple(inner_results),
        meta_scenario_ids=tuple(s.scenario_id for s in meta_scenarios),
    )


def mutate_meta_candidates(winner: MetaCandidate, generation: int) -> tuple[MetaCandidate, ...]:
    cfg = winner.config
    n = len(cfg.discovery_seeds)
    budgets = sorted({max(6, n - 4), n, n + 4})
    candidates: list[MetaCandidate] = []

    for budget in budgets:
        discovery = tuple(range(10_000 * generation, 10_000 * generation + budget))
        promotion = tuple(range(10_000 * generation + 1000, 10_000 * generation + 1030))
        candidates.append(
            MetaCandidate(
                f"g{generation}-{cfg.observation_mode}-b{budget}",
                replace(cfg, discovery_seeds=discovery, promotion_seeds=promotion),
            )
        )

    other_mode = "coarse" if cfg.observation_mode == "full" else "full"
    candidates.append(
        MetaCandidate(
            f"g{generation}-{other_mode}-b{n}",
            replace(
                cfg,
                observation_mode=other_mode,
                discovery_seeds=tuple(range(10_000 * generation + 2000, 10_000 * generation + 2000 + n)),
                promotion_seeds=tuple(range(10_000 * generation + 3000, 10_000 * generation + 3030)),
            ),
        )
    )
    return tuple(candidates)


def run_closed_meta_loop(
    *,
    world: ToyWorld,
    incumbent: PolicySpec,
    candidates: tuple[MetaCandidate, ...] | None = None,
    max_generations: int = 3,
) -> ClosedMetaRun:
    if max_generations < 1:
        raise ValueError("max_generations must be positive")

    current = candidates or default_meta_candidates()
    initial = current
    history: list[MetaImprovementResult] = []
    prior_signature: tuple[str, tuple[int, ...], int] | None = None
    converged = False
    winner = current[0]

    for generation in range(1, max_generations + 1):
        meta_seeds = tuple(range(900_000 + generation * 1000, 900_000 + generation * 1000 + 40))
        result = run_meta_improvement_loop(
            world=world,
            incumbent=incumbent,
            candidates=current,
            meta_seeds=meta_seeds,
        )
        history.append(result)
        winner = result.winner
        signature = (
            winner.config.observation_mode,
            winner.config.thresholds,
            len(winner.config.discovery_seeds),
        )
        if signature == prior_signature:
            converged = True
            break
        prior_signature = signature
        current = mutate_meta_candidates(winner, generation + 1)

    return ClosedMetaRun(
        initial_candidates=initial,
        final_winner=winner,
        generations=tuple(history),
        converged=converged,
    )
