import json
from pathlib import Path

from market_microcosm.coupled_audit_bundles import (
    coupled_audit_bundle_report_payload,
)


def main() -> None:
    payload = coupled_audit_bundle_report_payload()

    out = Path("artifacts/e061")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "coupled-audit-bundle-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "cover="
        + json.dumps(payload["bundle_cover"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_bundle_rule']}")


if __name__ == "__main__":
    main()
