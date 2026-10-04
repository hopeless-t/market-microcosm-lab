import json
from pathlib import Path

from market_microcosm.failure_domain_diversity import failure_domain_report_payload


def main() -> None:
    payload = failure_domain_report_payload()

    out = Path("artifacts/e022")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "failure-domain-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "topologies="
        + json.dumps(payload["topologies"], sort_keys=True)
    )
    print(
        "comparison="
        + json.dumps(payload["comparison"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(
        f"promoted-rule={payload['promoted_failure_domain_rule']}"
    )


if __name__ == "__main__":
    main()
