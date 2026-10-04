import json
from pathlib import Path

from market_microcosm.rolling_metric_nonidentifiability import (
    rolling_metric_nonidentifiability_report_payload,
)


def main() -> None:
    payload = rolling_metric_nonidentifiability_report_payload()

    out = Path("artifacts/e040")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "rolling-metric-nonidentifiability-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "ambiguity="
        + json.dumps(payload["exact_ambiguity"], sort_keys=True)
    )
    print(
        f"promoted-rule={payload['promoted_identifiability_rule']}"
    )


if __name__ == "__main__":
    main()
