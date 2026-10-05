import json
from pathlib import Path

from market_microcosm.research_portfolio_reobservation import rpe007_report_payload


def main() -> None:
    payload = rpe007_report_payload()

    out = Path("artifacts/rpe007")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "stale-reobservation-replan-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("stale-event=" + json.dumps(payload["stale_event"], sort_keys=True))
    print("policies=" + json.dumps(payload["policies"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))


if __name__ == "__main__":
    main()
