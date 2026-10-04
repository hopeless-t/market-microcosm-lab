import json
from pathlib import Path

from market_microcosm.post_exit_profitability import (
    post_exit_profitability_report_payload,
)


def main() -> None:
    payload = post_exit_profitability_report_payload()
    out = Path("artifacts/e090")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "post-exit-profitability-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("comparison=" + json.dumps(payload["comparison"], sort_keys=True))
    print("scalars=" + json.dumps(payload["scalar_evaluations"], sort_keys=True))


if __name__ == "__main__":
    main()
