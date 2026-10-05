import json
from pathlib import Path

from market_microcosm.metric_definition_drift import (
    metric_definition_drift_report_payload,
)


def main() -> None:
    payload = metric_definition_drift_report_payload()

    out = Path("artifacts/e027")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "metric-definition-drift-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "naive="
        + json.dumps(payload["naive_headline_growth"], sort_keys=True)
    )
    print(
        "authority="
        + json.dumps(payload["growth_authority"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_metric_rule']}")


if __name__ == "__main__":
    main()
