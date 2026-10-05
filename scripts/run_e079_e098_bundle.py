import json
from pathlib import Path

from market_microcosm.phase_e079_e098 import phase_report_payload


def main() -> None:
    payload = phase_report_payload()
    out = Path("artifacts/phase-e079-e098")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "phase-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("all-promoted=" + str(payload["all_experiments_promoted"]))
    print("count=" + str(payload["experiment_count"]))


if __name__ == "__main__":
    main()
