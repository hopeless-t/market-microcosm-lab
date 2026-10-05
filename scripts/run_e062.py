import json
from pathlib import Path

from market_microcosm.audit_evidence_failure_domains import (
    audit_evidence_failure_domain_report_payload,
)


def main() -> None:
    payload = audit_evidence_failure_domain_report_payload()

    out = Path("artifacts/e062")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "audit-evidence-failure-domain-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "robust-cover="
        + json.dumps(payload["robust_cover"], sort_keys=True)
    )
    print(
        "e061-authority="
        + payload[
            "e061_cost_authority_after_evidence_failure_model"
        ]
    )
    print(
        f"promoted-rule={payload['promoted_failure_domain_rule']}"
    )


if __name__ == "__main__":
    main()
