import json
from pathlib import Path

from market_microcosm.withdrawal_governance_action import (
    withdrawal_governance_report_payload,
)


def main() -> None:
    payload = withdrawal_governance_report_payload()
    out = Path("artifacts/e086")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "withdrawal-governance-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("actions=" + json.dumps(payload["actions"], sort_keys=True))


if __name__ == "__main__":
    main()
