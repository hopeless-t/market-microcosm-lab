import json
from pathlib import Path

from market_microcosm.adaptive_sampling import adaptive_sampling_report_payload


def main() -> None:
    source = Path("artifacts/e014/interaction-surface-report.json")
    e014 = json.loads(source.read_text())
    payload = adaptive_sampling_report_payload(e014)

    out = Path("artifacts/e015")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "adaptive-boundary-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    print("aggregate=" + json.dumps(payload["aggregate"], sort_keys=True))
    print("promotion-gate=" + json.dumps(payload["promotion_gate"], sort_keys=True))
    print(f"promoted={payload['promoted']}")


if __name__ == "__main__":
    main()
