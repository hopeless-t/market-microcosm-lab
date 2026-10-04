import json
from pathlib import Path

from market_microcosm.lineage_probe_portfolio import (
    minimum_probe_portfolio_report_payload,
)


def main() -> None:
    payload = minimum_probe_portfolio_report_payload()

    out = Path("artifacts/e052")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "lineage-probe-portfolio-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("reference=" + json.dumps(payload["reference"], sort_keys=True))
    print(f"promoted-rule={payload['promoted_probe_rule']}")


if __name__ == "__main__":
    main()
