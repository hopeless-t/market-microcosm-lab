import json
from pathlib import Path

from market_microcosm.ecology import MarketWorld, default_mechanisms
from market_microcosm.pressure import (
    pressure_ladder,
    pressure_report_payload,
    scan_pressure,
)


def main() -> None:
    world = MarketWorld()
    mechanisms = default_mechanisms()
    points = pressure_ladder()
    results = scan_pressure(
        base_world=world,
        mechanisms=mechanisms,
        points=points,
    )
    payload = pressure_report_payload(
        results=results,
        mechanisms=mechanisms,
        points=points,
    )

    out = Path("artifacts/e011")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "pressure-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("knees=" + json.dumps(payload["knees"], sort_keys=True))
    failed = {
        x["mechanism_name"]: x["failure_month"]
        for x in payload["biopsies"]
        if x["failed"]
    }
    print("failure-months=" + json.dumps(failed, sort_keys=True))


if __name__ == "__main__":
    main()
