import json
from pathlib import Path

from market_microcosm.active_sensing import (
    active_sensing_report_payload,
)


def main() -> None:
    payload = active_sensing_report_payload()

    out = Path("artifacts/e045")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "active-sensing-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "search="
        + json.dumps(payload["candidate_search"], sort_keys=True)
    )
    print(
        f"promoted-rule={payload['promoted_active_sensing_rule']}"
    )


if __name__ == "__main__":
    main()
