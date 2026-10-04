import json
from pathlib import Path

from market_microcosm.jooto_viability_counterexample import (
    jooto_viability_report_payload,
)


def main() -> None:
    payload = jooto_viability_report_payload()
    out = Path("artifacts/e093")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "jooto-viability-counterexample-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(path)
    print("naive=" + json.dumps(payload["naive_traction_classifier"], sort_keys=True))
    print("multi=" + json.dumps(payload["multi_axis_classifier"], sort_keys=True))


if __name__ == "__main__":
    main()
