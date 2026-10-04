import json
from pathlib import Path

from market_microcosm.kpi_withdrawal_reason_typing import (
    withdrawal_reason_report_payload,
)


def main() -> None:
    payload = withdrawal_reason_report_payload()
    out = Path("artifacts/e082")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "kpi-withdrawal-reason-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("scalar=" + json.dumps(payload["scalar_classifier"], sort_keys=True))
    print("typed=" + json.dumps(payload["typed_classifier"], sort_keys=True))


if __name__ == "__main__":
    main()
