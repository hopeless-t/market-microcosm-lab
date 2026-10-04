import json
from pathlib import Path

from market_microcosm.heterogeneous_audit_allocation import (
    heterogeneous_audit_report_payload,
)


def main() -> None:
    payload = heterogeneous_audit_report_payload()

    out = Path("artifacts/e060")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "heterogeneous-audit-allocation-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "allocation="
        + json.dumps(payload["allocation"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_allocation_rule']}")


if __name__ == "__main__":
    main()
