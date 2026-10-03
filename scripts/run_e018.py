import json
from pathlib import Path

from market_microcosm.audit_portfolio import audit_portfolio_report_payload


def main() -> None:
    payload = audit_portfolio_report_payload()

    out = Path("artifacts/e018")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "audit-portfolio-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("aggregate=" + json.dumps(payload["aggregate"], sort_keys=True))
    print(
        "greedy-trap="
        + json.dumps(payload["greedy_trap"], sort_keys=True)
    )
    print(
        "infeasible="
        + json.dumps(payload["infeasible_mandatory_case"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-scheduler={payload['promoted_scheduler']}")


if __name__ == "__main__":
    main()
