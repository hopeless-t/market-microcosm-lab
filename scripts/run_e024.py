import json
from pathlib import Path

from market_microcosm.empirical_evidence import empirical_evidence_report_payload


def main() -> None:
    payload = empirical_evidence_report_payload()

    out = Path("artifacts/e024")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "empirical-evidence-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("portfolio=" + json.dumps(payload["public_portfolio"], sort_keys=True))
    print("anchors=" + json.dumps(payload["anchors"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))
    print(f"promoted-rule={payload['promoted_evidence_rule']}")


if __name__ == "__main__":
    main()
