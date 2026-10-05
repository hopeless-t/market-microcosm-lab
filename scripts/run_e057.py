import json
from pathlib import Path

from market_microcosm.recursive_measurement_lineage import (
    recursive_measurement_lineage_report_payload,
)


def main() -> None:
    payload = recursive_measurement_lineage_report_payload()

    out = Path("artifacts/e057")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "recursive-measurement-lineage-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("reference=" + json.dumps(payload["reference"], sort_keys=True))
    print(
        "e056-authority="
        + payload["e056_measurement_domain_authority_after_discovery"]
    )
    print(f"promoted-rule={payload['promoted_recursive_rule']}")


if __name__ == "__main__":
    main()
