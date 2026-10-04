import json
from pathlib import Path

from market_microcosm.funnel_proxy import funnel_proxy_report_payload


def main() -> None:
    payload = funnel_proxy_report_payload()

    out = Path("artifacts/e033")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "funnel-proxy-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "observations="
        + json.dumps(payload["empirical_observations"], sort_keys=True)
    )
    print(
        "witness="
        + json.dumps(payload["finite_proxy_witness"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_funnel_rule']}")


if __name__ == "__main__":
    main()
