import json
from pathlib import Path

from market_microcosm.temporal_evidence import temporal_evidence_report_payload


def main() -> None:
    payload = temporal_evidence_report_payload()

    out = Path("artifacts/e047")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "temporal-evidence-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "search="
        + json.dumps(payload["candidate_search"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_temporal_rule']}")


if __name__ == "__main__":
    main()
