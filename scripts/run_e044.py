import json
from pathlib import Path

from market_microcosm.robust_abstention import (
    robust_abstention_report_payload,
)


def main() -> None:
    payload = robust_abstention_report_payload()

    out = Path("artifacts/e044")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "robust-abstention-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "reference="
        + json.dumps(payload["reference"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_decision_rule']}")


if __name__ == "__main__":
    main()
