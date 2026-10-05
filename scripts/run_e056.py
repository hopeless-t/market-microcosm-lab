import json
from pathlib import Path

from market_microcosm.measurement_failure_domains import (
    measurement_failure_domain_report_payload,
)


def main() -> None:
    payload = measurement_failure_domain_report_payload()

    out = Path("artifacts/e056")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "measurement-failure-domain-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "counterexample="
        + json.dumps(
            payload["bad_common_mode_counterexample"],
            sort_keys=True,
        )
    )
    print(
        "diversified="
        + json.dumps(
            payload["diversified_root_fault_check"],
            sort_keys=True,
        )
    )
    print(f"promoted-rule={payload['promoted_domain_rule']}")


if __name__ == "__main__":
    main()
