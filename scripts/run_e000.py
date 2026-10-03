from pathlib import Path
import os

from market_microcosm.improvement import ImprovementConfig, run_closed_improvement_loop
from market_microcosm.meta_improvement import run_closed_meta_loop
from market_microcosm.policies import PolicySpec
from market_microcosm.report import closed_meta_json
from market_microcosm.toy_world import ToyWorld


def main() -> None:
    world = ToyWorld()
    incumbent = PolicySpec("incumbent-balanced", correction_threshold=99)
    revision = os.environ.get("GITHUB_SHA", "working-tree")

    inner = run_closed_improvement_loop(
        world=world,
        incumbent=incumbent,
        config=ImprovementConfig(),
        code_revision=revision,
    )
    meta = run_closed_meta_loop(
        world=world,
        incumbent=inner.final_policy,
        max_generations=3,
    )

    out = Path("artifacts/e000")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "meta-report.json"
    path.write_text(closed_meta_json(meta) + "\n", encoding="utf-8")

    print(path)
    print(f"inner-generations={len(inner.generations)}")
    print(f"inner-converged={inner.converged}")
    print(f"inner-final-policy={inner.final_policy.name}")
    print(f"meta-generations={len(meta.generations)}")
    print(f"meta-converged={meta.converged}")
    print(f"meta-winner={meta.final_winner.name}")


if __name__ == "__main__":
    main()
