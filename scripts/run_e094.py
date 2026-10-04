import json
from pathlib import Path

from market_microcosm.exit_runoff_state_machine import (
    exit_runoff_report_payload,
)


def main() -> None:
    payload = exit_runoff_report_payload()
    out = Path("artifacts/e094")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "exit-runoff-state-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("states=" + json.dumps(payload["states"], sort_keys=True))


if __name__ == "__main__":
    main()
