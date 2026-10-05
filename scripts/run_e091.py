import json
from pathlib import Path

from market_microcosm.replacement_kpi_bridge import (
    replacement_kpi_bridge_report_payload,
)


def main() -> None:
    payload = replacement_kpi_bridge_report_payload()
    out = Path("artifacts/e091")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "replacement-kpi-bridge-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("bridge=" + json.dumps(payload["old_to_replacement_bridge"], sort_keys=True))


if __name__ == "__main__":
    main()
