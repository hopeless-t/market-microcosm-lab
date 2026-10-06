import json
from pathlib import Path

from market_microcosm.research_portfolio_observation_common_mode import rpe010_report_payload


def main() -> None:
    payload = rpe010_report_payload()

    out = Path("artifacts/rpe010")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "observation-common-mode-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("comparison=" + json.dumps(payload["comparison"], sort_keys=True))
    print("policies=" + json.dumps(payload["policies"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))


if __name__ == "__main__":
    main()
