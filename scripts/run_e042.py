import json
from pathlib import Path

from market_microcosm.reporting_resolution import (
    reporting_resolution_report_payload,
)


def main() -> None:
    payload = reporting_resolution_report_payload()

    out = Path("artifacts/e042")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "reporting-resolution-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "reassessment="
        + json.dumps(payload["e038_reassessment"], sort_keys=True)
    )
    print(
        "legacy-authority="
        + payload["legacy_e038_sub1pct_precision_authority"]
    )
    print(f"promoted-rule={payload['promoted_resolution_rule']}")


if __name__ == "__main__":
    main()
