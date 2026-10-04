import json
from pathlib import Path

from market_microcosm.censored_evaluation_guard import (
    censored_evaluation_report_payload,
)


def main() -> None:
    payload = censored_evaluation_report_payload()
    out = Path("artifacts/e083")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "censored-evaluation-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("naive=" + json.dumps(payload["naive_complete_case"], sort_keys=True))
    print("aware=" + json.dumps(payload["coverage_aware"], sort_keys=True))


if __name__ == "__main__":
    main()
