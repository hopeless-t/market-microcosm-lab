import json
from pathlib import Path

from market_microcosm.public_warning_sufficiency import (
    public_evidence_sufficiency_report_payload,
)


def main() -> None:
    payload = public_evidence_sufficiency_report_payload()

    out = Path("artifacts/e065")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "public-warning-sufficiency-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("coverage=" + json.dumps(payload["coverage"], sort_keys=True))
    print(
        "decision="
        + json.dumps(payload["prospective_warning"], sort_keys=True)
    )
    print(
        f"promoted-rule={payload['promoted_sufficiency_rule']}"
    )


if __name__ == "__main__":
    main()
