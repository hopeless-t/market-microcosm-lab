import json
from pathlib import Path

from market_microcosm.exit_residual_value import residual_value_report_payload


def main() -> None:
    payload = residual_value_report_payload()
    out = Path("artifacts/e095")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "exit-residual-value-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("state=" + json.dumps(payload["exit_value_state"], sort_keys=True))


if __name__ == "__main__":
    main()
