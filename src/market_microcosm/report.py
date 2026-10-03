from __future__ import annotations

from dataclasses import asdict
import json

from .meta_improvement import MetaImprovementResult


def meta_result_json(result: MetaImprovementResult) -> str:
    payload = {
        "winner": result.winner.name,
        "scores": [asdict(s) for s in result.scores],
        "inner": [
            {
                "incumbent": r.incumbent.name,
                "challenger": r.challenger.name,
                "promoted": r.decision.promoted,
                "reasons": list(r.decision.reasons),
                "kernel_size": len(r.viability.kernel),
                "kernel_iterations": r.viability.iterations,
                "incumbent_holdout": asdict(r.incumbent_holdout),
                "challenger_holdout": asdict(r.challenger_holdout),
            }
            for r in result.inner_results
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)
