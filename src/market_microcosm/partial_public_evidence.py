from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations

AXES=("cash_collection_gap","fully_loaded_delivery_margin","market_headroom","downstream_funnel_success","strategic_exit_value_gap")
RANK={"absent":0,"partial":1,"direct":2}

@dataclass(frozen=True)
class PublicArtifact:
    artifact_id:str
    cost:int
    support:tuple[tuple[str,str],...]
    observation:str
    source_page:str
    def support_map(self)->dict[str,str]:
        return dict(self.support)

def public_artifacts()->tuple[PublicArtifact,...]:
    return (
        PublicArtifact("q3-financial-summary",1,(("fully_loaded_delivery_margin","partial"),),"FY2025 Q3 consolidated gross margin is 38.4%, but this mixes segments and does not isolate recurring SaaS human delivery burden or per-account fully-loaded delivery margin.","FY2025 Q3 supplemental material p.4"),
        PublicArtifact("q3-operating-profit-bridge",1,(("fully_loaded_delivery_margin","partial"),),"The operating-profit bridge identifies development outsourcing / service-development cost pressure but not product-level recurring delivery cost.","FY2025 Q3 supplemental material p.6"),
        PublicArtifact("q3-market-environment",1,(("market_headroom","partial"),),"The company publishes TAM/SAM/SOM-style context including an approximately 800bn JPY SOM construction, but this is not direct remaining company-specific obtainable headroom.","FY2025 Q3 supplemental material p.28"),
        PublicArtifact("q3-kpi-pages",1,tuple(),"ARR, churn, contracts, and ARPA are valid observations but do not directly satisfy the five structural warning axes.","FY2025 Q3 supplemental material pp.12-13"),
    )

def portfolio_coverage(selected:tuple[PublicArtifact,...])->dict:
    status={a:"absent" for a in AXES}
    for artifact in selected:
        for axis,support in artifact.support:
            if RANK[support]>RANK[status[axis]]: status[axis]=support
    direct=[a for a in AXES if status[a]=="direct"]
    partial=[a for a in AXES if status[a]=="partial"]
    absent=[a for a in AXES if status[a]=="absent"]
    return {"axis_status":status,"direct_axes":direct,"partial_axes":partial,"absent_axes":absent,"direct_count":len(direct),"partial_count":len(partial),"absent_count":len(absent),"direct_contract_complete":len(direct)==len(AXES)}

def exact_public_evidence_portfolio()->dict:
    catalog=public_artifacts()
    rows=[]
    for n in range(len(catalog)+1):
        for selected in combinations(catalog,n):
            rows.append({"artifact_ids":sorted(a.artifact_id for a in selected),"artifact_count":len(selected),"total_cost":sum(a.cost for a in selected),"coverage":portfolio_coverage(selected)})
    best=max(x["coverage"]["direct_count"] for x in rows); rows=[x for x in rows if x["coverage"]["direct_count"]==best]
    best=max(x["coverage"]["partial_count"] for x in rows); rows=[x for x in rows if x["coverage"]["partial_count"]==best]
    best=min(x["total_cost"] for x in rows); rows=[x for x in rows if x["total_cost"]==best]
    best=min(x["artifact_count"] for x in rows); rows=[x for x in rows if x["artifact_count"]==best]
    selected=min(rows,key=lambda x:x["artifact_ids"])
    return {"catalog":[{"artifact_id":a.artifact_id,"cost":a.cost,"support":a.support_map(),"observation":a.observation,"source_page":a.source_page} for a in catalog],"candidate_count":16,"selected":selected}

def partial_public_evidence_report_payload()->dict:
    result=exact_public_evidence_portfolio(); selected=result["selected"]; coverage=selected["coverage"]
    gates={
        "e065_zero_direct_coverage_is_confirmed":coverage["direct_count"]==0,
        "public_q3_material_contains_two_partial_axes":coverage["partial_count"]==2,
        "partial_axes_are_delivery_margin_and_market_headroom":coverage["partial_axes"]==["fully_loaded_delivery_margin","market_headroom"],
        "three_axes_remain_absent":coverage["absent_count"]==3,
        "minimum_partial_portfolio_cost_is_two":selected["total_cost"]==2,
        "minimum_portfolio_uses_financial_and_market_pages":selected["artifact_ids"]==["q3-financial-summary","q3-market-environment"],
        "partial_does_not_satisfy_direct_contract":coverage["direct_contract_complete"] is False,
        "prospective_warning_remains_abstain":True,
    }
    return {
        "experiment":"E066",
        "source":{"provider":"BBD Initiative Inc.","decision_cutoff":"2025-08-14","observations":{"consolidated_gross_margin_pct":38.4,"som_target_market_jpy_billions":800.0}},
        "portfolio":result,
        "e065_direct_coverage_authority":"CONFIRMED",
        "e065_information_granularity_authority":"REFINED",
        "prospective_warning":{"status":"ABSTAIN","reason":"DIRECT_FEATURE_CONTRACT_INCOMPLETE","partial_evidence_may_prioritize_acquisition":True,"partial_evidence_may_be_promoted_to_direct":False},
        "promotion_gate":gates,
        "promoted_observability_rule":"public-warning-evidence-separates-direct-partial-absent-v1" if all(gates.values()) else None,
        "model_update":"Public observability is three-valued. Partial evidence can constrain hypotheses and prioritize acquisition, but cannot silently satisfy a direct structural feature contract.",
        "limitations":"Partial classifications are semantic evidence judgments, not causal identification."
    }
