import json
from pathlib import Path

from market_microcosm.research_portfolio_prewarm_scheduler import rpe005_report_payload


def main() -> None:
    payload = rpe005_report_payload()

    out = Path("artifacts/rpe005")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "finite-prewarm-scheduler-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("deadline=" + json.dumps(payload["portfolios"]["deadline_trap"], sort_keys=True))
    print("density=" + json.dumps(payload["portfolios"]["density_trap"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))


if __name__ == "__main__":
    main()
