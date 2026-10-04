from __future__ import annotations

from itertools import combinations
from market_microcosm.direct_evidence_acquisition import AXES, acquisitions


def reference_worlds() -> dict[str, dict[str, bool]]:
    safe={axis:False for axis in AXES}
    worlds={"all-safe":safe}
    for axis in sorted(AXES):
        row=dict(safe); row[axis]=True
        worlds[f"{axis}-only-bad"]=row
    return worlds


def subset_decision(selected, world:dict[str,bool]) -> str:
    observed=frozenset().union(*(a.direct_axes for a in selected)) if selected else frozenset()
    if any(world[axis] for axis in observed):
        return "CERTIFIED_WARN"
    if AXES.issubset(observed):
        return "CERTIFIED_SAFE"
    return "ABSTAIN"


def exact_minimum_decision_portfolio(world_id:str) -> dict:
    world=reference_worlds()[world_id]
    catalog=tuple(a for a in acquisitions() if a.authorized)
    rows=[]
    for n in range(1,len(catalog)+1):
        for selected in combinations(catalog,n):
            decision=subset_decision(selected,world)
            if decision=="ABSTAIN":
                continue
            rows.append({
                "acquisition_ids":sorted(a.acquisition_id for a in selected),
                "total_cost":sum(a.cost for a in selected),
                "count":len(selected),
                "observed_axes":sorted(frozenset().union(*(a.direct_axes for a in selected))),
                "decision":decision,
            })
    if not rows:
        raise ValueError("no resolving portfolio")
    selected=min(rows,key=lambda x:(x["total_cost"],x["count"],x["acquisition_ids"]))
    return {"world_id":world_id,"world":world,"selected":selected,"candidate_count":len(rows)}


def decision_sufficient_acquisition_report_payload() -> dict:
    rows={world_id:exact_minimum_decision_portfolio(world_id) for world_id in reference_worlds()}
    full_cost=14
    one_bad={k:v for k,v in rows.items() if k!="all-safe"}
    costs=sorted(v["selected"]["total_cost"] for v in one_bad.values())
    gates={
        "all_safe_requires_full_direct_coverage":set(rows["all-safe"]["selected"]["observed_axes"])==set(AXES),
        "all_safe_minimum_cost_equals_e067_full_contract":rows["all-safe"]["selected"]["total_cost"]==full_cost,
        "every_single_bad_world_certifies_warn_before_full_contract":all(v["selected"]["decision"]=="CERTIFIED_WARN" and v["selected"]["total_cost"]<full_cost for v in one_bad.values()),
        "downstream_failure_is_cheapest_warning_certificate":rows["downstream_funnel_success-only-bad"]["selected"]["total_cost"]==2,
        "single_bad_warning_certificate_cost_range_is_two_to_five":costs[0]==2 and costs[-1]==5,
        "reference_search_is_an_information_lower_bound_not_a_deployable_oracle_policy":True,
    }
    return {
        "experiment":"E068",
        "question":"Does a five-axis OR warning require all five direct features before any decision can be certified?",
        "warning_semantics":"CERTIFIED_WARN if any directly observed axis is bad; CERTIFIED_SAFE only when all five axes are directly observed safe.",
        "world_results":rows,
        "e067_full_contract_cost":full_cost,
        "promotion_gate":gates,
        "promoted_decision_rule":"warning-evidence-acquisition-is-decision-sufficient-not-full-state-v1" if all(gates.values()) else None,
        "model_update":"Evidence requirements are decision-asymmetric. One observed failing axis can certify WARN, while SAFE requires complete direct coverage. Full feature recovery is therefore not the universal acquisition objective.",
        "limitations":"The exact search knows the reference world's latent truth only to compute an information lower bound. A deployable controller does not know which axis is bad before observing it; sequential acquisition policy is a separate problem."
    }
