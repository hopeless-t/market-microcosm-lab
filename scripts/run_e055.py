import json
from pathlib import Path

from market_microcosm.redundant_probe_synthesis import (
    redundancy_synthesis_report_payload,
)


def main() -> None:
    payload = redundancy_synthesis_report_payload()

    out = Path("artifacts/e055")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "redundant-probe-synthesis-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "synthesis="
        + json.dumps(payload["synthesis"], sort_keys=True)
    )
    print(
        "decode="
        + json.dumps(payload["exhaustive_decode"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_redundancy_rule']}")


if __name__ == "__main__":
    main()
