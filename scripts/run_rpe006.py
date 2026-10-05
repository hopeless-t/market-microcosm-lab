import json
from pathlib import Path

from market_microcosm.research_portfolio_prewarm_dp import rpe006_report_payload


def main() -> None:
    payload = rpe006_report_payload()

    out = Path("artifacts/rpe006")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "bounded-prewarm-dp-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    suite = payload["suite"]
    print(path)
    print("summary=" + json.dumps({
        "exact_value_match_rate": suite["exact_value_match_rate"],
        "exact_selection_match_rate": suite["exact_selection_match_rate"],
        "aggregate_work_reduction_fraction": suite["aggregate_work_reduction_fraction"],
        "minimum_per_portfolio_work_reduction_fraction": suite["minimum_per_portfolio_work_reduction_fraction"],
    }, sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))


if __name__ == "__main__":
    main()
