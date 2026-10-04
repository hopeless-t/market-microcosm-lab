import json
from pathlib import Path

from market_microcosm.governance_checkpoint_timeline import (
    governance_checkpoint_report_payload,
)


def main() -> None:
    payload = governance_checkpoint_report_payload()
    out = Path("artifacts/e087")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "governance-checkpoint-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("timeline=" + json.dumps(payload["timeline"], sort_keys=True))


if __name__ == "__main__":
    main()
