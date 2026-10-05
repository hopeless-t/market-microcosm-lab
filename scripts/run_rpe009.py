import json
from pathlib import Path

from market_microcosm.research_portfolio_hazard_guard import rpe009_report_payload


def main() -> None:
    payload = rpe009_report_payload()

    out = Path("artifacts/rpe009")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "atom-hazard-channel-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("policies=" + json.dumps(payload["policies"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))


if __name__ == "__main__":
    main()
