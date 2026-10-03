from pathlib import Path

from market_microcosm.meta_improvement import run_meta_improvement_loop
from market_microcosm.policies import PolicySpec
from market_microcosm.report import meta_result_json
from market_microcosm.toy_world import ToyWorld


def main() -> None:
    world = ToyWorld()
    incumbent = PolicySpec("incumbent-balanced", correction_threshold=99)
    result = run_meta_improvement_loop(world=world, incumbent=incumbent)
    out = Path("artifacts/e000")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "meta-report.json"
    path.write_text(meta_result_json(result) + "\n", encoding="utf-8")
    print(path)
    print(f"meta-winner={result.winner.name}")


if __name__ == "__main__":
    main()
