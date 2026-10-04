import json
from pathlib import Path

from market_microcosm.regional_complexity import (
    regional_complexity_report_payload,
)


def main() -> None:
    payload = regional_complexity_report_payload()

    out = Path("artifacts/e025")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "regional-complexity-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "selection="
        + json.dumps(payload["complexity_selection"], sort_keys=True)
    )
    print(
        "holdout="
        + json.dumps(payload["forward_holdout"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_regional_rule']}")


if __name__ == "__main__":
    main()
