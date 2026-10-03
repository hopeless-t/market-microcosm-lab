from dataclasses import asdict
import json
from pathlib import Path

from market_microcosm.ecological_evaluation import evaluate_mechanism
from market_microcosm.ecological_improvement import (
    MarketImprovementConfig,
    run_closed_market_improvement,
    run_market_meta_improvement,
)
from market_microcosm.ecology import MarketWorld, default_mechanisms


def main() -> None:
    world = MarketWorld()
    mechanisms = default_mechanisms()
    incumbent = mechanisms[0]

    baseline = [
        evaluate_mechanism(
            world,
            mechanism,
            seeds=tuple(range(5000, 5040)),
            horizon=60,
        )
        for mechanism in mechanisms
    ]
    closed = run_closed_market_improvement(
        world=world,
        incumbent=incumbent,
        config=MarketImprovementConfig(),
    )
    meta = run_market_meta_improvement(
        world=world,
        incumbent=closed.final,
    )

    payload = {
        "experiment": "E010",
        "world": "stylized-ecological-market-v1",
        "baseline": [asdict(x) | {"survival_lcb95": x.survival_lcb95} for x in baseline],
        "inner": {
            "initial": closed.initial.name,
            "final": closed.final.name,
            "converged": closed.converged,
            "generations": [
                {
                    "incumbent": g.incumbent.name,
                    "challenger": g.challenger.name,
                    "promoted": g.decision.promoted,
                    "reasons": list(g.decision.reasons),
                    "incumbent_holdout": asdict(g.incumbent_holdout),
                    "challenger_holdout": asdict(g.challenger_holdout),
                }
                for g in closed.generations
            ],
        },
        "meta": {
            "winner": meta.winner.name,
            "scores": [asdict(x) for x in meta.scores],
        },
    }

    out = Path("artifacts/e010")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print(f"inner-final={closed.final.name}")
    print(f"meta-winner={meta.winner.name}")


if __name__ == "__main__":
    main()
