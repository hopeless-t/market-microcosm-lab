import json
from pathlib import Path

from market_microcosm.governance_evidence_availability import (
    governance_evidence_availability_report_payload,
)


def main() -> None:
    payload = governance_evidence_availability_report_payload()
    out = Path("artifacts/e088")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "governance-evidence-availability-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("checks=" + json.dumps(payload["public_authority_checks"], sort_keys=True))


if __name__ == "__main__":
    main()
