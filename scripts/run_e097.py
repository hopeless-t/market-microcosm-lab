import json
from pathlib import Path

from market_microcosm.transient_kpi_stress_negative_control import (
    transient_kpi_stress_report_payload,
)


def main() -> None:
    payload = transient_kpi_stress_report_payload()
    out = Path("artifacts/e097")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "transient-kpi-stress-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("transitions=" + json.dumps(payload["transitions"], sort_keys=True))
    print("decision=" + json.dumps(payload["holdout_aware_rule"], sort_keys=True))


if __name__ == "__main__":
    main()
