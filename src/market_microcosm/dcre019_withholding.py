from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WithholdingChoice:
    deploy: float
    withheld: float
    unmet_demand: float
    market_price: float
    gross_revenue: float
    withholding_penalty: float
    net_revenue: float


def evaluate_deployment(
    deploy: float,
    *,
    right_capacity: float = 60.0,
    baseline_capacity: float = 100.0,
    demand: float = 160.0,
    base_price: float = 1.0,
    scarcity_markup_per_unmet: float = 0.03,
    penalty_per_withheld: float = 0.0,
) -> WithholdingChoice:
    if not 0.0 <= deploy <= right_capacity:
        raise ValueError("deploy must be within capacity right")
    withheld = right_capacity - deploy
    total_capacity = baseline_capacity + deploy
    unmet = max(0.0, demand - total_capacity)
    market_price = base_price + scarcity_markup_per_unmet * unmet
    gross = deploy * market_price
    penalty = penalty_per_withheld * withheld
    return WithholdingChoice(
        deploy=deploy,
        withheld=withheld,
        unmet_demand=unmet,
        market_price=market_price,
        gross_revenue=gross,
        withholding_penalty=penalty,
        net_revenue=gross - penalty,
    )


def choose_deployment(*, penalty_per_withheld: float = 0.0) -> WithholdingChoice:
    choices = tuple(
        evaluate_deployment(
            deploy,
            penalty_per_withheld=penalty_per_withheld,
        )
        for deploy in (0.0, 20.0, 40.0, 60.0)
    )
    return max(choices, key=lambda row: (row.net_revenue, row.deploy))


def frozen_withholding() -> dict[str, WithholdingChoice]:
    return {
        "unconstrained": choose_deployment(penalty_per_withheld=0.0),
        "use_or_lose": choose_deployment(penalty_per_withheld=0.25),
    }
