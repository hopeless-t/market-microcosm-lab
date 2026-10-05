import json
from pathlib import Path

from market_microcosm.censored_accuracy_interval import (
    censored_accuracy_interval_report_payload,
)


def main() -> None:
    payload = censored_accuracy_interval_report_payload()
    out = Path("artifacts/e084")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "censored-accuracy-interval-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("interval=" + json.dumps(payload["accuracy_interval"], sort_keys=True))
    print("decisions=" + json.dumps(payload["threshold_decisions"], sort_keys=True))


if __name__ == "__main__":
    main()
