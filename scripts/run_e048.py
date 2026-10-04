import json
from pathlib import Path

from market_microcosm.evidence_quorum import evidence_quorum_report_payload


def main() -> None:
    payload = evidence_quorum_report_payload()

    out = Path("artifacts/e048")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "evidence-quorum-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "reference="
        + json.dumps(payload["single_witness_reference"], sort_keys=True)
    )
    print(
        "conflict="
        + json.dumps(payload["conflict_reference"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_quorum_rule']}")


if __name__ == "__main__":
    main()
