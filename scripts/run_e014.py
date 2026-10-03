import json
from pathlib import Path

from market_microcosm.ecology import MarketWorld, default_mechanisms
from market_microcosm.interactions import interaction_report_payload


def main() -> None:
    payload = interaction_report_payload(
        base_world=MarketWorld(),
        mechanisms=default_mechanisms(),
    )

    out = Path("artifacts/e014")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "interaction-surface-report.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(path)
    compact = {}
    for pair, mechanisms in payload["summaries"].items():
        compact[pair] = {
            mechanism: {
                "frontier": row["frontier"],
                "interaction_only_cells": row["interaction_only_cells"],
                "max_excess_additive": round(
                    row["max_survival_loss_excess_over_additive"], 3
                ),
            }
            for mechanism, row in mechanisms.items()
        }
    print("interaction-summary=" + json.dumps(compact, sort_keys=True))


if __name__ == "__main__":
    main()
