import json
from pathlib import Path

from market_microcosm.ecology import MarketWorld, default_mechanisms
from market_microcosm.sensitivity import decomposition_report_payload


def main() -> None:
    payload = decomposition_report_payload(
        base_world=MarketWorld(),
        mechanisms=default_mechanisms(),
    )

    out = Path("artifacts/e013")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "pressure-decomposition-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("knees=" + json.dumps(payload["knees"], sort_keys=True))

    failure_modes = {}
    for biopsy in payload["biopsies"]:
        key = f"{biopsy['axis']}::{biopsy['mechanism_name']}"
        failure_modes[key] = {
            "failed": biopsy["failed"],
            "failure_month": biopsy["failure_month"],
            "failure_reasons": biopsy["failure_reasons"],
        }

    print("failure-modes=" + json.dumps(failure_modes, sort_keys=True))


if __name__ == "__main__":
    main()
