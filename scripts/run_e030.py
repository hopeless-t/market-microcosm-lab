import json
from pathlib import Path

from market_microcosm.churn_semantics import churn_semantics_report_payload


def main() -> None:
    payload = churn_semantics_report_payload()

    out = Path("artifacts/e030")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "churn-semantics-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "change="
        + json.dumps(payload["endpoint_change"], sort_keys=True)
    )
    print(
        "counterexample="
        + json.dumps(payload["sign_counterexample"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_churn_rule']}")


if __name__ == "__main__":
    main()
