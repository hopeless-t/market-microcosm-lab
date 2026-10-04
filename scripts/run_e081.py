import json
from pathlib import Path

from market_microcosm.disclosure_selection_bias import (
    disclosure_selection_bias_report_payload,
)


def main() -> None:
    payload = disclosure_selection_bias_report_payload()
    out = Path("artifacts/e081")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "disclosure-selection-bias-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("complete-case=" + json.dumps(payload["complete_case_benchmark"], sort_keys=True))
    print("event-aware=" + json.dumps(payload["event_aware_benchmark"], sort_keys=True))


if __name__ == "__main__":
    main()
