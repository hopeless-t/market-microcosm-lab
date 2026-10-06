import json
from pathlib import Path

from market_microcosm.research_portfolio_real_fanout import rpe011_report_payload


def main() -> None:
    payload = rpe011_report_payload()

    out = Path("artifacts/rpe011")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "observed-strata-fanout-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("observed=" + json.dumps(payload["observed"], sort_keys=True))
    print("counterfactual=" + json.dumps(payload["counterfactual_envelope"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))


if __name__ == "__main__":
    main()
