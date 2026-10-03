from __future__ import annotations

from dataclasses import asdict
import json

from .meta_improvement import ClosedMetaRun, MetaImprovementResult


def meta_result_payload(result: MetaImprovementResult) -> dict:
    return {
        "winner": result.winner.name,
        "meta_scenario_ids": list(result.meta_scenario_ids),
        "scores": [asdict(s) for s in result.scores],
        "inner": [
            {
                "incumbent": r.incumbent.name,
                "challenger": r.challenger.name,
                "promoted": r.decision.promoted,
                "reasons": list(r.decision.reasons),
                "kernel_size": len(r.viability.kernel),
                "kernel_iterations": r.viability.iterations,
                "discovery_run_id": r.discovery_manifest.run_id,
                "promotion_run_id": r.promotion_manifest.run_id,
                "incumbent_holdout": asdict(r.incumbent_holdout),
                "challenger_holdout": asdict(r.challenger_holdout),
            }
            for r in result.inner_results
        ],
    }


def meta_result_json(result: MetaImprovementResult) -> str:
    return json.dumps(meta_result_payload(result), indent=2, sort_keys=True)


def closed_meta_json(result: ClosedMetaRun) -> str:
    payload = {
        "final_winner": result.final_winner.name,
        "converged": result.converged,
        "generation_count": len(result.generations),
        "generations": [meta_result_payload(g) for g in result.generations],
    }
    return json.dumps(payload, indent=2, sort_keys=True)
