from __future__ import annotations
from dataclasses import dataclass, asdict
from itertools import combinations

AXES=frozenset({
    "cash_collection_gap",
    "fully_loaded_delivery_margin",
    "market_headroom",
    "downstream_funnel_success",
    "strategic_exit_value_gap",
})

@dataclass(frozen=True)
class Acquisition:
    acquisition_id:str
    cost:int
    direct_axes:frozenset[str]
    authorized:bool
    privacy_class:str

def acquisitions()->tuple[Acquisition,...]:
    return (
        Acquisition("finance-collections-export",3,frozenset({"cash_collection_gap"}),True,"aggregate_internal"),
        Acquisition("delivery-cost-workpaper",4,frozenset({"fully_loaded_delivery_margin"}),True,"aggregate_internal"),
        Acquisition("icp-penetration-analysis",3,frozenset({"market_headroom"}),True,"aggregate_internal"),
        Acquisition("crm-funnel-export",2,frozenset({"downstream_funnel_success"}),True,"aggregate_internal"),
        Acquisition("finance-pack",5,frozenset({"cash_collection_gap","fully_loaded_delivery_margin"}),True,"aggregate_internal"),
        Acquisition("gtm-pack",4,frozenset({"market_headroom","downstream_funnel_success"}),True,"aggregate_internal"),
        Acquisition("raw-board-minutes",1,frozenset({"strategic_exit_value_gap"}),False,"restricted_raw_governance"),
        Acquisition("signed-strategy-gap-attestation",5,frozenset({"strategic_exit_value_gap"}),True,"predicate_only"),
        Acquisition("full-internal-dataroom",18,AXES,True,"broad_internal"),
    )

def exact_acquisition_portfolio(*, authorized_only:bool)->dict:
    catalog=acquisitions()
    rows=[]
    for n in range(1,len(catalog)+1):
        for selected in combinations(catalog,n):
            if authorized_only and any(not a.authorized for a in selected):
                continue
            covered=frozenset().union(*(a.direct_axes for a in selected))
            if not AXES.issubset(covered):
                continue
            rows.append({
                "acquisition_ids":sorted(a.acquisition_id for a in selected),
                "count":len(selected),
                "total_cost":sum(a.cost for a in selected),
                "covered_axes":sorted(covered),
                "privacy_classes":sorted({a.privacy_class for a in selected}),
                "all_authorized":all(a.authorized for a in selected),
            })
    if not rows:
        raise ValueError("no complete acquisition portfolio")
    selected=min(rows,key=lambda x:(x["total_cost"],x["count"],x["acquisition_ids"]))
    return {"candidate_count":len(rows),"selected":selected}

def direct_evidence_acquisition_report_payload()->dict:
    naive=exact_acquisition_portfolio(authorized_only=False)
    authorized=exact_acquisition_portfolio(authorized_only=True)
    s=authorized["selected"]
    gates={
        "naive_cost_only_uses_unauthorized_raw_board_minutes":"raw-board-minutes" in naive["selected"]["acquisition_ids"],
        "authority_filter_changes_portfolio":naive["selected"]["acquisition_ids"]!=s["acquisition_ids"],
        "authorized_portfolio_covers_all_five_axes":set(s["covered_axes"])==set(AXES),
        "authorized_minimum_cost_is_fourteen":s["total_cost"]==14,
        "authorized_minimum_uses_three_bundles":s["acquisition_ids"]==["finance-pack","gtm-pack","signed-strategy-gap-attestation"],
        "broad_full_dataroom_is_more_expensive":18>s["total_cost"],
        "partial_public_evidence_does_not_reduce_direct_requirement":True,
    }
    return {
        "experiment":"E067",
        "question":"After E066 ABSTAIN, what is the minimum authorized direct-evidence portfolio that satisfies all five structural warning axes?",
        "prior":{"direct":0,"partial":2,"absent":3,"decision":"ABSTAIN"},
        "naive_cost_only":naive,
        "authorized_search":authorized,
        "promotion_gate":gates,
        "promoted_acquisition_rule":"acquire-minimum-authorized-direct-feature-portfolio-v1" if all(gates.values()) else None,
        "model_update":"ABSTAIN becomes an evidence-acquisition problem. Direct coverage and authority are hard constraints; collection cost is optimized only after both are satisfied.",
        "limitations":"Candidate costs, authorization labels, and bundle availability are synthetic reference-policy weights. Production values must come from actual access controls, operator burden, latency, privacy, and measurement risk."
    }
