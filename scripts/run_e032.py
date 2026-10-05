import json
from pathlib import Path

from market_microcosm.cash_conversion_lag import (
    cash_conversion_lag_report_payload,
)


def main() -> None:
    payload = cash_conversion_lag_report_payload()

    out = Path("artifacts/e032")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "cash-conversion-lag-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "warning="
        + json.dumps(payload["warning_comparison"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_liquidity_rule']}")


if __name__ == "__main__":
    main()
