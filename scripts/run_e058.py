import json
from pathlib import Path

from market_microcosm.recursive_lineage_repair import (
    recursive_lineage_repair_report_payload,
)


def main() -> None:
    payload = recursive_lineage_repair_report_payload()

    out = Path("artifacts/e058")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "recursive-lineage-repair-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("synthesis=" + json.dumps(payload["synthesis"], sort_keys=True))
    print(
        "fault-check="
        + json.dumps(
            payload["single_provider_fault_check"],
            sort_keys=True,
        )
    )
    print(f"promoted-rule={payload['promoted_repair_rule']}")


if __name__ == "__main__":
    main()
