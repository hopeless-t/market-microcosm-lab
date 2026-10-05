import json
from pathlib import Path

from market_microcosm.warning_monte_carlo import (
    monte_carlo_warning_report_payload,
)


def main() -> None:
    payload = monte_carlo_warning_report_payload()

    out = Path("artifacts/e036")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "warning-monte-carlo-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("selection=" + json.dumps(payload["selection"], sort_keys=True))
    print(
        "holdout="
        + json.dumps(payload["holdout_scores"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_warning_search_rule']}")


if __name__ == "__main__":
    main()
