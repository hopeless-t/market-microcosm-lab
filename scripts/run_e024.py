from __future__ import annotations

import argparse
import json
from pathlib import Path

from market_microcosm.decision_relevance_holdout import (
    build_cross_loop_certificate,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--e015", type=Path, required=True)
    parser.add_argument("--e016", type=Path, required=True)
    parser.add_argument("--e017", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--workflow-run-id", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    certificate = build_cross_loop_certificate(
        json.loads(args.e015.read_text(encoding="utf-8")),
        json.loads(args.e016.read_text(encoding="utf-8")),
        json.loads(args.e017.read_text(encoding="utf-8")),
        source_commit=args.source_commit,
        workflow_run_id=args.workflow_run_id,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(certificate, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "qualified": certificate["qualification"]["qualified"],
        "adaptive_queries": certificate["e015"]["adaptive_queries"],
        "exhaustive_queries": certificate["e015"]["exhaustive_queries"],
        "e015_savings": certificate["e015"]["query_savings_fraction"],
        "adversarial_accuracy": certificate["e016"]["adversarial_accuracy"],
        "violations": certificate["e016"]["monotonicity_violation_count"],
        "post_audit_mode": certificate["e016"]["post_audit_mode"],
        "stable_e017_savings": certificate["e017"]["stable_query_savings_fraction"],
        "auto_apply_allowed": certificate["auto_apply_allowed"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
