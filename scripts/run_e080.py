import json
from pathlib import Path

from market_microcosm.reporting_kernel_state import reporting_kernel_report_payload


def main() -> None:
    payload = reporting_kernel_report_payload()
    out = Path("artifacts/e080")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "reporting-kernel-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("before=" + json.dumps(payload["before_kernel"], sort_keys=True))
    print("after=" + json.dumps(payload["after_kernel"], sort_keys=True))
    print("promoted-rule=" + str(payload["promoted_kernel_rule"]))


if __name__ == "__main__":
    main()
