from __future__ import annotations

from functools import lru_cache
from itertools import combinations
import random

from market_microcosm.research_portfolio_prewarm_scheduler import PrewarmJob, exact_oracle


HORIZON = 6
PORTFOLIO_COUNT = 32
JOBS_PER_PORTFOLIO = 10


def generated_portfolio(seed: int) -> tuple[PrewarmJob, ...]:
    rng = random.Random(seed)
    jobs: list[PrewarmJob] = []
    for index in range(JOBS_PER_PORTFOLIO):
        release = rng.randint(0, HORIZON - 2)
        max_window = HORIZON - release
        duration = rng.randint(1, min(2, max_window))
        deadline = rng.randint(release + duration, HORIZON)
        value = rng.randint(2, 20)
        jobs.append(
            PrewarmJob(
                name=f"J{index:02d}",
                release=release,
                deadline=deadline,
                duration=duration,
                value=value,
            )
        )
    return tuple(jobs)


def _placement_masks(job: PrewarmJob) -> tuple[int, ...]:
    masks: list[int] = []
    for slots in combinations(range(job.release, job.deadline), job.duration):
        mask = 0
        for slot in slots:
            mask |= 1 << slot
        masks.append(mask)
    return tuple(masks)


def bounded_dp(jobs: tuple[PrewarmJob, ...]) -> dict:
    ordered = tuple(sorted(jobs, key=lambda job: job.name))
    state_count = 0

    @lru_cache(maxsize=None)
    def solve(index: int, used_mask: int) -> tuple[int, int, tuple[str, ...]]:
        nonlocal state_count
        state_count += 1
        if index == len(ordered):
            return (0, 0, ())

        job = ordered[index]
        best = solve(index + 1, used_mask)
        for placement in _placement_masks(job):
            if placement & used_mask:
                continue
            suffix = solve(index + 1, used_mask | placement)
            candidate = (
                suffix[0] + job.value,
                suffix[1] - job.duration,
                tuple(sorted(suffix[2] + (job.name,))),
            )
            if candidate > best:
                best = candidate
        return best

    value, negative_duration, selected = solve(0, 0)
    return {
        "algorithm": "bounded-slot-mask-dp",
        "selected_names": list(selected),
        "total_value": value,
        "total_duration": -negative_duration,
        "work_units": state_count,
        "state_space_ceiling": (len(ordered) + 1) * (1 << HORIZON),
    }


def evaluate_generated_suite() -> dict:
    rows: list[dict] = []
    exact_match_count = 0
    selection_match_count = 0
    oracle_work = 0
    dp_work = 0
    minimum_reduction = 1.0

    for seed in range(1, PORTFOLIO_COUNT + 1):
        jobs = generated_portfolio(seed)
        oracle = exact_oracle(jobs)
        dp = bounded_dp(jobs)
        value_match = dp["total_value"] == oracle["total_value"]
        selection_match = dp["selected_names"] == sorted(oracle["selected"])
        exact_match_count += int(value_match)
        selection_match_count += int(selection_match)
        oracle_work += int(oracle["work_units"])
        dp_work += int(dp["work_units"])
        reduction = 1.0 - (int(dp["work_units"]) / int(oracle["work_units"]))
        minimum_reduction = min(minimum_reduction, reduction)
        rows.append(
            {
                "seed": seed,
                "oracle_value": oracle["total_value"],
                "dp_value": dp["total_value"],
                "value_match": value_match,
                "selection_match": selection_match,
                "oracle_work_units": oracle["work_units"],
                "dp_work_units": dp["work_units"],
                "work_reduction_fraction": reduction,
            }
        )

    return {
        "portfolio_count": PORTFOLIO_COUNT,
        "jobs_per_portfolio": JOBS_PER_PORTFOLIO,
        "horizon": HORIZON,
        "exact_value_match_rate": exact_match_count / PORTFOLIO_COUNT,
        "exact_selection_match_rate": selection_match_count / PORTFOLIO_COUNT,
        "oracle_work_units": oracle_work,
        "dp_work_units": dp_work,
        "aggregate_work_reduction_fraction": 1.0 - (dp_work / oracle_work),
        "minimum_per_portfolio_work_reduction_fraction": minimum_reduction,
        "rows": rows,
    }


def rpe006_report_payload() -> dict:
    suite = evaluate_generated_suite()
    gates = {
        "dp_matches_oracle_value_everywhere": suite["exact_value_match_rate"] == 1.0,
        "dp_matches_oracle_selection_everywhere": suite["exact_selection_match_rate"] == 1.0,
        "aggregate_work_reduction_at_least_60_percent": suite["aggregate_work_reduction_fraction"] >= 0.60,
        "every_portfolio_reduces_work_at_least_50_percent": suite["minimum_per_portfolio_work_reduction_fraction"] >= 0.50,
        "bounded_state_space_declared": all(
            row["dp_work_units"] <= (JOBS_PER_PORTFOLIO + 1) * (1 << HORIZON)
            for row in suite["rows"]
        ),
    }
    return {
        "experiment": "RPE-006",
        "title": "Bounded DP for finite prewarm scheduling",
        "suite": suite,
        "promotion_gate": gates,
        "candidate_scheduler": "bounded-slot-mask-dp",
        "claim_ceiling": "DETERMINISTIC_GENERATED_SMALL_WORLDS_ONLY_NO_SCALABLE_PRODUCTION_SCHEDULER_CLAIM",
    }
