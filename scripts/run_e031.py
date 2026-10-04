import json
from pathlib import Path

from market_microcosm.pmf_proxy_guard import pmf_proxy_guard_report_payload


def main() -> None:
    payload = pmf_proxy_guard_report_payload()

    out = Path("artifacts/e031")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "pmf-proxy-guard-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "proxy-trap="
        + json.dumps(payload["finite_proxy_trap"], sort_keys=True)
    )
    print(
        "promotion-gate="
        + json.dumps(payload["promotion_gate"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_proxy_rule']}")


if __name__ == "__main__":
    main()
