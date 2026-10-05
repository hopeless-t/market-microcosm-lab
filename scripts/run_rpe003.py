import json
from pathlib import Path

from market_microcosm.research_portfolio_residency import rpe003_report_payload


def main() -> None:
    payload = rpe003_report_payload()

    out = Path("artifacts/rpe003")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "curiosity-residency-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("comparison=" + json.dumps(payload["comparison"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))
    print(f"candidate-rule={payload['candidate_rule']}")


if __name__ == "__main__":
    main()
