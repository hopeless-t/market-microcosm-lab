import json
from pathlib import Path

from market_microcosm.human_delivery_cost import (
    human_delivery_cost_report_payload,
)


def main() -> None:
    payload = human_delivery_cost_report_payload()

    out = Path("artifacts/e034")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "human-delivery-cost-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print(
        "witness="
        + json.dumps(payload["finite_cost_witness"], sort_keys=True)
    )
    print(f"promoted-rule={payload['promoted_delivery_rule']}")


if __name__ == "__main__":
    main()
