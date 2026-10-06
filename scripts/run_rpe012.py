import json
from pathlib import Path

from market_microcosm.research_portfolio_projection_maturity import rpe012_report_payload


def main() -> None:
    payload = rpe012_report_payload()

    out = Path("artifacts/rpe012")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "projection-maturity-sample.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("summary=" + json.dumps(payload["summary"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))


if __name__ == "__main__":
    main()
