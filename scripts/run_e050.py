import json
from pathlib import Path

from market_microcosm.evidence_lineage import evidence_lineage_report_payload


def main() -> None:
    payload = evidence_lineage_report_payload()

    out = Path("artifacts/e050")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "evidence-lineage-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "hidden="
        + json.dumps(payload["hidden_root_reference"], sort_keys=True)
    )
    print(
        "repair="
        + json.dumps(payload["lineage_diversified_repair"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_lineage_rule']}")


if __name__ == "__main__":
    main()
