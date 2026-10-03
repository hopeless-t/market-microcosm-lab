from dataclasses import asdict
import json
from pathlib import Path

from market_microcosm.robust_search import run_evaluation_design_meta


def main() -> None:
    result = run_evaluation_design_meta()
    payload = {
        "experiment": "E012",
        "question": "Which evaluation curriculum selects the most robust mechanism?",
        "winner_design": result.winner_design,
        "winner_mechanism": result.winner_mechanism,
        "results": [
            {
                "design_name": x.design_name,
                "selected_mechanism": x.selected_mechanism,
                "search_cost": x.search_cost,
                "discovery_score": asdict(x.discovery_score),
                "meta_score": asdict(x.meta_score),
            }
            for x in result.results
        ],
    }

    out = Path("artifacts/e012")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "evaluation-design-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print(
        "design-selection="
        + json.dumps(
            {
                x.design_name: x.selected_mechanism
                for x in result.results
            },
            sort_keys=True,
        )
    )
    print(f"winner-design={result.winner_design}")
    print(f"winner-mechanism={result.winner_mechanism}")


if __name__ == "__main__":
    main()
