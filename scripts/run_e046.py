import json
from pathlib import Path

from market_microcosm.authority_constrained_sensing import (
    authority_constrained_active_sensing_report_payload,
)


def main() -> None:
    payload = authority_constrained_active_sensing_report_payload()

    out = Path("artifacts/e046")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "authority-constrained-sensing-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "search="
        + json.dumps(payload["candidate_search"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_authority_rule']}")


if __name__ == "__main__":
    main()
