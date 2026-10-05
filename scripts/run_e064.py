import json
from pathlib import Path

from market_microcosm.prospective_evidence_cutoff import (
    prospective_evidence_cutoff_report_payload,
)


def main() -> None:
    payload = prospective_evidence_cutoff_report_payload()

    out = Path("artifacts/e064")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "prospective-evidence-cutoff-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")

    print(path)
    print(
        "availability="
        + json.dumps(payload["availability"], sort_keys=True, default=str)
    )
    print(
        "features="
        + json.dumps(payload["feature_sets"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_cutoff_rule']}")


if __name__ == "__main__":
    main()
