import json
from pathlib import Path

from market_microcosm.warning_structural_drift import (
    structural_drift_report_payload,
)


def main() -> None:
    payload = structural_drift_report_payload()

    out = Path("artifacts/e037")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "warning-structural-drift-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "legacy="
        + json.dumps(payload["legacy_e036_score"], sort_keys=True)
    )
    print(
        "repaired="
        + json.dumps(payload["interaction_aware_score"], sort_keys=True)
    )
    print(f"legacy-authority={payload['legacy_authority_after_shift']}")
    print(f"promoted-rule={payload['promoted_repair_rule']}")


if __name__ == "__main__":
    main()
